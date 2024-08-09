from django.shortcuts import render
from django.shortcuts import redirect
import stripe
from django.db.models import F
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_eventstream import send_event
from user.decorators import user_has_marketing_plan_Permission
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import traceback
import time
from django.db import transaction
from datetime import datetime, date, timedelta
from django.template.loader import get_template
import requests
from user.models import *
from django.db.models import Q
from .models import *
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
import random
from filter_prospects.models import *
from notification.models import *
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.http import HttpResponseRedirect
from payments.views import is_subscribed
from django.core.mail import EmailMessage
from prospectx_new import settings as settings2
# from notification.views import send_twilio_message
import pytz
arr = {13:1, 14:2, 15:3, 16:4, 17:5, 18:6, 19:7, 20:8, 21:9, 22:10, 23:11, 24:12}
arr2 = {1:13, 2:14, 3:15, 4:16, 5:17, 6:18, 7:19, 8:20, 9:21, 10:22, 11:23, 0:12}


@user_has_marketing_plan_Permission
def marketing_sequence_list(request, pk):
    data_set = []
    if request.method == 'POST':
        name_search = request.POST.get("name_search")
        list_search = request.POST.getlist("list_search")
        temperature_search = request.POST.getlist("temperature_search")
        status_search = request.POST.getlist("status_search")
        approval_search = request.POST.getlist("approval_search")
        created_date = request.POST.get("datepicker1")
        if created_date:
            created_date = created_date.replace('/', '-')
            created_date = (datetime.datetime.strptime(created_date, "%Y-%m-%d")).date()
        try:
            sequences = MarketingSequence.objects.filter(user=request.user).select_related('list').order_by('-id')
            if name_search:
                sequences = [seq for seq in sequences if seq.name == name_search]
            if list_search:
                sequences = [seq for seq in sequences if str(seq.list.id) in list_search]
            if temperature_search:
                sequences = [seq for seq in sequences if seq.temperature in temperature_search]
            if status_search:
                sequences = [seq for seq in sequences if seq.status in status_search]
            if approval_search:
                sequences = [seq for seq in sequences if seq.approval in approval_search]
            if created_date:
                sequences = [seq for seq in sequences if seq.created_at.date() == created_date]

            sequence_data_list = []
            for sequence in sequences:
                created_at = sequence.created_at + timedelta(hours=-int(sequence.timezone_gap_in_hours))
                query_data = {
                    "id": sequence.id,
                    "name": sequence.name,
                    "list": sequence.list.list_name,
                    "temperature": sequence.temperature,
                    "status": sequence.status,
                    "date": created_at.strftime('%m/%d/%Y %H:%M:%S.%f').split('.')[0]
                }
                sequence_data_list.append(query_data)

            return render(request, 'marketing_machine/marketing_sequence_list.html', {"data_set": sequence_data_list,
                                                                                      "count": len(data_set)})
        except:
            print(traceback.format_exc())
            return redirect('/marketing/sequence_list/home/')
    else:
        # for active sequences
        all_active_sequence_ids = []
        sequences = MarketingSequence.objects.filter(user=request.user, status='Active').order_by('-id')
        if sequences:
            all_active_sequence_ids = [q.id for q in sequences]

        # for inactive sequences
        all_inactive_sequences_ids = []
        inactive_sequences = MarketingSequence.objects.filter(user=request.user, status='InActive').order_by('-id')
        if inactive_sequences:
            all_inactive_sequences_ids = [q.id for q in inactive_sequences]

        # for pending sequences
        all_pending_sequences_ids = []
        pending_sequences = MarketingSequence.objects.filter(user=request.user, status='Pending').order_by('-id')
        if pending_sequences:
            all_pending_sequences_ids = [q.id for q in pending_sequences]

        # All active
        all_active = sequences
        # call active
        call_active_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_active_sequence_ids) & Q(plan='Cold Call'))
        call_active_seq_ids = [s.sequence.id for s in call_active_plan]
        call_active_sequence = MarketingSequence.objects.filter(user=request.user, id__in=call_active_seq_ids)
        # mail active
        mail_active_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_active_sequence_ids) & Q(plan='Direct Mail'))
        mail_active_seq_ids = [s.sequence.id for s in mail_active_plan]
        mail_active_sequence = MarketingSequence.objects.filter(user=request.user, id__in=mail_active_seq_ids)
        # voice active
        voice_active_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_active_sequence_ids) & Q(plan='Voice Broadcast'))
        voice_active_seq_ids = [s.sequence.id for s in voice_active_plan]
        voice_active_sequence = MarketingSequence.objects.filter(user=request.user, id__in=voice_active_seq_ids)
        # rvm_active
        rvm_active_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_active_sequence_ids) & Q(plan='RVM'))
        rvm_active_plan_seq_ids = [s.sequence.id for s in rvm_active_plan]
        rvm_active_sequence = MarketingSequence.objects.filter(user=request.user, id__in=rvm_active_plan_seq_ids)
        # sms_active
        sms_active_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_active_sequence_ids) & Q(plan='SMS'))
        sms_active_plan_seq_ids = [s.sequence.id for s in sms_active_plan]
        sms_active_sequence = MarketingSequence.objects.filter(user=request.user, id__in=sms_active_plan_seq_ids)
        # email_active
        email_active_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_active_sequence_ids) & Q(plan='EMAIL'))
        email_active_plan_seq_ids = [s.sequence.id for s in email_active_plan]
        email_active_sequence = MarketingSequence.objects.filter(user=request.user, id__in=email_active_plan_seq_ids)

        # all_inactive
        all_inactive = inactive_sequences
        # call_inactive
        call_inactive_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_inactive_sequences_ids) & Q(plan='Cold Call'))
        call_inactive_seq_ids = [s.sequence.id for s in call_inactive_plan]
        call_inactive_sequence = MarketingSequence.objects.filter(user=request.user, id__in=call_inactive_seq_ids)
        # mail_inactive
        mail_inactive_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_inactive_sequences_ids) & Q(plan='Direct Mail'))
        mail_inactive_seq_ids = [s.sequence.id for s in mail_inactive_plan]
        mail_inactive_sequence = MarketingSequence.objects.filter(user=request.user, id__in=mail_inactive_seq_ids)
        # voice_inactive
        voice_inactive_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_inactive_sequences_ids) & Q(plan='Voice Broadcast'))
        voice_inactive_plan_seq_ids = [s.sequence.id for s in voice_inactive_plan]
        voice_inactive_sequence = MarketingSequence.objects.filter(user=request.user, id__in=voice_inactive_plan_seq_ids)
        # rvm_inactive
        rvm_inactive_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_inactive_sequences_ids) & Q(plan='RVM'))
        rvm_inactive_plan_seq_ids = [s.sequence.id for s in rvm_inactive_plan]
        rvm_inactive_sequence = MarketingSequence.objects.filter(user=request.user, id__in=rvm_inactive_plan_seq_ids)
        # sms_inactive
        sms_inactive_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_inactive_sequences_ids) & Q(plan='SMS'))
        sms_inactive_plan_seq_ids = [s.sequence.id for s in sms_inactive_plan]
        sms_inactive_sequence = MarketingSequence.objects.filter(user=request.user, id__in=sms_inactive_plan_seq_ids)
        # email_inactive
        email_inactive_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_inactive_sequences_ids) & Q(plan='EMAIL'))
        email_inactive_plan_seq_ids = [s.sequence.id for s in email_inactive_plan]
        email_inactive_sequence = MarketingSequence.objects.filter(user=request.user, id__in=email_inactive_plan_seq_ids)

        # all_pending
        all_pending = pending_sequences
        # call_pending
        call_pending_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_pending_sequences_ids) & Q(plan='Cold Call'))
        call_pending_plan_seq_ids = [s.sequence.id for s in call_pending_plan]
        call_pending_sequence = MarketingSequence.objects.filter(user=request.user, id__in=call_pending_plan_seq_ids)
        # mail_pending
        mail_pending_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_pending_sequences_ids) & Q(plan='Direct Mail'))
        mail_pending_plan_seq_ids = [s.sequence.id for s in mail_pending_plan]
        mail_pending_sequence = MarketingSequence.objects.filter(user=request.user, id__in=mail_pending_plan_seq_ids)
        # voice_pending
        voice_pending_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_pending_sequences_ids) & Q(plan='Voice Broadcast'))
        voice_pending_plan_seq_ids = [s.sequence.id for s in voice_pending_plan]
        voice_pending_sequence = MarketingSequence.objects.filter(user=request.user, id__in=voice_pending_plan_seq_ids)
        # rvm_pending
        rvm_pending_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_pending_sequences_ids) & Q(plan='RVM'))
        rvm_pending_plan_seq_ids = [s.sequence.id for s in rvm_pending_plan]
        rvm_pending_sequence = MarketingSequence.objects.filter(user=request.user, id__in=rvm_pending_plan_seq_ids)
        # sms_pending
        sms_pending_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_pending_sequences_ids) & Q(plan='SMS'))
        sms_pending_plan_seq_ids = [s.sequence.id for s in sms_pending_plan]
        sms_pending_sequence = MarketingSequence.objects.filter(user=request.user, id__in=sms_pending_plan_seq_ids)
        # email_pending
        email_pending_plan = MarketingPlan.objects.filter(Q(sequence_id__in=all_pending_sequences_ids) & Q(plan='EMAIL'))
        email_pending_plan_seq_ids = [s.sequence.id for s in email_pending_plan]
        email_pending_sequence = MarketingSequence.objects.filter(user=request.user, id__in=email_pending_plan_seq_ids)

        # all plans
        all_plans = MarketingSequence.objects.filter(user=request.user)
        # untouched_plan
        untouched_plan = MarketingSequence.objects.filter(user=request.user, planning_status='Untouched')
        # filtered_plan
        filtered_plan = MarketingSequence.objects.filter(user=request.user, planning_status='Filtered')
        # skipped_plan
        skipped_plan = MarketingSequence.objects.filter(user=request.user, planning_status='Skipped')
        # planned_plan
        planned_plan = MarketingSequence.objects.filter(user=request.user, planning_status='Planned')
        # planning_done_plan
        planning_done_plan = MarketingSequence.objects.filter(user=request.user, planning_done='Yes')
        # planning_not_done_plan
        planning_not_done_plan = MarketingSequence.objects.filter(user=request.user, planning_done='No')
        # marketing_created_plan
        marketing_created_plan = MarketingSequence.objects.filter(user=request.user, create_marketing='Yes')
        # marketing_not_created_plan
        marketing_not_created_plan = MarketingSequence.objects.filter(user=request.user, create_marketing='No')

        queries_counts = {
            "all_active": len(all_active),
            "call_active_plan": len(call_active_plan),
            "mail_active_plan": len(mail_active_plan),
            "voice_active_plan": len(voice_active_plan),
            "rvm_active_plan": len(rvm_active_plan),
            "sms_active_plan": len(sms_active_plan),
            "email_active_plan": len(email_active_plan),
            "all_inactive": len(all_inactive),
            "call_inactive_plan": len(call_inactive_plan),
            "mail_inactive_plan": len(mail_inactive_plan),
            "voice_inactive_plan": len(voice_inactive_plan),
            "rvm_inactive_plan": len(rvm_inactive_plan),
            "sms_inactive_plan": len(sms_inactive_plan),
            "email_inactive_plan": len(email_inactive_plan),
            "all_pending": len(all_pending),
            "call_pending_plan": len(call_pending_plan),
            "mail_pending_plan": len(mail_pending_plan),
            "voice_pending_plan": len(voice_pending_plan),
            "rvm_pending_plan": len(rvm_pending_plan),
            "sms_pending_plan": len(sms_pending_plan),
            "email_pending_plan": len(email_pending_plan),
            "all_plans": len(all_plans),
            "untouched_plan": len(untouched_plan),
            "filtered_plan": len(filtered_plan),
            "skipped_plan": len(skipped_plan),
            "planned_plan": len(planned_plan),
            "planning_done_plan": len(planning_done_plan),
            "planning_not_done_plan": len(planning_not_done_plan),
            "marketing_created_plan": len(marketing_created_plan),
            "marketing_not_created_plan": len(marketing_not_created_plan),
        }

        if pk == 'home':
            queryset = MarketingSequence.objects.filter(user=request.user).order_by('-id')

        elif pk == 'all_active':
            queryset = all_active

        elif pk == 'call_active':
            queryset = call_active_sequence

        elif pk == 'mail_active':
            queryset = mail_active_sequence

        elif pk == 'voice_active':
            queryset = voice_active_sequence

        elif pk == 'rvm_active':
            queryset = rvm_active_sequence

        elif pk == 'sms_active':
            queryset = sms_active_sequence

        elif pk == 'email_active':
            queryset = email_active_sequence

