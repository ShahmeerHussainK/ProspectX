from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from xforce_transactions.models import Transaction

from cash_buyer.models import Cash_Buyer


class sales(models.Model):
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
    Showing = (
        ('Showing Complete', 'Showing Complete'),
        ('No Showing Needed', 'No Showing Needed'),

    )
    Email = (
        ('no value', 'no value'),
        ('Send Email Content Above', 'Send Email Content Above'),
        ('Best and Highest', 'Best and Highest'),
        ('Pending Property', 'Pending Property'),
        ('Sold Property', 'Sold Property'),
    )
    Set_showing = (
        ('no value', 'no value'),
        ('Offer Accepted(Back to Transaction)', 'Offer Accepted(Back to Transaction)'),
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    deals = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    disposition_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disposition_manager", null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS, default='no value', blank=True, null=True)
    deadline_to_assign = models.DateTimeField(blank=True, null=True)
    email_blast = models.BooleanField(default=False)
    facebook_groups = models.BooleanField(default=False)
    call_vips = models.BooleanField(default=False)
    mls_cash_buyer = models.BooleanField(default=False)
    text_vip_buyers = models.BooleanField(default=False)
    marketing_price = models.IntegerField(blank=True, null=True)
    buy_now_price = models.IntegerField(null=True, blank=True)
    mls_price = models.CharField(max_length=255, blank=True, null=True)
    comps = models.TextField(max_length=2000, blank=True, null=True)
    arv = models.IntegerField(blank=True, null=True)
    lockbox_acess_info = models.TextField(max_length=2000, blank=True, null=True)
    website_pictures = models.CharField(max_length=250, null=True, blank=True)
    current_interest = models.ForeignKey(Cash_Buyer, on_delete=models.CASCADE, null=True, blank=True, related_name="current_interest")
    showing_date = models.DateTimeField(blank=True, null=True)
    set_showing = models.BooleanField(default=False)
    notes = models.TextField(max_length=2000, blank=True, null=True)
    attending_showing = models.ForeignKey(Cash_Buyer, on_delete=models.CASCADE, null=True, blank=True, related_name="attending_showing")
    showing = models.CharField(max_length=255, choices=Showing, blank=True, null=True)
    accepted_buyers = models.ForeignKey(Cash_Buyer, on_delete=models.CASCADE, null=True, blank=True, related_name="accepted_buyer")
    final_gross_sales_price = models.IntegerField(blank=True, null=True)
    buyer_entity_name = models.CharField(max_length=500, null=True, blank=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    finders_fee = models.IntegerField(blank=True, null=True)
    assigned = models.CharField(max_length=255, blank=True, null=True, choices=Set_showing)
    email_subject = models.CharField(max_length=500, null=True, blank=True)
    email_content = models.TextField(max_length=2000, null=True, blank=True)
    send_email = models.CharField(max_length=255, choices=Email, default='no value', blank=True, null=True)
    marketing_done = models.BooleanField(default=False)
    files = models.FileField(upload_to='sales/', default=None, null=True, blank=True)
    transactions = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='transaction', blank=True, null=True)
    from_transaction = models.BooleanField(default=False)


class sales_offer(models.Model):
    PHONE_CHOICES = (("Mobile", "Mobile"), ("Work", "Work"), ("Home", "Home"), ("Main", "Main"),
                     ("Work Fax", "Work Fax"), ("Private Fax", "Private Fax"), ("Other", "Other"))
    EMAIL_CHOICES = (("Work", "Work"), ("Home", "Home"), ("Other", "Other"))
    Sold_email_sent = (

        ('Yes', 'Yes'),
    )
    Pending_email_sent = (

        ('Yes', 'Yes'),
    )
    Counter_email_sent = (

        ('Yes', 'Yes'),
    )
    Add_cash_buyer = (

        ('Add Cash Buyer', 'Add Cash Buyer'),
    )
    Types_of_investor = (
        ('Rahabber', 'Rahabber'),
        ('Developer', 'Developer'),
        ('Builder', 'Builder'),
        ('Buy/Hold', 'Buy/Hold'),
        ('Realtor', 'Realtor'),
        ('Wholesaler', 'Wholesaler'),
        ('Private Buyer', 'Private Buyer'),
    )
    Offer_accepted = (

        ('Yes', 'Yes'),
    )
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(sales, on_delete=models.CASCADE, related_name="property")
    llc_purchase_name = models.CharField(max_length=75)
    full_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=254)
    email_type = models.CharField(max_length=20, choices=EMAIL_CHOICES, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    phone_type = models.CharField(max_length=20, choices=PHONE_CHOICES, null=True, blank=True)

    close_date = models.DateTimeField()
    offer_amount = models.IntegerField()
    offer_accepted = models.BooleanField(default=False)
    add_cash_buyer = models.BooleanField(default=False)
    additional_details = models.TextField(max_length=2000,blank=True, null=True)
    submission_date = models.DateTimeField(null=True,blank=True)
    investor_type = models.CharField(max_length=10, choices=Types_of_investor, blank=True, null=True)
    targeted_area = models.CharField(max_length=20, choices=STATE_CHOICES, blank=True, null=True)
    date = models.DateTimeField(null=True,blank=True)
    counter_email_offer_sent = models.BooleanField(default=False)
    pending_email_sent = models.BooleanField(default=False)
    sold_email_sent = models.BooleanField(default=False)
    file = models.FileField(upload_to='sales_offer/', default=None, null=True, blank=True)
    earnest_money_deposit = models.IntegerField()
    via_webform = models.CharField(max_length=6, default='no')

