import json
from datetime import datetime
from io import BytesIO
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from rest_framework import generics
from xforce_appointment.models import Appointment
from payments.views import is_subscribed
from prospectx_new import settings
from prospectx_new.settings import STRIPE_PUBLISHABLE_KEY, BASE_API_URL
from user.models import UserProfile
from xforce.utils import send_sms, get_comunity_people, round_robin_assignment, assign_lead_id, \
    get_comunity_people_with_role
from xforce_transactions.models import Transaction
from .serializers import *
from .utils import render_to_pdf
from django.contrib import messages


class AddSellerLead(generics.ListCreateAPIView):
    queryset = SellerLead.objects.all().order_by('id')
    serializer_class = SellerLeadsSerializer


class SellerList(ListView):
    model = SellerLead
    template_name = 'xforce/seller_lead/seller_lead_list.html'

    def get_queryset(self):
        return SellerLead.objects.filter(user=self.request.user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(SellerList, self).get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['user_uuid'] = user_profile.xforce_uuid
        return context


class UpdateSellerLead(generics.RetrieveUpdateDestroyAPIView):
    queryset = SellerLead.objects.all().order_by('id')
    serializer_class = SellerLeadsSerializer


def get_stage_of_contract():
    stage_of_contract = []
    for stage in SellerLead.STAGE_OF_CONTACT:
        stage_of_contract.append(stage[0])
    return stage_of_contract


def get_lead_status():
    lead_status = []
    for status in SellerLead.LEAD_STATUS:
        lead_status.append(status[0])
    return lead_status


def get_temperature():
    temperature = []
    for temp in SellerLead.TEMPERATURE:
        temperature.append(temp[0])
    return temperature


def get_follow_up_in():
    follow_up_in = []
    for follow_up in SellerLead.FOLLOW_UP_IN:
        follow_up_in.append(follow_up[0])
    return follow_up_in


def get_occupancy():
    occupancy = []
    for occu in SellerLead.OCCUPANCY:
        occupancy.append(occu[0])
    return occupancy


def get_made_offer():
    made_offer = []
    for offer in SellerLead.MADE_OFFER:
        made_offer.append(offer[0])
    return made_offer


def get_offer_status():
    offer_status = []
    for status in SellerLead.OFFER_STATUS:
        offer_status.append(status[0])
    return offer_status


def get_closing_costs():
    closing_cost = []
    for cost in SellerLead.CLOSING_COSTS:
        closing_cost.append(cost[0])
    return closing_cost


def get_contract_delivery():
    contract_delivery = []
    for contract in SellerLead.CONTACT_DELIVERY:
        contract_delivery.append(contract[0])
    return contract_delivery


def get_contract_action():
    contract_action = []
    for action in SellerLead.CONTRACT_ACTION:
        contract_action.append(action[0])
    return contract_action


def get_lead_source():
    lead_source = []
    for source in SellerLead.LEAD_SOURCE:
        lead_source.append(source[0])
    return lead_source


def get_deal_status():
    deal_status = []
    for deal in SellerLead.DEAL_STATUS:
        deal_status.append(deal[0])
    return deal_status


class SellerLeadView(View):
    @method_decorator(login_required)
    def get(self, request):
        company = Company.objects.filter(user=request.user)
        follow_up = FollowUp.objects.all()
        campaign = MarketingCampaign.objects.all()
        major_market = MajorMarket.objects.all()

        return render(request, 'xforce/seller_lead/add_seller_lead.html',
                      {
                          # 'users': get_comunity_people(request.user),
                          'campaigns': campaign,
                          'majormarket': major_market,
                          'company': company,
                          'follow_up': follow_up,
                          'stage_of_contract': get_stage_of_contract(),
                          'lead_status': get_lead_status(),
                          'temperature': get_temperature(),
                          'follow_up_in': get_follow_up_in(),
                          'occupancy': get_occupancy(),
                          'made_offer': get_made_offer(),
                          'offer_status': get_offer_status(),
                          'closing_cost': get_closing_costs(),
                          'contract_delivery': get_contract_delivery(),
                          'contract_action': get_contract_action(),
                          'lead_source': get_lead_source(),
                          'deal_status': get_deal_status(),
                          'edit': 'no'

                      })

    @method_decorator(login_required)
    def post(self, request):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        if not request.POST.get("temperature"):
            post_values["temperature"] = "Cold"
        if not request.POST.get("contract_action"):
            post_values['contract_action'] = ""
        if post_values['lead_status'] == "":
            post_values['lead_status'] = "New Untouched"

        if request.POST.get('best_call_back_time'):
            best_call_back_time = request.POST.get('best_call_back_time')
            best_call_back_time = datetime.strptime(best_call_back_time, "%m/%d/%y %H:%M")
            post_values['best_call_back_time'] = best_call_back_time

        if request.POST.get('follow_up_specific_date'):
            specific_date = request.POST.get('follow_up_specific_date')
            specific_date = datetime.strptime(specific_date, "%m/%d/%y %H:%M")
            post_values['follow_up_specific_date'] = specific_date

        if request.POST.get('app_date'):
            appt_start = request.POST.get('app_date')
            appt_start = datetime.strptime(appt_start, "%m/%d/%y %H:%M")
            post_values['app_date'] = appt_start
        attempts(request, post_values, data=None)

        query = SellerLead.objects.filter(user__in=get_people(request.user), property_address_map=post_values['property_address_map']).first()
        if query:
            query_id = query.id
            if request.FILES:
                response = requests.put(BASE_API_URL + 'seller/add_seller/' + str(query_id) + '/', data=post_values,
                                        files=request.FILES)
            else:
                post_values.pop('lead_file')
                response = requests.put(BASE_API_URL + 'seller/add_seller/' + str(query_id) + '/', data=post_values)
        else:

            response = requests.post(BASE_API_URL + 'seller/add_seller/', data=post_values, files=request.FILES)

        if response.status_code == 200:
            data = requests.get(BASE_API_URL + 'seller/add_seller/' + str(query_id))
            seller_lead_dict = json.loads(response.text)
            seller_lead = SellerLead.objects.get(pk=seller_lead_dict["id"])
            is_created = send_lead_to_transaction(request, seller_lead)
            # if not is_created:
            #     messages.error(request, "Transaction not created")
            send_lead_to_appointment(request, seller_lead)
            perform_call_attempts(request, seller_lead, data, post_values)
            perform_made_offers(request, seller_lead, data ,post_values)
            perform_contract_actions(request, seller_lead, data)
            return redirect('seller_list')

        if response.status_code == 201:
            seller_lead_dict = json.loads(response.text)
            seller_lead = SellerLead.objects.get(pk=seller_lead_dict["id"])
            is_assigned = round_robin_assignment(request, 'seller_lead', seller_lead)
            if not is_assigned:
                messages.error(request, "No lead manger was assigned to lead.")
            data = None
            # is_created = send_lead_to_transaction(request, seller_lead)    #do not sending lead to transaction on create
            # if not is_created:
            #     messages.error(request, "Transaction not created")
            send_lead_to_appointment(request, seller_lead)
            perform_call_attempts(request, seller_lead, data, post_values)
            perform_made_offers(request, seller_lead, data, post_values)
            perform_contract_actions(request, seller_lead, data)
            return redirect('seller_list')
        # users = User.objects.all()

        # selected_lead_manager = ''
        # if post_values['lead_manager']:
        #     selected_lead_manager = User.objects.filter(pk=post_values['lead_manager']).first()

        selected_lead_by = ''
        if post_values['lead_by']:
            selected_lead_by = User.objects.filter(pk=post_values['lead_by']).first()

        selected_compaign = ''
        if post_values['campaign']:
            selected_compaign = MarketingCampaign.objects.get(id=post_values['campaign'])

        selected_market = ''
        if post_values['major_market']:
            selected_market = MajorMarket.objects.get(id=post_values['major_market'])

        nurture_campaign = ''
        if post_values['nurture_campaign']:
            nurture_campaign = FollowUp.objects.filter(pk=post_values['nurture_campaign']).first()

        selected_title_company = ''
        if post_values['title_company']:
            selected_title_company = Company.objects.filter(pk=post_values['title_company']).first()

        company = Company.objects.filter(user=request.user)
        follow_up = FollowUp.objects.all()
        campaign = MarketingCampaign.objects.all()
        major_market = MajorMarket.objects.all()
        error_dict = {}

        for (key, value) in response.json().items():  # keys
            error_dict.update({key: value[0]})
            print(error_dict)
            context = {
                'errors': error_dict,
                'data': request.POST,
                'stage_of_contract': get_stage_of_contract(),
                'lead_status': get_lead_status(),
                'temperature': get_temperature(),
                'follow_up_in': get_follow_up_in(),
                'occupancy': get_occupancy(),
                'made_offer': get_made_offer(),
                'offer_status': get_offer_status(),
                'closing_cost': get_closing_costs(),
                'contract_delivery': get_contract_delivery(),
                'contract_action': get_contract_action(),
                'lead_source': get_lead_source(),
                'deal_status': get_deal_status(),
                # 'lead_manager': selected_lead_manager,
                'nurture_campaign': nurture_campaign,
                'sel_title_company': selected_title_company,
                'selected_campaign': selected_compaign,
                'selected_lead_by': selected_lead_by,
                'users': get_comunity_people(request.user),
                'campaigns': campaign,
                'majormarket': major_market,
                'selected_market': selected_market,
                'company': company,
                'follow_up': follow_up
            }
        return render(request, 'xforce/seller_lead/add_seller_lead.html', context)


class EditSellerLeadView(View):
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'seller/add_seller/' + str(pk))
        company = Company.objects.filter(user=request.user)
        follow_up = FollowUp.objects.all()

        campaigns = MarketingCampaign.objects.all()
        majormarket = MajorMarket.objects.all()

        a = response.json()

        user_name = a.get("lead_manager")
        tem = a.get("temperature")
        attempt = a.get("stage_of_contact")
        ofer = a.get("made_offer")
        lead_manager = User.objects.filter(pk=user_name).first()
        user_name = a.get("lead_by")
        selected_lead_by = User.objects.filter(pk=user_name).first()

        title_name = a.get("title_company")
        selected_title_company = Company.objects.filter(pk=title_name).first()

        campaign = a.get("campaign")
        selected_campaign = MarketingCampaign.objects.filter(pk=campaign).first()

        major_market = a.get("major_market")
        selected_major_market = MajorMarket.objects.filter(pk=major_market).first()
        context_data = response.json()

        nurture_campaign = a.get("nurture_campaign")
        sel_nurture_campaign = FollowUp.objects.filter(pk=nurture_campaign).first()

        if context_data['follow_up_specific_date']:
            follow_up_specific = datetime.strptime(context_data['follow_up_specific_date'], "%Y-%m-%dT%H:%M:%SZ")
            follow_up_specific = datetime.strftime(follow_up_specific, "%m/%d/%y %H:%M")
            context_data['follow_up_specific_date'] = follow_up_specific

        if context_data['best_call_back_time']:
            best_call_back_time = datetime.strptime(context_data['best_call_back_time'], "%Y-%m-%dT%H:%M:%SZ")
            best_call_back_time = datetime.strftime(best_call_back_time, "%m/%d/%y %H:%M")
            context_data['best_call_back_time'] = best_call_back_time



        if context_data['app_date']:
            appt_start = datetime.strptime(context_data['app_date'], "%Y-%m-%dT%H:%M:%SZ")
            appt_start = datetime.strftime(appt_start, "%m/%d/%y %H:%M")
            context_data['app_date'] = appt_start

        context = {
            "is_edit": True ,
            'tem': tem,
            'attempt': attempt,
            'ofer': ofer,
            'users': get_comunity_people_with_role(request.user, "lead"),
            'campaigns': campaigns,
            'majormarket': majormarket,
            'company': company,
            'selected_lead_by': selected_lead_by,
            'selected_title_company': selected_title_company,
            'selected_major_market': selected_major_market,
            'selected_campaign': selected_campaign,
            'nurture_campaign': sel_nurture_campaign,
            'follow_up': follow_up,
            'stage_of_contract': get_stage_of_contract(),
            'lead_status': get_lead_status(),
            'temperature': get_temperature(),
            'follow_up_in': get_follow_up_in(),
            'occupancy': get_occupancy(),
            'made_offer': get_made_offer(),
            'offer_status': get_offer_status(),
            'closing_cost': get_closing_costs(),
            'contract_delivery': get_contract_delivery(),
            'contract_action': get_contract_action(),
            'lead_source': get_lead_source(),
            'deal_status': get_deal_status(),
            'data': context_data,
            'lead_manager': lead_manager,
            'edit': 'yes',
            'web_form': True,
            # 'lead_by': lead_by,
            # 'title_company': title_company,
        }
        return render(request, 'xforce/seller_lead/add_seller_lead.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        data = requests.get(BASE_API_URL + 'seller/add_seller/' + str(pk))
        post_values = request.POST.copy()
        post_values['user'] = request.user.id

        if post_values['lead_status'] == "":
            post_values['lead_status'] = "New Untouched"

        if request.POST.get('follow_up_specific_date'):
            specific_date = request.POST.get('follow_up_specific_date')
            specific_date = datetime.strptime(specific_date, "%m/%d/%y %H:%M")
            post_values['follow_up_specific_date'] = specific_date
        if request.POST.get('app_date'):
            appt_start = request.POST.get('app_date')
            appt_start = datetime.strptime(appt_start, "%m/%d/%y %H:%M")
            post_values['app_date'] = appt_start
        if request.POST.get('best_call_back_time'):
            best_call_back_time = request.POST.get('best_call_back_time')
            best_call_back_time = datetime.strptime(best_call_back_time, "%m/%d/%y %H:%M")
            post_values['best_call_back_time'] = best_call_back_time
        attempts(request,post_values, data)
        if request.FILES:
            response = requests.put(BASE_API_URL + 'seller/add_seller/' + str(pk) + '/', data=post_values,
                                    files=request.FILES)
        else:
            post_values.pop('lead_file')
        response = requests.put(BASE_API_URL + 'seller/add_seller/' + str(pk) + '/', data=post_values)

        if response.status_code == 200:
            seller_lead_dict = json.loads(response.text)
            seller_lead = SellerLead.objects.get(pk=seller_lead_dict["id"])
            res = send_lead_to_transaction(request, seller_lead)
            if not res:
                messages.error(request, "No transaction manger was assigned to transaction.")
            send_lead_to_appointment(request, seller_lead)
            perform_call_attempts(request, seller_lead, data, post_values)
            perform_made_offers(request, seller_lead, data ,post_values)
            perform_contract_actions(request, seller_lead, data)
            return redirect('seller_list')
        # users = User.objects.all()
        company = Company.objects.filter(user=request.user)
        follow_up = FollowUp.objects.all()
        campaign = MarketingCampaign.objects.all()
        major_market = MajorMarket.objects.all()
        error_dict = {}

        selected_title_company = ''
        if post_values['title_company']:
            selected_title_company = Company.objects.filter(pk=post_values['title_company']).first()

        selected_major_market = ''
        if post_values['major_market']:
            selected_major_market = MajorMarket.objects.filter(pk=post_values['major_market']).first()

        selected_campaign = ''
        if post_values['campaign']:
            selected_campaign = MarketingCampaign.objects.filter(pk=post_values['campaign']).first()

        selected_lead_manager = ''
        if post_values['lead_manager']:
            selected_lead_manager = User.objects.filter(pk=post_values['lead_manager']).first()

        selected_nurture_campaign = ''
        if request.POST.get('nurture_campaign'):
            selected_nurture_campaign = FollowUp.objects.filter(pk=post_values['nurture_campaign']).first()

        selected_lead_by = ''
        if post_values['lead_by']:
            selected_lead_by = User.objects.filter(pk=post_values['lead_by']).first()

        for (key, value) in response.json().items():  # keys
            error_dict.update({key: value[0]})
            context = {
                "is_edit": True,
                'errors': error_dict,
                'data': request.POST,
                'stage_of_contract': get_stage_of_contract(),
                'lead_status': get_lead_status(),
                'temperature': get_temperature(),
                'follow_up_in': get_follow_up_in(),
                'occupancy': get_occupancy(),
                'made_offer': get_made_offer(),
                'offer_status': get_offer_status(),
                'closing_cost': get_closing_costs(),
                'contract_delivery': get_contract_delivery(),
                'contract_action': get_contract_action(),
                'lead_source': get_lead_source(),
                'deal_status': get_deal_status(),
                'users': get_comunity_people_with_role(request.user, "lead"),
                'campaigns': campaign,
                'majormarket': major_market,
                'company': company,
                'follow_up': follow_up,
                'lead_manager': selected_lead_manager,
                'nurture_campaign':selected_nurture_campaign,
                'sel_title_company':selected_title_company,
                'selected_market': selected_major_market,
                'selected_campaign': selected_campaign,
                'selected_lead_by': selected_lead_by,
                'edit': 'yes'
            }
        return render(request, 'xforce/seller_lead/add_seller_lead.html', context)


class ViewSellerLeadView(View):
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'seller/add_seller/' + str(pk))
        data = response.json()
        if User.objects.filter(id=data['lead_manager']).exists():
            lead_manager = User.objects.get(id=data['lead_manager'])
            data['lead_manager'] = lead_manager.first_name
        if User.objects.filter(id=data['lead_by']).exists():
            lead_by = User.objects.get(id=data['lead_by'])
            data['lead_by'] = lead_by.first_name
        if MajorMarket.objects.filter(id=data['major_market']).exists():
            major_market = MajorMarket.objects.get(id=data['major_market'])
            data['major_market'] = major_market.title
        if MarketingCampaign.objects.filter(id=data['campaign']):
            campaign = MarketingCampaign.objects.get(id=data['campaign'])
            data['campaign'] = campaign.title
        if Company.objects.filter(id=data['title_company']).exists():
            title_company = Company.objects.get(id=data['title_company'])
            data['title_company'] = title_company.title
        if data['nurture_campaign']:
            nurture_campaign = FollowUp.objects.get(id=data['nurture_campaign'])
            data['nurture_campaign'] = nurture_campaign.title
        if data['follow_up_specific_date']:
            follow_up_specific = datetime.strptime(data['follow_up_specific_date'], "%Y-%m-%dT%H:%M:%SZ")
            follow_up_specific = datetime.strftime(follow_up_specific, "%m/%d/%y %H:%M")
            data['follow_up_specific_date'] = follow_up_specific

        if data['app_date']:
            appt_start = datetime.strptime(data['app_date'], "%Y-%m-%dT%H:%M:%SZ")
            appt_start = datetime.strftime(appt_start, "%m/%d/%y %H:%M")
            data['app_date'] = appt_start

        if data['date']:
            date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
            date = datetime.strftime(date, "%m/%d/%y %H:%M")
            data['date'] = date

        return render(request, 'xforce/seller_lead/view_seller_lead.html', data)


