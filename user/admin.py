from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile, list_display=('id', 'user'))
admin.site.register(Role, list_display=('id', 'role_name'))
admin.site.register(Permissions, list_display=('id', ))
admin.site.register(UserStripeDetail, list_display=('id', 'user', ))
admin.site.register(Dashboard, list_display=('id', 'block_title', ))
admin.site.register(WelcomeEmail, list_display=('id', ))
admin.site.register(EmailContent, list_display=('id', ))
admin.site.register(UserStats)
