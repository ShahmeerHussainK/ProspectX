# Generated by Django 2.2.7 on 2020-04-07 13:22

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
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_title', models.CharField(max_length=100)),
                ('block_width', models.CharField(max_length=100)),
                ('block_content', models.CharField(max_length=1000)),
                ('block_image', models.CharField(default=1, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'DashBoard',
            },
        ),
        migrations.CreateModel(
            name='EmailContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_content', models.CharField(max_length=1000, null=True)),
            ],
            options={
                'verbose_name_plural': 'Email Content',
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('random_password', models.BooleanField(default=True)),
                ('activation_email', models.BooleanField(default=True)),
                ('marketing_plan', models.BooleanField(default=True)),
                ('skip_trace', models.BooleanField(default=True)),
                ('list_management', models.BooleanField(default=True)),
                ('access_import_log', models.BooleanField(default=True)),
                ('access_export_log', models.BooleanField(default=True)),
                ('access_tag_log', models.BooleanField(default=False)),
                ('access_xsite', models.BooleanField(default=True)),
                ('access_xforce', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Permission',
            },
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(choices=[('Super User', 'Super User'), ('Admin User', 'Admin User'), ('Sub User', 'Sub User')], default='Super User', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Role',
            },
        ),
        migrations.CreateModel(
            name='WelcomeEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_from', models.CharField(max_length=250)),
                ('email_content', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'WelcomeEmail',
            },
        ),
        migrations.CreateModel(
            name='UserStripeDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_token', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('subscription_id', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('subscription_status', models.CharField(choices=[('Subscribed', 'Subscribed'), ('Cancelled', 'Cancelled')], default='Subscribed', max_length=20)),
                ('subscription_cancel_date', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('customer_id', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('plan', models.CharField(choices=[('None', 'None'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='None', max_length=20)),
                ('subscription_started', models.BooleanField(default=False)),
                ('cancelled_before_starting', models.BooleanField(default=False)),
                ('trial_date', models.IntegerField(blank=True, default=0, null=True)),
                ('start_date', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserStripeDetail',
            },
        ),
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prospect_count', models.IntegerField(blank=True, default=0, null=True)),
                ('opted_out_count', models.IntegerField(blank=True, default=0, null=True)),
                ('vacant_count', models.IntegerField(blank=True, default=0, null=True)),
                ('absentee_count', models.IntegerField(blank=True, default=0, null=True)),
                ('total_users_count', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Stat',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('zip', models.CharField(blank=True, max_length=5, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('cell_phone', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('landline_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('profile_image', models.FileField(blank=True, default='user_images/default_image.jpg', null=True, upload_to='user_images/')),
                ('status', models.CharField(default='active', max_length=10)),
                ('skiptrace_price', models.DecimalField(decimal_places=2, default=0.85, max_digits=8)),
                ('bulk_skiptrace_price', models.DecimalField(decimal_places=2, default=0.15, max_digits=8)),
                ('email_verified', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
                ('permissions', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Permission_Object', to='user.Permissions')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserProfile',
            },
        ),
        migrations.CreateModel(
            name='PaymentInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('invoice_pdf', models.FileField(blank=True, default=None, null=True, upload_to='invoices/')),
                ('customer_id', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('package', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('status', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'PaymentInvoice',
            },
        ),
    ]