class DeleteSellerView(View):
    @method_decorator(login_required())
    def get(self, request, pk):
        requests.delete(BASE_API_URL + 'seller/add_seller/' + str(pk))
        return redirect('seller_list')


def send_lead_to_transaction(req, seller_lead):
    if req.POST.get('deal_action'):
        get_trans = Transaction.objects.filter(seller_id=seller_lead.id).first()
        if get_trans:
            Transaction.objects.filter(seller_id=seller_lead.id).update(
                property_address=seller_lead.property_address_map,
                status='Pending', potential='Wholesale', seller=seller_lead,
                transaction_manager=seller_lead.lead_manager, hoa=seller_lead.hoa,
                contract_price=seller_lead.contract_offer_amt,
                original_purchase_emd_amount=seller_lead.emd,
                company=seller_lead.title_company,
                lead_source=seller_lead.lead_source,
                detailed_source=seller_lead.detailed_source,
                campaigns=seller_lead.campaign,
                user=req.user

                )
        else:
            trans = Transaction.objects.create(property_address=seller_lead.property_address_map,
                                       status='Pending', potential='Wholesale', seller=seller_lead,
                                       transaction_manager=seller_lead.lead_manager, hoa=seller_lead.hoa,
                                       contract_price=seller_lead.contract_offer_amt,
                                       original_purchase_emd_amount=seller_lead.emd,
                                       company=seller_lead.title_company,
                                       lead_source=seller_lead.lead_source,
                                       detailed_source=seller_lead.detailed_source,
                                       campaigns=seller_lead.campaign,
                                       user=req.user,
                                       from_lead=True
                                       )
            res = round_robin_assignment(req, "transaction", trans)
            if not res:
                return False
        return True


