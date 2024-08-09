from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(SkipTraceFile)
admin.site.register(DestinationFields)
admin.site.register(SingleSkipTrace)
admin.site.register(EmailTraced)
admin.site.register(PhoneTraced)
admin.site.register(AddressTraced)
admin.site.register(PrepaidBalance)
