import json

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

from django.views import View


from .serializers import *


class totalView(View):
    def get(self, request, id):
        print("in")
        lead = SellerLead.objects.get(id=id)
        address = lead.property_address_map.replace(' ', '+')
        url = "http://www.totalviewrealestate.com/index.php?address={}".format(address)
        r = requests.get(url)
        # r = requests.get("http://www.totalviewrealestate.com/index.php?address=722+1st+St+Escalon,+CA+95320,+USA")
        soup = BeautifulSoup(r.content, 'html5lib')
        if soup.find("table", {"class": "pinfotab", "width": False}):
            table = soup.find("table", {"class": "pinfotab", "width": False}).findAll("tr")
            dictn = {}
            for tr in table:
                td_s = tr.findAll("td")
                if len(td_s) == 2:
                    dictn[td_s[0].text.strip()] = td_s[1].text.strip()
            for k, v in dictn.items():
                print(f"{k}: {v}")
            lead.sqft = dictn["SqFt:"]
            lead.lot_size = dictn['Lot Size:']
            lead.property_type = dictn['Property Type:']
            lead.year_built = dictn['Year Built:']
            val = dictn['Tax Assessment:'].strip('$')
            lead.tax_assessment = val.replace(',', '')
            lead.year_assessed = dictn['Year Assessed:']
            lead.save()
            print(r)
            dictn.update({'Tax Assessment:': lead.tax_assessment})
            dictn.update({'msg': "succesful_call"})
            return JsonResponse(dictn)
        else:
            lead.sqft = None
            lead.lot_size = None
            lead.property_type = None
            lead.year_built = None
            lead.tax_assessment = None
            lead.year_assessed = None
            lead.save()
            return JsonResponse({'msg':"unsuccesful_call"})




