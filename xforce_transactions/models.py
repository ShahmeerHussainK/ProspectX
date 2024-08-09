from django.contrib.auth.models import User
from django.db import models

from cash_buyer.models import Cash_Buyer
from marketing_machine.models import MarketingCampaign
from xforce_seller_leads.models import SellerLead
from xforce_settings.models import Company


class Transaction(models.Model):
    STATUS = (
        ('No Value', 'No Value'),
        ('Pending', 'Pending'),
        ('Marketing', 'Marketing'),
        ('Follow up / Offer', 'Follow up / Offer'),
        ('Schedule and Showing', 'Schedule and Showing'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Assigned', 'Assigned'),
        ('Closed', 'Closed'),
        ('Dead', 'Dead'),
        ('Renegotiate!', 'Renegotiate!')
    )
    POTENTIAL = (
        ('No Value', 'No Value'),
        ('Wholesale', 'Wholesale'),
        ('Asset', 'Asset'),
        ('Fix and Flip', 'Fix and Flip')
    )
    PENDING_STAGE = (
        ('No Value', 'No Value'),
        ('1-Receive Contract', '1-Receive Contract'),
        ('2-Contract Send To Title Company', '2-Contract Send To Title Company'),
        ('3-EMD Wired', '3-EMD Wired')
    )
    TITLE_ACTIONS = (
        ('No Value', 'No Value'),
        ('Email Contract To Title', 'Email Contract To Title'),
        ('Email Wire Number To Title', 'Email Wire Number To Title')
    )
    MARKETING_STAGE = (
        ('No Value', 'No Value'),
        ('Not Started', 'Not Started'),
        ('Pending', 'Pending'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Done! Buyer Found', 'Done! Buyer Found'),
        ('Not Applicable', 'Not Applicable')
    )
    SHOWING = (
        ('No Value', 'No Value'),
        ('Showing Complete', 'Showing Complete'),
        ('Not Showing Needed', 'Not Showing Needed')
    )
    ASSIGNED_STAGE = (
        ('No Value', 'No Value'),
        ('1- Assignment Send', '1- Assignment Send'),
        ('2- Assignment Received', '2- Assignment Received'),
        ('3- Assignment Send To Title Company', '3- Assignment Send To Title Company'),
        ('4- EMD Deposit', '4- EMD Deposit'),
        ('5- Set Closing Time', '5- Set Closing Time')
    )
    CONTRACT_ACTION = (
        ('No Value', 'No Value'),
        ('Generate Assignment Contract', 'Generate Assignment Contract'),
        ('Email Assignment Contract', 'Email Assignment Contract'),
        ('Email Assignment Contract To Title', 'Email Assignment Contract To Title'),
        ('Send Assignment Contract via esignature', 'Send Assignment Contract via esignature')
    )
    LEAD_SOURCE = (
        ('No Value', 'No Value'),
        ('Telemarketing', 'Telemarketing'),
        ('Direct Mail', 'Direct Mail'),
        ('PPC', 'PPC'),
        ('Social', 'Social'),
        ('Organic', 'Organic'),
        ('Generic', 'Generic'),
        ('Referral', 'Referral'),
        ('Voice Broadcast', 'Voice Broadcast'),
        ('RVM', 'RVM'),
        ('SMS', 'SMS'),
        ('JV', 'JV'),
        ('Bandit Signs', 'Bandit Signs')

    )
    CONTRACT_DELIVERY = (
        ('No Value', 'No Value'),
        ('eSignature', 'eSignature'),
        ('Email', 'Email'),
        ('In Person', 'In Person')
    )
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    property_address = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS, blank=True)
    potential = models.CharField(max_length=50, choices=POTENTIAL,null=True, blank=True)
    wait_for_refund = models.BooleanField(default=False, null=True, blank=True)
    seller = models.ForeignKey(SellerLead, on_delete=models.CASCADE, null=True, related_name='seller', blank=True)
    transaction_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                            related_name='manager_for_transaction')
    pending_stage = models.CharField(max_length=50, null=True, choices=PENDING_STAGE, blank=True)
    hoa = models.BooleanField(default=False, null=True, blank=True)
    preliminary_received = models.BooleanField(default=False, null=True, blank=True)
    reason_for_pending = models.TextField(max_length=2000, null=True, blank=True)
    purchase_contract_ratification_date_start = models.DateTimeField(null=True, blank=True)
    contract_date_start = models.DateTimeField(null=True, blank=True)
    contract_price = models.IntegerField(null=True, blank=True)
    original_purchase_emd_amount = models.IntegerField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='company_for_transaction')
    wire_confirmation_number = models.TextField(max_length=500, null=True, blank=True)
    title_actions = models.CharField(max_length=50, null=True, choices=TITLE_ACTIONS, blank=True)
    marketing_Stage = models.CharField(max_length=50, null=True, choices=MARKETING_STAGE, blank=True)
    marketing_needs = models.BooleanField(default=False, null=True, blank=True)
    marketing_price = models.IntegerField(blank=True, default=0)
    website_picture = models.CharField(max_length=255, null=True, blank=True)
    showing_date_start = models.DateTimeField(null=True, blank=True)
    deadline_to_accept_offer_start = models.DateTimeField(null=True, blank=True)
    showing = models.CharField(max_length=50, null=True, choices=SHOWING, blank=True)
    pre_assigned_status = models.BooleanField(default=False, null=True, blank=True)
    assignment_stage = models.CharField(max_length=50, null=True, choices=ASSIGNED_STAGE, blank=True)
    final_gross_sales_price = models.IntegerField(default=0)
    closing_date = models.DateField(null=True, blank=True)
    finder_fee = models.IntegerField(null=True, blank=True)
    buyer_contact_info = models.ForeignKey(Cash_Buyer, on_delete=models.CASCADE, null=True, related_name='cash_buyer',
                                           blank=True)
    buyer_entity_name = models.CharField(max_length=25, null=True, blank=True)
    assignment_emd_amount = models.IntegerField(null=True, blank=True)
    non_refundable = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    emd_date_start = models.DateTimeField(null=True, blank=True)
    assignment_fee = models.IntegerField(null=True, blank=True)
    other_terms = models.TextField(max_length=2000, null=True, blank=True)
    contract_action = models.CharField(max_length=50, null=True, choices=CONTRACT_ACTION, blank=True)
    notes = models.TextField(max_length=2000, null=True, blank=True)
    actual_close_date = models.DateField(null=True, blank=True)
    misc_expenses = models.IntegerField(null=True, blank=True)
    explanation_of_misc_expense = models.TextField(max_length=2000, null=True, blank=True)
    actual_profit = models.IntegerField(null=True, blank=True)
    closing_stage = models.BooleanField(default=False, null=True, blank=True)
    lead_source = models.CharField(max_length=50, null=True, choices=LEAD_SOURCE, blank=True)
    contract_delivery = models.CharField(max_length=50, null=True, choices=CONTRACT_DELIVERY, blank=True)
    detailed_source = models.TextField(max_length=500, null=True, blank=True)
    campaigns = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, null=True,blank=True,
                                  related_name='campaign_for_transaction')
    acq_sys_ref = models.CharField(max_length=100, null=True, blank=True)
    dispo_sys_ref = models.CharField(max_length=100, null=True, blank=True)
    transaction_file = models.FileField(upload_to='Transactions_Files/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    from_lead = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.property_address
