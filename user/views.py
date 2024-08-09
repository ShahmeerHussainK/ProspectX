import json
import traceback
import uuid
from datetime import datetime as dt, timedelta
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import F, Q, Sum
from django_eventstream import send_event
from notification.models import Notification_Pill
from xforce.utils import permissions_check
from xsiteApp.models import MembershipDetails, MembershipPlan
from xforce.models import XForceSubscriptionDetails, XForceSubscriptionPlan
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .send_cus_email import sendEmail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from .models import *
from affiliate.models import InviteUrl, InvitePayment
from django.conf import settings
import stripe
from payments.views import is_subscribed
from filter_prospects.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
import decimal
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from .serializers import UserSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
from skiptrace.models import PrepaidBalance
from django.contrib.messages import get_messages


# Create your views here.
def Signup(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    if request.method == 'GET':
        if request.user.is_authenticated:
            data = is_subscribed(request.user)
            return render(request, 'dashboard.html', {"context_key": context_key, "subscription": data})
        else:
            return render(request, 'user/register.html', {})

    elif request.method == 'POST':
        storage = get_messages(request)
        plan = request.POST.get('subscription_plan')
        invite = None
        for message in storage:
            invite = str(message)
        try:
            with transaction.atomic():
                form = UserForm(request.POST)
                profile_form = ProfileForm(request.POST)
                if form.is_valid() and profile_form.is_valid():
                    user = form.save(commit=False)
                    user.username = form.cleaned_data['email']
                    user.save()
                    permission = Permissions()
                    permission.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.permissions = permission
                    profile.plan = plan
                    profile.role = Role.objects.get(role_name="Admin User")
                    profile.xforce_uuid = uuid.uuid4().hex[:8]
                    profile.save()
                    welcome_email = WelcomeEmail.objects.filter(pk=1).first()
                    if welcome_email:
                        content = welcome_email.email_content
                        content = content.replace("%first_name%", form.cleaned_data['first_name'])
                        content = content.replace("%last_name%", form.cleaned_data['last_name'])
                        content = content.replace("%email%", form.cleaned_data['email'])
                        content = content.replace("%password%", form.cleaned_data['password1'])
                        content = content.replace("%phone%", profile_form.cleaned_data['cell_phone'])
                        ctx = {
                            'content': content,
                        }
                        to_email_list = [form.cleaned_data['email']]
                        subject = "Welcome to Prospectx"
                        html_message = render_to_string('user/Welcome_Email_Template.html', ctx)
                        plain_message = strip_tags(html_message)
                        from_email = welcome_email.email_from
                        send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                                  fail_silently=False)

                        InviteUrl.objects.create(user=user, url_name='usr{}'.format(user.id),
                                                 sub_id='sd{}'.format(user.id))
                        if invite:
                            ids = str(invite).split('-')
                            if len(ids) > 1:
                                InviteUrl.objects.filter(user=ids[0], sub_id=ids[1]).update(
                                    sign_up=F('sign_up') + 1)
                                qs_invite = InviteUrl.objects.get(user=ids[0], sub_id=ids[1])

                                InvitePayment.objects.create(invite_url=qs_invite, new_user=user.id, inv_user=int(ids[2]))
                    if plan == 'Monthly':
                        price = 'Monthly Plan $147.00'
                    else:
                        price = 'Yearly Plan $1411.00'
                    return render(request, 'user/register_plan.html',
                                  {'message': "Signup Successful, Enter Card Details Below!",
                                   'key': key, "email": user.email, "price": price})
                else:
                    if invite:
                        ids = str(invite).split('-')
                        messages.add_message(request, messages.INFO, '{}-{}-{}'.format(ids[0], ids[1], ids[2]))
                    return render(request, 'user/register.html', {'form': form, 'profile_form': profile_form})
        except:
            print(traceback.print_exc())
            return render(request, 'user/register.html', {"message": "There is some error!"})


