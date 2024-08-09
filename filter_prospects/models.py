from django.db import models
from django.contrib.auth.models import User
from postgres_copy import CopyManager
import datetime

from datetime import date
# Create your models here.
from django.utils import timezone
from django.utils.timezone import localtime, now
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj


status_choices = (
    ('Active', 'Active'),
    ('InActive', 'InActive'),
)

pulled_status_choices = (
    ('Pulled', 'Pulled'),
    ('Not Pulled', 'Not Pulled'),
)

import_choices = (
    ("Import and Update Existing Property Information", "Import and Update Existing Property Information"),
    ("Import and Don't Update Existing Property Information", "Import and Don't Update Existing Property Information"),
    ("Only Import New Addresses", "Only Import New Addresses"),
)

update_choices = (
    ("Update Only if Field has Content in Spreadsheet", "Update Only if Field has Content in Spreadsheet"),
    ("Update Even if Field on Spreadsheet is Empty", "Update Even if Field on Spreadsheet is Empty"),
)


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=256, null=True, blank=False)
    list_status = models.CharField(max_length=50, choices=status_choices, default='Active')
    import_data = models.BooleanField(default=True)
    import_option = models.CharField(max_length=256, choices=import_choices,
                                     default="Import and Update Existing Property Information")
    update_option = models.CharField(max_length=256, choices=update_choices,
                                     default="Update Only if Field has Content in Spreadsheet")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.list_name

    class Meta:
        unique_together = (('user', 'list_name'),)
    #     verbose_name_plural = 'List'


class ListSequence(models.Model):
    list = models.OneToOneField(List, on_delete=models.CASCADE)
    list_pull_everyday = models.IntegerField(default=0)
    pulled_status = models.CharField(max_length=50, choices=pulled_status_choices, default='Not Pulled')
    pull_date = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.list.list_name

    class Meta:
        verbose_name_plural = 'ListSequence'


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=256, null=True, blank=False)
    tag_status = models.CharField(max_length=50, choices=status_choices, default='Active')
    tag_description = models.CharField(max_length=500, null=True, blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        unique_together = (('user', 'tag_name'),)
        verbose_name_plural = 'Tag'


opt_out_choices = (
    ('yes', 'yes'),
    ('no', 'no'),
)
els_check_options = (
    ('in process', 'in process'),
    ('completed', 'completed'),
    ('added to es', 'added to es'),
    ('es done', 'es done'),
    # ('es fail', 'es fail'),
)


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    tag_id = models.IntegerField(null=True, blank=True)
    file_name = models.CharField(max_length=256, null=True, blank=False)
    file_size = models.IntegerField(default=0, null=True, blank=True)
    sheet_name = models.CharField(max_length=256, null=True, blank=False)
    destination_fields = models.CharField(max_length=1000, null=True, blank=False)
    is_process_complete = models.BooleanField(default=False)
    is_process_started = models.BooleanField(default=False)
    fail_reason = models.CharField(max_length=200, default="-")
    created_at = models.DateField(auto_now_add=True)
    imported = models.IntegerField(default=0)
    updated = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)
    validation_complete = models.BooleanField(default=False, null=True, blank=True)
    opt_out = models.CharField(max_length=10, choices=opt_out_choices, default="no")
    skip_traced = models.CharField(max_length=10, choices=opt_out_choices, default="no")
    update_check = models.BooleanField(default=False, null=True, blank=True)
    update_started = models.BooleanField(default=False, null=True, blank=True)
    update_try = models.IntegerField(default=0)
    els_status = models.CharField(max_length=200, choices=els_check_options,default="in process", null=True, blank=True)

    def __str__(self):
        return self.file_name + " " + str(self.pk)

    class Meta:
        verbose_name_plural = 'File'


