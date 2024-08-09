from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('notification_list', login_required(views.notification_list_view), name='notification_list'),
    path('reset_task_pill', login_required(views.reset_task_pill), name='reset_task_pill'),
    path('reset_notification_pill', login_required(views.reset_notification_pill), name='reset_notification_pill'),
    path('notification_status', login_required(views.notify_via_email_status), name='notification_status'),
]