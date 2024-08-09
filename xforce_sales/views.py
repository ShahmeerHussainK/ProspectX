import pandas as pd
from datetime import datetime
import requests
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from xforce.utils import send_sms, get_comunity_people_with_role, round_robin_assignment
from prospectx_new.settings import BASE_API_URL
from user.models import UserProfile
from xforce_sales.serializers import SalesofferSerializer, SalesSerializer
from .models import *
from xforce.utils import get_comunity_people
from django.http import HttpResponse
import csv
def get_choices():
    investor = []
    for Type_of_investor in sales_offer.Types_of_investor:
        investor.append(Type_of_investor[0])
    return investor


def get_areas():
    area = []
    for targeted_area in sales_offer.STATE_CHOICES:
        area.append(targeted_area[0])
    return area


def email_type():
    email = []
    for email_choc in sales_offer.EMAIL_CHOICES:
        email.append(email_choc[0])
    return email


def phone_type():
    phone = []
    for phone_choc in sales_offer.PHONE_CHOICES:
        phone.append(phone_choc[0])
    return phone


def get_status():
    status = []
    for statu in sales.STATUS:
        status.append(statu[0])
    return status


def get_showings():
    showings = []
    for showing in sales.Showing:
        showings.append(showing[0])
    return showings


def get_emails():
    emails = []
    for email in sales.Email:
        emails.append(email[0])
    return emails


def get_set_showing():
    set_showings = []
    for set_showing in sales.Set_showing:
        set_showings.append(set_showing[0])
    return set_showings


