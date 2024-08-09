from django.contrib.auth.models import User
from django.db import models
from user.models import UserProfile


class Temperature(models.Model):
    temperature = (
        ('cold', 'cold'),
        ('warm', 'warm'),
        ('hot', 'hot'),
    )
    temperature_name = models.CharField(max_length=10, choices=temperature, default='warm')

    def __str__(self):
        return self.temperature_name

    class Meta:
        verbose_name_plural = 'Temperature'


class Time(models.Model):
    time = (
        ('minutes', 'minutes'),
        ('hours', 'hours'),
        ('days', 'days'),
    )
    time_name = models.CharField(max_length=7, choices=time, default='minutes')

    def __str__(self):
        return self.time_name

    class Meta:
        verbose_name_plural = 'Time'


class Type(models.Model):
    type = (
        ('email', 'email'),
    )
    type_name = models.CharField(max_length=10, choices=type, default='email')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name_plural = 'Type'


class Task(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    assign_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    temperature = models.ForeignKey(Temperature, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    is_all_day_task = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    link = models.CharField(max_length=200, default="http://127.0.0.1:8000/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Task'


class Reminder(models.Model):
    type_email = models.ForeignKey(Type, on_delete=models.CASCADE, default="1")
    time_type = models.ForeignKey(Time, on_delete=models.CASCADE, default="1")
    time_count = models.IntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Reminder'

