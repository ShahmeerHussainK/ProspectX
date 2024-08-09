from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(InviteUrl)
admin.site.register(InvitePayment)
admin.site.register(Payouts)