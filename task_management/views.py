import traceback
from datetime import datetime, timedelta
from pprint import pprint
import stripe
from .entry_status import check_event
from django.forms.models import model_to_dict
from django.conf import settings
from django.core import serializers
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse, JsonResponse
import json
from django.template.loader import render_to_string
from django.db.models import Q, F
from task_management.forms import CreateTaskForm, CreateReminderForm, UpdateTaskForm
from task_management.serializer import ProfileSerializer, TaskSerializer, TaskSerializer3
from user.models import UserProfile
from .models import Task, Reminder, Type, Time
from payments.views import is_subscribed
from django.shortcuts import render
from django.db.models import Count


# celery -A prospectx_new beat -l info
# celery -A prospectx_new worker -l info

Reminder_FormSet = formset_factory(CreateReminderForm)
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django_eventstream import send_event
from django.core.mail import EmailMessage
from notification.models import *
from django.conf import settings

# import jsonpickle

Update_Reminder_FormSet = modelformset_factory(Reminder, fields=('type_email', 'time_type', 'time_count'), extra=0)


def index_evs(request):
    # user = User.objects.get(pk=1)
    return render(request, 'index.html', {"user": "user"})


def x_site_view(request):
    return render(request, 'coming_soon.html', {"user": "user"})


def x_force_view(request):
    return render(request, 'coming_soon.html', {"user": "user"})


