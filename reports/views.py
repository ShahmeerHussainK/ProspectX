import xlwt
from django.conf import settings
from django.core import serializers
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from filter_prospects.models import List, Prospect_Properties, File, CustomFieldsModel
from reports.models import ExportHistory
from user.decorators import user_has_report_history_Permission, user_has_skip_history_Permission
from user.models import UserProfile


@user_has_report_history_Permission
def report_history_page(request):
    return render(request, "reports/history.html")


@user_has_report_history_Permission
def report_history_data(request):
    data = dict()
    profile = UserProfile.objects.get(user=request.user)
    user = request.user
    if profile.role.role_name == "Admin User":
        users = UserProfile.objects.filter(created_by__user=request.user).values('user')
        files = File.objects.filter(Q(user=user) | Q(user__in=users)).values('list__created_at',
                                                                             'list__import_option',
                                                                             'list__list_name',
                                                                             'pk', 'fail_reason',
                                                                             'is_process_complete',
                                                                             'update_check',
                                                                             'imported',
                                                                             'skip_traced',
                                                                             'updated',
                                                                             'update_started',
                                                                             'els_status').order_by(
            '-id')
    else:
        users = UserProfile.objects.filter(created_by__user=profile.created_by.user).values('user')
        user = profile.created_by.user
        files = File.objects.filter(Q(user=user) | Q(user__in=users)).values('list__created_at',
                                                                             'list__import_option',
                                                                             'list__list_name',
                                                                             'pk', 'fail_reason',
                                                                             'is_process_complete',
                                                                             'update_check',
                                                                             'imported',
                                                                             'skip_traced',
                                                                             'updated',
                                                                             'update_started',
                                                                             'els_status').order_by(
            '-id')

    import_data = list(files)
    for dta in import_data:
        skipped = Prospect_Properties.objects.filter(file__pk=dta['pk'], skipped=True).count()
        file = File.objects.get(pk=dta['pk'])
        if dta['is_process_complete'] and dta['update_check'] and len(
                Prospect_Properties.objects.filter(file__pk=dta['pk'],
                                                   is_validate_complete=False)) == 0:
            processing_type = ""
            if not file.validation_complete:
                file.els_status = "completed"
                file.skipped = skipped
                file.validation_complete = True
                file.save()
            if dta['els_status'] == "es done":
                prosess_complete = True
            else:
                prosess_complete = False
                processing_type = "Adding to ELS"
        else:
            prosess_complete = False
            file.skipped = skipped
            file.save()
            if not dta['is_process_complete']:
                processing_type = "Uploading Prospects"
            elif dta['update_started'] and not dta['update_check']:
                processing_type = "Updating Prospects"
            else:
                processing_type = "Validating Prospects"
        dta.update({'overall_status': prosess_complete, "processing_type": processing_type, 'skipped': file.skipped})

    lists2 = ExportHistory.objects.filter(Q(user=user) | Q(user__in=users)).values('created_at', 'file_name',
                                                                                   'id').order_by('-id')
    export_data = list(lists2)

    data['import_history_data'] = import_data
    data['export_history_data'] = export_data
    return JsonResponse(data)


