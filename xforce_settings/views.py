import json

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from payments.views import is_subscribed
from prospectx_new.settings import STRIPE_PUBLISHABLE_KEY, BASE_API_URL
from .models import *
from .models import Company, XforceSettings, ContractTemplates
from .serializers import CompanySerializer
from .serializers import testSettingsSerializer


class AddCompany(generics.ListCreateAPIView):
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer


class UpdateCompany(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer


def get_choices():
    choices = []
    for choice in Company.STATE_CHOICES:
        choices.append(choice[0])
    return choices


class CompanyList(ListView):
    model = Company

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)


class CompanyView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'xforce_settings/company_form.html',
                      {'states': get_choices()})

    @method_decorator(login_required)
    def post(self, request):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        # files = request.FILES
        response = requests.post(BASE_API_URL + 'xforce_settings/company/', data=post_values, files=request.FILES)

        if response.status_code == 201:
            return redirect('company_list')
        errors = {}

        for (key, value) in response.json().items():
            errors[key] = value[0]
        context = {
                'states': get_choices(),
                'errors': errors,
                'data': request.POST
            }
        return render(request, 'xforce_settings/company_form.html', context)


class DeleteCompanyView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        requests.delete(BASE_API_URL + 'xforce_settings/company/' + str(pk))
        return redirect('company_list')


class EditCompanyView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'xforce_settings/company/' + str(pk))
        context = {
            'is_edit': True,
            'states': get_choices(),
            'data': response.json()
        }
        return render(request, 'xforce_settings/company_form.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        # files = request.FILES
        if request.FILES:

            response = requests.put(BASE_API_URL + 'xforce_settings/company/' + str(pk) + '/', data=post_values,
                             files=request.FILES)
        else:
            post_values.pop("company_img")
            response = requests.put(BASE_API_URL + 'xforce_settings/company/' + str(pk) + '/', data=post_values)

        if response.status_code == 200:
            return redirect('company_list')
        errors = {}

        for (key, value) in response.json().items():
            errors[key] = value[0]
        context = {
                'states': get_choices(),
                'errors': errors,
                'data': request.POST
            }
        return render(request, 'xforce_settings/company_form.html', context)


class ViewCompanyView(View):
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'xforce_settings/company/' + str(pk))
        data = response.json()
        return render(request, 'xforce_settings/view_company.html', data)


class SettingsList(ListView):
    model = XforceSettings


class AddSettings(generics.ListCreateAPIView):
    queryset = XforceSettings.objects.all().order_by('id')
    # parser_classes = (MultiPartParser,)
    serializer_class = testSettingsSerializer

    # def perform_create(self, serializer):
    #     ww = 1
    #     serializer.save(user=self.request.user)


class UpdateSettings(generics.RetrieveUpdateDestroyAPIView):
    queryset = XforceSettings.objects.all().order_by('id')
    serializer_class = testSettingsSerializer


def get_call_and_offer_types():
    types = []
    for type in CallAndOfferAttempts.Types:
        types.append(type[0])
    return types


def get_call_and_offer_actions():
    actions = []
    for action in CallAndOfferAttempts.Action:
        actions.append(action[0])
    return actions


def get_purchase_type():
    purchase_types = []
    for purchase_type in ContractTemplates.TYPE:
        purchase_types.append(purchase_type[0])
    return purchase_types


class XforceSettingsView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'xforce_settings/xforcesettings_form.html', {
            'types': get_call_and_offer_types(),
            'actions': get_call_and_offer_actions(),
            'purchase_types': get_purchase_type()})

    @method_decorator(login_required)
    def post(self, request):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        # post_values['logo'] = request.FILES['logo']
        # post_values['setting_file'] = request.FILES['setting_file']

        e_signature = []
        e_signature.append({
            'title': post_values['title'],
            'message': post_values['message'],
            'requester_name': post_values['requester_name'],
            'requester_email': post_values['requester_email'],
            'reminders': post_values['reminders'],
        })
        post_values['e_signature'] = e_signature

        title_company = []
        title_company.append({
            'email_subject': post_values['email_subject'],
            'email_body': post_values['email_body'],
        })
        post_values['title_company'] = title_company

        call_and_offers = []
        call_and_offers.append({
            "callandofferattempts_type": post_values['callandofferattempts_type'],
            'callandofferattempts_sms': post_values['callandofferattempts_sms'],
            'callandofferattempts_subject': post_values['callandofferattempts_subject'],
            'callandofferattempts_body': post_values['callandofferattempts_body'],
            'callandofferattempts_action': post_values['callandofferattempts_action']
        })
        post_values['call_and_offers'] = call_and_offers

        # post_values = json.dumps(post_values)

        response = requests.post(BASE_API_URL + 'xforce_settings/settings/', data=post_values,
                                 files=request.FILES)
        if response.status_code == 201:
            return redirect('company_list')
        errors = []
        for error in response.json().keys():
            # errors = errors + error
            errors.append(error)
        context = {
            'types': get_call_and_offer_types(),
            'actions': get_call_and_offer_actions(),
            'purchase_types': get_purchase_type(),
            'errors': errors,
            'data': request.POST
        }

        return render(request, 'xforce_settings/xforcesettings_form.html', context)
