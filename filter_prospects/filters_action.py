from pprint import pprint
import xlwt
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
import stripe

from filter_prospects.es_delete import bulk_delete_index
from filter_prospects.exec_query import *
from filter_prospects.filters import extract_request_data_for_action_count
# from filter_prospects.tasks import start_indexing
from filter_prospects.tasks import start_indexing
from prospectx_new import settings
import json
from .models import Prospect_Properties, List, Tag, File, CustomFieldsModel

stripe.api_key = settings.STRIPE_SECRET_KEY


# @method_decorator(login_required, name='post')
class perform_actions(View):
    def post(self, request):
        visible_ids = request.POST.getlist("visible_ids")
        my_list_parse = json.loads(visible_ids[0])
        pprint(my_list_parse)
        action = request.POST.get("table_action")
        perform_by = request.POST.get("perform_by")
        ids_list = []
        if perform_by == 'select_all':
            data = extract_request_data_for_action_count(request)

            # my_list_parse = run_query(data, "ids")
            my_list_parse, total_records = run_els_query(data, "ids")
            #
            # for item in my_list_parse:
            #     ids_list.append(item[0])

            # my_list_parse = ids_list

        list_name = request.POST.get("list_name")
        list_act = request.POST.get("list_act")
        tag_name = request.POST.get("tag_name")
        tag_act = request.POST.get("tag_act")

        data = {
            'ids': my_list_parse,
            'action': action,
            'list_name': list_name,
            'tag_name': tag_name,
            'list_act': list_act,
            'tag_act': tag_act

        }

        context = self.actions(request, data)

        return JsonResponse(context)

    def actions(self, request, data):
        # out_list = [item for t in data['ids'] for item in t]
        get_prospects = Prospect_Properties.objects.filter(id__in=data["ids"])
        context = {}
        if data['action'] == "create_list":
            if data['list_act'] == 'new':
                list_obj = List.objects.create(list_name=data['list_name'], user=request.user)
            elif data['list_act'] == 'old':
                list_obj = List.objects.filter(pk=data['list_name']).first()

            for pro in get_prospects:
                # obj = Prospect_Properties.objects.filter(propertyaddress=pro.propertyaddress).first()
                pro.list.add(list_obj)
                pro.save()
                list_count = pro.list.all().count()
                pro.list_count = list_count
                pro.save()
                start_indexing(get_prospects, "in action list_create")
            context = {
                "list_id": list_obj.id
            }
        elif data['action'] == "create_tag":
            if data['tag_act'] == 'new':
                tag_obj = Tag.objects.create(tag_name=data['tag_name'], user=request.user)
            elif data['tag_act'] == 'old':
                tag_obj = Tag.objects.filter(pk=data['tag_name']).first()
            for pro in get_prospects:
                # obj = Prospect_Properties.objects.filter(propertyaddress=pro.propertyaddress).first()
                pro.tag.add(tag_obj)
                pro.save()
                tag_count = pro.tag.all().count()
                pro.tag_count = tag_count
                pro.save()
                start_indexing(get_prospects, "in action tag_create")
            context = {
                "tag_id": tag_obj.id
            }
        elif data['action'] == "opt_out":
            # _ids = data['ids']
            # for _id in _ids:
            #     get_obj = Prospect_Properties.objects.get(id=_id)
            #     get_obj.opt_out = "yes"
            #     get_obj.save()
            for pro in get_prospects:
                pro.opt_out = "yes"
                pro.save()

            start_indexing(get_prospects,"in action opt_out")
        elif data['action'] == "delete":
            # call save here too
            bulk_delete_index(get_prospects, "in action delete")
            Prospect_Properties.objects.filter(id__in=data['ids']).delete()

        elif data['action'] == "export_to_excel":
            prospect_data = Prospect_Properties.objects.filter(id__in=data['ids'])
            exportdata = []
            for pros in prospect_data:
                list_count = len(
                    Prospect_Properties.objects.filter(propertyaddress=pros.propertyaddress).distinct('list'))
                tag_count = len(
                    Prospect_Properties.objects.filter(propertyaddress=pros.propertyaddress).distinct('tag'))
                exportdata.append(
                    (pros.fullname, pros.mailingaddress, pros.propertyaddress,
                     list_count, tag_count))

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="prospect_data.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Prospect_properties')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            custom_fields = CustomFieldsModel.objects.get(user=request.user)

            columns = ['Mailing Full Name', 'Mailing Address',
                       'Property Address', 'List Count', 'Tag Count']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            # queryset = queryset.values_list('user_name', 'date', 'user_score', 'time_taken', )
            for row in exportdata:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            user_id = request.user.pk
            wb.save("media/filter_action_export_to_excel/" + "prospect_data.xls")

        return context
