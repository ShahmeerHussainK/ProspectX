import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from prospectx_new.settings import BASE_API_URL
from .models import Appointment
from xforce_seller_leads.models import SellerLead
from .serializers import AppointmentSerializer
from datetime import datetime
from xforce.utils import format_time_obj, parse_str_to_time_obj
from xforce.utils import get_comunity_people

class AddAppointment(generics.ListCreateAPIView):
    queryset = Appointment.objects.all().order_by('id')
    serializer_class = AppointmentSerializer


class UpdateAppointment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all().order_by('id')
    serializer_class = AppointmentSerializer


# def get_going_status():
#     going_status = []
#     for status in Appointment.GOING_STATUS:
#         going_status.append(status[0])
#     return going_status


def get_offer_acceptance():
    offer_acceptance = []
    for offer_acceptances in Appointment.OFFER_ACCEPTANCE:
        offer_acceptance.append(offer_acceptances[0])
    return offer_acceptance


def get_appt_status():
    appt_status = []
    for appt in Appointment.APPT_STATUS:
        appt_status.append(appt[0])
    return appt_status


class AppointmentView(View):
    @method_decorator(login_required)
    def get(self, request):
        # users = User.objects.all()
        seller = SellerLead.objects.filter(user=request.user)
        context = {
            "OFFER_ACCEPTANCE": get_offer_acceptance(),
            "Appt_Status": get_appt_status(),
            "users": get_comunity_people(request.user),

            "sellers": seller,
        }
        return render(request, 'xforce/appointments/add_appointment.html', context)

    @method_decorator(login_required)
    def post(self, request):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        appt_date_start_str = request.POST.get('appt_date_start')
 #      appt_date_end_str = request.POST.get('appt_date_end')
        post_values['appt_date_start'] = parse_str_to_time_obj(appt_date_start_str)
#       post_values['appt_date_end'] = parse_str_to_time_obj(appt_date_end_str)
        response = requests.post(BASE_API_URL + 'appointment/appointments/', data=post_values,files=request.FILES)
        context = {'active_user_id': self.request.user.id}
        if response.status_code == 201:
            return render(request, 'xforce/appointments/list_appointments.html',context)

        errors = []
        for error in response.json().keys():
            errors.append(error)
            context = {
                       "OFFER_ACCEPTANCE": get_offer_acceptance(),
                       "Appt Status": get_appt_status(),
                       'errors': errors,
                       'data': request.POST,

                       }
            return render(request, 'xforce/appointments/add_appointment.html', context)


class DashboardAppointment(View):
    def get(self, request):
        return render(request, 'xforce/xforce.html')


class AppointmentList(ListView):
    model = Appointment
    template_name = 'xforce/appointments/list_appointments.html'
    # def get_queryset(self):
    #     return Appointment.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {'active_user_id': self.request.user.id}
        return context


class DeleteAppointmentView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        requests.delete(BASE_API_URL + 'appointment/appointments/' + str(pk))
        return redirect('appointment_list')


class ViewAppointmentView(View):
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'appointment/view_appointment/' + str(pk))
        data = response.json()
        context = {'active_user_id': self.request.user.id}
        return render(request, 'xforce/appointments/list_appointments.html', data)


class EditAppointmentView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        response = requests.get(BASE_API_URL + 'appointment/appointments/' + str(pk))
        # users = User.objects.all()
        Appointment.objects.all()
        response = response.json()
        if response["seller"]:

            seller_obj = SellerLead.objects.get(pk=response["seller"])
            response["seller"] = seller_obj

        # going_on_appt = User.objects.get(pk=response["going_on_appt"])
        if response["who_set_this_appt"]:
            who_set_this_appt = User.objects.get(pk=response["who_set_this_appt"])
            response["who_set_this_appt"] = who_set_this_appt

        if response["going_on_appt"]:
            going_on_appt = User.objects.get(pk=response["going_on_appt"])
            response["going_on_appt"] = going_on_appt

        if response["offer_acceptance"]:
            offer_acceptance = response["offer_acceptance"]
            response["offer_acceptance"] = offer_acceptance
        if response["appt_status"]:
            appt_status = response["appt_status"]
            response["appt_status"] = appt_status
        # response["who_set_this_appt"] = who_set_this_appt
        response["appt_date_start"] = format_time_obj(response["appt_date_start"])
    #   response["appt_date_end"] = format_time_obj(response["appt_date_end"])
        context = {
            "is_edit": True,
            "OFFER_ACCEPTANCE": get_offer_acceptance(),
            "Appt_Status": get_appt_status(),
            "users": get_comunity_people(request.user),

            "sellers": SellerLead.objects.filter(user=request.user),
            "data": response,
            # "who_set_this_appt" : going_on_appt
        }
        return render(request, 'xforce/appointments/add_appointment.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        appt_date_start_str = request.POST.get('appt_date_start')
  #     appt_date_end_str = request.POST.get('appt_date_end')
        if appt_date_start_str:
            post_values['appt_date_start'] = parse_str_to_time_obj(appt_date_start_str)
   #        post_values['appt_date_end'] = parse_str_to_time_obj(appt_date_end_str)

        if request.FILES:
            response = requests.put(BASE_API_URL + 'appointment/appointments/' + str(pk) + '/', data=post_values,
                                    files=request.FILES)
        else:
            post_values.pop('appt_file')
            response = requests.put(BASE_API_URL + 'appointment/appointments/' + str(pk) + '/', data=post_values)

        if response.status_code == 200:
            return redirect('appointment_list')


        who_set_this_appointment = User.objects.filter(pk=post_values['who_set_this_appt']).first()
        going_on_appointment = User.objects.filter(pk=post_values['going_on_appt']).first()
        errors = []
        for (key, value) in response.json().items():
            errors[key] = value[0]

        # for error in response.json().keys():
        #     errors.append(error)
            context = {
                       "OFFER_ACCEPTANCE": get_offer_acceptance(),
                       "Appt Status": get_appt_status(),
                       #'errors': errors,
                       'WHO_SET_THIS_APPT': who_set_this_appointment,
                       'GOING_ON_APPT': going_on_appointment,
                       'data': request.POST,
                       "errors": errors
                       }
            return render(request, 'xforce/appointments/add_appointment.html', context)


class apptCalendarView(APIView):
    def get(self, request, user_id):
        appointments = Appointment.objects.filter(user_id=user_id)
        appt_list = []
        for appt in appointments:
            id = appt.id
            title = appt.seller.seller_name
            start = str(appt.appt_date_start)
#           end = str(appt.appt_date_end)
            appt_entry = {'id': id, 'title': title, 'start': start}
            appt_list.append(appt_entry)
        return Response(appt_list)
