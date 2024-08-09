from django import forms
from xforce_settings.models import Company


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = ['user',]
