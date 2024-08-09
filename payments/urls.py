from . import views
from rest_framework import routers
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('packages', login_required(views.payments_and_packages), name='packages'),
    path('change_card', views.change_default_card.as_view(), name='change_card'),

    path('upgrade', login_required(views.upgrade_package), name='upgrade'),
    path('del_card/<str:card>/<str:customer>/', login_required(views.delete_card), name='del_card'),

    path('cancel_subs', views.CancelSubscription.as_view(), name='cancel_subs'),

    path('monthly_plan', login_required(views.create_monthly_plan), name='monthly_plan'),   # for one time use
    path('yearly_plan', login_required(views.create_yearly_plan), name='yearly_plan'),      # for one time use

    path('subscribe_monthly', login_required(views.subscribe_monthly_plan), name='subscribe_monthly'),
    path('subscribe_yearly', login_required(views.subscribe_yearly_plan), name='subscribe_yearly'),
    path('save_card', login_required(views.save_new_card), name='save_card'),

    path('hook', login_required(views.hook_stripe), name='hook'),


]
