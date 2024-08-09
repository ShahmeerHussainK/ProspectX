import datetime
import json
import os
import traceback
from math import ceil
from xml.etree import ElementTree as etree

from django.db.models import IntegerField, Value
from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import stripe
from django.contrib import messages
from django.conf import settings
from django.core.handlers import exception
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import Q, Count, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from elasticsearch_dsl.connections import connections
from oauth2client.service_account import ServiceAccountCredentials

from filter_prospects.documents import ProspectDocument
from filter_prospects.models import Prospect_Properties, File, List, Tag, AddressValidationCounter
from prospectx_new.settings import Godaddy_api_key, Godaddy_secret_key, BASE_DIR
from user.models import UserStripeDetail, UserProfile
from xsiteApp.forms import *
from xsiteApp.models import *
from xsiteApp.serializers import *
import requests
import whois
import time
from oauth2client.service_account import ServiceAccountCredentials
import pytz
from django.core.files.storage import FileSystemStorage
import decimal
from user.models import Revenue
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

# API key and secret are sent in the header
headers = {"Authorization": "sso-key {}:{}".format(Godaddy_api_key, Godaddy_secret_key)}

# Domain availability and purchasing end points
availability_url = "https://api.ote-godaddy.com/v1/domains/available"
purchasing_url = "https://api.ote-godaddy.com/v1/domains/purchase"
validate_url = "https://api.ote-godaddy.com/v1/domains/purchase/validate"
domain_url = "https://api.sandbox.namecheap.com/xml.response"


# Create your views here.
def xsite_websites(request):
    profile = UserProfile.objects.get(user=request.user)
    allow_sites = True
    allowed_sites = 1
    if profile.role.role_name == "Sub User":
        admin_user = profile.created_by.user
    else:
        admin_user = request.user
    users = UserProfile.objects.filter(created_by__user=admin_user).values('user')
    if not MembershipDetails.objects.filter(user=request.user).exists():
        MembershipDetails.objects.create(user=request.user,
                                         membership_plan=MembershipPlan.objects.first(),
                                         subscription_end_date=date.today())
    membership_details = MembershipDetails.objects.get(user=admin_user)
    if UserStripeDetail.objects.filter(user=admin_user).exists():
        # customer = UserStripeDetail.objects.get(user=admin_user).customer_id
        # subscriptions = stripe.Subscription.list(customer=customer)
        # print(membership_details.subscription_id)
        # print(subscriptions)
        # if membership_details.subscription_id in subscriptions['data'][0]['id']:
        try:
            if membership_details.subscription_id:
                stripe.Subscription.retrieve(membership_details.subscription_id)
                subscription = stripe.Subscription.retrieve(membership_details.subscription_id)
                membership_details.subscription_end_date = time.strftime("%Y-%m-%d", time.gmtime(
                    subscription.current_period_end))
                membership_details.save()
        except:
            print(traceback.print_exc())

    sites = Websites.objects.filter((Q(user=admin_user) | Q(user__in=users)) & Q(is_deleted=False)).order_by('-id')
    if MembershipDetails.objects.filter(user=admin_user, subscription_status="Subscribed").exists():
        allowed_sites = 3
    else:
        if MembershipDetails.objects.filter(user=admin_user, subscription_status="Cancelled").exists():
            monthly_subscription = MembershipDetails.objects.get(user=admin_user, subscription_status="Cancelled")
            if date.today() >= monthly_subscription.subscription_end_date:
                allow_sites = False
            else:
                allowed_sites = 3

    total_sites = allowed_sites - sites.count()
    return render(request, "xsite/websites.html",
                  {"websites": sites, "allowed_sites": total_sites, "allow_sites": allow_sites,
                   "site_count": allowed_sites, "user": request.user.email})


def website_setup(request):
    site_design = SiteDesign.objects.all().order_by('id')
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        profile = UserProfile.objects.get(user=profile.created_by.user)

    site_categories = SiteCategory.objects.all()
    # target_buyer = TargetAudience.objects.filter(audience__audience_name="Buyer")
    # target_seller = TargetAudience.objects.filter(audience__audience_name="Seller")
    return render(request, "xsite/website_setup.html",
                  {"site_design": site_design,
                   "settings": profile,
                   "site_categories": site_categories})  # , "target_buyer": target_buyer, "target_seller": target_seller})


def get_site_designs(request, category, stype):
    data = dict()
    try:
        site_type = True
        if stype == "website":
            site_type = False

        if int(category) == 1:
            data['buyer_sites'] = SiteDesignSerializer(
                SiteDesign.objects.filter(category__pk=category, is_lander_page=site_type,
                                          audience__audience_name="Buyer").order_by('id'), many=True).data
            data['seller_sites'] = SiteDesignSerializer(
                SiteDesign.objects.filter(category__pk=category, is_lander_page=site_type,
                                          audience__audience_name="Seller").order_by('id'), many=True).data
        else:
            data['sites'] = SiteDesignSerializer(
                SiteDesign.objects.filter(category__pk=category, is_lander_page=site_type), many=True).data
        return JsonResponse(data)
    except:
        data['message'] = "There is some error!"
        return JsonResponse(data, status=404)


# def get_content_pack(request, pk):
#     data = dict()
#     content_pack = ContentPack.objects.filter(target_audience__id=pk)
#     serializer = ContentPackSerializer(content_pack, many=True)
#     data['content_pack'] = serializer.data
#     return JsonResponse(data)


def delete_xsite_websites(request, pk):
    try:
        if Websites.objects.filter(pk=pk).exists():
            Websites.objects.filter(pk=pk).update(is_deleted=True)
            # Websites.objects.filter(pk=pk).delete()
            messages.add_message(request, messages.INFO, 'Site deleted successfully!')
            return redirect("/xsite/xsite_websites")
        else:
            messages.add_message(request, messages.INFO, 'Site does not exist!')
            return redirect("/xsite/xsite_websites")
    except:
        print(traceback.format_exc())
        messages.add_message(request, messages.INFO, 'There was an error!')
        return redirect("/xsite/xsite_websites")


def delete_xsite_websites_ajax(request, pk):
    data = dict()
    try:
        if Websites.objects.filter(pk=pk).exists():
            # Websites.objects.filter(pk=pk).delete()
            Websites.objects.filter(pk=pk).update(is_deleted=True)

            profile = UserProfile.objects.get(user=request.user)
            if profile.role.role_name == "Sub User":
                admin_user = profile.created_by.user
                users = UserProfile.objects.filter(created_by__user=admin_user).values('user')
                print(users)
                sites = Websites.objects.filter(
                    (Q(user=admin_user) | Q(user__in=users)) & Q(is_deleted=False)).order_by('-id')

            else:
                users = UserProfile.objects.filter(created_by__user=request.user).values('user')
                print(users)
                sites = Websites.objects.filter(
                    (Q(user=request.user) | Q(user__in=users)) & Q(is_deleted=False)).order_by('-id')
            serializer = WebsiteSerializer(sites, many=True)
            data['websites'] = serializer.data
            print(len(sites))
            data['site_count'] = len(sites)
            data['message'] = "Site deleted successfully!"
            return JsonResponse(data)
        else:
            data['message'] = "Site does not exist!"
            return JsonResponse(data, status=404)
    except:
        print(traceback.format_exc())
        data['message'] = "There was an error!"
        return JsonResponse(data, status=400)


def addYears(d, years):
    try:
        return d.replace(year=d.year + int(years))
    except ValueError:
        return d + (date(d.year + years, d.month, d.date) - date(d.year, d.month, d.date))


