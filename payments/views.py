from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import traceback
import time
from django.db import transaction
from django.core.mail import EmailMessage
from django.template.loader import get_template
import requests
from user.models import *
from django.db.models import Q
from .models import *
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
import random
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.http import HttpResponseRedirect
from datetime import datetime as datetime, timedelta

# Create your views here.


# packages base function for subscription check
def is_subscribed(user):
    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.role.role_name == 'Admin User':
            if UserStripeDetail.objects.filter(user=user).exists():
                # strp = UserStripeDetail.objects.get(user=user)
                # if strp.cancelled_before_starting:
                #     data = {
                #         "subscribed": "no",
                #     }
                #     return data
                # else:
                #     subs = stripe.Subscription.retrieve(strp.subscription_id)
                #     # print("subscription status: ", subs.status)
                #     if subs.status == 'canceled' or subs.status == 'unpaid' or subs.status == 'incomplete_expired':
                #         data = {
                #             "subscribed": "no",
                #         }
                #         return data
                #     else:
                data = {
                    "subscribed": "yes",
                }
                return data
            else:
                data = {
                    "subscribed": "no",
                }
                return data
        else:
            data = {
                "subscribed": "yes",
            }
            return data
    else:
        data = {
            "subscribed": "yes",
        }
        return data


def store_customer(request):
    try:
        user_id = request.POST.get('user_id')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        with transaction.atomic():
            token = stripe.Token.create(
                card={
                    'number': request.POST.get('number'),
                    'exp_month': request.POST.get('exp_month'),
                    'exp_year': request.POST.get('exp_year'),
                    'cvc': request.POST.get('cvc'),
                },
            )
            user = User.objects.get(id=user_id)

            UserStripeDetail.objects.create(user=user, token=token.id)

            return Response({"status": status.HTTP_200_OK, "data": token})

    except stripe.error.CardError as ce:
        print(traceback.print_exc())
        return False, ce


class AddNewCard(APIView):
    def post(self,request):
        try:
            user_id = request.POST.get('user_id')
            stripe.api_key = settings.STRIPE_SECRET_KEY
            with transaction.atomic():
                token = stripe.Token.create(
                    card={
                        'number': request.POST.get('number'),
                        'exp_month': request.POST.get('exp_month'),
                        'exp_year': request.POST.get('exp_year'),
                        'cvc': request.POST.get('cvc'),
                    },
                )
                user = User.objects.get(id=user_id)

                # UserStripeDetail.objects.create(user=user, token=token.id)

                return Response({"status": status.HTTP_200_OK, "data": token})

        except stripe.error.CardError as ce:
            print(traceback.print_exc())
            return False, ce


