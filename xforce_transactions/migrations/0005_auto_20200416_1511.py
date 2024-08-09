# Generated by Django 2.2.7 on 2020-04-16 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xforce_transactions', '0004_auto_20200415_0925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='contract_date_end',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='purchase_contract_ratification_date_end',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='contract_action',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('Generate Assignment Contract', 'Generate Assignment Contract'), ('Email Assignment Contract', 'Email Assignment Contract'), ('Email Assignment Contract To Title', 'Email Assignment Contract To Title'), ('Send Assignment Contract via esignature', 'Send Assignment Contract via esignature')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='marketing_price',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='potential',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('Wholesale', 'Wholesale'), ('Asset', 'Asset'), ('Fix and Flip', 'Fix and Flip')], max_length=50, null=True),
        ),
    ]