def add_site(request):
    try:
        msg = ""
        domain1 = request.POST.get("domain1")
        domain2 = request.POST.get("domain2")
        domain1_ext = request.POST.get("price")
        domain2_ext = request.POST.get("extension")
        duration = request.POST.get("duration")
        dial_code = request.POST.get("dial_code")
        if domain1:
            domain = domain1 + domain1_ext
        elif domain2:
            domain = domain2 + domain2_ext
            duration = 0
        # content_pack = request.POST.get("content_pack")
        site_design = request.POST.get("site_design")
        form = SettingsForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                site_design_obj = SiteDesign.objects.get(pk=site_design)
                content_pack_obj = site_design_obj.content_pack  # ContentPack.objects.get(pk=content_pack)
                site = Websites.objects.create(user=request.user, domain=domain,  # content_pack=content_pack_obj,
                                               site_design=site_design_obj,
                                               renewal_date=addYears(date.today(), duration))
                setting = form.save(commit=False)
                setting.site = site
                setting.save()

                TemplateContent.objects.create(site=site, content_pack_name=content_pack_obj.content_pack_name,
                                               html_head_content=site_design_obj.html_head_content,
                                               html_body_content=site_design_obj.html_body_content,
                                               logo=content_pack_obj.logo,
                                               banner_title=content_pack_obj.banner_title,
                                               banner_button_text=content_pack_obj.banner_button_text,
                                               about_us_title=content_pack_obj.about_us_title,
                                               about_us_desc=content_pack_obj.about_us_desc,
                                               video_link=content_pack_obj.video_link,
                                               video_title=content_pack_obj.video_title,
                                               video_desc=content_pack_obj.video_desc,
                                               testi_1_company_name=content_pack_obj.testi_1_company_name,
                                               testi_1_person_name=content_pack_obj.testi_1_person_name,
                                               testi_1_text=content_pack_obj.testi_1_text,
                                               testi_2_company_name=content_pack_obj.testi_2_company_name,
                                               testi_2_person_name=content_pack_obj.testi_2_person_name,
                                               testi_2_text=content_pack_obj.testi_2_text,
                                               testi_3_company_name=content_pack_obj.testi_3_company_name,
                                               testi_3_person_name=content_pack_obj.testi_3_person_name,
                                               testi_3_text=content_pack_obj.testi_3_text,
                                               other_details_title=content_pack_obj.other_details_title,
                                               other_details_desc=content_pack_obj.other_details_desc,
                                               call_to_action_text=content_pack_obj.call_to_action_text)
                Mail.objects.create(site=site, from_email="support@prospectx.com",
                                    subject="Xsite Email Assistance", content="Hi! We will contact you soon.")
                if domain1:
                    #     availability_res = []
                    #
                    #     print("------------------ Availability Check -----------------------")
                    #     print(availability_res)
                    #
                    #     root = etree.fromstring(availability_res.content)
                    #     for elem in root.iter():
                    #         if elem.tag == '{http://api.namecheap.com/xml.response}DomainCheckResult':
                    #             if elem.attrib['Available'] == 'true':
                    #                 print("Available")
                    #                 price_res = requests.post(url, params={'ApiUser': ApiUser, 'ApiKey': ApiKey,
                    #                                                        'Command': "namecheap.users.getPricing",
                    #                                                        'UserName': UserName, 'ClientIp': ClientIp,
                    #                                                        'ProductType': "DOMAIN",
                    #                                                        'ProductCategory': "DOMAINS",
                    #                                                        'ProductName': domain1_ext[1:]})
                    #
                    #                 print("------------------ Pricing Check -----------------------")
                    #                 print(price_res)
                    #                 print(price_res.text)
                    #
                    #                 pricing_root = etree.fromstring(price_res.content)
                    #                 price_root = pricing_root[3][0][0]
                    #                 for resp in price_root:
                    #                     if resp.attrib['Name'] == "register":
                    #                         for product_type in resp:
                    #                             if product_type.attrib['Name'] == domain1_ext[1:]:
                    #                                 for pricing_result in product_type:
                    #                                     if pricing_result.attrib['Duration'] == duration:
                    #                                         price = pricing_result.attrib['Price']
                    #                                         additional = pricing_result.attrib['AdditionalCost']
                    #
                    #                 total_price = float(price) + float(additional)
                    #                 print(total_price)
                    #                 extra = (total_price * 10) / 100
                    #                 print(extra)
                    #                 amount = round(total_price + extra, 2)
                    #                 print(amount)
                    #                 print(amount * 100)
                    amount = 100
                    site.domain_price = amount
                    site.save()
                    profile = UserProfile.objects.get(user=request.user)

                    if profile.role.role_name == "Sub User":
                        user = profile.created_by.user
                    else:
                        user = request.user

                    # customer_id = UserStripeDetail.objects.get(user=user).customer_id
                    # charge = stripe.Charge.create(
                    #     amount=round(amount * 100),
                    #     currency='usd',
                    #     customer=customer_id,  # Previously stored, then retrieved
                    # )
                    # print(charge.id)
                    # if charge.id:
                    #     phone = "+" + dial_code + "." + setting.phone.replace('-', '')
                    #
                    #     body = {
                    #         'ApiUser': ApiUser,
                    #         'ApiKey': ApiKey,
                    #         'Command': "namecheap.domains.create",
                    #         'UserName': UserName,
                    #         'ClientIp': ClientIp,
                    #
                    #         "AdminAddress1": setting.address,
                    #         "AdminCity": setting.city,
                    #         "AdminCountry": "US",
                    #         "AdminPostalCode": setting.zipcode,
                    #         "AdminStateProvince": setting.state,
                    #         "AdminEmailAddress": setting.contact_email,
                    #         "AdminFirstName": request.user.first_name,
                    #         "AdminLastName": request.user.last_name,
                    #         "AdminPhone": phone,
                    #
                    #         "AuxBillingAddress1": setting.address,
                    #         "AuxBillingCity": setting.city,
                    #         "AuxBillingCountry": "US",
                    #         "AuxBillingPostalCode": setting.zipcode,
                    #         "AuxBillingStateProvince": setting.state,
                    #         "AuxBillingEmailAddress": setting.contact_email,
                    #         "AuxBillingFirstName": request.user.first_name,
                    #         "AuxBillingLastName": request.user.last_name,
                    #         "AuxBillingPhone": phone,
                    #
                    #         "RegistrantAddress1": setting.address,
                    #         "RegistrantCity": setting.city,
                    #         "RegistrantCountry": "US",
                    #         "RegistrantPostalCode": setting.zipcode,
                    #         "RegistrantStateProvince": setting.state,
                    #         "RegistrantEmailAddress": setting.contact_email,
                    #         "RegistrantFirstName": request.user.first_name,
                    #         "RegistrantLastName": request.user.last_name,
                    #         "RegistrantPhone": phone,
                    #
                    #         "TechAddress1": setting.address,
                    #         "TechCity": setting.city,
                    #         "TechCountry": "US",
                    #         "TechPostalCode": setting.zipcode,
                    #         "TechStateProvince": setting.state,
                    #         "TechEmailAddress": setting.contact_email,
                    #         "TechFirstName": request.user.first_name,
                    #         "TechLastName": request.user.last_name,
                    #         "TechPhone": phone,
                    #
                    #         'DomainName': domain,
                    #         "Years": duration,
                    #     }
                    #
                    #     purchase_res = requests.get(url, params=body)
                    #
                    #     print("------------------ Purchase Check -----------------------")
                    #     print(purchase_res)
                    #     print(purchase_res.text)
                    #
                    #     purchase_root = etree.fromstring(purchase_res.content)
                    #     for elem in purchase_root.iter():
                    #         if elem.tag == '{http://api.namecheap.com/xml.response}DomainCreateResult':
                    #             if elem.attrib['Registered'] == 'true':
                    #                 pointing_res = requests.post(url, params={'ApiUser': ApiUser, 'ApiKey': ApiKey,
                    #                                                           'Command': "namecheap.domains.dns.setHosts",
                    #                                                           'UserName': UserName,
                    #                                                           'ClientIp': ClientIp,
                    #                                                           'SLD': domain1, 'TLD': domain1_ext[1:],
                    #                                                           'HostName1': '@',
                    #                                                           'RecordType1': 'FRAME',
                    #                                                           'Address1': 'http://127.0.0.1:8000/xsite/' + domain1 + domain1_ext[
                    #                                                                                                                  1:] + '/',
                    #                                                           'HostName2': 'www',
                    #                                                           'RecordType2': 'FRAME',
                    #                                                           'Address2': 'http://127.0.0.1:8000/xsite/' + domain1 + domain1_ext[
                    #                                                                                                                  1:] + '/'
                    #                                                           })
                    #                 print("------------------ Pointing Check -----------------------")
                    #                 print(pointing_res)
                    #                 print(pointing_res.text)
                    #                 root = etree.fromstring(pointing_res.content)
                    #                 for elem in root.iter():
                    #                     if elem.tag == '{http://api.namecheap.com/xml.response}DomainDNSSetHostsResult':
                    #                         if elem.attrib['IsSuccess'] == 'true':
                    #                             messages.add_message(request, messages.INFO,
                    #                                                  'Site Added Successfully! It can take about 30 minutes for this domain to properly set up')
                    #                             return redirect("/xsite/xsite_websites")
                    #                         else:
                    #                             refund = stripe.Refund.create(
                    #                                 charge=charge.id,
                    #                             )
                    #                             print(refund.id)
                    #                             msg = "Domain Pointing Error! Kindly try again later."
                    #                             raise exception
                    #             else:
                    #                 refund = stripe.Refund.create(
                    #                     charge=charge.id,
                    #                 )
                    #                 print(refund.id)
                    #                 msg = "Domain Purchase Error! Kindly try again later."
                    #                 raise exception
                    #     # refund = stripe.Refund.create(
                    #     #     charge=charge.id,
                    #     # )
                    #     # print(refund.id)
                    #     raise exception
                    # else:
                    #     msg = "Domain Payment Unsuccessful! Please try again later"
                    #     raise exception
                if (True):
                    site.is_existing = True
                    site.save()
                    messages.add_message(request, messages.INFO,
                                         'Site Added Successfully! Please point your domain to the following url: http://127.0.0.1:8000/xsite/' + domain2 + domain2_ext + '/')
                    return redirect("/xsite/xsite_websites")
        else:
            print(traceback.print_exc())
            messages.add_message(request, messages.INFO, 'There was an error!')
            return redirect("/xsite/xsite_websites")
    except:
        print(traceback.format_exc())
        if msg:
            messages.add_message(request, messages.INFO, msg)
        else:
            messages.add_message(request, messages.INFO, 'There was an error!')
        return redirect("/xsite/xsite_websites")


