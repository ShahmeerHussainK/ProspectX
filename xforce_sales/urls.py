from django.urls import path

from xforce_sales import views
from .webform import webFormSalesOffer
from .views import *

urlpatterns = [
    path('AddSales/', views.AddSales.as_view()),
    path('AddSales/<int:pk>/', views.UpdateSalesOffer.as_view()),
    path('AddSales/<int:pk>/', views.UpdateSalesOffer.as_view()),
    path('SalesList/', views.SalesList.as_view(), name='SalesList'),
    path('create_sales_offer/', views.SaleofferView.as_view(), name='create_sales_offer'),
    path('delete_offer/<int:pk>/', views.DeleteSales_offerView.as_view(), name='delete_offer'),
    path('edit/<int:pk>/', EditSalesOfferView.as_view(), name='edit'),
    path('view/<int:pk>/', views.ViewSalesOfferView.as_view(), name='view'),
    path('Sales/', views.Sales.as_view()),
    path('Sales/<int:pk>/', views.UpdateSales.as_view()),
    path('View_Sales/', views.Sales_View.as_view(), name='View_Sales'),
    path('Add_Sales/', views.AddSalesView.as_view(), name='Add_Sales'),
    path('Delete_Sales/<int:pk>/', views.DeleteSalesView.as_view(), name='Delete_Sales'),
    path('Edit_Sales/<int:pk>/', views.EditSalesView.as_view(), name='Edit_Sales'),
    path('sales_view/<int:pk>/', views.ViewSalesView.as_view(), name='sales_view'),
    path('download/<int:pk>/', views.download_offers, name="download"),
    path('sales_offer/<str:user_uuid>/webform', webFormSalesOffer.as_view(), name='web_form'),
    path('email_send/<int:pk>/<str:sub>/<str:cont>/', views.send_email.as_view(),name="email_send")
]
