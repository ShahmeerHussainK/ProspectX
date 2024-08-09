import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from rest_framework import generics

from prospectx_new.settings import BASE_API_URL
from .models import Cash_Buyer
from .serializers import Cash_BuyerSerializer


class AddCash_Buyer(generics.ListCreateAPIView):
    queryset = Cash_Buyer.objects.all().order_by('id')
    serializer_class = Cash_BuyerSerializer


class UpdateCash_Buyer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cash_Buyer.objects.all().order_by('id')
    serializer_class = Cash_BuyerSerializer


def get_states():
    states = []
    for choice in Cash_Buyer.STATE_CHOICES:
        states.append(choice[0])
    return states


def get_asset():
    assets = []
    for asset in Cash_Buyer.ASSET_CLASS:
        assets.append(asset[0])
    return assets


def get_investor():
    investors = []
    for investor in Cash_Buyer.INVESTOR_TYPE:
        investors.append(investor[0])
    return investors


def get_pricepoint():
    pricepoints = []
    for pricepoint in Cash_Buyer.PRICE_POINT:
        pricepoints.append(pricepoint[0])
    return pricepoints


def get_annualvolume():
    annualvolumes = []
    for annualvolume in Cash_Buyer.ANNUAL_VOLUME:
        annualvolumes.append(annualvolume[0])
    return annualvolumes


def get_financingtype():
    financingtypes = []
    for financingtype in Cash_Buyer.FINANCING_TYPE:
        financingtypes.append(financingtype[0])
    return financingtypes


class Cash_BuyerView(View):
    @method_decorator(login_required)
    def get(self, request):
        list_included = request.POST.getlist('type_of_investor')
        list_included_str = ''.join(list_included)
        list_included = list_included_str.split(',')




        # # json_response = response.json()
        # list_included_str = request.POST.getlist('type_of_investor').split(',')
        # # json_response['type_of_investor'] = investor_list

        return render(request, 'xforce/add_cash_buyer.html', {
                                                              'states': get_states(), 'assets': get_asset(),
                                                              "investors": get_investor(),
                                                              "pricepoints": get_pricepoint(),
                                                              "annualvolumes": get_annualvolume(),
                                                              "financingtypes": get_financingtype()})

    @method_decorator(login_required)
    def post(self, request):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        type_of_invs = request.POST.getlist('type_of_investor')
        type_of_invs_str = ','.join(type_of_invs)
        post_values['type_of_investor'] = type_of_invs_str
        # str_to_list = post_values['type_of_investor'].split(',')
        # post_values['type_of_investor'] = str_to_list




        response = requests.post(BASE_API_URL + 'cash_buyer/cash/', data=post_values, files=request.FILES)

        if response.status_code == 201:
            return redirect('buyerlist')

        errors = {}

        for (key, value) in response.json().items():
            errors[key] = value[0]

        type_of_invs_str = ','.join(type_of_invs)
        post_values['type_of_investor'] = type_of_invs_str
        str_to_list = post_values['type_of_investor'].split(',')
        post_values['type_of_investor'] = str_to_list

        context = {
                       'states': get_states(), 'assets': get_asset(),
                       "investors": get_investor(),
                       "pricepoints": get_pricepoint(),
                       "annualvolumes": get_annualvolume(),
                       "financingtypes": get_financingtype(),
                       'data': post_values,
                        'file' : request.FILES,
                        "errors": errors
                       }
        return render(request, 'xforce/add_cash_buyer.html',context)


class Cash_BuyerList(ListView):
    model = Cash_Buyer
    template_name = 'xforce/cash_buyer_list.html'
    def get_queryset(self):
        return Cash_Buyer.objects.filter(user=self.request.user)


class DeleteCash_BuyerView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        requests.delete(BASE_API_URL + 'cash_buyer/cash/' + str(pk))
        return redirect('buyerlist')


class ViewCash_BuyerView(View):
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'cash_buyer/cash/' + str(pk))
        data = response.json()
        return render(request, 'xforce/view_cash_buyer.html', data)


class dashboardCash_Buyer(View):
    def get(self, request):
        return render(request, 'xforce/xforce.html')


class EditCashBuyerView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'cash_buyer/cash/' + str(pk))
        json_response = response.json()
        investor_list = json_response['type_of_investor'].split(',')
        json_response['type_of_investor'] = investor_list

        context = {
            'is_edit': True,
            'states': get_states(), 'assets': get_asset(),
            "investors": get_investor(),
            "pricepoints": get_pricepoint(),
            "annualvolumes": get_annualvolume(),
            "financingtypes": get_financingtype(),
            'data': json_response
        }
        return render(request, 'xforce/add_cash_buyer.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id

        type_of_invs = request.POST.getlist('type_of_investor')
        type_of_invs_str = ','.join(type_of_invs)
        post_values['type_of_investor'] = type_of_invs_str
        if request.FILES:
            response = requests.put(BASE_API_URL + 'cash_buyer/cash/' + str(pk) + '/', data=post_values,
                                    files=request.FILES)
        else:

            post_values.pop('file')

            response = requests.put(BASE_API_URL + 'cash_buyer/cash/' + str(pk) + '/', data=post_values)




        if response.status_code == 200:
            return redirect('buyerlist')
        errors = {}

        for (key, value) in response.json().items():
            errors[key] = value[0]

        post_values['type_of_investor'] = type_of_invs_str
        str_to_list = post_values['type_of_investor'].split(',')
        post_values['type_of_investor'] = str_to_list


        context = {

                       'states': get_states(),
                        'assets': get_asset(),
                       "investors": get_investor(),
                       "pricepoints": get_pricepoint(),
                       "annualvolumes": get_annualvolume(),
                       "financingtypes": get_financingtype(),
                       #'errors': errors,
                       'data': post_values,

                       "errors": errors
        }
        return render(request, 'xforce/add_cash_buyer.html', context)
