from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ContractTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractTemplates
        fields = '__all__'


class CallrailSerializer (serializers.ModelSerializer):
    class Meta:
        model = Callrail
        fields = '__all__'


class E_SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = E_Signature_setting
        fields = '__all__'


class Title_Company_ActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title_Company_Actions
        fields = '__all__'


class CallAndOfferAttemptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallAndOfferAttempts
        fields = '__all__'

class XforceSettingsSerializer(serializers.ModelSerializer):


    class Meta:
        model = XforceSettings
        fields = "__all__"
        '''#fields = ['setting_name', 'entity_name', 'disposition_company_name',
                  'email_subject_for_comment', 'sms_phone_number',
                  'phone_number', 'email', 'website', 'logo', 'seller_missed_call_text',
                  'best_and_highest_email_template',
                  'pending_property_email_template', 'sold_property_email_template',
                  'file', ]'''



class testSettingsSerializer(serializers.ModelSerializer):

    callrail = CallrailSerializer(many=True)
    contract = ContractTemplatesSerializer(many=True)
    # e_signature = E_SignatureSerializer(many=True)
    # title_company = Title_Company_ActionsSerializer(many=True)
    # call_and_offers = CallAndOfferAttemptsSerializer(many=True)
    class Meta:
        model = XforceSettings
        # fields = '__all__'

        fields = ['setting_name', 'entity_name', 'disposition_company_name',
                   'email_subject_for_comment', 'sms_phone_number',
                   'phone_number', 'email', 'website', 'logo', 'seller_missed_call_text',
                   'best_and_highest_email_template',
                   'pending_property_email_template', 'sold_property_email_template',
                   'setting_file', 'user', 'callrail','contract'
            # ,'e_signature','title_company','call_and_offers',
        ]

    def to_internal_value(self, data):
        callrail = []
        # 'api': post_values.pop('api')[0]
        callrail={'api': data['api'],
                         'account_number': data['account_number'],
                         'company_id': data['company_id']}
        data['callrail[0]'] = callrail

        # contract = []
        contract={
            'contract_type': data['contract_type'],
            'contract_email_subject': data['contract_email_subject'],
            'contract_email_body': data['contract_email_body'],
            'contract_text': data['contract_text'],
        }
        data['contract[0]'] = contract

        return super(testSettingsSerializer, self).to_internal_value(data)

    def is_valid(self, raise_exception=True):
        val = super(testSettingsSerializer, self).is_valid(raise_exception=raise_exception)
        return val

    def create(self, validated_data):
        callrail_validated_list=validated_data.pop('callrail')
        contract_validated_list = validated_data.pop('contract')
        # e_signature_validated_list = validated_data.pop('e_signature')
        # title_company_validated_list = validated_data.pop('title_company')
        # call_and_offers_validated_list = validated_data.pop('call_and_offers')
        setting = XforceSettings.objects.create(**validated_data)

        for callrail in callrail_validated_list:
            callrail['setting'] = setting
            callrail_serializer = self.fields['callrail']

        callrail_serializer.create(callrail_validated_list)

        for contract in contract_validated_list:
            contract['setting'] = setting


            contract_serializer = self.fields['contract']
        contract_serializer.create(contract_validated_list)

        # for e_signature in e_signature_validated_list:
        #     e_signature['setting'] = setting
        #     e_signature_serializer=self.fields['e_signature']
        # e_signature_serializer.create(e_signature_validated_list)
        #
        # for title_company in title_company_validated_list:
        #     title_company['setting']=setting
        #     title_company_serializer=self.fields['title_company']
        # title_company_serializer.create(title_company_validated_list)
        #
        # for call_and_offers in call_and_offers_validated_list:
        #     call_and_offers['setting']=setting
        #     call_and_offers_serializer=self.fields['call_and_offers']
        # call_and_offers_serializer.create(call_and_offers_validated_list)

        return setting