# for inactive sidebar menu
        elif pk == 'all_inactive':
            queryset = all_inactive

        elif pk == 'call_inactive':
            queryset = call_inactive_sequence

        elif pk == 'mail_inactive':
            queryset = mail_inactive_sequence

        elif pk == 'voice_inactive':
            queryset = voice_inactive_sequence

        elif pk == 'rvm_inactive':
            queryset = rvm_inactive_sequence

        elif pk == 'sms_inactive':
            queryset = sms_inactive_sequence

        elif pk == 'email_inactive':
            queryset = email_inactive_sequence

# for pending sidebar menu
        elif pk == 'all_pending':
            queryset = all_pending

        elif pk == 'call_pending':
            queryset = call_pending_sequence

        elif pk == 'mail_pending':
            queryset = mail_pending_sequence

        elif pk == 'voice_pending':
            queryset = voice_pending_sequence

        elif pk == 'rvm_pending':
            queryset = rvm_pending_sequence

        elif pk == 'sms_pending':
            queryset = sms_pending_sequence

        elif pk == 'email_pending':
            queryset = email_pending_sequence

# for Planner view sidebar menu
        elif pk == 'all_plans':
            queryset = all_plans

        elif pk == 'untouched_plan':
            queryset = untouched_plan

        elif pk == 'filtered_plan':
            queryset = filtered_plan

        elif pk == 'skipped_plan':
            queryset = skipped_plan

        elif pk == 'planned_plan':
            queryset = planned_plan

        elif pk == 'planning_done_plan':
            queryset = planning_done_plan

        elif pk == 'planning_not_done_plan':
            queryset = planning_not_done_plan

        elif pk == 'marketing_created_plan':
            queryset = marketing_created_plan

        elif pk == 'marketing_not_created_plan':
            queryset = marketing_not_created_plan

        list_data = []
        lists = List.objects.filter(user=request.user)
        for lis in lists:
            lis_d = {
                "lis_id": lis.id,
                "lis_name": lis.list_name
            }
            list_data.append(lis_d)
        if queryset:
            for query in queryset.order_by('id').reverse():
                created_at = query.created_at + timedelta(hours=-int(query.timezone_gap_in_hours))
                query_data = {
                    "id": query.id,
                    "name": query.name,
                    "list": query.list.list_name,
                    "temperature": query.temperature,
                    "status": query.status,
                    "date": created_at.strftime('%m/%d/%Y %H:%M:%S.%f').split('.')[0]
                }
                data_set.append(query_data)

            return render(request, 'marketing_machine/marketing_sequence_list.html', {"queries_counts": queries_counts,
                                                                                      "list_data": list_data,
                                                                                      "data_set": data_set,
                                                                                      "count": len(data_set)})
        else:
            return render(request, 'marketing_machine/marketing_sequence_list.html', {"queries_counts": queries_counts,
                                                                                      "list_data": list_data,
                                                                                      "data_set": data_set,
                                                                                      "count": len(data_set)})


@user_has_marketing_plan_Permission
def marketing_campaign_list(request, pk):
    if request.method == 'POST':
        search_plan = request.POST.getlist("search_plan")
        temperature_search = request.POST.getlist("temperature_search")
        dist_search = request.POST.getlist("dist_search")
        approval_search = request.POST.getlist("approval_search")
        planning_done_search = request.POST.getlist("planning_done_search")
        scheduled_date = request.POST.get("datepicker1")
        if scheduled_date:
            scheduled_date = scheduled_date.replace('/', '-')
            scheduled_date = (datetime.datetime.strptime(scheduled_date, "%Y-%m-%d")).date()
        try:
            user_sequences = MarketingSequence.objects.filter(user=request.user)
            all_campaigns = MarketingCampaign.objects.all()
            campaigns = all_campaigns.select_related('plan').select_related('camp_sequence').filter(
                Q(camp_sequence__in=user_sequences) | Q(user=request.user.email)).order_by('-id')

            if planning_done_search:
                campaigns = [camp for camp in campaigns if camp.camp_sequence.planning_done in planning_done_search]
            if search_plan:
                campaigns = [camp for camp in campaigns if camp.plan.plan in search_plan]
            if temperature_search:
                campaigns = [camp for camp in campaigns if camp.temperature in temperature_search]
            if dist_search:
                campaigns = [camp for camp in campaigns if camp.distribution_status in dist_search]
            if approval_search:
                campaigns = [camp for camp in campaigns if camp.approval in approval_search]
            if scheduled_date:
                campaigns = [camp for camp in campaigns if camp.scheduled_plan_for.date() == scheduled_date]

            campaign_data_list = []
            for campaign in campaigns:
                schedule = campaign.scheduled_plan_for + timedelta(hours=-int(campaign.timezone_gap_in_hours))
                if schedule.hour < 12:
                    schedule = schedule.replace(hour=arr2[schedule.hour])
                created_at = campaign.created_at + timedelta(hours=-int(campaign.timezone_gap_in_hours))

                campaign_data = {
                    "id": campaign.id,
                    "plan": campaign.plan.plan,
                    "title": campaign.title,
                    # "planer": campaign.camp_sequence,
                    "created_at": created_at,
                    "hash_off": campaign.hash_off,
                    "temperature": campaign.temperature,
                    # "major_market": campaign.maj_market,
                    # "responsible": campaign.responsible,
                    # "send_via": campaign.plan.plan,
                    "dist_status": campaign.distribution_status,
                    "approval": campaign.approval,
                    # "units": campaign.total_units,
                    # "touch": campaign.template.touch_round_number if campaign.template else "",
                    "scheduled_plan_for": schedule,
                    # "notes": campaign.notes,
                    # "template": campaign.template.id if campaign.template else "",
                    # "mark_details": campaign.marketing_details,
                    # "image": campaign.campaign_file
                }
                campaign_data_list.append(campaign_data)

            return render(request, 'marketing_machine/campaign_list.html', {"campaign_data": campaign_data_list,
                                                                            # "counts": counts,
                                                                            })
        except:
            print(traceback.format_exc())
            return redirect('/marketing/campaign_list/home/')
    user_sequences = MarketingSequence.objects.filter(user=request.user)
    all_campaigns = MarketingCampaign.objects.select_related('plan').filter(Q(camp_sequence__in=user_sequences) | Q(user=request.user.email)).order_by('-id')

    try:
        today = [camp for camp in all_campaigns if camp.scheduled_plan_for.date() == datetime.date.today() or camp.user == request.user]
        tomorrow = [camp for camp in all_campaigns if camp.scheduled_plan_for.date() == datetime.date.today() + timedelta(days=1) or camp.user == request.user]
        future = [camp for camp in all_campaigns if camp.scheduled_plan_for.date() > datetime.date.today() or camp.user == request.user]
        past = [camp for camp in all_campaigns if camp.scheduled_plan_for.date() < datetime.date.today() or camp.user == request.user]
        if pk == 'home':
            campaigns = all_campaigns

        elif pk == 'today':
            campaigns = today

        elif pk == 'tomorrow':
            campaigns = tomorrow

        elif pk == 'future':
            campaigns = future

        elif pk == 'past':
            campaigns = past
        else:
            campaigns = all_campaigns
        campaign_data_list = []
        for campaign in campaigns:
            schedule = campaign.scheduled_plan_for + timedelta(hours=-int(campaign.timezone_gap_in_hours))
            if campaign.time_format == 'PM':
                schedule = schedule.replace(hour=arr2[schedule.hour])
            created_at = campaign.created_at + timedelta(hours=-int(campaign.timezone_gap_in_hours))
            campaign_data = {
                "id": campaign.id,
                "plan": campaign.plan.plan,
                "title": campaign.title,
                # "planer": campaign.camp_sequence,
                "created_at": created_at.strftime('%m/%d/%Y %H:%M:%S.%f').split('.')[0],
                "hash_off": campaign.hash_off,
                "temperature": campaign.temperature,
                # "major_market": campaign.maj_market,
                # "responsible": campaign.responsible,
                # "send_via": campaign.plan.plan,
                "dist_status": campaign.distribution_status,
                "approval": campaign.approval,
                # "units": campaign.total_units,
                # "touch": campaign.template.touch_round_number if campaign.template else "",
                "scheduled_plan_for": schedule.strftime('%m/%d/%Y %H:%M:%S.%f').split('.')[0],
                # "notes": campaign.notes,
                # "template": campaign.template.id if campaign.template else "",
                # "mark_details": campaign.marketing_details,
                # "image": campaign.campaign_file
            }
            campaign_data_list.append(campaign_data)
        counts = {
            "all": len(all_campaigns),
            "today": len(today),
            "tomorrow": len(tomorrow),
            "future": len(future),
            "past": len(past),
        }
        return render(request, 'marketing_machine/campaign_list.html', {"campaign_data": campaign_data_list,
                                                                        "counts": counts,
                                                                        })
    except:
        print(traceback.format_exc())
        return redirect('/marketing/campaign_list/home/')


