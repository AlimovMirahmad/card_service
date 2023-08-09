import uuid

from django.db import models
import random
from datetime import datetime, timedelta


def generate_card_number_uzcard():
    prefix = 8600
    bank_number = random.randint(1000, 9999)
    user_number = random.randint(10000000, 99999999)
    return prefix * (10 ** 12) + bank_number * (10 ** 8) + user_number


def generate_card_number_humo():
    prefix = 9860
    bank_number = random.randint(1000, 9999)
    user_number = random.randint(10000000, 99999999)
    return prefix * (10 ** 12) + bank_number * (10 ** 8) + user_number


class Uzcard(models.Model):
    holder_name = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(default=generate_card_number_uzcard)
    expire = models.DateField(default=datetime.now() + timedelta(days=4 * 365))
    sms_notification_number = models.IntegerField(default=998901234567)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.number)


class Humo(models.Model):
    holder_name = models.CharField(max_length=100)
    number = models.IntegerField(default=generate_card_number_humo)
    expire = models.DateField(default=datetime.now() + timedelta(days=4 * 365))
    sms_notification_number = models.IntegerField(default=998901234567)
    card_token = models.UUIDField(default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.number)


class Otp(models.Model):
    otp_code = models.IntegerField(default=0)
    otp_key = models.UUIDField(default=uuid.uuid4)
    card = models.ForeignKey(Uzcard, on_delete=models.CASCADE)
    expire = models.DateTimeField(auto_now_add=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class OtpHumo(models.Model):
    otp_code = models.IntegerField(default=0)
    otp_key = models.UUIDField(default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True, null=True)
    expire = models.DateTimeField(auto_now_add=True, null=True)
    card = models.ForeignKey(Humo, on_delete=models.CASCADE)


class Service(models.Model):
    name = models.CharField(max_length=100)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Payment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    card = models.ForeignKey(Humo, on_delete=models.CASCADE)
    how_much = models.FloatField(default=0)

    payment_created_at = models.DateTimeField(auto_now_add=True)

