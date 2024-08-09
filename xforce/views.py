from django.shortcuts import render
from marketing_machine.models import *
from .forms import *
import time
import decimal
import traceback
import stripe
from django.contrib import messages
from django.conf import settings
from django.core.handlers import exception
import datetime
from django.db import transaction
from django.db.models import Q, Count, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def xforce_packages_view(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role.role_name == "Sub User":
        return render(request, 'settings_coming_soon.html')
    if not XForceSubscriptionDetails.objects.filter(user=request.user).exists():
        XForceSubscriptionDetails.objects.create(user=request.user,
                                                 xforce_membership_plan=XForceSubscriptionPlan.objects.first(),
                                                 xforce_subscription_end_date=date.today())
    subscription_details = XForceSubscriptionDetails.objects.get(user=request.user)
    try:
        if subscription_details.xforce_subscription_id:
            stripe.Subscription.retrieve(subscription_details.xforce_subscription_id)
            subscription = stripe.Subscription.retrieve(subscription_details.xforce_subscription_id)
            subscription_details.xforce_subscription_end_date = time.strftime("%Y-%m-%d", time.gmtime(
                subscription.current_period_end))
            subscription_details.save()
    except:
        print(traceback.print_exc())
    return render(request, 'xforce/xforce_packages_and_plans.html', {"membership_details": subscription_details})


def subscribe_monthly(request):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        user = profile.created_by.user
    else:
        user = request.user

    customer_id = UserStripeDetail.objects.get(user=user).customer_id
    member_ship_detail = XForceSubscriptionDetails.objects.get(user=user)

    if XForceSubscriptionDetails.objects.filter(user=user, xforce_subscription_status="Subscribed"):
        stripe.Subscription.modify(
            member_ship_detail.xforce_subscription_id,
            cancel_at_period_end=True
        )
        XForceSubscriptionDetails.objects.filter(user=user).update(xforce_next_subscription_plan="Monthly",
                                                                   xforce_membership_plan=XForceSubscriptionPlan.objects.get(xforce_plan="Monthly"))
        messages.add_message(request, messages.INFO,
                             'Plan changed to Monthly subscription, '
                             'Payment will be deducted when your annual subscription period ends!')
    elif XForceSubscriptionDetails.objects.filter(user=user,
                                                  xforce_subscription_status="Cancelled") and date.today() < member_ship_detail.xforce_subscription_end_date:
        XForceSubscriptionDetails.objects.filter(user=user).update(xforce_next_subscription_plan="Monthly",
                                                                   xforce_subscription_status="Subscribed",
                                                                   xforce_membership_plan=XForceSubscriptionPlan.objects.get(xforce_plan="Monthly"))
        # s_amount = decimal.Decimal(97)
        # Revenue.objects.create(amount=s_amount)
        messages.add_message(request, messages.INFO,
                             'Monthly subscription Successful, '
                             'Payment will be deducted when your previous payed subscription period ends!')
    else:
        new_7_days = datetime.datetime.now() + datetime.timedelta(days=7)
        # today = datetime.datetime.timestamp(datetime.datetime.now())
        # start = datetime.datetime.timestamp(new_7_days)
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        'plan': "plan_HG6hCcpg2q8beJ",  # Monthly Plan
                        'quantity': 1,
                    }
                ],
                trial_end=new_7_days,
            )
            if subscription.status == 'active' or subscription.status == 'trialing':
                XForceSubscriptionDetails.objects.filter(user=user).update(xforce_subscription_status="Subscribed",
                                                                           xforce_membership_plan=XForceSubscriptionPlan.objects.get(
                                                                            xforce_plan="Monthly"),
                                                                           xforce_subscription_id=subscription.id,
                                                                           xforce_next_subscription_plan="None",
                                                                           xforce_subscription_end_date=time.strftime("%Y-%m-%d",
                                                                                                       time.gmtime(
                                                                                                           subscription.current_period_end)))
                s_amount = decimal.Decimal(147)
                Revenue.objects.create(amount=s_amount)
                messages.add_message(request, messages.INFO,
                                     'Monthly subscription Successful, '
                                     'You can check your invoice history in payments and packages section!')
            else:
                messages.add_message(request, messages.INFO,
                                     "There's some error with the card!")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.RateLimitError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.InvalidRequestError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.AuthenticationError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.StripeError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except Exception as e:
            print(traceback.print_exc())
            messages.add_message(request, messages.INFO, "There is some error with the card!")
    return redirect("/x_force/xforce_packages")


