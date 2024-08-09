from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import validate_email
from marketing_machine.models import MarketingCampaign, MajorMarket
from xforce_settings.models import Company


class FollowUp(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class SellerLead(models.Model):
    STAGE_OF_CONTACT = (
        ("No Attempt", "No Attempt"),
        ("Call Attempt 1", "Call Attempt 1"),
        ("Call Attempt 2", "Call Attempt 2"),
        ("Call Attempt 3", "Call Attempt 3"),
        ("Call Attempt 4", "Call Attempt 4"),
        ("Final Attempt", "Final Attempt"),
        ("CONTACTED", "CONTACTED")
    )
    LEAD_STATUS = (
        ("New Untouched", "New Untouched"),
        ("Discovery", "Discovery"),
        ("**Interested--> Updated Offer Status", "**Interested--> Updated Offer Status"),
        ("Not Interested / Follow Up", "Not Interested / Follow Up"),
        ("DO NOT CONTACT", "DO NOT CONTACT"),
        ("Solicitation Call / Wrong # / Other", "Solicitation Call / Wrong # / Other"),
        ("Wants Retails", "Wants Retails")

    )
    TEMPERATURE = (
        ("No Value", "No Value"),
        ("Cold", "Cold"),
        ("Hot", "Hot"),
        ("Warm", "Warm")
    )
    FOLLOW_UP_IN = (
        ("No Value", "No Value"),
        ("1 Day", "1 Day"),
        ("2 Days", "2 Days"),
        ("1 Week", "1 Week"),
        ("2 Weeks", "2 Weeks"),
        ("3 Weeks", "3 Weeks"),
        ("1 Month", "1 Month"),
        ("3 Months", "3 Months"),
        ("6 Months", "6 Months"),
        ("1 Year", "1 Year")
    )
    OCCUPANCY = (
        ("No Value", "No Value"),
        ("Vacant", "Vacant"),
        ("Owner Occupied", "Owner Occupied"),
        ("Tenants", "Tenants")
    )
    MADE_OFFER = (
        ("No Value", "No Value"),
        ("Make Offer", "Make Offer"),
        ("Make Attempt 1", "Make Attempt 1"),
        ("Make Attempt 2", "Make Attempt 2"),
        ("Make Attempt 3", "Make Attempt 3"),
        ("Make Attempt 4", "Make Attempt 4"),
        ("Made Offer", "Made Offer"),
        ("Offer Not Made", "Offer Not Made")
    )
    OFFER_STATUS = (
        ("No Value", "No Value"),
        ("Not Given", "Not Given"),
        ("Accepted", "Accepted"),
        ("Not Accepted", "Not Accepted"),
        ("Negotiating", "Negotiating"),
    )
    CLOSING_COSTS = (
        ("No Value", "No Value"),
        ("Each Party to Pay his or her Own Costs", "Each Party to Pay his or her Own Costs"),
        ("Paid in Full By Buyer", "Paid in Full By Buyer")
    )
    CONTACT_DELIVERY = (
        ("No Value", "No Value"),
        ("E Signature", "E Signature"),
        ("Email", "Email"),
        ("In Person", "In Person")
    )
    CONTRACT_ACTION = (
        ("No Value", "No Value"),
        ("Generate Contract", "Generate Contract"),
        ("Email Contract", "Email Contract"),
        ("E Signature", "E Signature"),
    )
    LEAD_SOURCE = (
        ("No Value", "No Value"),
        ("Telemarketing", "Telemarketing"),
        ("Direct Mail", "Direct Mail"),
        ("PPC", "PPC"),
        ("Social", "Social"),
        ("Organic", "Organic"),
        ("Generic", "Generic"),
        ("Referral", "Referral"),
        ("Voice Broadcast", "Voice Broadcast"),
        ("SMS", "SMS"),
        ("RVM", "RVM"),
        ("JV", "JV"),
        ("Bandit Signs", "Bandit Signs"),
        ("Expired Listing", "Expired Listing")
    )
    DEAL_STATUS = (
        ("No Value", "No Value"),
        ("Pending", "Pending"),
        ("Marketing", "Marketing"),
        ("Assigned", "Assigned"),
        ("$$$Closed$$$", "$$$Closed$$$"),
        ("Dead", "Dead")
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='leads_user')
    seller_name = models.CharField(max_length=150)
    lead_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='manager')
    tracker = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number up to 15 digits allowed.")
    seller_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    seller_email = models.EmailField(max_length=75, validators=[validate_email,], blank=True, null=True)
    # make property, seller_name field required
    property_address_map = models.TextField(max_length=200, blank=True, null=True)
    mailing_address = models.CharField(max_length=200, null=True, blank=True)
    total_view = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    outbound_call_lead = models.BooleanField(default=False)
    stage_of_contact = models.CharField(max_length=50, null=True, choices=STAGE_OF_CONTACT,blank=True)
    call_attempt = models.BooleanField(default=False)
    lead_status = models.CharField(max_length=50, null=True, choices=LEAD_STATUS,blank=True)
    temperature = models.CharField(max_length=50, null=True, choices=TEMPERATURE,blank=True)
    follow_up_in = models.CharField(max_length=50, null=True, choices=FOLLOW_UP_IN,blank=True)
    follow_up_specific_date = models.DateTimeField(null=True,blank=True)
    set_specific_follow_up = models.BooleanField(default=False)
    need_skip = models.BooleanField(default=False)
    info = models.TextField(max_length=2000, blank=True, null=True)
    nurture_campaign = models.ForeignKey(FollowUp, on_delete=models.CASCADE, null=True, related_name='follow_up',blank=True)
    nurture_campaign_action = models.BooleanField(default=False)
    occupancy = models.CharField(max_length=20, null=True, choices=OCCUPANCY)
    details = models.TextField(max_length=2000, blank=True, null=True)
    mortgage_amount = models.IntegerField(blank=True, null=True)
    asking_price = models.IntegerField(blank=True, null=True)
    hoa = models.BooleanField(default=False)
    best_call_back_time = models.DateTimeField(blank=True, null=True)
    miscellaneous_notes = models.TextField(max_length=2000, blank=True, null=True)
    get_data_from_total_view = models.BooleanField(default=False)
    sqft = models.IntegerField(blank=True, null=True)
    lot_size = models.IntegerField(blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True, default=None)
    year_built = models.IntegerField(blank=True, null=True)
    tax_assessment = models.IntegerField(blank=True, null=True)
    year_assessed = models.IntegerField(blank=True, null=True)
    property_value = models.IntegerField(blank=True, null=True)
    potential_offer = models.IntegerField(blank=True, null=True)
    arv = models.CharField(max_length=100, blank=True, null=True)
    mao = models.CharField(max_length=100, blank=True, null=True)
    mao_details = models.TextField(max_length=2000, blank=True, null=True)
    offer_range = models.CharField(max_length=50, blank=True, null=True)
    made_offer = models.CharField(max_length=20, choices=MADE_OFFER, null=True,blank=True)
    offer_attempt = models.BooleanField(default=False)
    offer_status = models.CharField(max_length=255, choices=OFFER_STATUS, null=True,blank=True)
    app_date = models.DateTimeField(blank=True, null=True)
    set_appointment = models.BooleanField(blank=True, null=True)
    note_for_agent = models.TextField(max_length=2000, blank=True, null=True)
    canceled_appointment = models.BooleanField(default=False, blank=True, null=True)
    contract_offer_amt = models.IntegerField(default=0)
    title_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='company_for_seller',blank=True)
    emd = models.IntegerField(default=0)
    closing_costs = models.CharField(max_length=50, blank=True, null=True, choices=CLOSING_COSTS)
    closing_no_day = models.IntegerField(blank=True, null=True)
    to_vacate_on = models.CharField(max_length=100, blank=True, null=True)
    other_terms = models.TextField(max_length=2000, blank=True, null=True)
    deal_details = models.TextField(max_length=2000, blank=True, null=True)
    deal_action = models.BooleanField(default=False, blank=True, null=True)
    contract_delivery = models.CharField(max_length=20, null=True, choices=CONTACT_DELIVERY, blank=True)
    contract_action = models.CharField(max_length=20, null=True, choices=CONTRACT_ACTION, blank=True)
    lead_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='lead_by', blank=True)
    call_log = models.CharField(max_length=500, blank=True, null=True)
    sms_log = models.CharField(max_length=500, blank=True, null=True)
    lead_source = models.CharField(max_length=20, blank=True, null=True, choices=LEAD_SOURCE)
    detailed_source = models.TextField(max_length=500, blank=True, null=True)
    detailed_source = models.TextField(max_length=2000, blank=True, null=True)
    deal_status = models.CharField(max_length=20, blank=True, null=True, choices=DEAL_STATUS)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='campaign_for_seller_lead', null=True, blank=True)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='campaign_for_seller_lead', null=True, blank=True)
    major_market = models.ForeignKey(MajorMarket, on_delete=models.CASCADE, related_name='major_market', null=True, blank=True)
    lead_file = models.FileField(upload_to='seller_lead_files/', null=True, blank=True)
    via_webform = models.CharField(max_length=6, default='no')

    def __str__(self):
        return self.seller_name


class RoundRobinCounter(models.Model):
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE)
    lead_task_cc = models.IntegerField(default=0)
    transaction_task_cc = models.IntegerField(default=0)
    sale_task_cc = models.IntegerField(default=0)

    def __str__(self):
        return self.admin_user.email
