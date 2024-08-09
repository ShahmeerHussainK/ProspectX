from django.urls import path

from . import views

urlpatterns = [
    path('company/', views.AddCompany.as_view()),
    path('company/<int:pk>/', views.UpdateCompany.as_view()),
    path('delete_company/<int:pk>/', views.DeleteCompanyView.as_view(), name='delete_company'),
    path('edit_company/<int:pk>/', views.EditCompanyView.as_view(), name='edit_company'),
    path('company_list/', views.CompanyList.as_view(), name='company_list'),
    path('view_company/<int:pk>/', views.ViewCompanyView.as_view(), name='view_company'),
    path('create_company/', views.CompanyView.as_view(), name='create_company'),
    path('settings_list/', views.SettingsList.as_view(), name='Settings_list'),
    path('settings/', views.AddSettings.as_view()),
    path('create_setting/', views.XforceSettingsView.as_view(), name='create_setting'),

]
