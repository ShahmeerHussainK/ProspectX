from pprint import pprint
import psycopg2
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
import stripe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from filter_prospects.db_connection import get_local_connection
from filter_prospects.exec_query import run_els_query
from prospectx_new import settings
from user.decorators import user_has_list_management_Permission
from user.models import UserProfile
from .models import List, Tag, Save_Filter, CustomFieldsModel
from .models import Prospect_Properties
from django.core.paginator import Paginator

stripe.api_key = settings.STRIPE_SECRET_KEY


def filter_query(request):
    myList = []
    try:
        connection = get_local_connection()
        cursor = connection.cursor()
        # filter_prospects_prospect_properties

        query_all_prospectx = """SELECT DISTINCT ON (propertyaddress) propertyaddress,fullname, mailingaddress, p.id,absentee,vacant, opt_out,
                                    (SELECT COUNT(DISTINCT list_id) FROM filter_prospects_prospect_properties fp WHERE fp.propertyaddress = p.propertyaddress) AS list_count,
                                    (SELECT COUNT(DISTINCT tag_id) FROM filter_prospects_prospect_properties fp WHERE fp.propertyaddress = p.propertyaddress) AS tag_count,
                                    (SELECT array_to_string(array_agg(name), ',') FROM marketing_machine_marketingsequence s WHERE s.list_id = p.list_id) AS sequences
                                """

        cursor.execute(query_all_prospectx)
        all_prospectx = cursor.fetchall()
        pprint(all_prospectx)

        for pro in all_prospectx:
            mydict = {}
            mydict.update({"propertyaddress": pro[0]})
            mydict.update({"fullname": pro[1]})
            mydict.update({"mailingaddress": pro[2]})
            mydict.update({"id": pro[3]})
            mydict.update({"absentee": pro[4]})
            mydict.update({"list_count": pro[7]})
            mydict.update({"tag_count": pro[8]})
            mydict.update({"sequence": pro[9]})
            myList.append(mydict)

    except (Exception, psycopg2.Error) as error:
        print("error")
        print(error)
    all_lists = List.objects.filter(user=request.user)
    all_tags = Tag.objects.filter(user=request.user)
    get_save_filters = Save_Filter.objects.filter(user=request.user)
    return myList, all_lists, all_tags, get_save_filters


def get_comunity_ids(usr):
    user_comunity_people_ids = []

    usr_profile = UserProfile.objects.get(user=usr)
    if usr_profile.role.role_name == 'Admin User':
        sub_users_list = UserProfile.objects.filter(created_by=usr_profile)
        user_comunity_people_ids.append(usr.id)
    elif usr_profile.role.role_name == 'Sub User':
        get_admin = usr_profile.created_by  # sub user's admin
        sub_users_list = UserProfile.objects.filter(created_by=get_admin)
        user_comunity_people_ids.append(get_admin.user.id)
    for each_usr in sub_users_list:
        user_comunity_people_ids.append(each_usr.user.id)

    return user_comunity_people_ids


def get_comunity_lists_tags(usr):
    profile = UserProfile.objects.get(user=usr)
    if profile.role.role_name == "Admin User":
        user = usr
    else:
        user = profile.created_by.user
    users = UserProfile.objects.filter(created_by__user=user).values('user')
    all_list = List.objects.filter(Q(user=user) | Q(user__in=users))
    all_tag = Tag.objects.filter(Q(user=user) | Q(user__in=users))

    return all_list, all_tag


@login_required
@user_has_list_management_Permission
def filter_view(request):
    com_lists, com_tags = get_comunity_lists_tags(request.user)
    get_save_filters = Save_Filter.objects.filter(user=request.user)
    get_obj = CustomFieldsModel.objects.get(user=request.user)
    context = {
        "custom1": get_obj.custom1,
        "custom2": get_obj.custom2,
        "custom3": get_obj.custom3,
        "custom4": get_obj.custom4,
        "custom5": get_obj.custom5,
        "custom6": get_obj.custom6,
        "custom7": get_obj.custom7,
        "custom8": get_obj.custom8,
        "custom9": get_obj.custom9,
        "custom10": get_obj.custom10,
        "com_lists": com_lists,
        "com_tags": com_tags,
        "save_filters": get_save_filters,
    }

    return render(request, "filter_prospects/filter-prospect2.html", context)


