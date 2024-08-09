from django.contrib import admin

# Register your models here.
from reports.models import ExportHistory

admin.site.register(ExportHistory)