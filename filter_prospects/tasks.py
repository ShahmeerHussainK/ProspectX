import traceback
import time
import numpy
import stripe
from django.db.models import F
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from datetime import timedelta
from task_management.models import Reminder
from user.models import UserProfile, UserStripeDetail, UserStats
from xsiteApp.models import Websites
from .models import *
from notification.models import *
from django.conf import settings
from django.core.mail import EmailMessage
from django_eventstream import send_event
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# from .views import read_data_from_file_and_save_in_database

logger = get_task_logger(__name__)
from filter_prospects.models import *
from django.db.models import Q, F
import os
import requests
import json
import random
# Create your views here.
import pandas as pd
from prospectx_new import settings
from prospectx_new.settings import BASE_DIR, Godaddy_api_key, Godaddy_secret_key
from django.http import JsonResponse
from math import ceil
from django.db.models import IntegerField, Value

# API key and secret are sent in the header
headers = {"Authorization": "sso-key {}:{}".format(Godaddy_api_key, Godaddy_secret_key)}
renewal_url = "https://api.ote-godaddy.com/v1/domains/"


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="check_excel_file_uploades",
    ignore_result=True
)
def check_excel_file_uploades():
    print("In Import Function")
    temp = {}
    print(File.objects.filter(Q(is_process_started=True) & ~Q(els_status='es done')).count())
    if File.objects.filter(Q(is_process_started=True) & ~Q(els_status='es done')).count() == 0:
        print("picking up a new file to import")
        file_obj = File.objects.filter(is_process_started=False).order_by("file_size")[:1]
        insert_count = 0
        for files in file_obj:
            files.is_process_started = True
            files.save()
            try:
                profile = UserProfile.objects.get(user=files.user)
                if profile.role.role_name == "Admin User":
                    user = files.user
                else:
                    user = profile.created_by.user
                users = UserProfile.objects.filter(created_by__user=user).values('user')

                path = os.path.join(BASE_DIR, 'media') + "/files"
                file_path = path + '/' + files.file_name
                keep_col = files.destination_fields.split(',')

                if not ".csv" in files.file_name:
                    data_xls = pd.read_excel(file_path)
                    file_path = path + '/' + files.file_name.split('.')[0] + '.csv'
                    data_xls.to_csv(file_path, encoding='utf-8', index=False)
                    data_xls = pd.read_csv(file_path)
                else:
                    data_xls = pd.read_csv(file_path)

                data = dict()
                j = 0
                col_name = ""
                col_name1 = ""
                col_name2 = ""
                col_name3 = ""
                for i in data_xls:
                    if keep_col[j] != "not_import":
                        data[keep_col[j]] = i
                        if keep_col[j] == "propertyaddress":
                            col_name = i
                        if keep_col[j] == "propertycity":
                            col_name1 = i
                        if keep_col[j] == "propertystate":
                            col_name2 = i
                        if keep_col[j] == "propertyzip":
                            col_name3 = i
                    j += 1

                modified_data_xls = data_xls[data_xls[col_name].notna()]
                modified_data_xls = modified_data_xls[data_xls[col_name1].notna()]
                modified_data_xls = modified_data_xls[data_xls[col_name2].notna()]
                modified_data_xls = modified_data_xls[data_xls[col_name3].notna()]
                modified_data_xls = modified_data_xls.drop_duplicates([col_name])

                all_addresses = modified_data_xls[col_name]
                all_addresses_list = all_addresses.tolist()  # all address list

                existing_prospects = Prospect_Properties.objects.filter(
                    (Q(file__user=user) | Q(file__user__in=users)) & Q(
                        propertyaddress__in=all_addresses_list) & Q(file__pk__lte=files.pk)).distinct(
                    'propertyaddress').values_list('propertyaddress', flat=True)
                copy_existing_prospects = list(existing_prospects)

                data['opt_out'] = 'opt_out'
                data['skip_traced'] = 'skip_traced'
                data['is_validate_complete'] = 'is_validate_complete'
                data['skipped'] = 'skipped'
                data['list_count'] = 'list_count'
                data['tag_count'] = 'tag_count'
                data['added_to_els'] = 'added_to_els'

                opt_out_list = []
                skip_traced_list = []
                skipped_list = []
                is_validate_complete_list = []
                list_count = []
                tag_count = []

                for i in range(len(modified_data_xls.index)):
                    if all_addresses_list[i] in copy_existing_prospects:
                        is_validate_complete_list.append(True)
                    else:
                        is_validate_complete_list.append(False)
                    skipped_list.append(False)
                    opt_out_list.append(files.opt_out)
                    print(files.skip_traced)
                    skip_traced_list.append(files.skip_traced)
                    list_count.append(1)
                    if files.tag_id:
                        tag_count.append(1)
                    else:
                        tag_count.append(0)

                modified_data_xls['opt_out'] = opt_out_list
                modified_data_xls['skip_traced'] = skip_traced_list
                modified_data_xls['is_validate_complete'] = is_validate_complete_list
                modified_data_xls['skipped'] = skipped_list
                modified_data_xls['list_count'] = list_count
                modified_data_xls['tag_count'] = tag_count
                modified_data_xls['added_to_els'] = skipped_list

                modified_data_xls.to_csv(file_path, encoding='utf-8', index=False)
                print(modified_data_xls)
                insert_count = Prospect_Properties.objects.from_csv(file_path, data)
                files.imported = insert_count
                files.is_process_complete = True
                files.save()

                counter = AddressValidationCounter.objects.get(id=1)
                last_upload_id = counter.last_uploaded_address  # db last record before upload
                last_upload_id_2 = counter.last_uploaded_address + insert_count  # db last record id after upload
                counter.last_uploaded_address = last_upload_id_2
                counter.save()

                files.update_started = True
                files.save()
                prospects = Prospect_Properties.objects.filter(
                    Q(pk__lte=last_upload_id_2) & Q(pk__gt=last_upload_id) & Q(file__pk=None)).order_by('-id')
                for prospect in prospects:
                    try:
                        prospect.file.add(files.pk)
                        prospect.list.add(files.list.pk)
                        if files.tag_id:
                            prospect.tag.add(files.tag_id)
                        if prospect.propertyaddress in copy_existing_prospects:
                            pros = Prospect_Properties.objects.filter(
                                (Q(file__user=user) | Q(file__user__in=users)) & Q(
                                    propertyaddress=prospect.propertyaddress) & Q(file__pk__lte=files.pk)).order_by(
                                '-id')
                            update_id = list(pros.values_list('pk', flat=True)[:1])
                            delete_ids = list(pros.values_list('pk', flat=True)[1:])
                            files.updated = files.updated + 1
                            files.imported = files.imported - 1
                            lists_list = []
                            tags_list = []
                            files_list = []
                            api_check = False
                            vacant = True
                            api_response = "Address Is Not Valid Address"
                            skipped = True
                            for p in pros:
                                lists_list.extend(p.list.all())
                                tags_list.extend(p.tag.all())
                                files_list.extend(p.file.all())
                                if p.id != update_id[0] and p.is_validate_complete:
                                    api_check = True
                                    vacant = p.vacant
                                    api_response = p.api_response
                                    skipped = p.skipped
                            updated_prospect = Prospect_Properties.objects.get(pk=update_id[0])
                            updated_prospect.list.add(*lists_list)
                            updated_prospect.tag.add(*tags_list)
                            updated_prospect.file.add(*files_list)
                            updated_prospect.list_count = updated_prospect.list.count()
                            updated_prospect.tag_count = updated_prospect.tag.count()
                            if api_check:
                                updated_prospect.vacant = vacant
                                updated_prospect.api_response = api_response
                                updated_prospect.skipped = skipped
                            else:
                                updated_prospect.is_validate_complete = False
                                if counter.last_valid_address > update_id[0]:
                                    counter.last_valid_address = update_id[0]
                                    counter.save()
                            updated_prospect.save()
                            Prospect_Properties.objects.filter(pk__in=delete_ids).delete()
                            files.save()
                    except:
                        files.update_try = files.update_try + 1
                        print(traceback.print_exc())
                print("File, List, Tag Added to Prospects")

                files.update_check = True
                if files.update_try > 0:
                    files.fail_reason = str(files.update_try) + " Prospects failed to update"
                files.save()
            except:
                print(traceback.print_exc())
                files.is_process_complete = True
                files.fail_reason = "Import Process Failed"
                files.update_check = True
                files.els_status = "es done"
                files.save()
        temp['insert_count'] = insert_count
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="validate_from_smarty_streets",
    ignore_result=True
)
def validate_from_smarty_streets():
    print("Smarty Street Validation Started")
    last_address_id = AddressValidationCounter.objects.get(id=1).last_valid_address
    try:
        print(last_address_id)
        prospect_obj = Prospect_Properties.objects.filter(is_validate_complete=False,
                                                          id__gte=last_address_id).order_by(
            "id")[:5000]
        prospect_ids_addresses = list(
            prospect_obj.values('pk', 'propertyaddress', 'mailingaddress', 'mailingcity', 'mailingstate',
                                'mailingzip'))
        prospect_ids = list(prospect_obj.values_list('pk', flat=True))
        if prospect_obj:
            last_id = prospect_obj.values_list('pk', flat=True)
            size = len(last_id)
            print(last_id[size - 1])
            AddressValidationCounter.objects.update(last_valid_address=last_id[size - 1])
        prospect_obj_dict_property = prospect_obj.annotate(street=F('propertyaddress'), city=F('propertycity'),
                                                           state=F('propertystate'),
                                                           candidates=Value(10,
                                                                            output_field=IntegerField())).values(
            'street',
            'city', 'state',
            'candidates')
        prospect_obj_property_100_list = list(prospect_obj_dict_property)
        prospect_obj_dict_mailing = prospect_obj.annotate(street=F('mailingaddress'), city=F('propertycity'),
                                                          state=F('propertystate'),
                                                          candidates=Value(10, output_field=IntegerField())).values(
            'street',
            'city', 'state',
            'candidates')
        prospect_obj_mailing_100_list = list(prospect_obj_dict_mailing)

        index = ceil(len(prospect_obj_property_100_list) / 100)

        for i in range(0, index):
            records_100_property = prospect_obj_property_100_list[i * 100:i * 100 + 100]
            all_100 = list(prospect_ids[i * 100:i * 100 + 100])
            # url = URL + '?auth-id=' + auth_id + '&auth-token=' + auth_token
            # res = requests.post(url, json=records_100_property, headers=smarty_street_headers)
            json_response = {}

            if json.dumps(json_response) == "[]":
                Prospect_Properties.objects.filter(pk__in=all_100).update(is_validate_complete=True, skipped=True,
                                                                          api_response="Address Is Not Valid Address",
                                                                          vacant=False)
            else:
                valid_prospect_list = [d['input_index'] for d in json_response]
                j = 0
                valid_prospects = []
                for prospect in valid_prospect_list:
                    dpv_vacant = True if (json_response[j]['analysis']['dpv_vacant'] == 'Y') else False
                    prospect_index = next(
                        (index for (index, d) in enumerate(prospect_ids_addresses) if
                         d["propertyaddress"] == records_100_property[prospect]['street']),
                        None)

                    valid_prospects.append(prospect_ids_addresses[prospect_index]['pk'])
                    Prospect_Properties.objects.filter(pk=prospect_ids_addresses[prospect_index]['pk']).update(
                        is_validate_complete=True, skipped=False,
                        api_response="-",
                        vacant=dpv_vacant)
                    j += 1

                Prospect_Properties.objects.filter(pk__in=all_100).exclude(pk__in=valid_prospects).update(
                    is_validate_complete=True,
                    skipped=True,
                    api_response="Address Is Not Valid Address",
                    vacant=False)

            records_100_mailing = prospect_obj_mailing_100_list[i * 100:i * 100 + 100]
            all_100_mailing = list(prospect_ids[i * 100:i * 100 + 100])
            prospect_empty_mailing_index = [index for (index, d) in enumerate(prospect_ids_addresses) if
                                            d["mailingaddress"] is None or d["mailingcity"] is None or
                                            d['mailingstate'] is None or d['mailingzip'] is None]
            records_100_mailing_removed_empty = [i for j, i in enumerate(records_100_mailing) if
                                                 j not in prospect_empty_mailing_index]
            if len(records_100_mailing_removed_empty) > 0:
                empty_mailing_ids = []
                for ind in prospect_empty_mailing_index:
                    empty_mailing_ids.append(prospect_ids_addresses[ind]['pk'])
                res = requests.post(url, json=records_100_mailing_removed_empty, headers=smarty_street_headers)
                json_response = res.json()

                if json.dumps(json_response) == "[]":
                    Prospect_Properties.objects.filter(pk__in=all_100_mailing).update(
                        mailingaddress=F('propertyaddress'),
                        mailingcity=F('propertycity'),
                        mailingstate=F('propertystate'),
                        mailingzip=F('propertyzip'))
                else:
                    valid_prospect_list_indices = [d['input_index'] for d in json_response]
                    valid_prospect_list = [records_100_mailing_removed_empty[i]['street'] for i in
                                           valid_prospect_list_indices]
                    prospect_valid_index = [index for (index, d) in enumerate(prospect_ids_addresses) if
                                            d["mailingaddress"] in valid_prospect_list]
                    valid_mailing_ids = []
                    for ind in prospect_valid_index:
                        valid_mailing_ids.append(prospect_ids_addresses[ind]['pk'])
                    Prospect_Properties.objects.filter(pk__in=all_100_mailing).exclude(
                        pk__in=valid_mailing_ids).update(
                        mailingaddress=F('propertyaddress'),
                        mailingcity=F('propertycity'),
                        mailingstate=F('propertystate'),
                        mailingzip=F('propertyzip'))
            else:
                Prospect_Properties.objects.filter(pk__in=all_100_mailing).update(
                    mailingaddress=F('propertyaddress'),
                    mailingcity=F('propertycity'),
                    mailingstate=F('propertystate'),
                    mailingzip=F('propertyzip'))
    except:
        print(traceback.print_exc())
        AddressValidationCounter.objects.update(last_valid_address=last_address_id)
    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="file_status_update",
    ignore_result=True
)
def file_status_update():
    print("In file Status Update")
    files = File.objects.filter(is_process_complete=True, update_check=True, validation_complete=False)
    for file in files:
        if Prospect_Properties.objects.filter(file__pk=file.pk,
                                              is_validate_complete=False).count() == 0:
            print("File Validation Completed")
            file.els_status = "completed"
            file.skipped = Prospect_Properties.objects.filter(file__pk=file.pk, skipped=True).count()
            file.validation_complete = True
            file.save()

    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="send_reminders",
    ignore_result=True
)
def send_reminders():
    t = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
    time = datetime.datetime.strptime(t, '%m/%d/%Y %I:%M %p')

    task = Reminder.objects.filter(sent=False).values('id', 'task__start_date_time', 'time_count',
                                                      'time_type__time_name', 'task__created_by__first_name',
                                                      'task__created_by__last_name', 'task__created_by__email',
                                                      'task__title')
    for tsk in task:
        if tsk['time_type__time_name'] == "days":
            sending_time = tsk['task__start_date_time'] + timedelta(days=tsk['time_count'])
        elif tsk['time_type__time_name'] == "minutes":
            sending_time = tsk['task__start_date_time'] + timedelta(minutes=tsk['time_count'])
        elif tsk['time_type__time_name'] == "hours":
            sending_time = tsk['task__start_date_time'] + timedelta(hours=tsk['time_count'])
        sending_time = sending_time.strftime('%m/%d/%Y %I:%M %p')
        sending_time = datetime.datetime.strptime(sending_time, '%m/%d/%Y %I:%M %p')
        if sending_time <= time:
            content = "This is to remind you that your task <b>" + tsk['task__title'] + "</b> is due soon."
            ctx = {
                'content': content,
                'first_name': tsk['task__created_by__first_name'],
                'last_name': tsk['task__created_by__last_name'],
                'domain': "18.223.227.40",
            }
            to_email_list = [tsk['task__created_by__email']]
            subject = "Prospectx :: Task Reminder"
            html_message = render_to_string(
                '../templates/partials/Reminder_Email.html', ctx)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                      fail_silently=False)
            Reminder.objects.filter(id=tsk['id']).update(sent=True)
    temp = {}
    return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(hour="*/24")),
    name="pull_list_everyday",
    ignore_result=True
)
def pull_list_everyday():  # to pull the lists
    # ListSequence.objects.filter(pulled_status='Not Pulled',
    #                             pull_date=datetime.now().date()).update(pulled_status='Pulled')
    list_sequence = ListSequence.objects.filter(pulled_status='Not Pulled', pull_date=datetime.datetime.now().date())
    email_from = settings.EMAIL_HOST_USER
    for seq in list_sequence:
        user = seq.list.user
        seq.pulled_status = 'Pulled'
        seq.save()
        send_event('prospectx' + str(user.id), 'message',
                   "A List " + seq.list.list_name + " you created has been Pulled!")
        Notification.objects.create(user=user, title="A List " + seq.list.list_name + " you created has been Pulled!")
        Notification_Pill.objects.filter(user=user).update(notification_pill=F('notification_pill') + 1)
        # if Notification_Pill.objects.filter(user=user, email_notification=True):
        #     email_to = user.]email
        #     message_body = "A List " + seq.list.list_name + " you created has been Pulled!"
        #     send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
        #     send_email.content_subtype = 'html'
        #     send_email.send()

    temp = {}
    return JsonResponse(temp)


