from django.urls import path
from .views import ConfirmOtpCode, PhoneTokenCreateAPIView, PaymentCreateAPIView


urlpatterns = [
    path('init/', PhoneTokenCreateAPIView.as_view()),
    path('confirm/', ConfirmOtpCode.as_view({'post': 'verify'})),
    path('payment/<str:card_key>/', PaymentCreateAPIView.as_view())

]
