"""prospectx_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from task_management.views import *
from user.views import revenue_view

urlpatterns = [
    path('index/', index_evs, name='index'),
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('user/', include('user_management.urls')),
    path('payments/', include('payments.urls')),
    path('marketing/', include('marketing_machine.urls')),
    path('filter/', include('filter_prospects.urls')),
    path('task/', include('task_management.urls')),
    path('report/', include('reports.urls')),
    path('xsite/', include('xsiteApp.urls')),
    path('skiptrace/', include('skiptrace.urls')),
    path('notification/', include('notification.urls')),
    path('affiliate/', include('affiliate.urls')),
    path('x_force/', include('xforce.urls'), name='xforce_dashboard'),
    path('cash_buyer/',include('cash_buyer.urls')),
    path('sales/', include('xforce_sales.urls')),
    path('xforce_settings/', include('xforce_settings.urls')),
    path('seller/', include('xforce_seller_leads.urls')),
    path('xforce_transactions/', include('xforce_transactions.urls')),
    path('appointment/', include('xforce_appointment.urls')),
    path('revenue', revenue_view, name='revenue'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
