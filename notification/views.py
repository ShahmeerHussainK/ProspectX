from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from twilio.rest import Client
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from prospectx_new.settings import account_sid_twilio, auth_token_twilio
from notification.models import Notification, Notification_Pill
from task_management.models import Reminder
import traceback


# def send_twilio_message(number, message):
#     try:
#         client = Client(account_sid_twilio, auth_token_twilio)
#         client.messages.create(
#             to=number,
#             from_="+12029913629",
#             body=message
#         )
#         # client.calls.create(
#         #     url='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
#         #     to='+92300202184833',
#         #     from_='+12029913629'
#         # )
#         data = {
#             "subscribed": "yes",
#         }
#         return {"data": data}
#     except:
#         print(traceback.print_exc())
#         data = {
#             "subscribed": "yes",
#         }
#         return {"data": data}


def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user)
    i = 1
    for notification in notifications:
        notification.id = i
        i += 1
    notifications.order_by('-id')
    return render(request, "notifications/notifications_list.html", {'notifications': notifications})


def reset_task_pill(request):
    Notification_Pill.objects.filter(user=request.user).update(task_pill=0)
    return JsonResponse({"message": "Task Pill Reset successfull"})


def reset_notification_pill(request):
    Notification_Pill.objects.filter(user=request.user).update(notification_pill=0)
    return JsonResponse({"message": "Notification Pill Reset successfull"})


def notify_via_email_status(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            status = request.POST.get('status')
            sms_status = request.POST.get('sms-status')
            print("sms_status:",sms_status)
            if sms_status == "on":
                sms_status = True
            else:
                sms_status = False

            if status == 'on':
                status = True
            else:
                status = False
            print("we are in post: ", status)
            Notification_Pill.objects.filter(user=request.user).update(email_notification=status, sms_notification=sms_status)
            return redirect('home')
        else:
            return redirect('home')
    else:
        notification = Notification_Pill.objects.filter(user=request.user)
        print("we are in get: ", notification[0].email_notification)
        return render(request, 'notifications/email_notification.html', {"data": notification[0]})