def save_mail(request, pk):
    try:
        form = MailForm(request.POST)
        if form.is_valid():
            Mail.objects.filter(site__id=pk).update(from_email=form.cleaned_data['from_email'],
                                                    subject=form.cleaned_data['subject'],
                                                    content=form.cleaned_data['content'])
            data = {'message': "Mail updated Successfully!"}
            return JsonResponse(data)
        else:
            print(form.errors)
            data = {'mail_form': form.errors}
            return JsonResponse(data, status=400)
    except:
        print(traceback.format_exc())
        data = {'message': "There was an error!"}
        return JsonResponse(data, status=400)


def get_mail_data(request, pk):
    data = dict()
    mail = Mail.objects.get(site__id=pk)
    serializer = MailSerializer(mail)
    data['mail'] = serializer.data
    return JsonResponse(data)


@xframe_options_exempt
def site_preview(request, pk):
    buyer_options = BuyerOptions.objects.all()
    favicon = TemplateContent.objects.get(site__pk=pk).logo
    listing_options = ListingOptions.objects.all()
    site_design = Websites.objects.get(pk=pk).site_design.template_name
    return render(request, "xsite/site_design_templates/xsite_template_preview.html",
                  {"site_id": pk, "buyer_options": buyer_options, "listing_options": listing_options,
                   "site_design": site_design, "favicon": favicon})


@xframe_options_exempt
def site_preview_through_domain(request, domain):
    if Websites.objects.filter(domain=domain, is_deleted=False).exists():
        site = Websites.objects.get(domain=domain)
        template = site.site_design.template_url
        print(site.site_design.template_url)
        template_content = TemplateContent.objects.get(site__pk=site.pk)
        audience_name = site.site_design.audience.audience_name
        company_name = Settings.objects.get(site__pk=site.pk).company_name
        buyer_options = BuyerOptions.objects.all()
        listing_options = ListingOptions.objects.all()

        profile = UserProfile.objects.get(user=site.user)
        settings = Settings.objects.get(site=site)
        if settings.phone:
            phone = settings.phone
        else:
            phone = profile.cell_phone

        if settings.contact_email:
            email = settings.contact_email
        else:
            email = profile.user.email

        if settings.address and settings.city and settings.state and settings.zipcode:
            address = settings.address
            location = settings.city + ", " + settings.state + " " + settings.zipcode
        elif profile.address and profile.city and profile.state and profile.zip:
            address = profile.address
            location = profile.city + ", " + profile.state + " " + profile.zip
        else:
            address = ""
            location = ""

        return render(request, template,
                      {"template_content": template_content, "company_name": company_name,
                       "audience_type": audience_name,
                       "buyer_options": buyer_options, "listing_options": listing_options, "phone": phone,
                       "email": email,
                       "address": address, "location": location})
        buyer_options = BuyerOptions.objects.all()
        favicon = TemplateContent.objects.get(site__pk=site.pk).logo
        listing_options = ListingOptions.objects.all()
        site_design = site.site_design.template_name
        print(site.pk)
        return render(request, "xsite/site_design_templates/xsite_template_preview.html",
                      {"site_id": site.pk, "buyer_options": buyer_options, "listing_options": listing_options,
                       "site_design": site_design, "favicon": favicon})
    else:
        return JsonResponse({"message": "Domain does not exist"})


def check_domain_availability(request, domain, duration):
    data = dict()
    print(type(duration))
    print(duration)
    # try:
    #     ext = domain.split(".", 1)[1]
    #     print(ext)
    #
    #     availability_res = requests.post(url, params={'ApiUser': ApiUser, 'ApiKey': ApiKey,
    #                                                   'Command': "namecheap.domains.check",
    #                                                   'UserName': UserName, 'ClientIp': ClientIp,
    #                                                   'DomainList': domain})
    #
    #     print("------------------ Availability Check -----------------------")
    #     print(availability_res)
    #     print(availability_res.text)
    #
    #     root = etree.fromstring(availability_res.content)
    #     for elem in root.iter():
    #         if elem.tag == '{http://api.namecheap.com/xml.response}DomainCheckResult':
    #             if elem.attrib['Available'] == 'true':
    #                 print("Available")
    #                 # if duration != 0:
    #                 #     price_res = requests.post(url, params={'ApiUser': ApiUser, 'ApiKey': ApiKey,
    #                 #                                            'Command': "namecheap.users.getPricing",
    #                 #                                            'UserName': UserName, 'ClientIp': ClientIp,
    #                 #                                            'ProductType': "DOMAIN", 'ProductCategory': "DOMAINS",
    #                 #                                            'ProductName': ext})
    #                 #
    #                 #     print("------------------ Pricing Check -----------------------")
    #                 #     print(price_res)
    #                 #     print(price_res.text)
    #                 #
    #                 #     pricing_root = etree.fromstring(price_res.content)
    #                 #     price_root = pricing_root[3][0][0]
    #                 #     for resp in price_root:
    #                 #         if resp.attrib['Name'] == "register":
    #                 #             for product_type in resp:
    #                 #                 if product_type.attrib['Name'] == ext:
    #                 #                     for pricing_result in product_type:
    #                 #                         print(type(pricing_result.attrib['Duration']))
    #                 #                         if pricing_result.attrib['Duration'] == str(duration):
    #                 #                             price = pricing_result.attrib['Price']
    #                 #                             additional = pricing_result.attrib['AdditionalCost']
    #                 #
    #                 #     total_price = float(price) + float(additional)
    #                 #     print(total_price)
    #                 #     extra = (total_price * 10) / 100
    #                 #     print(extra)
    #                 #     amount = round(total_price + extra, 2)
    #                 #     print(amount)
    #                 #     print(amount * 100)
    #                 #
    #                 #     data = {"message": "Domain does not exist",
    #                 #             "message2": "Requested domain is available at " + str(amount) + " USD",
    #                 #             "amount": amount}
    #                 # else:
    #                 #     data = {"message": "Domain does not exist"}
    #             else:
    #                 print("Not Available")
    #                 if Websites.objects.filter(domain=domain, is_deleted=False).exists():
    #                     data = {"message": "Domain is already taken"}
    #                 else:
    #                     data = {"message": "Domain exists"}
    #     # check = whois.whois(domain)
    #     # print(check)
    #     # price = json.loads(availability_res.text)['domains'][0]['price']
    #     return JsonResponse(data)
    # except:
    #     print(traceback.print_exc())
    #     data = {"message": "There is some error!"}
    #     return JsonResponse(data, status=400)
        # import pdb;pdb.set_trace()
    return JsonResponse({"message": "Domain exists"},status=200)


def get_edit_site(request, type, pk):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role.role_name == "Admin User":
        user = request.user
    else:
        user = profile.created_by.user
    users = UserProfile.objects.filter(created_by__user=user).values('user')
    sites = Websites.objects.filter((Q(user=user) | Q(user__in=users)) & Q(is_deleted=False)).order_by('-id')
    site_content = get_object_or_404(Websites, pk=pk)
    buyer_options = BuyerOptions.objects.all()
    listing_options = ListingOptions.objects.all()
    return render(request, "xsite/edit_template_vvveb.html",
                  {"site_id": pk, "websites": sites, "site_name": site_content.site_design.template_name,
                   "buyer_options": buyer_options, "listing_options": listing_options, "type": type})


def Update_site(request, pk):
    print(pk)
    try:
        site_content = get_object_or_404(TemplateContent, site__pk=pk)
        content_form = TemplateContentForm(request.POST, request.FILES, instance=site_content)
        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.site = Websites.objects.get(pk=pk)
            content.save()
            messages.add_message(request, messages.INFO, 'Site content updated successfully!')
            return redirect('/xsite/xsite_websites')
        else:
            return render(request, "xsite/edit_template.html", {"site": pk, "form": content_form})
    except:
        print(traceback.format_exc())
        messages.add_message(request, messages.INFO, 'There was an error!')
        return redirect("/xsite/get_edit_site/" + str(pk) + "/")