class SalesList(ListView):
    model = sales_offer
    template_name = 'xforce/sales_offers/sales_offer_list.html'

    def get_queryset(self):
        return sales_offer.objects.filter(user=self.request.user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(SalesList, self).get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['user_uuid'] = user_profile.xforce_uuid
        return context


class AddSales(generics.ListCreateAPIView):
    queryset = sales_offer.objects.all().order_by('id')
    serializer_class = SalesofferSerializer


class UpdateSalesOffer(generics.RetrieveUpdateDestroyAPIView):
    queryset = sales_offer.objects.all().order_by('id')
    serializer_class = SalesofferSerializer


class SaleofferView(View):
    @method_decorator(login_required)
    def get(self, request):
        properties = sales.objects.filter(created_by=request.user)
        return render(request, 'xforce/sales_offers/new_property_offer.html',
                      {'investor_type': get_choices(),
                       'targeted_area': get_areas(),
                       'email_type': email_type(),
                       'phone_type': phone_type(),
                       'property': properties
                       })

    @method_decorator(login_required)
    def post(self, request):
        properties = sales.objects.filter(created_by=request.user)
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        if request.POST.get('close_date'):
            date_got = request.POST.get('close_date')

            date_got = datetime.strptime(date_got, "%m/%d/%y %H:%M")
            post_values['close_date'] = date_got
        if request.POST.get('submission_date'):
            showing_dat = request.POST.get('submission_date')
            showing_dat = datetime.strptime(showing_dat, "%m/%d/%y %H:%M")
            post_values['submission_date'] = showing_dat
        if request.POST.get('date'):
            closing_dat = request.POST.get('date')
            closing_dat = datetime.strptime(closing_dat, "%m/%d/%y %H:%M")
            post_values['date'] = closing_dat


        response = requests.post(BASE_API_URL + 'sales/AddSales/', data=post_values, files=request.FILES)
        if response.status_code == 201:
            cash = request.POST.get("add_cash_buyer")
            dictcash = {}
            if cash:

                dictcash['buyer_name'] = request.POST.get('full_name')
                dictcash['entity_name'] = request.POST.get('llc_purchase_name')
                dictcash['phone_number'] = request.POST.get('phone_number')
                dictcash['email'] = request.POST.get('email')
                dictcash['realtor_name'] = ''
                dictcash['VIP'] = 'false'
                dictcash['needs_updating'] = 'false'
                dictcash['active'] = 'null'
                dictcash['target_area'] = request.POST.get('targeted_area')
                dictcash['asset_class'] = request.POST.get('asset_class')
                dictcash['notes'] = ''
                dictcash['type_of_investor'] = request.POST.get('investor_type')
                dictcash['price_point'] = request.POST.get('price_point')
                dictcash['minimum_return_requirement'] = ''
                dictcash['annual_volume'] = request.POST.get('annual_volume')
                dictcash['financing_type'] = request.POST.get('financing_type')
                dictcash['additional_notes'] = ''
                dictcash['office_address'] = ''
                dictcash['Search_query_toi'] = ''
                dictcash['user'] = request.user.id
                headers = {'Content-type': 'application/json'}
                responsecash = requests.post(BASE_API_URL + 'cash_buyer/cash/', data=json.dumps(dictcash),
                                             headers=headers)
                if responsecash.status_code == 201:
                    return redirect('SalesList')

            accepted = request.POST.get("offer_accepted")
            if accepted:
                sale_update = sales.objects.filter(id=request.POST.get("property")).update(status="Offer Accepted")

            return redirect('SalesList')
        if post_values['property']:
            saless = post_values['property']
            select_property = sales.objects.filter(pk=saless).first()

            errors = {}
            for (key, value) in response.json().items():
                errors[key] = value[0]
            context = {
                'investor_type': get_choices(),
                'targeted_area': get_areas(),
                'email_type': email_type(),
                'phone_type': phone_type(),
                'states': get_choices(),
                'errors': errors,
                'data': request.POST,
                'property': properties,
                "select_property": select_property
            }
            return render(request, 'xforce/sales_offers/new_property_offer.html', context)

        else:
            errors = {}
            for (key, value) in response.json().items():
                errors[key] = value[0]
            context = {
                'investor_type': get_choices(),
                'targeted_area': get_areas(),
                'email_type': email_type(),
                'phone_type': phone_type(),
                'states': get_choices(),
                'errors': errors,
                'data': request.POST,
                'property': properties,
            }
            return render(request, 'xforce/sales_offers/new_property_offer.html', context)


class DeleteSales_offerView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        requests.delete(BASE_API_URL + 'sales/AddSales/' + str(pk))
        return redirect('SalesList')


class ViewSalesOfferView(View):
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'sales/AddSales/' + str(pk))
        data = response.json()

        t_property = sales.objects.get(id=data['property'])
        data['property'] = t_property.deals.property_address

        if data['close_date']:
            deadline_to_assign = datetime.strptime(data['close_date'], "%Y-%m-%dT%H:%M:%SZ")
            deadline_to_assign = datetime.strftime(deadline_to_assign, "%m/%d/%y %H:%M")
            data['close_date'] = deadline_to_assign

        if data['submission_date']:
            showing_dat = datetime.strptime(data['submission_date'], "%Y-%m-%dT%H:%M:%SZ")
            showing_dat = datetime.strftime(showing_dat, "%m/%d/%y %H:%M")
            data['submission_date'] = showing_dat

        if data['date']:
            closing_dat = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%SZ")
            closing_dat = datetime.strftime(closing_dat, "%m/%d/%y %H:%M")
            data['date'] = closing_dat


        return render(request, 'xforce/sales_offers/view_sales_offer.html', data)


