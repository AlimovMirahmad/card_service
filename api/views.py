from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, \
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Uzcard, Humo, Otp, OtpHumo, Payment, Service
from .serializer import HumoSerializer, UzCardSerializer, PaymentSerializer
from .permission import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
import random


class PhoneTokenCreateAPIView(CreateAPIView):
    queryset = Humo.objects.all()
    serializer_class = HumoSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        otp_code = random.randint(100000, 999999)

        humo_card = Humo.objects.get(number=request.data.get('number'), expire=request.data.get("expire"))

        otp = OtpHumo.objects.create(otp_code=otp_code, card=humo_card)
        otp.expire = otp.created + timedelta(minutes=3)
        otp.save(update_fields=['expire'])
        print(humo_card.sms_notification_number, otp.otp_code)
        return Response(
            {
                "status": "ok",
                "otp_token": otp.otp_key,
                # 'otp_code': otp.otp_code
            }, status=status.HTTP_201_CREATED
        )


class ConfirmOtpCode(viewsets.ViewSet):
    queryset = OtpHumo.objects.all()

    def verify(self, request, *args, **kwargs):
        otp_key = request.data.get('otp_key')
        otp_code = request.data.get('otp_code')
        otp = OtpHumo.objects.filter(otp_key=otp_key).last()

        if otp is None:
            return Response(
                {
                    "error": "otpKey not found"
                }, status=status.HTTP_404_NOT_FOUND
            )
        elif otp.expire < timezone.now():
            otp.delete()
            return Response(
                {"error": "OtpKey истек"}, status=status.HTTP_400_BAD_REQUEST
            )
        elif otp_code != otp.otp_code:
            return Response(
                {"error": "Недопустимый OtpCode"}, status=status.HTTP_400_BAD_REQUEST
            )
        elif otp.expire > timezone.now() and int(otp_code) == otp.otp_code:
            humo = Humo.objects.filter(id=otp.card.id).last()
            humo.is_verified = True
            humo.save(update_fields=['is_verified'])
            otp.delete()
            return Response(
                {"status": "ok",
                 'card_token': humo.card_token}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Неверный OTP или OTP уже использован"}, status=status.HTTP_400_BAD_REQUEST
            )


class PaymentCreateAPIView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = Service.objects.filter(id=request.data.get('service')).last()
            except Service.DoesNotExist:
                return Response({'error': 'Objects not found'}, status=status.HTTP_404_NOT_FOUND)
            try:
                card = Humo.objects.get(card_token=kwargs.get("card_key"))
            except Service.DoesNotExist:
                return Response({'error': 'Objects not found'}, status=status.HTTP_404_NOT_FOUND)
            try:
                how_much = request.data.get('how_much')
                print(type(how_much))
                if how_much < card.balance:
                    service.balance += how_much
                    service.save(update_fields=['balance'])
                    card.balance -= how_much
                    card.save(update_fields=['balance'])
                    return Response(
                        {
                            "status": "ok"
                        }, status=status.HTTP_201_CREATED
                    )
                else:
                    return Response({'error': "you don't have enough in your account"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
        return Response({"error": 'er'}, status=status.HTTP_400_BAD_REQUEST)
