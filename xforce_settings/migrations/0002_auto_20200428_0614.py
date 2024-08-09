# Generated by Django 2.2.7 on 2020-04-28 06:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xforce_settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Phone number up to 15 digits allowed.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