# Create your views here.
def CreateTask(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    dataa = is_subscribed(request.user)
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            reminder_formset = Reminder_FormSet(request.POST)
            task_form = CreateTaskForm( request.POST)

            if user.role.role_name == "Admin User":
                if reminder_formset.is_valid() and task_form.is_valid():
                    task = task_form.save(commit=False)
                    task.created_by = request.user
                    current_url = get_current_site(request).domain + "task/all_tasks_calendar/"
                    task.link = current_url
                    task.save()
                    for reminder in reminder_formset:
                        rem = reminder.save(commit=False)
                        rem.task = task
                        rem.save()
                    data = {
                        'message': "Task Created Successfully!"
                    }
                    print("Admin Success")
                    if task_form.cleaned_data['assign_to']:
                        send_event('prospectx' + str(task_form.cleaned_data['assign_to'].user.id), 'message',
                                   'Task Management ('+task.title+') is assigned by Admin')
                        Notification.objects.create(user=task_form.cleaned_data['assign_to'].user,
                                                    title="Task Management ("+task.title+") is assigned by Admin")
                        Notification_Pill.objects.filter(user=task_form.cleaned_data['assign_to'].user).update(
                            notification_pill=F('notification_pill') + 1)
                        if Notification_Pill.objects.filter(user=task_form.cleaned_data['assign_to'].user, email_notification=True):
                            email_from = settings.EMAIL_HOST_USER
                            email_to = task_form.cleaned_data['assign_to'].user.email
                            message_body = "A New Task " + task.title + " has been assigned to you!"
                            send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                            send_email.content_subtype = 'html'
                            send_email.send()
                    channel = 'prospectx' + str(request.user.id)
                    send_event(channel, 'message', 'Task')

                    Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
                    return JsonResponse(data)
                else:
                    print(task_form.errors)
                    print(reminder_formset.errors)
                    data = {
                        'message': "Validation Error",
                        'task_form': task_form.errors
                    }
                    print("failure")
                    return JsonResponse(data, status=400)
            else:
                if task_form.is_valid():
                    task = task_form.save(commit=False)
                    task.created_by = request.user
                    current_url = get_current_site(request).domain + "task/all_tasks_calendar/"
                    task.link = current_url
                    task.save()
                    data = {
                        'message': "Task Created Successfully!"
                    }
                    send_event('prospectx' + str(request.user.id), 'message', 'Task')
                    Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
                    print("Other Users Success")
                    return JsonResponse(data)
                else:
                    print(json.dumps(task_form.errors))
                    data = {
                        'message': "Validation Error",
                        'task_form': task_form.errors
                    }
                    print("failure 2")
                    return JsonResponse(data, status=400)
        except:
            data = {
                "message": "There is some error!"
            }
            print("failed badly")
            return JsonResponse(data, status=400)


def LinkTask(request, pk):
    print("linked")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    user = UserProfile.objects.get(user=request.user)
    if request.method == "GET":
        user_profile = UserProfile.objects.get(user=request.user)

        context = {}
        context.update({"context_key": context_key})
        context.update({"subscription": data})
        if Task.objects.filter(pk=pk).exists():
            task = Task.objects.get(pk=pk)
        else:
            context.update({"message": "Task does not exist", "type": "info"})
            return render(request, 'tasks_calendar.html', context)
        context.update({"task": task.pk})
        if task.created_by == request.user:
            context.update({"message": "You can not link task with yourself", "type": "info"})
            return render(request, 'tasks_calendar.html', context)
        profile = UserProfile.objects.get(user=task.created_by)
        if user_profile.role.role_name == "Admin User":
            if profile.role.role_name == "Admin User":
                context.update({"message": "you don't have permission to view this task", "type": "info"})
                return render(request, 'tasks_calendar.html', context)
            elif profile.role.role_name == "Sub User" and profile.created_by.pk != request.user.pk:
                context.update({"message": "you don't have permission to view this task", "type": "info"})
                return render(request, 'tasks_calendar.html', context)

        elif user_profile.role.role_name == "Sub User":
            if profile.role.role_name == "Admin User" and profile.user.pk != user_profile.created_by.pk:
                context.update({"message": "you don't have permission to view this task", "type": "info"})
                return render(request, 'tasks_calendar.html', context)
            elif profile.role.role_name == "Sub User" and profile.created_by.pk != user_profile.created_by.pk:
                context.update({"message": "you don't have permission to view this task", "type": "info"})
                return render(request, 'tasks_calendar.html', context)
        return render(request, 'tasks_calendar.html', context)


def UpdateTask(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    dataa = is_subscribed(request.user)
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            reminder_formset = Reminder_FormSet(request.POST)
            update_reminder_formset = Update_Reminder_FormSet(request.POST, prefix='update')
            update_task_form = UpdateTaskForm(request.POST)

            if user.role.role_name == "Admin User":
                if update_task_form.is_valid():
                    old_assignee = Task.objects.get(pk=update_task_form.cleaned_data['id']).assign_to
                    Task.objects.filter(pk=update_task_form.cleaned_data['id']).update(
                        title=update_task_form.cleaned_data['title'],
                        description=update_task_form.cleaned_data['description'],
                        assign_to=update_task_form.cleaned_data['assign_to'],
                        start_date_time=update_task_form.cleaned_data['start_date_time'],
                        end_date_time=update_task_form.cleaned_data['end_date_time'],
                        is_all_day_task=update_task_form.cleaned_data['is_all_day_task'],
                        is_completed=update_task_form.cleaned_data['is_completed'],
                        temperature=update_task_form.cleaned_data['temperature'])

                    task = Task.objects.get(pk=update_task_form.cleaned_data['id'])
                    keys = Reminder.objects.filter(task__pk=task.pk).values('pk')
                    keys = list(keys)
                    i = 0
                    update_keys = []
                    for update_reminder in update_reminder_formset:
                        if update_reminder.data.get('update-' + str(i) + '-id'):
                            rem = Reminder.objects.filter(pk=update_reminder.data.get('update-' + str(i) + '-id'))
                            rem.update(time_type=update_reminder.data.get('update-' + str(i) + '-time_type'),
                                       time_count=update_reminder.data.get('update-' + str(i) + '-time_count'),
                                       task=task)
                            update_keys.append(update_reminder.data.get('update-' + str(i) + '-id'))
                        i += 1

                    for key in keys:
                        if str(key['pk']) not in update_keys:
                            Reminder.objects.filter(pk=key['pk']).delete()

                    i = 0
                    for create_reminder in reminder_formset:
                        if create_reminder.data.get('form-' + str(i) + '-time_count'):
                            print(create_reminder.data.get('form-' + str(i) + '-time_count'))
                            Reminder.objects.create(
                                time_count=create_reminder.data.get('form-' + str(i) + '-time_count'),
                                time_type=Time.objects.get(
                                    pk=create_reminder.data.get('form-' + str(i) + '-time_type')),
                                type_email=Type.objects.get(
                                    pk=create_reminder.data.get('form-' + str(i) + '-type_email')),
                                task=task)
                        i += 1
                    data = {
                        'message': "Task Updated Successfully!"
                    }

                    # Notifications for admin user
                    if update_task_form.cleaned_data['assign_to']:
                        if old_assignee:
                            if old_assignee.user == update_task_form.cleaned_data['assign_to'].user:
                                send_event('prospectx' + str(update_task_form.cleaned_data['assign_to'].user.id),
                                           'message',
                                           'Task Management ('+task.title+') is updated by Admin')
                                Notification_Pill.objects.filter(
                                    user=update_task_form.cleaned_data['assign_to'].user).update(
                                    notification_pill=F('notification_pill') + 1)
                                Notification.objects.create(user=update_task_form.cleaned_data['assign_to'].user,
                                                            title="Task Management ("+task.title+") is updated by Admin")
                                if Notification_Pill.objects.filter(user=update_task_form.cleaned_data['assign_to'].user,
                                                                    email_notification=True):
                                    email_from = settings.EMAIL_HOST_USER
                                    email_to = update_task_form.cleaned_data['assign_to'].user.email
                                    message_body = "Task " + task.title + " has been updated!"
                                    send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                                    send_email.content_subtype = 'html'
                                    send_email.send()
                            else:
                                send_event('prospectx' + str(old_assignee.user.id), 'message',
                                           'Task Management ('+task.title+') is removed by Admin')
                                Notification.objects.create(user=old_assignee.user,
                                                            title="Task Management ("+task.title+") is removed by Admin")
                                Notification_Pill.objects.filter(user=old_assignee.user).update(
                                    notification_pill=F('notification_pill') + 1)
                                if Notification_Pill.objects.filter(user=old_assignee.user,
                                                                    email_notification=True):
                                    email_from = settings.EMAIL_HOST_USER
                                    email_to = old_assignee.user.email
                                    message_body = "Task " + task.title + " has been removed.!"
                                    send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                                    send_email.content_subtype = 'html'
                                    send_email.send()
                                send_event('prospectx' + str(update_task_form.cleaned_data['assign_to'].user.id),
                                           'message',
                                           'Task Management ('+task.title+') is assigned by Admin')
                                Notification_Pill.objects.filter(
                                    user=update_task_form.cleaned_data['assign_to'].user).update(
                                    notification_pill=F('notification_pill') + 1)
                                Notification.objects.create(user=update_task_form.cleaned_data['assign_to'].user,
                                                            title="Task Management ("+task.title+") is assigned by Admin")
                                if Notification_Pill.objects.filter(user=update_task_form.cleaned_data['assign_to'].user,
                                                                    email_notification=True):
                                    email_from = settings.EMAIL_HOST_USER
                                    email_to = update_task_form.cleaned_data['assign_to'].user.email
                                    message_body = "A New Task " + task.title + " has been assigned to you!"
                                    send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                                    send_email.content_subtype = 'html'
                                    send_email.send()
                        else:
                            send_event('prospectx' + str(update_task_form.cleaned_data['assign_to'].user.id), 'message',
                                       'Task Management ('+task.title+') is assigned by Admin')
                            Notification.objects.create(user=update_task_form.cleaned_data['assign_to'].user,
                                                        title="Task Management ("+task.title+") is assigned by Admin")
                            Notification_Pill.objects.filter(
                                user=update_task_form.cleaned_data['assign_to'].user).update(
                                notification_pill=F('notification_pill') + 1)
                            if Notification_Pill.objects.filter(user=update_task_form.cleaned_data['assign_to'].user,
                                                                email_notification=True):
                                email_from = settings.EMAIL_HOST_USER
                                email_to = update_task_form.cleaned_data['assign_to'].user.email
                                message_body = "A New Task " + task.title + " has been assigned to you!"
                                send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                                send_email.content_subtype = 'html'
                                send_email.send()
                    elif old_assignee:
                        send_event('prospectx' + str(old_assignee.user.id), 'message',
                                   'Task Management ('+task.title+') is removed by Admin')
                        Notification.objects.create(user=old_assignee.user,
                                                    title="Task Management ("+task.title+") is removed by Admin")
                        Notification_Pill.objects.filter(user=old_assignee.user).update(
                            notification_pill=F('notification_pill') + 1)
                        if Notification_Pill.objects.filter(user=old_assignee.user,
                                                            email_notification=True):
                            email_from = settings.EMAIL_HOST_USER
                            email_to = old_assignee.user.email
                            message_body = "Task " + task.title + " has been removed!"
                            send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                            send_email.content_subtype = 'html'
                            send_email.send()

                    send_event('prospectx' + str(request.user.id), 'message', 'Task')
                    Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
                    print("Admin Success")
                    return JsonResponse(data)
                else:
                    print(update_task_form.errors)
                    print(reminder_formset.errors)
                    data = {
                        'message': "Validation Error",
                        'task_form': update_task_form.errors
                    }
                    print("failure")
                    return JsonResponse(data, status=400)
            else:
                if update_task_form.is_valid():
                    Task.objects.filter(pk=update_task_form.cleaned_data['id']).update(
                        title=update_task_form.cleaned_data['title'],
                        description=update_task_form.cleaned_data['description'],
                        # assign_to=update_task_form.cleaned_data['assign_to'],
                        start_date_time=update_task_form.cleaned_data['start_date_time'],
                        end_date_time=update_task_form.cleaned_data['end_date_time'],
                        is_all_day_task=update_task_form.cleaned_data['is_all_day_task'],
                        is_completed=update_task_form.cleaned_data['is_completed'],
                        temperature=update_task_form.cleaned_data['temperature'])

                    task = Task.objects.get(pk=update_task_form.cleaned_data['id'])
                    if user.role.role_name == "Sub User":
                        if task.created_by != request.user:
                            send_event('prospectx' + str(task.created_by.id), 'message',
                                       'Task Management ('+task.title+') is updated') # subuser
                            Notification.objects.create(user=task.created_by,
                                                        title="Task Management ("+task.title+") is updated")
                            Notification_Pill.objects.filter(user=task.created_by).update(
                                notification_pill=F('notification_pill') + 1)
                            if Notification_Pill.objects.filter(user=task.created_by,
                                                                email_notification=True):
                                email_from = settings.EMAIL_HOST_USER
                                email_to = task.created_by.email
                                message_body = "Task " + task.title + " has been updated!"
                                send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                                send_email.content_subtype = 'html'
                                send_email.send()
                    data = {
                        'message': "Task Updated Successfully!"
                    }
                    send_event('prospectx' + str(request.user.id), 'message', 'Task')
                    Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
                    print("Other Users Success")
                    return JsonResponse(data)
                else:
                    print(json.dumps(update_task_form.errors))
                    data = {
                        'message': "Validation Error",
                        'task_form': update_task_form.errors
                    }
                    print("failure 2")
                    return JsonResponse(data, status=400)
        except:
            print(traceback.format_exc())
            data = {
                "message": "There is some error!"
            }
            print("failed badly")
            return JsonResponse(data, status=400)


def DeleteTask(request, id):
    try:
        user = UserProfile.objects.get(user=request.user)
        if Task.objects.filter(pk=id).exists():
            task = Task.objects.get(pk=id)
            Task.objects.filter(pk=id).delete()
            data = {"message": "Deleted successfully"}
            if user.user != task.created_by:
                send_event('prospectx' + str(task.created_by.id), 'message',
                           'Task Management ('+task.title+') is deleted')
                Notification.objects.create(user=task.created_by,
                                            title="Task Management ("+task.title+") is deleted")
                Notification_Pill.objects.filter(user=task.created_by).update(
                    notification_pill=F('notification_pill') + 1)
                if Notification_Pill.objects.filter(user=task.created_by,
                                                    email_notification=True):
                    email_from = settings.EMAIL_HOST_USER
                    email_to = task.created_by.email
                    message_body = "Task " + task.title + " has been deleted!"
                    send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                    send_email.content_subtype = 'html'
                    send_email.send()
            if task.assign_to and user != task.assign_to:
                send_event('prospectx' + str(task.assign_to.user.id), 'message',
                           'Task Management ('+task.title+') is deleted')
                Notification.objects.create(user=task.assign_to.user,
                                            title="Task Management ("+task.title+") is deleted")
                Notification_Pill.objects.filter(user=task.assign_to.user).update(
                    notification_pill=F('notification_pill') + 1)
                if Notification_Pill.objects.filter(user=task.assign_to.user,
                                                    email_notification=True):
                    email_from = settings.EMAIL_HOST_USER
                    email_to = task.assign_to.user.email
                    message_body = "Task " + task.title + " has been deleted!"
                    send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                    send_email.content_subtype = 'html'
                    send_email.send()
            send_event('prospectx' + str(request.user.id), 'message', 'Task')
            Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
            return JsonResponse(data)
        else:
            print("out")
            data = {"message": "Task does not exist"}
            return JsonResponse(data)
    except:
        print(traceback.format_exc())
        data = {"message": "There was an error!"}
        return JsonResponse(data)


def DuplicateTask(request, id):
    try:
        user = UserProfile.objects.get(user=request.user)
        if Task.objects.filter(pk=id).exists():
            task = Task.objects.get(pk=id)
            reminder = Reminder.objects.filter(task=task).values('pk')
            profile = UserProfile.objects.get(user=request.user)
            if profile.role.role_name == "Admin User":
                duplicate = Task.objects.create(created_by=request.user,
                                            title=task.title,
                                            description=task.description,
                                            assign_to=task.assign_to,
                                            temperature=task.temperature,
                                            start_date_time=task.start_date_time,
                                            end_date_time=task.end_date_time,
                                            is_all_day_task=task.is_all_day_task,
                                            is_completed=task.is_completed)

                for rem in reminder:
                    remind = Reminder.objects.get(pk=rem['pk'])
                    remind.pk = None
                    remind.task = duplicate
                    remind.save()
            else:
                Task.objects.create(created_by=request.user,
                                                title=task.title,
                                                description=task.description,
                                                # assign_to=task.assign_to,
                                                temperature=task.temperature,
                                                start_date_time=task.start_date_time,
                                                end_date_time=task.end_date_time,
                                                is_all_day_task=task.is_all_day_task,
                                                is_completed=task.is_completed)
            if task.assign_to and user != task.assign_to:
                send_event('prospectx' + str(task.assign_to.user.id), 'message',
                           'Task Management ('+task.title+') is duplicated')
                Notification.objects.create(user=task.assign_to.user,
                                            title="Task Management ("+task.title+") is duplicated")
                Notification_Pill.objects.filter(user=task.assign_to.user).update(
                    notification_pill=F('notification_pill') + 1)
                if Notification_Pill.objects.filter(user=task.assign_to.user,
                                                    email_notification=True):
                    email_from = settings.EMAIL_HOST_USER
                    email_to = task.assign_to.user.email
                    message_body = "Task " + task.title + " has been duplicated!"
                    send_email = EmailMessage("Prospect X", message_body, email_from, [email_to])
                    send_email.content_subtype = 'html'
                    send_email.send()
            print("here")
            send_event('prospectx' + str(request.user.id), 'message', 'Task')
            Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
            data = {"message": "Task Duplicated Successfully"}
            return JsonResponse(data)
        else:
            data = {"message": "Task does not exist"}
            return JsonResponse(data)
    except:
        print(traceback.format_exc())
        data = {"message": "There was an error!"}
        return JsonResponse(data)


def index(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    return render(request, 'calendar_view.html', {"context_key": context_key, "subscription": data})


def taskView(request):
    print("hello world")
    print("in task view")
    get_profile = UserProfile.objects.get(user=request.user)
    json_list = []
    today_datetime = datetime.today()
    action = request.GET['event']
    from django.utils.timezone import utc

    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    if get_profile.role.role_name == 'Sub User':
        if request.is_ajax():
            print('Its ajax from fullCalendar')

        try:
            start = datetime.fromtimestamp(int(request.GET.get('start', False))).replace(tzinfo=utc)
            end = datetime.fromtimestamp(int(request.GET.get('end', False)))
        except ValueError:
            # start = datetime.now.replace(tzinfo=utc)
            start = datetime.now()
            end = start + timedelta(days=7)
        if action == 'all':
            entries = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile))
        elif action == 'over_due':
            entries = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile),
                                          end_date_time__lt=today_datetime, is_completed=False)
        elif action == 'upcoming_task':
            entries = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile),
                                          start_date_time__gt=today_datetime, is_completed=False)
            # print(entries)

        for entry in entries:
            inc_date = entry.end_date_time + timedelta(days=1)
            print(entry.end_date_time)
            print(inc_date)
            color = check_event(entry)
            id = entry.id
            title = entry.title
            start = str(entry.start_date_time)
            end = str(entry.end_date_time)
            # end = str(inc_date)
            allDay = entry.is_all_day_task
            created_by = entry.created_by
            temperature = entry.temperature
            is_completed = entry.is_completed
            description = entry.description
            reminders = entry.reminder_set.all()
            assign_to = ProfileSerializer(entry.assign_to).data
            subusers = ProfileSerializer(UserProfile.objects.filter(created_by__user=request.user), many=True).data
            for u in subusers:
                print(u.id)

            json_entry = {'id': id, 'title': title, 'start': start, 'end': end, 'description': description,
                          "color": color,
                          'allDay': allDay,
                          'assign_to': assign_to, 'subusers': subusers,
                          'temperature': temperature.temperature_name, 'is_completed': is_completed,
                          'reminders': serializers.serialize('json', reminders)}
            json_list.append(json_entry)
    else:
        if request.is_ajax():
            print('Its ajax from fullCalendar')

        try:
            start = datetime.fromtimestamp(int(request.GET.get('start', False))).replace(tzinfo=utc)
            end = datetime.fromtimestamp(int(request.GET.get('end', False)))
        except ValueError:
            # start = datetime.now.replace(tzinfo=utc)
            start = datetime.now()
            end = start + timedelta(days=7)
        if action == 'all':
            entries = Task.objects.filter(created_by=request.user)
        elif action == 'over_due':
            entries = Task.objects.filter(end_date_time__lt=today_datetime, is_completed=False, created_by=request.user)
        elif action == 'upcoming_task':
            entries = Task.objects.filter(start_date_time__gt=today_datetime, is_completed=False,
                                          created_by=request.user)
        # print(entries)

        for entry in entries:
            inc_date = entry.end_date_time + timedelta(days=1)
            print(entry.end_date_time)
            print(inc_date)
            color = check_event(entry)
            id = entry.id
            title = entry.title
            start = str(entry.start_date_time)
            end = str(entry.end_date_time)
            # end = str(inc_date)
            allDay = entry.is_all_day_task
            created_by = entry.created_by
            temperature = entry.temperature
            is_completed = entry.is_completed
            description = entry.description
            reminders = entry.reminder_set.all()
            assign_to = ProfileSerializer(entry.assign_to).data
            subusers = ProfileSerializer(UserProfile.objects.filter(created_by__user=request.user), many=True).data

            json_entry = {'id': id, 'title': title, 'start': start, 'end': end, 'description': description,
                          'allDay': allDay, 'color': color,
                          'assign_to': assign_to, 'subusers': subusers,
                          'temperature': temperature.temperature_name, 'is_completed': is_completed,
                          'reminders': serializers.serialize('json', reminders)}
            json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')