# @periodic_task(
#     run_every=(crontab(hour="*/24")),
#     name="vacant_check_from_smarty_streets",
#     ignore_result=True
# )
# def vacant_check_from_smarty_streets():
#     prospect_obj = Prospect_Properties.objects.filter(is_validate_complete=True, propertyaddress__isnull=False,
#                                                       propertycity__isnull=False).order_by("-id")
#     URL = 'https://us-street.api.smartystreets.com/street-address'
#     for prospect in prospect_obj:
#         auth_id = 'd51dda1c-77b4-d022-bd6a-74464e9a9c4f'
#         auth_token = 'nl79JhmzvS1AykC866jI'
#         street = prospect.propertyaddress
#         city_id = prospect.propertycity
#         state = prospect.propertystate
#         candidates = 10
#         url = URL + '?auth-id=' + auth_id + '&auth-token=' + auth_token + '&street=' + street + '&city=' + city_id + '&state=' + state + '&candidates=' + str(
#             candidates)
#         res = requests.get(url)
#         json_response = res.json()
#         current_vacant_status = prospect.vacant
#
#         dpv_vacant = False
#         if len(json_response) > 0:
#             if 'dpv_vacant' in json_response[0]['analysis']:
#                 dpv_vacant = True if (json_response[0]['analysis']['dpv_vacant'] == 'Y') else False
#                 if current_vacant_status is False and dpv_vacant is True:
#                     lists = prospect.list.all()
#                     if len(lists) > 0:
#                         user = lists[0].user
#                         send_event('ProspectX' + str(user), 'message',
#                                    'New Vacant for Address ' + street + ', ' + city_id + ', ' + state)
#                         Notification_Pill.objects.filter(user=user).update(
#                             notification_pill=F('notification_pill') + 1)
#                         # if old_user != user:
#                         Notification.objects.create(user=user,
#                                                     title='New Vacant for Address ' + street + ', ' + city_id + ', ' + state)
#                         # old_user = user
#
#         Prospect_Properties.objects.filter(pk=prospect.id).update(vacant=dpv_vacant)
#
#     logger.info("ProspectX")
#     logger.debug("ProspectX Processing has been completed.")
#
#     temp = {}
#     return JsonResponse(temp)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="get_dashboard_stats",
    ignore_result=True
)
def get_dashboard_stats():
    super_user = UserProfile.objects.get(role__role_name="Super User").user
    other_users = UserProfile.objects.filter(Q(role__role_name="Admin User") | Q(role__role_name="Sub User")).order_by(
        '-id')
    if UserStats.objects.filter(user=super_user).exists():
        super_user_stats = UserStats.objects.get(user=super_user)
        prospect_obj = Prospect_Properties.objects.all()
        super_user_stats.prospect_count = len(prospect_obj)
        super_user_stats.opted_out_count = len(prospect_obj.filter(opt_out="yes"))
        super_user_stats.vacant_count = len(prospect_obj.filter(vacant=True))
        super_user_stats.absentee_count = len(prospect_obj.filter(absentee=True))
        super_user_stats.total_users_count = len(UserProfile.objects.filter(role__role_name='Admin User'))
        super_user_stats.save()

    for user in other_users:
        if UserStats.objects.filter(user=user.user).exists():
            other_user_stats = UserStats.objects.get(user=user.user)
            prospect_obj = Prospect_Properties.objects.filter(list__user=user.user)
            other_user_stats.prospect_count = len(prospect_obj)
            other_user_stats.opted_out_count = len(prospect_obj.filter(opt_out="yes"))
            other_user_stats.vacant_count = len(prospect_obj.filter(vacant=True))
            other_user_stats.absentee_count = len(prospect_obj.filter(absentee=True))
            other_user_stats.save()

    logger.info("ProspectX")
    logger.debug("ProspectX Dashboard Query.")

    temp = {}
    return JsonResponse(temp)


