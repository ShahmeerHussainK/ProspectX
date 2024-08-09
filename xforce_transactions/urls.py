from django.urls import path

from . import views

urlpatterns = [
    path('transaction_list/', views.TransactionList.as_view(), name='transaction_list'),
    path('transaction/', views.AddTransaction.as_view(), name='add_transaction_api'),
    path('transaction/<int:pk>/', views.UpdateTransaction.as_view(), name='update_transaction_api'),
    path('new_transaction/', views.TransactionView.as_view(), name='new_transaction'),
    path('view_transaction/<int:pk>/', views.ViewTransaction.as_view(), name='view_transaction'),
    path('edit_transaction/<int:pk>/', views.EditTransaction.as_view(), name='edit_transaction'),
    path('delete_transaction/<int:pk>/', views.DeleteTransaction.as_view(), name='delete_transaction'),


    ]

