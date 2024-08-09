from django.db import models
from django.contrib.auth.models import User
import datetime

status_choices = (
    ("Uploaded", "Uploaded"),
    ("Pending", "Pending")
)


class SkipTraceFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=256, null=True, blank=False)
    status = models.CharField(max_length=50, choices=status_choices, default='Pending')
    total_records = models.CharField(max_length=50, null=True, blank=True, default='0')
    existing_matches = models.CharField(max_length=50, null=True, blank=True, default='0')
    existing_match_savings = models.CharField(max_length=50, null=True, blank=True, default='0')
    total_hits = models.CharField(max_length=50, null=True, blank=True, default='0')
    hits_percentage = models.CharField(max_length=50, null=True, blank=True, default='0')
    total_cost = models.CharField(max_length=50, null=True, blank=True, default='0')
    sheet_name = models.CharField(max_length=256, null=True, blank=True)
    destination_fields = models.CharField(max_length=1000, null=True, blank=False)
    is_process_complete = models.BooleanField(default=False)
    existing_file = models.BooleanField(default=False)
    records_created = models.BooleanField(default=False)
    should_trace = models.BooleanField(default=False)
    fail_reason = models.CharField(max_length=200, default="-")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'SkipTraceFile'


class DestinationFields(models.Model):
    file = models.ForeignKey(SkipTraceFile, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    full_name = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    last_name = models.CharField(max_length=256, null=True, blank=True)
    property_address = models.CharField(max_length=256, null=True, blank=False)
    property_address2 = models.CharField(max_length=256, null=True, blank=True)
    property_city = models.CharField(max_length=256, null=True, blank=False)
    property_state = models.CharField(max_length=256, null=True, blank=False)
    property_zip = models.CharField(max_length=256, null=True, blank=False)
    mailing_address = models.CharField(max_length=256, null=True, blank=True)
    mailing_address2 = models.CharField(max_length=256, null=True, blank=True)
    mailing_city = models.CharField(max_length=256, null=True, blank=True)
    mailing_state = models.CharField(max_length=256, null=True, blank=True)
    mailing_zip = models.CharField(max_length=256, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    phone = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    address = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    api_response = models.TextField(null=True, blank=True)
    is_validation_complete = models.BooleanField(default=False)


class SingleSkipTrace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    full_name = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    file_name = models.CharField(max_length=1000, null=True, blank=True, default="#")
    last_name = models.CharField(max_length=256, null=True, blank=True)
    property_address = models.CharField(max_length=256, null=True, blank=False)
    property_address2 = models.CharField(max_length=256, null=True, blank=True)
    property_city = models.CharField(max_length=256, null=True, blank=False)
    property_state = models.CharField(max_length=256, null=True, blank=False)
    property_zip = models.CharField(max_length=256, null=True, blank=False)
    mailing_address = models.CharField(max_length=256, null=True, blank=True)
    mailing_address2 = models.CharField(max_length=256, null=True, blank=True)
    mailing_city = models.CharField(max_length=256, null=True, blank=True)
    mailing_state = models.CharField(max_length=256, null=True, blank=True)
    mailing_zip = models.CharField(max_length=256, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    phone = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    address = models.CharField(max_length=1000, null=True, blank=True, default=" ")
    api_response = models.TextField(null=True, blank=True)
    is_validation_complete = models.BooleanField(default=False)


class EmailTraced(models.Model):
    skiptrace = models.ForeignKey(SingleSkipTrace, on_delete=models.CASCADE, default=None)
    email = models.CharField(max_length=1000, null=True, blank=True, default=None)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'EmailTraced'


class PhoneTraced(models.Model):
    skiptrace = models.ForeignKey(SingleSkipTrace, on_delete=models.CASCADE, default=None)
    phone = models.CharField(max_length=1000, null=True, blank=True, default=None)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name_plural = 'PhoneTraced'


class AddressTraced(models.Model):
    skiptrace = models.ForeignKey(SingleSkipTrace, on_delete=models.CASCADE, default=None)
    address = models.CharField(max_length=1000, null=True, blank=True, default=None)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = 'AddressTraced'


class PrepaidBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    skiptrace_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.85)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name_plural = 'PrepaidBalance'
