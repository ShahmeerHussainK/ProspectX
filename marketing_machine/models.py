from django.db import models
from datetime import timezone
from user.models import *
from filter_prospects.models import *
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.utils import timezone
from django.utils.timezone import localtime, now

status_choices = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('InActive', 'InActive'),
    )
temperature_choices = (
        ('Cold', 'Cold'),
        ('Warm', 'Warm'),
        ('Hot', 'Hot'),
    )


plan_choices = (
        ('Cold Call', 'Cold Call'),
        ('Direct Mail', 'Direct Mail'),
        ('Voice Broadcast', 'Voice Broadcast'),
        ('RVM', 'RVM'),
        ('SMS', 'SMS'),
        ('EMAIL', 'EMAIL'),
    )

distribution_choices = (
        ('Pending', 'Pending'),
        ('Untouched', 'Untouched'),
        ('Completed', 'Completed'),
    )

approval_choices = (
        ('Pending', 'Pending'),
        ('Approved to Merchant', 'Approved to Merchant'),
    )

planning_choices = (
        ('Untouched', 'Untouched'),
        ('Filtered', 'Filtered'),
        ('Skipped', 'Skipped'),
        ('Planned', 'Planned'),
    )

market_plan_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )


camp_status_choices = (
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
)


class MajorMarket(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, default=None, unique=True)
    market = models.CharField(max_length=255, blank=True, null=True, default=None)
    state = models.CharField(max_length=255, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'MajorMarket'


class MarketingSequence(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='user')
    list = models.ForeignKey('filter_prospects.List', on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=255, choices=status_choices, default='Pending')
    temperature = models.CharField(max_length=255, choices=temperature_choices, default='Cold')
    details = models.CharField(max_length=500, blank=True, null=True, default=None)
    planning_status = models.CharField(max_length=255, choices=planning_choices, default='Untouched')
    create_marketing = models.CharField(max_length=255, choices=market_plan_choices, default='No')
    planning_done = models.CharField(max_length=255, choices=market_plan_choices, default='No')
    is_completed = models.CharField(max_length=255, choices=market_plan_choices, default='No')
    timezone_gap_in_hours = models.CharField(max_length=10, null=True, blank=True, default="0")
    # maj_market = models.ForeignKey(MajorMarket, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    # responsible = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='responsible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + "-" + self.name

    class Meta:
        verbose_name_plural = 'MarketingSequence'


class MarketingPlan(models.Model):
    sequence = models.ForeignKey(MarketingSequence, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    plan = models.CharField(max_length=255, choices=plan_choices, default='Cold Call')
    touch_rounds = models.IntegerField(default=0)      # how many rounds for this plan
    break_into = models.IntegerField(default=0)
    current_round = models.IntegerField(default=0)     # to check what current campaign round is for celery
    is_completed = models.BooleanField(default=False)  # to check if celery ran all the campaigns of this plan or not
    days_gap_in_campaign = models.CharField(max_length=50, null=True, blank=True, default="0")
    send_on = models.CharField(max_length=20, blank=True, null=True, default='M-S')
    scheduled_plan_for = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sequence.name if self.sequence else self.plan

    class Meta:
        verbose_name_plural = 'MarketingPlan'


class PlanRoundTemplate(models.Model):
    plan = models.ForeignKey(MarketingPlan, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    detail = models.CharField(max_length=255, blank=True, null=True, default="")
    more_info = models.CharField(max_length=255, blank=True, null=True, default="")
    touch_round_number = models.CharField(max_length=100, blank=True, null=True, default="")   # round number of plan(touch)
    touch_status = models.CharField(max_length=255, choices=status_choices, default='Active')
    touch_round_after_days = models.IntegerField(default=0)                              # gap in this round to next one
    touch_file = models.FileField(upload_to='touch_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan.sequence.name if self.plan.sequence else self.name + "-" + self.plan.plan + str(self.touch_round_number)

    class Meta:
        verbose_name_plural = 'PlanRoundTemplate'


class MarketingCampaign(models.Model):
    camp_sequence = models.ForeignKey(MarketingSequence, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    plan = models.ForeignKey(MarketingPlan, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    template = models.OneToOneField(PlanRoundTemplate, on_delete=models.CASCADE, default=None, null=True, blank=True)
    user = models.CharField(max_length=255, blank=True, null=True, default=None)
    title = models.CharField(max_length=255, blank=True, null=True, default=None)
    campaigning_status = models.CharField(max_length=50, choices=camp_status_choices, default='Pending')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    hash_off = models.CharField(max_length=255, blank=True, null=True, default=None)
    temperature = models.CharField(max_length=255, choices=temperature_choices, default='Cold')
    distribution_status = models.CharField(max_length=255, choices=distribution_choices, default='Pending')
    approval = models.CharField(max_length=255, choices=approval_choices, default='Pending')
    total_units = models.IntegerField(default=0)       # total prospects in a list maybe?
    scheduled_plan_for = models.DateTimeField(blank=True, null=True)
    timezone_gap_in_hours = models.CharField(max_length=10, null=True, blank=True, default="0")
    days_gap_in_campaign = models.CharField(max_length=50, null=True, blank=True, default="0")
    notes = models.CharField(max_length=255, blank=True, null=True, default=None)
    marketing_details = models.CharField(max_length=255, blank=True, null=True, default=None)
    break_into = models.IntegerField(default=0)
    send_on = models.CharField(max_length=20, blank=True, null=True, default='M-S')
    time_format = models.CharField(max_length=20, blank=True, null=True, default='AM')
    maj_market = models.ForeignKey(MajorMarket, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='responsible')
    campaign_file = models.FileField(upload_to='campaign_files/', null=True, blank=True)
    campaign_records_list = models.TextField(blank=True, null=True, default='')
    current_campaign = models.BooleanField(default=False)
    is_single = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan.sequence.name if self.plan.sequence else self.title + " " + self.plan.plan if self.plan else "anonymous plan"

    class Meta:
        verbose_name_plural = 'MarketingCampaign'


class CampaignManagement(models.Model):     # for celery
    sequence = models.ForeignKey(MarketingSequence, on_delete=models.CASCADE, default=None)
    prospect = models.ForeignKey(Prospect_Properties, on_delete=models.CASCADE, default=None)
    plan = models.CharField(max_length=255, choices=plan_choices, default='Cold Call')
    current_round = models.IntegerField(default=0)

    def __str__(self):
        return self.sequence.name + " " + self.plan + " " + str(self.current_round)

    class Meta:
        verbose_name_plural = 'CampaignManagement'