def Signin(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}

    if request.method == 'GET':
        if request.user.is_authenticated:
            data = is_subscribed(request.user)
            return render(request, 'dashboard.html', {"context_key": context_key, "subscription": data})
        else:
            return render(request, 'user/login.html', {})

    elif request.method == 'POST':
        try:
            token = request.POST.get('token')
            email = request.POST.get('email')
        except:
            token = None
            email = None
        if token and email:
            user_plan = UserProfile.objects.get(user__email=email)
            if user_plan.plan == 'Monthly':
                plan_id = 'plan_HG6fCTjltYzi7i'   # basic monthly test plan id
                price = 'Monthly Plan $147.00'
                # s_amount = decimal.Decimal(397.00)
                # bonus = decimal.Decimal(79.4)
            else:
                plan_id = 'plan_HG6jeY9IIyUnHM'   # basic yearly test plan id
                price = 'Yearly Plan $1411.00'
                # s_amount = decimal.Decimal(3997.00)
                # bonus = decimal.Decimal(799.4)
            try:
                subs_new = dt.now() + timedelta(days=7)
                today = dt.timestamp(dt.now())
                start = dt.timestamp(subs_new)
                with transaction.atomic():
                    customer = stripe.Customer.create(
                        email=email,
                        source=token,
                    )
                    cus_id = customer.id
                    trial_subs = stripe.Subscription.create(
                        customer=customer,
                        items=[
                            {
                                #'plan': "plan_HDpAyYOz1b5xMN",  # $1 for a Year
                                'quantity': 1,
                                #'price':200
                            }
                        ],
                    )

                    if trial_subs.status == 'active':
                        subscription = stripe.Subscription.create(
                            customer=cus_id,
                            items=[
                                {
                                    #'plan': plan_id,
                                    'quantity': 1,
                                    #'price':200
                                }
                            ],
                            trial_end=subs_new,
                        )
                        user = User.objects.get(email=email)
                        if UserStripeDetail.objects.filter(user=user).exists():
                            UserStripeDetail.objects.filter(user=user).update(customer_id=cus_id,
                                                                              subscription_id=subscription.id,
                                                                              subscription_status='Subscribed',
                                                                              subscription_cancel_date=str(subscription.current_period_end),
                                                                              plan=user_plan.plan, stripe_token=token,
                                                                              trial_date=int(today), start_date=int(start))
                        else:
                            UserStripeDetail.objects.create(user=user, customer_id=cus_id,
                                                            subscription_id=subscription.id,
                                                            subscription_status='Subscribed',
                                                            subscription_cancel_date=str(
                                                                  subscription.current_period_end),
                                                            plan=user_plan.plan, stripe_token=token,
                                                            trial_date=int(today),
                                                            start_date=int(start))
                        # s_amount = decimal.Decimal(397.00)
                        # Revenue.objects.create(amount=s_amount)

                        # bonus = decimal.Decimal(79.4)
                        # qs_invite = InvitePayment.objects \
                        #     .filter(new_user=user.id, payment_status=0, balance=decimal.Decimal(0.0)) \
                        #     .update(payment_status=1, balance=bonus)
                        return render(request, 'user/login.html',
                                      {'message': user_plan.plan+" Subscription Successful!"})
                    else:
                        if cus_id:
                            stripe.Customer.delete(cus_id)
                        return render(request, 'user/register_plan.html',
                                      {'message': "There is some error with the Card!",'key': key, "email": email, "price": price})
            except stripe.error.CardError as e:
                body = e.json_body
                err = body['error']
                return render(request, 'user/register_plan.html',
                              {'message': err['message'], 'key': key, "email": email, "price": price})
            except stripe.error.RateLimitError as e:
                print(traceback.print_exc())
                body = e.json_body
                err = body['error']
                return render(request, 'user/register_plan.html',
                              {'message': err['message'], 'key': key, "email": email, "price": price})
            except stripe.error.InvalidRequestError as e:
                print(traceback.print_exc())
                body = e.json_body
                err = body['error']
                return render(request, 'user/register_plan.html',
                              {'message': err['message'], 'key': key, "email": email, "price": price})
            except stripe.error.AuthenticationError as e:
                print(traceback.print_exc())
                body = e.json_body
                err = body['error']
                return render(request, 'user/register_plan.html',
                              {'message': err['message'], 'key': key, "email": email, "price": price})
            except stripe.error.StripeError as e:
                print(traceback.print_exc())
                body = e.json_body
                err = body['error']
                return render(request, 'user/register_plan.html',
                              {'message': err['message'], 'key': key, "email": email, "price": price})
            except Exception as e:
                print(traceback.print_exc())
                return render(request, 'user/register_plan.html',
                              {'message': 'There is some error with the card!', 'key': key, "email": email, "price": price})
        else:
            pass
        try:

            form = UserLoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
                user_profile = UserProfile.objects.get(user=user)
                # if user_profile.plan != 'None' and not UserStripeDetail.objects.filter(user=user).exists():
                #     plan = user_profile.plan
                #     if plan == 'Monthly':
                #         price = 'Monthly Plan $147.00'
                #     else:
                #         price = 'Yearly Plan $1411.00'
                #     return render(request, 'user/register_plan.html',
                #                   {'message': "Please complete your profile by entering payment details before logIn!",
                #                    'key': key, "email": user.email, "price": price})
                if user:
                    user_profile = UserProfile.objects.get(user__email=form.cleaned_data['email'])
                    if user_profile.role.role_name == 'Sub User' and user_profile.email_verified == False:
                        return render(request, 'user/login.html', {"message": "Please verify your email!"})
                    if user_profile.role.role_name == 'Sub User' and user_profile.status == 'inactive':
                        return render(request, 'user/login.html', {"message": "Your account is Inactive!"})
                    else:
                        login(request, user)
                        if not form.cleaned_data['remember_me']:
                            request.session.set_expiry(300)
                        if not user_profile.profile_image:
                            user_profile.profile_image = "default_image.jpg"
                        if not Notification_Pill.objects.filter(user=request.user).exists():
                            Notification_Pill.objects.create(user=request.user)
                        if not CustomFieldsModel.objects.filter(user=request.user).exists():
                            CustomFieldsModel.objects.create(user=request.user)
                        if user_profile.role.role_name != "Sub User":
                            if not MembershipDetails.objects.filter(user=request.user).exists():
                                MembershipDetails.objects.create(user=request.user,
                                                                 membership_plan=MembershipPlan.objects.first(),
                                                                 subscription_end_date=date.today())
                            if not XForceSubscriptionDetails.objects.filter(user=request.user).exists():
                                XForceSubscriptionDetails.objects.create(user=request.user,
                                                                         xforce_membership_plan=XForceSubscriptionPlan.objects.first(),
                                                                         xforce_subscription_end_date=date.today())
                        try:
                            UserStats.objects.create(user=user)
                        except:
                            pass
                        return redirect('home')
                else:
                    return render(request, 'user/login.html', {"message": "Incorrect email or password!"})
            else:
                return render(request, 'user/login.html', {'form': form})
        except:
            print(traceback.format_exc())
            return render(request, 'user/login.html', {"message": "There is some error!"})


def UpdateProfile(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    if request.method == 'GET':
        if User.objects.filter(username=request.user.username).exists():
            user = User.objects.get(username=request.user.username)
            user_profile = UserProfile.objects.get(user__username=request.user.username)
            return render(request, 'user/profile.html', {'user_data': user, 'user_profile': user_profile,
                                                         "page": 'update_profile'})
        else:
            return render(request, 'user/profile.html', {"page": 'update_profile'})

    elif request.method == 'POST':
        try:
            form = UpdateProfileForm(request.POST)
            instance = get_object_or_404(UserProfile, user__username=request.user.username)
            profile_form = UpdateProfileForm2(request.POST, request.FILES, instance=instance)
            if form.is_valid() and profile_form.is_valid():
                if form.cleaned_data['email'] != request.user.email and User.objects.filter(
                        username=form.cleaned_data['email']).exists():
                    return render(request, 'user/profile.html',
                                  {"message": "Email already exists!", 'form': form, 'profile_form': profile_form,
                                   "context_key": context_key, "subscription": data})

                if request.user.email != form.cleaned_data['email']:
                    current_site = get_current_site(request)
                    content = "Your ProspectX account email has been changed successfully. Your new email is:"
                    ctx = {
                        'password': form.cleaned_data['email'],
                        'content': content,
                        'email_verification': 'None',
                        'user': request.user,
                        'domain': current_site.domain,
                    }
                    to_email_list = [request.user.email]
                    subject = "Prospectx"
                    html_message = render_to_string(
                        'user/CustomAlert.html', ctx)
                    plain_message = strip_tags(html_message)
                    from_email = settings.EMAIL_HOST_USER
                    send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                              fail_silently=False)
                User.objects.filter(username=request.user.username).update(first_name=form.cleaned_data['first_name'],
                                                                           last_name=form.cleaned_data['last_name'],
                                                                           email=form.cleaned_data['email'],
                                                                           username=form.cleaned_data['email'])
                profile_form.save()

                return render(request, 'user/profile.html', {'form': form, 'profile_form': profile_form,
                                                             'message': "Profile has been updated successfully!",
                                                             "page": 'update_profile'})
            else:
                return render(request, 'user/profile.html', {'form': form, 'profile_form': profile_form,
                                                             "page": 'update_profile'})
        except:
            print(traceback.print_exc())
            return render(request, 'user/profile.html', {"message": "There is some error!",
                                                         "page": 'update_profile'})


