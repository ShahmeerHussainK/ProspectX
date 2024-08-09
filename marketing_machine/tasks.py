from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from task_management.models import Reminder
from .models import *
logger = get_task_logger(__name__)
from filter_prospects.models import *
from marketing_machine.models import *
from datetime import datetime, date, timedelta, timezone
from django.db.models import Q
import os
import requests
import json
import random
# Create your views here.
import pandas as pd
from prospectx_new import settings
from prospectx_new.settings import BASE_DIR
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.utils.timezone import utc
import traceback
from twilio.rest import Client
from prospectx_new.settings import account_sid_twilio, auth_token_twilio

arr = {13:1, 14:2, 15:3, 16:4, 17:5, 18:6, 19:7, 20:8, 21:9, 22:10, 23:11, 0:12}


@periodic_task(
    run_every=(crontab(minute='*/3')),
    name="run_single_marketing_campaigns",
    ignore_result=True
)
def run_single_marketing_campaigns():
    campaigns = MarketingCampaign.objects.filter(Q(campaigning_status='Pending') & Q(plan__plan='EMAIL')
                                                 & Q(camp_sequence__isnull=False)& Q(is_single=True))
    for camp in campaigns:
        prospect_obj = Prospect_Properties.objects.filter(list=camp.camp_sequence.list)
        if prospect_obj:
            emails = [e.email for e in prospect_obj if e.email != '']
            # print("Emails: ", emails)
            email_to = []
            if camp.template:
                if camp.responsible:
                    email_to.append(camp.responsible.email)
                else:
                    email_to.append(settings.EMAIL_HOST_USER)
                # time_zone = pytz.timezone('US/Arizona')
                # sdate = datetime.now()
                # sdate2 = time_zone.localize(sdate)
                # utc_date_time2 = sdate2.astimezone(pytz.utc)
                # print("utc_date_time2: ", utc_date_time2)
                #
                # print("utc: ",  datetime.utcnow())
                # print("scheduled_plan_for: ",  camp.scheduled_plan_for.utcnow())
                print("utc.date(): ", datetime.today().date())
                print("camp.scheduled_plan_for.date(): ", camp.scheduled_plan_for.date())
                print("datetime.today().hour: ", datetime.today().hour)
                print("camp.scheduled_plan_for.hour: ", camp.scheduled_plan_for.hour)
                if datetime.today().date() == camp.scheduled_plan_for.date():
                    if camp.scheduled_plan_for.hour > 12:
                        plan_hour = arr[camp.scheduled_plan_for.hour]
                    else:
                        plan_hour = camp.scheduled_plan_for.hour
                    if datetime.today().hour == plan_hour:
                        email_from = settings.EMAIL_HOST_USER
                        # print("in email: ", email_from)
                        # print("camp.template.detail: ", camp.template.detail)
                        message_body = camp.template.detail
                        send_email = EmailMessage("Prospect X", message_body, email_from, email_to, emails)
                        send_email.content_subtype = 'html'
                        send_email.send()
                        camp.campaigning_status = 'Sent'
                        camp.distribution_status = 'Completed'
                        camp.save()
                        # print("email sent")
    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/5', day_of_week='mon-fri')),
    name="run_sequence_campaigns1",
    ignore_result=True
)
def run_sequence_campaigns1():
    sequences = MarketingSequence.objects.filter(Q(create_marketing='Yes') & Q(is_completed='No')).order_by("id")
    for sequence in sequences:
        campaigns = MarketingCampaign.objects.filter(Q(campaigning_status='Pending') & Q(plan__plan='EMAIL')
                                                     & Q(camp_sequence=sequence) & Q(plan__send_on='M-F')
                                                     & Q(is_single=False)).order_by('id')
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if campaigns:
            # next_campaign = False
            ids = ''
            if campaigns.filter(current_campaign=True).exists():
                campaign = campaigns.filter(current_campaign=True).first()
                next_campaign = campaigns.filter(id=campaign.id + 1)
                #     next_campaign[0].current_campaign = True
                #     next_campaign[0].save()
                #     print("next_campaign  id: ", next_campaign[0].id)
                # record_ids = campaign.campaign_records_list
                # if next_campaign:

                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:

                    email_to = []
                    if campaign.template:
                        if campaign.responsible:
                            email_to.append(campaign.responsible.email)
                        else:
                            email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date() mon-fri: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                existing_records = campaign.campaign_records_list
                                emails = []
                                # emails = [e.email for e in prospect_obj if str(e.id) not in existing_records]
                                for i in prospect_obj:
                                    if str(i.id) not in existing_records:
                                        emails.append(i.email)
                                        ids += str(i.id) + ','
                                existing_records += ids
                                email_from = settings.EMAIL_HOST_USER
                                message_body = campaign.template.detail
                                send_email = EmailMessage("Prospect X", message_body, email_from, email_to, emails)
                                send_email.content_subtype = 'html'
                                send_email.send()
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.campaign_records_list = existing_records
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (campaign.scheduled_plan_for +
                                            timedelta(days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days+1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()

            else:
                campaign = campaigns[0]
                next_campaign = campaigns.filter(id=campaign.id + 1)
                # if campaigns[1]:
                    # next_campaign = campaigns[1]
                    # campaigns[1].current_campaign = True
                    # campaigns[1].save()

                    # record_ids = campaign.campaign_records_list
                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:
                    # emails = [e.email for e in prospect_obj if e.email != '']
                    # for i in prospect_obj:
                    #     ids += i.id+','
                    email_to = []
                    if campaign.template:
                        if campaign.responsible:
                            email_to.append(campaign.responsible.email)
                        else:
                            email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date() mon-fri: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                existing_records = campaign.campaign_records_list
                                emails = []
                                # emails = [e.email for e in prospect_obj if str(e.id) not in existing_records]
                                for i in prospect_obj:
                                    if str(i.id) not in existing_records:
                                        emails.append(i.email)
                                        ids += str(i.id) + ','
                                existing_records += ids
                                email_from = settings.EMAIL_HOST_USER
                                message_body = campaign.template.detail
                                send_email = EmailMessage("Prospect X", message_body, email_from, email_to, emails)
                                send_email.content_subtype = 'html'
                                send_email.send()
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days + 1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()

    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/5', day_of_week='mon-sat')),
    name="run_sequence_campaigns2",
    ignore_result=True
)
def run_sequence_campaigns2():
    sequences = MarketingSequence.objects.filter(Q(create_marketing='Yes') & Q(is_completed='No')).order_by("id")
    for sequence in sequences:
        campaigns = MarketingCampaign.objects.filter(Q(campaigning_status='Pending') & Q(plan__plan='EMAIL')
                                                     & Q(camp_sequence=sequence) & Q(plan__send_on='M-S')
                                                     & Q(is_single=False)).order_by('id')
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if campaigns:
            # next_campaign = False
            ids = ''
            if campaigns.filter(current_campaign=True).exists():
                campaign = campaigns.filter(current_campaign=True).first()
                next_campaign = campaigns.filter(id=campaign.id + 1)
                # if next_campaign:
                #     next_campaign[0].current_campaign = True
                #     next_campaign[0].save()
                #     print("next_campaign  id: ", next_campaign[0].id)
                # record_ids = campaign.campaign_records_list
                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:
                    # emails = [e.email for e in prospect_obj if e.email != '']
                    # for i in prospect_obj:
                    #     ids += i.id+','
                    email_to = []
                    if campaign.template:
                        if campaign.responsible:
                            email_to.append(campaign.responsible.email)
                        else:
                            email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date() mon-sat: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                existing_records = campaign.campaign_records_list
                                emails = []
                                # emails = [e.email for e in prospect_obj if str(e.id) not in existing_records]
                                for i in prospect_obj:
                                    if str(i.id) not in existing_records:
                                        emails.append(i.email)
                                        ids += str(i.id) + ','
                                existing_records += ids
                                email_from = settings.EMAIL_HOST_USER
                                message_body = campaign.template.detail
                                send_email = EmailMessage("Prospect X", message_body, email_from, email_to, emails)
                                send_email.content_subtype = 'html'
                                send_email.send()
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days + 1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()

            else:
                campaign = campaigns[0]
                next_campaign = campaigns.filter(id=campaign.id + 1)
                # if campaigns[1]:
                    # next_campaign = campaigns[1]
                    # campaigns[1].current_campaign = True
                    # campaigns[1].save()

                    # record_ids = campaign.campaign_records_list
                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:
                    # emails = [e.email for e in prospect_obj if e.email != '']
                    # for i in prospect_obj:
                    #     ids += i.id+','
                    email_to = []
                    if campaign.template:
                        if campaign.responsible:
                            email_to.append(campaign.responsible.email)
                        else:
                            email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date()mon-sat: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                existing_records = campaign.campaign_records_list
                                emails = []
                                # emails = [e.email for e in prospect_obj if str(e.id) not in existing_records]
                                for i in prospect_obj:
                                    if str(i.id) not in existing_records:
                                        emails.append(i.email)
                                        ids += str(i.id) + ','
                                existing_records += ids
                                email_from = settings.EMAIL_HOST_USER
                                message_body = campaign.template.detail
                                send_email = EmailMessage("Prospect X", message_body, email_from, email_to, emails)
                                send_email.content_subtype = 'html'
                                send_email.send()
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days + 1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()

    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="run_single_marketing_campaigns_sms",
    ignore_result=True
)
def run_single_marketing_campaigns_sms():
    campaigns = MarketingCampaign.objects.filter(Q(campaigning_status='Pending') & Q(plan__plan='SMS')
                                                 & Q(camp_sequence__isnull=False) & Q(is_single=True) &
                                                 Q(scheduled_plan_for__date=datetime.today().date()))
    print("campaigns got: ", campaigns)
    for camp in campaigns:
        print("in for loop")
        prospect_obj = Prospect_Properties.objects.filter(list=camp.camp_sequence.list)
        print("pros: ", prospect_obj)
        if prospect_obj:
            # emails = [e.email for e in prospect_obj if e.email != '']
            # print("Emails: ", emails)
            # email_to = []
            print("sms campaign")
            if camp.template:
                # if camp.responsible:
                #     email_to.append(camp.responsible.email)
                # else:
                #     email_to.append(settings.EMAIL_HOST_USER)
                print("sms campaign 2")
                print("single sms utc.date(): ", datetime.today().date())
                print("single sms camp.scheduled_plan_for.date(): ", camp.scheduled_plan_for.date())
                print("single sms datetime.today().hour: ", datetime.today().hour)
                print("single sms camp.scheduled_plan_for.hour: ", camp.scheduled_plan_for.hour)
                # if datetime.today().date() == camp.scheduled_plan_for.date():
                # if camp.scheduled_plan_for.hour > 12:
                #     plan_hour = arr[camp.scheduled_plan_for.hour]
                # else:
                #     plan_hour = camp.scheduled_plan_for.hour
                if datetime.today().hour == camp.scheduled_plan_for.hour:
                    client = Client(account_sid_twilio, auth_token_twilio)
                    message = client.messages.create(
                        from_='+12057515885',
                        body=camp.template.detail,
                        to='+923002021848',
                    )
                    camp.campaigning_status = 'Sent'
                    camp.distribution_status = 'Completed'
                    camp.save()
                    print(message.sid)
    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/5', day_of_week='mon-fri')),
    name="run_sequence_campaigns_sms1",
    ignore_result=True
)
def run_sequence_campaigns_sms1():
    sequences = MarketingSequence.objects.filter(Q(create_marketing='Yes') & Q(is_completed='No')).order_by("id")
    for sequence in sequences:
        campaigns = MarketingCampaign.objects.filter(Q(campaigning_status='Pending') & Q(plan__plan='SMS')
                                                     & Q(camp_sequence=sequence) & Q(plan__send_on='M-F')
                                                     & Q(is_single=False)).order_by('id')
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if campaigns:
            # next_campaign = False
            ids = ''
            if campaigns.filter(current_campaign=True).exists():
                campaign = campaigns.filter(current_campaign=True).first()
                next_campaign = campaigns.filter(id=campaign.id + 1)
                #     next_campaign[0].current_campaign = True
                #     next_campaign[0].save()
                #     print("next_campaign  id: ", next_campaign[0].id)
                # record_ids = campaign.campaign_records_list
                # if next_campaign:

                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:
                    # existing_records = sequence.campaign_records_list
                    # emails = [e.email for e in prospect_obj if e.email != '']
                    # for i in prospect_obj:
                    #     if str(i.id) not in ids:
                    #         ids += str(i.id)+','
                    # email_to = []
                    if campaign.template:
                        # if campaign.responsible:
                        #     email_to.append(campaign.responsible.email)
                        # else:
                        #     email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date() mon-fri: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                client = Client(account_sid_twilio, auth_token_twilio)
                                message = client.messages.create(
                                    from_='+12057515885',
                                    body=campaign.template.detail,
                                    to='+923002021848',
                                )
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (campaign.scheduled_plan_for +
                                            timedelta(days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days+1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()

            else:
                campaign = campaigns[0]
                next_campaign = campaigns.filter(id=campaign.id + 1)
                # if campaigns[1]:
                    # next_campaign = campaigns[1]
                    # campaigns[1].current_campaign = True
                    # campaigns[1].save()

                    # record_ids = campaign.campaign_records_list
                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:
                    # emails = [e.email for e in prospect_obj if e.email != '']
                    # for i in prospect_obj:
                    #     ids += i.id+','
                    # email_to = []
                    if campaign.template:
                        # if campaign.responsible:
                        #     email_to.append(campaign.responsible.email)
                        # else:
                        #     email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date() mon-fri: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                client = Client(account_sid_twilio, auth_token_twilio)
                                message = client.messages.create(
                                    from_='+12057515885',
                                    body=campaign.template.detail,
                                    to='+923002021848',
                                )
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = campaign.scheduled_plan_for + timedelta(
                                            days=campaign.template.touch_round_after_days + 1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()

    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/5', day_of_week='mon-sat')),
    name="run_sequence_campaigns_sms2",
    ignore_result=True
)
def run_sequence_campaigns_sms2():
    sequences = MarketingSequence.objects.filter(Q(create_marketing='Yes') & Q(is_completed='No')).order_by("id")
    for sequence in sequences:
        campaigns = MarketingCampaign.objects.filter(Q(campaigning_status='Pending') & Q(plan__plan='SMS')
                                                     & Q(camp_sequence=sequence) & Q(plan__send_on='M-S')
                                                     & Q(is_single=False)).order_by('id')
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if campaigns:
            # next_campaign = False
            # ids = ''
            if campaigns.filter(current_campaign=True).exists():
                campaign = campaigns.filter(current_campaign=True).first()
                next_campaign = campaigns.filter(id=campaign.id + 1)
                # if next_campaign:
                #     next_campaign[0].current_campaign = True
                #     next_campaign[0].save()
                #     print("next_campaign  id: ", next_campaign[0].id)
                # record_ids = campaign.campaign_records_list
                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:
                    # emails = [e.email for e in prospect_obj if e.email != '']
                    # for i in prospect_obj:
                    #     ids += i.id+','
                    # email_to = []
                    if campaign.template:
                        # if campaign.responsible:
                        #     email_to.append(campaign.responsible.email)
                        # else:
                        #     email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date() mon-sat: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                client = Client(account_sid_twilio, auth_token_twilio)
                                message = client.messages.create(
                                    from_='+12057515885',
                                    body=campaign.template.detail,
                                    to='+923002021848',
                                )
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days + 1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()

            else:
                campaign = campaigns[0]
                next_campaign = campaigns.filter(id=campaign.id + 1)
                # if campaigns[1]:
                    # next_campaign = campaigns[1]
                    # campaigns[1].current_campaign = True
                    # campaigns[1].save()

                    # record_ids = campaign.campaign_records_list
                prospect_obj = Prospect_Properties.objects.filter(list=campaign.camp_sequence.list)
                if prospect_obj:
                    # emails = [e.email for e in prospect_obj if e.email != '']
                    # for i in prospect_obj:
                    #     ids += i.id+','
                    # email_to = []
                    if campaign.template:
                        # if campaign.responsible:
                            # email_to.append(campaign.responsible.email)
                        # else:
                        #     email_to.append(settings.EMAIL_HOST_USER)
                        print("utc.date()mon-sat: ", datetime.today().date())
                        print("camp.scheduled_plan_for.date(): ", campaign.scheduled_plan_for.date())
                        print("datetime.today().hour: ", datetime.today().hour)
                        print("camp.scheduled_plan_for.astimezone(utc).hour: ", campaign.scheduled_plan_for.hour)
                        if datetime.today().date() == campaign.scheduled_plan_for.date():
                            if campaign.scheduled_plan_for.hour > 12:
                                plan_hour = arr[campaign.scheduled_plan_for.hour]
                            else:
                                plan_hour = campaign.scheduled_plan_for.hour
                            if datetime.today().hour == plan_hour:
                                client = Client(account_sid_twilio, auth_token_twilio)
                                message = client.messages.create(
                                    from_='+12057515885',
                                    body=campaign.template.detail,
                                    to='+923002021848',
                                )
                                campaign.campaigning_status = 'Sent'
                                campaign.current_campaign = False
                                campaign.distribution_status = 'Completed'
                                campaign.save()

                                if next_campaign:
                                    next_campaign[0].current_campaign = True
                                    if (datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)).strftime("%A") in week_days:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days)
                                    else:
                                        next_day = datetime.today() + timedelta(
                                            days=campaign.template.touch_round_after_days + 1)
                                    if next_day.strftime("%A") in week_days:
                                        pass
                                    else:
                                        next_day += timedelta(days=1)
                                    next_campaign[0].scheduled_plan_for = next_day
                                    next_campaign[0].save()
                                else:
                                    sequence.is_completed = 'Yes'
                                    sequence.save()
    temp = {}
    return JsonResponse(temp)
