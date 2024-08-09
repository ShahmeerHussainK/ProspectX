from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('xsite_websites', login_required(views.xsite_websites), name='xsite_websites'),
    path('xsite_setup', login_required(views.website_setup), name='xsite_setup'),
    path('get_site_designs/<str:category>/<str:stype>/', login_required(views.get_site_designs), name='get_site_designs'),
    path('delete/<int:pk>/', login_required(views.delete_xsite_websites), name='delete_xsite_websites'),
    path('delete_ajax/<int:pk>/', login_required(views.delete_xsite_websites_ajax), name='delete_xsite_websites_ajax'),
    path('add_site', login_required(views.add_site), name='add_site'),
    path('save_mail/<int:pk>/', login_required(views.save_mail), name='save_mail'),
    path('get_mail_data/<int:pk>/', login_required(views.get_mail_data), name='get_mail_data'),
    path('<int:pk>/', views.site_preview, name='site_preview'),
    path('get_edit_site/<str:type>/<int:pk>/', login_required(views.get_edit_site), name='get_edit_site'),
    path('update_site/<int:pk>/', login_required(views.Update_site), name='update_site'),
    path('create_lead/<int:pk>/', views.Create_Lead, name='create_lead'),
    path('extra_property_information/<int:pk>/', views.AddExtraPropertyInformation, name='extra_property_information'),
    path('check_domain_availability/<str:domain>/<int:duration>/', login_required(views.check_domain_availability),
         name='check_domain_availability'),
    path('upgrade_membership', login_required(views.UpgradeMembership), name='upgrade_membership'),
    path('dashboard/<int:pk>/', login_required(views.dashboard), name='dashboard'),
    path('statistics/<int:pk>/', login_required(views.statistics), name='statistics'),
    path('subscribe_monthly/<str:plan>/', login_required(views.subscribe_monthly), name='subscribe_monthly'),
    path('subscribe_yearly/<str:plan>/', login_required(views.subscribe_yearly), name='subscribe_yearly'),
    path('cancel_subscription', login_required(views.cancel_subscription), name='cancel_subscription'),
    path('get_leads/<int:pk>/', login_required(views.get_leads), name='get_leads'),
    path('get_leads_won/<int:pk>/', login_required(views.get_leads_won), name='get_leads_won'),
    path('get_leads_dead/<int:pk>/', login_required(views.get_leads_dead), name='get_leads_dead'),
    path('change_lead_status/<int:pk>/<str:status>/', login_required(views.change_lead_status),
         name='change_lead_status'),
    path('change_read_status/<int:pk>/', login_required(views.change_read_status), name='change_read_status'),
    path('local_time_statistics/<int:pk>/<str:startDate>/', login_required(views.local_time_statistics),
         name='local_time_statistics'),
    path('facebook_pixels/<int:pk>/', login_required(views.facebook_pixels), name='facebook_pixels'),
    path('save_facebook_pixels/<int:pk>/', login_required(views.save_facebook_pixels), name='save_facebook_pixels'),
    path('google_tag_manager/<int:pk>/', login_required(views.google_tag_manager), name='google_tag_manager'),
    path('save_google_tag_manager/<int:pk>/', views.save_google_tag_manager, name='save_google_tag_manager'),
    path('website_logo/<int:pk>/', login_required(views.website_logo), name='website_logo'),
    path('save_logo/<int:pk>/', login_required(views.save_logo), name='save_logo'),
    path('renew_domain_info/<int:pk>/', login_required(views.renew_domain_info), name='renew_domain_info'),
    path('renew_domain/<int:pk>/<int:duration>/', login_required(views.renew_domain), name='renew_domain'),
    path('get_price/<int:pk>/<int:duration>/', login_required(views.get_price), name='get_price'),

    #Testing URLS
    path('save_template/<int:pk>/', login_required(views.save_template), name='save_template'),
    path('get_template_data/<int:pk>/', views.get_template_data, name='get_template_data'),
    path('save_image', login_required(views.save_image), name='save_image'),

    #Domain Pointing
    path('<str:domain>/', views.site_preview_through_domain, name='site_preview_through_domain'),
]
