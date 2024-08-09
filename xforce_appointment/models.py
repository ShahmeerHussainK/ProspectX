from django.contrib.auth.models import User
from django.db import models

from xforce_seller_leads.models import SellerLead
from xforce_transactions.models import Transaction


class Appointment(models.Model):
    # GOING_STATUS = (
    #     ('No Value', 'No Value'),
    #     ("Attending", "Attending"),
    #     ("Not Attending", "Not Attending"),
    #     ("Maybe Attending", "Maybe Attending")
    # )

    OFFER_ACCEPTANCE = (
        ('No Value', 'No Value'),
        ("**Not Accepted - Set Appointment", "**Not Accepted - Set Appointment"),
        ("**ACCEPTED - Set Appointment", "**ACCEPTED - Set Appointment")
    )

    APPT_STATUS = (
        ('No Value', 'No Value'),
        ("COMPLETED", "COMPLETED"),
        ("Not Kept", "Not Kept")
    )
    seller = models.ForeignKey(SellerLead, on_delete=models.CASCADE, related_name="seller_for_appointment", null=True)
    #transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transaction", null=True)
    appt_date_start = models.DateTimeField(null=True)
    property_address = models.TextField(max_length=250, null=True)
    who_set_this_appt = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="set_appt_user")
    going_on_appt = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="going_user")
    # going_status = models.CharField(max_length=20, choices=GOING_STATUS, null=True)
    offer_acceptance = models.CharField(max_length=200, choices=OFFER_ACCEPTANCE, null=True)
    appt_status = models.CharField(max_length=200, choices=APPT_STATUS, null=True)
    notes = models.TextField(max_length=2000, null=True)
    tags = models.CharField(max_length=100, null=True, blank=True)
    appt_file = models.FileField(upload_to='appointments_files/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