def get_list_data(request, category):
    get_profile = UserProfile.objects.get(user=request.user)
    tasks = None
    today_datetime = datetime.today()
    today_date = datetime.today().date()
    now = timezone.now()
    yesterday = datetime.today().date() - timedelta(1)
    tasks_formsets = []
    if get_profile.role.role_name == 'Sub User':
        if category == "all":
            tasks = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile)).order_by('-id')
            pprint(tasks)
        if category == "daily_task":
            tasks = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile),
                                        start_date_time__lte=today_datetime, end_date_time__gte=today_datetime,
                                        is_completed=False).order_by('-id')
        if category == "past_due_task":
            tasks = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile),
                                        end_date_time__lt=today_datetime, is_completed=False).order_by('-id')
        if category == "future_pending_task":
            tasks = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile),
                                        start_date_time__gt=today_datetime, is_completed=False).order_by('-id')
        if category == "completed_task":
            tasks = Task.objects.filter(Q(created_by=request.user) | Q(assign_to=get_profile),
                                        is_completed=True).order_by('-id')

        daily_due_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__lte=today_datetime,
            end_date_time__gte=today_datetime,
            is_completed=False)

        daily_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__lte=today_datetime,
            end_date_time__gte=today_datetime,
            is_completed=False).count()

        past_due_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), end_date_time__lt=today_datetime,
            is_completed=False)

        past_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), end_date_time__lt=today_datetime,
            is_completed=False).count()

        future_pending_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__gt=today_datetime,
            is_completed=False)

        future_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__gt=today_datetime,
            is_completed=False).count()

        completed_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), is_completed=True)

        completed_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), is_completed=True).count()

        context = {"tasks": tasks,
                   'daily_due_tasks': daily_due_tasks,
                   'past_due_tasks': past_due_tasks,
                   'future_pending_tasks': future_pending_tasks,
                   'completed_tasks': completed_tasks

                   }
        pprint(tasks)
        subusers = ProfileSerializer(UserProfile.objects.filter(created_by__user=request.user), many=True).data
        if request.is_ajax():
            print('Its ajax from fullCalendar list')
            context = {"tasks": TaskSerializer(tasks, many=True).data,
                       'daily_due_tasks': json.dumps(list(daily_due_tasks)),
                       'past_due_tasks': json.dumps(list(past_due_tasks)),
                       'future_pending_tasks': json.dumps(list(future_pending_tasks)),
                       'completed_tasks': json.dumps(list(completed_tasks)),
                       'subusers': subusers,
                       "future_count": future_count,
                       "past_count": past_count,
                       "daily_count": daily_count,
                       "completed_count": completed_count
                       }
            return JsonResponse(context, content_type="application/json")
        return context
    else:
        if category == "all":
            tasks = Task.objects.filter(created_by=request.user).order_by('-id')

        if category == "daily_task":
            tasks = Task.objects.filter(start_date_time__lte=today_datetime, end_date_time__gte=today_datetime,
                                        is_completed=False, created_by=request.user).order_by('-id')
        if category == "past_due_task":
            tasks = Task.objects.filter(end_date_time__lt=today_datetime, is_completed=False,
                                        created_by=request.user).order_by('-id')
        if category == "future_pending_task":
            tasks = Task.objects.filter(start_date_time__gt=today_datetime, is_completed=False,
                                        created_by=request.user).order_by('-id')
        if category == "completed_task":
            tasks = Task.objects.filter(is_completed=True, created_by=request.user).order_by('-id')

        daily_due_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__lte=today_datetime,
            end_date_time__gte=today_datetime,
            is_completed=False)

        daily_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__lte=today_datetime,
            end_date_time__gte=today_datetime,
            is_completed=False).count()

        past_due_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), end_date_time__lt=today_datetime,
            is_completed=False)

        past_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), end_date_time__lt=today_datetime,
            is_completed=False).count()

        future_pending_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__gt=today_datetime,
            is_completed=False)

        future_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), start_date_time__gt=today_datetime,
            is_completed=False).count()

        completed_tasks = Task.objects.values('assign_to__user__id', 'assign_to__user__first_name').annotate(
            task_count=Count('id')).filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), is_completed=True)

        completed_count = Task.objects.filter(
            Q(created_by=request.user) | Q(assign_to=get_profile), is_completed=True).count()


        context = {"tasks": tasks,
                   'daily_due_tasks': daily_due_tasks,
                   'past_due_tasks': past_due_tasks,
                   'future_pending_tasks': future_pending_tasks,
                   'completed_tasks': completed_tasks, "future_count": future_count,

                   }
        subusers = ProfileSerializer(UserProfile.objects.filter(created_by__user=request.user), many=True).data
        if request.is_ajax():
            print('Its ajax from fullCalendar list')
            context = {"tasks": TaskSerializer(tasks, many=True).data,
                       'daily_due_tasks': json.dumps(list(daily_due_tasks)),
                       'past_due_tasks': json.dumps(list(past_due_tasks)),
                       'future_pending_tasks': json.dumps(list(future_pending_tasks)),
                       'completed_tasks': json.dumps(list(completed_tasks)),
                       'subusers': subusers,
                       "future_count": future_count,
                       "past_count": past_count,
                       "daily_count": daily_count,
                       "completed_count": completed_count
                       }
            return JsonResponse(context, content_type="application/json")
        return context


