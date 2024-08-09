from datetime import date

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# from user.models import sub_status
class Audience(models.Model):
    audience = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller'),
    )
    audience_name = models.CharField(max_length=10, choices=audience, default='Buyer')

    def __str__(self):
        return self.audience_name

    class Meta:
        verbose_name_plural = 'Audience'


class SiteCategory(models.Model):
    category_name = models.CharField(max_length=30)
    category_desc = models.CharField(max_length=250)
    category_icon = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Site Category'

# class Target(models.Model):
#     target = (
#         ('Renters', 'Renters'),
#         ('Investment Properties', 'Investment Properties'),
#         ('Dream Home', 'Dream Home'),
#         ('Land/Ranches/Farms', 'Land/Ranches/Farms'),
#         ('LandContracts/Leases', 'LandContracts/Leases'),
#         ('Vacation Properties', 'Vacation Properties'),
#         ('Landlord Buyer', 'Landlord Buyer'),
#         ('Generic Buyer', 'Generic Buyer'),
#
#         ('Stop Foreclosure', 'Stop Foreclosure'),
#         ('Sell Fast', 'Sell Fast'),
#         ('Home Improvement', 'Home Improvement'),
#         ('Sell Without Agent', 'Sell Without Agent'),
#         ('Commercial', 'Commercial'),
#     )
#     target_name = models.CharField(max_length=30, choices=target, default='Renters')
#
#     def __str__(self):
#         return self.target_name
#
#     class Meta:
#         verbose_name_plural = 'Target'
#
#
# class TargetAudience(models.Model):
#     target = models.ForeignKey(Target, on_delete=models.CASCADE)
#     audience = models.ForeignKey(Audience, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = 'Target Audience'


class ContentPack(models.Model):
    # target_audience = models.ForeignKey(TargetAudience, on_delete=models.CASCADE, default=1, null=True, blank=True)
    content_pack_name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to='xsite_images/website_logos/', default='xsite_images/website_logos/xsite_logo.png')
    banner_title = models.CharField(max_length=300)
    banner_button_text = models.CharField(max_length=300)
    about_us_title = models.CharField(max_length=300)
    about_us_desc = models.TextField()
    video_link = models.CharField(max_length=300)
    video_title = models.CharField(max_length=300)
    video_desc = models.TextField()
    testi_1_company_name = models.CharField(max_length=300)
    testi_1_person_name = models.CharField(max_length=300)
    testi_1_text = models.TextField()

    testi_2_company_name = models.CharField(max_length=300, null=True, blank=True)
    testi_2_person_name = models.CharField(max_length=300, null=True, blank=True)
    testi_2_text = models.TextField(null=True, blank=True)

    testi_3_company_name = models.CharField(max_length=300, null=True, blank=True)
    testi_3_person_name = models.CharField(max_length=300, null=True, blank=True)
    testi_3_text = models.TextField(null=True, blank=True)

    other_details_title = models.CharField(max_length=300)
    other_details_desc = models.TextField()

    call_to_action_text = models.CharField(max_length=300)

    def __str__(self):
        return self.content_pack_name

    class Meta:
        verbose_name_plural = 'Content Pack'


class SiteDesign(models.Model):
    template_name = models.CharField(max_length=50)
    html_head_content = models.TextField(default="nothing")
    html_body_content = models.TextField(default="nothing")
    template_url = models.CharField(max_length=200, default="xsite/site_design_templates/xsite_template_1.html")
    template_image = models.CharField(max_length=200, default="/Site_Design_imgs/Brownstone.png")
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE)
    category = models.ForeignKey(SiteCategory, on_delete=models.CASCADE, null=True)
    is_lander_page = models.BooleanField(default=True)
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE)

    def __str__(self):
        return self.template_name

    class Meta:
        verbose_name_plural = 'Site Design'


class Websites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=200)
    site_design = models.ForeignKey(SiteDesign, on_delete=models.CASCADE)
    # content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    renewal_date = models.DateField()  # , default="2020-02-06")
    domain_price = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)
    is_existing = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name_plural = 'Site'


class TemplateContent(models.Model):
    site = models.ForeignKey(Websites, on_delete=models.CASCADE, null=True, blank=True)
    html_head_content = models.TextField(default="nothing")
    html_body_content = models.TextField(default="nothing")
    facebook_book_pixel = models.TextField(default="", null=True, blank=True)
    google_tag_manager_head = models.TextField(default="", null=True, blank=True)
    google_tag_manager_body = models.TextField(default="", null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    content_pack_name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to='xsite_images/website_logos/', default='xsite_images/website_logos/xsite_logo.png',
                             null=True, blank=True)
    banner_title = models.CharField(max_length=300)
    banner_button_text = models.CharField(max_length=300)
    about_us_title = models.CharField(max_length=300)
    about_us_desc = models.TextField()
    video_link = models.CharField(max_length=300)
    video_title = models.CharField(max_length=300)
    video_desc = models.TextField()
    testi_1_company_name = models.CharField(max_length=300)
    testi_1_person_name = models.CharField(max_length=300)
    testi_1_text = models.TextField()

    testi_2_company_name = models.CharField(max_length=300, null=True, blank=True)
    testi_2_person_name = models.CharField(max_length=300, null=True, blank=True)
    testi_2_text = models.TextField(null=True, blank=True)

    testi_3_company_name = models.CharField(max_length=300, null=True, blank=True)
    testi_3_person_name = models.CharField(max_length=300, null=True, blank=True)
    testi_3_text = models.TextField(null=True, blank=True)

    other_details_title = models.CharField(max_length=300)
    other_details_desc = models.TextField()

    call_to_action_text = models.CharField(max_length=300)

    # def __str__(self):
    #     return str(self.site) + " " + self.content_pack_name

    class Meta:
        verbose_name_plural = 'Template Content'


