from django.core.exceptions import ValidationError

from .models import *
from django import forms


class ProspectForm(forms.ModelForm):
    is_validated = forms.CharField()
    total_phone_fields = forms.CharField(required=False)
    total_custom_fields = forms.CharField(required=False)

    class Meta:
        model = Prospect_Properties
        fields = '__all__'
        extra_fields = ['is_validated', 'total_phone_fields', 'total_custom_fields']
        exclude = ['api_response']

    def clean_propertyzip(self):
        propertyzip = self.cleaned_data.get('propertyzip')
        if not propertyzip:
            raise forms.ValidationError(u'This field is required')
        if len(propertyzip) < 5:
            raise forms.ValidationError(u'Too Short')
        return propertyzip

    def clean_mailingzip(self):
        mailingzip = self.cleaned_data.get('mailingzip')
        if mailingzip and len(mailingzip) < 5:
            raise forms.ValidationError(u'Too Short')
        return mailingzip

    def clean_phonelandline(self):
        phonelandline = self.cleaned_data.get('phonelandline')
        if phonelandline and len(phonelandline) < 12:
            raise forms.ValidationError(u'Too Short')
        return phonelandline

    def clean_phoneother(self):
        phoneother = self.cleaned_data.get('phoneother')
        if phoneother and len(phoneother) < 12:
            raise forms.ValidationError(u'Too Short')
        return phoneother

    def clean_phone1(self):
        phone1 = self.cleaned_data.get('phone1')
        if phone1 and len(phone1) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone1

    def clean_phone2(self):
        phone2 = self.cleaned_data.get('phone2')
        if phone2 and len(phone2) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone2

    def clean_phone3(self):
        phone3 = self.cleaned_data.get('phone3')
        if phone3 and len(phone3) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone3

    def clean_phone4(self):
        phone4 = self.cleaned_data.get('phone4')
        if phone4 and len(phone4) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone4

    def clean_phone5(self):
        phone5 = self.cleaned_data.get('phone5')
        if phone5 and len(phone5) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone5

    def clean_phone6(self):
        phone6 = self.cleaned_data.get('phone6')
        if phone6 and len(phone6) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone6

    def clean_phone7(self):
        phone7 = self.cleaned_data.get('phone7')
        if phone7 and len(phone7) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone7

    def clean_phone8(self):
        phone8 = self.cleaned_data.get('phone8')
        if phone8 and len(phone8) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone8

    def clean_phone9(self):
        phone9 = self.cleaned_data.get('phone9')
        if phone9 and len(phone9) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone9

    def clean_phone10(self):
        phone10 = self.cleaned_data.get('phone10')
        if phone10 and len(phone10) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone10

    def clean(self):
        phonecell = self.cleaned_data.get('phonecell')
        print(phonecell)
        if self.cleaned_data.get('is_validated') != 'valid':
            raise ValidationError({
                'phonecell': forms.ValidationError(self.cleaned_data.get('is_validated')),
            })
        return self.cleaned_data

