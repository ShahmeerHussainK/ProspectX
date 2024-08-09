from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns=[
    path('',x_force_view,name='x_force'),
    path('xforce_packages',xforce_packages_view,name='xforce_packages'),
    path('subscribe_monthly/', login_required(subscribe_monthly), name='subscribe_monthly'),
    path('subscribe_yearly/', login_required(subscribe_yearly), name='subscribe_yearly'),
    path('cancel_subscription', login_required(cancel_subscription), name='cancel_subscription'),
    path('add_seller_lead',add_seller_lead,name='add_seller_lead'),
    path('add_title_company',add_title_company, name="add_seller_lead"),
    # path('new_transactions',new_transactions,name="new_transactions"),
    path('add_appointment',add_appointment,name="add_appointment"),
    path('add_sales',add_sales,name="add_sales"),
    path('add_team_member',add_team_member,name="add_team_member"),

    ]