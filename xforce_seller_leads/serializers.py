from rest_framework import serializers

from .models import *


class SellerLeadsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerLead
        fields = '__all__'
