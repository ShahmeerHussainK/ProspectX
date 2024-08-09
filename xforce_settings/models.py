from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class Company(models.Model):
    STATE_CHOICES = (("Alabama", "Alabama"), ("Alaska", "Alaska"), ("Arizona", "Arizona"), ("Arkansas", "Arkansas"),
                     ("California", "California"), ("Colorado", "Colorado"), ("Connecticut", "Connecticut"),
                     ("Delaware", "Delaware"),
                     ("Florida", "Florida"), ("Georgia", "Georgia"), ("Hawaii", "Hawaii"), ("Idaho", "Idaho"),
                     ("Illinois", "Illinois"),
                     ("Indiana", "Indiana"), ("Iowa", "Iowa"), ("Kansas", "Kansas"), ("Kentucky", "Kentucky"),
                     ("Louisiana", "Louisiana"), ("Maine", "Maine"), ("Maryland", "Maryland"),
                     ("Massachusetts", "Massachusetts"),
                     ("Michigan", "Michigan"), ("Minnesota", "Minnesota"), ("Mississippi", "Mississippi"),
                     ("Missouri", "Missouri"),
                     ("Montana", "Montana"), ("Nebraska", "Nebraska"), ("Nevada", "Nevada"),
                     ("New Hampshire", "New Hampshire"),
                     ("New Jersey", "New Jersey"), ("New Mexico", "New Mexico"), ("New York", "New York"),
                     ("North Carolina", "North Carolina"), ("North Dakota", "North Dakota"), ("Ohio", "Ohio"),
                     ("Oklahoma", "Oklahoma"),
                     ("Oregon", "Oregon"), ("Pennsylvania", "Pennsylvania"), ("Rhode Island", "Rhode Island"),
                     ("South Carolina", "South Carolina"), ("South Dakota", "South Dakota"), ("Tennessee", "Tennessee"),
                     ("Texas", "Texas"), ("Utah", "Utah"), ("Vermont", "Vermont"), ("Virginia", "Virginia"),
                     ("Washington", "Washington"), ("West Virginia", "West Virginia"), ("Wisconsin", "Wisconsin"),
                     ("Wyoming", "Wyoming"))

    title = models.CharField(max_length=150, unique=True)
    escrow_officer = models.CharField(max_length=150)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(max_length=200)
    status = models.BooleanField(default=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    address = models.CharField(max_length=255)
    company_img = models.FileField(upload_to='company/', default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class XforceSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    setting_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    entity_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    disposition_company_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    email_subject_for_comment = models.CharField(max_length=255, null=True, blank=True, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+1999999999'. Up to 15 digits allowed.")
    sms_phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True, default=None)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True, default=None)
    email = models.EmailField(max_length=100, null=True, blank=True, default=None)
    website = models.CharField(max_length=255, null=True, blank=True, default=None)
    logo = models.FileField(upload_to="settings_logo/", null=True, blank=True, default=None)
    seller_missed_call_text = models.TextField(max_length=500, null=True, blank=True, default=None)
    missed_call_trigger = models.BooleanField(default=False, null=True, blank=True)
    best_and_highest_email_template = models.CharField(max_length=255, null=True, blank=True, default=None)
    pending_property_email_template = models.CharField(max_length=255, null=True, blank=True, default=None)
    sold_property_email_template = models.CharField(max_length=255, null=True, blank=True, default=None)
    setting_file = models.FileField(upload_to="xforce_settings_files/", null=True, blank=True, default=None)


class ContractTemplates(models.Model):
    TYPE = (
        ("Purchase", "Purchase"),
        ("Assignment", "Assignment")
    )
    setting = models.ForeignKey(XforceSettings, related_name='contract', on_delete=models.CASCADE, null=True,
                                blank=True, default=None)
    contract_type = models.CharField(max_length=25, choices=TYPE, null=True, blank=True, default=None)
    contract_email_subject = models.CharField(max_length=255, null=True, blank=True, default=None)
    contract_email_body = models.CharField(max_length=255, null=True, blank=True, default=None)
    contract_text = models.TextField(max_length=3000, null=True, blank=True, default=None)


class Callrail(models.Model):
    setting = models.ForeignKey(XforceSettings, related_name='callrail', on_delete=models.CASCADE, null=True,
                                blank=True, default=None)
    api = models.CharField(max_length=255, null=True, blank=True, default=None)
    account_number = models.IntegerField()
    company_id = models.CharField(max_length=255, null=True, blank=True, default=None)


class E_Signature_setting(models.Model):
    setting = models.ForeignKey(XforceSettings, related_name='e_signature', on_delete=models.CASCADE, null=True,
                                blank=True, default=None)
    title = models.CharField(max_length=255, null=True, blank=True, default=None)
    message = models.CharField(max_length=255, null=True, blank=True, default=None)
    requester_name = models.EmailField(max_length=50, null=True, blank=True, default=None)
    requester_email = models.EmailField(max_length=50, null=True, blank=True, default=None)
    reminders = models.CharField(max_length=255, null=True, blank=True, default=None)


class Title_Company_Actions(models.Model):
    setting = models.ForeignKey(XforceSettings, related_name='title_company', on_delete=models.CASCADE, null=True,
                                blank=True, default=None)
    email_subject = models.CharField(max_length=255, null=True, blank=True, default=None)
    email_body = models.CharField(max_length=255, null=True, blank=True, default=None)


class CallAndOfferAttempts(models.Model):
    Types = (
        ("1st Call Attempt SMS", "1st Call Attempt SMS"),
        ("2nd Call Attempt SMS", "2nd Call Attempt SMS"),
        ("3rd call Attempt SMS", "3rd call Attempt SMS"),
        ("4th call Attempt SMS", "4th call Attempt SMS"),
        ("Final call Attempt SMS", "Final call Attempt SMS"),
        ("After Speaking with Seller SMS", "After Speaking with Seller SMS"),
        ("1st Call Attempt Email", "1st Call Attempt Email"),
        ("2nd Call Attempt Email", "2nd Call Attempt Email"),
        ("3rd Call Attempt Email", "3rd Call Attempt Email"),
        ("4th Call Attempt Email", "4th Call Attempt Email"),
        ("Final Call Attempt Email", "Final Call Attempt Email"),
        ("After Speaking with Seller Email", "After Speaking with Seller Email"),
        ("1st Offer Attempt SMS", "1st Offer Attempt SMS"),
        ("2nd Offer Attempt SMS", "2nd Offer Attempt SMS"),
        ("3rd Offer Attempt SMS", "3rd Offer Attempt SMS"),
        ("4th Offer Attempt SMS", "4th Offer Attempt SMS"),
        ("Final Offer Made SMS", "Final Offer Made SMS"),
        ("1st Offer Attempt Email", "1st Offer Attempt Email"),
        ("2nd Offer Attempt Email", "2nd Offer Attempt Email"),
        ("3rd Offer Attempt Email", "3rd Offer Attempt Email"),
        ("4th Offer Attempt Email", "4th Offer Attempt Email"),
        ("Final Offer Made Email", "Final Offer Made Email")
    )
    Action = (
        ("SMS Only", "SMS Only"),
        ("Email Only", "Email Only"),
        ("Send Both", "Send Both")
    )
    setting = models.ForeignKey(XforceSettings, related_name='call_and_offers', on_delete=models.CASCADE, null=True,
                                blank=True, default=None)
    callandofferattempts_type = models.CharField(max_length=25, choices=Types, null=True, blank=True, default=None)
    callandofferattempts_sms = models.CharField(max_length=255, null=True, blank=True, default=None)
    callandofferattempts_subject = models.CharField(max_length=255, null=True, blank=True, default=None)
    callandofferattempts_body = models.CharField(max_length=255, null=True, blank=True, default=None)
    callandofferattempts_action = models.CharField(max_length=50, choices=Action, null=True, blank=True, default=None)
