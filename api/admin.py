from django.contrib import admin
from .models import Uzcard, Humo, Service, OtpHumo

admin.site.register(Humo)
admin.site.register(Uzcard)
admin.site.register(Service)
admin.site.register(OtpHumo)

