from django.shortcuts import render, get_object_or_404
import datetime
import traceback
import os
import random
import requests
from django.db.models import Count
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from filter_prospects.es_delete import bulk_delete_index
from filter_prospects.filters import filter_query
from filter_prospects.forms import ProspectForm
from filter_prospects.models import *
from django.db.models import Q

# Create your views here.
import pandas as pd

from marketing_machine.models import MarketingSequence, MarketingPlan, MarketingCampaign
from user.decorators import user_has_list_management_Permission
from user.models import UserProfile, UserStats

from .serializer import *
from prospectx_new import settings
from prospectx_new.settings import BASE_DIR
import stripe
from payments.views import is_subscribed
import traceback

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@login_required
@user_has_list_management_Permission
def prospects(request):
    if CustomFieldsModel.objects.filter(user=request.user).exists():
        custom_fields = CustomFieldsModel.objects.get(user=request.user)
    else:
        custom_fields = CustomFieldsModel.objects.create(user=request.user)
    return render(request, 'filter_prospects/import-prospect.html', {"custom_fields": custom_fields})


@login_required
@user_has_list_management_Permission
def upload_file(request):
    print("enter in uplaod file", type(request.FILES.get('file')))
    print("usser id is ========", request.user)
    file = request.FILES.get("file")
    try:
        path = settings.MEDIA_ROOT + '/files'
        fs = FileSystemStorage(path, None, file_permissions_mode=0o644)
        id_ = str(random.sample(range(1000), 1)[0]) + "_" + str(random.sample(range(100), 1)[0])
        filename = id_ + "_" + file.name
        fs.save(filename, file)
        print(str(file.name))
        path = os.path.join(BASE_DIR, 'media') + "/files"
        file_path = path + '/' + filename
        ar = []
        sheets = []
        if ".csv" in file.name:
            df = pd.read_csv(file_path)
            sheets.append("WorkSheet")
            for data in df:
                ar.append(data)
        else:
            xl = pd.ExcelFile(file_path)
            sheet_name = xl.sheet_names
            for sheet in sheet_name:
                sheets.append(sheet)
            print("==================", xl.sheet_names)

            for i in pd.read_excel(file_path):
                if "Unnamed:" not in i:
                    ar.append(i)
        temp = {
            "sheet_name": sheets,
            "header": ar,
            "file_name": filename
        }
        return JsonResponse(temp)
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        # raise Exception('not save in save image in folder!')
        temp = {
            "sheet_name": False,
            "header": "",
            "file_name": ""
        }
        return JsonResponse(temp)


