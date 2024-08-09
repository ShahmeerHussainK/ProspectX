from django.db import models
from django.contrib.auth.models import User


class XForceSubscriptionPlan(models.Model):
    xforce_plan = models.CharField(max_length=100)
    xforce_billing_amount = models.FloatField()

    def __str__(self):
        return self.xforce_plan

    class Meta:
        verbose_name_plural = 'XForce Subscription Plan'


xforce_subscription_status = (
    ('Not Subscribed', 'Not Subscribed'),
    ('Subscribed', 'Subscribed'),
    ('Cancelled', 'Cancelled'),
)

xforce_next_subscription_plan = (
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly'),
    ('None', 'None'),
)


class XForceSubscriptionDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xforce_membership_plan = models.ForeignKey(XForceSubscriptionPlan, on_delete=models.CASCADE)
    xforce_subscription_id = models.CharField(max_length=255, blank=True, null=True, default=None)
    xforce_subscription_status = models.CharField(max_length=20, choices=xforce_subscription_status, default='Not Subscribed')
    xforce_subscription_end_date = models.DateField(blank=True, null=True)
    xforce_next_subscription_plan = models.CharField(max_length=50, choices=xforce_next_subscription_plan, default="None")
    xforce_account_status = models.CharField(max_length=10, default="active")

    class Meta:
        verbose_name_plural = 'Subscription Details'
