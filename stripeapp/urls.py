from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import PaymentRequestView

urlpatterns = [
    path('token/', csrf_exempt(PaymentRequestView.as_view()), name="payment"),
]