@user_has_marketing_plan_Permission
def create_marketing_sequence(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        time_dif = request.POST.get("time_dif")
        lists = request.POST.get("lists")
        temperature = request.POST.get("customRadio")
        seq_status = request.POST.get("customRadio8")
        details = request.POST.get("text_area")
        try:
            if title and lists and temperature and seq_status:
                rec_list = List.objects.get(id=lists)
                MarketingSequence.objects.create(user=request.user, name=title, list=rec_list,
                                                 status=seq_status, temperature=temperature,
                                                 timezone_gap_in_hours=time_dif, details=details,
                                                 created_at=datetime.datetime.now())

                data_set = []
                queryset = MarketingSequence.objects.filter(user=request.user)
                for query in queryset:
                    query_data = {
                        "id": query.id,
                        "name": query.name,
                        "list": query.list.list_name,
                        "temperature": query.temperature,
                        "status": query.status,
                        "date": query.created_at
                    }
                    data_set.append(query_data)
                return redirect('/marketing/sequence_list/home')
            else:
                return redirect('/marketing/sequence_list/home')
        except:
            print(traceback.print_exc())
            return redirect('/marketing/sequence_list/home')

    list_data = []
    lists = List.objects.filter(user=request.user)
    for lis in lists:
        lis_d = {
            "lis_id": lis.id,
            "lis_name": lis.list_name
        }
        list_data.append(lis_d)
    return render(request, 'marketing_machine/create_sequence.html', {"list_data": list_data})


@user_has_marketing_plan_Permission
def update_marketing_sequence(request, pk):
    if request.method == 'POST':
        try:
            seq_name = request.POST.get("seq_name")
            status_radio = request.POST.get("status_radio")
            time_dif = request.POST.get("time_dif")
            temperature_radio = request.POST.get("temperature_radio")

            m_market = request.POST.get("markets")
            major_market = MajorMarket.objects.filter(title=m_market)

            seq_details = request.POST.get("seq_details")

            planning_status = request.POST.get("planning_status")

            create_marketing = request.POST.get("create_marketing_radio")

            planning_done = request.POST.get("planning_done_radio")

            Cold_Call_date = request.POST.get("Cold_Call_date")

            Direct_Mail_date = request.POST.get("Direct_Mail_date")

            Voice_Broadcast_date = request.POST.get("Voice_Broadcast_date")

            RVM_date = request.POST.get("RVM_date")

            SMS_date = request.POST.get("SMS_date")

            Email_date = request.POST.get("Email_date")

            plan_details = request.POST.get("plan_details")
            responsible_user_id = request.POST.get("responsible_user")
            print("responsible_user: ", responsible_user_id)
            if responsible_user_id:
                res_user = User.objects.filter(id=responsible_user_id)
                try:
                    send_event('prospectx' + str(responsible_user_id), 'message', 'A New Marketing Campaign has been updated for you!')
                    Notification.objects.create(user_id=responsible_user_id, title="A New Marketing Campaign has been updated for you!")
                    Notification_Pill.objects.filter(user_id=responsible_user_id).update(notification_pill=F('notification_pill') + 1)
                    if Notification_Pill.objects.filter(user_id=responsible_user_id, email_notification=True):
                        email_from = settings.EMAIL_HOST_USER
                        email_to = res_user[0].email
                        message_body = "A New Marketing Sequence "+seq_name+" has been updated for you!"
                        send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                        send_email.content_subtype = 'html'
                        send_email.send()
                except:
                    print(traceback.format_exc())
            else:
                res_user = None
            print("res_user is: ", res_user)
            call_break = int(request.POST.get("call_break"))
            call_break_td = ''
            for i in range(1, call_break + 1):
                call_break_td += request.POST.get("call_break" + str(i))
            if call_break_td == '':
                call_break_td = '0'

            dir_mail_break = int(request.POST.get("dir_mail_break"))
            dir_mail_break_td = ''
            for i in range(1, dir_mail_break + 1):
                dir_mail_break_td += request.POST.get("dir_mail_break" + str(i))
            if dir_mail_break_td == '':
                dir_mail_break_td = '0'
            print("dir_mail_break_td: ", dir_mail_break_td[0])
            voice_break = int(request.POST.get("voice_break"))
            voice_break_td = ''
            for i in range(1, voice_break + 1):
                voice_break_td += request.POST.get("voice_break" + str(i))
            if voice_break_td == '':
                voice_break_td = '0'

            rvm_break = int(request.POST.get("rvm_break"))
            rvm_break_td = ''
            for i in range(1, rvm_break + 1):
                rvm_break_td += request.POST.get("rvm_break" + str(i))
            if rvm_break_td == '':
                rvm_break_td = '0'

            sms_break = int(request.POST.get("sms_break"))
            sms_break_td = ''
            for i in range(1, sms_break + 1):
                sms_break_td += request.POST.get("sms_break" + str(i))
            if sms_break_td == '':
                sms_break_td = '0'

            email_break = int(request.POST.get("email_break"))
            email_break_td = ''
            for i in range(1, email_break + 1):
                email_break_td += request.POST.get("email_break" + str(i))
            if email_break_td == '':
                email_break_td = '0'

            send_on_call = request.POST.get("send_on_call")

            send_on_dir_mail = request.POST.get("send_on_dir_mail")

            send_on_voice = request.POST.get("send_on_voice")

            send_on_rvm = request.POST.get("send_on_rvm")

            send_on_sms = request.POST.get("send_on_sms")

            send_on_email = request.POST.get("send_on_email")

            # if request.FILES:
            #     image = request.FILES.get('campaign_file')

            # Updating Sequence Fields
            MarketingSequence.objects.filter(id=pk).update(name=seq_name,
                                                           status=status_radio,
                                                           temperature=temperature_radio, details=seq_details,
                                                           planning_status=planning_status,
                                                           create_marketing=create_marketing,
                                                           planning_done=planning_done,
                                                           )
            marketing_sequence = MarketingSequence.objects.get(id=pk)

            # Updating Marketing and Templates of Sequence
            # for cold call
            if MarketingPlan.objects.filter(Q(sequence=marketing_sequence) & Q(plan='Cold Call')).exists():
                print("cold call exists")
                update_call_plan = MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='Cold Call'))
                temps1 = PlanRoundTemplate.objects.filter(plan=update_call_plan[0]).order_by('id')

                for c in range(len(temps1)):
                    c_round = request.POST.get("Cold_Call" + str(c+1))
                    if c_round and int(c_round) > 0:
                        temps1[c].touch_round_after_days = c_round
                        temps1[c].save()
                if create_marketing == 'Yes':
                    Cold_Call_date = Cold_Call_date.replace('/', '-')
                    try:
                        Cold_Call_date = datetime.datetime.strptime(Cold_Call_date, "%Y-%m-%d %H:%M:%S.%f")
                        # Cold_Call_date = Cold_Call_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    except:
                        Cold_Call_date = datetime.datetime.strptime(Cold_Call_date, "%Y-%m-%d %H:%M")
                    Cold_Call_date += timedelta(hours=int(time_dif))
                    if Cold_Call_date.hour > 12:
                        Cold_Call_date = Cold_Call_date.replace(hour=arr[Cold_Call_date.hour])
                    else:
                        pass
                    if MarketingCampaign.objects.filter(Q(camp_sequence=marketing_sequence) &
                                                        Q(plan=update_call_plan[0])).exists():
                        call_plan_updating = MarketingCampaign.objects.filter(Q(camp_sequence=marketing_sequence) &
                                                                              Q(plan=update_call_plan[0]))
                        call_plan_updating.delete()
                    with transaction.atomic():
                        for c in range(len(temps1)):
                            MarketingCampaign.objects.create(camp_sequence=marketing_sequence,
                                                             plan=update_call_plan[0],
                                                             template=temps1[c],
                                                             title=update_call_plan[
                                                                       0].sequence.name + " " +
                                                                   update_call_plan[
                                                                       0].plan + str(c + 1),
                                                             hash_off=str(c + 1) + ' of ' + str(len(temps1)),
                                                             temperature=temperature_radio,
                                                             scheduled_plan_for=Cold_Call_date,
                                                             timezone_gap_in_hours=time_dif,
                                                             # days_gap_in_campaign=call_break_td[c],
                                                             marketing_details=plan_details,
                                                             break_into=call_break,
                                                             maj_market=major_market[0],
                                                             responsible=res_user[0],
                                                             send_on=send_on_call,
                                                             user=request.user.email)
                        MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='Cold Call')).update(break_into=call_break,
                                                                                                      days_gap_in_campaign=call_break_td,
                                                                                                      send_on=send_on_call,
                                                                                                      scheduled_plan_for=Cold_Call_date)

            # for direct mail
            if MarketingPlan.objects.filter(Q(sequence=marketing_sequence) & Q(plan='Direct Mail')).exists():
                update_dir_mail_plan = MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='Direct Mail'))
                temps2 = PlanRoundTemplate.objects.filter(plan=update_dir_mail_plan[0]).order_by('id')

                for d in range(len(temps2)):
                    with transaction.atomic():
                        d_round = request.POST.get("Direct_Mail" + str(d + 1))
                        if d_round and int(d_round) > 0:
                            temps2[d].touch_round_after_days = d_round
                            temps2[d].save()
                if create_marketing == 'Yes':
                    Direct_Mail_date = Direct_Mail_date.replace('/', '-')
                    try:
                        Direct_Mail_date = datetime.datetime.strptime(Direct_Mail_date, "%Y-%m-%d %H:%M:%S.%f")
                        # Direct_Mail_date = Direct_Mail_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    except:
                        Direct_Mail_date = datetime.datetime.strptime(Direct_Mail_date, "%Y-%m-%d %H:%M")
                    Direct_Mail_date += timedelta(hours=int(time_dif))
                    if Direct_Mail_date.hour > 12:
                        Direct_Mail_date = Direct_Mail_date.replace(hour=arr[Direct_Mail_date.hour])
                    else:
                        pass
                    if MarketingCampaign.objects.filter(Q(camp_sequence=marketing_sequence) &
                                                        Q(plan=update_dir_mail_plan[0])).exists():
                        dir_call_plan_updating = MarketingCampaign.objects.filter(
                            Q(camp_sequence=marketing_sequence) &
                            Q(plan=update_dir_mail_plan[0]))
                        dir_call_plan_updating.delete()
                    with transaction.atomic():
                        for d in range(len(temps2)):
                            MarketingCampaign.objects.create(camp_sequence=marketing_sequence,
                                                             plan=update_dir_mail_plan[0],
                                                             template=temps2[d],
                                                             title=update_dir_mail_plan[
                                                                       0].sequence.name + " " +
                                                                   update_dir_mail_plan[
                                                                       0].plan + str(d + 1),
                                                             hash_off=str(d + 1) + ' of ' + str(len(temps2)),
                                                             temperature=temperature_radio,
                                                             scheduled_plan_for=Direct_Mail_date,
                                                             timezone_gap_in_hours=time_dif,
                                                             # days_gap_in_campaign=dir_mail_break_td[d],
                                                             marketing_details=plan_details,
                                                             break_into=dir_mail_break,
                                                             maj_market=major_market[0],
                                                             responsible=res_user[0],
                                                             send_on=send_on_dir_mail,
                                                             user=request.user.email)
                        MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='Direct Mail')).update(break_into=dir_mail_break,
                                                                                                        days_gap_in_campaign=dir_mail_break_td,
                                                                                                        send_on=send_on_dir_mail,
                                                                                                        scheduled_plan_for=Direct_Mail_date)

            # for Voice Broadcast
            if MarketingPlan.objects.filter(Q(sequence=marketing_sequence) & Q(plan='Voice Broadcast')).exists():
                update_voice_plan = MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='Voice Broadcast'))
                temps3 = PlanRoundTemplate.objects.filter(plan=update_voice_plan[0]).order_by('id')

                for v in range(len(temps3)):
                    with transaction.atomic():
                        v_round = request.POST.get("Voice_Broadcast" + str(v + 1))
                        if v_round and int(v_round) > 0:
                            temps3[v].touch_round_after_days = v_round
                            temps3[v].save()

                if create_marketing == 'Yes':
                    Voice_Broadcast_date = Voice_Broadcast_date.replace('/', '-')
                    try:
                        Voice_Broadcast_date = datetime.datetime.strptime(Voice_Broadcast_date, "%Y-%m-%d %H:%M:%S.%f")
                        # Voice_Broadcast_date = Voice_Broadcast_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    except:
                        Voice_Broadcast_date = datetime.datetime.strptime(Voice_Broadcast_date, "%Y-%m-%d %H:%M")
                    Voice_Broadcast_date += timedelta(hours=int(time_dif))
                    if Voice_Broadcast_date.hour > 12:
                        Voice_Broadcast_date = Voice_Broadcast_date.replace(hour=arr[Voice_Broadcast_date.hour])
                    else:
                        pass
                    if MarketingCampaign.objects.filter(Q(camp_sequence=marketing_sequence) &
                                                        Q(plan=update_voice_plan[0])).exists():
                        call_plan_updating = MarketingCampaign.objects.filter(
                            Q(camp_sequence=marketing_sequence) &
                            Q(plan=update_voice_plan[0]))
                        call_plan_updating.delete()
                    with transaction.atomic():
                        for v in range(len(temps3)):
                            MarketingCampaign.objects.create(camp_sequence=marketing_sequence,
                                                             plan=update_voice_plan[0],
                                                             template=temps3[v],
                                                             title=update_voice_plan[
                                                                       0].sequence.name + " " +
                                                                   update_voice_plan[
                                                                       0].plan + str(v + 1),
                                                             hash_off=str(v + 1) + ' of ' + str(len(temps3)),
                                                             temperature=temperature_radio,
                                                             scheduled_plan_for=Voice_Broadcast_date,
                                                             timezone_gap_in_hours=time_dif,
                                                             # days_gap_in_campaign=voice_break_td[v],
                                                             marketing_details=plan_details,
                                                             break_into=voice_break,
                                                             maj_market=major_market[0],
                                                             responsible=res_user[0],
                                                             send_on=send_on_voice,
                                                             user=request.user.email)
                        MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='Voice Broadcast')).update(break_into=voice_break,
                                                                                                            days_gap_in_campaign=voice_break_td,
                                                                                                            send_on=send_on_voice,
                                                                                                            scheduled_plan_for=Voice_Broadcast_date)

            # for RVM
            if MarketingPlan.objects.filter(Q(sequence=marketing_sequence) & Q(plan='RVM')).exists():
                update_rvm_plan = MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='RVM'))
                temps4 = PlanRoundTemplate.objects.filter(plan=update_rvm_plan[0]).order_by('id')

                for r in range(len(temps4)):
                    with transaction.atomic():
                        r_round = request.POST.get("RVM" + str(r + 1))
                        if r_round and int(r_round) > 0:
                            temps4[r].touch_round_after_days = r_round
                            temps4[r].save()

                if create_marketing == 'Yes':
                    RVM_date = RVM_date.replace('/', '-')
                    try:
                        RVM_date = datetime.datetime.strptime(RVM_date, "%Y-%m-%d %H:%M:%S.%f")
                        # RVM_date = RVM_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    except:
                        RVM_date = datetime.datetime.strptime(RVM_date, "%Y-%m-%d %H:%M")
                    RVM_date += timedelta(hours=int(time_dif))
                    if RVM_date.hour > 12:
                        RVM_date = RVM_date.replace(hour=arr[RVM_date.hour])
                    else:
                        pass
                    if MarketingCampaign.objects.filter(Q(camp_sequence=marketing_sequence) &
                                                        Q(plan=update_rvm_plan[0])).exists():
                        call_plan_updating = MarketingCampaign.objects.filter(
                            Q(camp_sequence=marketing_sequence) &
                            Q(plan=update_rvm_plan[0]))
                        call_plan_updating.delete()
                    with transaction.atomic():
                        for r in range(len(temps4)):
                            MarketingCampaign.objects.create(camp_sequence=marketing_sequence,
                                                             plan=update_rvm_plan[0],
                                                             template=temps4[r],
                                                             title=update_rvm_plan[
                                                                       0].sequence.name + " " +
                                                                   update_rvm_plan[
                                                                       0].plan + str(r + 1),
                                                             hash_off=str(r + 1) + ' of ' + str(len(temps4)),
                                                             temperature=temperature_radio,
                                                             scheduled_plan_for=RVM_date,
                                                             timezone_gap_in_hours=time_dif,
                                                             # days_gap_in_campaign=rvm_break_td[r],
                                                             marketing_details=plan_details,
                                                             break_into=rvm_break,
                                                             maj_market=major_market[0],
                                                             responsible=res_user[0],
                                                             send_on=send_on_rvm,
                                                             user=request.user.email)
                        MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='RVM')).update(break_into=rvm_break,
                                                                                                days_gap_in_campaign=rvm_break_td,
                                                                                                send_on=send_on_rvm,
                                                                                                scheduled_plan_for=RVM_date)

            # for SMS
            if MarketingPlan.objects.filter(Q(sequence=marketing_sequence) & Q(plan='SMS')).exists():
                update_sms_plan = MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='SMS'))
                temps5 = PlanRoundTemplate.objects.filter(plan=update_sms_plan[0]).order_by('id')

                for s in range(len(temps5)):
                    with transaction.atomic():
                        s_round = request.POST.get("SMS" + str(s + 1))
                        if s_round and int(s_round) > 0:
                            temps5[s].touch_round_after_days = s_round
                            temps5[s].save()

                if create_marketing == 'Yes':
                    SMS_date = SMS_date.replace('/', '-')
                    try:
                        SMS_date = datetime.datetime.strptime(SMS_date, "%Y-%m-%d %H:%M:%S.%f")
                        # SMS_date = SMS_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    except:
                        SMS_date = datetime.datetime.strptime(SMS_date, "%Y-%m-%d %H:%M")
                    SMS_date += timedelta(hours=int(time_dif))
                    if SMS_date.hour > 12:
                        SMS_date = SMS_date.replace(hour=arr[SMS_date.hour])
                    else:
                        pass
                    if MarketingCampaign.objects.filter(Q(camp_sequence=marketing_sequence) &
                                                        Q(plan=update_sms_plan[0])).exists():
                        call_plan_updating = MarketingCampaign.objects.filter(
                            Q(camp_sequence=marketing_sequence) &
                            Q(plan=update_sms_plan[0]))
                        call_plan_updating.delete()
                    with transaction.atomic():
                        for s in range(len(temps5)):
                            MarketingCampaign.objects.create(camp_sequence=marketing_sequence,
                                                             plan=update_sms_plan[0],
                                                             template=temps5[s],
                                                             title=update_sms_plan[
                                                                       0].sequence.name + " " +
                                                                   update_sms_plan[
                                                                       0].plan + str(s + 1),
                                                             hash_off=str(s + 1) + ' of ' + str(len(temps5)),
                                                             temperature=temperature_radio,
                                                             scheduled_plan_for=SMS_date,
                                                             timezone_gap_in_hours=time_dif,
                                                             # days_gap_in_campaign=sms_break_td[s],
                                                             marketing_details=plan_details,
                                                             break_into=sms_break,
                                                             maj_market=major_market[0],
                                                             responsible=res_user[0],
                                                             send_on=send_on_sms,
                                                             user=request.user.email)
                        MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='SMS')).update(break_into=sms_break,
                                                                                                days_gap_in_campaign=sms_break_td,
                                                                                                send_on=send_on_sms,
                                                                                                scheduled_plan_for=SMS_date)

            # for EMAIL
            if MarketingPlan.objects.filter(Q(sequence=marketing_sequence) & Q(plan='EMAIL')).exists():
                update_email_plan = MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='EMAIL'))
                temps6 = PlanRoundTemplate.objects.filter(plan=update_email_plan[0]).order_by('id')

                for e in range(len(temps6)):
                    with transaction.atomic():
                        e_round = request.POST.get("EMAIL" + str(e + 1))
                        if e_round and int(e_round) > 0:
                            temps6[e].touch_round_after_days = e_round
                            temps6[e].save()

                if create_marketing == 'Yes':
                    Email_date = Email_date.replace('/', '-')
                    try:
                        Email_date = datetime.datetime.strptime(Email_date, "%Y-%m-%d %H:%M:%S.%f")
                        # Email_date = Email_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    except:
                        Email_date = datetime.datetime.strptime(Email_date, "%Y-%m-%d %H:%M")
                    Email_date += timedelta(hours=int(time_dif))
                    if Email_date.hour > 12:
                        Email_date = Email_date.replace(hour=arr[Email_date.hour])
                    else:
                        pass
                    if MarketingCampaign.objects.filter(Q(camp_sequence=marketing_sequence) &
                                                        Q(plan=update_email_plan[0])).exists():
                        call_plan_updating = MarketingCampaign.objects.filter(
                            Q(camp_sequence=marketing_sequence) &
                            Q(plan=update_email_plan[0]))
                        call_plan_updating.delete()
                    with transaction.atomic():
                        for e in range(len(temps6)):
                            MarketingCampaign.objects.create(camp_sequence=marketing_sequence,
                                                             plan=update_email_plan[0],
                                                             template=temps6[e],
                                                             title=update_email_plan[
                                                                       0].sequence.name + " " +
                                                                   update_email_plan[
                                                                       0].plan + str(e + 1),
                                                             hash_off=str(e + 1) + ' of ' + str(len(temps6)),
                                                             temperature=temperature_radio,
                                                             scheduled_plan_for=Email_date,
                                                             timezone_gap_in_hours=time_dif,
                                                             # days_gap_in_campaign=email_break_td[e],
                                                             marketing_details=plan_details,
                                                             break_into=email_break,
                                                             maj_market=major_market[0],
                                                             responsible=res_user[0],
                                                             send_on=send_on_email,
                                                             user=request.user.email)

                        MarketingPlan.objects.filter(Q(sequence__id=pk) & Q(plan='EMAIL')).update(break_into=email_break,
                                                                                                  days_gap_in_campaign=email_break_td,
                                                                                                  send_on=send_on_email,
                                                                                                  scheduled_plan_for=Email_date)

            return redirect('/marketing/sequence_list/home')
        except:
            print(traceback.print_exc())
            return redirect('/marketing/sequence_list/home')
    else:
        schedule_date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')
        sc_date = {
            'Cold Call': schedule_date,
            'Direct Mail': schedule_date,
            'Voice Broadcast': schedule_date,
            'RVM': schedule_date,
            'SMS': schedule_date,
            'EMAIL': schedule_date
        }

        campaign_gap = {
            'Cold Call': [],
            'Direct Mail': [],
            'Voice Broadcast': [],
            'RVM': [],
            'SMS': [],
            'EMAIL': []
        }

        break_into = {
            'Cold Call': 0,
            'Direct Mail': 0,
            'Voice Broadcast': 0,
            'RVM': 0,
            'SMS': 0,
            'EMAIL': 0
        }
        send_on = {
            'Cold Call': 'M-S',
            'Direct Mail': 'M-S',
            'Voice Broadcast': 'M-S',
            'RVM': 'M-S',
            'SMS': 'M-S',
            'EMAIL': 'M-S'
        }
        queryset = MarketingSequence.objects.get(id=pk)
        total_records = Prospect_Properties.objects.filter(list=queryset.list)
        sequence_plans = MarketingPlan.objects.filter(sequence=queryset)
        plans_data = []
        plan_status = []
        if sequence_plans:
            for plan in sequence_plans:
                # sc_date[plan.plan] = plan.scheduled_plan_for.strftime('%Y/%m/%d %H:%M:%S.%f')
                campaign_gap[plan.plan] = [int(g) for g in plan.days_gap_in_campaign]
                temp_length = 0
                temp_ids = []
                temp = PlanRoundTemplate.objects.filter(plan=plan).order_by('id')
                if temp:
                    temp_length = len(temp)
                    temp_ids = [[i.id, i.touch_status, i.touch_round_after_days] for i in temp]

                if MarketingCampaign.objects.filter(plan=plan).exists():
                    schedule = MarketingCampaign.objects.filter(plan=plan).order_by('id')
                    schedule_plan_date = schedule[0].scheduled_plan_for + timedelta(hours=-int(queryset.timezone_gap_in_hours))
                    if schedule_plan_date.hour < 12:
                        schedule_plan_date = schedule_plan_date.replace(hour=arr2[schedule_plan_date.hour])
                    sc_date[plan.plan] = schedule_plan_date.strftime('%Y/%m/%d %H:%M:%S.%f')
                    if plan.plan in break_into:
                        break_into[plan.plan] = plan.break_into
                    if plan.plan in send_on:
                        send_on[plan.plan] = plan.send_on

                    plan_status.append({plan.plan: [s.campaigning_status for s in schedule]})

                plans_dict = {
                    plan.plan: temp_length,
                    "temp_ids": temp_ids,
                    "lengths": temp_length,
                }
                plans_data.append(plans_dict)
        major_markets = MajorMarket.objects.all()
        sub = UserProfile.objects.get(user=request.user)

        if sub.role.role_name == "Sub User":
            sub_users = UserProfile.objects.filter(created_by=sub.created_by)
        else:
            sub_users = UserProfile.objects.filter(created_by=sub, role__role_name='Sub User')
        users_list = []
        for users in sub_users:
            lis_data = {
                "id": users.user.id,
                "username": users.user.username
            }
            users_list.append(lis_data)
        print("users_list: ",users_list)
        break_into['cold_call'] = break_into.pop('Cold Call')
        break_into['direct_mail'] = break_into.pop('Direct Mail')
        break_into['voice_broadcast'] = break_into.pop('Voice Broadcast')

        campaign_gap['cold_call'] = campaign_gap.pop('Cold Call')
        campaign_gap['direct_mail'] = campaign_gap.pop('Direct Mail')
        campaign_gap['voice_broadcast'] = campaign_gap.pop('Voice Broadcast')

        send_on['cold_call'] = send_on.pop('Cold Call')
        send_on['direct_mail'] = send_on.pop('Direct Mail')
        send_on['voice_broadcast'] = send_on.pop('Voice Broadcast')

        sc_date['cold_call'] = sc_date.pop('Cold Call')
        sc_date['direct_mail'] = sc_date.pop('Direct Mail')
        sc_date['voice_broadcast'] = sc_date.pop('Voice Broadcast')

        # total_records_list = []
        # for records in total_records:
        #     rec_data = {
        #         "name": records.firstname +' '+ records.lastname,
        #         "propertyaddress": records.propertyaddress + ' , ' + records.propertycity + (' , ' + records.propertystate if records.propertystate else +' , '+records.propertyzip),
        #         "mailingaddress": records.mailingaddress if records.mailingaddress else "",
        #         "list_count": records.list_count,
        #         "tag_count": records.tag_count
        #     }
        #     total_records_list.append(rec_data)

        return render(request, 'marketing_machine/marketing_plan.html', {"queryset": queryset,
                                                                         "total_records": len(total_records),
                                                                         "related_prospects_data": [],
                                                                         "rounds": [i for i in range(1, 31)],
                                                                         "scheduled_date": sc_date,
                                                                         "campaign_gap": campaign_gap,
                                                                         "break_into": break_into,
                                                                         "send_on": send_on,
                                                                         "sub_users": users_list,
                                                                         "major_markets": major_markets,
                                                                         "plans_data": plans_data,
                                                                         "plan_status": plan_status,
                                                                         "user_name": request.user.id})


