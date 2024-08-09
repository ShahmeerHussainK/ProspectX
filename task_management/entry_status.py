from datetime import datetime, timedelta


def check_event(event):
    from django.utils.timezone import now, timedelta

    today_datetime = now()

    # today_datetime = datetime.now()

    if event.start_date_time <= today_datetime and event.end_date_time >= today_datetime and event.is_completed is False:

        # "on_going_task"
        return '#6ee2dc'
    elif event.end_date_time < today_datetime and event.is_completed is False:
        # "past_due_tasks"
        return '#800000'
    elif event.start_date_time > today_datetime and event.is_completed is False:
        # "future_pending_tasks"
        return '#cde67f'
    elif event.is_completed is True:
        # "completed_tasks"
        return '#006a4e'






        daily_due_tasks = Task.objects.filter(start_date_time__lte=today_datetime, end_date_time__gte=today_datetime,
                                              is_completed=False, created_by=request.user).values('title',
                                                                                                  'assign_to__user__email',
                                                                                                  'assign_to__user__first_name').annotate(
            task_count=Count('assign_to'))

        # daily_due_tasks = Task.objects.raw('SELECT  FROM myapp_members GROUP BY designation')
        past_due_tasks = Task.objects.filter(end_date_time__lt=today_datetime, is_completed=False,
                                             created_by=request.user).values('title',
                                                                             'assign_to__user__email',
                                                                             'assign_to__user__first_name').annotate(
            task_count=Count('assign_to'))

        future_pending_tasks = Task.objects.filter(start_date_time__gt=today_datetime, is_completed=False,
                                                   created_by=request.user).values('title',
                                                                                   'assign_to__user__email',
                                                                                   'assign_to__user__first_name').annotate(
            task_count=Count('assign_to'))
        # future_pending_tasks = Task.objects.values('assign_to__user__first_name').annotate(task_count=Count('assign_to'))

        completed_tasks = Task.objects.filter(is_completed=True, created_by=request.user).values('title',
                                                                                                 'assign_to__user__email',
                                                                                                 'assign_to__user__first_name').annotate(
            task_count=Count('assign_to'))
