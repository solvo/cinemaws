from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
import json

from mvtheater.models import Matinees, Tickets, Clients
from stripeapp.models import Transaction
from stripeapp.serializers import DetailedTransactionSerializer

class PaymentRequestView(generics.GenericAPIView):

    """
    This class handle the request after the middleware is done. You can access the data set in the request.
    """
    def post(self, request):
        if hasattr(request,'transaction_error'):
            transaction_error = request.transaction_error
            return HttpResponse(transaction_error)
        if hasattr(request, 'transaction_pk'):
            transaction_pk = request.transaction_pk

        detailed_transaction_object = DetailedTransactionSerializer(Transaction.objects.get(pk=transaction_pk))
        matinee_pk = request.matinee_pk
        matinee = get_object_or_404(Matinees,pk = matinee_pk)
        new_ticket = Tickets.objects.create(matinee=matinee, transaction=Transaction.objects.get(pk=transaction_pk))
        if request.user.is_authenticated:
            new_ticket.client = Clients.objects.get(pk=request.user.pk)
            new_ticket.save()
        return JsonResponse({"ticket": str(new_ticket.matinee),
                             "request_id": detailed_transaction_object['request_id']['id'].value,
                             "transaction" : detailed_transaction_object['request_id']['trans_id'].value,
                             "card_num": detailed_transaction_object['request_id']['cc_num'].value,
                             "amount": detailed_transaction_object['request_id']['amount'].value,
                              "status": detailed_transaction_object['response_id']['status'].value},safe=False)


