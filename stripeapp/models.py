from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models


class CCRequest(models.Model):
    """
    This model will save the incoming request data:

        **Note:
            This data will send to stripe api, to simulate the card authentication.
             {
                        "cc_num": "4111111111111111",
                        "cvv": "123",
                        "exp_date": "1219",
                        "trans_id": "321654351687",
                        "amount": "12.00"
             }
    """

    trans_id = models.CharField(max_length=100)

    cc_num_validator = RegexValidator(regex=r"^\d*$")
    cc_num = models.CharField("Credit Card number", validators=[cc_num_validator],max_length=16, null=False)

    cvv_validator = RegexValidator(regex=r"^\d*$")
    cvv = models.CharField("CVV", validators=[cvv_validator], max_length=4, null=False)

    exp_date_validator = RegexValidator(regex=r"^\d*$")
    exp_date = models.CharField("Expiration date",validators=[exp_date_validator], max_length=4, null=False)

    amount = models.IntegerField("Amount",null=True,blank=True,validators=[MinValueValidator(0), MaxValueValidator(99999999)])

class CreditCardInfo(models.Model):
        """
        Model in charge of validate and save the data coming in the response from Stripe.
        This information is stracted from CreditCardTokenResponse
        """
        address_city = models.CharField(max_length=100, null=True, blank=True)
        address_country = models.CharField(max_length=50, null=True, blank=True)
        address_line1 = models.CharField(max_length=100, null=True, blank=True)
        address_line1_check = models.CharField(max_length=50, null=True, blank=True)
        address_line2 = models.CharField(max_length=100, null=True, blank=True)
        address_state = models.CharField(max_length=50, null=True, blank=True)
        address_zip = models.CharField(max_length=10, null=True, blank=True)
        address_zip_check = models.CharField(max_length=10, null=True, blank=True)
        brand = models.CharField(max_length=50, null=True, blank=True)
        country = models.CharField(max_length=50, null=True, blank=True)
        cvc_check = models.CharField(max_length=10, null=True, blank=True)
        dynamic_last4 = models.CharField(max_length=50, null=True, blank=True)
        exp_month = models.PositiveIntegerField()
        exp_year = models.PositiveIntegerField()
        fingerprint = models.CharField(max_length=60, null=True, blank=True)
        funding = models.CharField(max_length=60, null=True, blank=True)
        id_card = models.CharField(max_length=60, null=True, blank=True)
        last4 = models.CharField(max_length=4, null=True, blank=True)
        name = models.CharField(max_length=60, null=True, blank=True)
        object = models.CharField(max_length=40, null=True, blank=True)
        tokenization_method = models.CharField(max_length=60, null=True, blank=True)

class CreditCardToken(models.Model):
    """
    Handle the card information

    **Note_
        All the fields are provided by stripe/api/ Tokens.

        visit: https://stripe.com/docs/api/tokens/create_card
                see Response (Square)  details.
    """
    client_ip = models.CharField(max_length=15, null=True, blank=True)
    created = models.CharField(max_length=50, null=True, blank=True)
    token_id = models.CharField(max_length=50, null=True, blank=True,unique=True)
    livemode = models.BooleanField()
    object = models.CharField(max_length=40, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    used = models.BooleanField()
    cc_info = models.ForeignKey(CreditCardInfo, on_delete=models.CASCADE)

class ChargeRequest(models.Model):
    """
    Handle the charge info,this is used to create a charge with stripe api.
    This information is saved for control porpouses.
    **Note_
            All the fields are provided by stripe/api/ Charges.

            visit: https://stripe.com/docs/api/charges
                    see Response (Square)  details.
    """

    amount = models.PositiveIntegerField(null=True,blank=True)
    currency = models.CharField(max_length=10,null=True,blank=True)
    source = models.ForeignKey(CreditCardToken,to_field="token_id",on_delete=models.CASCADE)


class ChargeResponse(models.Model):
    """
    Handle the charge response info, this informations is for responses control.

      **Note_
        All the fields are provided by stripe/api/ Tokens.

        visit: https://stripe.com/docs/api/tokens/create_card
                see Response (Square)  details.

    """

    charge_id = models.CharField(max_length=150,null=True,blank=True)
    object = models.CharField(max_length=40,null=True,blank=True)
    c_card = models.ForeignKey(CreditCardInfo,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True,blank=True)
    amount_refunded = models.IntegerField(null=True,blank=True)
    funding = models.CharField(max_length=30,null=True,blank=True)
    balance_transaction = models.CharField(max_length=60,null=True,blank=True)
    currency = models.CharField(max_length=10,null=True,blank=True)
    description = models.CharField(max_length=150,null=True,blank=True)
    paid = models.BooleanField()
    payment_method = models.CharField(max_length=150,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)

class Transaction(models.Model):
    """
    Model in charge of contains the request, it's for control.
    """
    request_id = models.ForeignKey(CCRequest, on_delete=models.CASCADE)
    response_id = models.ForeignKey(ChargeResponse, on_delete=models.CASCADE)