def send_lead_to_appointment(req, seller_lead):
    if req.POST.get('set_appointment'):
        get_appt = Appointment.objects.filter(seller=seller_lead.id).first()
        if req.POST.get("app_date"):
            if get_appt:
                Appointment.objects.filter(seller=seller_lead.id).update(
                    user = req.user,
                    seller=seller_lead,
                    appt_date_start = seller_lead.app_date,
                    property_address = seller_lead.property_address_map,
                    who_set_this_appt = req.user,
                    going_on_appt = req.user
                    )
            else:
                Appointment.objects.create(
                    seller=seller_lead,
                    appt_date_start=seller_lead.app_date,
                    property_address=seller_lead.property_address_map,
                    who_set_this_appt=req.user,
                    going_on_appt=req.user,
                    user = req.user
                )


def generate_contract(request, seller_lead):
    data = {
        'prosperty_address': seller_lead.property_address_map,
        'contract_offer_amt': seller_lead.contract_offer_amt,
        'emd': seller_lead.emd
    }
    pdf = render_to_pdf('xforce/seller_lead/pdf/contract.html', data)
    filename = "Contract {}.pdf".format(seller_lead.property_address_map)
    seller_lead.lead_file.save(filename, File(BytesIO(pdf.content)))
    seller_lead.save()


