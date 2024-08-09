from django.forms import formset_factory, modelformset_factory
import stripe
from django.conf import settings
from datetime import date, datetime
from notification.models import Notification, Notification_Pill

stripe.api_key = settings.STRIPE_SECRET_KEY
from user.models import *
from payments.views import is_subscribed
from filter_prospects.models import List, CustomFieldsModel, Prospect_Properties
from task_management.forms import CreateReminderForm
from task_management.models import Reminder
from user.models import UserProfile, Dashboard


def context(request):
    total_admin_users = 0
    # total_sub_users = 0
    # total_active_sub_users = 0
    # total_inactive_sub_users = 0
    role = 'Admin User'
    userData = UserProfile.objects.none()
    dashboard_data = Dashboard.objects.none()
    lists = List.objects.none()
    image = "media/user_images/default_image.jpg"
    myuser = UserProfile.objects.none()
    permissions = Permissions.objects.none()
    customfields = CustomFieldsModel.objects.none()
    notification = Notification.objects.none()
    pills = Notification_Pill.objects.none()
    first_name = None

    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = None
    data = False

    if request.user.is_authenticated:
        # total_admin_users = len(UserProfile.objects.filter(role__role_name='Admin User'))
        # total_sub_users = len(UserProfile.objects.filter(role__role_name='Sub User'))
        # total_active_sub_users = len(UserProfile.objects.filter(role__role_name='Sub User', status='active', created_by__user=request.user))
        # total_inactive_sub_users = len(UserProfile.objects.filter(role__role_name='Sub User', status='inactive', created_by__user=request.user))
        if UserProfile.objects.filter(user=request.user).exists():
            user = UserProfile.objects.get(user=request.user)
            role = user.role.role_name
            first_name = request.user.first_name if request.user.first_name else request.user.username
            image = UserProfile.objects.get(user=request.user).profile_image.url
            permissions = UserProfile.objects.get(user=request.user).permissions
            if role == 'Admin User':
                if UserStripeDetail.objects.filter(user=request.user, subscription_status="Cancelled").exists():
                    monthly_subscription = UserStripeDetail.objects.get(user=request.user, subscription_status="Cancelled")
                    if date.today() >= monthly_subscription.subscription_end_date:
                        Permissions.objects.filter(pk=user.permissions.id).update(marketing_plan=False,
                                                                                  skip_trace=False,
                                                                                  list_management=False,
                                                                                  access_import_log=False,
                                                                                  access_export_log=False,
                                                                                  access_tag_log=False)

        userData = UserProfile.objects.filter(created_by__user=request.user, role__role_name="Sub User")
        if CustomFieldsModel.objects.filter(user=request.user).exists():
            customfields = CustomFieldsModel.objects.get(user=request.user)
        lists = List.objects.filter(user=request.user)
        dashboard_data = Dashboard.objects.all().order_by('id')
        try:
            user_stats = UserStats.objects.get(user=request.user)
        except:
            user_stats = UserStats.objects.create(user=request.user)
        # if role == "Super User":
        for dashboard in dashboard_data:
            content = dashboard.block_content
            content = content.replace('%prospects%', str(user_stats.prospect_count))
            content = content.replace('%opted_out%', str(user_stats.opted_out_count))
            content = content.replace('%vacants%', str(user_stats.vacant_count))
            content = content.replace('%absentee%', str(user_stats.absentee_count))
            dashboard.block_content = content
        total_admin_users = user_stats.total_users_count
        # else:
        #     for dashboard in dashboard_data:
        #         content = dashboard.block_content
        #         content = content.replace('%prospects%', str(len(Prospect_Properties.objects.filter(list__user=request.user).distinct('propertyaddress'))))
        #         content = content.replace('%opted_out%', str(len(Prospect_Properties.objects.filter(list__user=request.user, opt_out="yes").distinct('propertyaddress'))))
        #         content = content.replace('%vacants%', str(len(Prospect_Properties.objects.filter(list__user=request.user, vacant=True).distinct('propertyaddress'))))
        #         content = content.replace('%absentee%', str(len(Prospect_Properties.objects.filter(list__user=request.user, absentee=True).distinct('propertyaddress'))))
        #         dashboard.block_content = content
        # myuser = UserProfile.objects.filter(user=request.user)
        notification = Notification.objects.filter(user=request.user).order_by('-id')
        if Notification_Pill.objects.filter(user=request.user).exists():
            pills = Notification_Pill.objects.get(user=request.user)
        context_key = {'key': key}
        data = is_subscribed(request.user)


    return {
        'total_admin_users': total_admin_users,
        # 'total_sub_users': total_sub_users,
        # 'total_active_sub_users': total_active_sub_users,
        # 'total_inactive_sub_users': total_inactive_sub_users,
        'role': role,
        'first_name': first_name,
        'permissions': permissions,
        'lists': lists,
        'userData': userData,
        'image': image,
        'dashboard_data': dashboard_data,
        'myuser': myuser,
        "context_key": context_key,
        "subscription": data,
        "customfields": customfields,
        "notifications4": notification[:4],
        "notifications_count": len(notification),
        "pills": pills
    }