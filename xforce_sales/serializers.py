from rest_framework import serializers

from .models import sales_offer, sales


class SalesofferSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales_offer
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = '__all__'