@csrf_exempt
@xframe_options_exempt
def Create_Lead(request, pk):
    try:
        assistance = "off"
        if request.POST.get('immediate_assistance'):
            assistance = "on"
        site = Websites.objects.get(pk=pk)
        form = LeadForm(request.POST)
        valid = True
        select_msg = ""
        if request.POST.get('audience') == 'Buyer':
            if not request.POST.get('what_are_you_looking_for'):
                select_msg = "This field is required."
                valid = False

        if form.is_valid() and valid:
            lead = form.save(commit=False)
            lead.site = site
            lead.status = Status.objects.get(status_name="New")
            lead.save()

            if request.POST.get('audience') == 'Buyer':
                mail = Mail.objects.get(site__pk=pk)
                ctx = {
                    'content': mail.content,
                    'fullname': form.cleaned_data['fullname']
                }
                to_email_list = [form.cleaned_data['email']]
                subject = mail.subject
                html_message = render_to_string('xsite/Email_Template.html', ctx)
                plain_message = strip_tags(html_message)
                from_email = mail.from_email
                send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                          fail_silently=False)
                messages.add_message(request, messages.INFO, 'Lead Created Successfully!')
                return redirect("/xsite/" + str(pk) + "/")
                # return render(request, "xsite/xsite_leadform.html", {"site": lead.pk})
            else:
                # ExtraPropertyInformation.objects.create(lead=lead)
                mail = Mail.objects.get(site__pk=pk)
                ctx = {
                    'content': mail.content,
                    'fullname': form.cleaned_data['fullname']
                }
                to_email_list = [form.cleaned_data['email']]
                subject = mail.subject
                html_message = render_to_string('xsite/Email_Template.html', ctx)
                plain_message = strip_tags(html_message)
                from_email = mail.from_email
                send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                          fail_silently=False)
                messages.add_message(request, messages.INFO, 'Lead Created Successfully!')
                return render(request, "xsite/xsite_download_pdf.html")
        else:
            buyer_options = BuyerOptions.objects.all()
            listing_options = ListingOptions.objects.all()
            profile = UserProfile.objects.get(user=request.user)
            site_design = Websites.objects.get(pk=pk).site_design.template_name
            return render(request, "xsite/site_design_templates/xsite_template_preview.html",
                          {"form": form, "site_id": pk,
                           "buyer_options": buyer_options, "listing_options": listing_options, "assistance": assistance,
                           "select_msg": select_msg, "profile": profile, "site_design": site_design})
    except:
        print(traceback.format_exc())
        messages.add_message(request, messages.INFO, 'There was an error!')
        return redirect("/xsite/" + str(pk) + "/")


@csrf_exempt
@xframe_options_exempt
def Create_Lead_Ajax(request, pk):
    try:
        # assistance = "off"
        # if request.POST.get('immediate_assistance'):
        #     assistance = "on"
        site = Websites.objects.get(pk=pk)
        form = LeadForm(request.POST)
        valid = True
        select_msg = ""
        if request.POST.get('audience') == 'Buyer':
            if not request.POST.get('what_are_you_looking_for'):
                select_msg = "This field is required."
                valid = False

        if form.is_valid() and valid:
            lead = form.save(commit=False)
            lead.site = site
            lead.status = Status.objects.get(status_name="New")
            lead.save()

            if request.POST.get('audience') == 'Buyer':
                mail = Mail.objects.get(site__pk=pk)
                ctx = {
                    'content': mail.content,
                    'fullname': form.cleaned_data['fullname']
                }
                to_email_list = [form.cleaned_data['email']]
                subject = mail.subject
                html_message = render_to_string('xsite/Email_Template.html', ctx)
                plain_message = strip_tags(html_message)
                from_email = mail.from_email
                send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                          fail_silently=False)
                messages.add_message(request, messages.INFO, 'Lead Created Successfully!')
                return redirect("/xsite/" + str(pk) + "/")
                # return render(request, "xsite/xsite_leadform.html", {"site": lead.pk})
            else:
                # ExtraPropertyInformation.objects.create(lead=lead)
                mail = Mail.objects.get(site__pk=pk)
                ctx = {
                    'content': mail.content,
                    'fullname': form.cleaned_data['fullname']
                }
                to_email_list = [form.cleaned_data['email']]
                subject = mail.subject
                html_message = render_to_string('xsite/Email_Template.html', ctx)
                plain_message = strip_tags(html_message)
                from_email = mail.from_email
                send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                          fail_silently=False)
                messages.add_message(request, messages.INFO, 'Lead Created Successfully!')
                return render(request, "xsite/xsite_download_pdf.html")
        else:
            buyer_options = BuyerOptions.objects.all()
            listing_options = ListingOptions.objects.all()
            profile = UserProfile.objects.get(user=request.user)
            site_design = Websites.objects.get(pk=pk).site_design.template_name
            return render(request, "xsite/site_design_templates/xsite_template_preview.html",
                          {"form": form, "site_id": pk,
                           "buyer_options": buyer_options, "listing_options": listing_options, "assistance": assistance,
                           "select_msg": select_msg, "profile": profile, "site_design": site_design})
    except:
        print(traceback.format_exc())
        messages.add_message(request, messages.INFO, 'There was an error!')
        return redirect("/xsite/" + str(pk) + "/")


def AddExtraPropertyInformation(request, pk):
    try:
        lead = Leads.objects.get(pk=pk)
        form = ExtraPropertyInformationForm(request.POST)
        print(form)
        if form.is_valid():

            extra_property_info = form.save(commit=False)
            extra_property_info.lead = lead
            extra_property_info.save()
            mail = Mail.objects.get(site__pk=lead.site.pk)
            ctx = {
                'content': mail.content,
                'fullname': lead.fullname
            }
            to_email_list = [lead.email]
            subject = mail.subject
            html_message = render_to_string('xsite/Email_Template.html', ctx)
            plain_message = strip_tags(html_message)
            from_email = mail.from_email
            send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
                      fail_silently=False)
            messages.add_message(request, messages.INFO, 'Lead Created Successfully!')
            return redirect("/xsite/" + str(lead.site.pk) + "/")
        else:
            return render(request, "xsite/xsite_leadform.html", {"form": form, "site": pk})
    except:
        print(traceback.format_exc())
        messages.add_message(request, messages.INFO, 'There was an error!')
        return redirect("/xsite/" + str(lead.site.pk) + "/")


def UpgradeMembership(request):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        return render(request, 'settings_coming_soon.html')
    membership_details = MembershipDetails.objects.get(user=request.user)
    try:
        if membership_details.subscription_id:
            stripe.Subscription.retrieve(membership_details.subscription_id)
            subscription = stripe.Subscription.retrieve(membership_details.subscription_id)
            membership_details.subscription_end_date = time.strftime("%Y-%m-%d", time.gmtime(
                subscription.current_period_end))
            membership_details.save()
    except:
        print(traceback.print_exc())
    return render(request, 'xsite/xsite_update_membership_plan.html', {"membership_details": membership_details})


def subscribe_monthly(request, plan):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        user = profile.created_by.user
    else:
        user = request.user

    customer_id = UserStripeDetail.objects.get(user=user).customer_id
    member_ship_detail = MembershipDetails.objects.get(user=user)

    if MembershipDetails.objects.filter(user=user, subscription_status="Subscribed"):
        stripe.Subscription.modify(
            member_ship_detail.subscription_id,
            cancel_at_period_end=True
        )
        MembershipDetails.objects.filter(user=user).update(next_subscription_plan="Monthly",
                                                           membership_plan=MembershipPlan.objects.get(plan="Monthly"))
        messages.add_message(request, messages.INFO,
                             'Plan changed to Monthly subscription, '
                             'Payment will be deducted when your annual subscription period ends!')
    elif MembershipDetails.objects.filter(user=user,
                                          subscription_status="Cancelled") and date.today() < member_ship_detail.subscription_end_date:
        MembershipDetails.objects.filter(user=user).update(next_subscription_plan="Monthly",
                                                           subscription_status="Subscribed",
                                                           membership_plan=MembershipPlan.objects.get(plan="Monthly"))
        # s_amount = decimal.Decimal(97)
        # Revenue.objects.create(amount=s_amount)
        messages.add_message(request, messages.INFO,
                             'Monthly subscription Successful, '
                             'Payment will be deducted when your previous payed subscription period ends!')
    else:
        new_7_days = datetime.datetime.now() + datetime.timedelta(days=7)
        # today = datetime.datetime.timestamp(datetime.datetime.now())
        # start = datetime.datetime.timestamp(new_7_days)
        try:
            if plan == 'simple':
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[
                        {
                            'plan': "plan_HG6gElR3A5ph6b",  # Monthly Plan plan_Gi1KATDSAZwOtU
                            'quantity': 1,
                        }
                    ],
                    trial_end=new_7_days,
                )
                if subscription.status == 'active' or subscription.status == 'trialing':
                    MembershipDetails.objects.filter(user=user).update(subscription_status="Subscribed",
                                                                       membership_plan=MembershipPlan.objects.get(
                                                                           plan="Monthly"),
                                                                       subscription_id=subscription.id,
                                                                       next_subscription_plan="None",
                                                                       subscription_end_date=time.strftime("%Y-%m-%d",
                                                                                                           time.gmtime(
                                                                                                               subscription.current_period_end)))
                    s_amount = decimal.Decimal(97)
                    Revenue.objects.create(amount=s_amount)
                    messages.add_message(request, messages.INFO,
                                         'Monthly subscription Successful, '
                                         'You can check your invoice history in payments and packages section!')
                else:
                    messages.add_message(request, messages.INFO,
                                         "There's some error with the card!")
            else:
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[
                        {
                            'plan': "plan_HImITssww7jOeK",  # Monthly Plan plan_Gi1KATDSAZwOtU
                            'quantity': 1,
                        }
                    ],
                    trial_end=new_7_days,
                )
                if subscription.status == 'active' or subscription.status == 'trialing':
                    MembershipDetails.objects.filter(user=user).update(subscription_status="Subscribed",
                                                                       membership_plan=MembershipPlan.objects.get(
                                                                           plan="Monthly"),
                                                                       subscription_id=subscription.id,
                                                                       next_subscription_plan="None",
                                                                       subscription_end_date=time.strftime("%Y-%m-%d",
                                                                                                           time.gmtime(
                                                                                                               subscription.current_period_end)))
                    bbc = MembershipDetails.objects.get(user=user)
                    s_amount = decimal.Decimal(144)
                    Revenue.objects.create(amount=s_amount)
                    messages.add_message(request, messages.INFO,
                                         'Monthly subscription Successful, '
                                         'You can check your invoice history in payments and packages section!')
                else:
                    messages.add_message(request, messages.INFO,
                                         "There's some error with the card!")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.RateLimitError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.InvalidRequestError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.AuthenticationError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.StripeError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except Exception as e:
            print(traceback.print_exc())
            messages.add_message(request, messages.INFO, "There is some error with the card!")
    return redirect("/xsite/upgrade_membership")


