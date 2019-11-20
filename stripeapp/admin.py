from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CCRequest)
admin.site.register(CreditCardInfo)
admin.site.register(ChargeResponse)
admin.site.register(CreditCardToken)
admin.site.register(Transaction)
admin.site.register(ChargeRequest)
