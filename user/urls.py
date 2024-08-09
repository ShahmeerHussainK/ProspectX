from django.urls import path, re_path
from . import views
from .views import StripeWebhook, PullListManually, GetListSequence, UpdateCreateSequence, UpdateCustomFields, ViewListDetail, \
    CheckExistingTag
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from .email_verification import activate
from .forms import EmailValidationOnForgotPassword

urlpatterns = [

    path('signup', views.Signup),
    path('', views.Signin, name='login'),
    path('reset_password', PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword,
                                                     html_email_template_name='registration/password_reset_html_email.html')),
    path('password_reset_done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('subscription_web_hook', StripeWebhook.as_view(), name='subscription_web_hook'),
    re_path('password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('password_reset_complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('update_profile', login_required(views.UpdateProfile, ), name='update_profile'),
    path('change_password', login_required(views.ChangePassword), name='change_password'),
    path('home', login_required(views.Home), name='home'),
    path('logout', login_required(views.Logout), name='logout'),
    path('get_users', login_required(views.getSubUser), name='users'),
    path('add_sub_user', login_required(views.registerSubUser), name='add-sub-users'),
    path('delete_sub_user/<int:pk>/', login_required(views.deleteSubUser), name='delete-sub-users'),
    path('update_sub_user/<int:pk>/', login_required(views.updateSubUser), name='update-sub-users'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
    path('manage_dashboard', login_required(views.DashBoard), name='manage_dashboard'),
    path('manage_welcome_email', login_required(views.WelcomeEmailView), name='manage_welcome_email'),
    path('send_email', login_required(views.SendEmailView), name='send_email'),
    path('add_block', login_required(views.AddBlock), name='add_block'),
    path('update_block/<int:pk>/', login_required(views.UpdateBlock), name='update_block'),
    path('delete_block/<int:pk>/', login_required(views.DeleteBlock), name='delete_block'),
    # list management urls
    path('list_management', login_required(views.list_management_view, ), name='list_management'),
    path('tags_management', login_required(views.tags_management_view, ), name='tags_management'),
    path('create_tag', login_required(views.create_new_tag_view, ), name='create_tag'),
    path('add_new_list', login_required(views.add_new_list_view, ), name='add_new_list'),
    path('update_list/<int:pk>/', login_required(views.update_list_view, ), name='update_list'),
    path('get_sequence', GetListSequence.as_view(), name='get_sequence'),
    path('list_pull', PullListManually.as_view(), name='list_pull'),
    path('campaign_settings', login_required(views.campaign_settings_view, ), name='campaign_settings'),
    path('skiptrace_settings', login_required(views.skiptrace_settings_view, ), name='skiptrace_settings'),
    path('xforce_settings', login_required(views.xforce_settings_view, ), name='xforce_settings'),
    path('update_or_create_sequence', UpdateCreateSequence.as_view(), name='update_or_create_sequence'),
    path('view_list', ViewListDetail.as_view(), name='view_list'),
    path('check_tag', CheckExistingTag.as_view(), name='check_tag'),
    path('del_list/<int:pk>/', login_required(views.delete_list_view), name='del_list'),
    path('update_tag/<int:pk>/', login_required(views.update_tag_view), name='update_tag'),
    path('del_tag/<int:pk>/', login_required(views.delete_tag_view), name='del_tag'),
    path('custom_update', UpdateCustomFields.as_view(), name='custom_update'),
    path('get_admin_users/<str:filter>/', login_required(views.get_admin_users), name='get_admin_users'),
]