class GetRelatedProspects(APIView):
    def post(self, request):
        pk = request.data.get('seq_id')
        queryset = MarketingSequence.objects.get(id=pk)
        total_records = Prospect_Properties.objects.filter(list=queryset.list)
        total_records_list = []
        for records in total_records:
            rec_data = {
                "name": records.firstname + ' ' + records.lastname,
                "propertyaddress": records.propertyaddress + ' , ' + records.propertycity + (
                    ' , ' + records.propertystate if records.propertystate else +' , ' + records.propertyzip),
                "mailingaddress": records.mailingaddress if records.mailingaddress else "",
                "list_count": records.list_count,
                "tag_count": records.tag_count
            }
            total_records_list.append(rec_data)
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Success",
            "data": total_records_list
        })


# @method_decorator(user_has_marketing_plan_Permission, name='post')
class CreatePlanTemplatesAndPlans(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        sequence_id = request.data.get('seq')
        temp_count = request.data.get('temp_count')
        market_plan = request.data.get('market_plan')
        sequence = MarketingSequence.objects.get(id=sequence_id)
        try:
            temp_ids = []
            if MarketingPlan.objects.filter(Q(sequence_id=sequence_id) & Q(plan=market_plan)).exists():
                MarketingPlan.objects.filter(sequence_id=sequence_id, plan=market_plan).update(touch_rounds=temp_count)
                if temp_count == '0':
                    MarketingPlan.objects.filter(Q(sequence_id=sequence_id) & Q(plan=market_plan)).delete()
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Success",
                        "temp_ids": temp_ids,
                    })
                else:
                    with transaction.atomic():
                        new_marketing = MarketingPlan.objects.filter(Q(sequence=sequence) & Q(plan=market_plan))
                        PlanRoundTemplate.objects.filter(plan=new_marketing[0]).delete()
                        objects = (PlanRoundTemplate(plan=new_marketing[0], name=market_plan + "- Touch %s" % i,
                                                     detail="Create template for :" + market_plan + "- Touch %s" % i,
                                                     more_info="Create template for :" + market_plan + "- Touch %s" % i,
                                                     touch_round_number="Touch %s" % i,
                                                     touch_status='Active') for i in range(1, int(temp_count) + 1))
                        PlanRoundTemplate.objects.bulk_create(list(objects))
                        queryset = PlanRoundTemplate.objects.filter(plan=new_marketing[0]).order_by('id')
                        return Response({
                            "status": status.HTTP_200_OK,
                            "message": "Success",
                            "temp_ids": [k.id for k in queryset],
                        })
            else:
                with transaction.atomic():
                    new_marketing = MarketingPlan.objects.create(sequence=sequence, plan=market_plan,
                                                                 touch_rounds=temp_count, days_gap_in_campaign=0,
                                                                 created_at=datetime.datetime.now())
                    objects = (PlanRoundTemplate(plan=new_marketing, name=market_plan+"- Touch %s" % i,
                                                 detail="Create template for :"+market_plan+"- Touch %s" % i,
                                                 more_info="Create template for :"+market_plan+"- Touch %s" % i,
                                                 touch_round_number="Touch %s" % i,
                                                 touch_status='Active') for i in range(1, int(temp_count)+1))
                    PlanRoundTemplate.objects.bulk_create(list(objects))
                    queryset = PlanRoundTemplate.objects.filter(plan=new_marketing).order_by('id')
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Success",
                        "temp_ids": [k.id for k in queryset],
                    })
        except:
            print(traceback.print_exc())
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                             "message": "Server error"})


