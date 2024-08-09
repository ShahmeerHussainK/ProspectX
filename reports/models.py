from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ExportHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100, default="file")
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name_plural = 'Export History'