def extract_request_data_for_action_count(req):
    search_query = req.POST.get('search_query')
    list_included = req.POST.getlist('list1')
    list_excluded = req.POST.getlist('list2')
    radio_list_in = req.POST.get('customRadio-list')
    tag_included = req.POST.getlist('tag1')
    tag_excluded = req.POST.getlist('tag2')
    radio_tag_in = req.POST.get('customRadio-tag')
    list_count = req.POST.get("list-count")
    list_count_total = req.POST.get("list-count-total")
    tag_count = req.POST.get("tag-count")
    tag_count_total = req.POST.get("tag-count-total")

    absentee = req.POST.get("absentee")
    vacant = req.POST.get("vacant")
    skipped = req.POST.get("skipped")
    opt_out = req.POST.get("opt-out")

    filters_condition = req.POST.get("options-filter-cond")
    select_key = req.POST.getlist('select-key')
    select_con = req.POST.getlist('select-con')
    select_val = req.POST.getlist('select-val')

    start = int(req.POST.get('start', 0))
    length = int(req.POST.get('length', 10))

    data = {
        'list_included': list_included,
        'list_excluded': list_excluded,
        'radio_list_in': radio_list_in,
        'tag_included': tag_included,
        'tag_excluded': tag_excluded,
        'radio_tag_in': radio_tag_in,
        'list_count': list_count,
        'tag_count': tag_count,
        'list_count_total': list_count_total,
        'tag_count_total': tag_count_total,
        'absentee': absentee,
        'vacant': vacant,
        'skipped': skipped,
        'opt_out': opt_out,
        'filters_condition': filters_condition,
        'select_key': select_key,
        'select_con': select_con,
        'select_val': select_val,
        'search_query': search_query,
        'user_id': get_comunity_ids(req.user),
        'start': start,
        'length': length

    }
    return data


def extract_request_data(req):
    search_query = req.POST.get('search_query')
    list_included = req.POST.get('list1')
    if list_included:
        list_included = list(list_included.split(","))
    list_excluded = req.POST.get('list2')
    if list_excluded:
        list_excluded = list(list_excluded.split(","))
    radio_list_in = req.POST.get('customRadio-list')

    tag_included = req.POST.get('tag1')
    if tag_included:
        tag_included = list(tag_included.split(","))
    tag_excluded = req.POST.get('tag2')
    if tag_excluded:
        tag_excluded = list(tag_excluded.split(","))

    radio_tag_in = req.POST.get('customRadio-tag')

    list_count = req.POST.get("list-count")
    list_count_total = req.POST.get("list-count-total")
    tag_count = req.POST.get("tag-count")
    tag_count_total = req.POST.get("tag-count-total")

    absentee = req.POST.get("absentee")
    vacant = req.POST.get("vacant")
    skipped = req.POST.get("skipped")
    opt_out = req.POST.get("opt-out")

    filters_condition = req.POST.get("options-filter-cond")
    select_key = req.POST.get('select-key')
    select_con = req.POST.get('select-con')
    select_val = req.POST.get('select-val')

    start = int(req.POST.get('start', 0))
    length = int(req.POST.get('length', 10))

    data = {
        'list_included': list_included,
        'list_excluded': list_excluded,
        'radio_list_in': radio_list_in,
        'tag_included': tag_included,
        'tag_excluded': tag_excluded,
        'radio_tag_in': radio_tag_in,
        'list_count': list_count,
        'tag_count': tag_count,
        'list_count_total': list_count_total,
        'tag_count_total': tag_count_total,
        'absentee': absentee,
        'vacant': vacant,
        'skipped': skipped,
        'opt_out': opt_out,
        'filters_condition': filters_condition,
        'select_key': list(select_key.split(",")),
        'select_con': list(select_con.split(",")),
        'select_val': list(select_val.split(",")),
        'search_query': search_query,
        # 'user_id': req.user.id,
        'user_id': get_comunity_ids(req.user),
        'start': start,
        'length': length

    }
    return data


