from datetime import datetime

from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class InviteUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_name = models.CharField(max_length=10)
    sub_id = models.CharField(max_length=10, default=User)
    click = models.IntegerField(default=0)
    sign_up = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email


class InvitePayment(models.Model):
    invite_url = models.ForeignKey(InviteUrl, on_delete=models.SET_NULL, null=True)
    payment_status = models.IntegerField(default=0)
    new_user = models.IntegerField(default=0)
    inv_user = models.IntegerField(default=0)
    balance = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.invite_url.sub_id


class Payouts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payout_id = models.CharField(max_length=20)
    payout_amount = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(default=datetime.now)