# =============== ES celery tasks =================#

es = Elasticsearch()


def start_indexing(data, via):
    print("indexing is started via", via)
    try:
        actions = [
            {"_index": "prospect_properties",
             "_type": "doc",
             "_id": obj.id,
             "_source": {
                 "id": obj.id,
                 "fullname": obj.fullname,
                 "firstname": obj.firstname,
                 "lastname": obj.lastname,
                 "propertyaddress": obj.propertyaddress,
                 "propertyaddress2": obj.propertyaddress2,
                 "propertycity": obj.propertycity,
                 "propertystate": obj.propertystate,
                 "propertyzip": obj.propertyzip,
                 "mailingaddress": obj.mailingaddress,
                 "mailingaddress2": obj.mailingaddress2,
                 "mailingcity": obj.mailingcity,
                 "mailingstate": obj.mailingstate,
                 "mailingzip": obj.mailingzip,
                 "email": obj.email,
                 "email2": obj.email2,
                 "phoneother": obj.phoneother,
                 "phonecell": obj.phonecell,
                 "phonelandline": obj.phonelandline,
                 "phone1": obj.phone1,
                 "phone2": obj.phone2,
                 "phone3": obj.phone3,
                 "phone4": obj.phone4,
                 "phone5": obj.phone5,
                 "phone6": obj.phone6,
                 "phone7": obj.phone7,
                 "phone8": obj.phone8,
                 "phone9": obj.phone9,
                 "phone10": obj.phone10,
                 "absentee": obj.absentee,
                 "vacant": obj.vacant,
                 "skipped": obj.skipped,
                 "is_validate_complete": obj.is_validate_complete,
                 "opt_out": obj.opt_out,
                 "custome1": obj.custome1,
                 "custome2": obj.custome2,
                 "custome3": obj.custome3,
                 "custome4": obj.custome4,
                 "custome5": obj.custome5,
                 "custome6": obj.custome6,
                 "custome7": obj.custome7,
                 "custome8": obj.custome8,
                 "custome9": obj.custome9,
                 "custome10": obj.custome10,
                 "notes": obj.notes,
                 "list": list_indexing(obj),
                 "tag": tag_indexing(obj)
             }
             }
            for obj in data
        ]
        bulk(es, actions, chunk_size=10000, request_timeout=300000)
        print("indexing complete")
        return True

    except Exception as e:
        print(e)
        return False


