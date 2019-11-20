import stripe
import re
import logging
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_429_TOO_MANY_REQUESTS, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_406_NOT_ACCEPTABLE,HTTP_500_INTERNAL_SERVER_ERROR
from stripe.error import InvalidRequestError, RateLimitError, CardError, AuthenticationError,APIError

from mvtheater.models import Matinees
from stripeapp.models import CreditCardInfo, Transaction
from stripeapp.serializers import CCardRequestSerializer, ChargeRequestSerializer, CreditCardInfoSerializer, \
    CreditCardTokenSerializer, ChargeResponseSerializer, TransactionSerializer, DetailedTransactionSerializer
stripe.api_key = settings.STRIPE_SECRET_KEY
NEXEMPT_URLS = [re.compile(settings.APPLY_URL.lstrip('/'))]

class PaymentMiddleware:
    def parse_credit_card_token_data(self,token_response,card_info_pk):
        """
        This method prepare the token data structure for CreditCardTokenSerializer.
        :param token_response:
        :param card_info_pk:
        :return: CreditCardToke(Model) Structure
        """
        return {
            "cc_info": card_info_pk,
            "client_ip": token_response["client_ip"],
            "created": token_response["created"],
            "token_id": token_response["id"],
            "livemode": token_response["livemode"],
            "object": token_response["object"],
            "type": token_response["type"],
            "used": token_response["used"],
        }
    def parse_charge_response_data(self,stripe_response,card_pk):
        """
        This method prepare the stripe_response data to be compatible with ChargeResponseSerializer
        :param stripe_response: Contains Stripe response information
        :param card_pk: fk with CreditCard Model
        :return: ChargeResponse Model Structure.
        """
        return {
            'charge_id': stripe_response['id'],
            'object': stripe_response['object'],
            'c_card': card_pk,
            'amount': stripe_response['amount'],
            'amount_refunded': stripe_response['amount_refunded'],
            'balance_transaction': stripe_response['balance_transaction'],
            'funding': stripe_response['source']['funding'],
            'currency': stripe_response['currency'],
            'description': stripe_response['description'],
            'paid': stripe_response['paid'],
            'payment_method': stripe_response['payment_method'],
            'status': stripe_response['status']
        }
    def get_credit_card_info_pk(self,card_id):
        """
        This methos find the card by the pk.
        :param card_id:
        :return: CreditCardInfo Object.
        """
        tmp_data = get_object_or_404(CreditCardInfo, id_card=card_id)
        return tmp_data
    def save_credit_card_token_date(self, token_response):
        """
        This method parse the token_response data into the CreditCardInfo and CreditCardToken Models.
        :param token_response:
        :return:
        """
        card_data = token_response.pop('card')
        card_data.id_card = card_data.pop('id')
        credit_card_info_serializer = CreditCardInfoSerializer(data=card_data)

        if credit_card_info_serializer.is_valid():
            #datos tarjeta
            card_info_object = credit_card_info_serializer.save()
            credit_card_token_data = self.parse_credit_card_token_data(token_response,card_info_object.pk)
            credit_card_token_serializer = CreditCardTokenSerializer(data=credit_card_token_data)
            if credit_card_token_serializer.is_valid():
                card_token_info = credit_card_token_serializer.save()
                return card_token_info
            else:
                return JsonResponse(
                    {"error": credit_card_info_serializer.errors,
                     "description": "Information provided does not match with CreditCardToken Fields."},
                    status=HTTP_406_NOT_ACCEPTABLE)
        else:
            return JsonResponse(
                {"error": credit_card_info_serializer.errors,
                 "description": "Information provided does not match with CreditCard Fields."},
                status=HTTP_406_NOT_ACCEPTABLE)
    def get_credit_card_token(self, request_data):
        """
        This method handle the Credit Card Request, simulate the Tokenization of the Credit card info,
        then save card token data  on DB.
        :param request_data: // this param contains Credit Card Request info-
        :return: card_token_data // this var hold the card token information
        """
        ccrequest_serializer = CCardRequestSerializer(data=request_data)
        if ccrequest_serializer.is_valid(raise_exception=True):
            ccrequest_object = ccrequest_serializer.save(request_data)
            stripe_response = stripe.Token.create(
                card={
                    'number': ccrequest_serializer.validated_data['cc_num'],
                    # the first 2 values are for the month and the last 2 for the year
                    'exp_month': ccrequest_serializer.validated_data['exp_date'][:2],
                    'exp_year': ccrequest_serializer.validated_data['exp_date'][2:],
                    'cvc': ccrequest_serializer.validated_data['cvv'],
                },)
            card_token_data = self.save_credit_card_token_date(stripe_response)
            card_token_data.rpk = ccrequest_object.pk
            return card_token_data
    def charge(self, request_data):
        """
        This method try to simulate the charge process, try to create Charge Request
        :param request_data: //Hold all charge info
        :return ChargeResponse Object:
        """
        charge_request_serializer = ChargeRequestSerializer(data=request_data)
        if charge_request_serializer.is_valid(raise_exception=True):
            charge_request_serializer.save()
            token_data = stripe.Token.retrieve(request_data['source'])
            stripe_response = stripe.Charge.create(amount=request_data['amount'],
                                                   currency=request_data['currency'],
                                                   card=token_data)
            card_info_pk = self.get_credit_card_info_pk(stripe_response['source']['id'])
            charge_response_object = self.parse_charge_response_data(stripe_response,card_info_pk.pk)
            charge_response_serializer = ChargeResponseSerializer(data=charge_response_object)
            if charge_response_serializer.is_valid():
                charge_object = charge_response_serializer.save()
                return charge_object
            else:
                return JsonResponse(
                    {"error": charge_response_serializer.errors,
                     "description": "Information returned by Stripe did not match with serializer."},
                    status=HTTP_406_NOT_ACCEPTABLE)
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        """
        This method will validate if the data matches with the models applying a specific logic;
        Based on the result it will handle a response or a HTTP error response.
        Only support POST request
        **Note:
            This method only affect an specific view.
        :param request: Contains the payment request information such as trans_id, cc_number, exp_date ,cvv and amount.
        :return: The method must return a Charge process result, if everything is correct otherwise it will return an HTTP error.
        """
        #Exemp root from the middleware
        path = request.path_info.lstrip('/')
        url_not_exempt = any(url.match(path) for url in NEXEMPT_URLS)

        if url_not_exempt:
            if request.method == 'POST':
                try:
                    request_data = json.loads(request.body)
                    #CHECK IF THERE ARE FREE SLOTS ON CINEMA AT AT SPECIFIC MATINEE
                    matinee_pk = request_data['matinee']
                    matinee = get_object_or_404(Matinees,pk = matinee_pk)
                    tickets_quantity = matinee.tickets.count()
                    if tickets_quantity < int(matinee.cinema.seating_capacity):
                        card_token_data = self.get_credit_card_token(request_data)
                        charge_response = self.charge({'amount':request_data['amount'],'source':card_token_data.token_id,'currency':'usd'})
                        transaction_serializer = TransactionSerializer(data = {'request_id':card_token_data.rpk,'response_id':charge_response.pk})
                        if transaction_serializer.is_valid(raise_exception=True):
                            transaction_object = transaction_serializer.save()
                            setattr(request, "transaction_pk", transaction_object.pk)
                            setattr(request, "matinee_pk", matinee_pk)
                    else:
                        setattr(request,'transaction_error',{'error':'This matinee have 0 tickets left. Try another one.'})
                except InvalidRequestError as error:
                    return JsonResponse({"error": str(error), "description": "Invalid parameters were provided to API"},
                        status=HTTP_400_BAD_REQUEST)
                except CardError as error:
                    return JsonResponse({"error": str(error), "description": "Invalid CreditCard information, does not match."},
                        status=HTTP_400_BAD_REQUEST)
                except RateLimitError as error:
                    return JsonResponse({"error": str(error), "description": "Too many request to the api in short time"},
                        status=HTTP_429_TOO_MANY_REQUESTS)
                except AuthenticationError as error:
                    return JsonResponse({"errors": str(error),"detail": "Authentication with API has failed",},
                        status=HTTP_401_UNAUTHORIZED)
                except APIError as error:
                    return JsonResponse({"errors": str(error),"detail": "API has failed",},
                        status=HTTP_401_UNAUTHORIZED)
                except Exception as validation_error:
                    return JsonResponse({"errors": str(validation_error), "detail": "Something went wrong during request", },
                                        status=HTTP_500_INTERNAL_SERVER_ERROR)
        response = self.get_response(request)
        return response