def send_contract(request, seller_lead):
    if not seller_lead.lead_file:
        generate_contract(request, seller_lead)
    msg = EmailMessage('Contract', 'Below is attached Contract file', settings.EMAIL_HOST_USER,
                       [seller_lead.seller_email])
    msg.content_subtype = "html"
    msg.attach_file('media/seller_lead_files/Contract_{}.pdf'.format(
        seller_lead.property_address_map.replace(" ", "_")))
    msg.send()


def perform_contract_actions(request, seller_lead, data):
    if not data:
        if request.POST.get('contract_action') == 'Generate Contract':
            generate_contract(request, seller_lead)
        elif request.POST.get('contract_action') == 'Email Contract':
            send_contract(request, seller_lead)
    if data:
        data = data.json()
        if data.get('contract_action') == request.POST.get('contract_action') :
            pass

        if (data.get('contract_action') == "E Signature" or data.get('contract_action') == 'No Value' or data.get('contract_action') == '' or data.get('contract_action') == 'Email Contract') and request.POST.get('contract_action') == 'Generate Contract':
            generate_contract(request, seller_lead)

        if (data.get('contract_action') == "E Signature" or data.get('contract_action') == 'No Value' or data.get('contract_action') == '' or data.get('contract_action') == 'Generate Contract') and request.POST.get('contract_action') == 'Email Contract':
            send_contract(request, seller_lead)