class apply_filters(View):

    def post(self, request):
        action = request.POST.get("action")
        draw = int(request.POST.get('draw', 1))
        myList = []
        if action == "count":
            data = extract_request_data_for_action_count(request)

        else:
            data = extract_request_data(request)
        all_prospectx, records_total = run_els_query(data, action)
        records_filtered = records_total['value'] if isinstance(records_total, dict) else records_total
        records_total = records_total['value'] if isinstance(records_total, dict) else records_total

        # page = request.POST.get('page', draw)
        paginator = Paginator(all_prospectx, 10)
        page_number = data["start"] / data["length"] + 1
        try:
            prospects = paginator.page(page_number)
        except PageNotAnInteger:
            prospects = paginator.page(1)
        except EmptyPage:
            prospects = paginator.page(paginator.num_pages)

        context = {}
        if action == "count":
            context.update({
                "prospects_count": records_total

            })

        elif action == "all" or action == "search":
            context.update({
                'data': list(prospects),
                'recordsTotal': records_total,
                'recordsFiltered': records_filtered,
                'draw': draw,

            })

        return JsonResponse(context)


class save_filters(View):
    def post(self, request):
        context = ""
        action = request.POST.get('action')
        filter_name = request.POST.get('filter_name')

        search_query = request.POST.get('search_query')

        list_included = request.POST.getlist('list1')
        list_included_str = ','.join(list_included)

        list_excluded = request.POST.getlist('list2')
        list_excluded_str = ','.join(list_excluded)

        radio_list_in = request.POST['customRadio-list']

        tag_included = request.POST.getlist('tag1')
        tag_included_str = ','.join(tag_included)

        tag_excluded = request.POST.getlist('tag2')
        tag_excluded_str = ','.join(tag_excluded)
        radio_tag_in = request.POST['customRadio-tag']

        list_count = request.POST["list-count"]
        tag_count = request.POST["tag-count"]

        absentee = request.POST["absentee"]
        vacant = request.POST["vacant"]
        skipped = request.POST["skipped"]
        opt_out = request.POST["opt-out"]

        optional_field_filters_condition = request.POST["options-filter-cond"]
        select_key = request.POST.getlist('select-key')
        select_key = ','.join(select_key)
        select_con = request.POST.getlist('select-con')
        select_con = ','.join(select_con)
        select_val = request.POST.getlist('select-val')
        select_val = ','.join(select_val)

        key = select_key
        cond = select_con
        val = select_val

        # key = json.dumps(select_key)
        # cond = json.dumps(select_con)
        # val = json.dumps(select_val)

        if action == 'old_filter':

            Save_Filter.objects.filter(pk=int(filter_name)).update(user=request.user,
                                                                   search_query=search_query,
                                                                   lists_inc=list_included_str,
                                                                   list_inc_radio=radio_list_in,
                                                                   lists_exc=list_excluded_str,
                                                                   list_count_sel=list_count,
                                                                   tags_inc=tag_included_str,
                                                                   tag_inc_radio=radio_tag_in,
                                                                   tags_exc=tag_excluded_str,
                                                                   tag_count_sel=tag_count,
                                                                   absentee=absentee,
                                                                   vacant=vacant,
                                                                   skipped=skipped,
                                                                   opt_out=opt_out,
                                                                   optional_field_filters_select_key=key,
                                                                   optional_field_filters_select_con=cond,
                                                                   optional_field_filters_select_val=val,
                                                                   optional_field_filters_condition_and_or=optional_field_filters_condition)
            context = {
                "message": "Save Filter updated"
            }
        else:
            obj = Save_Filter.objects.create(user=request.user,
                                             search_query=search_query,
                                             filter_name=filter_name,
                                             list_inc_radio=radio_list_in,
                                             lists_inc=list_included_str,
                                             lists_exc=list_excluded_str,
                                             list_count_sel=list_count,
                                             tags_inc=tag_included_str,
                                             tag_inc_radio=radio_tag_in,
                                             tags_exc=tag_excluded_str,
                                             tag_count_sel=tag_count, absentee=absentee,
                                             vacant=vacant,
                                             skipped=skipped,
                                             opt_out=opt_out,
                                             optional_field_filters_select_key=key,
                                             optional_field_filters_select_con=cond,
                                             optional_field_filters_select_val=val,
                                             optional_field_filters_condition_and_or=optional_field_filters_condition)

            context = {
                "message": "Save Filter Created",
                "action": "new_filter",
                "new_filter_id": obj.id,
                "new_filter_name": obj.filter_name
            }
        return JsonResponse(context)


