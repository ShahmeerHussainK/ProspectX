import requests
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views import View
from django.db.models.signals import post_save
# from xforce.utils import send_sms
from prospectx_new.settings import BASE_API_URL
from .models import *
from .views import get_choices, get_areas, email_type, phone_type


class webFormSalesOffer(View):
    def get(self, request, user_uuid):
        user = User.objects.get(userprofile__xforce_uuid=user_uuid)
        sales_data = sales.objects.filter(created_by=user)
        return render(request, 'xforce/sales_offers/webform_new_sale_offer.html',
                      {'investor_type': get_choices(),
                       'targeted_area': get_areas(),
                       'email_type': email_type(),
                       'phone_type': phone_type(),
                       'all_sales': sales_data

                       })

    def post(self, request, user_uuid):
        user = User.objects.get(userprofile__xforce_uuid=user_uuid)
        properties = sales.objects.filter(created_by=user)
        post_values = request.POST.copy()
        sales_data = sales.objects.filter(created_by=user)
        if request.POST.get('close_date'):
            date_got = request.POST.get('close_date')
            date_got = datetime.strptime(date_got, "%m/%d/%y %H:%M")
            post_values['close_date'] = date_got
        post_values['user'] = user.id


        response = requests.post(BASE_API_URL + 'sales/AddSales/', data=post_values)
        if response.status_code == 201:
            context = {"from": "offer"}
            return render(request, 'xforce/sales_offers/thanks.html', context)
        error_dict = {}
        for (key, value) in response.json().items():  # keys
            error_dict.update({key: value[0]})
            print(error_dict)
        context = {
            'states': get_choices(),
            'errors': error_dict,
            'data': request.POST,
            'property': properties,
            'all_sales': sales_data

        }
        return render(request, 'xforce/sales_offers/webform_new_sale_offer.html', context)
