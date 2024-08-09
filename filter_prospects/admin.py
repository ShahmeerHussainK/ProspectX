from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(File)
admin.site.register(List)
admin.site.register(ListSequence)
admin.site.register(CustomFieldsModel)
admin.site.register(Tag)
# admin.site.register(Prospect_Properties)
admin.site.register(Save_Filter)
admin.site.register(AddressValidationCounter)


class ProspectPropertiesAdmin(admin.ModelAdmin):
    search_fields = ['id', 'propertyaddress']
    list_display = ['id', 'propertyaddress']


admin.site.register(Prospect_Properties, ProspectPropertiesAdmin)
