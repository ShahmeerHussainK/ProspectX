# Generated by Django 2.2.7 on 2020-04-29 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xforce_sales', '0010_auto_20200428_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='comps',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='email_content',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='lockbox_acess_info',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='notes',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='sales_offer',
            name='additional_details',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