@user_has_marketing_plan_Permission
def marketing_template_view(request, pk):

    if request.method == 'POST':
        try:
            detail = request.POST.get("detail")
            info = request.POST.get("info")
            touch_status = request.POST.get("customRadio1")

            obj = PlanRoundTemplate.objects.get(id=pk)
            obj.detail = detail
            obj.more_info = info
            obj.touch_status = touch_status
            if request.FILES:
                image = request.FILES.get('image')
                obj.touch_file = image
            obj.save()
        except:
            print(traceback.print_exc())
            return render(request, 'marketing_machine/templates_list.html')
        return redirect('/marketing/templates_list/home')

    queryset = PlanRoundTemplate.objects.get(id=pk)
    return render(request, 'marketing_machine/marketing_template.html', {"queryset": queryset})


@user_has_marketing_plan_Permission
def marketing_templates_list(request, pk):
    queryset = []
    if request.method == 'POST':
        pass
    else:
        user_sequences = MarketingSequence.objects.filter(user=request.user)
        all_plans = MarketingPlan.objects.filter(sequence__in=user_sequences)
        # for active templates
        active_templates = PlanRoundTemplate.objects.filter(plan__in=all_plans, touch_status='Active')
        call_active = active_templates.filter(plan__plan='Cold Call')
        mail_active = active_templates.filter(plan__plan='Direct Mail')
        voice_active = active_templates.filter(plan__plan='Voice Broadcast')
        rvm_active = active_templates.filter(plan__plan='RVM')
        sms_active = active_templates.filter(plan__plan='SMS')
        email_active = active_templates.filter(plan__plan='EMAIL')

        # for inactive templates
        inactive_templates = PlanRoundTemplate.objects.filter(plan__in=all_plans, touch_status='InActive')
        call_inactive = inactive_templates.filter(plan__plan='Cold Call')
        mail_inactive = inactive_templates.filter(plan__plan='Direct Mail')
        voice_inactive = inactive_templates.filter(plan__plan='Voice Broadcast')
        rvm_inactive = inactive_templates.filter(plan__plan='RVM')
        sms_inactive = inactive_templates.filter(plan__plan='SMS')
        email_inactive = inactive_templates.filter(plan__plan='EMAIL')

        # for pending templates
        pending_templates = PlanRoundTemplate.objects.filter(plan__in=all_plans, touch_status='Pending')
        call_pending = pending_templates.filter(plan__plan='Cold Call')
        mail_pending = pending_templates.filter(plan__plan='Direct Mail')
        voice_pending = pending_templates.filter(plan__plan='Voice Broadcast')
        rvm_pending = pending_templates.filter(plan__plan='RVM')
        sms_pending = pending_templates.filter(plan__plan='SMS')
        email_pending = pending_templates.filter(plan__plan='EMAIL')

        templates_count = {
            "active_templates": len(active_templates),
            "call_active": len(call_active),
            "mail_active": len(mail_active),
            "voice_active": len(voice_active),
            "rvm_active": len(rvm_active),
            "sms_active": len(sms_active),
            "email_active": len(email_active),
            "inactive_templates": len(inactive_templates),
            "call_inactive": len(call_inactive),
            "mail_inactive": len(mail_inactive),
            "voice_inactive": len(voice_inactive),
            "rvm_inactive": len(rvm_inactive),
            "sms_inactive": len(sms_inactive),
            "email_inactive": len(email_inactive),
            "pending_templates": len(pending_templates),
            "call_pending": len(call_pending),
            "mail_pending": len(mail_pending),
            "voice_pending": len(voice_pending),
            "rvm_pending": len(rvm_pending),
            "sms_pending": len(sms_pending),
            "email_pending": len(email_pending),
        }

        if pk == 'home':
            queryset = PlanRoundTemplate.objects.filter(plan__in=all_plans)

        elif pk == 'all_active':
            queryset = active_templates

        elif pk == 'call_active':
            queryset = call_active

        elif pk == 'mail_active':
            queryset = mail_active

        elif pk == 'voice_active':
            queryset = voice_active

        elif pk == 'rvm_active':
            queryset = rvm_active

        elif pk == 'sms_active':
            queryset = sms_active

        elif pk == 'email_active':
            queryset = email_active

        # for inactive sidebar menu
        elif pk == 'all_inactive':
            queryset = inactive_templates

        elif pk == 'call_inactive':
            queryset = call_inactive

        elif pk == 'mail_inactive':
            queryset = mail_inactive

        elif pk == 'voice_inactive':
            queryset = voice_inactive

        elif pk == 'rvm_inactive':
            queryset = rvm_inactive

        elif pk == 'sms_inactive':
            queryset = sms_inactive

        elif pk == 'email_inactive':
            queryset = email_inactive

        # for pending sidebar menu
        elif pk == 'all_pending':
            queryset = pending_templates

        elif pk == 'call_pending':
            queryset = call_pending

        elif pk == 'mail_pending':
            queryset = mail_pending

        elif pk == 'voice_pending':
            queryset = voice_pending

        elif pk == 'rvm_pending':
            queryset = rvm_pending

        elif pk == 'sms_pending':
            queryset = sms_pending

        elif pk == 'email_pending':
            queryset = email_pending

        data_set = []
        if queryset:
            for query in queryset:
                query_data = {
                    "id": query.id,
                    "name": query.name,
                    "plan": query.plan.plan,
                    "sequence": query.plan.sequence.name,
                    "status": query.touch_status,
                    "date": query.created_at.strftime('%m/%d/%Y %H:%M:%S.%f').split('.')[0]
                }
                data_set.append(query_data)

        return render(request, 'marketing_machine/templates_list.html', {"templates_count": templates_count,
                                                                         "data_set": data_set})


