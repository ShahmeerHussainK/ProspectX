
from django.db import migrations


def task_data_migrations(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    # User = apps.get_model('auth', 'User')
    Temperature = apps.get_model('task_management', 'Temperature')
    Time = apps.get_model('task_management', 'Time')
    Type = apps.get_model('task_management', 'Type')

    Temperature.objects.create(temperature_name="warm")
    Temperature.objects.create(temperature_name="cold")
    Temperature.objects.create(temperature_name="hot")

    Time.objects.create(time_name="minutes")
    Time.objects.create(time_name="hours")
    Time.objects.create(time_name="days")

    Type.objects.create(type_name="email")


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(task_data_migrations),
    ]