def make_saved_filter_data(request, obj):
    data = {
        'list_included': obj.lists_inc,  # its list_included_str
        'list_excluded': obj.lists_exc,
        'radio_list_in': obj.list_inc_radio,
        'tag_included': obj.tags_inc,
        'tag_excluded': obj.tags_exc,
        'radio_tag_in': obj.tag_inc_radio,
        'list_count': obj.list_count_sel,
        'tag_count': obj.tag_count_sel,
        'absentee': obj.absentee,
        'vacant': obj.vacant,
        'skipped': obj.skipped,
        'opt_out': obj.opt_out,
        'filters_condition': obj.optional_field_filters_condition_and_or,
        'select_key': obj.optional_field_filters_select_key,
        'select_con': obj.optional_field_filters_select_con,
        'select_val': obj.optional_field_filters_select_val,
        'search_query': obj.search_query,
        'user_id': get_comunity_ids(request.user),
        'start': int(request.GET.get('start', 0)),
        'length': int(request.GET.get('length', 10)),
        'list_count_total': List.objects.filter(user=request.user).count(),
        'tag_count_total': Tag.objects.filter(user=request.user).count()

    }
    return data


class existing_filters(View):
    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        filter_id = request.GET.get('filter_id')
        user = request.user
        obj = Save_Filter.objects.get(user=request.user, pk=filter_id)
        pprint(obj.lists_inc)
        pprint(type(obj.lists_inc))

        data = make_saved_filter_data(request, obj)
        myList = []
        action = "all"
        all_prospectx, records_total = run_els_query(data, action)
        records_filtered = records_total['value'] if isinstance(records_total, dict) else records_total
        records_total = records_total['value'] if isinstance(records_total, dict) else records_total
        paginator = Paginator(all_prospectx, 10)
        page_number = data["start"] / data["length"] + 1
        try:
            prospects = paginator.page(page_number)
        except PageNotAnInteger:
            prospects = paginator.page(1)
        except EmptyPage:
            prospects = paginator.page(paginator.num_pages)

        context = {
            'data': list(prospects),
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'draw': draw,
            'applied_saved_form': serializers.serialize('json', [obj]),
            'list_count_total': List.objects.filter(user=request.user).count(),
            'tag_count_total': Tag.objects.filter(user=request.user).count(),
        }
        return JsonResponse(context)


class get_sequences(View):
    def get(self, request):
        id = request.GET.get("id")
        market_seq = []
        get_pros = Prospect_Properties.objects.get(pk=id)
        lists = get_pros.list.all()
        for list in lists:
            all_marketing_seq_of_list = list.marketingsequence_set.all()
            for seq in all_marketing_seq_of_list:
                market_seq.append(seq.name)
        return JsonResponse(dict(sequences=market_seq))
