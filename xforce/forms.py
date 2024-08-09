from django import forms
from .models import *


class add_seller_leads_form(forms.Form):

    class Meta:
        model = User
        fields = ('seller_name',
                  'property_address_map',
                  'outbound_call_lead',
                  'follow_up_in',

                  )
