from . import views
from .views import GetRelatedProspects, GetSearchedCampaigns, UpdateMajorMarket, CreatePlanTemplatesAndPlans, GetCampaignDetails, GetTemplateDetails, CreateMajorMarket, GetMajorMarkets, GetSequenceDetails
from rest_framework import routers
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('sequence_list/<str:pk>/', login_required(views.marketing_sequence_list), name='sequence_list'),
    path('create_sequence', login_required(views.create_marketing_sequence), name='create_sequence'),
    path('update_sequence/<int:pk>/', login_required(views.update_marketing_sequence), name='update_sequence'),
    path('del_seq/<int:pk>/', login_required(views.delete_sequence), name='del_seq'),

    path('create_campaign', login_required(views.create_marketing_campaign), name='create_campaign'),
    path('update_campaign/<int:pk>/', login_required(views.update_marketing_campaign), name='update_campaign'),
    path('campaign_list/<str:pk>/', login_required(views.marketing_campaign_list), name='campaign_list'),
    path('del_camp/<int:pk>/', login_required(views.delete_campaign), name='del_camp'),

    path('marketing_template/<int:pk>/', login_required(views.marketing_template_view), name='marketing_template'),
    path('templates_list/<str:pk>/', login_required(views.marketing_templates_list), name='templates_list'),
    path('del_temp/<int:pk>/', login_required(views.delete_template), name='del_temp'),

    path('sequence_campaigns/<int:pk>/', login_required(views.sequence_campaign_list), name='sequence_campaigns'),

    path('create_plan_template', CreatePlanTemplatesAndPlans.as_view(), name='create_plan_template'),
    path('major_market', CreateMajorMarket.as_view(), name='major_market'),

    path('get_markets', GetMajorMarkets.as_view(), name='get_markets'),
    path('update_market', UpdateMajorMarket.as_view(), name='update_market'),
    path('del_market/<int:pk>/', login_required(views.delete_market_view), name='del_market'),

    path('related_prospects', GetRelatedProspects.as_view(), name='related_prospects'),
    path('sequence_details', GetSequenceDetails.as_view(), name='sequence_details'),
    path('template_details', GetTemplateDetails.as_view(), name='template_details'),
    path('campaign_details', GetCampaignDetails.as_view(), name='campaign_details'),
    path('search_campaigns', GetSearchedCampaigns.as_view(), name='search_campaigns'),
    path('major_markets', login_required(views.major_markets_view), name='major_markets'),

]