def subscribe_yearly(request):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        user = profile.created_by.user
    else:
        user = request.user

    customer_id = UserStripeDetail.objects.get(user=user).customer_id
    member_ship_detail = XForceSubscriptionDetails.objects.get(user=user)

    if XForceSubscriptionDetails.objects.filter(user=user, xforce_subscription_status="Subscribed"):
        stripe.Subscription.modify(
            member_ship_detail.xforce_subscription_id,
            cancel_at_period_end=True
        )
        XForceSubscriptionDetails.objects.filter(user=user).update(xforce_next_subscription_plan="Yearly",
                                                                   xforce_membership_plan=XForceSubscriptionPlan.objects.get(xforce_plan="Yearly"))
        messages.add_message(request, messages.INFO,
                             'Plan changed to Yearly subscription, '
                             'Payment will be deducted when your monthly subscription period ends!')
    elif XForceSubscriptionDetails.objects.filter(user=user,
                                                  xforce_subscription_status="Cancelled") and date.today() < member_ship_detail.xforce_subscription_end_date:
        XForceSubscriptionDetails.objects.filter(user=user).update(xforce_next_subscription_plan="Yearly",
                                                                   xforce_subscription_status="Subscribed",
                                                                   xforce_membership_plan=XForceSubscriptionPlan.objects.get(xforce_plan="Yearly"))
        # s_amount = decimal.Decimal(219)
        # Revenue.objects.create(amount=s_amount)
        messages.add_message(request, messages.INFO,
                             'Yearly subscription Successful, '
                             'Payment will be deducted when your previous payed subscription period ends!')
    else:
        new_7_days = datetime.datetime.now() + datetime.timedelta(days=7)
        # today = datetime.datetime.timestamp(datetime.datetime.now())
        # start = datetime.datetime.timestamp(new_7_days)
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        'plan': "plan_HG6lnAjVeDtMmp",  # Yearly Plan
                        'quantity': 1,
                    }
                ],
                trial_end=new_7_days,
            )
            if subscription.status == 'active' or subscription.status == 'trialing':
                XForceSubscriptionDetails.objects.filter(user=user).update(xforce_subscription_status="Subscribed",
                                                                           xforce_membership_plan=XForceSubscriptionPlan.objects.get(xforce_plan="Yearly"),
                                                                           xforce_subscription_id=subscription.id,
                                                                           xforce_next_subscription_plan="None",
                                                                           xforce_subscription_end_date=time.strftime("%Y-%m-%d", time.gmtime(
                                                                            subscription.current_period_end)))
                s_amount = decimal.Decimal(1411)
                Revenue.objects.create(amount=s_amount)
                messages.add_message(request, messages.INFO,
                                     'Yearly subscription Successful, '
                                     'You can check your invoice history in payments and packages section!')
            else:
                messages.add_message(request, messages.INFO,
                                     "There's some error with the card!")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.RateLimitError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.InvalidRequestError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.AuthenticationError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.StripeError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except Exception as e:
            print(traceback.print_exc())
            messages.add_message(request, messages.INFO, "There is some error with the card!")

    return redirect("/x_force/xforce_packages")


def cancel_subscription(request):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        user = profile.created_by.user
    else:
        user = request.user

    customer = UserStripeDetail.objects.get(user=user).customer_id
    membership_details = XForceSubscriptionDetails.objects.get(user=user)
    subscriptions = stripe.Subscription.list(customer=customer)
    if membership_details.xforce_subscription_id in subscriptions:
        stripe.Subscription.delete(XForceSubscriptionDetails.objects.get(user=user).xforce_subscription_id)

    XForceSubscriptionDetails.objects.filter(user=user).update(
        xforce_subscription_status='Cancelled',
        xforce_next_subscription_plan="None")

    messages.add_message(request, messages.INFO,
                         'Subscription cancelled Successfully!')
    return redirect("/x_force/xforce_packages")


def x_force_view(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role.role_name == "Sub User":
        admin_user = profile.created_by.user
    else:
        if XForceSubscriptionDetails.objects.filter(user=request.user, xforce_subscription_status="Cancelled"):
            monthly_subscription = XForceSubscriptionDetails.objects.get(user=request.user,
                                                                         xforce_subscription_status="Cancelled")
            if date.today() >= monthly_subscription.xforce_subscription_end_date:
                messages.add_message(request, messages.INFO,
                                     "Your Need to Subscribe to the XForce Module Plan!")
                return redirect('/xforce/xforce_packages')
        admin_user = request.user
    # users = UserProfile.objects.filter(created_by__user=admin_user).values('user')
    if not XForceSubscriptionDetails.objects.filter(user=request.user).exists():
        XForceSubscriptionDetails.objects.create(user=request.user,
                                                 xforce_membership_plan=XForceSubscriptionPlan.objects.first(),
                                                 xforce_subscription_end_date=date.today())
    subscription_details = XForceSubscriptionDetails.objects.get(user=admin_user)
    if UserStripeDetail.objects.filter(user=admin_user).exists():
        try:
            if subscription_details.xforce_subscription_id:
                stripe.Subscription.retrieve(subscription_details.xforce_subscription_id)
                subscription = stripe.Subscription.retrieve(subscription_details.xforce_subscription_id)
                subscription_details.xforce_subscription_end_date = time.strftime("%Y-%m-%d", time.gmtime(
                    subscription.current_period_end))
                subscription_details.save()
        except:
            print(traceback.print_exc())
    return render(request, 'xforce/xforce.html')


def add_team_member(request):
    return render(request,"xforce/add_team_member.html")


def add_seller_lead(request):

    lead_manager=User.objects.all()
    campaign=MarketingCampaign.objects.all()

    context={"lead_manager":lead_manager,
             "campaign":campaign}
    if request.method == "POST":
        form = add_seller_leads_form(request.POST)
        if form.is_valid():
            seller_lead = form.save(commit=False)
            seller_lead.save()
            return render(request, "xforce/xforce.html")
    else:
        form = add_seller_leads_form()
    return render(request, 'xforce/add_seller_lead.html', context, {"form": form})


def add_title_company(request):
    return render(request, "xforce/add_title_company.html")


def new_transactions(request):
    return render(request, "xforce/new_transactions.html")


def add_appointment(request):
    return render(request, "xforce/add_appointment.html")


def add_sales(request):
    return render(request, "xforce/add_sales.html")