def list_indexing(pros):
    all_lists = pros.list.all()
    list_array = []
    for list in all_lists:
        cus_dict = {
            'list_name': list.list_name,
            'id': list.id,
            'user': {
                'id': list.user.id,
                'email': list.user.email
            }
        }
        list_array.append(cus_dict)

    return list_array


def tag_indexing(pros):
    all_tags = pros.tag.all()
    tag_array = []
    for tag in all_tags:
        cus_dict = {
            'tag_name': tag.tag_name,
            'id': tag.id,
            'user': {
                'id': tag.user.id,
                'email': tag.user.email
            }
        }
        tag_array.append(cus_dict)

    return tag_array


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="bulk_indexing",
    ignore_result=True
)
def prospects_bulk_indexing():
    file_obj = File.objects.filter(els_status='completed').order_by('id').first()
    print("in bulk indexing")

    if file_obj:
        print(file_obj.file_name)
        prospects_to_index = Prospect_Properties.objects.filter(file__pk=file_obj.pk)
        print("in bulk indexing count is {}".format(prospects_to_index.count()))
        if prospects_to_index:
            file_obj.els_status = 'added to es'
            file_obj.save()
            start = prospects_to_index.first().id
            end = prospects_to_index.last().id
            batch_size = 50000

            try:
                for i in range(start, end + 1, + batch_size):
                    pros_data = Prospect_Properties.objects.filter(pk__gte=i, pk__lt=i + batch_size).order_by('id')
                    if start_indexing(pros_data, "bulk method"):
                        Prospect_Properties.objects.filter(pk__gte=i, pk__lt=i + batch_size).update(added_to_els=True)

            except Exception as e:
                print(e)
                file_obj.fail_reason = 'es fail'
                file_obj.save()

            file_obj.els_status = 'es done'
            file_obj.save()
            print("bulk indexing complete ")
            print("file added to ES")
            return JsonResponse({})
