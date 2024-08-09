from . import views
from rest_framework import routers
from .views import GetHitsCount, ThirdPrtySkipTrace, GetSingleSkipTrace, AddExistingFileForSkipTrace, Add_New_Payment_View
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('skip_trace/<str:pk>/', login_required(views.skip_trace_files_list), name='skip_trace'),
    path('single_trace', login_required(views.single_skip_trace_view), name='single_trace'),
    path('skip_trace_existing', login_required(views.skip_trace_existing_file_view), name='skip_trace_existing'),
    path('upload_skip_trace', login_required(views.upload_skiptrace_file), name='upload_skip_trace'),
    path('get_col_skip_trace', login_required(views.get_col_by_skip_trace_sheet_name), name='get_col_skip_trace'),
    path('skip_trace_upload', login_required(views.upload_skip_trace_file), name='skip_trace_upload'),
    path('add_skip_trace', login_required(views.add_new_skip_trace_list), name='add_skip_trace'),
    path('hit_percent', GetHitsCount.as_view(), name='hit_percent'),
    path('single_skip_show', GetSingleSkipTrace.as_view(), name='single_skip_show'),
    path('third_skip_show', ThirdPrtySkipTrace.as_view(), name='third_skip_show'),
    path('add_existing_skip_trace', AddExistingFileForSkipTrace.as_view(), name='add_existing_skip_trace'),
    path('add_payment', Add_New_Payment_View.as_view(), name='add_payment'),
    path('small_plan', login_required(views.success_purchase_small_plan), name='small_plan'),
]
