from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audience_name', models.CharField(choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], default='Buyer', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Audience',
            },
        ),
        migrations.CreateModel(
            name='BuyerOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(choices=[('Commercial', 'Commercial'), ('Investor', 'Investor'), ('Landlord', 'Landlord'), ('Landlord - Turn Key', 'Landlord - Turn Key'), ('Lease Option', 'Lease Option'), ('Owner Finance', 'Owner Finance'), ('Rehabber', 'Rehabber'), ('Renter', 'Renter'), ('Retail', 'Retail')], default='Commercial', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Buyer Option',
            },
        ),
        migrations.CreateModel(
            name='ContentPack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_pack_name', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.ImageField(default='content_pack_logo_images/logo.png', upload_to='content_pack_logo_images/')),
                ('banner_title', models.CharField(max_length=300)),
                ('banner_button_text', models.CharField(max_length=300)),
                ('about_us_title', models.CharField(max_length=300)),
                ('about_us_desc', models.TextField()),
                ('video_link', models.CharField(max_length=300)),
                ('video_title', models.CharField(max_length=300)),
                ('video_desc', models.TextField()),
                ('testi_1_company_name', models.CharField(max_length=300)),
                ('testi_1_person_name', models.CharField(max_length=300)),
                ('testi_1_text', models.TextField()),
                ('testi_2_company_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_2_person_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_2_text', models.TextField(blank=True, null=True)),
                ('testi_3_company_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_3_person_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_3_text', models.TextField(blank=True, null=True)),
                ('other_details_title', models.CharField(max_length=300)),
                ('other_details_desc', models.TextField()),
                ('call_to_action_text', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Content Pack',
            },
        ),
        migrations.CreateModel(
            name='ListingOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_name', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Will Be Listed Soon', 'Will Be Listed Soon')], default='Yes', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Listing Option',
            },
        ),
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=100)),
                ('billing_amount', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Membership Plan',
            },
        ),
        migrations.CreateModel(
            name='SiteDesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=50)),
                ('html_head_content', models.CharField(default='nothing', max_length=100000)),
                ('html_body_content', models.CharField(default='nothing', max_length=100000)),
                ('template_url', models.CharField(default='xsite/site_design_templates/xsite_template_1.html', max_length=200)),
                ('template_image', models.CharField(default='/Site_Design_imgs/Brownstone.png', max_length=200)),
                ('audience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.Audience')),
                ('content_pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.ContentPack')),
            ],
            options={
                'verbose_name_plural': 'Site Design',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(choices=[('New', 'New'), ('Follow Up', 'Follow Up'), ('Pending', 'Pending'), ('Won', 'Won'), ('Dead', 'Dead')], default='New', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Websites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=200)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('renewal_date', models.DateField()),
                ('domain_price', models.FloatField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('site_design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.SiteDesign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Site',
            },
        ),
        migrations.CreateModel(
            name='TemplateContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_head_content', models.CharField(default='nothing', max_length=100000)),
                ('html_body_content', models.CharField(default='nothing', max_length=100000)),
                ('is_edited', models.BooleanField(default=False)),
                ('content_pack_name', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.ImageField(blank=True, default='content_pack_logo_images/logo.png', null=True, upload_to='content_pack_logo_images/')),
                ('banner_title', models.CharField(max_length=300)),
                ('banner_button_text', models.CharField(max_length=300)),
                ('about_us_title', models.CharField(max_length=300)),
                ('about_us_desc', models.TextField()),
                ('video_link', models.CharField(max_length=300)),
                ('video_title', models.CharField(max_length=300)),
                ('video_desc', models.TextField()),
                ('testi_1_company_name', models.CharField(max_length=300)),
                ('testi_1_person_name', models.CharField(max_length=300)),
                ('testi_1_text', models.TextField()),
                ('testi_2_company_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_2_person_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_2_text', models.TextField(blank=True, null=True)),
                ('testi_3_company_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_3_person_name', models.CharField(blank=True, max_length=300, null=True)),
                ('testi_3_text', models.TextField(blank=True, null=True)),
                ('other_details_title', models.CharField(max_length=300)),
                ('other_details_desc', models.TextField()),
                ('call_to_action_text', models.CharField(max_length=300)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.Websites')),
            ],
            options={
                'verbose_name_plural': 'Template Content',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=5, null=True)),
                ('phone', models.CharField(blank=True, max_length=256, null=True)),
                ('fax', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=100, null=True)),
                ('parent_website_url', models.CharField(blank=True, max_length=300, null=True)),
                ('google_analytics_tracking_code', models.CharField(blank=True, max_length=100, null=True)),
                ('website_title', models.CharField(blank=True, max_length=100, null=True)),
                ('redirect_url', models.CharField(blank=True, max_length=300, null=True)),
                ('site', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.Websites')),
            ],
            options={
                'verbose_name_plural': 'Setting',
            },
        ),
        migrations.CreateModel(
            name='MembershipDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('subscription_status', models.CharField(choices=[('Not Subscribed', 'Not Subscribed'), ('Subscribed', 'Subscribed'), ('Cancelled', 'Cancelled')], default='Not Subscribed', max_length=20)),
                ('subscription_end_date', models.DateField(blank=True, null=True)),
                ('next_subscription_plan', models.CharField(choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly'), ('None', 'None')], default='None', max_length=50)),
                ('account_status', models.CharField(default='active', max_length=10)),
                ('membership_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.MembershipPlan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Membership Details',
            },
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_email', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=500)),
                ('site', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.Websites')),
            ],
            options={
                'verbose_name_plural': 'Mail',
            },
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_marked_read', models.BooleanField(default=False)),
                ('fullname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=256)),
                ('street_address', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('zip', models.CharField(blank=True, max_length=5, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('asking_price', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('is_home_listed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.ListingOptions')),
                ('site', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.Websites')),
                ('status', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.Status')),
                ('what_are_you_looking_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.BuyerOptions')),
            ],
            options={
                'verbose_name_plural': 'Lead',
            },
        ),
        migrations.CreateModel(
            name='ExtraPropertyInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(max_length=50)),
                ('min_bedrooms', models.IntegerField(default=0)),
                ('max_bedrooms', models.IntegerField(default=0)),
                ('style_of_property', models.CharField(max_length=50)),
                ('min_bathrooms', models.IntegerField(default=0)),
                ('max_bathrooms', models.IntegerField(default=0)),
                ('min_price', models.FloatField(blank=True, default=0, null=True)),
                ('max_price', models.FloatField(blank=True, default=0, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('zip', models.CharField(blank=True, max_length=5, null=True)),
                ('phone', models.CharField(blank=True, max_length=256, null=True)),
                ('sms_notifications', models.BooleanField(default=False)),
                ('voice_notifications', models.BooleanField(default=False)),
                ('buying_plan', models.CharField(max_length=100)),
                ('buying_reason', models.CharField(max_length=100)),
                ('rent_or_own', models.CharField(max_length=5)),
                ('sell_before_moving', models.CharField(max_length=4)),
                ('source', models.CharField(max_length=50)),
                ('finance', models.CharField(max_length=100)),
                ('pre_qualified', models.CharField(max_length=100)),
                ('amount', models.FloatField(blank=True, default=0, null=True)),
                ('down_payment', models.FloatField(blank=True, default=0, null=True)),
                ('lead', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='xsiteApp.Leads')),
            ],
            options={
                'verbose_name_plural': 'Extra Property Information',
            },
        ),
    ]