def list_management_view(request):
    prospect_lists = List.objects.filter(user=request.user).order_by('-id')
    list_data = []
    for lists in prospect_lists:
        sequence = ListSequence.objects.filter(list=lists)
        list_object = {
            "id": lists.id,
            "name": lists.list_name,
            "list_status": lists.list_status,
            "seq_id": "",
            "pulled_status": "",
            "pull_date": "",
        }
        if sequence:
            list_object["seq_id"] = sequence[0].id
            list_object["pulled_status"] = sequence[0].pulled_status
            list_object["pull_date"] = sequence[0].pull_date
        list_data.append(list_object)
    custom_fields_data = {"user_id": request.user.id, "custom1": "", "custom2": "", "custom3": "", "custom4": "",
                          "custom5": "", "custom6": "", "custom7": "", "custom8": "", "custom9": "", "custom10": ""}
    custom_fields = CustomFieldsModel.objects.filter(user=request.user)
    if custom_fields:
        custom_fields_data["custom1"] = custom_fields[0].custom1
        custom_fields_data["custom2"] = custom_fields[0].custom2
        custom_fields_data["custom3"] = custom_fields[0].custom3
        custom_fields_data["custom4"] = custom_fields[0].custom4
        custom_fields_data["custom5"] = custom_fields[0].custom5
        custom_fields_data["custom6"] = custom_fields[0].custom6
        custom_fields_data["custom7"] = custom_fields[0].custom7
        custom_fields_data["custom8"] = custom_fields[0].custom8
        custom_fields_data["custom9"] = custom_fields[0].custom9
        custom_fields_data["custom10"] = custom_fields[0].custom10
        custom_fields_data["user_id"] = custom_fields[0].user.id
    today_date = date.today().strftime('%m-%d-%Y')
    return render(request, 'user/list_management.html', {"page": 'list_management',
                                                         "prospect_lists": list_data,
                                                         "custom_fields_data": custom_fields_data,
                                                         "today_date": today_date})


class UpdateCustomFields(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        custom1 = request.data.get("custom1")
        custom2 = request.data.get("custom2")
        custom3 = request.data.get("custom3")
        custom4 = request.data.get("custom4")
        custom5 = request.data.get("custom5")
        custom6 = request.data.get("custom6")
        custom7 = request.data.get("custom7")
        custom8 = request.data.get("custom8")
        custom9 = request.data.get("custom9")
        custom10 = request.data.get("custom10")
        user_id = request.data.get("user_id")
        try:
            if custom1 and custom2 and custom3 and user_id:
                if CustomFieldsModel.objects.filter(user_id=user_id).exists():
                    CustomFieldsModel.objects.filter(user_id=user_id).update(custom1=custom1, custom2=custom2,
                                                                             custom3=custom3, custom4=custom4,
                                                                             custom5=custom5, custom6=custom6,
                                                                             custom7=custom7, custom8=custom8,
                                                                             custom9=custom9, custom10=custom10)
                    return redirect('/list_management')
                else:
                    CustomFieldsModel.objects.create(user_id=user_id, custom1=custom1, custom2=custom2, custom3=custom3,
                                                     custom4=custom4, custom5=custom5, custom6=custom6,
                                                     custom7=custom7, custom8=custom8, custom9=custom9,
                                                     custom10=custom10)

                    return redirect('/list_management')
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Failed",
                })
        except:
            print(traceback.print_exc())
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "There is some error!",
            })


def tags_management_view(request):
    tags_lists = Tag.objects.filter(user=request.user).order_by('-id')
    list_data = []
    for tag in tags_lists:
        tag_object = {
            "id": tag.id,
            "name": tag.tag_name,
            "tag_status": tag.tag_status,
            "tag_description": tag.tag_description,
        }
        list_data.append(tag_object)
    today_date = date.today().strftime('%Y-%m-%d')
    return render(request, 'user/tag_management.html', {"tags_list": list_data,
                                                        "today_date": today_date})


def create_new_tag_view(request):
    if request.method == 'POST':
        try:
            name = request.POST.get("name")
            description = request.POST.get("description")
            tag_status = request.POST.get("status")
            if name and status:
                if Tag.objects.filter(user=request.user, tag_name=name).exists():
                    return render(request, 'user/add_new_tag.html', {"user": request.user.id,
                                                                     "msg": "Tag Already Exists!"})
                elif name.isspace():
                    return render(request, 'user/add_new_tag.html', {"user": request.user.id,
                                                                     "msg": "Please give proper name to the tag!"})
                else:
                    Tag.objects.create(user=request.user, tag_name=name,
                                       tag_description=description, tag_status=tag_status)
                    return redirect('tags_management')
            else:
                return render(request, 'user/add_new_tag.html',
                              {"message": "There is some error!", "user": request.user})
        except:
            print(traceback.print_exc())
            return render(request, 'user/add_new_tag.html', {"message": "There is some error!", "user": request.user})
    else:
        return render(request, 'user/add_new_tag.html', {"user": request.user.id})