@login_required
@user_has_list_management_Permission
def get_all_list_and_tags_by_user_id(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role.role_name == "Admin User":
        user = request.user
    else:
        user = profile.created_by.user
    users = UserProfile.objects.filter(created_by__user=user).values('user')
    print("=================================================")
    print(users)

    list_objects = List.objects.filter(Q(user=user) | Q(user__in=users))
    tag_objects = Tag.objects.filter(Q(user=user) | Q(user__in=users))
    print(tag_objects)
    print(list_objects)
    list = []
    tag = []
    if list_objects.exists():
        for data in list_objects:
            temp = {
                "id": data.id,
                "list_name": data.list_name
            }
            list.append(temp)
    if tag_objects.exists():
        for data in tag_objects:
            temp = {
                "id": data.id,
                "tag_name": data.tag_name
            }
            tag.append(temp)

    temp = {
        "list": list,
        "tag": tag
    }
    return JsonResponse(temp)


@login_required
@user_has_list_management_Permission
def save_file_and_list_tags_by_user(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role.role_name == "Admin User":
        user = request.user
    else:
        user = profile.created_by.user
    users = UserProfile.objects.filter(created_by__user=user).values('user')

    print(request.user)
    print("enter in save file list and tags ")
    print(request.POST)
    # print(request.POST["file_name"])
    # print(request.POST["create_list_value"])
    # print(request.POST["select_list_value"])
    print("source fields are", request.POST["source_field"])
    # print("===========sheet name==========",request.POST["sheet_name"])
    # print("==========source filed========",request.POST["source_field"])
    select_list_value = request.POST["select_list_value"]
    create_list_value = request.POST["create_list_value"]

    # enter_tag_description = request.POST["enter_tag_description"]
    create_a_tag = request.POST["create_a_tag"]
    select_a_tag = request.POST["select_a_tag"]
    select_opt_out = request.POST["select_opt_out"]
    select_skip_traced = request.POST["select_skip_traced"]
    if select_list_value:
        print("enter in select list value")
        if select_a_tag == "true":
            select_tag_existing = request.POST["select_tag_existing"]

            list_obj = List.objects.filter(id=select_list_value)
            file_obj = File()
            file_obj.opt_out = select_opt_out
            file_obj.skip_traced = select_skip_traced
            file_obj.user = request.user
            if select_tag_existing == "select":
                pass
            else:
                tag_obj = Tag.objects.filter(id=int(select_tag_existing))
                file_obj.tag_id = tag_obj[0].id
            file_obj.list = list_obj[0]
            file_obj.file_name = request.POST["file_name"]
            path = os.path.join(BASE_DIR, 'media') + "/files"
            file_path = path + '/' + file_obj.file_name
            file_obj.file_size = os.path.getsize(file_path)
            file_obj.created_at = datetime.datetime.now().date()
            file_obj.sheet_name = request.POST["sheet_name"]
            file_obj.destination_fields = request.POST["source_field"]

            file_obj.save()

        if create_a_tag == "true":
            enter_tag_name = request.POST["enter_tag_name"]
            print(enter_tag_name + "-------")
            exists_tag = Tag.objects.filter(Q(tag_name=enter_tag_name) & (Q(user=user) | Q(user__in=users)))
            if exists_tag.exists():
                temp = {
                    "status": 202,
                    "message": "Tag already exists"
                }
                return JsonResponse(temp)
            else:

                if enter_tag_name != "":

                    if enter_tag_name.strip() == "":
                        temp = {
                            "status": 202,
                            "message": "Enter a valid tag name"
                        }
                        return JsonResponse(temp)
                if enter_tag_name:
                    tag_obj = Tag()
                    tag_obj.tag_name = enter_tag_name
                    tag_obj.user = request.user
                    tag_obj.tag_description = request.POST["enter_tag_description"]
                    tag_obj.created_at = datetime.datetime.now().date()
                    tag_obj.save()

                list_obj = List.objects.filter(id=select_list_value)
                file_obj = File()
                file_obj.opt_out = select_opt_out
                file_obj.skip_traced = select_skip_traced
                file_obj.user = request.user
                if enter_tag_name:
                    file_obj.tag_id = tag_obj.id
                file_obj.list = list_obj[0]
                file_obj.file_name = request.POST["file_name"]
                path = os.path.join(BASE_DIR, 'media') + "/files"
                file_path = path + '/' + file_obj.file_name
                file_obj.file_size = os.path.getsize(file_path)
                file_obj.sheet_name = request.POST["sheet_name"]
                file_obj.destination_fields = request.POST["source_field"]
                file_obj.created_at = datetime.datetime.now().date()
                file_obj.save()
        temp = {
            "status": 200,
            "message": "List Save sucessfully"
        }
        return JsonResponse(temp)
    else:
        print("enter in create list value")
        list_obj = List.objects.filter(Q(list_name__icontains=create_list_value) & (Q(user=user) | Q(user__in=users)))
        if list_obj.exists():
            temp = {
                "status": 201,
                "message": "List already exists"
            }
            return JsonResponse(temp)
        else:
            print("enter in create list else part")
            if select_a_tag == "true":
                select_tag_existing = request.POST["select_tag_existing"]

                list_obj = List()
                list_obj.user = request.user
                list_obj.list_name = create_list_value
                list_obj.created_at = datetime.datetime.now().date()
                list_obj.save()
                file_obj = File()
                file_obj.opt_out = select_opt_out
                file_obj.skip_traced = select_skip_traced
                file_obj.user = request.user
                if select_tag_existing == "select":
                    pass
                else:
                    tag_obj = Tag.objects.filter(id=int(select_tag_existing))
                    file_obj.tag_id = tag_obj[0].id
                file_obj.list = list_obj
                file_obj.file_name = request.POST["file_name"]
                path = os.path.join(BASE_DIR, 'media') + "/files"
                file_path = path + '/' + file_obj.file_name
                file_obj.file_size = os.path.getsize(file_path)
                file_obj.sheet_name = request.POST["sheet_name"]
                file_obj.destination_fields = request.POST["source_field"]
                file_obj.created_at = datetime.datetime.now().date()
                file_obj.save()

            if create_a_tag == "true":
                enter_tag_name = request.POST["enter_tag_name"]
                print(enter_tag_name + "-------")
                exists_tag = Tag.objects.filter(Q(tag_name=enter_tag_name)  & (Q(user=user) | Q(user__in=users)))
                if exists_tag.exists():
                    temp = {
                        "status": 202,
                        "message": "Tag already exists"
                    }
                    return JsonResponse(temp)
                else:
                    if enter_tag_name != "":
                        if enter_tag_name.strip() == "":
                            temp = {
                                "status": 202,
                                "message": "Enter a valid tag name"
                            }
                            return JsonResponse(temp)
                    list_obj = List()
                    list_obj.user = request.user
                    list_obj.list_name = create_list_value
                    list_obj.created_at = datetime.datetime.now().date()
                    list_obj.save()

                    if enter_tag_name:
                        tag_obj = Tag()
                        tag_obj.tag_name = enter_tag_name
                        tag_obj.user = request.user
                        tag_obj.tag_description = request.POST["enter_tag_description"]
                        tag_obj.created_at = datetime.datetime.now().date()
                        tag_obj.save()

                    file_obj = File()
                    file_obj.user = request.user
                    if enter_tag_name:
                        file_obj.tag_id = tag_obj.id
                    file_obj.list = list_obj
                    file_obj.file_name = request.POST["file_name"]
                    path = os.path.join(BASE_DIR, 'media') + "/files"
                    file_path = path + '/' + file_obj.file_name
                    file_obj.file_size = os.path.getsize(file_path)
                    file_obj.sheet_name = request.POST["sheet_name"]
                    file_obj.destination_fields = request.POST["source_field"]
                    file_obj.created_at = datetime.datetime.now().date()
                    file_obj.opt_out = select_opt_out
                    file_obj.skip_traced = select_skip_traced
                    file_obj.save()
            temp = {
                "status": 200,
                "message": "List Saved Successfully"
            }
            return JsonResponse(temp)


@login_required
@user_has_list_management_Permission
def add_new_list_without_file(request):
    user = request.user
    list_name = request.POST["list_name"]
    list_status = request.POST["list_status"]
    import_data = request.POST["import_data"]
    import_option = request.POST["import_option"]
    update_option = request.POST["update_option"]
    list_id = request.POST.get("list_id")
    import_data = True if import_data == 'Yes' else False

    if user.is_authenticated and list_id:
        List.objects.filter(id=list_id).update(list_name=list_name,
                                               list_status=list_status, import_data=import_data,
                                               import_option=import_option, update_option=update_option)

        temp = {
            "status": 200,
            "message": "List Updated Successfully"
        }
        return JsonResponse(temp)

    if user and list_name and list_status and import_option and update_option:
        try:
            list_obj = List.objects.filter(Q(list_name=list_name) & Q(user=user))
            if list_obj.exists():
                temp = {
                    "status": 202,
                }
                return JsonResponse(temp)
            else:
                List.objects.create(user=user, list_name=list_name,
                                    list_status=list_status,
                                    import_data=import_data, import_option=import_option,
                                    update_option=update_option)

                temp = {
                    "status": 200,
                    "message": "List Saved Successfully"
                }
                return JsonResponse(temp)
        except:
            print(traceback.print_exc())
            temp = {
                "status": 500,
            }
            return JsonResponse(temp)
    else:
        temp = {
            "status": 202,
        }
        return JsonResponse(temp)


@login_required
@user_has_list_management_Permission
def add_new_list(request):
    user = request.user
    file_name = request.POST["file_name"]
    sheet_name = request.POST["sheet_name"]
    list_name = request.POST["create_list_value"]
    list_status = request.POST["list_status"]
    import_data = request.POST["import_data"]
    import_option = request.POST["import_option"]
    update_option = request.POST["update_option"]
    source_fields = request.POST["source_field"]
    import_data = True if import_data == 'Yes' else False

    list_id = request.POST.get("list_id")

    if user.is_authenticated and list_id:
        try:
            fields_list = source_fields.split(",")
            fields = ''
            for f in fields_list:
                if fields == '':
                    fields += f
                else:
                    fields += ',' + f
            with transaction.atomic():
                List.objects.filter(id=list_id).update(list_name=list_name,
                                                       list_status=list_status, import_data=import_data,
                                                       import_option=import_option, update_option=update_option)
                File.objects.filter(user=request.user, list_id=list_id).delete()
                File.objects.create(user=request.user, list_id=list_id, file_name=file_name,
                                    sheet_name=sheet_name, destination_fields=fields)
                temp = {
                    "status": 200,
                    "message": "List Updated Successfully"
                }
                return JsonResponse(temp)
        except:
            print(traceback.format_exc())
            temp = {
                "status": 200,
                "message": "There is some error"
            }
            return JsonResponse(temp)
    if 'propertyaddress' in source_fields and 'propertycity' in source_fields:
        if 'propertystate' in source_fields or 'propertyzip' in source_fields:
            try:
                list_obj = List.objects.filter(Q(list_name__icontains=list_name) & Q(user=request.user))
                if list_obj.exists():
                    temp = {
                        "status": 202,
                    }
                    return JsonResponse(temp)
                else:
                    fields_list = source_fields.split(",")
                    fields = ''
                    print("enter in create list value")
                    for f in fields_list:
                        # if f != 'not_import':
                        if fields == '':
                            fields += f
                        else:
                            fields += ',' + f
                    with transaction.atomic():
                        created_list = List.objects.create(user=request.user, list_name=list_name,
                                                           list_status=list_status,
                                                           import_data=import_data, import_option=import_option,
                                                           update_option=update_option)
                        File.objects.create(user=request.user, list=created_list, file_name=file_name,
                                            sheet_name=sheet_name, destination_fields=fields)
                        print("successfully created file and list")
                        temp = {
                            "status": 200,
                            "message": "List Saved Successfully"
                        }
                        return JsonResponse(temp)
            except:
                print(traceback.print_exc())
                temp = {
                    "status": 500,
                }
                return JsonResponse(temp)
        else:
            temp = {
                "status": 201,
            }
            return JsonResponse(temp)
    else:
        temp = {
            "status": 201,
        }
        return JsonResponse(temp)


@login_required
@user_has_list_management_Permission
def show_all_upload_file_process_by_user(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    file_obj = File.objects.filter(user=request.user)
    print(file_obj)
    context = {'file_obj': file_obj, "context_key": context_key, "subscription": data}
    return render(request, 'filter_prospects/show-all-uploaded-files.html', context)


@login_required
@user_has_list_management_Permission
def get_col_by_sheet_name(request):
    print(request.POST["file_name"])

    path = os.path.join(BASE_DIR, 'media') + "/files"
    file_path = path + '/' + request.POST["file_name"]
    print(file_path)
    ar = []
    sheets = []
    if ".csv" in request.POST["file_name"]:
        df = pd.read_csv(file_path)
        for data in df:
            ar.append(data)
    else:
        for i in pd.read_excel(file_path, sheet_name=request.POST["sheet_name"]):
            if "Unnamed:" not in i:
                ar.append(i)
    temp = {

        "header": ar,
        "file_name": request.POST["file_name"]
    }
    return JsonResponse(temp)


# ------------------------------------- Prospect Management --------------------------------------------------

@login_required
@user_has_list_management_Permission
def AddProspect(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    try:
        if request.method == "GET":
            return render(request, 'filter_prospects/add-new-prospect.html',
                          {"context_key": context_key, "subscription": data})
        elif request.method == "POST":
            form = ProspectForm(request.POST)
            if form.is_valid():

                profile = UserProfile.objects.get(user=request.user)
                user = request.user
                if profile.role.role_name == "Admin User":
                    users = UserProfile.objects.filter(created_by__user=request.user).values('user')
                else:
                    users = UserProfile.objects.filter(created_by__user=profile.created_by.user).values('user')
                    user = profile.created_by.user

                if form.cleaned_data['opt_out']:
                    opt_out = "yes"
                else:
                    opt_out = "no"

                if form.cleaned_data['donotcall']:
                    dnc = "yes"
                else:
                    dnc = "no"
                if not Prospect_Properties.objects.filter((Q(file__user=user) | Q(file__user__in=users) | Q(
                        list__user=user) | Q(list__user__in=users)) & Q(
                    propertyaddress=form.cleaned_data['propertyaddress'])).exists():
                    prospect = form.save(commit=False)
                    prospect.is_validate_complete = False
                    prospect.opt_out = opt_out
                    prospect.donotcall = dnc
                    prospect.save()
                    get_id = prospect.id
                    prospect.list.add(request.POST.get('list_obj'))

                    if AddressValidationCounter.objects.filter(id=1).exists():
                        counter = AddressValidationCounter.objects.get(id=1)
                        counter.last_uploaded_address = counter.last_uploaded_address + 1
                        counter.save()
                    else:
                        AddressValidationCounter.objects.create(last_valid_address=0, last_uploaded_address=1)

                    if UserStats.objects.filter(user=request.user).exists():
                        other_user_stats = UserStats.objects.get(user=request.user)
                        other_user_stats.prospect_count += 1
                        other_user_stats.save()

                else:
                    Prospect_Properties.objects.filter((Q(file__user=user) | Q(file__user__in=users) | Q(
                        list__user=user) | Q(list__user__in=users)) & Q(
                        propertyaddress=form.cleaned_data['propertyaddress'])).update(
                        fullname=form.cleaned_data['fullname'],
                        firstname=form.cleaned_data['firstname'],
                        lastname=form.cleaned_data['lastname'],
                        propertyaddress2=form.cleaned_data['propertyaddress2'],
                        propertycity=form.cleaned_data['propertycity'],
                        propertystate=form.cleaned_data['propertystate'],
                        propertyzip=form.cleaned_data['propertyzip'],
                        mailingaddress=form.cleaned_data['mailingaddress'],
                        mailingaddress2=form.cleaned_data['mailingaddress2'],
                        mailingcity=form.cleaned_data['mailingcity'],
                        mailingstate=form.cleaned_data['mailingstate'],
                        mailingzip=form.cleaned_data['mailingzip'],
                        phoneother=form.cleaned_data['phoneother'],
                        phonecell=form.cleaned_data['phonecell'],
                        phonelandline=form.cleaned_data['phonelandline'],
                        phone1=form.cleaned_data['phone1'],
                        phone2=form.cleaned_data['phone2'],
                        phone3=form.cleaned_data['phone3'],
                        phone4=form.cleaned_data['phone4'],
                        phone5=form.cleaned_data['phone5'],
                        phone6=form.cleaned_data['phone6'],
                        phone7=form.cleaned_data['phone7'],
                        phone8=form.cleaned_data['phone8'],
                        phone9=form.cleaned_data['phone9'],
                        phone10=form.cleaned_data['phone10'],
                        email=form.cleaned_data['email'],
                        email2=form.cleaned_data['email2'],
                        notes=form.cleaned_data['notes'],
                        deceased=form.cleaned_data['deceased'],
                        yearbuilt=form.cleaned_data['yearbuilt'],
                        donotcall=dnc,
                        opt_out=opt_out,
                        status=form.cleaned_data['status'],
                        vacant=form.cleaned_data['vacant'],
                        custome1=form.cleaned_data['custome1'],
                        custome2=form.cleaned_data['custome2'],
                        custome3=form.cleaned_data['custome3'],
                        custome4=form.cleaned_data['custome4'],
                        custome5=form.cleaned_data['custome5'],
                        custome6=form.cleaned_data['custome6'],
                        custome7=form.cleaned_data['custome7'],
                        custome8=form.cleaned_data['custome8'],
                        custome9=form.cleaned_data['custome9'],
                        custome10=form.cleaned_data['custome10'],
                    )
                    prospect = Prospect_Properties.objects.get((Q(file__user=user) | Q(file__user__in=users) | Q(
                        list__user=user) | Q(list__user__in=users)) & Q(
                        propertyaddress=form.cleaned_data['propertyaddress']))
                    if not prospect.list.filter(pk=request.POST.get('list_obj')):
                        prospect.list.add(request.POST.get('list_obj'))
                list_count = prospect.list.all().count()
                tag_count = prospect.tag.all().count()
                prospect.list_count = list_count
                prospect.tag_count = tag_count
                prospect.updated_check = True
                prospect.save()
                get_obj_to_index = Prospect_Properties.objects.get(pk=prospect.id)
                myList, all_lists, all_tags, get_save_filters = filter_query(request)

                return render(request, "filter_prospects/filter-prospect2.html",
                              {"context_key": context_key, "subscription": data, "prospects": myList,
                               "lists": all_lists,
                               "tags": all_tags,
                               "save_filters": get_save_filters,
                               "message": "Prospect Added to the List Successfully", "error_type": "success"})
            else:
                total_phone_fields = request.POST.get('total_phone_fields')
                total_custom_fields = request.POST.get('total_custom_fields')
                return render(request, 'filter_prospects/add-new-prospect.html',
                              {"context_key": context_key, "subscription": data,
                               'form': form, "error_type": "warning", "total_phone_fields": total_phone_fields,
                               "total_custom_fields": total_custom_fields,
                               "list_obj": int(request.POST.get('list_obj'))})
    except:
        print(traceback.print_exc())
        return render(request, 'filter_prospects/add-new-prospect.html',
                      {"context_key": context_key, "subscription": data, "message": "There is some error",
                       "error_type": "error"})


@login_required
@user_has_list_management_Permission
def UpdateProspect(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    try:
        if request.method == "GET":
            prospect = get_object_or_404(Prospect_Properties, pk=id)
            return render(request, 'filter_prospects/update_prospect.html',
                          {"context_key": context_key, "subscription": data, "prospect": prospect})
        elif request.method == "POST":

            instance = get_object_or_404(Prospect_Properties, id=id)
            print(instance)
            form = ProspectForm(request.POST or None, instance=instance)
            if form.is_valid():
                if form.cleaned_data['opt_out']:
                    opt_out = "yes"
                else:
                    opt_out = "no"

                if form.cleaned_data['donotcall']:
                    dnc = "yes"
                else:
                    dnc = "no"
                prospect = form.save(commit=False)
                prospect.opt_out = opt_out
                prospect.donotcall = dnc
                prospect.updated_check=True
                prospect.save()
                myList, all_lists, all_tags, get_save_filters = filter_query(request)

                return render(request, "filter_prospects/filter-prospect2.html",
                              {"context_key": context_key, "subscription": data, "prospects": myList,
                               "lists": all_lists,
                               "tags": all_tags,
                               "save_filters": get_save_filters,
                               "message": "Prospect Updated Successfully", "error_type": "success"})
            else:
                prospect = get_object_or_404(Prospect_Properties, pk=id)
                print(prospect)
                return render(request, 'filter_prospects/update_prospect.html',
                              {"context_key": context_key, "subscription": data, 'form': form,
                               "prospect": prospect})
    except:
        prospect = get_object_or_404(Prospect_Properties, pk=id)
        print(prospect)
        print(traceback.print_exc())
        return render(request, 'filter_prospects/update_prospect.html',
                      {"context_key": context_key, "subscription": data, "message": "There is some error",
                       "prospect": prospect, "error_type": "error"})


@login_required
@user_has_list_management_Permission
def UpdateProspectAjax(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    try:
        if request.method == "GET":
            prospect = get_object_or_404(Prospect_Properties, pk=id)
            print(prospect)
            return render(request, 'filter_prospects/update_prospect.html',
                          {"context_key": context_key, "subscription": data, "prospect": prospect})
        elif request.method == "POST":
            instance = get_object_or_404(Prospect_Properties, id=id)
            print(instance)
            form = ProspectForm(request.POST or None, instance=instance)
            print(form)
            if form.is_valid():
                if form.cleaned_data['opt_out']:
                    opt_out = "yes"
                else:
                    opt_out = "no"

                if form.cleaned_data['donotcall']:
                    dnc = "yes"
                else:
                    dnc = "no"
                prospect = form.save(commit=False)
                prospect.opt_out = opt_out
                prospect.donotcall = dnc
                prospect.updated_check = True
                prospect.save()

                data = {"message": "Prospect Updated Successfully"}
                return JsonResponse(data)
            else:
                data = {'update_prospect_form': form.errors, "message": "Form Validation Failed"}
                return JsonResponse(data, status=400)
    except:
        print(traceback.print_exc())
        data = {"message": "There is some error"}
        return JsonResponse(data, status=400)


@login_required
@user_has_list_management_Permission
def DeleteProspect(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    try:
        if Prospect_Properties.objects.filter(pk=pk).exists():
            bulk_delete_index(Prospect_Properties.objects.filter(pk=pk), "delete index from view")
            Prospect_Properties.objects.filter(pk=pk).delete()
            myList, all_lists, all_tags, get_save_filters = filter_query(request)
            if UserStats.objects.filter(user=request.user).exists():
                other_user_stats = UserStats.objects.get(user=request.user)
                other_user_stats.prospect_count -= 1
                other_user_stats.save()
            return render(request, 'filter_prospects/filter-prospect2.html',
                          {"context_key": context_key, "subscription": data, "prospects": myList,
                           "lists": all_lists,
                           "tags": all_tags,
                           "save_filters": get_save_filters,
                           "message": "Prospect Deleted Successfully", "error_type": "success"})

        else:
            myList, all_lists, all_tags, get_save_filters = filter_query(request)
            return render(request, 'filter_prospects/filter-prospect2.html',
                          {"context_key": context_key, "subscription": data, "prospects": myList,
                           "lists": all_lists,
                           "tags": all_tags,
                           "save_filters": get_save_filters,
                           "message": "Prospect does not exist", "error_type": "info"})
    except:
        myList, all_lists, all_tags, get_save_filters = filter_query(request)
        return render(request, 'filter_prospects/filter-prospect2.html',
                      {"context_key": context_key, "subscription": data, "prospects": myList,
                       "lists": all_lists,
                       "tags": all_tags,
                       "save_filters": get_save_filters,
                       'message': "There is some error!", "error_type": "error"})


def ViewProspectDetails(request, id):
    data = dict()
    if Prospect_Properties.objects.filter(pk=id).exists():

        prospect = Prospect_Properties.objects.get(pk=id)
        serializer = ProspectSerializer(prospect)
        lists = prospect.list.all()
        serializer2 = ListSerializer(lists, many=True)
        tags = prospect.tag.all()
        serializer3 = TagSerializer(tags, many=True)
        list1 = lists.values_list('pk', flat=True)
        data2 = []

        for lst in list1:
            marketing_sequence = MarketingSequence.objects.filter(list__pk=lst).values_list('id', flat=True)

            Cold_Call_Pending = 0
            Cold_Call_Sent = 0
            Direct_Mail_Pending = 0
            Direct_Mail_Sent = 0
            Voice_Broadcast_Pending = 0
            Voice_Broadcast_Sent = 0
            RVM_Pending = 0
            RVM_Sent = 0
            SMS_Pending = 0
            SMS_Sent = 0
            Email_Pending = 0
            Email_Sent = 0

            Cold_Call_Plan = MarketingPlan.objects.filter(sequence__pk__in=marketing_sequence, plan='Cold Call')
            for plan in Cold_Call_Plan:
                Cold_Call_Pending = len(
                    MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Pending"))
                print(Cold_Call_Pending)
                Cold_Call_Sent = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Sent"))

            Direct_Mail_Plan = MarketingPlan.objects.filter(sequence__pk__in=marketing_sequence, plan='Direct Mail')
            for plan in Direct_Mail_Plan:
                Direct_Mail_Pending = len(
                    MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Pending"))
                Direct_Mail_Sent = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Sent"))

            Voice_Broadcast_Plan = MarketingPlan.objects.filter(sequence__pk__in=marketing_sequence,
                                                                plan='Voice Broadcast')
            for plan in Voice_Broadcast_Plan:
                Voice_Broadcast_Pending = len(
                    MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Pending"))
                Voice_Broadcast_Sent = len(
                    MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Sent"))

            RVM_Plan = MarketingPlan.objects.filter(sequence__pk__in=marketing_sequence, plan='RVM')
            for plan in RVM_Plan:
                RVM_Pending = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Pending"))
                RVM_Sent = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Sent"))

            SMS_Plan = MarketingPlan.objects.filter(sequence__pk__in=marketing_sequence, plan='SMS')
            for plan in SMS_Plan:
                SMS_Pending = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Pending"))
                SMS_Sent = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Sent"))

            Email_Plan = MarketingPlan.objects.filter(sequence__pk__in=marketing_sequence, plan='EMAIL')
            for plan in Email_Plan:
                Email_Pending = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Pending"))
                Email_Sent = len(MarketingCampaign.objects.filter(plan__pk=plan.pk, campaigning_status="Sent"))

            Count = {
                'list': lst,
                'Cold_Call_Pending': Cold_Call_Pending,
                'Cold_Call_Sent': Cold_Call_Sent,
                'Direct_Mail_Pending': Direct_Mail_Pending,
                'Direct_Mail_Sent': Direct_Mail_Sent,
                'Voice_Broadcast_Pending': Voice_Broadcast_Pending,
                'Voice_Broadcast_Sent': Voice_Broadcast_Sent,
                'RVM_Pending': RVM_Pending,
                'RVM_Sent': RVM_Sent,
                'SMS_Pending': SMS_Pending,
                'SMS_Sent': SMS_Sent,
                'Email_Pending': Email_Pending,
                'Email_Sent': Email_Sent
            }
            data2.append(Count)

        print(data2)
        data['prospect_obj'] = serializer.data
        data['lists'] = serializer2.data
        data['tags'] = serializer3.data
        data['list_count'] = data2
    return JsonResponse(data)


@login_required
@user_has_list_management_Permission
def DeleteProspectList(request, prospect_id, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    pro_obj= ''
    try:
        if Prospect_Properties.objects.filter(id=prospect_id, list__pk=id).exists():
            Prospect_Properties.objects.get(id=prospect_id).list.remove(id)
            prospect = Prospect_Properties.objects.get(id=prospect_id)
            list_count = prospect.list.all().count()
            prospect.list_count = list_count
            prospect.updated_check = True
            prospect.save()

            myList, all_lists, all_tags, get_save_filters = filter_query(request)
            return render(request, 'filter_prospects/filter-prospect2.html',
                          {"context_key": context_key, "subscription": data, "prospects": myList,
                           "lists": all_lists,
                           "tags": all_tags,
                           "save_filters": get_save_filters,
                           "message": "List Deleted Successfully", "error_type": "success"})
        else:
            myList, all_lists, all_tags, get_save_filters = filter_query(request)
            return render(request, 'filter_prospects/filter-prospect2.html',
                          {"context_key": context_key, "subscription": data, "prospects": myList,
                           "lists": all_lists,
                           "tags": all_tags,
                           "save_filters": get_save_filters,
                           "message": "List does not exist", "error_type": "info"})
    except:
        myList, all_lists, all_tags, get_save_filters = filter_query(request)
        return render(request, 'filter_prospects/filter-prospect2.html',
                      {"context_key": context_key, "subscription": data, "prospects": myList,
                       "lists": all_lists,
                       "tags": all_tags,
                       "save_filters": get_save_filters,
                       'message': "There is some error!", "error_type": "error"})


@login_required
@user_has_list_management_Permission
def DeleteProspectTag(request, prospect_id, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)

    try:
        if Prospect_Properties.objects.filter(id=prospect_id, tag__pk=id).exists():
            Prospect_Properties.objects.get(id=prospect_id).tag.remove(id)
            prospect = Prospect_Properties.objects.get(id=prospect_id)
            tag_count = prospect.tag.all().count()
            prospect.tag_count = tag_count
            prospect.updated_check = True
            prospect.save()

            myList, all_lists, all_tags, get_save_filters = filter_query(request)
            return render(request, 'filter_prospects/filter-prospect2.html',
                          {"context_key": context_key, "subscription": data, "prospects": myList,
                           "lists": all_lists,
                           "tags": all_tags,
                           "save_filters": get_save_filters,
                           "message": "Tag Deleted Successfully", "error_type": "success"})
        else:
            myList, all_lists, all_tags, get_save_filters = filter_query(request)
            return render(request, 'filter_prospects/filter-prospect2.html',
                          {"context_key": context_key, "subscription": data, "prospects": myList,
                           "lists": all_lists,
                           "tags": all_tags,
                           "save_filters": get_save_filters,
                           "message": "Tag does not exist", "error_type": "info"})
    except:
        myList, all_lists, all_tags, get_save_filters = filter_query(request)
        return render(request, 'filter_prospects/filter-prospect2.html',
                      {"context_key": context_key, "subscription": data, "prospects": myList,
                       "lists": all_lists,
                       "tags": all_tags,
                       "save_filters": get_save_filters,
                       'message': "There is some error!", "error_type": "error"})
