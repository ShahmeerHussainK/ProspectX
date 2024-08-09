from . import views
from rest_framework import routers
from .views import AffiliateDashboardView, InviteSignIn, DelUrl
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('dashboard', login_required(AffiliateDashboardView), name='affiliate_dashboard'),
    path('', InviteSignIn, name='invite'),
    path('del', login_required(DelUrl), name="del_url")
]