def update_tag_view(request, pk):
    if request.method == 'POST':
        try:
            name = request.POST.get("name")
            description = request.POST.get("description")
            tag_status = request.POST.get("status")
            if name and status:
                if Tag.objects.filter(~Q(id=pk)).filter(user=request.user, tag_name=name).exists():
                    tag = Tag.objects.get(id=pk)
                    return render(request, 'user/update_tag.html', {"user": request.user.id, "tag": tag,
                                                                    "msg": "Tag Already Exists!"})
                elif name.isspace():
                    tag = Tag.objects.get(id=pk)
                    return render(request, 'user/update_tag.html', {"user": request.user.id, "tag": tag,
                                                                    "msg": "Please give proper name to the tag!"})
                else:
                    Tag.objects.filter(id=pk).update(tag_name=name,
                                                     tag_description=description,
                                                     tag_status=tag_status)
                    return redirect('tags_management')
            else:
                return render(request, 'user/update_tag.html', {"message": "There is some error!"})
        except:
            print(traceback.print_exc())
            return render(request, 'user/update_tag.html', {"message": "There is some error!"})
    else:
        tag = Tag.objects.get(id=pk)
        return render(request, 'user/update_tag.html', {"tag": tag})


class CheckExistingTag(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        name = request.data.get("name")
        user_got = request.data.get("user")
        tag_status = request.data.get("tag_status")
        description = request.data.get("description")
        try:
            if name and user_got and tag_status:
                if Tag.objects.filter(user_id=user_got, tag_name=name).exists():
                    return Response({
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "Tag Already Exists!",
                    })
                else:
                    Tag.objects.create(user=user_got, tag_name=name,
                                       tag_description=description,
                                       tag_status=tag_status)
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "",
                    })
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Tag Already Exists!",
                })
        except:
            print(traceback.format_exc())
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Tag Already Exists!",
            })


class GetListSequence(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        ids = request.data.get("id")
        if ids:
            list_sequence = ListSequence.objects.get(id=ids)
            list_sequence_data = {
                "pull_every_day": list_sequence.list_pull_everyday,
                "pulled_status": list_sequence.pulled_status,
                "pull_date": list_sequence.pull_date,
            }
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Success",
                "list_sequence_data": list_sequence_data
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Failed",
                "list_sequence_data": ""
            })


class PullListManually(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            sequence_id = request.data.get("seq_id")
            list_id = request.data.get("list_id")
            if ListSequence.objects.filter(list_id=list_id).exists():
                ListSequence.objects.filter(id=sequence_id).update(pulled_status="Pulled",
                                                                   pull_date=datetime.date.today())
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Success",
                })
            else:
                ListSequence.objects.create(list_id=list_id, list_pull_everyday=0,
                                            pulled_status="Pulled", pull_date=datetime.date.today())
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Success",
                })
        except:
            print(traceback.format_exc())
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "error",
            })


class UpdateCreateSequence(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        list_id = request.data.get("list_id")
        sequence_id = request.data.get("sequence_id")
        pull_date = request.data.get("date")
        pulled = request.data.get("pulled")
        pull_every_day = request.data.get("pull_every_day")
        if list_id and list_id != '':
            if List.objects.filter(id=list_id).exists():
                list_got = List.objects.get(id=list_id)
                if sequence_id:
                    if ListSequence.objects.filter(id=sequence_id).exists():
                        ListSequence.objects.filter(id=sequence_id).update(list_pull_everyday=pull_every_day,
                                                                           pulled_status=pulled,
                                                                           pull_date=pull_date)
                        return Response({
                            "status": status.HTTP_200_OK,
                            "message": "Success",
                        })
                    else:
                        ListSequence.objects.create(list_pull_everyday=pull_every_day, pulled_status=pulled,
                                                    pull_date=pull_date, list=list_got)
                        return Response({
                            "status": status.HTTP_200_OK,
                            "message": "Success",
                        })
                else:
                    ListSequence.objects.create(list_pull_everyday=pull_every_day, pulled_status=pulled,
                                                pull_date=pull_date, list=list_got)
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Success",
                    })
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Failed",
                })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Failed",
            })


class ViewListDetail(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        list_id = request.data.get("id")
        list_data = {}
        if list_id:
            if List.objects.filter(id=list_id).exists():
                list_got = List.objects.get(id=list_id)
                list_data = {
                    "name": list_got.list_name,
                    "created_by": list_got.user.username,
                    "list_status": list_got.list_status,
                    "import_data": list_got.import_data,
                    "update_option": list_got.update_option,
                    "created_at": list_got.created_at,
                    "list_pull_everyday": "",
                    "pulled_status": "",
                    "pull_date": "",
                }
                if ListSequence.objects.filter(list=list_got).exists():
                    list_sequence = ListSequence.objects.get(list=list_got)
                    list_data["list_pull_everyday"] = list_sequence.list_pull_everyday
                    list_data["pulled_status"] = list_sequence.pulled_status
                    list_data["pull_date"] = list_sequence.pull_date
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Success",
                    "list_data": list_data,
                })
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Failed",
                    "list_data": list_data,
                })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Failed",
                "list_data": list_data,
            })


def delete_list_view(request, pk):
    if request.user.is_authenticated:
        try:
            abc = List.objects.filter(id=pk)
            abc.delete()
            return redirect('/list_management')
        except:
            print(traceback.print_exc())
            return redirect('/list_management')
    else:
        return redirect('/list_management')


def delete_tag_view(request, pk):
    if request.user.is_authenticated:
        try:
            Tag.objects.filter(id=pk).delete()
            return redirect('/tags_management')
        except:
            print(traceback.print_exc())
            return redirect('/tags_management')
    else:
        return redirect('/tags_management')


def add_new_list_view(request):
    if CustomFieldsModel.objects.filter(user=request.user).exists():
        custom_fields = CustomFieldsModel.objects.get(user=request.user)
    else:
        custom_fields = CustomFieldsModel.objects.create(user=request.user)
    return render(request, 'user/add_new_list.html', {"page": 'list_management',
                                                      "custom_fields": custom_fields})


def campaign_settings_view(request):
    return render(request, 'coming_soon_settings.html', )


def skiptrace_settings_view(request):
    return render(request, 'settings_coming_soon.html', )


def xforce_settings_view(request):
    return render(request, 'settings_coming_soon.html', )


def update_list_view(request, pk):
    if request.method == 'POST':
        pass
    else:
        list_data = List.objects.get(id=pk)
        if CustomFieldsModel.objects.filter(user=request.user).exists():
            custom_fields = CustomFieldsModel.objects.get(user=request.user)
        else:
            custom_fields = CustomFieldsModel.objects.create(user=request.user)
        return render(request, 'user/update_list.html', {"data": list_data,
                                                         "custom_fields": custom_fields})


