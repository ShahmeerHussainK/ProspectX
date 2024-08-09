from rest_framework import serializers

from .models import Cash_Buyer


class Cash_BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash_Buyer
        fields = '__all__'
