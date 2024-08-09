from datetime import datetime
from datetime import date
from user.models import UserProfile
from django.contrib import messages
from twilio.rest import Client
from django.core.mail import send_mail
from django.conf import settings
import requests
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User
from marketing_machine.models import MarketingCampaign
from prospectx_new.settings import BASE_API_URL
from .models import Transaction
from xforce_settings.models import Company
from xforce_seller_leads.models import SellerLead
from django.views.generic import ListView
from .serializers import TransactionSerializers
from rest_framework import generics
from cash_buyer.models import Cash_Buyer
from xforce_sales.models import sales
from xforce.utils import get_comunity_people,comunity_people_with_role, get_comunity_people_with_role, round_robin_assignment
from prospectx_new.settings import account_sid_twilio, auth_token_twilio
from rest_framework.response import Response
from django.http import HttpResponse
import json
from .utils import render_to_pdf
from io import BytesIO
from django.core.files import File
from django.core.mail import EmailMessage



# Create your views here.


def get_seller_leads(request):
    return SellerLead.objects.filter(user=request.user)
    # return SellerLead.objects.filter(user=request.user)

def get_transaction_managers(req):
    return get_comunity_people_with_role(req.user, "transaction"),


def get_cash_buyers(request):
    # return Cash_Buyer.objects.all()
    return Cash_Buyer.objects.filter(user=request.user)


def get_company(request):
    return Company.objects.filter(user=request.user)


def get_status():
    choices = []
    for choice in Transaction.STATUS:
        choices.append(choice[0])
    return choices


def get_potential():
    choices = []
    for choice in Transaction.POTENTIAL:
        choices.append(choice[0])
    return choices


def get_pending_stage():
    choices = []
    for choice in Transaction.PENDING_STAGE:
        choices.append(choice[0])
    return choices


def get_title_actions():
    choices = []
    for choice in Transaction.TITLE_ACTIONS:
        choices.append(choice[0])
    return choices


def get_contract_action():
    choices = []
    for choice in Transaction.CONTRACT_ACTION:
        choices.append(choice[0])
    return choices


def get_marketing_stage():
    choices = []
    for choice in Transaction.MARKETING_STAGE:
        choices.append(choice[0])
    return choices


def get_assigned_stage():
    choices = []
    for choice in Transaction.ASSIGNED_STAGE:
        choices.append(choice[0])
    return choices


def get_showing():
    choices = []
    for choice in Transaction.SHOWING:
        choices.append(choice[0])
    return choices


def get_lead_source():
    choices = []
    for choice in Transaction.LEAD_SOURCE:
        choices.append(choice[0])
    return choices


def get_campaign():
    return MarketingCampaign.objects.all()


def get_contract_delivery():
    choices = []
    for choice in Transaction.CONTRACT_DELIVERY:
        choices.append(choice[0])
    return choices