def ChangePassword(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user__username=request.user.username)
    data = is_subscribed(request.user)
    if request.method == 'GET':
        return render(request, 'user/profile.html',
                      {'user_data': user, 'user_profile': user_profile, "context_key": context_key,
                       "subscription": data})

    elif request.method == 'POST':
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                current_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                confirm_new_password = form.cleaned_data['confirm_new_password']
                if request.user.check_password(current_password) is False:
                    data = {
                        'message': "Current Password Incorrect!"
                    }
                    return JsonResponse(data, status=400)
                if new_password == current_password:
                    data = {
                        'message': "Current and New Password are same!"
                    }
                    return JsonResponse(data, status=400)
                elif new_password != confirm_new_password:
                    data = {
                        'message': "Password and Confirm Password didn't match!"
                    }
                    return JsonResponse(data, status=400)
                elif new_password.isnumeric():
                    data = {
                        'message': "Your password cannot be entirely numeric!"
                    }
                    return JsonResponse(data, status=400)
                elif len(new_password) < 8:
                    data = {
                        'message': "Your password must contain at least 8 characters!"
                    }
                    return JsonResponse(data, status=400)

                User.objects.filter(username=request.user.username).update(password=make_password(new_password))
                user = User.objects.get(username=request.user.username)
                update_session_auth_hash(request, user)
                data = {
                    'message': "Password Changed Successfully!"
                }
                return JsonResponse(data)
            else:
                data = {
                    'message': "Please enter all fields!"
                }
                return JsonResponse(data, status=400)
        except:
            data = {
                'message': "There is some error!"
            }
            return JsonResponse(data, status=400)


def Home(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_role = user_profile.role.role_name
        if not user_profile.profile_image:
            user_profile.profile_image = "default_image.jpg"
            user_profile = user_profile.profile_image
        else:
            user_profile = user_profile.profile_image
        monthly = request.POST.get('monthly')
        yearly = request.POST.get('yearly')
        try:
            if not yearly:
                subs_new = dt.now() + timedelta(days=7)
                today = dt.timestamp(dt.now())
                start = dt.timestamp(subs_new)

                user = request.user
                token = request.POST['stripeToken']
                if UserStripeDetail.objects.filter(user=user, stripe_token=token).exists():
                    return render(request, 'dashboard.html',
                                  {"context_key": context_key, "subscription": data, "role": user_role,
                                   'user_profile': user_profile})
                with transaction.atomic():

                    if UserStripeDetail.objects.filter(user=user).exists():
                        details = UserStripeDetail.objects.filter(user=user)
                        stripe.Customer.delete(details[0].customer_id)
                        customer = stripe.Customer.create(
                            email=user.email,
                            source=token,
                        )
                    else:
                        customer = stripe.Customer.create(
                            email=user.email,
                            source=token,
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
                                                                          subscription_id=subscription.id,
                                                                          subscription_status='Subscribed',
                                                                          subscription_cancel_date=str(
                                                                              subscription.current_period_end),
                                                                          plan='Monthly', trial_date=int(today),
                                                                          start_date=int(start),
                                                                          cancelled_before_starting=False)
                        s_amount = decimal.Decimal(147.00)
                        Revenue.objects.create(amount=s_amount)

                    else:
                        UserStripeDetail.objects.create(user=user, stripe_token=token, customer_id=customer.id,
                                                        subscription_id=subscription.id, subscription_status='Subscribed',
                                                        subscription_cancel_date=str(subscription.current_period_end),
                                                        plan='Monthly', trial_date=int(today), start_date=int(start))
                        s_amount = decimal.Decimal(147.00)
                        Revenue.objects.create(amount=s_amount)

                    bonus = decimal.Decimal(29.4)
                    qs_invite = InvitePayment.objects \
                        .filter(new_user=user.id, payment_status=0, balance=decimal.Decimal(0.0)) \
                        .update(payment_status=1, balance=bonus)

                    data = is_subscribed(request.user)
                    return render(request, 'dashboard.html',
                                  {"context_key": context_key, "subscription": data, "role": user_role,
                                   'user_profile': user_profile})

            elif not monthly:
                subs_new = dt.now() + timedelta(days=7)
                today = dt.timestamp(dt.now())
                start = dt.timestamp(subs_new)

                user = request.user
                token = request.POST['stripeToken']
                if UserStripeDetail.objects.filter(user=user, stripe_token=token).exists():
                    return render(request, 'dashboard.html',
                                  {"context_key": context_key, "subscription": data, "role": user_role,
                                   'user_profile': user_profile})
                with transaction.atomic():
                    # user = User.objects.get(id=user_id)
                    if UserStripeDetail.objects.filter(user=user).exists():
                        details = UserStripeDetail.objects.filter(user=user)
                        stripe.Customer.delete(details[0].customer_id)
                        customer = stripe.Customer.create(
                            email=user.email,
                            source=token,
                        )
                    else:
                        customer = stripe.Customer.create(
                            email=user.email,
                            source=token,
                        )

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
                                                                              subscription.current_period_end),
                                                                          plan='Yearly', trial_date=int(today),
                                                                          start_date=int(start),
                                                                          cancelled_before_starting=False)
                        s_amount = decimal.Decimal(1411.00)
                        Revenue.objects.create(amount=s_amount)

                    else:
                        UserStripeDetail.objects.create(user=user, stripe_token=token, customer_id=customer.id,
                                                        subscription_id=subscription.id, subscription_status='Subscribed',
                                                        subscription_cancel_date=str(subscription.current_period_end),
                                                        plan='Yearly', trial_date=int(today), start_date=int(start))
                        s_amount = decimal.Decimal(1411.00)
                        Revenue.objects.create(amount=s_amount)

                    bonus = decimal.Decimal(282.2)
                    qs_invite = InvitePayment.objects \
                        .filter(new_user=user.id, payment_status=0, balance=decimal.Decimal(0.0)) \
                        .update(payment_status=1, balance=bonus)
                    data = is_subscribed(request.user)
                    return render(request, 'dashboard.html',
                                  {"context_key": context_key, "subscription": data, "role": user_role,
                                   'user_profile': user_profile})
            else:
                data = is_subscribed(request.user)
                return render(request, 'dashboard.html',
                              {"context_key": context_key, "subscription": data, "role": user_role,
                               'user_profile': user_profile})
        except:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            key = settings.STRIPE_PUBLISHABLE_KEY
            context_key = {'key': key}
            data = {"subscribed": "yes", }
            user_profile = UserProfile.objects.get(user=request.user)
            user_role = user_profile.role.role_name
            if not user_profile.profile_image:
                user_profile.profile_image = "default_image.jpg"
                user_profile = user_profile.profile_image
            else:
                user_profile = user_profile.profile_image
            return render(request, 'dashboard.html',
                          {"context_key": context_key, "subscription": data, "role": user_role,
                           'user_profile': user_profile})
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        key = settings.STRIPE_PUBLISHABLE_KEY
        context_key = {'key': key}
        data = is_subscribed(request.user)
        user_profile = UserProfile.objects.get(user=request.user)
        user_role = user_profile.role.role_name
        if not user_profile.profile_image:
            user_profile.profile_image = "default_image.jpg"
            user_profile = user_profile.profile_image
        else:
            user_profile = user_profile.profile_image
        return render(request, 'dashboard.html', {"context_key": context_key, "subscription": data, "role": user_role,
                                                  'user_profile': user_profile})