@user_has_marketing_plan_Permission
def create_marketing_campaign(request):
    if request.method == 'POST':
        try:
            title = request.POST.get("title")
            time_dif = request.POST.get("time_dif")
            planer = request.POST.get("planer")
            hash_off = request.POST.get("hash_off")
            temperature = request.POST.get("temperature")
            maj_market = request.POST.get("maj_market")
            responsible = request.POST.get("responsible")
            send_via = request.POST.get("send_via")
            dist_status = request.POST.get("dist_status")
            approval = request.POST.get("approval")
            total_units = request.POST.get("total_units")
            touch = request.POST.get("touch")
            scheduled_for = request.POST.get("scheduled_for")
            notes = request.POST.get("notes")
            mark_details = request.POST.get("mark_details")

            scheduled_for = scheduled_for.replace('/', '-')
            try:
                scheduled_for = datetime.datetime.strptime(scheduled_for, "%Y-%m-%d %H:%M:%S.%f")
            except:
                scheduled_for = datetime.datetime.strptime(scheduled_for, "%Y-%m-%d %H:%M")
            scheduled_for = scheduled_for + timedelta(hours=int(time_dif))
            if scheduled_for.hour > 12:
                scheduled_for = scheduled_for.replace(hour=arr[scheduled_for.hour])
                time_format = 'PM'
            else:
                time_format = 'AM'
            major_market = MajorMarket.objects.get(id=maj_market)
            if planer:
                sequence = MarketingSequence.objects.get(id=planer)
            else:
                sequence = None
            if responsible:
                responsible_user = User.objects.get(username=responsible)
                send_event('prospectx' + str(responsible_user.id), 'message', 'A New Marketing Campaign has been created for you!')
                Notification.objects.create(user=responsible_user, title="A New Marketing Campaign has been created for you!")
                Notification_Pill.objects.filter(user=responsible_user).update(notification_pill=F('notification_pill') + 1)
                # message_body = "A New Marketing Campaign " + title + " for the Plan " + send_via + \
                #                " against Sequence " + sequence.name if sequence else "Anonymous" + " has been created for you!"
                # send_twilio_message("user", message_body)
                if Notification_Pill.objects.filter(user=responsible_user, email_notification=True):
                    email_from = settings.EMAIL_HOST_USER
                    email_to = responsible_user.email
                    message_body = "A New Marketing Campaign " + title + " for the Plan " + send_via + \
                                   " against Sequence " + sequence.name if sequence else "Anonymous" + " has been created for you!"
                    send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                    send_email.content_subtype = 'html'
                    send_email.send()
                    # send_twilio_message(1, message_body)
            else:
                responsible_user = None
            with transaction.atomic():
                if sequence:
                    if MarketingPlan.objects.filter(sequence=sequence, plan=send_via).exists():
                        MarketingPlan.objects.filter(Q(sequence=sequence) & Q(plan=send_via)).update(touch_rounds=touch)
                    else:
                        MarketingPlan.objects.create(sequence=sequence, plan=send_via, touch_rounds=touch,
                                                     days_gap_in_campaign='0', created_at=datetime.datetime.now())
                    plan = MarketingPlan.objects.filter(sequence=sequence, plan=send_via)
                    template = PlanRoundTemplate.objects.create(plan=plan[0], name=send_via+' - Touch '+str(touch),
                                                                detail='Create template for :'+send_via+' - Touch '+str(touch),
                                                                more_info='Create template for :'+send_via+' - Touch '+str(touch),
                                                                touch_round_number='Touch '+str(touch))

                    MarketingCampaign.objects.create(camp_sequence=sequence, plan=plan[0], template=template,
                                                     title=title, hash_off=hash_off, temperature= temperature,
                                                     distribution_status=dist_status, approval=approval,
                                                     total_units=total_units, scheduled_plan_for=scheduled_for,
                                                     notes=notes, marketing_details=mark_details,
                                                     timezone_gap_in_hours=time_dif,
                                                     time_format=time_format,
                                                     maj_market=major_market,
                                                     responsible=responsible_user,
                                                     is_single=True,
                                                     created_at=datetime.datetime.now(),
                                                     )
                    if request.FILES:
                        image = request.FILES.get('image')
                        MarketingCampaign.objects.filter(Q(camp_sequence=sequence) & Q(plan=plan[0]) & Q(template=template)).update(campaign_file=image)
                else:
                    mark_plan = MarketingPlan.objects.create(plan=send_via, touch_rounds=touch,
                                                             days_gap_in_campaign='0', created_at=datetime.datetime.now())
                    template = PlanRoundTemplate.objects.create(plan=mark_plan, name=send_via + ' - Touch ' + str(touch),
                                                                detail='Create template for :' + send_via + ' - Touch ' + str(
                                                                    touch),
                                                                more_info='Create template for :' + send_via + ' - Touch ' + str(
                                                                    touch),
                                                                touch_round_number='Touch ' + str(touch))
                    MarketingCampaign.objects.create(plan=mark_plan, template=template, user=request.user.email,
                                                     title=title, hash_off=hash_off, temperature=temperature,
                                                     distribution_status=dist_status, approval=approval,
                                                     total_units=total_units, scheduled_plan_for=scheduled_for,
                                                     notes=notes, marketing_details=mark_details,
                                                     timezone_gap_in_hours=time_dif,
                                                     maj_market=major_market,
                                                     responsible=responsible_user,
                                                     is_single=True,
                                                     created_at=datetime.datetime.now(),
                                                     )
                return redirect('/marketing/campaign_list/home')
        except:
            print(traceback.print_exc())
            return redirect('/marketing/campaign_list/home')
    sequences = MarketingSequence.objects.filter(user=request.user)
    markets = MajorMarket.objects.all()
    user = UserProfile.objects.get(user=request.user)
    if user.role.role_name == "Sub User":
        sub_users = UserProfile.objects.filter(created_by=user.created_by)
    else:
        sub_users = UserProfile.objects.filter(created_by=user, role__role_name='Sub User')
    users_list = []
    for users in sub_users:
        lis_data = {
            "id": users.id,
            "username": users.user.username
        }
        users_list.append(lis_data)
    today_date = datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S.%f')
    return render(request, 'marketing_machine/create_campaign.html', {"sequences": sequences,
                                                                      "users_list": users_list,
                                                                      "markets": markets,
                                                                      "rounds": [i for i in range(1, 31)],
                                                                      "today_date": today_date,
                                                                      })