@user_has_skip_history_Permission
def export_to_excel(request, id):
    print(id)
    data = dict()
    exportdata = []
    prospect = Prospect_Properties.objects.filter(file__id=id)
    for pros in prospect:
        list_count = len(Prospect_Properties.objects.filter(propertyaddress=pros.propertyaddress).distinct('list'))
        print(pros.opt_out)
        if pros.opt_out:
            opt = "Yes"
        else:
            opt = "No"
        if pros.skip_traced:
            skip_trc = "Yes"
        else:
            skip_trc = "No"

        if pros.donotcall:
            dnc = "Yes"
        else:
            dnc = "No"

        if pros.vacant:
            vacant = "Yes"
        else:
            vacant = "No"

        if pros.absentee:
            absentee = "Yes"
        else:
            absentee = "No"

        if pros.api_response != "Address Is Not Valid Address":
            response = ""
        else:
            response = pros.api_response
        tag_count = Prospect_Properties.objects.filter(file__id=id).values('file__id').annotate(tagged=Count('tag'))
        if tag_count and tag_count[0]['tagged'] > 0:
            status = "Tagged"
        else:
            status = ""
        exportdata.append((pros.fullname, pros.firstname, pros.lastname, pros.mailingaddress, pros.mailingaddress2,
                           pros.mailingcity, pros.mailingstate, pros.mailingzip, pros.propertyaddress,
                           pros.propertyaddress2, pros.propertycity, pros.propertystate, pros.propertyzip,
                           pros.phonecell, pros.phonelandline, pros.phoneother, pros.phone1, pros.phone2, pros.phone3,
                           pros.phone4, pros.phone5, pros.phone6, pros.phone7, pros.phone8, pros.phone9, pros.phone10,
                           pros.email, pros.email2, pros.custome1,
                           pros.custome2, pros.custome3, pros.custome4, pros.custome5, pros.custome6, pros.custome7,
                           pros.custome8, pros.custome9, pros.custome10, opt, skip_trc, dnc, vacant, absentee, "",
                           list_count, pros.notes, status, response))

    print(exportdata)
    file_name = File.objects.get(id=id).file_name
    file_name = file_name.replace('.xlsx', '.xls')
    print(file_name)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Prospect_properties')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    custom_fields = CustomFieldsModel.objects.get(user=request.user)

    columns = ['Mailing Full Name', 'Mailing First Name', 'Mailing Last Name', 'Mailing Address', 'Mailing Address 2',
               'Mailing City', 'Mailing State', 'Mailing Zip', 'Prospect Address', 'Prospect Address 2',
               'Prospect City', 'Prospect State', 'Prospect Zip', 'Phone Cell', 'Phone Landline', 'Phone Other',
               'Phone 1', 'Phone 2', 'Phone 3', 'Phone 4', 'Phone 5', 'Phone 6', 'Phone 7', 'Phone 8', 'Phone 9',
               'Phone 10', 'Email', 'Email2',
               custom_fields.custom1, custom_fields.custom2, custom_fields.custom3, custom_fields.custom4,
               custom_fields.custom5, custom_fields.custom6, custom_fields.custom7, custom_fields.custom8,
               custom_fields.custom9, custom_fields.custom10, 'Opt-Out', 'Skip Traced', 'Do Not Call', 'Vacancy',
               'Absentee', 'Mailer Count', 'List Count', 'Notes', 'Status', 'Fail-Reason']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in exportdata:
        print(row)
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    user_id = request.user.pk
    wb.save("media/exported_files/" + file_name)

    profile = UserProfile.objects.get(user=request.user)
    user = request.user
    if profile.role.role_name == "Admin User":
        users = UserProfile.objects.filter(created_by__user=request.user).values('user')
    else:
        users = UserProfile.objects.filter(created_by__user=profile.created_by.user).values('user')
        user = profile.created_by.user

    if not ExportHistory.objects.filter((Q(user=user) | Q(user__in=users)) & Q(file_name=file_name)).exists():
        ExportHistory.objects.create(user=request.user, file_name=file_name)
    else:
        ExportHistory.objects.filter((Q(user=user) | Q(user__in=users)) & Q(file_name=file_name)).update(
            user=request.user,
            file_name=file_name)

    return JsonResponse(data)


@user_has_skip_history_Permission
def skipped_history_page(request, id):
    skipped_prospects = Prospect_Properties.objects.filter(file__id=id, skipped=True)
    list = File.objects.get(id=id).list
    return render(request, "reports/skipped_history_details.html",
                  {"skipped_prospects": skipped_prospects, "import_option": list.import_option,
                   "list_name": list.list_name})
