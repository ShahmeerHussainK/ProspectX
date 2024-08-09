from django.contrib.auth.models import User
from django.db.models import Q

from prospectx_new.settings import account_sid_twilio, auth_token_twilio
from twilio.rest import Client
from datetime import datetime
from django.http import HttpResponse
from user.models import UserProfile
from xforce_sales.models import sales
from xforce_seller_leads.models import SellerLead, RoundRobinCounter
from xforce_transactions.models import Transaction


def format_time_obj(date_obj):  # display on frontend
    time_obj = datetime.strptime(date_obj, "%Y-%m-%dT%H:%M:%SZ")
    date_str = datetime.strftime(time_obj, "%m/%d/%y %H:%M")
    return date_str


def parse_str_to_time_obj(date_str):  # save in db
    date_obj = datetime.strptime(date_str, "%m/%d/%y %H:%M")
    return date_obj


def send_sms(to, body):
    msg = {}
    try:
        client = Client(set, auth_token_twilio)
        message = client.messages.create(
            from_='+12057515885',
            body=body,
            # to=to,
            to='+923002021848',
        )
        msg.update({"sms_status": True})
    except Exception as e:
        msg.update({"sms_status": False})


def get_comunity_people(usr):   # admin will not be included in list
    user_comunity_people = []
    sub_users_list = []
    usr_profile = UserProfile.objects.get(user_id=usr.id)

    if usr_profile.role.role_name == 'Admin User':
        sub_users_list = UserProfile.objects.filter(created_by=usr_profile)

    elif usr_profile.role.role_name == 'Sub User':
        get_admin = usr_profile.created_by  # sub user's admin
        sub_users_list = UserProfile.objects.filter(created_by=get_admin).exclude(user=usr_profile.user)

    for each_profile in sub_users_list:
        user_comunity_people.append(each_profile.user)
    return user_comunity_people


def get_comunity_people_with_role(usr, role):   # admin will not be included in list
    user_comunity_people = []
    sub_users_list = []
    usr_profile = UserProfile.objects.get(user_id=usr.id)
    if role:
        if role == "lead":
            query = Q(permissions__lead_manager=True)
        elif role == "transaction":
            query = Q(permissions__transaction_manager=True)
        elif role == "sale":
            query = Q(permissions__disposition_manager=True)

    if usr_profile.role.role_name == 'Admin User':
        sub_users_list = UserProfile.objects.filter(query, created_by=usr_profile)

    elif usr_profile.role.role_name == 'Sub User':
        get_admin = usr_profile.created_by  # sub user's admin
        sub_users_list = UserProfile.objects.filter(query, created_by=get_admin).exclude(user=usr_profile.user)

    for each_profile in sub_users_list:
        user_comunity_people.append(each_profile.user)
    return user_comunity_people


def get_comunity_people_queryset(usr):   # admin will not be included in list
    usr_profile = get_profile(usr)
    sub_users_list = UserProfile.objects.none()
    if usr_profile.role.role_name == 'Admin User':
        sub_users_list = UserProfile.objects.filter(created_by=usr_profile).order_by('user_id')

    elif usr_profile.role.role_name == 'Sub User':
        get_admin = usr_profile.created_by  # sub user's admin
        sub_users_list = UserProfile.objects.filter(created_by=get_admin).exclude(user=usr_profile.user).order_by('user_id')

    return sub_users_list


def round_robin_assignment(req, app, instance):
    sub_users = get_comunity_people_queryset(req.user)
    if app == "seller_lead":
        lead_role_sb = sub_users.filter(permissions__lead_manager=True)
        if lead_role_sb.count() > 0:
            rbr_object = assign_lead_id(req, app)
            sub_users_list = list(lead_role_sb)
            task_number__c = rbr_object.lead_task_cc-1
            round_robin_id__c = (task_number__c % lead_role_sb.count())+1
            instance.lead_manager = sub_users_list[round_robin_id__c-1].user   # list is starting from 0
            instance.save()
            return True
    elif app == "transaction":
        trans_role_sb = sub_users.filter(permissions__transaction_manager=True)
        if trans_role_sb.count() > 0:
            rbr_object = assign_lead_id(req, app)
            sub_users_list = list(trans_role_sb)
            task_number__c = rbr_object.transaction_task_cc - 1
            round_robin_id__c = (task_number__c % trans_role_sb.count()) + 1
            instance.transaction_manager = sub_users_list[round_robin_id__c - 1].user  # list is starting from 0
            instance.save()
            return True
    elif app == "sale":
        sale_role_sb = sub_users.filter(permissions__disposition_manager=True)
        if sale_role_sb.count() > 0:
            rbr_object = assign_lead_id(req, app)
            sub_users_list = list(sale_role_sb)
            task_number__c = rbr_object.sale_task_cc - 1
            round_robin_id__c = (task_number__c % sale_role_sb.count()) + 1
            instance.disposition_manager = sub_users_list[round_robin_id__c - 1].user  # list is starting from 0
            instance.save()
            return True
    return False


def assign_lead_id(req, app):
    admin_user = get_admin(req.user)

    if RoundRobinCounter.objects.filter(admin_user=admin_user).exists():
        rbr_obj = RoundRobinCounter.objects.filter(admin_user=admin_user).first()
    else:
        rbr_obj = RoundRobinCounter.objects.create(admin_user=admin_user)
    if app == "seller_lead":
        rbr_obj.lead_task_cc = rbr_obj.lead_task_cc + 1
        rbr_obj.save()
    elif app == "transaction":
        rbr_obj.transaction_task_cc = rbr_obj.transaction_task_cc + 1
        rbr_obj.save()
    elif app == "sale":
        rbr_obj.sale_task_cc = rbr_obj.sale_task_cc + 1
        rbr_obj.save()
    return rbr_obj


def get_admin(user):
    get_profile = UserProfile.objects.get(user=user)
    if get_profile.role.role_name == 'Admin User':
        return get_profile.user
    elif get_profile.role.role_name == 'Sub User':
        get_admin = get_profile.created_by
        return get_admin.user


def get_profile(user):
    return UserProfile.objects.get(user=user)


def permissions_check(per_obj):
    user = per_obj.Permission_Object.user
    try:
        if not per_obj.lead_manager:
            SellerLead.objects.filter(lead_manager=user).update(lead_manager=None)
        if not per_obj.transaction_manager:
            Transaction.objects.filter(transaction_manager=user).update(transaction_manager=None)
        if not per_obj.disposition_manager:
            sales.objects.filter(disposition_manager=user).update(disposition_manager=None)
    except Exception as e:
        print(e)


def comunity_people_with_role(usr, role):   # admin will not be included in list
    user_comunity_people = []
    sub_users_list = []
    usr_profile = UserProfile.objects.get(user_id=usr.id)
    if role:
        if role == "lead":
            query = Q(permissions__lead_manager=True)
        elif role == "transaction":
            query = Q(permissions__transaction_manager=True)
        elif role == "sale":
            query = Q(permissions__disposition_manager=True)

    if usr_profile.role.role_name == 'Admin User':
        sub_users_list = UserProfile.objects.filter(query, created_by=usr_profile)

    elif usr_profile.role.role_name == 'Sub User':
        get_admin = usr_profile.created_by  # sub user's admin
        sub_users_list = UserProfile.objects.filter(query, created_by=get_admin).exclude(user=usr_profile.user)

    for each_profile in sub_users_list:
        user_comunity_people.append(each_profile.user)
    return sub_users_list