def subscribe_yearly(request, plan):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        user = profile.created_by.user
    else:
        user = request.user

    customer_id = UserStripeDetail.objects.get(user=user).customer_id
    member_ship_detail = MembershipDetails.objects.get(user=user)

    if MembershipDetails.objects.filter(user=user, subscription_status="Subscribed"):
        stripe.Subscription.modify(
            member_ship_detail.subscription_id,
            cancel_at_period_end=True
        )
        MembershipDetails.objects.filter(user=user).update(next_subscription_plan="Yearly",
                                                           membership_plan=MembershipPlan.objects.get(plan="Yearly"))
        messages.add_message(request, messages.INFO,
                             'Plan changed to Yearly subscription, '
                             'Payment will be deducted when your monthly subscription period ends!')
    elif MembershipDetails.objects.filter(user=user,
                                          subscription_status="Cancelled") and date.today() < member_ship_detail.subscription_end_date:
        MembershipDetails.objects.filter(user=user).update(next_subscription_plan="Yearly",
                                                           subscription_status="Subscribed",
                                                           membership_plan=MembershipPlan.objects.get(plan="Yearly"))
        # s_amount = decimal.Decimal(219)
        # Revenue.objects.create(amount=s_amount)
        messages.add_message(request, messages.INFO,
                             'Yearly subscription Successful, '
                             'Payment will be deducted when your previous payed subscription period ends!')
    else:
        new_7_days = datetime.datetime.now() + datetime.timedelta(days=7)
        # today = datetime.datetime.timestamp(datetime.datetime.now())
        # start = datetime.datetime.timestamp(new_7_days)
        try:
            if plan == 'simple':
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[
                        {
                            'plan': "plan_HG6kLvfwdWhvwD",  # Yearly Plan plan_Gi1KBUF6m49jy2
                            'quantity': 1,
                        }
                    ],
                    trial_end=new_7_days,
                )
                if subscription.status == 'active' or subscription.status == 'trialing':
                    MembershipDetails.objects.filter(user=user).update(subscription_status="Subscribed",
                                                                       membership_plan=MembershipPlan.objects.get(
                                                                           plan="Yearly"),
                                                                       subscription_id=subscription.id,
                                                                       next_subscription_plan="None",
                                                                       subscription_end_date=time.strftime("%Y-%m-%d",
                                                                                                           time.gmtime(
                                                                                                               subscription.current_period_end)))
                    s_amount = decimal.Decimal(931)
                    Revenue.objects.create(amount=s_amount)
                    messages.add_message(request, messages.INFO,
                                         'Yearly subscription Successful, '
                                         'You can check your invoice history in payments and packages section!')
                else:
                    messages.add_message(request, messages.INFO,
                                         "There's some error with the card!")

            else:
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[
                        {
                            'plan': "plan_HImKa19m4cX71U",  # Yearly Plan plan_Gi1KBUF6m49jy2
                            'quantity': 1,
                        }
                    ],
                    trial_end=new_7_days,
                )
                if subscription.status == 'active' or subscription.status == 'trialing':
                    MembershipDetails.objects.filter(user=user).update(subscription_status="Subscribed",
                                                                       membership_plan=MembershipPlan.objects.get(
                                                                           plan="Yearly"),
                                                                       subscription_id=subscription.id,
                                                                       next_subscription_plan="None",
                                                                       subscription_end_date=time.strftime("%Y-%m-%d",
                                                                                                           time.gmtime(
                                                                                                               subscription.current_period_end)))
                    s_amount = decimal.Decimal(1382)
                    Revenue.objects.create(amount=s_amount)
                    messages.add_message(request, messages.INFO,
                                         'Yearly subscription Successful, '
                                         'You can check your invoice history in payments and packages section!')
                else:
                    messages.add_message(request, messages.INFO,
                                         "There's some error with the card!")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.RateLimitError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.InvalidRequestError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.AuthenticationError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except stripe.error.StripeError as e:
            print(traceback.print_exc())
            body = e.json_body
            err = body['error']
            messages.add_message(request, messages.INFO, err['message'])
        except Exception as e:
            print(traceback.print_exc())
            messages.add_message(request, messages.INFO, "There is some error with the card!")

    return redirect("/xsite/upgrade_membership")


def cancel_subscription(request):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name == "Sub User":
        user = profile.created_by.user
    else:
        user = request.user

    customer = UserStripeDetail.objects.get(user=user).customer_id
    membership_details = MembershipDetails.objects.get(user=user)
    subscriptions = stripe.Subscription.list(customer=customer)
    if membership_details.subscription_id in subscriptions:
        stripe.Subscription.delete(MembershipDetails.objects.get(user=user).subscription_id)

    MembershipDetails.objects.filter(user=user).update(
        subscription_status='Cancelled',
        next_subscription_plan="None")

    messages.add_message(request, messages.INFO,
                         'Subscription cancelled Successfully, '
                         'You can use three sites until your payed subscription period ends!')
    return redirect("/xsite/upgrade_membership")


def dashboard(request, pk):
    won = Leads.objects.filter(site__pk=pk, status__status_name="Won").count()
    dead = Leads.objects.filter(site__pk=pk, status__status_name="Dead").count()
    other = Leads.objects.filter(Q(site__pk=pk) & (
            Q(status__status_name="New") | Q(status__status_name="Follow Up") | Q(
        status__status_name="Pending"))).count()
    audience_name = Websites.objects.get(pk=pk).site_design.audience.audience_name
    is_existing = Websites.objects.get(pk=pk).is_existing
    return render(request, 'xsite/Xsite_dashboard.html',
                  {"site": pk, "won": won, "dead": dead, "other": other, "audience_type": audience_name,
                   "is_existing": is_existing})


def get_leads_won(request, pk):
    data = dict()
    try:
        search_value = request.GET.get('search[value]')
        if search_value:
            all_leads = Leads.objects.filter(
                Q(site__pk=pk) & Q(status__status_name="Won") & (
                        Q(fullname__icontains=search_value) | Q(email__icontains=search_value))).order_by('-id')
        else:
            all_leads = Leads.objects.filter(site__pk=pk, status__status_name="Won").order_by('-id')

        # leads_extra_info = ExtraPropertyInformation.objects.filter(lead__pk__in=all_leads.values('pk')).order_by('-id')
        #
        # if Websites.objects.get(pk=pk).content_pack.target_audience.audience.audience_name == "Buyer":
        #     paginator = Paginator(leads_extra_info, 10)
        #     page_number = int(request.GET.get('start', 0)) / int(request.GET.get('length', 10)) + 1
        #     try:
        #         leads = paginator.page(page_number)
        #     except PageNotAnInteger:
        #         leads = paginator.page(1)
        #     except EmptyPage:
        #         leads = paginator.page(paginator.num_pages)
        #     serializer = ExtraPropertyInformationSerializer(leads, many=True)
        #     print(serializer.data)
        # else:
        paginator = Paginator(all_leads, 10)
        page_number = int(request.GET.get('start', 0)) / int(request.GET.get('length', 10)) + 1
        try:
            leads = paginator.page(page_number)
        except PageNotAnInteger:
            leads = paginator.page(1)
        except EmptyPage:
            leads = paginator.page(paginator.num_pages)
        serializer = LeadSerializer(leads, many=True)
        # print(serializer.data)

        return JsonResponse({
            "draw": int(request.GET.get('draw', 1)),
            "recordsTotal": all_leads.count(),
            "recordsFiltered": all_leads.count(),
            "data": serializer.data
        })
    except:
        print(traceback.format_exc())
        data['message'] = "There is some error!"
        return JsonResponse(data, 500)


