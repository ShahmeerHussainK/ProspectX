from django.contrib.auth.models import User
from django.db import models


# Create your models here.
plans = (
    ('None', 'None'),
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly'),
)


class Role(models.Model):
    roles = (
        ('Super User', 'Super User'),
        ('Admin User', 'Admin User'),
        ('Sub User', 'Sub User'),
    )
    role_name = models.CharField(max_length=10, choices=roles, default='Super User')

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name_plural = 'Role'


class Permissions(models.Model):
    random_password = models.BooleanField(default=True)
    activation_email = models.BooleanField(default=True)
    marketing_plan = models.BooleanField(default=True)
    skip_trace = models.BooleanField(default=True)
    list_management = models.BooleanField(default=True)
    access_import_log = models.BooleanField(default=True)
    access_export_log = models.BooleanField(default=True)
    access_tag_log = models.BooleanField(default=False)
    access_xsite = models.BooleanField(default=True)
    access_xforce = models.BooleanField(default=True)
    lead_manager = models.BooleanField(default=False)
    transaction_manager = models.BooleanField(default=False)
    disposition_manager = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Permission'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    cell_phone = models.CharField(max_length=15, blank=True, null=True, default=None)
    landline_phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.FileField(upload_to='user_images/', default='user_images/default_image.jpg', null=True,
                                     blank=True)
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)
    permissions = models.OneToOneField(Permissions, on_delete=models.CASCADE, default=1,
                                       related_name='Permission_Object')
    status = models.CharField(max_length=10, default='active')
    plan = models.CharField(max_length=20, choices=plans, default='None')
    skiptrace_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.85)
    bulk_skiptrace_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.15)
    email_verified = models.BooleanField(default=True)
    xforce_uuid = models.CharField(null=True, blank=True, max_length=8, unique=True)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'UserProfile'


class PaymentInvoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    invoice_id = models.CharField(max_length=255, blank=True, null=True, default=None)
    invoice_pdf = models.FileField(upload_to='invoices/', default=None, null=True, blank=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True, default=None)
    amount = models.CharField(max_length=255, blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    package = models.CharField(max_length=100, blank=True, null=True, default=None)
    status = models.CharField(max_length=50, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'PaymentInvoice'


sub_status = (
    ('Subscribed', 'Subscribed'),
    ('Cancelled', 'Cancelled'),
)


class UserStripeDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    stripe_token = models.CharField(max_length=255, blank=True, null=True, default=None)
    subscription_id = models.CharField(max_length=255, blank=True, null=True, default=None)
    subscription_status = models.CharField(max_length=20, choices=sub_status, default='Subscribed')
    subscription_cancel_date = models.CharField(max_length=100, blank=True, null=True, default=None)
    customer_id = models.CharField(max_length=255, blank=True, null=True, default=None)
    plan = models.CharField(max_length=20, choices=plans, default='None')
    subscription_started = models.BooleanField(default=False)
    cancelled_before_starting = models.BooleanField(default=False)
    trial_date = models.IntegerField(blank=True, null=True, default=0)
    start_date = models.IntegerField(blank=True, null=True, default=0)
    subscription_end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'UserStripeDetail'


class Dashboard(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    block_title = models.CharField(max_length=100)
    block_width = models.CharField(max_length=100)
    block_content = models.CharField(max_length=1000)
    block_image = models.CharField(max_length=100, default=1)

    def __str__(self):
        return self.block_title

    class Meta:
        verbose_name_plural = 'DashBoard'


class WelcomeEmail(models.Model):
    email_from = models.CharField(max_length=250)
    email_content = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = 'WelcomeEmail'


class EmailContent(models.Model):
    email_content = models.CharField(max_length=1000, null=True)

    class Meta:
        verbose_name_plural = 'Email Content'


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    prospect_count = models.IntegerField(blank=True, null=True, default=0)
    opted_out_count = models.IntegerField(blank=True, null=True, default=0)
    vacant_count = models.IntegerField(blank=True, null=True, default=0)
    absentee_count = models.IntegerField(blank=True, null=True, default=0)
    total_users_count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'User Stat'


class Revenue(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