@user_has_marketing_plan_Permission
def update_marketing_campaign(request, pk):
    if request.method == 'POST':
        title = request.POST.get("title")
        time_dif = request.POST.get("time_dif")
        camp_id = request.POST.get("camp_id")
        seq_id = request.POST.get("seq_id")
        hash_off = request.POST.get("hash_off")
        temperature = request.POST.get("temperature")
        maj_market = request.POST.get("maj_market")
        responsible = request.POST.get("responsible")
        send_via = request.POST.get("send_via2")
        dist_status = request.POST.get("dist_status")
        approval = request.POST.get("approval")
        total_units = request.POST.get("total_units")
        # touch = request.POST.get("touch")
        scheduled_for = request.POST.get("scheduled_for")
        scheduled_for = scheduled_for.replace('/', '-')
        try:
            scheduled_for = datetime.datetime.strptime(scheduled_for, "%Y-%m-%d %H:%M:%S.%f")
        except:
            scheduled_for = datetime.datetime.strptime(scheduled_for, "%Y-%m-%d %H:%M")
        scheduled_for = scheduled_for+ timedelta(hours=int(time_dif))
        notes = request.POST.get("notes")
        mark_details = request.POST.get("mark_details")
        # temp_id = request.POST.get("temp_id")
        # plan_id = request.POST.get("plan_id")
        # print("seq_id: ", seq_id)
        major_market = MajorMarket.objects.get(id=maj_market)
        if seq_id != 'None':
            sequence = MarketingSequence.objects.get(id=seq_id)
        else:
            sequence = None
        if responsible:
            responsible_user = User.objects.get(username=responsible)
            send_event('Prospect X' + str(responsible_user.id), 'message',
                       'A Marketing Campaign has been updated!')
            Notification.objects.create(user=responsible_user,
                                        title="A Marketing Campaign has been updated!")
            Notification_Pill.objects.filter(user=responsible_user).update(notification_pill=F('notification_pill') + 1)
            if Notification_Pill.objects.filter(user=responsible_user, email_notification=True):
                email_from = settings.EMAIL_HOST_USER
                email_to = responsible_user.email
                message_body = "A Marketing Campaign " + title + " for the Plan " + send_via + \
                               " against Sequence " + sequence.name if sequence else "Anonymous"+ " has been Updated!"
                send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                send_email.content_subtype = 'html'
                send_email.send()
        else:
            responsible_user = None
        try:
            with transaction.atomic():
                if sequence:
                    MarketingCampaign.objects.filter(id=camp_id).update(
                        camp_sequence=sequence,
                        hash_off=hash_off, temperature=temperature,
                        distribution_status=dist_status, approval=approval,
                        total_units=total_units, scheduled_plan_for=scheduled_for,
                        timezone_gap_in_hours=time_dif,
                        notes=notes, marketing_details=mark_details,
                        maj_market=major_market,
                        responsible=responsible_user,
                    )

                else:
                    MarketingCampaign.objects.filter(id=camp_id).update(
                                                    camp_sequence=sequence,
                                                    hash_off=hash_off, temperature=temperature,
                                                    distribution_status=dist_status, approval=approval,
                                                    total_units=total_units, scheduled_plan_for=scheduled_for,
                                                    notes=notes, marketing_details=mark_details,
                                                    maj_market=major_market,
                                                    timezone_gap_in_hours=time_dif,
                                                    responsible=responsible_user,
                                                )

            return redirect('/marketing/campaign_list/home/')
        except:
            print(traceback.print_exc())
            return render(request, 'marketing_machine/update_campaign.html')
    major_market_query = MajorMarket.objects.all()
    user = UserProfile.objects.get(user=request.user)
    if user.role.role_name == "Sub User":
        responsible_users_query = UserProfile.objects.filter(created_by=user.created_by)
    else:
        responsible_users_query = UserProfile.objects.filter(created_by=user, role__role_name='Sub User')
    campaign = MarketingCampaign.objects.get(id=pk)
    sequences = MarketingSequence.objects.filter(user=request.user)
    schedule = campaign.scheduled_plan_for + timedelta(hours=-int(campaign.timezone_gap_in_hours))
    if campaign.time_format == 'PM':
        schedule = schedule.replace(hour=arr2[schedule.hour])
    campaign_data = {
        "id": campaign.id,
        "title": campaign.title,
        "planer": campaign.camp_sequence.name if campaign.camp_sequence else None,
        "seq_id": campaign.camp_sequence.id if campaign.camp_sequence else None,
        "hash_off": campaign.hash_off,
        "temperature": campaign.temperature,
        "major_market": campaign.maj_market.id if campaign.maj_market else None,
        "responsible": campaign.responsible.username if campaign.responsible else None,
        "send_via": campaign.plan.plan if campaign.plan else "Anonymous",
        "plan_id": campaign.plan.id if campaign.plan else "Anonymous",
        "dist_status": campaign.distribution_status,
        "approval": campaign.approval,
        "units": campaign.total_units,
        "touch": campaign.template.touch_round_number if campaign.template else "",
        "scheduled_plan_for": schedule.strftime('%Y/%m/%d %H:%M:%S.%f'),
        "notes": campaign.notes,
        "template": campaign.template.id if campaign.template else "",
        "template_name": campaign.template.name if campaign.template else "",
        "mark_details": campaign.marketing_details,
        "image": campaign.campaign_file.url if campaign.campaign_file else None
    }

    return render(request, 'marketing_machine/update_campaign.html', {"campaign_data": campaign_data,
                                                                      "major_market_query": major_market_query,
                                                                      "responsible_users_query": responsible_users_query,
                                                                      "sequences": sequences,
                                                                      })