def get_leads_dead(request, pk):
    data = dict()
    try:
        search_value = request.GET.get('search[value]')
        if search_value:
            all_leads = Leads.objects.filter(
                Q(site__pk=pk) & Q(status__status_name="Dead") & (
                        Q(fullname__icontains=search_value) | Q(email__icontains=search_value))).order_by('-id')
        else:
            all_leads = Leads.objects.filter(site__pk=pk, status__status_name="Dead").order_by('-id')

        # leads_extra_info = ExtraPropertyInformation.objects.filter(lead__pk__in=all_leads.values('pk')).order_by('-id')
        #
        # if Websites.objects.get(pk=pk).content_pack.target_audience.audience.audience_name == "Buyer":
        #     paginator = Paginator(leads_extra_info, 10)
        #     page_number = int(request.GET.get('start', 0)) / int(request.GET.get('length', 10)) + 1
        #     try:
        #         leads = paginator.page(page_number)
        #     except PageNotAnInteger:
        #         leads = paginator.page(1)
        #     except EmptyPage:
        #         leads = paginator.page(paginator.num_pages)
        #     serializer = ExtraPropertyInformationSerializer(leads, many=True)
        #     print(serializer.data)
        # else:
        paginator = Paginator(all_leads, 10)
        page_number = int(request.GET.get('start', 0)) / int(request.GET.get('length', 10)) + 1
        try:
            leads = paginator.page(page_number)
        except PageNotAnInteger:
            leads = paginator.page(1)
        except EmptyPage:
            leads = paginator.page(paginator.num_pages)
        serializer = LeadSerializer(leads, many=True)
        # print(serializer.data)

        return JsonResponse({
            "draw": int(request.GET.get('draw', 1)),
            "recordsTotal": all_leads.count(),
            "recordsFiltered": all_leads.count(),
            "data": serializer.data
        })
    except:
        print(traceback.format_exc())
        data['message'] = "There is some error!"
        return JsonResponse(data, 500)


def get_leads(request, pk):
    data = dict()
    try:
        # col = request.GET.get('order[i][column]')
        # col_dir = request.GET.get('order[i][dir]')
        # print(col)
        # print(col_dir)
        search_value = request.GET.get('search[value]')
        if search_value:
            all_leads = Leads.objects.filter(
                Q(site__pk=pk) & (Q(status__status_name="New") | Q(status__status_name="Follow Up") | Q(
                    status__status_name="Pending")) & (
                        Q(fullname__icontains=search_value) | Q(email__icontains=search_value))).order_by('-id')
        else:
            all_leads = Leads.objects.filter(
                Q(site__pk=pk) & (Q(status__status_name="New") | Q(status__status_name="Follow Up") | Q(
                    status__status_name="Pending"))).order_by('-id')

        # leads_extra_info = ExtraPropertyInformation.objects.filter(lead__pk__in=all_leads.values('pk')).order_by('-id')
        #
        # print(Websites.objects.get(pk=pk).content_pack.target_audience.audience.audience_name)

        # if Websites.objects.get(pk=pk).content_pack.target_audience.audience.audience_name == "Buyer":
        #     paginator = Paginator(leads_extra_info, 10)
        #     page_number = int(request.GET.get('start', 0)) / int(request.GET.get('length', 10)) + 1
        #     try:
        #         leads = paginator.page(page_number)
        #     except PageNotAnInteger:
        #         leads = paginator.page(1)
        #     except EmptyPage:
        #         leads = paginator.page(paginator.num_pages)
        #     serializer = ExtraPropertyInformationSerializer(leads, many=True)
        #     print(serializer.data)
        # else:
        paginator = Paginator(all_leads, 10)
        page_number = int(request.GET.get('start', 0)) / int(request.GET.get('length', 10)) + 1
        try:
            leads = paginator.page(page_number)
        except PageNotAnInteger:
            leads = paginator.page(1)
        except EmptyPage:
            leads = paginator.page(paginator.num_pages)
        serializer = LeadSerializer(leads, many=True)

        return JsonResponse({
            "draw": int(request.GET.get('draw', 1)),
            "recordsTotal": all_leads.count(),
            "recordsFiltered": all_leads.count(),
            "data": serializer.data
        })
    except:
        print(traceback.format_exc())
        data['message'] = "There is some error!"
        return JsonResponse(data, 500)


def change_lead_status(request, pk, status):
    data = dict()
    try:
        Leads.objects.filter(pk=pk).update(status=Status.objects.get(status_name=status))
        site = Leads.objects.get(pk=pk).site.pk
        won = Leads.objects.filter(site__pk=site, status__status_name="Won").count()
        dead = Leads.objects.filter(site__pk=site, status__status_name="Dead").count()
        other = Leads.objects.filter(Q(site__pk=site) & (
                Q(status__status_name="New") | Q(status__status_name="Follow Up") | Q(
            status__status_name="Pending"))).count()

        return JsonResponse({
            "message": "Lead status changed successfully!",
            "won": won,
            "dead": dead,
            "other": other
        })
    except:
        print(traceback.format_exc())
        data['message'] = "There is some error!"
        return JsonResponse(data, 500)


def change_read_status(request, pk):
    data = dict()
    try:
        if Leads.objects.filter(pk=pk, is_marked_read=False).exists():
            Leads.objects.filter(pk=pk).update(is_marked_read=True)
            msg = "Lead has been marked read successfully!"
        else:
            Leads.objects.filter(pk=pk).update(is_marked_read=False)
            msg = "Lead has been marked unread successfully!"

        site = Leads.objects.get(pk=pk).site.pk
        won = Leads.objects.filter(site__pk=site, status__status_name="Won").count()
        dead = Leads.objects.filter(site__pk=site, status__status_name="Dead").count()
        other = Leads.objects.filter(Q(site__pk=site) & (
                Q(status__status_name="New") | Q(status__status_name="Follow Up") | Q(
            status__status_name="Pending"))).count()

        return JsonResponse({
            "message": msg,
            "won": won,
            "dead": dead,
            "other": other
        })
    except:
        print(traceback.format_exc())
        data['message'] = "There is some error!"
        return JsonResponse(data, 500)


