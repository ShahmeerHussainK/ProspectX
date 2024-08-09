from rest_framework import serializers
from .models import *


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Websites
        fields = '__all__'


# class ContentPackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContentPack
#         fields = '__all__'


class TemplateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateContent
        fields = '__all__'


class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingOptions
        fields = '__all__'


class BuyerOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerOptions
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    is_home_listed = ListingSerializer()
    what_are_you_looking_for = BuyerOptionsSerializer()

    class Meta:
        model = Leads
        fields = '__all__'


class SiteDesignSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteDesign
        fields = '__all__'


# class ExtraPropertyInformationSerializer(serializers.ModelSerializer):
#     lead = LeadSerializer()
#
#     class Meta:
#         model = ExtraPropertyInformation
#         fields = '__all__'
