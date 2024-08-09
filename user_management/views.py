import traceback
from datetime import date

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from filter_prospects.models import CustomFieldsModel
from notification.models import Notification_Pill
from user.forms import UpdateProfileForm, UpdateProfileForm2
from user.models import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

from xsiteApp.models import MembershipDetails, MembershipPlan
from .models import *
from django.conf import settings
import stripe
from payments.views import is_subscribed

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@login_required
def GetSubAdminDetail(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    admin_users = UserProfile.objects.filter(role__role_name='Admin User')
    users_ls = []
    for usr in admin_users:
        try:
            stus = is_subscribed(usr.user_id)
            if stus['subscribed'] == 'yes':
                status = 'Active'
            else:
                status = 'In Active'
        except:
            status = 'In Active'
        res = {'first_name': usr.user.first_name, 'last_name': usr.user.last_name, 'email': usr.user.email,
               'skiptrace_price': usr.skiptrace_price, 'bulk_skiptrace_price': usr.bulk_skiptrace_price,
               'status': status, 'user_id': usr.user.id}
        users_ls.append(res)

    context = {'admin_users': users_ls, "context_key": context_key, "subscription": data}

    if request.method == 'POST':
        print('here it is found', request.user)

    return render(request, 'user/admin_users.html', context)


@login_required
def update_skiptrace_price(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            price = request.POST.get('price')
            bulk_price = request.POST.get('bulk_price')
            UserProfile.objects.filter(user_id=pk).update(skiptrace_price=price, bulk_skiptrace_price=bulk_price)
            return redirect('/user/sub-admins-detail')
        else:
            return redirect('/user/sub-admins-detail')
    else:
        data = UserProfile.objects.filter(user_id=pk)
        return render(request, 'user/skiptrace_pricing.html', {"data": data[0]})


@login_required
def UserDelete(request, pk, msg, page):
    if msg.lower() == "yes":
        if User.objects.filter(pk=pk).exists():
            User.objects.filter(pk=pk).delete()
            messages.add_message(request, messages.INFO, 'User has been deleted successfully')
        else:
            messages.add_message(request, messages.INFO, 'User does not exist')
    else:
        messages.add_message(request, messages.INFO, str(page))
    next_page = request.GET['next']
    return redirect(next_page)


@login_required
def UserLogin(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    print("ener user")
    user = UserProfile.objects.get(user=request.user)
    user_role = user.role
    user_id = request.user.id
    print("user id: ", user_id)

    user = get_object_or_404(User, pk=pk)
    if user:
        # context = {'user_role': user_role, 'user_id':request.user.id, "context_key": context_key, "subscription": data}
        login(request, user)
        user_profile = UserProfile.objects.get(user__email=user.email)
        if not user_profile.profile_image:
            user_profile.profile_image = "default_image.jpg"
        if not Notification_Pill.objects.filter(user=user).exists():
            Notification_Pill.objects.create(user=user)
        if not CustomFieldsModel.objects.filter(user=user).exists():
            CustomFieldsModel.objects.create(user=user)
        if user_profile.role.role_name != "Sub User":
            if not MembershipDetails.objects.filter(user=request.user).exists():
                MembershipDetails.objects.create(user=request.user,
                                                 membership_plan=MembershipPlan.objects.first(),
                                                 subscription_end_date=date.today())
        data = is_subscribed(user)
        enable_back = True
        context = {'user_role': user_role, 'user_id': user_id,
                   "context_key": context_key, "subscription": data, "enable_back": enable_back}
        return render(request, 'dashboard.html', context)
    else:
        print("sub admin view")
        return redirect('sub-admin')


@login_required
def ChangeUserPassword(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        password = request.POST['User_password']
        confirm_password = request.POST['User_confirmPassword']
        if password == confirm_password:
            new_password = make_password(password)
            user.password = new_password
            user.save()
            update_session_auth_hash(request, user)
            current_site = get_current_site(request)
            content = "Your ProspectX password has been changed by the administration. Your new password is:"
            ctx = {
                'password': password,
                'content': content,
                'email_verification': 'None',
                'user': user,
                'domain': current_site.domain,
            }
            to_email_list = [user.email]
            subject = "Prospectx"
            html_message = render_to_string(
                'user/CustomAlert.html', ctx)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                      fail_silently=False)
            messages.add_message(request, messages.SUCCESS, "Password has been updated successfully")
        else:
            messages.add_message(request, messages.INFO, "Password doesn't match")
            print(request.path_info)
            return HttpResponseRedirect(request.path_info)

    return render(request, 'user/change-user-password.html', {"context_key": context_key, "subscription": data})


@login_required
def profile(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        if password:
            if check_password(password, request.user.password):
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.email = email
                request.user.save()
                messages.add_message(request, messages.SUCCESS, "Profile has been updated successfully")
            else:
                messages.add_message(request, messages.SUCCESS, "Incorrect Password")
        else:
            pass

    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    context = {'first_name': first_name, 'last_name': last_name, 'email': email,
               "context_key": context_key, "subscription": data}
    return render(request, 'user/superadmin_profile.html', context)
#
# @login_required
# def superDashboard(request):
#     login(request, request.user)
#     return render(request, 'dashboard.html')


def UpdateUserProfile(request, pk):
    user = User.objects.get(pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'GET':
        if User.objects.filter(pk=pk).exists():

            return render(request, 'user/User2profile.html', {'user_data': user, 'user_profile': user_profile,
                                                              "page": 'update_profile'})
        else:
            return render(request, 'user/User2profile.html', {"page": 'update_profile'})

    elif request.method == 'POST':
        try:
            user = User.objects.get(pk=pk)
            form = UpdateProfileForm(request.POST)
            instance = get_object_or_404(UserProfile, user=user)
            profile_form = UpdateProfileForm2(request.POST, request.FILES, instance=instance)

            if form.is_valid() and profile_form.is_valid():
                if form.cleaned_data['email'] != user.email and User.objects.filter(
                        username=form.cleaned_data['email']).exists():
                    return render(request, 'user/profile.html',
                                  {"message": "Email already exists!", 'form': form, 'profile_form': profile_form,
                                   })
                if user.email != form.cleaned_data['email']:
                    print("in mail change")
                    current_site = get_current_site(request)
                    content = "Your ProspectX account email has been changed by the administration. Your new email is:"
                    ctx = {
                        'password': form.cleaned_data['email'],
                        'content': content,
                        'email_verification': 'None',
                        'user': user,
                        'domain': current_site.domain,
                    }
                    to_email_list = [user.email]
                    subject = "Prospectx"
                    html_message = render_to_string(
                        'user/CustomAlert.html', ctx)
                    plain_message = strip_tags(html_message)
                    from_email = settings.EMAIL_HOST_USER
                    send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                              fail_silently=False)
                User.objects.filter(pk=pk).update(first_name=form.cleaned_data['first_name'],
                                                  last_name=form.cleaned_data['last_name'],
                                                  email=form.cleaned_data['email'],
                                                  username=form.cleaned_data['email'])
                profile_form.save()

                admin_users = UserProfile.objects.filter(role__role_name='Admin User')
                context = {
                    'admin_users': admin_users
                }
                return render(request, 'user/admin_users.html', context)
            else:
                return render(request, 'user/User2profile.html', {'form': form, 'profile_form': profile_form,
                                                                  'user_data': user, 'user_profile': user_profile,
                                                                  "page": 'update_profile'})
        except:
            print(traceback.print_exc())
            return render(request, 'user/User2profile.html', {"message": "There is some error!",
                                                              "page": 'update_profile'})
