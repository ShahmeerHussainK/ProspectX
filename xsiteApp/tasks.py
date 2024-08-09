from datetime import timedelta

import stripe
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
import time

from django.db.models import F
from django_eventstream import send_event

from notification.models import Notification_Pill, Notification

from user.models import UserStripeDetail, UserProfile, Revenue
from xsiteApp.models import MembershipDetails, MembershipPlan, Websites

logger = get_task_logger(__name__)
from filter_prospects.models import *
from django.http import JsonResponse
import requests
import json
import decimal


@periodic_task(
    run_every=(crontab(hour="*/24")),
    name="notify_domain_expiry",
    ignore_result=True
)
def notify_domain_expiry():
    current_date = date.today()
    sites = Websites.objects.all()
    for site in sites:
        site_date = site.renewal_date
        user = UserProfile.objects.get(user=site.user).user
        if site_date == current_date:
            site.is_expired = True
            site.save()
            send_event('prospectx' + str(user.id),
                       'message',
                       'Your domain (' + site.domain + ') has expired.')
            Notification_Pill.objects.filter(
                user=user).update(
                notification_pill=F('notification_pill') + 1)
            Notification.objects.create(user=user,
                                        title="Your domain (" + site.domain + ") has expired.")
        elif (current_date + timedelta(days=30)) == site_date:
            send_event('prospectx' + str(user.id),
                       'message',
                       'Your domain (' + site.domain + ') will be expired in 30 days.')
            Notification_Pill.objects.filter(
                user=user).update(
                notification_pill=F('notification_pill') + 1)
            Notification.objects.create(user=user,
                                        title="Your domain (" + site.domain + ") will be expired in 30 days.")
        elif (current_date + timedelta(days=15)) == site_date:
            send_event('prospectx' + str(user.id),
                       'message',
                       'Your domain (' + site.domain + ') will be expired in 15 days.')
            Notification_Pill.objects.filter(
                user=user).update(
                notification_pill=F('notification_pill') + 1)
            Notification.objects.create(user=user,
                                        title="Your domain (" + site.domain + ") will be expired in 15 days.")
        elif (current_date + timedelta(days=7)) == site_date:
            send_event('prospectx' + str(user.id),
                       'message',
                       'Your domain (' + site.domain + ') will be expired in 7 days.')
            Notification_Pill.objects.filter(
                user=user).update(
                notification_pill=F('notification_pill') + 1)
            Notification.objects.create(user=user,
                                        title="Your domain (" + site.domain + ") will be expired in 7 days.")

    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(hour="*/24")),
    name="change_subscription_plan",
    ignore_result=True
)
def change_subscription_plan():
    monthly_subscription = MembershipDetails.objects.filter(subscription_status="Subscribed",
                                                            next_subscription_plan="Monthly")

    for subscription in monthly_subscription:
        if date.today() == subscription.subscription_end_date:
            stripe.Subscription.delete(MembershipDetails.objects.get(user=subscription.user).subscription_id)
            customer_id = UserStripeDetail.objects.get(user=subscription.user).customer_id
            subs = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        'plan': "plan_Gi1KATDSAZwOtU",  # Monthly Plan plan_Gi1KATDSAZwOtU
                        'quantity': 1,
                    }
                ],
            )
            subscription.membership_plan = MembershipPlan.objects.get(plan="Monthly")
            subscription.next_subscription_plan = "None"
            subscription.subscription_id = subs.id
            subscription.subscription_end_date = time.strftime("%Y-%m-%d", time.gmtime(
                subs.current_period_end))
            subscription.save()
            s_amount = decimal.Decimal(47)
            Revenue.objects.create(amount=s_amount)

    yearly_subscription = MembershipDetails.objects.filter(subscription_status="Subscribed",
                                                           next_subscription_plan="Yearly")

    for subscription in yearly_subscription:
        if date.today() == subscription.subscription_end_date:
            stripe.Subscription.delete(MembershipDetails.objects.get(user=subscription.user).subscription_id)
            customer_id = UserStripeDetail.objects.get(user=subscription.user).customer_id
            subs = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        'plan': "plan_Gi1KBUF6m49jy2",  # Monthly Plan plan_Gi1KATDSAZwOtU
                        'quantity': 1,
                    }
                ],
            )
            subscription.membership_plan = MembershipPlan.objects.get(plan="Yearly")
            subscription.next_subscription_plan = "None"
            subscription.subscription_id = subs.id
            subscription.subscription_end_date = time.strftime("%Y-%m-%d", time.gmtime(
                subs.current_period_end))
            subscription.save()
            s_amount = decimal.Decimal(219)
            Revenue.objects.create(amount=s_amount)

    temp = {}
    return JsonResponse(temp)
