# Generated by Django 2.2.7 on 2020-05-07 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xforce_seller_leads', '0010_sellerlead_mailing_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerlead',
            name='actions',
        ),
    ]
