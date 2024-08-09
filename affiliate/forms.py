from django import forms
from . import models


class InviteUrlForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(InviteUrlForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.InviteUrl
        fields = ('url_name', 'sub_id',)

    def clean_url_name(self):
        url_name = self.cleaned_data.get('url_name')
        if models.InviteUrl.objects.filter(user=self.user, url_name=url_name).exists():
            raise forms.ValidationError(u'Already exists.')
        if not url_name:
            raise forms.ValidationError(u'This field is required.')
        if len(url_name) > 5:
            raise forms.ValidationError(u'Enter just 5 characters')
        return url_name

    def clean_sub_id(self):
        sub_id = self.cleaned_data.get('sub_id')
        if models.InviteUrl.objects.filter(user=self.user, sub_id=sub_id).exists():
            raise forms.ValidationError(u'Already exists.')
        if not sub_id:
            raise forms.ValidationError(u'This field is required.')
        if len(sub_id) > 5:
            raise forms.ValidationError(u'Enter just 5 characters')
        return sub_id


class PaymentForm(forms.Form):
    payout_email = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_payout_email(self):
        payout_email = self.cleaned_data.get('payout_email')
        if not payout_email:
            raise forms.ValidationError(u'This field is required.')
        return payout_email

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount:
            raise forms.ValidationError(u'This field is required.')
        return amount