def perform_call_attempts(request, lead, data, post_values):
    stage_of_contact_list = ["Call Attempt 1", "Call Attempt 2", "Call Attempt 3", "Call Attempt 4",
                             "Final Attempt", "CONTACTED"]
    subject_list = ["Call Attempt 1 Email", "Call Attempt 2 Email", "Call Attempt 3 Email", "Call Attempt 4 Email",
                    "Final Attempt", "CONTACTED Email"]
    if not data:
        if post_values['stage_of_contact']:
            val = post_values['stage_of_contact']
            if val in stage_of_contact_list:
                email_content = "This is message from {}"
                subject = subject_list[stage_of_contact_list.index(val)]
                send_mail(subject, email_content.format(subject), settings.EMAIL_HOST_USER,
                          [request.POST.get('seller_email')])
                to = lead.seller_phone
                body = email_content
                e = send_sms(to, body)
    if data:
        data = data.json()
        if data.get('stage_of_contact') == post_values["stage_of_contact"]:
            pass

        if data.get('stage_of_contact') != post_values["stage_of_contact"]:
            val = post_values["stage_of_contact"]
            if val in stage_of_contact_list:
                email_content = "This is message from {}"
                subject = subject_list[stage_of_contact_list.index(val)]
                send_mail(subject, email_content.format(subject), settings.EMAIL_HOST_USER,
                          [request.POST.get('seller_email')])
                to = lead.seller_phone
                body = email_content
                e = send_sms(to, body)