class EditSalesOfferView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        properties = sales.objects.filter(created_by=request.user)
        response = requests.get(BASE_API_URL + 'sales/AddSales/' + str(pk))
        context_data = response.json()

        saless = context_data.get("property")
        select_property = sales.objects.filter(pk=saless).first()
        if context_data['close_date']:
            deadline_to_assign = datetime.strptime(context_data['close_date'], "%Y-%m-%dT%H:%M:%SZ")
            deadline_to_assign = datetime.strftime(deadline_to_assign, "%m/%d/%y %H:%M")
            context_data['close_date'] = deadline_to_assign

        if context_data['submission_date']:
            showing_dat = datetime.strptime(context_data['submission_date'], "%Y-%m-%dT%H:%M:%SZ")
            showing_dat = datetime.strftime(showing_dat, "%m/%d/%y %H:%M")
            context_data['submission_date'] = showing_dat

        if context_data['date']:
            closing_dat = datetime.strptime(context_data['date'], "%Y-%m-%dT%H:%M:%SZ")
            closing_dat = datetime.strftime(closing_dat, "%m/%d/%y %H:%M")
            context_data['date'] = closing_dat


        context = {
            'investor_type': get_choices(),
            'targeted_area': get_areas(),
            'email_type': email_type(),
            'phone_type': phone_type(),
            'data': context_data,
            'ddddddd': context_data['file'],
            'property': properties,
            "select_property": select_property

        }
        return render(request, 'xforce/sales_offers/new_property_offer.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        properties = sales.objects.filter(created_by=request.user)
        post_values = request.POST.copy()
        post_values['user'] = request.user.id



        if request.POST.get('close_date'):
            date_got = request.POST.get('close_date')
            date_got = datetime.strptime(date_got, "%m/%d/%y %H:%M")
            post_values['close_date'] = date_got

        if request.POST.get('submission_date'):
            showing_dat = request.POST.get('submission_date')
            showing_dat = datetime.strptime(showing_dat, "%m/%d/%y %H:%M")
            post_values['submission_date'] = showing_dat

        if request.POST.get('date'):
            closing_dat = request.POST.get('date')
            closing_dat = datetime.strptime(closing_dat, "%m/%d/%y %H:%M")
            post_values['date'] = closing_dat

        response = requests.get(BASE_API_URL + 'sales/AddSales/' + str(pk))
        data = response.json()
        p_data = data["add_cash_buyer"]

        if request.FILES:
            response = requests.put(BASE_API_URL + 'sales/AddSales/' + str(pk) + '/', data=post_values,
                                    files=request.FILES)
        else:
            post_values.pop('file')

            response = requests.put(BASE_API_URL + 'sales/AddSales/' + str(pk) + '/', data=post_values)
        if response.status_code == 200:
            cash = request.POST.get("add_cash_buyer")
            dictcash = {}
            if cash:

                if p_data:
                    pass
                else:
                    dictcash['buyer_name'] = request.POST.get('full_name')
                    dictcash['entity_name'] = request.POST.get('llc_purchase_name')
                    dictcash['phone_number'] = request.POST.get('phone_number')
                    dictcash['email'] = request.POST.get('email')
                    dictcash['realtor_name'] = ''
                    dictcash['VIP'] = 'false'
                    dictcash['needs_updating'] = 'false'
                    dictcash['active'] = 'null'
                    dictcash['target_area'] = request.POST.get('targeted_area')
                    dictcash['asset_class'] = request.POST.get('asset_class')
                    dictcash['notes'] = ''
                    dictcash['type_of_investor'] = request.POST.get('investor_type')
                    dictcash['price_point'] = request.POST.get('price_point')
                    dictcash['minimum_return_requirement'] = ''
                    dictcash['annual_volume'] = request.POST.get('annual_volume')
                    dictcash['financing_type'] = request.POST.get('financing_type')
                    dictcash['additional_notes'] = ''
                    dictcash['office_address'] = ''
                    dictcash['Search_query_toi'] = ''
                    dictcash['user'] = request.user.id
                    headers = {'Content-type': 'application/json'}
                    responsecash = requests.post(BASE_API_URL + 'cash_buyer/cash/', data=json.dumps(dictcash),
                                                 headers=headers)
                    if responsecash.status_code == 201:
                        return redirect('SalesList')
            accepted = request.POST.get("offer_accepted")
            if accepted:
                sale_update = sales.objects.filter(id=request.POST.get("property")).update(status="Offer Accepted")

            return redirect('SalesList')
        if post_values['property']:
            saless = post_values['property']
            select_property = sales.objects.filter(pk=saless).first()

            errors = {}
            for (key, value) in response.json().items():
                errors[key] = value[0]
            context = {
                'investor_type': get_choices(),
                'targeted_area': get_areas(),
                'email_type': email_type(),
                'phone_type': phone_type(),
                'states': get_choices(),
                'errors': errors,
                'data': request.POST,
                'property': properties,
                "select_property": select_property
            }
            return render(request, 'xforce/sales_offers/new_property_offer.html', context)

        else:
            errors = {}
            for (key, value) in response.json().items():
                errors[key] = value[0]
            context = {
                'investor_type': get_choices(),
                'targeted_area': get_areas(),
                'email_type': email_type(),
                'phone_type': phone_type(),
                'states': get_choices(),
                'errors': errors,
                'data': request.POST,
                'property': properties,
            }
            return render(request, 'xforce/sales_offers/new_property_offer.html', context)


class Sales(generics.ListCreateAPIView):
    queryset = sales.objects.all().order_by('id')
    serializer_class = SalesSerializer


class UpdateSales(generics.RetrieveUpdateDestroyAPIView):
    queryset = sales.objects.all().order_by('id')
    serializer_class = SalesSerializer


class Sales_View(ListView):
    model = sales
    template_name = 'xforce/sales/sales_list.html'

    def get_queryset(self):
        return sales.objects.filter(created_by=self.request.user).order_by("-id")


class AddSalesView(View):
    @method_decorator(login_required)
    @method_decorator(login_required)
    def get(self, request):
        # users = User.objects.all()
        cash_buyer = Cash_Buyer.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user)
        return render(request, 'xforce/sales/add_sales.html',
                      {
                          "users": get_comunity_people(request.user),
                          "status": get_status(),
                          "showings": get_showings(),
                          'set_showings': get_set_showing(),
                          'send_email': get_emails(),
                          'transactions': transactions,
                          "Cash_buyers": cash_buyer})

    @method_decorator(login_required)
    def post(self, request):
        post_values = request.POST.copy()
        post_values['created_by'] = request.user.id

        selected_deals = ''
        if post_values['deals']:
            selected_deals = Transaction.objects.filter(pk=post_values['deals']).first()

        selected_interested = ''
        if post_values['current_interest']:
            selected_interested = Cash_Buyer.objects.filter(pk=post_values['current_interest']).first()

        selected_attending = ''
        if post_values['attending_showing']:
            selected_attending = Cash_Buyer.objects.filter(pk=post_values['attending_showing']).first()

        selected_accepted = ''
        if post_values['accepted_buyers']:
            selected_accepted = Cash_Buyer.objects.filter(pk=post_values['accepted_buyers']).first()

        if request.POST.get("status") == "" :
            post_values["status"] = "Pending"

        if post_values["final_gross_sales_price"] == "":
            post_values["final_gross_sales_price"] = 0

        if post_values["finders_fee"] == "":
            post_values["finders_fee"] = 0

        if request.POST.get('deadline_to_assign'):
            date_got = request.POST.get('deadline_to_assign')

            date_got = datetime.strptime(date_got, "%m/%d/%y %H:%M")

            post_values['deadline_to_assign'] = date_got
        if request.POST.get('showing_date'):
            showing_dat = request.POST.get('showing_date')

            showing_dat = datetime.strptime(showing_dat, "%m/%d/%y %H:%M")
            post_values['showing_date'] = showing_dat
        if request.POST.get('closing_date'):
            closing_dat = request.POST.get('closing_date')

            closing_dat = datetime.strptime(closing_dat, "%m/%d/%y %H:%M")
            post_values['closing_date'] = closing_dat
        assigned = request.POST.get("assigned")
        set_show = request.POST.get("set_showing")
        transaction_id = request.POST.get("deals")
        is_transaction = Transaction.objects.filter(id=transaction_id)
        if set_show:
            post_values["status"] = "Schedule and Showing"


        if assigned == "Offer Accepted(Back to Transaction)":
            post_values["status"] = "Offer Accepted"

        response = requests.post(BASE_API_URL + 'sales/Sales/', data=post_values, files=request.FILES)
        if response.status_code == 201:
            sale_dict = json.loads(response.text)
            sale = sales.objects.get(pk=sale_dict["id"])
            is_assigned = round_robin_assignment(request, 'sale', sale)
            if not is_assigned:
                messages.error(request, "No disposition manger was assigned to sale.")
            if is_transaction:
                if assigned == "Offer Accepted(Back to Transaction)":
                    post_values["status"] = "Offer Accepted"

                    transaction_update = Transaction.objects.filter(id=transaction_id).update(status="Offer Accepted",
                                                                                              final_gross_sales_price=int(post_values["final_gross_sales_price"]),
                                                                                              finder_fee=int(post_values["finders_fee"]),
                                                                                              buyer_entity_name=post_values['buyer_entity_name'],
                                                                                              buyer_contact_info=post_values['accepted_buyers'])
                else:
                    if set_show:
                        transaction_update = Transaction.objects.filter(id=transaction_id).update(
                            status="Schedule and Showing")
            return redirect('View_Sales')
        users = User.objects.all()
        user_name = post_values['disposition_manager']
        selected_manager = User.objects.filter(pk=user_name).first()
        cash_buyer = Cash_Buyer.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user)
        errors = {}
        for (key, value) in response.json().items():
            errors[key] = value[0]
        context = {
            "status": get_status(),
            "showings": get_showings(),
            "set_showings": get_set_showing(),
            "send_email": get_emails(),
            "data": request.POST,
            "users": get_comunity_people(request.user),
            "Selected_manager": selected_manager,
            "errors": response.json(),
            "t_property": selected_deals,
            "curr_interest": selected_interested,
            "att_showing": selected_attending,
            "acc_buyer": selected_accepted,
            'transactions': transactions,
            "Cash_buyers": cash_buyer
        }
        return render(request, 'xforce/sales/add_sales.html', context)


