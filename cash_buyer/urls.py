from django.urls import path

from . import views

urlpatterns = [
    path('cash/', views.AddCash_Buyer.as_view()),
    path('cash/<int:pk>/', views.UpdateCash_Buyer.as_view()),
    path('delete_cashbuyer/<int:pk>/', views.DeleteCash_BuyerView.as_view(), name='delete_cashbuyer'),
    path('edit_cashbuyer/<int:pk>/', views.EditCashBuyerView.as_view(), name='edit_cashbuyer'),
    path('buyer/', views.Cash_BuyerView.as_view(), name='buyer'),
    path('buyerlist/', views.Cash_BuyerList.as_view(), name='buyerlist'),
    path('view_cash_buyer/<int:pk>', views.ViewCash_BuyerView.as_view(), name='view_cash_buyer'),
    path('dashboard/', views.dashboardCash_Buyer.as_view(), name='dashboard')
]