# def google_analytics_data(request, pk, startDate):
#     try:
#         API_URL = ['https://www.googleapis.com/auth/analytics.readonly']
#         KEY_FILE_LOCATION = 'My Project-4669dd846f3a.json'
#
#         view_id = "211416192"
#
#         credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, API_URL)
#
#         # Build the service object.
#         analytics = build('analyticsreporting', 'v4', credentials=credentials)
#
#         site_creation_date = Websites.objects.get(pk=pk).created_at.strftime("%Y-%m-%d")
#         # if startDate < site_creation_date:
#         #     startDate = site_creation_date
#         startDate = startDate  # "2020-02-10"
#         endDate = "today"
#         pagePath = 'ga:pagePath=={}'.format("/xsite/" + str(pk) + "/")
#         body = {
#             'reportRequests': [
#                 {
#                     'viewId': view_id,
#                     'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
#                     'dimensions': [{'name': 'ga:date'}],
#                     'metrics': [{'expression': 'ga:pageviews'}, {'expression': 'ga:users'},
#                                 {'expression': 'ga:avgtimeonpage'}],
#                     'filtersExpression': pagePath
#                 }]
#         }
#
#         response = analytics.reports().batchGet(body=body).execute()
#         print(response)
#
#         if "rows" in response['reports'][0]['data']:
#
#             length = len(response['reports'][0]['data']['rows'])
#             mylist = []
#             for i in range(length):
#                 res = response['reports'][0]['data']['rows'][i]['dimensions'][0]
#                 res2 = response['reports'][0]['data']['rows'][i]['metrics'][0]['values'][0]
#                 visit_date = res[:4] + "-" + res[4:6] + "-" + res[6:8]
#                 if i == 0 and visit_date != startDate:
#                     mylist.append({'date': startDate, 'visitors': 0})
#                 mylist.append({'date': visit_date, 'visitors': res2})
#             if visit_date != date.today().strftime("%Y-%m-%d"):
#                 mylist.append({'date': date.today().strftime("%Y-%m-%d"), 'visitors': 0})
#             data = dict()
#             data['list_data'] = mylist
#             data['size'] = length
#             data['total_visitors'] = response['reports'][0]['data']['totals'][0]['values'][0]
#             # data['total_users'] = response['reports'][0]['data']['totals'][0]['values'][1]
#             data['avg_time'] = round((float(response['reports'][0]['data']['totals'][0]['values'][2])) / 60, 2)
#
#             body = {
#                 'reportRequests': [
#                     {
#                         'viewId': view_id,
#                         'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
#                         'dimensions': [{'name': 'ga:deviceCategory'}],
#                         'metrics': [{'expression': 'ga:pageviews'}, {'expression': 'ga:users'},
#                                     {'expression': 'ga:avgtimeonpage'}],
#                         'filtersExpression': pagePath
#                     }]
#             }
#             response = analytics.reports().batchGet(body=body).execute()
#
#             lod = response['reports'][0]['data']['rows']
#             length2 = len(response['reports'][0]['data']['rows'])
#             for i in range(length2):
#                 if lod[i]['dimensions'][0] == "mobile":
#                     total_mobile_visitors = lod[i]['metrics'][0]['values'][0]
#                     total_visitors = response['reports'][0]['data']['totals'][0]['values'][0]
#                     percentage_mobile_visitors = int(total_mobile_visitors) / int(total_visitors) * 100
#                     data['percentage_mobile_visitors'] = round(percentage_mobile_visitors, 2)
#                 else:
#                     total_mobile_visitors = 0
#                     data['percentage_mobile_visitors'] = total_mobile_visitors
#
#             data['total_leads'] = Leads.objects.filter(site__pk=pk, created_at__gte=startDate).count()
#         else:
#             mylist = []
#             mylist.append({'date': startDate, 'visitors': 0})
#             mylist.append({'date': date.today().strftime("%Y-%m-%d"), 'visitors': 0})
#             data = dict()
#             data['list_data'] = mylist
#             data['size'] = 0
#             data['total_visitors'] = 0
#             data['avg_time'] = 0
#             data['percentage_mobile_visitors'] = 0
#             data['total_leads'] = Leads.objects.filter(site__pk=pk, created_at__gte=startDate).count()
#
#         return JsonResponse(data)
#     except:
#         data = dict()
#         data['message'] = "There is some error!"
#         return JsonResponse(data, 500)


def statistics(request, pk):
    datee = date.today()
    datee = datee.strftime("%Y-%m-%d")
    site_creation_date = Websites.objects.get(pk=pk).created_at.strftime("%Y-%m-%d")
    is_existing = Websites.objects.get(pk=pk).is_existing
    return render(request, 'xsite/Xsite_statistics.html',
                  {"site": pk, "startDate": datee, "site_creation_date": site_creation_date,
                   "is_existing": is_existing})


def local_time_statistics(request, pk, startDate):
    try:
        domain = Websites.objects.get(pk=pk).domain
        print(domain)
        API_URL = ['https://www.googleapis.com/auth/analytics.readonly']
        KEY_FILE_LOCATION = 'My Project-4669dd846f3a.json'

        view_id = "211416192"

        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, API_URL)

        # Build the service object.
        analytics = build('analyticsreporting', 'v4', credentials=credentials)

        # site_creation_date = Websites.objects.get(pk=pk).created_at.strftime("%Y-%m-%d")
        # if startDate < site_creation_date:
        #     startDate = site_creation_date
        startDate = startDate  # "2020-02-10"
        endDate = "today"
        pagePath = 'ga:pagePath=={}'.format("/xsite/" + domain + "/")
        body = {
            'reportRequests': [
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
                    'dimensions': [{'name': 'ga:hour'}, {'name': 'ga:date'}],
                    'metrics': [{'expression': 'ga:pageviews'}, {'expression': 'ga:users'},
                                {'expression': 'ga:avgtimeonpage'}],
                    'filtersExpression': pagePath
                }]
        }

        response = analytics.reports().batchGet(body=body).execute()

        time_zone = pytz.timezone('US/Arizona')
        sdate = datetime.datetime(int(startDate[:4]), int(startDate[5:7]), int(startDate[8:10]), 00)
        sdate2 = time_zone.localize(sdate)
        utc_date_time2 = sdate2.astimezone(pytz.utc)

        enddate = date.today().strftime("%Y-%m-%d")
        edate = datetime.datetime(int(enddate[:4]), int(enddate[5:7]), int(enddate[8:10]), 00)
        edate2 = time_zone.localize(edate)
        utc_date_time3 = edate2.astimezone(pytz.utc)

        if "rows" in response['reports'][0]['data']:

            length = len(response['reports'][0]['data']['rows'])
            mylist = []
            for i in range(length):
                res = response['reports'][0]['data']['rows'][i]['dimensions'][0]
                res2 = response['reports'][0]['data']['rows'][i]['dimensions'][1]
                res3 = response['reports'][0]['data']['rows'][i]['metrics'][0]['values'][0]

                d = datetime.datetime(int(res2[:4]), int(res2[4:6]), int(res2[6:8]), int(res))
                d2 = time_zone.localize(d)
                utc_date_time = d2.astimezone(pytz.utc)

                if i == 0 and utc_date_time != utc_date_time2:
                    mylist.append({'date': utc_date_time2, 'visitors': 0})
                mylist.append({'date': utc_date_time, 'visitors': res3})

            if utc_date_time != utc_date_time3:
                mylist.append({'date': utc_date_time3, 'visitors': 0})

            data = dict()
            data['list_data'] = mylist
            data['size'] = length
            data['total_visitors'] = response['reports'][0]['data']['totals'][0]['values'][0]
            data['avg_time'] = round((float(response['reports'][0]['data']['totals'][0]['values'][2])) / 60, 2)

            body = {
                'reportRequests': [
                    {
                        'viewId': view_id,
                        'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
                        'dimensions': [{'name': 'ga:deviceCategory'}],
                        'metrics': [{'expression': 'ga:pageviews'}, {'expression': 'ga:users'},
                                    {'expression': 'ga:avgtimeonpage'}],
                        'filtersExpression': pagePath
                    }]
            }
            response = analytics.reports().batchGet(body=body).execute()

            lod = response['reports'][0]['data']['rows']
            length2 = len(response['reports'][0]['data']['rows'])
            for i in range(length2):
                if lod[i]['dimensions'][0] == "mobile":
                    total_mobile_visitors = lod[i]['metrics'][0]['values'][0]
                    total_visitors = response['reports'][0]['data']['totals'][0]['values'][0]
                    percentage_mobile_visitors = int(total_mobile_visitors) / int(total_visitors) * 100
                    data['percentage_mobile_visitors'] = round(percentage_mobile_visitors, 2)
                else:
                    total_mobile_visitors = 0
                    data['percentage_mobile_visitors'] = total_mobile_visitors

            data['total_leads'] = Leads.objects.filter(site__pk=pk, created_at__gte=startDate).count()
        else:
            mylist = []
            mylist.append({'date': startDate, 'visitors': 0})
            mylist.append({'date': date.today().strftime("%Y-%m-%d"), 'visitors': 0})
            data = dict()
            data['list_data'] = mylist
            data['size'] = 0
            data['total_visitors'] = 0
            data['avg_time'] = 0
            data['percentage_mobile_visitors'] = 0
            data['total_leads'] = Leads.objects.filter(site__pk=pk, created_at__gte=startDate).count()

        # leads = Leads.objects.filter(site__pk=pk, created_at__gte=startDate)
        # for lead in leads:
        #     print(lead.created_at)

        return JsonResponse(data)
    except:
        data = dict()
        data['message'] = "There is some error!"
        return JsonResponse(data, 500)


def get_template_data(request, pk):
    print("Data Fetch")
    print(pk)
    data = dict()
    site = Websites.objects.get(pk=pk)
    template_content = TemplateContent.objects.get(site__pk=pk)
    data['html_body_content'] = site.site_design.html_body_content
    data['html_head_content'] = site.site_design.html_head_content
    data['template_content'] = TemplateContentSerializer(template_content).data
    data['audience_name'] = site.site_design.audience.audience_name
    data['company_name'] = Settings.objects.get(site__pk=pk).company_name
    profile = UserProfile.objects.get(user=site.user)
    settings = Settings.objects.get(site=site)
    if settings.phone:
        phone = settings.phone
    else:
        phone = profile.cell_phone

    if settings.contact_email:
        email = settings.contact_email
    else:
        email = profile.user.email

    if settings.address and settings.city and settings.state and settings.zipcode:
        address = settings.address
        location = settings.city + ", " + settings.state + " " + settings.zipcode
    elif profile.address and profile.city and profile.state and profile.zip:
        address = profile.address
        location = profile.city + ", " + profile.state + " " + profile.zip
    else:
        address = ""
        location = ""

    print(location)
    data['phone'] = phone
    data['email'] = email
    data['address'] = address
    data['location'] = location

    return JsonResponse(data)


