from django.urls import path
from . import views

urlpatterns = [
path('sub-admins-detail', views.GetSubAdminDetail, name='sub-admin'),
path('skip_trace_price/<int:pk>', views.update_skiptrace_price, name='skip_trace_price'),
path('delete/<int:pk>/<str:msg>/<int:page>/', views.UserDelete, name='delete-user'),
path('login/<int:pk>', views.UserLogin, name='login-user'),
path('change-user-password/<int:pk>', views.ChangeUserPassword, name='change-user-password'),
# path('update-user-profile/', views.UpdateUserProfile, name='update-user-profile'),
path('update-user-profile/<int:pk>/', views.UpdateUserProfile, name='update-user-profile'),
path('profile', views.profile, name='profile'),
# path('dashboard', views.superDashboard, name='super-dashboard')
]