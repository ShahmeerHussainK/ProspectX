from django.urls import path

from . import views

urlpatterns = [
    path('appointments/', views.AddAppointment.as_view()),
    path('appointments/<int:pk>/', views.UpdateAppointment.as_view()),
    path('delete_appointment/<int:pk>/', views.DeleteAppointmentView.as_view(), name='delete_Appointment'),
    path('edit_appointment/<int:pk>/', views.EditAppointmentView.as_view(), name='edit_Appointment'),
    path('appointmentview/', views.AppointmentView.as_view(), name='appointment'),
    path('appointment_list/', views.AppointmentList.as_view(), name='appointment_list'),
    path('view_appointment/<int:pk>', views.ViewAppointmentView.as_view(), name='view_Appointment'),
    path('dashboard/', views.DashboardAppointment.as_view(), name='dashboard'),

    path('calendar_appts/<int:user_id>/', views.apptCalendarView.as_view(), name='appt_calendar_view'),



 ]
