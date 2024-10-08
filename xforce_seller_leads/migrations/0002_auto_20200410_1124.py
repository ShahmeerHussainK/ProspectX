# Generated by Django 2.2.7 on 2020-04-10 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xforce_seller_leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerlead',
            name='actions',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('Send To E-Sign', 'Send To E-Sign'), ('Send To E-Sign Base 64', 'Send To E-Sign Base 64')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='campaign',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaign_for_seller_lead', to='marketing_machine.MarketingCampaign'),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='contract_action',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('Generate Contract', 'Generate Contract'), ('Email Contract', 'Email Contract')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='contract_delivery',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('E Signature', 'E Signature'), ('Email', 'Email'), ('In Person', 'In Person')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='follow_up_in',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('1 Day', '1 Day'), ('2 Days', '2 Days'), ('1 Week', '1 Week'), ('2 Weeks', '2 Weeks'), ('3 Weeks', '3 Weeks'), ('1 Month', '1 Month'), ('3 Months', '3 Months'), ('6 Months', '6 Months'), ('1 Year', '1 Year')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='follow_up_specific_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='lead_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='lead_file',
            field=models.FileField(blank=True, null=True, upload_to='seller_lead_files/'),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='lead_status',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('New Untouched', 'New Untouched'), ('Discovery', 'Discovery'), ('**Interested--> Updated Offer Status', '**Interested--> Updated Offer Status'), ('Not Interested / Follow Up', 'Not Interested / Follow Up'), ('DO NOT CONTACT', 'DO NOT CONTACT'), ('Solicitation Call / Wrong # / Other', 'Solicitation Call / Wrong # / Other'), ('Wants Retails', 'Wants Retails')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='made_offer',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('Make Offer', 'Make Offer'), ('Make Attempt 1', 'Make Attempt 1'), ('Make Attempt 2', 'Make Attempt 2'), ('Make Attempt 3', 'Make Attempt 3'), ('Make Attempt 4 > 1', 'Make Attempt 4 > 1'), ('Made Offer', 'Made Offer'), ('Offer Not Made', 'Offer Not Made')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='nurture_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow_up', to='xforce_seller_leads.FollowUp'),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='offer_status',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('Not Given', 'Not Given'), ('Accepted', 'Accepted'), ('Not Accepted', 'Not Accepted'), ('Negotiating', 'Negotiating')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='stage_of_contact',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('No Attempt', 'No Attempt'), ('Call Attempt 1', 'Call Attempt 1'), ('Call Attempt 2', 'Call Attempt 2'), ('Call Attempt 3', 'Call Attempt 3'), ('Call Attempt 4', 'Call Attempt 4'), ('Final Attempt > 1', 'Final Attempt > 1'), ('CONTACTED', 'CONTACTED')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='temperature',
            field=models.CharField(blank=True, choices=[('No Value', 'No Value'), ('Hot', 'Hot'), ('Warm', 'Warm'), ('Cold', 'Cold'), ('Dead', 'Dead')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sellerlead',
            name='title_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_for_seller', to='xforce_settings.Company'),
        ),
    ]
