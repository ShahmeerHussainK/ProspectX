from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.exceptions import ValidationError

from .models import *
from django import forms


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = '__all__'


class LeadForm(forms.ModelForm):
    class Meta:
        model = Leads
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError(u'This field is required')
        elif len(phone) < 12:
            raise forms.ValidationError(u'Too Short')
        return phone


class ExtraPropertyInformationForm(forms.ModelForm):
    class Meta:
        model = ExtraPropertyInformation
        fields = '__all__'


class TemplateContentForm(forms.ModelForm):
    logo = forms.ImageField(required=False)

    class Meta:
        model = TemplateContent
        fields = '__all__'


class LogoForm(forms.ModelForm):
    logo = forms.ImageField(required=True)

    class Meta:
        model = TemplateContent
        fields = ('logo',)
