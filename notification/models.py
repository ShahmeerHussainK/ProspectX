from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Notification'


class Notification_Pill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_notification = models.BooleanField(default=False)
    sms_notification = models.BooleanField(default=False)
    task_pill = models.IntegerField(default=0)
    notification_pill = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Notification_Pill'
