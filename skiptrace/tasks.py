from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from .models import *
from .views import *
import datetime
import decimal

logger = get_task_logger(__name__)
from filter_prospects.models import *
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
import traceback
import time
import base64


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="skip_trace_create_records",
    ignore_result=True
)
def skip_trace_create_records():
    skip_traces = SkipTraceFile.objects.filter(records_created=False).order_by("id")[:1]
    if skip_traces:
        skip_traces[0].records_created = True
        skip_traces[0].save()
        if ".csv" in skip_traces[0].file_name:
            try:
                x = skip_traces[0].destination_fields.split(",")
                path = os.path.join(BASE_DIR, 'media') + "/skiptrace_files"
                file_path = path + '/' + skip_traces[0].file_name
                try:
                    df = pd.read_csv(file_path)
                except:
                    print("exception in csv pd")
                    print(traceback.format_exc())
                ar = []
                for i in pd.read_csv(file_path):
                    ar.append(i)
                print(ar)
                total_records = len(df.index)
                skip_traces[0].total_records = total_records
                skip_id = skip_traces[0].id
                skip_traces[0].save()
                seconds_in_day = 24 * 60 * 60
                for i in df.index:
                    property_obj = DestinationFields()
                    property_obj.file_id = skip_id
                    for index in range(len(ar)):
                        if x[index] == "not_import":
                            pass
                        if x[index] == "firstname":
                            property_obj.first_name = df[ar[index]][i]
                            print("============", df[ar[index]][i], "==============", i)
                        if x[index] == "lastname":
                            property_obj.last_name = df[ar[index]][i]
                            print("============", df[ar[index]][i], "==============", i)
                        if x[index] == "propertyaddress":
                            property_obj.property_address = df[ar[index]][i]
                            print("============", df[ar[index]][i], "==============", i)
                        if x[index] == "propertyaddress2":
                            property_obj.property_address2 = df[ar[index]][i]
                        if x[index] == "propertycity":
                            property_obj.property_city = df[ar[index]][i]
                        if x[index] == "propertystate":
                            property_obj.property_state = df[ar[index]][i]
                        if x[index] == "propertyzip":
                            property_obj.property_zip = df[ar[index]][i]
                        if x[index] == "mailingaddress":
                            property_obj.mailing_address = df[ar[index]][i]
                        if x[index] == "mailingaddress2":
                            property_obj.mailing_address2 = df[ar[index]][i]
                        if x[index] == "mailingcity":
                            property_obj.mailing_city = df[ar[index]][i]
                        if x[index] == "mailingstate":
                            property_obj.mailing_state = df[ar[index]][i]
                        if x[index] == "mailingzip":
                            property_obj.mailing_zip = df[ar[index]][i]
                    property_obj.save()
            except:
                print("we are in inner exception")
                print(traceback.print_exc())
        else:
            try:
                x = skip_traces[0].destination_fields.split(",")
                print(x)
                path = os.path.join(BASE_DIR, 'media') + "/skiptrace_files"
                file_path = path + '/' + skip_traces[0].file_name
                try:
                    df = pd.read_excel(file_path)
                except:
                    print("exception in excel pandas")
                    print(traceback.format_exc())
                ar = []
                for i in pd.read_excel(file_path):
                    if "Unnamed:" not in i:
                        ar.append(i)
                print(ar)
                total_records = len(df.index)
                skip_traces[0].total_records = total_records
                skip_id = skip_traces[0].id
                skip_traces[0].save()
                for i in df.index:
                    property_obj = DestinationFields()
                    property_obj.file_id = skip_id
                    # property_obj.save()
                    for index in range(len(ar)):
                        if x[index] == "not_import":
                            pass
                        if x[index] == "firstname":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.first_name = df[ar[index]][i]
                            print("============", df[ar[index]][i], "==============", i)
                        if x[index] == "lastname":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.last_name = df[ar[index]][i]
                            print("============", df[ar[index]][i], "==============", i)
                        if x[index] == "propertyaddress":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.property_address = df[ar[index]][i]
                            print("============", df[ar[index]][i], "==============", i)
                        if x[index] == "propertyaddress2":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.property_address2 = df[ar[index]][i]
                        if x[index] == "propertycity":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.property_city = df[ar[index]][i]
                        if x[index] == "propertystate":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.property_state = df[ar[index]][i]
                        if x[index] == "propertyzip":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.property_zip = df[ar[index]][i]
                        if x[index] == "mailingaddress":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.mailing_address = df[ar[index]][i]
                        if x[index] == "mailingaddress2":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.mailing_address2 = df[ar[index]][i]
                        if x[index] == "mailingcity":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.mailing_city = df[ar[index]][i]
                        if x[index] == "mailingstate":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.mailing_state = df[ar[index]][i]
                        if x[index] == "mailingzip":
                            if str(df[ar[index]][i]) != "nan":
                                property_obj.mailing_zip = df[ar[index]][i]
                    property_obj.save()
            except:
                print("we are in outer exception")
                print(traceback.print_exc())
                skip_traces[0].save()
        skip_traces[0].should_trace = True
        skip_traces[0].save()
    temp = {}
    return JsonResponse(temp)