class DeleteSalesView(View):
    @method_decorator(login_required())
    def get(self, request, pk):
        requests.delete(BASE_API_URL + 'sales/Sales/' + str(pk))
        return redirect('View_Sales')


class EditSalesView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        s_offers = sales_offer.objects.filter(property=pk)
        transactions = Transaction.objects.filter(user=request.user)

        response = requests.get(BASE_API_URL + 'sales/Sales/' + str(pk))
        data = response.json()
        t_property = data.get("deals")
        t_property = Transaction.objects.filter(pk=t_property).first()

        user_name = data.get("disposition_manager")
        selected_manager = User.objects.filter(pk=user_name).first()

        name = data.get("accepted_buyers")
        acc_buyer = Cash_Buyer.objects.filter(pk=name).first()

        name = data.get("attending_showing")
        att_showing = Cash_Buyer.objects.filter(pk=name).first()

        name = data.get("current_interest")
        curr_interest = Cash_Buyer.objects.filter(pk=name).first()

        context_data = response.json()
        if context_data['deadline_to_assign']:
            deadline_to_assign = datetime.strptime(context_data['deadline_to_assign'], "%Y-%m-%dT%H:%M:%SZ")
            deadline_to_assign = datetime.strftime(deadline_to_assign, "%m/%d/%y %H:%M")
            context_data['deadline_to_assign'] = deadline_to_assign

        if context_data['showing_date']:
            showing_dat = datetime.strptime(context_data['showing_date'], "%Y-%m-%dT%H:%M:%SZ")
            showing_dat = datetime.strftime(showing_dat, "%m/%d/%y %H:%M")
            context_data['showing_date'] = showing_dat

        if context_data['closing_date']:
            closing_dat = datetime.strptime(context_data['closing_date'], "%Y-%m-%dT%H:%M:%SZ")
            closing_dat = datetime.strftime(closing_dat, "%m/%d/%y %H:%M")
            context_data['closing_date'] = closing_dat
        users = User.objects.all()
        cash_buyer = Cash_Buyer.objects.filter(user=request.user)
        context = {
            'is_edit': True,
            'offer_count': len(s_offers),
            "status": get_status(),
            "showings": get_showings(),
            'set_showings': get_set_showing(),
            'Cash_buyers': cash_buyer,
            'send_email': get_emails(),
            'Selected_manager': selected_manager,
            'data': context_data,
            'users': get_comunity_people_with_role(request.user, 'sale'),
            'acc_buyer': acc_buyer,
            'att_showing': att_showing,
            'curr_interest': curr_interest,
            'sales_offers': s_offers,
            'transactions': transactions,
            't_property': t_property
        }

        return render(request, 'xforce/sales/add_sales.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        response = requests.get(BASE_API_URL + 'sales/Sales/' + str(pk))
        data = response.json()
        s_offers = sales_offer.objects.filter(property=pk)
        post_values = request.POST.copy()

        if not request.POST.get("deals"):
            post_values["deals"] = data.get("deals")

        if not request.POST.get("assigned"):
            post_values["assigned"] = ""


        if post_values["final_gross_sales_price"] == "":
            post_values["final_gross_sales_price"] = 0

        if post_values["finders_fee"] == "":
            post_values["finders_fee"] = 0

        selected_deals = ''
        if post_values['deals']:
            selected_deals = Transaction.objects.filter(pk=post_values['deals']).first()

        selected_interested = ''
        if post_values['current_interest']:
            selected_interested = Cash_Buyer.objects.filter(pk=post_values['current_interest']).first()

        selected_attending = ''
        if post_values['attending_showing']:
            selected_attending = Cash_Buyer.objects.filter(pk=post_values['attending_showing']).first()

        selected_accepted = ''
        if post_values['accepted_buyers']:
            selected_accepted = Cash_Buyer.objects.filter(pk=post_values['accepted_buyers']).first()

        if data.get("from_transaction"):
            post_values["from_transaction"] = True

        post_values['created_by'] = request.user.id
        if request.POST.get('deadline_to_assign'):
            date_got = request.POST.get('deadline_to_assign')
            date_got = datetime.strptime(date_got, "%m/%d/%y %H:%M")
            post_values['deadline_to_assign'] = date_got
        if request.POST.get('showing_date'):
            showing_dat = request.POST.get('showing_date')
            showing_dat = datetime.strptime(showing_dat, "%m/%d/%y %H:%M")
            post_values['showing_date'] = showing_dat

        if request.POST.get('closing_date'):
            closing_dat = request.POST.get('closing_date')
            closing_dat = datetime.strptime(closing_dat, "%m/%d/%y %H:%M")
            post_values['closing_date'] = closing_dat
        if post_values["accepted_buyers"]:
            email_con = Cash_Buyer.objects.filter(id=post_values['accepted_buyers']).first()
            ac_buyer = email_con.email
            buyer_contact = email_con.phone_number

        offer_email = sales_offer.objects.values_list("email").filter(property=pk)
        emails = []
        for email in offer_email:
            emails.append(email[0])


        data_email_send = data.get("send_email")
        post_email_send = request.POST.get("send_email")
        p_email_subject = data.get("email_subject")
        email_subject = request.POST.get("email_subject")
        p_email_content = data.get("email_content")
        email_content = request.POST.get("email_content")
        assigned = request.POST.get("assigned")
        transaction_id = post_values["deals"]
        is_transaction = Transaction.objects.filter(id=transaction_id)
        set_show = request.POST.get("set_showing")
        unique_email = request.POST.get("unique_email")
        if set_show:
            post_values["status"] = "Schedule and Showing"
        if request.FILES:
            response = requests.put(BASE_API_URL + 'sales/Sales/' + str(pk) + '/', data=post_values,
                                    files=request.FILES)
        else:
            post_values.pop('files')

            response = requests.put(BASE_API_URL + 'sales/Sales/' + str(pk) + '/', data=post_values)

        if response.status_code == 200:
            if is_transaction:
                if assigned == "Offer Accepted(Back to Transaction)":
                    sales_update = sales.objects.filter(id=pk).update(status="Offer Accepted")
                    transaction_update = Transaction.objects.filter(id=transaction_id).update(status="Offer Accepted",
                                                                                              final_gross_sales_price=int(post_values["final_gross_sales_price"]),
                                                                                              finder_fee=int(post_values["finders_fee"]),
                                                                                              buyer_entity_name=post_values['buyer_entity_name'],
                                                                                              buyer_contact_info=post_values['accepted_buyers'])
                else:
                    if set_show:
                        sales_update = sales.objects.filter(id=pk).update(status="Schedule and Showing")
                        transaction_update = Transaction.objects.filter(id=transaction_id).update(
                            status="Schedule and Showing")

            if s_offers:
                # if unique_email:
                #     if p_email_subject != email_subject or p_email_content != email_content:
                #         for mail in emails:
                #             subject = email_subject
                #             message = email_content
                #             send_mail(subject, message, settings.EMAIL_HOST_USER, [mail, ])

                if data_email_send != post_email_send:
                    if post_email_send == "Best and Highest":
                        for mail in emails:
                            subject = "Best and Highest"
                            message = "Best and Highest"
                            send_mail(subject, message, settings.EMAIL_HOST_USER, [mail,])
                        offer_update = sales_offer.objects.filter(property=pk).update(counter_email_offer_sent="True")

                    if post_email_send == "Pending Property":
                        for mail in emails:
                            subject = 'Now Property is Pending'
                            message = 'Pending Property '
                            send_mail(subject, message, settings.EMAIL_HOST_USER, [mail,])
                        offer_update = sales_offer.objects.filter(property=pk).update(pending_email_sent="True")

                    if post_email_send == "Sold Property":
                        for mail in emails:
                            subject = 'Sold Property'
                            message = 'Property has been sold'
                            send_mail(subject, message, settings.EMAIL_HOST_USER, [mail,])
                        offer_update = sales_offer.objects.filter(property=pk).update(sold_email_sent="True")

            return redirect('View_Sales')

        users = User.objects.all()
        selected_manager = User.objects.filter(pk=post_values['disposition_manager']).first()
        cash_buyer = Cash_Buyer.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user)

        errors = {}
        for (key, value) in response.json().items():
            errors[key] = value[0]
        context = {
            'is_edit': True,
            "status": get_status(),
            "showings": get_showings(),
            'set_showings': get_set_showing(),
            'send_email': get_emails(),
            'errors': errors,
            'users': get_comunity_people_with_role(request.user, 'sale'),
            'Selected_manager': selected_manager,
            'data': request.POST,
            "t_property": selected_deals,
            "curr_interest": selected_interested,
            "att_showing": selected_attending,
            "acc_buyer": selected_accepted,
            'transactions': transactions,
            "Cash_buyers": cash_buyer
        }
        return render(request, 'xforce/sales/add_sales.html', context)


