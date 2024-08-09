from django import forms
from xforce_sales.models import sales_offer,sales


class SaleForm(forms.ModelForm):

    class Meta:
        model = sales_offer
        exclude = ['user',]
class Sale(forms.ModelForm):

    class Meta:
        model = sales
        exclude = ['created_by',]