class Prospect_Properties(models.Model):
    list = models.ManyToManyField(List, null=True, blank=True)
    tag = models.ManyToManyField(Tag, null=True, blank=True)
    list_count = models.IntegerField(default=0, null=True, blank=True)
    tag_count = models.IntegerField(default=0, null=True, blank=True)
    file = models.ManyToManyField(File, null=True, blank=True)
    fullname = models.CharField(max_length=256, null=True, blank=True)
    firstname = models.CharField(max_length=256, null=True, blank=True)
    lastname = models.CharField(max_length=256, null=True, blank=True)
    propertyaddress = models.CharField(max_length=256, null=True, blank=False)
    propertyaddress2 = models.CharField(max_length=256, null=True, blank=True)
    propertycity = models.CharField(max_length=256, null=True, blank=False)
    propertystate = models.CharField(max_length=256, null=True, blank=False)
    propertyzip = models.CharField(max_length=256, null=True, blank=False)
    mailingaddress = models.CharField(max_length=256, null=True, blank=True)
    mailingaddress2 = models.CharField(max_length=256, null=True, blank=True)
    mailingcity = models.CharField(max_length=256, null=True, blank=True)
    mailingstate = models.CharField(max_length=256, null=True, blank=True)
    mailingzip = models.CharField(max_length=256, null=True, blank=True)
    phoneother = models.CharField(max_length=256, null=True, blank=True)
    phonecell = models.CharField(max_length=256, null=True, blank=True)
    phonelandline = models.CharField(max_length=256, null=True, blank=True)
    phone1 = models.CharField(max_length=256, null=True, blank=True)
    phone2 = models.CharField(max_length=256, null=True, blank=True)
    phone3 = models.CharField(max_length=256, null=True, blank=True)
    phone4 = models.CharField(max_length=256, null=True, blank=True)
    phone5 = models.CharField(max_length=256, null=True, blank=True)
    phone6 = models.CharField(max_length=256, null=True, blank=True)
    phone7 = models.CharField(max_length=256, null=True, blank=True)
    phone8 = models.CharField(max_length=256, null=True, blank=True)
    phone9 = models.CharField(max_length=256, null=True, blank=True)
    phone10 = models.CharField(max_length=256, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    email2 = models.CharField(max_length=256, null=True, blank=True)
    notes = models.CharField(max_length=256, null=True, blank=True)
    deceased = models.CharField(max_length=256, null=True, blank=True)
    yearbuilt = models.CharField(max_length=256, null=True, blank=True)
    donotcall = models.CharField(max_length=256, null=True, blank=True)
    opt_out = models.CharField(max_length=256, null=True, blank=True)
    skip_traced = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    skipped = models.BooleanField(default=False, null=True, blank=True)
    vacant = models.BooleanField(default=False, null=True, blank=True)
    absentee = models.BooleanField(default=False, null=True, blank=True)
    api_response = models.TextField(null=True, blank=True)
    custome1 = models.CharField(max_length=256, null=True, blank=True)
    custome2 = models.CharField(max_length=256, null=True, blank=True)
    custome3 = models.CharField(max_length=256, null=True, blank=True)
    custome4 = models.CharField(max_length=256, null=True, blank=True)
    custome5 = models.CharField(max_length=256, null=True, blank=True)
    custome6 = models.CharField(max_length=256, null=True, blank=True)
    custome7 = models.CharField(max_length=256, null=True, blank=True)
    custome8 = models.CharField(max_length=256, null=True, blank=True)
    custome9 = models.CharField(max_length=256, null=True, blank=True)
    custome10 = models.CharField(max_length=256, null=True, blank=True)
    is_validate_complete = models.BooleanField(default=False, null=True, blank=True)
    temp = models.CharField(max_length=246, null=True, blank=True)
    objects = CopyManager()
    added_to_els = models.BooleanField(default=False)


    def __str__(self):
        return self.propertyaddress

    def indexing(self):
        from filter_prospects.documents import ProspectDocument
        obj = ProspectDocument(
            meta={'id': self.id},
            fullname=self.fullname,
            firstname=self.firstname,
            lastname=self.lastname,
            propertyaddress=self.propertyaddress,
            propertyaddress2=self.propertyaddress2,
            propertycity=self.propertycity,
            propertystate=self.propertystate,
            propertyzip=self.propertyzip,
            mailingaddress=self.mailingaddress,
            mailingaddress2=self.mailingaddress2,
            mailingcity=self.mailingcity,
            mailingstate=self.mailingstate,
            mailingzip=self.mailingzip,
            email=self.email,
            email2=self.email2,
            phoneother=self.phoneother,
            phonecell=self.phonecell,
            phonelandline=self.phonelandline,
            phone1=self.phone1,
            phone2=self.phone2,
            phone3=self.phone3,
            phone4=self.phone4,
            phone5=self.phone5,
            phone6=self.phone6,
            phone7=self.phone7,
            phone8=self.phone8,
            phone9=self.phone9,
            phone10=self.phone10,
            absentee=self.absentee,
            vacant=self.vacant,
            skipped=self.skipped,
            is_validate_complete=self.is_validate_complete,
            opt_out=self.opt_out,
            custome1=self.custome1,
            custome2=self.custome2,
            custome3=self.custome3,
            custome4=self.custome4,
            custome5=self.custome5,
            custome6=self.custome6,
            custome7=self.custome7,
            custome8=self.custome8,
            custome9=self.custome9,
            custome10=self.custome10,
            notes=self.notes,
            list=self.list,
            tag=self.tag,

        )
        obj.save()
        return obj.to_dict(include_meta=True)

    # def list_indexing(self):
    #     return {
    #         'list_name': self.list.list_name,
    #         'id':  self.list.id,
    #         'user': {
    #                 'id': self.list.user.id,
    #                 'email': self.list.user.email
    #             }
    #     }


    class Meta:
        verbose_name_plural = 'Prospect_Property'


class CustomFieldsModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    custom1 = models.CharField(max_length=256, null=True, blank=True, default="custom1")
    custom2 = models.CharField(max_length=256, null=True, blank=True, default="custom2")
    custom3 = models.CharField(max_length=256, null=True, blank=True, default="custom3")
    custom4 = models.CharField(max_length=256, null=True, blank=True, default="custom4")
    custom5 = models.CharField(max_length=256, null=True, blank=True, default="custom5")
    custom6 = models.CharField(max_length=256, null=True, blank=True, default="custom6")
    custom7 = models.CharField(max_length=256, null=True, blank=True, default="custom7")
    custom8 = models.CharField(max_length=256, null=True, blank=True, default="custom8")
    custom9 = models.CharField(max_length=256, null=True, blank=True, default="custom9")
    custom10 = models.CharField(max_length=256, null=True, blank=True, default="custom10")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'CustomFieldsModel'


abs_vac = (
    ('Yes', 'Yes'),
    ('No', 'No'),

)

option_filter_choices = (
    ('And', 'And'),
    ('Or', 'Or'),
)

radio_inc = (
    ('in', 'in'),
    ('on', 'on'),
)


class Save_Filter(models.Model):
    filter_name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    search_query = models.TextField(null=True, blank=True)

    lists_inc = models.CharField(max_length=200, null=True, blank=True)
    lists_exc = models.CharField(max_length=200, null=True, blank=True)
    list_count_sel = models.CharField(max_length=50)
    list_inc_radio = models.CharField(max_length=10, choices=radio_inc, null=True, blank=True)

    tags_inc = models.CharField(max_length=200, null=True, blank=True)
    tags_exc = models.CharField(max_length=200, null=True, blank=True)
    tag_count_sel = models.CharField(max_length=50)
    tag_inc_radio = models.CharField(max_length=10, choices=radio_inc, null=True, blank=True)

    absentee = models.CharField(max_length=10, null=True, blank=True)
    vacant = models.CharField(max_length=10, null=True, blank=True)
    skipped = models.CharField(max_length=10, null=True, blank=True)
    opt_out = models.CharField(max_length=10, null=True, blank=True)
    optional_field_filters_condition_and_or = models.CharField(max_length=10)
    optional_field_filters_select_key = models.TextField(null=True, blank=True)
    optional_field_filters_select_con = models.TextField(null=True, blank=True)
    optional_field_filters_select_val = models.TextField(null=True, blank=True)

    search_query = models.CharField(max_length=500, null=True, blank=True)
    # optional_field_filters_condition = models.CharField(max_length=10, choices=option_filter_choices,null=True, blank=True)


class AddressValidationCounter(models.Model):
    last_valid_address = models.IntegerField(default=0)
    last_uploaded_address = models.IntegerField(default=0)