class AddTransaction(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializers


class UpdateTransaction(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializers


class TransactionList(ListView):
    model = Transaction
    template_name = 'xforce/transactions/transaction_list.html'


    def get_context_data(self, *args, **kwargs):
        context = super(TransactionList, self).get_context_data(*args, **kwargs)

        context['transactions'] = Transaction.objects.filter(user=self.request.user).order_by("-id")
        return context


class TransactionView(View):

    @method_decorator(login_required)
    def get(self, request):
        context = {
            'seller_leads': get_seller_leads(request),
            'transaction_managers': get_comunity_people_with_role(request.user, "transaction"),
            'companies': get_company(request),
            'status_opt': get_status(),
            'potential_opt': get_potential(),
            'pending_stage_opt': get_pending_stage(),
            'title_actions_opt': get_title_actions(),
            'marketing_stage_opt': get_marketing_stage(),
            'assigned_stage_opt': get_assigned_stage(),
            'showing_opt': get_showing(),
            'cash_buyers': get_cash_buyers(request),
            'contract_actions': get_contract_action(),
            'lead_sources': get_lead_source(),
            'contract_delivery_opt': get_contract_delivery(),
            'campaigns': get_campaign()
        }
        return render(request, 'xforce/transactions/new_transactions.html', context)

    @method_decorator(login_required)
    def post(self, request):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id

        manager = request.POST.get('transaction_manager')
        if request.POST.get('transaction_manager'):
            user_name = post_values['transaction_manager']
            manager = User.objects.filter(pk=user_name).first()

        campai = request.POST.get('campaigns')
        if request.POST.get('campaigns'):
            campaign = post_values['campaigns']
            campai = MarketingCampaign.objects.get(id=campaign)

        seller =request.POST.get('seller')

        if request.POST.get('seller'):
            seller = post_values['seller']
            seller = SellerLead.objects.get(id=seller)

        company = ''
        if request.POST.get('company'):
            company = post_values['company']
            company = Company.objects.get(id=company)

        # if post_values["final_gross_sales_price"] == "":
        #     post_values["final_gross_sales_price"] = 0
        # if post_values["contract_price"] == "":
        #     post_values["contract_price"] = 0
        # if post_values["misc_expenses"] == "":
        #     post_values["misc_expenses"] = 0
        #
        # gross_price = post_values["final_gross_sales_price"]
        # contract_price = post_values["contract_price"]
        # misc_exp = post_values["misc_expenses"]
        # post_values["actual_profit"] = str(int(gross_price) - int(contract_price))
        # actual_profit = post_values["actual_profit"]
        # post_values["actual_profit"] = str(int(actual_profit) - int(misc_exp))



        if request.POST.get('contract_date_start'):
            contract_date_start = request.POST.get('contract_date_start')
            specific_date1 = datetime.strptime(contract_date_start, "%m/%d/%y %H:%M")
            post_values['contract_date_start'] = specific_date1

        if request.POST.get('contract_date_end'):
            contract_date_end = request.POST.get('contract_date_end')
            specific_date2 = datetime.strptime(contract_date_end, "%m/%d/%y %H:%M")
            post_values['contract_date_end'] = specific_date2

        if request.POST.get('purchase_contract_ratification_date_start'):
            purchase_contract_ratification_date_start = request.POST.get('purchase_contract_ratification_date_start')
            purchase_contract_ratification_date_start = datetime.strptime(purchase_contract_ratification_date_start,
                                                                          "%m/%d/%y %H:%M")
            post_values['purchase_contract_ratification_date_start'] = purchase_contract_ratification_date_start

        if request.POST.get('purchase_contract_ratification_date_end'):
            purchase_contract_ratification_date_end = request.POST.get('purchase_contract_ratification_date_end')
            purchase_contract_ratification_date_end = datetime.strptime(purchase_contract_ratification_date_end,
                                                                        "%m/%d/%y %H:%M")
            post_values['purchase_contract_ratification_date_end'] = purchase_contract_ratification_date_end

        if request.POST.get('showing_date_start'):
            showing_date_start = request.POST.get('showing_date_start')
            showing_date_start = datetime.strptime(showing_date_start, "%m/%d/%y %H:%M")
            post_values['showing_date_start'] = showing_date_start

        if request.POST.get('closing_date'):
            close_date = request.POST.get('closing_date')
            close_date = datetime.strptime(close_date, "%m/%d/%y").date()
            post_values['closing_date'] = close_date
        else:
            post_values['closing_date'] = str(request.POST.get('closing_date').replace("None", ""))

        if request.POST.get('emd_date_start'):
            emd_date_start = request.POST.get('emd_date_start')
            emd_date_start = datetime.strptime(emd_date_start, "%m/%d/%y %H:%M")
            post_values['emd_date_start'] = emd_date_start

        if request.POST.get('actual_close_date'):
            actual_date = request.POST.get('actual_close_date')
            actual_date = datetime.strptime(actual_date, "%m/%d/%y").date()
            post_values['actual_close_date'] = actual_date

        if request.POST.get('deadline_to_accept_offer_start'):
            deadline_to_accept_offer_start = request.POST.get('deadline_to_accept_offer_start')
            deadline_to_accept_offer_start = datetime.strptime(deadline_to_accept_offer_start, "%m/%d/%y %H:%M")
            post_values['deadline_to_accept_offer_start'] = deadline_to_accept_offer_start

        post_values['contract_price'] = str(request.POST.get('contract_price')).replace("None", "")
        # post_values['closing_date'] = str(request.POST.get('closing_date').replace("None", ""))
        response = requests.post(BASE_API_URL + 'xforce_transactions/transaction/', data=post_values,
                                 files=request.FILES)

        if response.status_code == 201:
            trans_dict = json.loads(response.text)
            transaction = Transaction.objects.get(pk=trans_dict["id"])
            is_assigned = round_robin_assignment(request, 'transaction', transaction)
            if not is_assigned:
                messages.error(request, "No transaction manger was assigned to transaction.")
            send_sales = request.POST.get('pre_assigned_status')
            sales_dict = {}

            if send_sales:
                sales_dict['created_by'] = request.user.id

                sales_dict['deals'] = response.json()['id']
                sales_dict['status'] = request.POST.get('status')
                sales_dict['disposition_manager'] = request.user.id
                sales_dict['from_transaction'] = True
                if request.POST.get('marketing_price'):

                    sales_dict['marketing_price'] = request.POST.get('marketing_price')
                sales_dict['transactions'] = response.json()['id']
                sales_dict['showing'] = 'Showing Complete'

                responsesales = requests.post(BASE_API_URL + 'sales/Sales/', data=json.dumps(sales_dict), headers={'content-type' : 'application/json'},)
                if responsesales.status_code == 201:
                    pass
            trans = Transaction.objects.get(pk=response.json()['id'])
            if request.POST.get('contract_action') == 'Generate Assignment Contract':
                generate_contract(request, trans)


            if request.POST.get('contract_action') == 'Email Assignment Contract To Title':


                if request.POST.get('company'):

                    company = Company.objects.filter(id=request.POST.get('company')).first()
                    company_email = company.email
                    if not trans.transaction_file:
                        generate_contract(request, trans)
                    # subject = 'Thank you for registering to our site'
                    msg = EmailMessage('Contract', 'Below is attached Contract file', settings.EMAIL_HOST_USER, [company_email,])
                    msg.content_subtype = "html"
                    msg.attach_file('media/Transactions_Files/Contract_{}.pdf'.format(
                        trans.property_address.replace(" ", "_")))
                    msg.send()
            if request.POST.get('contract_action') == 'Email Assignment Contract':

                if request.POST.get('buyer_contact_info'):

                    buyer_info = Cash_Buyer.objects.filter(id=request.POST.get('buyer_contact_info')).first()
                    # subject = 'Thank you for registering to our site'
                    # message = '  Email from xforce '
                    if not trans.transaction_file:
                        generate_contract(request, trans)
                    msg=EmailMessage('Contract', 'Below is attached Contract file', settings.EMAIL_HOST_USER, [buyer_info.email, ])
                    msg.content_subtype = "html"
                    msg.attach_file('media/Transactions_Files/Contract_{}.pdf'.format(
                        trans.property_address.replace(" ", "_")))
                    msg.send()
            if request.POST.get('title_actions'):
                if post_values['title_actions'] == 'Email Contract To Title':
                    if request.POST.get('company'):
                        email_contract = Company.objects.filter(id=post_values['company']).first()
                        subject = 'Thank you for registering to our site'
                        send_mail(subject, email_contract.title, settings.EMAIL_HOST_USER, [email_contract.email,])

                if post_values['title_actions'] == 'Email Wire Number To Title':
                    if request.POST.get('company'):
                        com_wire_no = Company.objects.filter(id=post_values['company']).first()
                        subject = 'Thank you for registering to our site'
                        send_mail(subject, post_values['wire_confirmation_number'], settings.EMAIL_HOST_USER, [com_wire_no.email, ])

            return redirect('transaction_list')

        errors = {}
        for (key, value) in response.json().items():
            errors[key] = value[0]

        context = {
                'errors': errors,
                'data': request.POST,
                'seller_leads': get_seller_leads(request),
                'transaction_managers': get_transaction_managers(request),
                'companies': get_company(request),
                'status_opt': get_status(),
                'potential_opt': get_potential(),
                'pending_stage_opt': get_pending_stage(),
                'title_actions_opt': get_title_actions(),
                'marketing_stage_opt': get_marketing_stage(),
                'assigned_stage_opt': get_assigned_stage(),
                'showing_opt': get_showing(),
                'cash_buyers': get_cash_buyers(request),
                'contract_actions': get_contract_action(),
                'lead_sources': get_lead_source(),
                'contract_delivery_opt': get_contract_delivery(),
                'campaigns': get_campaign(),
                'seller': seller,
                'campaign': campai,
                'manager': manager,
                'company': company
        }
        return render(request, 'xforce/transactions/new_transactions.html', context)


class ViewTransaction(View):
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'xforce_transactions/transaction/' + str(pk))
        data = response.json()
        if data['transaction_manager']:
            manager = User.objects.get(id=data['transaction_manager'])
            data['transaction_manager'] = manager.first_name
        if data['seller']:
            seller = SellerLead.objects.get(id=data['seller'])
            data['seller'] = seller.seller_name
        if data['company']:
            company = Company.objects.get(id=data['company'])
            data['company'] = company.title
        if data['buyer_contact_info']:
            buyer = Cash_Buyer.objects.get(id=data['buyer_contact_info'])
            data['buyer_contact_info'] = buyer.buyer_name
        if data['campaigns']:
            campaigns = MarketingCampaign.objects.get(id=data['campaigns'])
            data['campaigns'] = campaigns

        if data['purchase_contract_ratification_date_start']:
            purchase_contract_ratification_date_start = datetime.strptime(
                response.json()['purchase_contract_ratification_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            purchase_contract_ratification_date_start = datetime.strftime(purchase_contract_ratification_date_start,
                                                                          "%m/%d/%y %H:%M")
            data["purchase_contract_ratification_date_start"] = purchase_contract_ratification_date_start



        if data['contract_date_start']:
            contract_date_start = datetime.strptime(response.json()['contract_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            contract_date_start = datetime.strftime(contract_date_start, "%m/%d/%y %H:%M")
            data["contract_date_start"] = contract_date_start



        if data['showing_date_start']:
            showing_date_start = datetime.strptime(response.json()['showing_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            showing_date_start = datetime.strftime(showing_date_start, "%m/%d/%y %H:%M")
            data["showing_date_start"] = showing_date_start



        if data['deadline_to_accept_offer_start']:
            deadline_to_accept_offer_start = datetime.strptime(response.json()['deadline_to_accept_offer_start'],
                                                               "%Y-%m-%dT%H:%M:%SZ")
            deadline_to_accept_offer_start = datetime.strftime(deadline_to_accept_offer_start, "%m/%d/%y %H:%M")
            data["deadline_to_accept_offer_start"] = deadline_to_accept_offer_start

        if data['deadline_to_accept_offer_start']:
            deadline_to_accept_offer_end = datetime.strptime(response.json()['deadline_to_accept_offer_start'],
                                                             "%Y-%m-%dT%H:%M:%SZ")
            deadline_to_accept_offer_end = datetime.strftime(deadline_to_accept_offer_end, "%m/%d/%y %H:%M")
            data["deadline_to_accept_offer_end"] = deadline_to_accept_offer_end

        if data['emd_date_start']:
            emd_date_start = datetime.strptime(response.json()['emd_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            emd_date_start = datetime.strftime(emd_date_start, "%m/%d/%y %H:%M")
            data["emd_date_start"] = emd_date_start



        return render(request, 'xforce/transactions/view_transaction.html', data)


def date_to_db(date_val):
    specific_date1 = datetime.strptime(date_val, "%m/%d/%y %H:%M")
    return specific_date1


class EditTransaction(View):
    @method_decorator(login_required())
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'xforce_transactions/transaction/' + str(pk))
        json_response = response.json()

        user_name = json_response.get("transaction_manager")
        t_manager = UserProfile.objects.filter(user=user_name).first()

        user_name = json_response.get("seller")
        n_seller = SellerLead.objects.filter(pk=user_name).first()

        user_name = json_response.get("company")
        n_company = Company.objects.filter(pk=user_name).first()

        user_name = json_response.get("buyer_contact_info")
        buyer = Cash_Buyer.objects.filter(pk=user_name).first()

        user_name = json_response.get("campaigns")
        n_campaign = MarketingCampaign.objects.filter(pk=user_name).first()

        if json_response['purchase_contract_ratification_date_start']:
            purchase_contract_ratification_date_start = datetime.strptime(
                response.json()['purchase_contract_ratification_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            purchase_contract_ratification_date_start = datetime.strftime(purchase_contract_ratification_date_start,
                                                                          "%m/%d/%y %H:%M")
            json_response["purchase_contract_ratification_date_start"] = purchase_contract_ratification_date_start
        else:
            json_response['purchase_contract_ratification_date_start'] = str(json_response['purchase_contract_ratification_date_start']).replace("None", "")

        if json_response['contract_date_start']:
            contract_date_start = datetime.strptime(response.json()['contract_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            contract_date_start = datetime.strftime(contract_date_start, "%m/%d/%y %H:%M")
            json_response["contract_date_start"] = contract_date_start
        else:
            json_response['contract_date_start'] = str(json_response['contract_date_start']).replace("None","")

        if json_response['showing_date_start']:
            showing_date_start = datetime.strptime(response.json()['showing_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            showing_date_start = datetime.strftime(showing_date_start, "%m/%d/%y %H:%M")
            json_response["showing_date_start"] = showing_date_start
        else:
            json_response['showing_date_start'] = str(json_response['showing_date_start']).replace("None", "")

        if json_response['deadline_to_accept_offer_start']:
            deadline_to_accept_offer_start = datetime.strptime(response.json()['deadline_to_accept_offer_start'],
                                                               "%Y-%m-%dT%H:%M:%SZ")
            deadline_to_accept_offer_start = datetime.strftime(deadline_to_accept_offer_start, "%m/%d/%y %H:%M")
            json_response["deadline_to_accept_offer_start"] = deadline_to_accept_offer_start
        else:
            json_response['deadline_to_accept_offer_start'] = str(json_response['deadline_to_accept_offer_start']).replace("None", "")

        if json_response['emd_date_start']:
            emd_date_start = datetime.strptime(response.json()['emd_date_start'], "%Y-%m-%dT%H:%M:%SZ")
            emd_date_start = datetime.strftime(emd_date_start, "%m/%d/%y %H:%M")
            json_response["emd_date_start"] = emd_date_start
        else:
            json_response['emd_date_start'] = str(json_response['emd_date_start']).replace("None","")
        json_response['closing_date'] = str(json_response['closing_date']).replace("None","")
        json_response['actual_close_date'] = str(json_response['actual_close_date']).replace("None", "")

        context = {
            'is_edit': True,
            'seller_leads': get_seller_leads(request),
            'transaction_managers': comunity_people_with_role(request.user, "transaction"),
            'companies': get_company(request),
            'status_opt': get_status(),
            'potential_opt': get_potential(),
            'pending_stage_opt': get_pending_stage(),
            'title_actions_opt': get_title_actions(),
            'marketing_stage_opt': get_marketing_stage(),
            'assigned_stage_opt': get_assigned_stage(),
            'showing_opt': get_showing(),
            'cash_buyers': get_cash_buyers(request),
            'contract_actions': get_contract_action(),
            'lead_sources': get_lead_source(),
            'contract_delivery_opt': get_contract_delivery(),
            'campaigns': get_campaign(),
            'data': json_response,
            'manager': t_manager,
            'seller': n_seller,
            'company': n_company,
            'buyer': buyer,
            'campaign': n_campaign
        }
        return render(request, 'xforce/transactions/new_transactions.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        response = requests.get(BASE_API_URL + 'xforce_transactions/transaction/' + str(pk))
        json_response = response.json()

        # if post_values["final_gross_sales_price"] == "":
        #     post_values["final_gross_sales_price"] = 0
        # if post_values["contract_price"] == "":
        #     post_values["contract_price"] = 0
        # if post_values["misc_expenses"] == "":
        #     post_values["misc_expenses"] = 0
        #
        # gross_price = post_values["final_gross_sales_price"]
        # contract_price = post_values["contract_price"]
        # misc_exp = post_values["misc_expenses"]
        # post_values["actual_profit"] = str(int(gross_price) - int(contract_price))
        # actual_profit = post_values["actual_profit"]
        # post_values["actual_profit"] = str(int(actual_profit) - int(misc_exp))

        if request.POST.get('contract_date_start') != 'None':
            post_values['contract_date_start'] = date_to_db(request.POST.get('contract_date_start'))
        else:
            post_values['contract_date_start']= request.POST.get('contract_date_start').replace('None', '')


        c = request.POST.get('purchase_contract_ratification_date_start')
        if request.POST.get('purchase_contract_ratification_date_start') != 'None':
            if request.POST.get('purchase_contract_ratification_date_start'):
                post_values['purchase_contract_ratification_date_start'] = date_to_db(
                request.POST.get('purchase_contract_ratification_date_start'))
        else:
            post_values['purchase_contract_ratification_date_start']= c.replace('None', '')


        if request.POST.get('showing_date_start') != 'None':
            if request.POST.get('showing_date_start'):
                post_values['showing_date_start'] = date_to_db(request.POST.get('showing_date_start'))
        else:
            post_values['showing_date_start'] = request.POST.get('showing_date_start').replace('None', '')



        if request.POST.get('deadline_to_accept_offer_start') != 'None':
            if request.POST.get('deadline_to_accept_offer_start'):
                post_values['deadline_to_accept_offer_start'] = date_to_db(
                request.POST.get('deadline_to_accept_offer_start'))
        else:
            post_values['deadline_to_accept_offer_start']= request.POST.get('deadline_to_accept_offer_start').replace('None', '')

        if request.POST.get('emd_date_start') != 'None':
            if request.POST.get('emd_date_start'):
                post_values['emd_date_start'] = date_to_db(request.POST.get('emd_date_start'))
        else:
            post_values['emd_date_start'] = request.POST.get('emd_date_start').replace('None', '')

        if request.POST.get('closing_date') != 'None' and request.POST.get('closing_date'):
            if request.POST.get('closing_date'):
                if request.POST.get('closing_date') != json_response.get("closing_date"):
                    close_date = datetime.strptime(request.POST.get('closing_date'), "%m/%d/%y")
                    post_values['closing_date'] = datetime.strftime(close_date, "%Y-%m-%d")
                else:
                    post_values['closing_date'] = request.POST.get('closing_date')
        else:
            post_values['closing_date'] = request.POST.get('closing_date').replace('None','')

        if request.POST.get('actual_close_date') != 'None' and request.POST.get('actual_close_date'):
            if request.POST.get('actual_close_date') != json_response.get('actual_close_date'):
                post_values['actual_close_date'] = datetime.strftime(datetime.strptime(request.POST.get('actual_close_date'), "%m/%d/%y"), "%Y-%m-%d")
        else:
            post_values['actual_close_date'] = request.POST.get('actual_close_date').replace('None','')

        response = requests.get(BASE_API_URL + 'xforce_transactions/transaction/' + str(pk))
        json_response = response.json()

        if json_response.get("from_lead"):
            post_values["from_lead"] = True

        if request.FILES:
            response = requests.put(BASE_API_URL + 'xforce_transactions/transaction/' + str(pk) + '/', data=post_values,
                                files=request.FILES)
        else:
            post_values.pop('transaction_file')
            response = requests.put(BASE_API_URL + 'xforce_transactions/transaction/' + str(pk) + '/', data=post_values)


        if response.status_code == 200:

            send_sales = request.POST.get('pre_assigned_status')

            sales_dict = {}

            if send_sales:
                fetch_sales = sales.objects.filter(transactions=pk).first()

                if fetch_sales:
                    sales_update = sales.objects.filter(transactions=pk).update(
                        deals=response.json()['id'],

                        marketing_price=request.POST.get('marketing_price'), status=request.POST.get('status'))
                else:

                    sales_dict['created_by'] = request.user.id

                    sales_dict['deals'] = response.json()['id']
                    sales_dict['status'] = request.POST.get('status')
                    sales_dict['disposition_manager'] = request.user.id
                    sales_dict['from_transaction'] = True
                    if request.POST.get('marketing_price'):

                        sales_dict['marketing_price'] = request.POST.get('marketing_price')
                    sales_dict['transactions'] = response.json()['id']
                    sales_dict['showing'] = 'Showing Complete'

                    responsesales = requests.post(BASE_API_URL + 'sales/Sales/', data=json.dumps(sales_dict),
                                                  headers={'content-type': 'application/json'}, )
                    if responsesales.status_code == 201:
                        sale_dict = json.loads(responsesales.text)
                        sale = sales.objects.get(pk=sale_dict["id"])
                        is_assigned = round_robin_assignment(request, 'sale', sale)
                        if not is_assigned:
                            messages.error(request, "No disposition manger was assigned to sale.")

            trans = Transaction.objects.get(pk=response.json()['id'])
            buyer = str(request.POST.get('buyer_contact_info')) != str(json_response.get("buyer_contact_info"))
            comp = str(request.POST.get('company')) != str(json_response.get("company"))
            trans = Transaction.objects.get(pk=response.json()['id'])
            if json_response.get("contract_action") != request.POST.get('contract_action') or buyer or comp:



                if request.POST.get('contract_action') == 'Generate Assignment Contract':
                    generate_contract(request, trans)

                if request.POST.get('contract_action') == 'Email Assignment Contract To Title':
                    if request.POST.get('company'):
                        if str(request.POST.get('company')):
                            company = Company.objects.filter(id=request.POST.get('company')).first()
                            if not trans.transaction_file:
                                generate_contract(request, trans)

                            msg = EmailMessage('Contract', 'Below is attached Contract file', settings.EMAIL_HOST_USER, [company.email,])
                            msg.content_subtype = "html"
                            msg.attach_file('media/Transactions_Files/Contract_{}.pdf'.format(
                                trans.property_address.replace(" ", "_")))
                            msg.send()
                if request.POST.get('contract_action') == 'Email Assignment Contract':

                    if request.POST.get('buyer_contact_info'):
                        if str(request.POST.get('buyer_contact_info')):
                            if not trans.transaction_file:
                                generate_contract(request, trans)
                            buyer_info = Cash_Buyer.objects.filter(id=request.POST.get('buyer_contact_info')).first()
                            msg = EmailMessage('Contract', 'Below is attached Contract file', settings.EMAIL_HOST_USER, [buyer_info.email, ])
                            msg.content_subtype = "html"
                            msg.attach_file('media/Transactions_Files/Contract_{}.pdf'.format(
                                trans.property_address.replace(" ", "_")))
                            msg.send()
            if request.POST.get('title_actions'):

                if post_values['title_actions'] != json_response.get('title_actions'):

                    if post_values['title_actions'] == 'Email Contract To Title':
                        if post_values['company']:

                            email_contract = Company.objects.filter(id=post_values['company']).first()
                            subject = 'Thank you for registering to our site'
                            send_mail(subject,email_contract.title, settings.EMAIL_HOST_USER, [email_contract.email, ])

                    elif post_values['title_actions'] == 'Email Wire Number To Title':
                        if post_values['company']:

                            com_wire_no = Company.objects.filter(id=post_values['company']).first()
                            subject = 'Thank you for registering to our site'
                            send_mail(subject, post_values['wire_confirmation_number'], settings.EMAIL_HOST_USER, [com_wire_no.email, ])

            return redirect('transaction_list')

        manager = User.objects.filter(pk=post_values['transaction_manager']).first()

        errors = {}
        for (key, value) in response.json().items():
            errors[key] = value[0]
            context = {
                'errors': errors,
                'data': request.POST,
                'manager': manager
            }
        return render(request, 'xforce/transactions/new_transactions.html', context)


class DeleteTransaction(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        requests.delete(BASE_API_URL + 'xforce_transactions/transaction/' + str(pk))
        return redirect('transaction_list')

def generate_contract(request, trans):

    data = {
        'property_address': trans.property_address,
        'status': trans.status,
        'trans': trans.potential
    }
    pdf = render_to_pdf('xforce/transactions/pdf/contract.html', data)
    filename = "Contract {}.pdf".format(trans.property_address)
    trans.transaction_file.save(filename, File(BytesIO(pdf.content)))
    trans.save()
    return trans.transaction_file

# def send_contract(request, trans):
#     if not trans.transaction_file:
#         generate_contract(request, trans)
#     msg = send_mail('Contract', 'Below is attached Contract file', settings.EMAIL_HOST_USER,
#                        ['shahh8517@gmaail.com'])
#     msg.content_subtype = "html"
#     msg.attach_file('media/transaction_files/Contract_{}.pdf'.format(
#         trans.property_address.replace(" ", "_")))
#     msg.send()