# @method_decorator(user_has_marketing_plan_Permission, name='post')
class CreateMajorMarket(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        mark_title = request.data.get("mark_title")
        market = request.data.get("market")
        state = request.data.get("state")
        try:
            if mark_title and market and state:
                if MajorMarket.objects.filter(title=mark_title).exists():
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Market Already Exists",
                    })
                else:
                    markets = MajorMarket.objects.create(title=mark_title, market=market, state=state)
                    data = {
                        "id": markets.id,
                        "title": mark_title
                    }
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Success",
                        "market_data": data
                    })
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Failed",
            })
        except:
            print(traceback.print_exc())
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                             "message": "Internal Server error"})


# @method_decorator(user_has_marketing_plan_Permission, name='post')
class GetMajorMarkets(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        markets = MajorMarket.objects.all()
        market_data = []
        for market in markets:
            data = {
                "id": market.id,
                "title": market.title
            }
            market_data.append(data)
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Success",
            "market_data": market_data
        })


class UpdateMajorMarket(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        title = request.data.get("title")
        market = request.data.get("market")
        state = request.data.get("state")
        id = request.data.get("id")
        try:
            if title and market and state and id:
                if MajorMarket.objects.filter(~Q(id=id)).filter(title=title).exists():
                    return Response({
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "message": "Market Already Exists",
                    })
                else:
                    MajorMarket.objects.filter(id=id).update(title=title, state=state, market=market)
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Market Updated Successfully",
                    })
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


def delete_market_view(request, pk):
    if request.user.is_authenticated:
        try:
            MajorMarket.objects.filter(id=pk).delete()
            return redirect('/marketing/major_markets')
        except:
            print(traceback.print_exc())
            return redirect('/marketing/major_markets')
    else:
        return redirect('/marketing/major_markets')


def major_markets_view(request):
    user = request.user
    major_markets = MajorMarket.objects.all().order_by('-id')
    return render(request, 'user/major_market_list.html', {"data": major_markets})


# @method_decorator(user_has_marketing_plan_Permission, name='post')
class GetSequenceDetails(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        id = request.data.get("id")
        campaign = MarketingSequence.objects.get(id=id)
        list_count = Prospect_Properties.objects.filter(list=campaign.list)
        market_data = {
            "name": campaign.name,
            "user": campaign.user.username,
            "list": campaign.list.list_name,
            "list_count": len(list_count),
            "status": campaign.status,
            "temperature": campaign.temperature,
            "details": campaign.details,
            "planning_status": campaign.planning_status,
            "create_marketing": campaign.create_marketing,
            "planning_done": campaign.planning_done,
            "created_at": campaign.created_at.date(),
        }
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Success",
            "market_data": market_data
        })


# @method_decorator(user_has_marketing_plan_Permission, name='post')
class GetTemplateDetails(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        id = request.data.get("id")
        template = PlanRoundTemplate.objects.get(id=id)
        template_data = {
            "name": template.name,
            "sequence": template.plan.sequence.name,
            "plan": template.plan.plan,
            "touch_round_number": template.touch_round_number,
            "touch_status": template.touch_status,
            "touch_round_after_days": template.touch_round_after_days,
            "detail": template.detail,
            "more_info": template.more_info,
            "created_at": template.created_at.date(),
        }
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Success",
            "template_data": template_data
        })


# @method_decorator(user_has_marketing_plan_Permission, name='post')
class GetCampaignDetails(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        id = request.data.get("id")
        campaign = MarketingCampaign.objects.get(id=id)
        campaign_data = {
            "name": campaign.title,
            "sequence": campaign.camp_sequence.name if campaign.camp_sequence else "Anonymous",
            "plan": campaign.plan.plan,
            "hash_off": campaign.hash_off,
            "temperature": campaign.temperature,
            "distribution_status": campaign.distribution_status,
            "approval": campaign.approval,
            "scheduled_plan_for": campaign.scheduled_plan_for,
            "notes": campaign.notes,
            "marketing_details": campaign.marketing_details,
            "break_into": campaign.break_into,
            "send_on": campaign.send_on,
            "maj_market": campaign.maj_market.title if campaign.maj_market else None,
            "responsible": campaign.responsible.username if campaign.responsible else None,
            "created_at": campaign.created_at.date(),
        }
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Success",
            "campaign_data": campaign_data
        })


class GetSearchedCampaigns(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        search_plan = request.data.get("search_plan")
        temperature_search = request.data.get("temperature_search")
        dist_search = request.data.get("dist_search")
        approval_search = request.data.get("approval_search")
        search_scheduled = request.data.get("search_scheduled")

        print("search plan: ", search_plan)
        print("temperature_search: ", temperature_search)
        print("dist_search: ", dist_search)
        print("approval_search: ", approval_search)
        print("search_scheduled: ", search_scheduled)
        campaign_data = MarketingCampaign.objects.filter(Q(plan__plan__in=search_plan) & Q(temperature__in=temperature_search)
                                                         & Q(distribution_status__in=dist_search) &
                                                         Q(approval__in=approval_search))
        print("campaign_data searched: ", campaign_data)
        campaign = MarketingCampaign.objects.get(id=id)
        campaign_data = {
            "name": campaign.title,
            "sequence": campaign.camp_sequence.name if campaign.camp_sequence else "Anonymous",
            "plan": campaign.plan.plan,
            "hash_off": campaign.hash_off,
            "temperature": campaign.temperature,
            "distribution_status": campaign.distribution_status,
            "approval": campaign.approval,
            "scheduled_plan_for": campaign.scheduled_plan_for,
            "notes": campaign.notes,
            "marketing_details": campaign.marketing_details,
            "break_into": campaign.break_into,
            "send_on": campaign.send_on,
            "maj_market": campaign.maj_market.title if campaign.maj_market else None,
            "responsible": campaign.responsible.username if campaign.responsible else None,
            "created_at": campaign.created_at.date(),
        }
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Success",
            "campaign_data": campaign_data
        })


@user_has_marketing_plan_Permission
def sequence_campaign_list(request, pk):
    campaigns = MarketingCampaign.objects.filter(camp_sequence__id=pk).order_by('-id')
    campaign_data = []
    for campaign in campaigns:
        schedule = campaign.scheduled_plan_for + timedelta(hours=-int(campaign.timezone_gap_in_hours))
        if schedule.hour < 12:
            schedule = schedule.replace(hour=arr2[schedule.hour])
        created_at = campaign.created_at + timedelta(hours=-int(campaign.timezone_gap_in_hours))
        data = {
            "id": campaign.id,
            "plan": campaign.plan.plan,
            "title": campaign.title,
            "planer": campaign.camp_sequence,
            "created_at": created_at,
            "hash_off": campaign.hash_off,
            "temperature": campaign.temperature,
            "major_market": campaign.maj_market,
            "responsible": campaign.responsible,
            "send_via": campaign.plan.plan,
            "distribution_status": campaign.distribution_status,
            "approval": campaign.approval,
            "units": campaign.total_units,
            "touch": campaign.template.touch_round_number if campaign.template else "",
            "scheduled_plan_for": schedule.strftime('%m/%d/%Y %H:%M:%S.%f').split('.')[0],
            "notes": campaign.notes,
            "template": campaign.template.id if campaign.template else "",
            "mark_details": campaign.marketing_details,
            "image": campaign.campaign_file
        }
        campaign_data.append(data)
    return render(request, 'marketing_machine/sequence_campaigns.html', {"campaigns_query": campaign_data})


@user_has_marketing_plan_Permission
def delete_sequence(request, pk):
    if request.user.is_authenticated:
        try:
            abc = MarketingSequence.objects.filter(id=pk)
            abc.delete()
            return redirect('/marketing/sequence_list/home')
        except:
            print(traceback.print_exc())
            return redirect('/marketing/sequence_list/home')
    else:
        return redirect('/marketing/sequence_list/home')


@user_has_marketing_plan_Permission
def delete_campaign(request, pk):
    if request.user.is_authenticated:
        try:
            abc = MarketingCampaign.objects.filter(id=pk)
            abc.delete()
            return redirect('/marketing/campaign_list/home')
        except:
            print(traceback.print_exc())
            return redirect('/marketing/campaign_list/home')
    else:
        return redirect('/marketing/campaign_list/home')


@user_has_marketing_plan_Permission
def delete_template(request, pk):
    if request.user.is_authenticated:
        try:
            abc = PlanRoundTemplate.objects.filter(id=pk)
            abc.delete()
            return redirect('/marketing/templates_list/home')
        except:
            print(traceback.print_exc())
            return redirect('/marketing/templates_list/home')
    else:
        return redirect('/marketing/templates_list/home')

