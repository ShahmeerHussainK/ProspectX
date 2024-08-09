from rest_framework import serializers
from .models import Transaction
from xforce_seller_leads.serializers import SellerLeadsSerializer


class TransactionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'



# class TransactionSerializers(serializers.ModelSerializer):
#     seller = serializers.CharField(read_only=True, source="seller.seller_name")
#     transaction_manager = serializers.CharField(read_only=True, source="transaction_manager.email")
#     company = serializers.CharField(read_only=True, source="company.title")
#     buyer_contact_info = serializers.CharField(read_only=True, source="buyer_contact_info.buyer_name")
#     campaigns = serializers.CharField(read_only=True, source="campaigns.title")
#
#     class Meta:
#         model = Transaction
#         fields = '__all__'


