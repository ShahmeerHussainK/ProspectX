from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .models import InviteUrl, InvitePayment, Payouts
from user.decorators import is_admin_user
from django.contrib import messages
from django.db.models import F, Sum
from .forms import InviteUrlForm, PaymentForm
import paypalrestsdk
from paypalrestsdk import Payout
from datetime import datetime
import urllib.parse as urlparse
from urllib.parse import parse_qs
from user.models import UserProfile


# Create your views here.

def paypal_payout(email, amount, batch_id):
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "AaWIHxNphtZ4sBEi1oDVnsk4KAN0WtTskLnnETZ2wmm_Jci3r_5t_lzALcPUmv5IskpHdYKv0zBDNBOk",
        "client_secret": "ELX6uls4K5DmsfPCL3cGTt1RkVVOQgvuqPbRuy6XAygLdqxNxeznphf2gWn5uHXGkbWr83IGyKECkoev"})
    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": batch_id,
            "email_subject": "You have a payment",

        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": float(amount),
                    "currency": "USD"
                },
                "receiver": email,
                "note": "Thank you.",
                "sender_item_id": "item_1"
            }
        ]
    })

    if payout.create(sync_mode=False):
        payout_id = payout.batch_header.payout_batch_id
        print("payout[%s] created successfully" % (payout_id))
        return payout_id
    else:
        print(payout.error)
        return None


@is_admin_user
def AffiliateDashboardView(request):
    base_url = 'http://{}'.format(get_current_site(request).domain)
    urls = InviteUrl.objects.filter(user=request.user)
    clicks = InviteUrl.objects.filter(user=request.user).all().aggregate(Sum('click'))
    if clicks['click__sum']:
        t_clicks = clicks['click__sum']
    else:
        t_clicks = 0
    sign_ups = InviteUrl.objects.filter(user=request.user).aggregate(Sum('sign_up'))
    if sign_ups['sign_up__sum']:
        t_sign_ups = sign_ups['sign_up__sum']
    else:
        t_sign_ups = 0
    balance = InvitePayment.objects.filter(inv_user=request.user.id, payment_status=1).aggregate(Sum('balance'))

    if balance['balance__sum']:
        t_balance = balance['balance__sum']
    else:
        t_balance = 0
    image = UserProfile.objects.get(user=request.user).profile_image
    image = '/media/{}'.format(image)
    url_ls = []
    for url in urls:
        inv_url = '{}/affiliate?ur={}&deal={}&sid={}'.format(base_url, request.user.id, url.url_name, url.sub_id)
        url_ls.append({"inv_url": inv_url, "click": url.click, "sign_up": url.sign_up})
    if request.method == 'POST':
        url_form = request.POST.get('url_form')
        payout_form = request.POST.get('payout_form')
        if url_form == 'True':
            form = InviteUrlForm(request.user, request.POST)
            if form.is_valid():
                inv_url = form.save(commit=False)
                inv_url.user = request.user
                inv_url.save()
                return redirect('/affiliate/dashboard')
            else:
                return render(request, 'affiliate/affiliate_dashboard.html',
                              {"form": form, "urls": url_ls, 'clicks': t_clicks, "sign_ups": t_sign_ups,
                               "balance": t_balance})
        elif payout_form == 'True':
            form = PaymentForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("payout_email")
                amount = form.cleaned_data.get("amount")
                if amount < balance['balance__sum']:
                    dt = datetime.now()
                    t_stamp = datetime.timestamp(dt)
                    payout_id = paypal_payout(email, amount, 'user-{}-{}'.format(request.user.id, t_stamp))
                    if payout_id:
                        Payouts.objects.create(user=request.user, payout_id=payout_id, payout_amount=amount)
                        qs_balance = InvitePayment.objects.filter(inv_user=request.user.id)
                        if qs_balance:
                            for blnc in qs_balance:
                                bonus = blnc.balance
                                if amount > bonus:

                                    amount = amount - blnc.balance
                                    blnc.balance = 0.0
                                    blnc.save()
                                else:
                                    bonus = bonus - amount
                                    blnc.balance = bonus
                                    blnc.save()
                        new_blnc = InvitePayment.objects.filter(inv_user=request.user.id, payment_status=1).aggregate(
                            Sum('balance'))
                        if new_blnc['balance__sum']:
                            t_balance = new_blnc['balance__sum']
                        else:
                            t_balance = 0
                        return JsonResponse({"success": "Payment successfully done", "balance": t_balance})
                    else:
                        return JsonResponse({"error": "Something went wrong. Please try again", "urls": url_ls,
                                             'clicks': t_clicks, "sign_ups": t_sign_ups, "balance": t_balance},
                                            status=400)
                else:
                    return JsonResponse(
                        {"amount_error": "Please enter correct amount", "urls": url_ls, 'clicks': t_clicks,
                         "sign_ups": t_sign_ups, "balance": t_balance}, status=400)
            else:
                return JsonResponse(
                    {"form": form.errors, "urls": url_ls, 'clicks': t_clicks, "sign_ups": t_sign_ups,
                     "balance": t_balance},
                    status=400)

                # return redirect(None)

    elif request.method == 'GET':
        return render(request, 'affiliate/affiliate_dashboard.html',
                      {"urls": url_ls, 'clicks': t_clicks, "sign_ups": t_sign_ups, "balance": t_balance,
                       'image': image})


#
def InviteSignIn(request):
    deal = request.GET.get('deal')
    sub_id = request.GET.get('sid')
    u_id = request.GET.get('ur')
    if u_id and sub_id and deal:
        InviteUrl.objects.filter(user=u_id, sub_id=sub_id, url_name=deal).update(click=F('click') + 1)
        messages.add_message(request, messages.INFO, '{}-{}-{}'.format(u_id, sub_id, u_id))
        return redirect('/signup')
    else:
        return redirect('home')


def DelUrl(request):
    if request.method == 'POST':
        inv_url = request.POST.get('inv_url')
        parsed = urlparse.urlparse(inv_url)
        q_param = parse_qs(parsed.query)
        name = q_param['deal'][0]
        sid = q_param['sid'][0]
        up = request.POST.get('update')
        if up == 'true':
            new_name = request.POST.get('new_name')
            new_sid = request.POST.get('new_sid')
            InviteUrl.objects.filter(user=request.user, url_name=name, sub_id=sid).update(url_name=new_name,
                                                                                          sub_id=new_sid)
            return JsonResponse({'data': 'success'})
        else:
            InviteUrl.objects.filter(user=request.user, url_name=name, sub_id=sid).delete()
            return JsonResponse({'data': 'success'})