def save_template(request, pk):
    try:
        TemplateContent.objects.filter(site__pk=pk).update(html_body_content=request.POST.get('body'), is_edited=True)
        return JsonResponse({"message": "Template saved successfully"})
    except:
        return JsonResponse({"message": "There was an error!"}, status=404)


def save_image(request):
    myfile = request.FILES['file']
    fs = FileSystemStorage(location='media/xsite_images/website_editor_images')
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = "/media/xsite_images/website_editor_images/" + filename
    return JsonResponse({"message": "Image saved successfully", "uploaded_file_url": uploaded_file_url})


def facebook_pixels(request, pk):
    template_content = TemplateContent.objects.get(site__pk=pk)
    facebook_pixel = template_content.facebook_book_pixel
    return render(request, 'xsite/Xsite_facebook_pixels.html',
                  {"site": pk, "facebook_pixel": facebook_pixel, "is_existing": template_content.site.is_existing})


def save_facebook_pixels(request, pk):
    try:
        fp_head = request.POST.get("facebook_pixel").replace("<!-- Facebook Pixel Code -->", "").split('>')
        if fp_head[0].lstrip() != "<script" and request.POST.get("facebook_pixel"):
            messages.add_message(request, messages.INFO, 'Please add Facebook Pixels Script only!')
        else:
            messages.add_message(request, messages.INFO, 'Script saved successfully!')
            TemplateContent.objects.filter(site__pk=pk).update(facebook_book_pixel=request.POST.get("facebook_pixel"))

        return redirect("/xsite/facebook_pixels/" + str(pk) + "/")
    except:
        messages.add_message(request, messages.INFO, 'There was some error!')
        return redirect("/xsite/facebook_pixels/" + str(pk) + "/")


def google_tag_manager(request, pk):
    template_content = TemplateContent.objects.get(site__pk=pk)
    google_tag_manager_head = template_content.google_tag_manager_head
    google_tag_manager_body = template_content.google_tag_manager_body
    return render(request, 'xsite/Xsite_google_tag_manager.html',
                  {"site": pk, "google_tag_manager_head": google_tag_manager_head,
                   "google_tag_manager_body": google_tag_manager_body,
                   "is_existing": template_content.site.is_existing})


def save_google_tag_manager(request, pk):
    try:
        gtm_body = request.POST.get("google_tag_manager_body").replace("<!-- Google Tag Manager (noscript) -->",
                                                                       "").split('>')
        gtm_head = request.POST.get("google_tag_manager_head").replace("<!-- Google Tag Manager -->", "").split('>')

        if (gtm_body[0].lstrip() != "<noscript" or gtm_head[0].lstrip() != "<script") and (
                request.POST.get("google_tag_manager_head") or request.POST.get("google_tag_manager_body")):
            messages.add_message(request, messages.INFO, 'Please add Google Tag Manager Script only!')
        else:
            messages.add_message(request, messages.INFO, 'Script saved successfully!')
            TemplateContent.objects.filter(site__pk=pk).update(
                google_tag_manager_head=request.POST.get("google_tag_manager_head"),
                google_tag_manager_body=request.POST.get("google_tag_manager_body"))

        return redirect("/xsite/google_tag_manager/" + str(pk) + "/")
    except:
        messages.add_message(request, messages.INFO, 'There was some error!')
        return redirect("/xsite/facebook_pixels/" + str(pk) + "/")


def website_logo(request, pk):
    is_existing = Websites.objects.get(pk=pk).is_existing
    return render(request, 'xsite/Xsite_website_logo.html', {"site": pk, "is_existing": is_existing})


def save_logo(request, pk):
    try:
        instance = get_object_or_404(TemplateContent, site__pk=pk)
        logo_form = LogoForm(request.POST, request.FILES, instance=instance)
        if logo_form.is_valid():
            logo_form.save()
            messages.add_message(request, messages.INFO, 'Logo saved successfully!')
        else:
            messages.add_message(request, messages.INFO, 'There was some error!')
    except:
        messages.add_message(request, messages.INFO, 'There was some error!')
    return redirect("/xsite/website_logo/" + str(pk) + "/")


def renew_domain_info(request, pk):
    site = Websites.objects.get(pk=pk)
    current_date = date.today()

    current_year = int(current_date.year)
    max_renewal_duration = current_year + 10
    expiry_year = int(site.renewal_date.year)
    max_renewal_duration = max_renewal_duration - expiry_year

    maxed_out = False
    if max_renewal_duration == 0:
        maxed_out = True

    renewal_allowed = True
    if site.is_expired:
        renewal_allowed = False

    return render(request, 'xsite/Xsite_renew_domain.html',
                  {"site": pk, "renewal_data": site.renewal_date, "renewal_allowed": renewal_allowed,
                   "max_renewal_duration": range(1, max_renewal_duration + 1), "maxed_out": maxed_out})


def get_price(request, pk, duration):
    try:
        site = Websites.objects.get(pk=pk)
        price_res = requests.post(url, params={'ApiUser': ApiUser, 'ApiKey': ApiKey,
                                               'Command': "namecheap.users.getPricing",
                                               'UserName': UserName, 'ClientIp': ClientIp,
                                               'ProductType': "DOMAIN", 'ProductCategory': "DOMAINS",
                                               'ProductName': site.domain.split(".", 1)[1]})

        print("------------------ Pricing Check -----------------------")
        print(price_res)
        print(price_res.text)

        pricing_root = etree.fromstring(price_res.content)
        price_root = pricing_root[3][0][0]
        for resp in price_root:
            if resp.attrib['Name'] == "renew":
                for product_type in resp:
                    if product_type.attrib['Name'] == site.domain.split(".", 1)[1]:
                        for pricing_result in product_type:
                            if pricing_result.attrib['Duration'] == str(duration):
                                price = pricing_result.attrib['Price']
                                additional = pricing_result.attrib['AdditionalCost']

        total_price = float(price) + float(additional)
        print(total_price)
        extra = (total_price * 10) / 100
        print(extra)
        amount = round(total_price + extra, 2)
        return JsonResponse({"amount": amount})
    except:
        print(traceback.print_exc())
        return JsonResponse({"message": "There is some error!"}, status=404)


def renew_domain(request, pk, duration):
    try:
        site = Websites.objects.get(pk=pk)

        profile = UserProfile.objects.get(user=site.user)

        if profile.role.role_name == "Sub User":
            user = profile.created_by.user
        else:
            user = profile.user

        customer_id = UserStripeDetail.objects.get(user=user).customer_id

        price_res = requests.post(url, params={'ApiUser': ApiUser, 'ApiKey': ApiKey,
                                               'Command': "namecheap.users.getPricing",
                                               'UserName': UserName, 'ClientIp': ClientIp,
                                               'ProductType': "DOMAIN", 'ProductCategory': "DOMAINS",
                                               'ProductName': site.domain.split(".", 1)[1]})

        print("------------------ Pricing Check -----------------------")
        print(price_res)
        print(price_res.text)

        pricing_root = etree.fromstring(price_res.content)
        price_root = pricing_root[3][0][0]
        for resp in price_root:
            if resp.attrib['Name'] == "renew":
                for product_type in resp:
                    if product_type.attrib['Name'] == site.domain.split(".", 1)[1]:
                        for pricing_result in product_type:
                            if pricing_result.attrib['Duration'] == str(duration):
                                price = pricing_result.attrib['Price']
                                additional = pricing_result.attrib['AdditionalCost']

        total_price = float(price) + float(additional)
        print(total_price)
        extra = (total_price * 10) / 100
        print(extra)
        amount = round(total_price + extra, 2)
        print(amount)
        print(round(amount * 100))

        charge = stripe.Charge.create(
            amount=round(amount * 100),  # $15.00 this time
            currency='usd',
            customer=customer_id,  # Previously stored, then retrieved
        )
        print(charge.id)

        renewal_res = requests.post(url, params={'ApiUser': ApiUser, 'ApiKey': ApiKey,
                                                 'Command': "namecheap.domains.renew",
                                                 'UserName': UserName, 'ClientIp': ClientIp,
                                                 'DomainName': site.domain, 'Years': duration})
        print("========================")
        print(renewal_res)
        print(renewal_res.text)
        renewal_root = etree.fromstring(renewal_res.content)
        for elem in renewal_root.iter():
            if elem.tag == '{http://api.namecheap.com/xml.response}DomainRenewResult':
                if elem.attrib['Renew'] == 'true':
                    site.renewal_date = addYears(site.renewal_date, duration)
                    site.save()
                else:
                    refund = stripe.Refund.create(
                        charge=charge.id,
                    )
                    print(refund.id)
        messages.add_message(request, messages.INFO, 'Domain renewed successfully!')
    except:
        print(traceback.print_exc())
        messages.add_message(request, messages.INFO, 'There was some error!')
    return redirect("/xsite/renew_domain_info/" + str(pk) + "/")