def string_to_list(field, df):
    """splitting string and returning list of split string"""
    split_string = []
    new_cols = {}
    max_ = 0
    for i in df[field]:
        try:
            if len(i.split("!")) > max_:
                max_ = len(i.split("!"))

            split_string.append(i.split("!"))
        except:
            split_string.append([' '])

    for i in range(1, max_ + 1):
        new_cols[field + str(i)] = []
    for i in split_string:
        if type(i) == list:
            for i2 in range(max_):
                try:
                    new_cols[field + str(i2+1)].append(i[i2])
                except:
                    new_cols[field + str(i2+1)].append(' ')
        else:
            new_cols[field+str(1)].append(' ')
    return new_cols


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="skip_trace_in_background",
    ignore_result=True
)

def skip_trace_in_background():
    skip_traces = SkipTraceFile.objects.filter(records_created=True, is_process_complete=False, should_trace=True).order_by("id")[:1]
    count = 0
    if skip_traces:
        try:
            skip_traces[0].is_process_complete = True
            skip_traces[0].save()
            user = skip_traces[0].user
            first_time = datetime.datetime.now()
            url1 = "https://login-api.idicore.com/apiclient"       #  "https://login-api-test.idicore.com/apiclient"
            payload = "{\"glba\":\"otheruse\",\"dppa\":\"none\"}"
            url2 = "https://api.idicore.com/search"                # "https://api-test.idicore.com/search"
            # d = base64.b64encode(
            #     b'api-client@acesolutionstest:U9fXWXBjX!e8yqL8ixRDSg&gFbN8zbk!kU4L4XyGhfCzm6Umz&YLJX7LBaVT26jd')
            d = base64.b64encode(
                b'api-client@acesolutions:ELw%7UYUbfkb5V!naYXhksX2Tu3LYvA%dqvA5YkevtXU%4x59GLnvhnJ5kqiL4Bi')
            abc = "Basic " + str(d.decode("utf-8"))
            headers = {
                'authorization': abc,
                'content-type': "application/json"
            }
            response = requests.request("POST", url1, data=payload, headers=headers)
            my_token = response.text  # token created for 15 minutes
            print("creating first time token: ", response)
            print("first_time: ", first_time)
            destination_fields = DestinationFields.objects.filter(file=skip_traces[0])
            total_records = len(destination_fields)
            for dest_fields in destination_fields:
                last_time = datetime.datetime.now()
                time_dif = last_time - first_time
                dif_in_minutes = time_dif.total_seconds() / 60
                if dif_in_minutes > 12:
                    d = base64.b64encode(
                        b'api-client@acesolutions:ELw%7UYUbfkb5V!naYXhksX2Tu3LYvA%dqvA5YkevtXU%4x59GLnvhnJ5kqiL4Bi')
                    abc = "Basic " + str(d.decode("utf-8"))
                    headers = {
                        'authorization': abc,
                        'content-type': "application/json"
                    }
                    response = requests.request("POST", url1, data=payload, headers=headers)
                    my_token = response.text  # token created for 15 minutes
                    first_time = datetime.datetime.now()
                    print("first time was: ", first_time)
                    print("last time is: ", last_time)
                    print("creating token again: ", response)
                else:
                    pass
                headers2 = {
                    'authorization': my_token,
                    'content-type': "application/json",
                    # 'content-type': "application/x-www-form-urlencoded",
                    'accept': "application/json"  # json
                }
                input_dict = {"lastName": dest_fields.last_name, "firstName": dest_fields.first_name, "address": dest_fields.property_address,
                              "city": dest_fields.property_city, "state": dest_fields.property_state, "zip": dest_fields.property_zip, "referenceId": "ABC-xyz1",
                              "fields": ["name", "phone", "address", "email"]}

                text_data = ' '
                name = ''
                phone = ''
                email = ''
                address = ''
                try:
                    json_body = json.dumps(input_dict)
                    response = requests.request("POST", url2, data=json_body, headers=headers2)
                    if response.status_code == 200:
                        print("we are in status code 200")
                        response_got = response.json()
                        text_data = response_got['result']
                        if text_data:
                            if 'name' in text_data[0]:
                                for n in text_data[0]['name']:
                                    name += n['data'] + '!'
                                name = name[:-1]
                            if 'phone' in text_data[0]:
                                for p in text_data[0]['phone']:
                                    phone += p['type'] + ' : ' + p['number'] + '!'
                                phone = phone[:-1]
                            if 'email' in text_data[0]:
                                for e in text_data[0]['email']:
                                    email += e['data'] + '!'
                                email = email[:-1]
                            if 'address' in text_data[0]:
                                for a in text_data[0]['address']:
                                    address += 'From: ' + a['dateRange'].split('-')[0] + ' To ' + \
                                               a['dateRange'].split('-')[1] + ' :\n' + a['data'] + '!'
                                address = address[:-1]
                                if text_data[0]['address']:
                                    prepaid_balance = PrepaidBalance.objects.get(user=user)
                                    prepaid_balance.amount = prepaid_balance.amount - decimal.Decimal(0.15)
                                    prepaid_balance.save()
                                    count += 1
                                    skip_traces[0].total_hits = count
                                    skip_traces[0].hits_percentage = str(int((count * 100) / total_records))
                                    skip_traces[0].save()
                    dest_fields.full_name = name
                    dest_fields.email = email
                    dest_fields.phone = phone
                    dest_fields.address = address
                    dest_fields.api_response = text_data
                    dest_fields.is_validation_complete = True
                    dest_fields.save()
                    print("success in saving data in database")

                except:
                    print("we are in inner exception")
                    print("error in saving data in database")
                    print(traceback.format_exc())
            try:
                fields = skip_traces[0].destination_fields.split(",")
                fields.extend(['Full_Name', 'Emails', 'Phones', 'Addresses'])
                data = DestinationFields.objects.filter(file_id=skip_traces[0].id).order_by('-id')
                header = dict((el, '') for el in fields if el != "not_import")
                if 'firstname' in fields:
                    header['firstname'] = [i.first_name for i in data]
                if 'lastname' in fields:
                    header['lastname'] = [i.last_name for i in data]
                if 'propertyaddress' in fields:
                    header['propertyaddress'] = [i.property_address for i in data]
                if 'propertycity' in fields:
                    header['propertycity'] = [i.property_city for i in data]
                if 'propertystate' in fields:
                    header['propertystate'] = [i.property_state for i in data]
                if 'propertyzip' in fields:
                    header['propertyzip'] = [i.property_zip for i in data]
                if 'mailingaddress' in fields:
                    header['mailingaddress'] = [i.mailing_address for i in data]
                if 'mailingcity' in fields:
                    header['mailingcity'] = [i.mailing_city for i in data]
                if 'mailingstate' in fields:
                    header['mailingstate'] = [i.mailing_state for i in data]
                if 'mailingzip' in fields:
                    header['mailingzip'] = [i.mailing_zip for i in data]

                header['Full_Name'] = [i.full_name for i in data]

                header['Emails'] = [i.email for i in data]
                header['Phones'] = [i.phone for i in data]
                header['Addresses'] = [i.address for i in data]

                print("dictionary got is: ", header)
                base_path = os.path.join(BASE_DIR, 'media') + "/exported_skiptrace"
                file_path = base_path + '/' + skip_traces[0].file_name
                df = pd.DataFrame(header)

                ####
                df1 = string_to_list('Emails',df)
                df2 = string_to_list('Phones',df)
                df3 = string_to_list('Addresses',df)
                df1 = pd.DataFrame({key: pd.Series(value) for key, value in df1.items()})
                df2 = pd.DataFrame({key: pd.Series(value) for key, value in df2.items()})
                df3 = pd.DataFrame({key: pd.Series(value) for key, value in df3.items()})
                df = pd.concat([df, df1, df2, df3], axis=1)
                df = df.drop(['Emails', 'Phones', 'Addresses'], axis=1)


                ####


                ####

                print("data frame we got: ", df)
                writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

                df.to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()

                print("success in writing data in file")

                skip_traces[0].status = 'Uploaded'
                skip_traces[0].is_process_complete = True
                skip_traces[0].save()
            except:
                print("we are in outer exception")
                print("error in writing data in file")
                print(traceback.print_exc())
                skip_traces[0].is_process_complete = True
                skip_traces[0].status = 'Pending'
                skip_traces[0].fail_reason = "Import Process Failed"
                skip_traces[0].save()
        except:
            print("Error in records with csv file")
            print("error in writing data in file")
            print(traceback.print_exc())
            skip_traces[0].is_process_complete = True
            skip_traces[0].status = 'Pending'
            skip_traces[0].fail_reason = "Import Process Failed"
            skip_traces[0].save()
    temp = {}
    return JsonResponse(temp)
