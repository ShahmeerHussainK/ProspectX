from django.urls import path

from .total_view import totalView

from .views import *
from .webform import webFormSellerLead

urlpatterns = [
    path('add_seller/', AddSellerLead.as_view()),
    path('add_seller/<int:pk>/', UpdateSellerLead.as_view()),
    path('new_seller_lead/', SellerLeadView.as_view(), name="new_seller_lead"),
    path('edit_seller_lead/<int:pk>/', EditSellerLeadView.as_view(), name="edit_seller_lead"),
    path('seller_list/', SellerList.as_view(), name="seller_list"),
    path('view_lead/<int:pk>/', ViewSellerLeadView.as_view(), name="view_lead"),
    path('delete/<int:pk>/', DeleteSellerView.as_view(), name='delete'),
    path('seller_lead/<str:user_uuid>/webform', webFormSellerLead.as_view(), name='web_form'),

    path('total_view/<int:id>/', totalView.as_view(), name='web_form'),
]
