import requests
from django.shortcuts import render
from django.views import View

# from xforce.utils import send_sms
from prospectx_new.settings import BASE_API_URL
from .models import *
from .views import get_temperature, get_occupancy


class webFormSellerLead(View):
    def get(self, request, user_uuid):
        users = User.objects.all()
        return render(request, 'xforce/seller_lead/webform_new_seller_lead.html',
                      {
                          'users': users,
                          'temperature': get_temperature(),
                          'occupancy': get_occupancy(),
                      })

    def post(self, request,user_uuid):
        post_values = request.POST.copy()
        user = User.objects.get(userprofile__xforce_uuid=user_uuid)
        post_values['user'] = user.id
        response = requests.post(BASE_API_URL + 'seller/add_seller/', data=post_values, files=request.FILES)

        if response.status_code == 201:
            context = {"from": "lead"}
            return render(request, 'xforce/sales_offers/thanks.html', context)
        users = User.objects.all()
        error_dict = {}

        for (key, value) in response.json().items():  # keys
            error_dict.update({key: value[0]})
            print(error_dict)
            context = {
                'errors': error_dict,
                'data': request.POST,
                'occupancy': get_occupancy(),
                'users': users,
            }
        return render(request, 'xforce/seller_lead/webform_new_seller_lead.html', context)