def payment(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    return render(request, 'payments/payment.html', context_key)


def create_monthly_plan(request):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        plan = stripe.Plan.create(
            amount=39700,
            interval="month",
            product={
                "name": "Monthly ProspectX"
            },
            currency="USD",
        )
        return render(request, 'payments/payment_and_packages.html')

    except stripe.error.CardError as ce:
        print(traceback.print_exc())
        return render(request, 'payments/payment_and_packages.html')


def create_yearly_plan(request):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        plan = stripe.Plan.create(
            amount=399700,
            interval="year",
            product={
                "name": "Yearly ProspectX"
            },
            currency="USD",
        )
        return render(request, 'payments/payment_and_packages.html')

    except stripe.error.CardError as ce:
        print(traceback.print_exc())
        return render(request, 'payments/payment_and_packages.html')


def subscribe_monthly_plan(request):
    try:
        user = request.user
        token = request.POST['stripeToken']
        with transaction.atomic():

            customer = stripe.Customer.create(
                email=user.email,
                source= token,
            )

            subscription = stripe.Subscription.create(
                customer=customer,
                items=[
                    {
                        'plan': 'plan_HG6fCTjltYzi7i',   # basic monthly test plan id
                        'quantity': 1,
                    }
                ],
            )
            if UserStripeDetail.objects.filter(user=user).exists():
                UserStripeDetail.objects.filter(user=user).update(stripe_token=token, customer_id=customer.id,
                                                                  subscription_id=subscription.id, subscription_status='Subscribed',
                                                                  subscription_cancel_date=str(subscription.current_period_end), plan='Monthly')
            else:
                UserStripeDetail.objects.create(user=user, stripe_token=token, customer_id=customer.id,
                                                subscription_id=subscription.id, subscription_status='Subscribed',
                                                subscription_cancel_date=str(subscription.current_period_end), plan='Monthly')

            return render(request, 'dashboard.html')

    except:
        print(traceback.print_exc())
        return render(request, 'payments/payment_and_packages.html', {"context": context, "invoices_list": invoices_list})


def subscribe_yearly_plan(request):
    try:
        user = request.user
        token = request.POST['stripeToken']
        with transaction.atomic():
            # user = User.objects.get(id=user_id)

            customer = stripe.Customer.create(
                email=user.email,
                source=token,
            )
            # customer = UserStripeDetail.objects.get(user=user)

            subscription = stripe.Subscription.create(
                customer=customer,
                items=[
                    {
                        'plan': 'plan_HG6jeY9IIyUnHM',   # basic yearly test plan id
                        'quantity': 1,
                    }
                ],
            )

            if UserStripeDetail.objects.filter(user=user).exists():
                UserStripeDetail.objects.filter(user=user).update(stripe_token=token, customer_id=customer.id,
                                                                  subscription_id=subscription.id,
                                                                  subscription_status='Subscribed',
                                                                  subscription_cancel_date=str(
                                                                      subscription.current_period_end), plan='Yearly')
            else:
                UserStripeDetail.objects.create(user=user, stripe_token=token, customer_id=customer.id,
                                                subscription_id=subscription.id, subscription_status='Subscribed',
                                                subscription_cancel_date=str(subscription.current_period_end), plan='Yearly')

            return render(request, 'dashboard.html')


    except:
        print(traceback.print_exc())
        return render(request, 'dashboard.html')


def upgrade_package(request):
    customer = UserStripeDetail.objects.filter(user=request.user)
    if request.method == 'POST':
        yearly = request.POST.get('yearly')
        monthly = request.POST.get('monthly')
        if monthly:
            try:
                user = request.user
                with transaction.atomic():
                    if customer[0].subscription_status == 'Subscribed':
                        stripe.Subscription.modify(
                            customer[0].subscription_id,
                            cancel_at_period_end=True
                        )
                    else:
                        pass
                    subscription = stripe.Subscription.create(
                        customer=customer[0].customer_id,
                        items=[
                            {
                                'plan': 'plan_HG6fCTjltYzi7i',   # basic monthly test plan id
                                'quantity': 1,
                            }
                        ],
                    )

                    UserStripeDetail.objects.filter(user=user).update(user=user,
                                                                      subscription_id=subscription.id, subscription_status='Subscribed',
                                                                      subscription_cancel_date=str(subscription.current_period_end),
                                                                      plan='Monthly',
                                                                      subscription_end_date=time.strftime("%Y-%m-%d", time.gmtime(subscription.current_period_end)))
                    user_profile = UserProfile.objects.get(user=user)
                    Permissions.objects.filter(pk=user_profile.permissions.id).update(marketing_plan=True,
                                                                                      skip_trace=True,
                                                                                      list_management=True,
                                                                                      access_import_log=True,
                                                                                      access_export_log=True,
                                                                                      access_tag_log=True)
                    messages.success(request, "Successfully Downgraded to Monthly Plan!", extra_tags='updated')
                    return redirect('/payments/packages')
            except stripe.error.RateLimitError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.InvalidRequestError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.AuthenticationError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.StripeError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.CardError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except Exception as e:
                print(traceback.print_exc())
                messages.success(request, "There is some error with the request!", extra_tags='updated')
                return redirect('/payments/packages')
        elif yearly:
            try:
                user = request.user
                with transaction.atomic():
                    if customer[0].subscription_status == 'Subscribed':
                        stripe.Subscription.modify(
                            customer[0].subscription_id,
                            cancel_at_period_end=True
                        )
                    else:
                        pass
                    subscription = stripe.Subscription.create(
                        customer=customer[0].customer_id,
                        items=[
                            {
                                'plan': 'plan_HG6jeY9IIyUnHM',   # basic yearly test plan id
                                'quantity': 1,
                            }
                        ],
                    )

                    UserStripeDetail.objects.filter(user=user).update(user=user,
                                                                      subscription_id=subscription.id, subscription_status='Subscribed',
                                                                      subscription_cancel_date=str(subscription.current_period_end),
                                                                      plan='Yearly',
                                                                      subscription_end_date=time.strftime("%Y-%m-%d", time.gmtime(subscription.current_period_end)))
                    user_profile = UserProfile.objects.get(user=user)
                    Permissions.objects.filter(pk=user_profile.permissions.id).update(marketing_plan=True,
                                                                                      skip_trace=True,
                                                                                      list_management=True,
                                                                                      access_import_log=True,
                                                                                      access_export_log=True,
                                                                                      access_tag_log=True)
                    messages.success(request, "Successfully Upgraded to Yearly Plan!", extra_tags='updated')
                    return redirect('/payments/packages')
            except stripe.error.RateLimitError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.InvalidRequestError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.AuthenticationError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.StripeError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except stripe.error.CardError as e:
                body = e.json_body
                err = body['error']
                messages.success(request, err['message'], extra_tags='updated')
                return redirect('/payments/packages')
            except Exception as e:
                print(traceback.print_exc())
                messages.success(request, "There is some error with the request!", extra_tags='updated')
                return redirect('/payments/packages')
        else:
            return redirect('/payments/packages')
    else:
        return redirect('/payments/packages')


def add_new_card(request):
    intent = stripe.SetupIntent.create()
    client_secret = intent.client_secret
    return render(request, 'payments/payment.html', {"secret": client_secret})


def save_new_card(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {"key": key}
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payment_method = stripe.PaymentMethod.attach(
        intent.payment_method,
        customer='cus_GB2KLC2kCHhxGF'
    )

    return render(request, 'payments/save_card.html', {"context_key": context_key})


@login_required(login_url='/user/login')
def payments_and_packages(request):
    if UserStripeDetail.objects.filter(user=request.user).exists:
        customer = UserStripeDetail.objects.filter(user=request.user)
        email = customer[0].user.email
    else:
        email = request.user.email
    subscriptions = {
        "id": customer[0].subscription_id,
        "status": customer[0].subscription_status,
        "cancel_date": customer[0].subscription_cancel_date,
        "plan": customer[0].plan,
    }
    # adding new card
    if request.method == 'POST':
        try:
            stripe.Customer.create_source(
                customer[0].customer_id,
                source=request.POST['stripeToken']
            )
            messages.success(request, "New Card Added Successfully!", extra_tags='updated')
            return redirect('/payments/packages')
        except:
            print(traceback.format_exc())
            messages.success(request, "Could Not Add New Card, Please try again later!", extra_tags='updated')
            return redirect('/payments/packages')
    else:
        last_4 = []
        cards_list = []
        invoices_list = []
        try:
            cards = stripe.Customer.list_sources(
                customer[0].customer_id,
                limit=3,
                object='card'
            )
            count = 1
            for card in cards.data:
                if card.last4 not in last_4:
                    card_data = {
                        "id": card.id,
                        "brand": card.brand,
                        "expiry": str(card.exp_month) + "/" + str(card.exp_year),
                        "last4": card.last4,
                        "customer_id": card.customer,
                        "count": count
                    }
                    last_4.append(card.last4)
                    count +=1
                    cards_list.append(card_data)

            invoices = stripe.Invoice.list(customer=customer[0].customer_id)

            for inv in invoices.data:
                p = inv.lines.data[0].plan
                if p:
                    plan = "Active" if p.active == True else "Cancelled"
                else:
                    plan = "None"
                if inv.lines.data[0].plan:
                    pkg = inv.lines.data[0].plan.nickname + (' Trial' if inv.lines.data[0]['amount'] == 0 else "")
                else:
                    pkg = "SkipTrace Fee"
                invoice = {
                    "number": inv.number,
                    "date": time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime(inv.created)),
                    "package": pkg,
                    "status": plan if plan != "None" else "Charged",
                    "amount": '$'+str(inv.lines.data[0]['amount']/100),
                    "file": inv.invoice_pdf
                }
                invoices_list.append(invoice)

            return render(request, 'payments/payment_and_packages.html', {"invoices_list": invoices_list,
                                                                          "cards": cards_list, "count": len(cards_list),
                                                                          "email": email, "subs": subscriptions})
        except:
            print(traceback.print_exc())
            return render(request, 'payments/payment_and_packages.html', {"invoices_list": invoices_list,
                                                                          "cards": cards_list, "count": len(cards_list),
                                                                          "email": email, "subs": subscriptions})


def delete_card(request, card, customer):
    try:
        stripe.Customer.delete_source(
            customer,
            card
        )
        messages.success(request, "Card Deleted Successfully!", extra_tags='updated')
        return redirect('/payments/packages')
    except:
        print(traceback.format_exc())
        messages.success(request, "Could not Delete Card!", extra_tags='updated')
        return redirect('/payments/packages')


class change_default_card(APIView):
    def post(self, request):
        key = settings.STRIPE_PUBLISHABLE_KEY
        card = request.POST['card']
        customer = request.POST['customer']
        try:
            stripe.Customer.modify(
                customer,
                default_source=card,
            )
            context_key = {'key': key}
            messages.success(request, "Changed Default Card Successfully!", extra_tags='updated')
            # return redirect('/payments/packages')
            return Response(
                {"status": status.HTTP_200_OK, "context_key": context_key})
        except:
            messages.success(request, "Could Not Change Default Card!", extra_tags='updated')
            # return redirect('/payments/packages')
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST})


