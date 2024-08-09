from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Cash_Buyer(models.Model):
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

    ASSET_CLASS = (
        ("Single Family Residential", "Single Family Residential"),
        ("Multi Family", "Multi Family"),
        ("Vacant Lots", "Vacant Lots"),
        ("Manufactured Home", "Manufactured Home"),
        ("Townhomes/ Condos", "Townhomes/ Condos")
    )

    INVESTOR_TYPE = (
        ("Rehabber", "Rehabber"),
        ("Developer", "Developer"),
        ("Builder", "Builder"),
        ("Buy/Hold", "Buy/Hold"),
        ("Realtor", "Realtor"),
        ("Wholesaler", "Wholesaler"),
        ("Private Buyer", "Private Buyer")
    )

    PRICE_POINT = (
        ("No Limit", "No Limit"),
        ("< $50,000", "< $50,000"),
        (" $50,001 - $100,000", "$50,001 - $100,000 "),
        (" $100,001 - $150,000", "$100,001 - $150,000 "),
        (" $150,001 - $200,000", "$150,001 - $200,000 "),
        (" $200,001 - $250,000", "$200,001 - $250,000 "),
        (" $250,001 - $300,000", "$250,001 - $300,000 "),
        (" $300,001 - $350,000", "$300,001 - $350,000 "),
        (" $350,001 - $400,000", "$350,001 - $400,000 "),
        (" $400,001 - $500,000", "$400,001 - $500,000 "),
        (" $500,001 - $750,000", "$500,001 - $750,000 "),
        (" $750,001 - $ 1Million", "$750,001 - $ 1Million"),
        ("> 1Million", "> 1Million"),
    )

    ANNUAL_VOLUME = (
        ("1-5(Mom & Pop Investor)", "1-5(Mom & Pop Investor)"),
        ("6-10", "6-10"),
        ("11-15", "11-15"),
        ("16-20", "16-20"),
        ("20-30", "20-30"),
        ("31-50", "31-50"),
        ("51-75", "51-75"),
        ("76-100", "76-100"),
        ("100+ (Professional)", "100+ (Professional)")
    )

    FINANCING_TYPE = (
        ("Cash Purchase", "Cash Purchase"),
        ("Hard Money", "Hard Money"),
        ("Private Capital", "Private Capital"),
        ("IRA", "IRA"),
        ("Other", "Other")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=150, blank=True, null=True)
    entity_name = models.CharField(max_length=150, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+1999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    realtor_name = models.CharField(max_length=150, null=True, blank=True)
    VIP = models.BooleanField(default=True, null=True, blank=True)
    needs_updating = models.BooleanField(default=True, null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    target_area = models.CharField(max_length=255, choices=STATE_CHOICES, null=True, blank=True)
    asset_class = models.CharField(max_length=255, choices=ASSET_CLASS, null=True, blank=True)
    notes = models.TextField(max_length=2000, null=True, blank=True)
    type_of_investor = models.CharField(max_length=100, null=True, blank=True)
    price_point = models.CharField(max_length=255, choices=PRICE_POINT, null=True, blank=True)
    minimum_return_requirement = models.CharField(max_length=255, null=True, blank=True)
    annual_volume = models.CharField(max_length=255, choices=ANNUAL_VOLUME, null=True, blank=True)
    financing_type = models.CharField(max_length=255, choices=FINANCING_TYPE, null=True, blank=True)
    additional_notes = models.TextField(max_length=2000, null=True, blank=True)
    office_address = models.CharField(max_length=255, null=True, blank=True)
    Search_query_toi = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='cash_buyer_files/', null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True)

    def str_to_list(self):
        print("in model func")
        self.type_of_investor.split(',')
        return self.type_of_investor.split(',')

    def __str__(self):
       return self.buyer_name
