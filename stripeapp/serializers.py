from .utils import ccard_mask, cvv_mask
from .models import CCRequest, CreditCardToken, CreditCardInfo,ChargeRequest,ChargeResponse, Transaction
from rest_framework import serializers

class CCardRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = CCRequest
        fields = '__all__'



    def save(self, data):
        """
        This method is in charge of save the credit card filtered with custopm masks.
        :param data: Contains the payment/charge information that must be masked.
        :return: It returns a credit_card object.
        """

        cvv = cvv_mask(data['cvv'])
        credit_card_number = ccard_mask(data['cc_num'])
        expiration_date = data['exp_date']
        transaction = data['trans_id']
        amount = data['amount']

        credit_card = CCRequest.objects.create(trans_id=transaction, cc_num=credit_card_number, cvv=cvv, exp_date=expiration_date, amount=amount)

        return credit_card


class CreditCardTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardToken
        fields = "__all__"

class CreditCardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardInfo
        fields = "__all__"

class ChargeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeRequest
        fields = "__all__"

class ChargeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeResponse
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
class DetailedTransactionSerializer(serializers.ModelSerializer):
    request_id = CCardRequestSerializer()
    response_id = ChargeResponseSerializer()
    class Meta:
        model = Transaction
        fields = ('request_id','response_id')