def perform_made_offers(request, lead, data, post_values ):
    made_offer_list = ["Make Attempt 1", "Make Attempt 2", "Make Attempt 3", "Make Attempt 4", "Made Offer"]
    made_offer_subject_list = ["Make Attempt 1 Email", "Make Attempt 2 Email", "Make Attempt 3 Email",
                               "Make Attempt 4", "Made Offer"]

    if not data:
        if post_values['made_offer']:
            val = post_values['made_offer']
            if val in made_offer_list:
                email_content = "This is message from {}"
                subject = made_offer_subject_list[made_offer_list.index(val)]
                send_mail(subject, email_content.format(subject), settings.EMAIL_HOST_USER,
                          [request.POST.get('seller_email')])
                to = lead.seller_phone
                body = email_content
                send_sms(to, body)

    if data:
        data = data.json()
        if data.get('made_offer') != post_values['made_offer']:
            val = post_values['made_offer']
            if val in made_offer_list:
                email_content = "This is message from {}"
                subject = made_offer_subject_list[made_offer_list.index(val)]
                send_mail(subject, email_content.format(subject), settings.EMAIL_HOST_USER,
                          [request.POST.get('seller_email')])
                to = lead.seller_phone
                body = email_content
                send_sms(to, body)


def attempts(request, post_values, data):
    if not data:
        if request.POST.get("call"):
            post_values["stage_of_contact"] = post_values["call"]
        else:
            post_values["stage_of_contact"] = "Call Attempt 1"

        if request.POST.get("call") == "CONTACTED":
            if request.POST.get("offer"):
                post_values["made_offer"] = post_values["offer"]
            else:
                post_values["made_offer"] = "Make Attempt 1"
        else:
            post_values["made_offer"] = ""

    if data:
        j_data = data.json()

        if j_data.get("stage_of_contact") == "Call Attempt 1" and post_values["call"] == "Call Attempt 1":
            post_values["stage_of_contact"] = "Call Attempt 2"
        elif j_data.get("stage_of_contact") == "Call Attempt 2" and post_values["call"] == "Call Attempt 2":
            post_values["stage_of_contact"] = "Call Attempt 3"
        elif j_data.get("stage_of_contact") == "Call Attempt 3" and post_values["call"] == "Call Attempt 3":
            post_values["stage_of_contact"] = "Call Attempt 4"
        elif j_data.get("stage_of_contact") == "Call Attempt 4" and post_values["call"] == "Call Attempt 4":
            post_values["stage_of_contact"] = "Final Attempt"
        elif j_data.get("stage_of_contact") == "Final Attempt" and post_values["call"] == "Final Attempt":
            post_values["stage_of_contact"] = "CONTACTED"
        elif j_data.get("stage_of_contact") == "CONTACTED" and post_values["call"] == "CONTACTED":
            post_values["stage_of_contact"] = "CONTACTED"
        else:
            if j_data.get("stage_of_contact") != post_values["call"]:
                post_values["stage_of_contact"] = post_values["call"]

        if j_data.get("stage_of_contact") == "CONTACTED":
            if post_values["offer"] == "":
                post_values["made_offer"] = "Make Attempt 1"
            if j_data.get("made_offer") == "Make Attempt 1" and post_values["offer"] == "Make Attempt 1":
                post_values["made_offer"] = "Make Attempt 2"
            elif j_data.get("made_offer") == "Make Attempt 2" and post_values["offer"] == "Make Attempt 2":
                post_values["made_offer"] = "Make Attempt 3"
            elif j_data.get("made_offer") == "Make Attempt 3" and post_values["offer"] == "Make Attempt 3":
                post_values["made_offer"] = "Make Attempt 4"
            elif j_data.get("made_offer") == "Make Attempt 4" and post_values["offer"] == "Make Attempt 4":
                post_values["made_offer"] = "Made Offer"
            elif j_data.get("made_offer") == "Made Offer" and post_values["offer"] == "Made Offer":
                post_values["made_offer"] = "Offer Not Made"
            elif j_data.get("made_offer") == "Offer Not Made" and post_values["offer"] == "Offer Not Made":
                post_values["made_offer"] = "Offer Not Made"

            else:
                if j_data.get("made_offer") != post_values["offer"]:
                    post_values["made_offer"] = post_values["offer"]

        else:
            post_values["made_offer"] = post_values["offer"]


def get_people(usr):
    user_comunity_people = []
    sub_users_list = []
    usr_profile = UserProfile.objects.get(user_id=usr.id)

    if usr_profile.role.role_name == 'Admin User':
        user_comunity_people.append(usr_profile.user)
        sub_users_list = UserProfile.objects.filter(created_by=usr_profile)

    elif usr_profile.role.role_name == 'Sub User':
        get_admin = usr_profile.created_by  # sub user's admin
        user_comunity_people.append(get_admin.user)
        sub_users_list = UserProfile.objects.filter(created_by=get_admin).exclude(user = usr_profile.user)

    for each_profile in sub_users_list:
        user_comunity_people.append(each_profile.user)
    return user_comunity_people