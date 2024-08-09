from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Reminder)
admin.site.register(Task)
admin.site.register(Temperature)
admin.site.register(Time)
admin.site.register(Type)