def Logout(request):
    if request.method == 'GET':
        send_event('prospectx' + str(request.user.id), 'message', 'logout')
        logout(request)
        return render(request, 'user/login.html', {})


def getSubUser(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    if request.method == 'GET':
        subUsers = UserProfile.objects.filter(created_by__user=request.user)
        context = {'subUsers': subUsers, "context_key": context_key, "subscription": data}
        return render(request, "user/users.html", context)


def registerSubUser(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    if request.method == 'GET':
        return render(request, 'user/addSubUser.html', {"context_key": context_key, "subscription": data})

    elif request.method == 'POST':
        ran_password = ''
        try:
            form = AddUserForm(request.POST)
            profile_form = AddProfileForm(request.POST)
            permission_form = PermissionForm(request.POST)
            if form.is_valid() and profile_form.is_valid() and permission_form.is_valid():
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                random_check = permission_form.cleaned_data['random_password']
                email_verified = permission_form.cleaned_data['activation_email']
                current_site = get_current_site(request)

                if random_check:
                    ran_password = User.objects.make_random_password()
                    user.password = make_password(ran_password)

                user.save()
                permission = permission_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.permissions = permission
                profile.created_by = UserProfile.objects.get(user=request.user)
                profile.role = Role.objects.get(id=3)
                if email_verified:
                    profile.email_verified = False
                profile.save()
                Notification_Pill.objects.create(user=user)
                type = 'new'
                users = [request.user, user]
                sub_user = user
                if random_check:
                    password_param = ran_password
                else:
                    password_param = form.cleaned_data['password1']

                for obj in users:
                    role = UserProfile.objects.get(user=obj).role.role_name
                    sendEmail(obj, password_param, type, email_verified, current_site, role, sub_user)

                subUsers = UserProfile.objects.filter(created_by__user=request.user)
                context = {'subUsers': subUsers, "context_key": context_key, "subscription": data}
                return render(request, 'user/users.html', context)
            else:
                return render(request, 'user/addSubUser.html',
                              {'form': form, 'profile_form': profile_form, 'permission_form': permission_form,
                               "context_key": context_key, "subscription": data
                               })
        except:
            print(traceback.print_exc())
            return render(request, 'user/addSubUser.html', {"message": "There is some error!",
                                                            "context_key": context_key, "subscription": data})


def deleteSubUser(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    user = User.objects.get(pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    permission_obj = user_profile.permissions
    Permissions.objects.filter(pk=permission_obj.pk).delete()
    User.objects.filter(pk=pk).delete()
    subUsers = UserProfile.objects.filter(created_by__user=request.user)
    context = {'subUsers': subUsers, "context_key": context_key, "subscription": data}
    return render(request, "user/users.html", context)


def updateSubUser(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    if request.method == 'GET':
        try:
            subuser = UserProfile.objects.get(id=pk, created_by__user=request.user)
            user = subuser.user
            permission = subuser.permissions
            return render(request, 'user/updateSubUser.html',
                          {'subuser': subuser, 'userr': user, 'permission': permission,
                           "context_key": context_key, "subscription": data})
        except:
            subUsers = UserProfile.objects.filter(created_by__user=request.user)
            context = {'subUsers': subUsers, 'message': "There was some error.", "context_key": context_key,
                       "subscription": data}
            return render(request, 'user/users.html', context)

    elif request.method == 'POST':
        try:
            form = UpdateUserForm(request.POST)
            profile_form = AddProfileForm(request.POST)
            permission_form = PermissionForm(request.POST)

            subUsers = UserProfile.objects.filter(created_by__user=request.user)
            subuser = UserProfile.objects.get(id=pk, created_by__user=request.user)
            if form.is_valid() and profile_form.is_valid() and permission_form.is_valid():
                random_check = permission_form.cleaned_data['random_password']

                profile_obj = UserProfile.objects.get(pk=pk)
                user_obj = profile_obj.user
                permission_obj = profile_obj.permissions
                if random_check:
                    ran_password = User.objects.make_random_password()
                    User.objects.filter(username=user_obj.username).update(first_name=form.cleaned_data['first_name'],
                                                                           last_name=form.cleaned_data['last_name'],
                                                                           email=form.cleaned_data['email'],
                                                                           username=form.cleaned_data['email'],
                                                                           password=make_password(ran_password))

                else:
                    pass1 = form.cleaned_data['password1']
                    if pass1 == "":
                        User.objects.filter(username=user_obj.username).update(
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            username=form.cleaned_data['email'])
                    else:
                        User.objects.filter(username=user_obj.username).update(
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            username=form.cleaned_data['email'],
                            password=make_password(
                                form.cleaned_data['password1']))

                UserProfile.objects.filter(pk=profile_obj.pk).update(
                    cell_phone=profile_form.cleaned_data['cell_phone'],
                    status=profile_form.cleaned_data['status'])
                Permissions.objects.filter(pk=permission_obj.pk).update(
                    random_password=permission_form.cleaned_data['random_password'],
                    marketing_plan=permission_form.cleaned_data['marketing_plan'],
                    skip_trace=permission_form.cleaned_data['skip_trace'],
                    list_management=permission_form.cleaned_data['list_management'],
                    access_import_log=permission_form.cleaned_data['access_import_log'],
                    access_export_log=permission_form.cleaned_data['access_export_log'],
                    access_tag_log=permission_form.cleaned_data['access_tag_log'],
                    access_xsite=permission_form.cleaned_data['access_xsite'],
                    access_xforce=permission_form.cleaned_data['access_xforce'],
                    lead_manager=permission_form.cleaned_data['lead_manager'],
                    transaction_manager=permission_form.cleaned_data['transaction_manager'],
                    disposition_manager=permission_form.cleaned_data['disposition_manager']

                )
                permissions_check(Permissions.objects.get(pk=permission_obj.pk))
                user = User.objects.get(username=form.cleaned_data['email'])
                current_site = get_current_site(request)
                type = 'update'
                users = [request.user, user]
                sub_user = user
                if random_check:
                    pwd_param = ran_password
                else:
                    pwd_param = form.cleaned_data['password1']
                if random_check or form.cleaned_data['password1'] != "":
                    for obj in users:
                        role = UserProfile.objects.get(user=obj).role.role_name
                        sendEmail(obj, pwd_param, type, False, current_site, role, sub_user)
                context = {'subUsers': subUsers, "context_key": context_key, "subscription": data}
                return render(request, 'user/users.html', context)
            else:
                return render(request, 'user/updateSubUser.html',
                              {'form': form, 'profile_form': profile_form, 'permission_form': permission_form,
                               'subuser': subuser, "context_key": context_key, "subscription": data})
        except:
            return render(request, 'user/updateSubUser.html',
                          {"message": "There is some error!", "context_key": context_key, "subscription": data})


def DashBoard(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)

    if request.method == "GET":
        blocks = Dashboard.objects.all().order_by('id')
        return render(request, 'user/manage_dashboard.html',
                      {"context_key": context_key, "subscription": data, 'blocks': blocks})


def AddBlock(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)

    if request.method == "GET":
        return render(request, 'user/addblock.html',
                      {"context_key": context_key, "subscription": data})
    elif request.method == "POST":
        form = AddBlockForm(request.POST)
        try:
            if form.is_valid():
                block = form.save(commit=False)
                block.save()
                blocks = Dashboard.objects.all().order_by('id')
                return render(request, 'user/manage_dashboard.html',
                              {"context_key": context_key, "subscription": data, "blocks": blocks})
            else:

                return render(request, 'user/addblock.html',
                              {"context_key": context_key, "subscription": data, 'form': form})
        except:
            return render(request, 'user/addblock.html',
                          {"context_key": context_key, "subscription": data, 'message': 'There is some error!'})


def UpdateBlock(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)

    if request.method == "GET":
        block = Dashboard.objects.get(pk=pk)
        return render(request, 'user/updateblock.html',
                      {"context_key": context_key, "subscription": data,
                       'block_title': block.block_title,
                       'block_width': block.block_width,
                       'block_content': block.block_content,
                       'block_image': block.block_image})
    elif request.method == "POST":
        form = AddBlockForm(request.POST)
        try:
            if form.is_valid():
                Dashboard.objects.filter(pk=pk).update(block_title=form.cleaned_data['block_title'],
                                                       block_width=form.cleaned_data['block_width'],
                                                       # str(
                                                       #     float(form.cleaned_data['block_width'][:-1]) - 1) + "%",
                                                       block_content=form.cleaned_data['block_content'],
                                                       block_image=form.cleaned_data['block_image'])

                blocks = Dashboard.objects.all().order_by('id')
                return render(request, 'user/manage_dashboard.html',
                              {"context_key": context_key, "subscription": data, "blocks": blocks})
            else:

                return render(request, 'user/addblock.html',
                              {"context_key": context_key, "subscription": data, 'form': form})
        except:
            return render(request, 'user/addblock.html',
                          {"context_key": context_key, "subscription": data, 'message': 'There is some error!'})


def DeleteBlock(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    try:
        Dashboard.objects.filter(pk=pk).delete()
        blocks = Dashboard.objects.all().order_by('id')
        return render(request, 'user/manage_dashboard.html',
                      {"context_key": context_key, "subscription": data, "blocks": blocks})
    except:
        blocks = Dashboard.objects.all()
        return render(request, 'user/manage_dashboard.html',
                      {"context_key": context_key, "subscription": data, "blocks": blocks,
                       'message': "There is some error!"})


def WelcomeEmailView(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)

    if request.method == "GET":
        email_template = WelcomeEmail.objects.get(pk=1)

        users = User.objects.filter(
            id__in=UserProfile.objects.filter(role__role_name="Admin User").values_list('user__pk'))
        content = EmailContent.objects.get(id=1).email_content
        return render(request, 'user/manage_welcome_email.html',
                      {"context_key": context_key, "subscription": data,
                       'email_from': email_template.email_from,
                       'email_content': email_template.email_content, "email_content2": content, 'users': users})
    elif request.method == "POST":
        form = EmailTemplateForm(request.POST)
        try:
            if form.is_valid():
                WelcomeEmail.objects.filter(pk=1).update(email_from=form.cleaned_data['email_from'],
                                                         email_content=form.cleaned_data['email_content'])

                email_template = WelcomeEmail.objects.get(pk=1)
                users = User.objects.all().exclude(email=request.user.email)
                messages.add_message(request, messages.INFO, 'Email content updated successfully!')
                return render(request, 'user/manage_welcome_email.html',
                              {"context_key": context_key, "subscription": data,
                               'email_from': email_template.email_from,
                               'email_content': email_template.email_content, 'users': users})
            else:
                email_template = WelcomeEmail.objects.get(pk=1)
                users = User.objects.all().exclude(email=request.user.email)
                messages.add_message(request, messages.INFO, 'There is some error!')
                return render(request, 'user/manage_welcome_email.html',
                              {"context_key": context_key, "subscription": data,
                               'email_from': email_template.email_from,
                               'email_content': email_template.email_content, 'form': form.errors, 'users': users})
        except:
            users = User.objects.all().exclude(email=request.user.email)
            messages.add_message(request, messages.INFO, 'There is some error!')
            return render(request, 'user/manage_welcome_email.html',
                          {'email_from': email_template.email_from,
                           'email_content': email_template.email_content, 'users': users,
                           'message': 'There is some error!'})


def SendEmailView(request):
    form = SendEmailTemplateForm(request.POST)
    try:
        if form.is_valid():
            content = form.cleaned_data['email_content']
            ctx = {
                'content': content,
            }
            to_email_list = request.POST.getlist('email_to')
            subject = "Prospectx"
            html_message = render_to_string(
                'user/Welcome_Email_Template.html', ctx)
            plain_message = strip_tags(html_message)
            from_email = form.cleaned_data['email_from']
            send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                      fail_silently=False)
            EmailContent.objects.update(email_content=content)
            messages.add_message(request, messages.INFO, 'Email sent successfully!')
            return redirect("manage_welcome_email")
        else:
            messages.add_message(request, messages.INFO, 'There was an error!')
            return redirect("manage_welcome_email")
    except:
        messages.add_message(request, messages.INFO, 'There was an error!')
        return redirect("manage_welcome_email")


def get_admin_users(request, filter):
    try:
        if filter == "all":
            users_list = User.objects.filter(
                id__in=UserProfile.objects.filter(role__role_name="Admin User").values_list('user__pk'))
        elif filter == "paid":
            users = User.objects.filter(
                id__in=UserProfile.objects.filter(role__role_name="Admin User").values_list('user__pk'))
            users_list = []
            for user in users:
                if UserStripeDetail.objects.filter(Q(user__id=user.pk) & Q(subscription_status="Subscribed")).exists():
                    users_list.append(user)
                elif UserStripeDetail.objects.filter(Q(user__id=user.pk) &
                                                     Q(subscription_status="Cancelled") &
                                                     Q(subscription_cancel_date__gt=date.today())).exists():
                    users_list.append(user)
        else:
            users = User.objects.filter(
                id__in=UserProfile.objects.filter(role__role_name="Admin User").values_list('user__pk'))
            users_list = []
            for user in users:
                if not UserStripeDetail.objects.filter(user__id=user.pk).exists():
                    users_list.append(user)
                elif UserStripeDetail.objects.filter(Q(user__id=user.pk) & Q(subscription_status="Cancelled") & Q(
                        subscription_cancel_date__lte=date.today())).exists():
                    users_list.append(user)
        users = users_list
        serializer = UserSerializer(users, many=True)
        return JsonResponse({"users": serializer.data})
    except:
        print(traceback.print_exc())
        return JsonResponse({"message": "There is some error!"}, status=400)


def revenue_view(request):
    res = []
    if request.method == 'GET':
        end_date = datetime.datetime.today()
        start_date = datetime.datetime.today() - timedelta(days=30)
        qs = Revenue.objects.all().filter(created_at__range=[start_date.date(), end_date.date()])
        total = qs.aggregate(Sum('amount'))
        ls_dr = {}
        for dt in qs:
            amnt = float(dt.amount)
            dat = str(dt.created_at.date())
            if dat in ls_dr:
                ls_dr[dat] = ls_dr[dat] + amnt
            else:
                ls_dr[dat] = amnt
        for key in ls_dr.keys():
            res.append({'x': key, 'y': ls_dr[key]})
        return render(request, 'revenue.html', {"data": res, "total": total['amount__sum']})

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        qs = Revenue.objects.all().filter(created_at__range=[start_date, end_date])
        ls_dr = {}
        for dt in qs:
            amnt = float(dt.amount)
            dat = str(dt.created_at.date())
            if dat in ls_dr:
                ls_dr[dat] = ls_dr[dat] + amnt
            else:
                ls_dr[dat] = amnt
        for key in ls_dr.keys():
            res.append({'x': key, 'y': ls_dr[key]})
        return JsonResponse({'data': res})


class StripeWebhook(APIView):
    def post(self, request):
        try:
            print("yes webhook running")
            stripe.api_key = settings.STRIPE_SECRET_KEY

            event_json = json.loads(request.body)
            print("webhook: ", event_json)
            if event_json['type'] == 'charge.succeeded':
                print("charge succeeded", event_json['id'])

            if event_json['type'] == "invoice.payment_failed":
                print("invoice payment failed", event_json['id'])
                subscription = event_json['data']['object']['lines']['data'][0]['subscription']
                print("subscription id ", subscription)
                cust = event_json['data']['object']['customer']
                if UserStripeDetail.objects.filter(customer_id=cust).exists():
                    customer = UserStripeDetail.objects.filter(customer_id=cust)
                    if customer[0].user.email:
                        email_from = settings.EMAIL_HOST_USER
                        message_body = get_template('email_webhook.html').render({'messsage': " "})
                        sendemail = EmailMessage("Transaction Failed!", message_body, email_from,
                                                 [customer[0].user.email, ])
                        sendemail.content_subtype = 'html'
                        sendemail.send()

                        messagebody = get_template('email_webhook_owner.html').render(
                            {'Username': customer[0].user.username, 'Email': customer[0].user.email,
                             'Subscription_ID': subscription})
                        emailSend = EmailMessage("User Transaction Failed!", messagebody, email_from,
                                                 [email_from, ])
                        emailSend.content_subtype = 'html'
                        emailSend.send()
                else:
                    pass

            if event_json['type'] == "invoice.payment_succeeded":
                print("invoice payment succeeded", event_json['id'])

            if event_json['type'] == 'charge.failed':
                print("charge failed", event_json['id'])
                cust = event_json['data']['object']['source']['customer']
                if UserStripeDetail.objects.filter(customer_id=cust).exists():
                    customer = UserStripeDetail.objects.filter(customer_id=cust)
                    if customer[0].user.email:
                        email_from = settings.EMAIL_HOST_USER
                        # message_body = get_template('email_webhook.html').render({'messsage': " "})
                        sendemail = EmailMessage("Transaction Failed!", "message_body", email_from,
                                                 [customer[0].user.email, ])
                        sendemail.content_subtype = 'html'
                        sendemail.send()

                        messagebody = get_template('email_webhook_owner.html').render(
                            {'Username': customer[0].user.username, 'Email': customer[0].user.email,
                             'Subscription_ID': subscription})
                        emailSend = EmailMessage("User Transaction Failed!", messagebody, email_from,
                                                 [email_from, ])
                        emailSend.content_subtype = 'html'
                        emailSend.send()
                else:
                    pass

            return Response({"status": status.HTTP_200_OK})

        except:
            print("there is some issue")
            print(traceback.print_exc())
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR})



