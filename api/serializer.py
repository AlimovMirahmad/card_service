from rest_framework import serializers
from .models import Service, Uzcard, Humo, Payment
from rest_framework.response import Response
from rest_framework import status


class HumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Humo
        fields = ['number', 'expire']


class UzCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzcard
        fields = ['number', 'expire']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['service', 'how_much']