class CancelSubscription(APIView):
    def post(self, request):
        subs_id = request.POST['subs_id']
        obj = UserStripeDetail.objects.get(subscription_id=subs_id)
        today = datetime.timestamp(datetime.now())
        if int(today) <= obj.start_date:
            subscription = stripe.Subscription.retrieve(subs_id)
            UserStripeDetail.objects.filter(subscription_id=subs_id).update(
                # subscription_cancel_date=str(int(today)),
                # cancelled_before_starting=True,
                subscription_status='Cancelled',
                subscription_end_date=time.strftime("%Y-%m-%d", time.gmtime(subscription.current_period_end)))
            stripe.Subscription.delete(subs_id)
            # user_profile = UserProfile.objects.get(user=obj.user)
            # Permissions.objects.filter(pk=user_profile.permissions.id).update(marketing_plan=False,
            #                                                                   skip_trace=False,
            #                                                                   list_management=False,
            #                                                                   access_import_log=False,
            #                                                                   access_export_log=False,
            #                                                                   access_tag_log=False)
            messages.success(request, "Subscription Cancelled Successfully!", extra_tags='updated')
            return Response(
                {"status": status.HTTP_200_OK, })
        else:
            try:
                modify = stripe.Subscription.modify(
                    subs_id,
                    cancel_at_period_end=True
                )

                UserStripeDetail.objects.filter(subscription_id=subs_id).update(subscription_cancel_date=str(modify.current_period_end),
                                                                                subscription_status='Cancelled')
                user_profile = UserProfile.objects.get(user=obj.user)
                Permissions.objects.filter(pk=user_profile.permissions.id).update(marketing_plan=False,
                                                                                  skip_trace=False,
                                                                                  list_management=False,
                                                                                  access_import_log=False,
                                                                                  access_export_log=False,
                                                                                  access_tag_log=False)
                messages.success(request, "Subscription Cancelled Successfully!", extra_tags='updated')
                return Response(
                    {"status": status.HTTP_200_OK, })
            except:
                print(traceback.print_exc())
                return Response(
                    {"status": status.HTTP_400_BAD_REQUEST, })


def hook_stripe(request):
    try:
        event_json = json.loads(request.body)
        print(event_json)

        return Response({"status": status.HTTP_200_OK, "data": ""})

    except stripe.error.CardError as ce:
        print(traceback.print_exc())
        return False, ce