class WebsitePages(models.Model):
    page_name = models.CharField(max_length=50)
    html_head_content = models.TextField(default="nothing")
    html_body_content = models.TextField(default="nothing")
    template_content = models.ForeignKey(TemplateContent, on_delete=models.CASCADE)

    def __str__(self):
        return self.page_name + " " + self.template_content.site.domain

    class Meta:
        verbose_name_plural = 'Website Page'


class Mail(models.Model):
    site = models.ForeignKey(Websites, on_delete=models.CASCADE, blank=True)
    from_email = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = 'Mail'


class MembershipPlan(models.Model):
    plan = models.CharField(max_length=100)
    billing_amount = models.FloatField()

    def __str__(self):
        return self.plan

    class Meta:
        verbose_name_plural = 'Membership Plan'


subscription_status = (
    ('Not Subscribed', 'Not Subscribed'),
    ('Subscribed', 'Subscribed'),
    ('Cancelled', 'Cancelled'),
)

next_subscription_plan = (
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly'),
    ('None', 'None'),
)


class MembershipDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    subscription_id = models.CharField(max_length=255, blank=True, null=True, default=None)
    subscription_status = models.CharField(max_length=20, choices=subscription_status, default='Not Subscribed')
    subscription_end_date = models.DateField(blank=True, null=True)
    next_subscription_plan = models.CharField(max_length=50, choices=next_subscription_plan, default="None")
    account_status = models.CharField(max_length=10, default="active")

    class Meta:
        verbose_name_plural = 'Membership Details'


class Status(models.Model):
    status = (
        ('New', 'New'),
        ('Follow Up', 'Follow Up'),
        ('Pending', 'Pending'),
        ('Won', 'Won'),
        ('Dead', 'Dead'),
    )
    status_name = models.CharField(max_length=10, choices=status, default='New')

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name_plural = 'Status'


class BuyerOptions(models.Model):
    options = (
        ('Commercial', 'Commercial'),
        ('Investor', 'Investor'),
        ('Landlord', 'Landlord'),
        ('Landlord - Turn Key', 'Landlord - Turn Key'),
        ('Lease Option', 'Lease Option'),
        ('Owner Finance', 'Owner Finance'),
        ('Rehabber', 'Rehabber'),
        ('Renter', 'Renter'),
        ('Retail', 'Retail'),
    )
    option_name = models.CharField(max_length=20, choices=options, default='Commercial')

    def __str__(self):
        return self.option_name

    class Meta:
        verbose_name_plural = 'Buyer Option'


class ListingOptions(models.Model):
    listing = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Will Be Listed Soon', 'Will Be Listed Soon'),
    )
    listing_name = models.CharField(max_length=20, choices=listing, default='Yes')

    def __str__(self):
        return self.listing_name

    class Meta:
        verbose_name_plural = 'Listing Option'


class Leads(models.Model):
    site = models.ForeignKey(Websites, on_delete=models.CASCADE, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True)
    is_marked_read = models.BooleanField(default=False)
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=256)
    what_are_you_looking_for = models.ForeignKey(BuyerOptions, on_delete=models.CASCADE, blank=True, null=True)
    street_address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    is_home_listed = models.ForeignKey(ListingOptions, on_delete=models.CASCADE, blank=True, null=True)
    asking_price = models.FloatField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Lead'


class ExtraPropertyInformation(models.Model):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE, blank=True)
    property_type = models.CharField(max_length=50)
    min_bedrooms = models.IntegerField(default=0)
    max_bedrooms = models.IntegerField(default=0)
    style_of_property = models.CharField(max_length=50)
    min_bathrooms = models.IntegerField(default=0)
    max_bathrooms = models.IntegerField(default=0)
    min_price = models.FloatField(default=0, blank=True, null=True)
    max_price = models.FloatField(default=0, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=256, blank=True, null=True)
    sms_notifications = models.BooleanField(default=False)
    voice_notifications = models.BooleanField(default=False)
    buying_plan = models.CharField(max_length=100)
    buying_reason = models.CharField(max_length=100)
    rent_or_own = models.CharField(max_length=5)
    sell_before_moving = models.CharField(max_length=4)
    source = models.CharField(max_length=50)
    finance = models.CharField(max_length=100)
    pre_qualified = models.CharField(max_length=100)
    amount = models.FloatField(default=0, blank=True, null=True)
    down_payment = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Extra Property Information'


class Settings(models.Model):
    site = models.ForeignKey(Websites, on_delete=models.CASCADE, blank=True)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=256, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    contact_email = models.CharField(max_length=100, blank=True, null=True)
    parent_website_url = models.CharField(max_length=300, blank=True, null=True)
    google_analytics_tracking_code = models.CharField(max_length=100, blank=True, null=True)
    website_title = models.CharField(max_length=100, blank=True, null=True)
    redirect_url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'Setting'