class ViewSalesView(View):
    def get(self, request, pk):
        s_offers = sales_offer.objects.filter(property=pk)
        response = requests.get(BASE_API_URL + 'sales/Sales/' + str(pk) + '/')
        data = response.json()
        t_property = Transaction.objects.get(id=data['deals'])
        data['deals'] = t_property.property_address
        manager = User.objects.get(id=data['disposition_manager'])
        data['disposition_manager'] = manager.username
        if data['current_interest']:
            cur_interested = Cash_Buyer.objects.get(id=data['current_interest'])
            data['current_interest'] = cur_interested.buyer_name
        if data['attending_showing']:
            att_showing = Cash_Buyer.objects.get(id=data['attending_showing'])
            data['attending_showing'] = att_showing.buyer_name
        if data['accepted_buyers']:
            acc_buyer = Cash_Buyer.objects.get(id=data['accepted_buyers'])
            data['accepted_buyers'] = acc_buyer.buyer_name

        if data['deadline_to_assign']:
            deadline_to_assign = datetime.strptime(data['deadline_to_assign'], "%Y-%m-%dT%H:%M:%SZ")
            deadline_to_assign = datetime.strftime(deadline_to_assign, "%m/%d/%y %H:%M")
            data['deadline_to_assign'] = deadline_to_assign

        if data['showing_date']:
            showing_dat = datetime.strptime(data['showing_date'], "%Y-%m-%dT%H:%M:%SZ")
            showing_dat = datetime.strftime(showing_dat, "%m/%d/%y %H:%M")
            data['showing_date'] = showing_dat
        if data['closing_date']:
            closing_dat = datetime.strptime(data['closing_date'], "%Y-%m-%dT%H:%M:%SZ")
            closing_dat = datetime.strftime(closing_dat, "%m/%d/%y %H:%M")
            data['closing_date'] = closing_dat
        context = {
            "data":data,
            'sales_offers': s_offers
        }

        return render(request, 'xforce/sales/view_sales.html', context)


def download_offers(request, pk):
    s_offers = sales_offer.objects.filter(property=pk)
    response = HttpResponse(content_type='text/csv')
    response["Content-Disposition"] = 'attachment; filename="Offers.csv"'
    writer = csv.writer(response, delimiter=',')
    writer.writerow(['Property', 'First Name', 'Soonest Close Date', 'Offer Amount'])
    for offers in s_offers:
        writer.writerow([offers.property.deals.property_address, offers.full_name, offers.close_date ,offers.offer_amount])

    return response

class send_email(View):
    def get(self, request, pk, sub, cont):
        print(pk)
        offer_email = sales_offer.objects.values_list("email").filter(property=pk)
        emails = []
        for email in offer_email:
            emails.append(email[0])

        for mail in emails:
            subject = sub
            message = cont
            send_mail(subject, message, settings.EMAIL_HOST_USER, [mail, ])

        return HttpResponse("ajax work")