def all_tasks_calendar(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    context_key = {'key': key}
    data = is_subscribed(request.user)
    # context = get_list_data(request,category)
    context = {}
    context.update({"context_key": context_key})
    context.update({"subscription": data})

    return render(request, 'tasks_calendar.html', context)


def add_event(request):
    print("request come")
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Task(title=str(title), start_date_time=start, end_date_time=end)
    event.save()
    data = {}
    return JsonResponse(data)


def task_formsets(request, id):
    data = dict()
    task_id = id
    task_obj = Task.objects.get(id=task_id)
    all_reminders = task_obj.reminder_set.all()
    updates_reminder_form = Update_Reminder_FormSet(queryset=all_reminders, prefix='update')

    context = {'reminder_form': Reminder_FormSet(), 'updates_reminder_form': updates_reminder_form}

    data['html_form'] = render_to_string('_partial_update_formset.html',
                                         context,
                                         request=request, )
    return JsonResponse(data)


def create_task_formsets(request):
    data = dict()
    context = {'reminder_form': Reminder_FormSet()}
    data['html_form'] = render_to_string('_partial_create_formset.html',
                                         context,
                                         request=request, )
    return JsonResponse(data)


def LinkedTask(request, id):
    data = dict()
    task_id = id
    task_obj = Task.objects.get(id=task_id)
    context = {'reminder_form': Reminder_FormSet()}
    data['html_form'] = render_to_string('_partial_create_formset.html',
                                         context,
                                         request=request, )
    serializer = TaskSerializer3(task_obj)
    data['task_obj'] = serializer.data
    return JsonResponse(data)


def SaveLinkedTask(request):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        key = settings.STRIPE_PUBLISHABLE_KEY
        context_key = {'key': key}
        data = is_subscribed(request.user)
        user = UserProfile.objects.get(user=request.user)
        try:
            reminder_formset = Reminder_FormSet(request.POST)
            update_task_form = UpdateTaskForm(request.POST)
            if user.role.role_name == "Admin User":
                if update_task_form.is_valid():
                    Task.objects.filter(pk=update_task_form.cleaned_data['id']).update(
                        title=update_task_form.cleaned_data['title'],
                        description=update_task_form.cleaned_data['description'],
                        assign_to=update_task_form.cleaned_data['assign_to'],
                        start_date_time=update_task_form.cleaned_data['start_date_time'],
                        end_date_time=update_task_form.cleaned_data['end_date_time'],
                        is_all_day_task=update_task_form.cleaned_data['is_all_day_task'],
                        is_completed=update_task_form.cleaned_data['is_completed'],
                        temperature=update_task_form.cleaned_data['temperature'])

                    new_task = Task.objects.create(created_by=request.user,
                                                   title=update_task_form.cleaned_data['title'],
                                                   description=update_task_form.cleaned_data['description'],
                                                   assign_to=update_task_form.cleaned_data['assign_to'],
                                                   start_date_time=update_task_form.cleaned_data['start_date_time'],
                                                   end_date_time=update_task_form.cleaned_data['end_date_time'],
                                                   is_all_day_task=update_task_form.cleaned_data['is_all_day_task'],
                                                   is_completed=update_task_form.cleaned_data['is_completed'],
                                                   temperature=update_task_form.cleaned_data['temperature'])

                    task = Task.objects.get(pk=update_task_form.cleaned_data['id'])

                    i = 0
                    for create_reminder in reminder_formset:
                        if create_reminder.data.get('form-' + str(i) + '-time_count'):
                            Reminder.objects.create(
                                time_count=create_reminder.data.get('form-' + str(i) + '-time_count'),
                                time_type=Time.objects.get(
                                    pk=create_reminder.data.get('form-' + str(i) + '-time_type')),
                                type_email=Type.objects.get(
                                    pk=create_reminder.data.get('form-' + str(i) + '-type_email')),
                                task=new_task)
                        i += 1
                    data = {
                        'message': "Task Linked Successfully!"
                    }
                    send_event('prospectx' + str(request.user.id), 'message', 'Task')
                    Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
                    print("Admin Success")
                    return JsonResponse(data)
                else:
                    print(update_task_form.errors)
                    print(reminder_formset.errors)
                    data = {
                        'message': "Validation Error",
                        'task_form': update_task_form.errors
                    }
                    print("failure")
                    return JsonResponse(data, status=400)
            else:
                if update_task_form.is_valid():
                    Task.objects.filter(pk=update_task_form.cleaned_data['id']).update(
                        title=update_task_form.cleaned_data['title'],
                        description=update_task_form.cleaned_data['description'],
                        assign_to=update_task_form.cleaned_data['assign_to'],
                        start_date_time=update_task_form.cleaned_data['start_date_time'],
                        end_date_time=update_task_form.cleaned_data['end_date_time'],
                        is_all_day_task=update_task_form.cleaned_data['is_all_day_task'],
                        is_completed=update_task_form.cleaned_data['is_completed'],
                        temperature=update_task_form.cleaned_data['temperature'])

                    Task.objects.create(created_by=request.user,
                                        title=update_task_form.cleaned_data['title'],
                                        description=update_task_form.cleaned_data['description'],
                                        assign_to=update_task_form.cleaned_data['assign_to'],
                                        start_date_time=update_task_form.cleaned_data['start_date_time'],
                                        end_date_time=update_task_form.cleaned_data['end_date_time'],
                                        is_all_day_task=update_task_form.cleaned_data['is_all_day_task'],
                                        is_completed=update_task_form.cleaned_data['is_completed'],
                                        temperature=update_task_form.cleaned_data['temperature'])

                    data = {
                        'message': "Task Linked Successfully!"
                    }
                    print("Other Users Success")
                    send_event('prospectx' + str(request.user.id), 'message', 'Task')
                    Notification_Pill.objects.filter(user=request.user).update(task_pill=F('task_pill') + 1)
                    return JsonResponse(data)
                else:
                    print(json.dumps(update_task_form.errors))
                    data = {
                        'message': "Validation Error",
                        'task_form': update_task_form.errors
                    }
                    print("failure 2")
                    return JsonResponse(data, status=400)
        except:
            print(traceback.format_exc())
            data = {
                "message": "There is some error!"
            }
            print("failed badly")
            return JsonResponse(data, status=400)
