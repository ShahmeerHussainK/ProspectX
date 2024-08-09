import datetime
from .models import *
from django import forms
from django.core.exceptions import ValidationError


class CreateTaskForm(forms.ModelForm):
    start_date_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'])
    end_date_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'])

    class Meta:
        model = Task
        fields = ('title', 'description', 'assign_to', 'temperature', 'start_date_time', 'end_date_time', 'is_all_day_task', )

    def clean(self):
        start_date_time = self.cleaned_data.get('start_date_time')
        end_date_time = self.cleaned_data.get('end_date_time')
        print(start_date_time)
        print(end_date_time)
        t = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
        time = datetime.datetime.strptime(t, '%m/%d/%Y %I:%M %p')
        st =start_date_time.strftime('%m/%d/%Y %I:%M %p')
        date = datetime.datetime.strptime(st, '%m/%d/%Y %I:%M %p')
        print(date)
        print(time)
        if date < time:
            raise ValidationError({'start_date_time': forms.ValidationError('Cannot create task on past dates.')})
        if start_date_time == end_date_time:
            raise ValidationError(
                {'start_date_time': forms.ValidationError('Start and end time cannot be same')})
        if start_date_time > end_date_time:
            raise ValidationError({'start_date_time': forms.ValidationError('Start date cannot be greater than end date.')})
        return self.cleaned_data


class UpdateTaskForm(forms.ModelForm):
    start_date_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'])
    end_date_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p'])
    id = forms.IntegerField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'assign_to', 'temperature', 'start_date_time', 'end_date_time', 'is_all_day_task', 'is_completed')

    def clean(self):
        start_date_time = self.cleaned_data.get('start_date_time')
        end_date_time = self.cleaned_data.get('end_date_time')
        t = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
        time = datetime.datetime.strptime(t, '%m/%d/%Y %I:%M %p')
        st = start_date_time.strftime('%m/%d/%Y %I:%M %p')
        date = datetime.datetime.strptime(st, '%m/%d/%Y %I:%M %p')
        if date < time:
            raise ValidationError({'start_date_time': forms.ValidationError('Cannot create task on past dates.')})
        if start_date_time == end_date_time:
            raise ValidationError(
                {'start_date_time': forms.ValidationError('Start and end time cannot be same')})
        if start_date_time > end_date_time:
            raise ValidationError({'start_date_time': forms.ValidationError('Start date cannot be greater than end date.')})
        return self.cleaned_data


class CreateReminderForm(forms.ModelForm):

    class Meta:
        model = Reminder
        fields = ('type_email', 'time_type', 'time_count', )


class UpdateReminderForm(forms.ModelForm):

    class Meta:
        model = Reminder
        fields = ('id', 'type_email', 'time_type', 'time_count', )