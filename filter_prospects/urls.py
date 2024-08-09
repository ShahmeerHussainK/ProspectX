from django.urls import path

# from filter_prospects.es_test_file import prospects_bulk_indexing, prospects_single_indexing
from . import views
from .filters import *
from .filters_action import *

from .myevents import my_send_event

urlpatterns = [
    path('import_file', views.prospects, name='prospects'),
    path('add_list', views.add_new_list, name='add_list'),  # add list in create list under settings
    path('add_list_without_file', views.add_new_list_without_file, name='add_list_without_file'),  # add list without file upload in create list under settings
    path('upload_file', views.upload_file, name='upload_file'),
    path('get_all_list_and_tags_by_user_id', views.get_all_list_and_tags_by_user_id, name='get_all_list_and_tags_by_user_id'),
    path('save_file_and_list_tags_by_user', views.save_file_and_list_tags_by_user, name='save_file_and_list_tags_by_user'),
    path('show_all_uploaded_file_process_by_user', views.show_all_upload_file_process_by_user, name='show_all_uploaded_file_process_by_user'),
    path('get_col_by_sheet_name', views.get_col_by_sheet_name, name='get_col_by_sheet_name'),
    # path('read_data_from_file_and_save_in_database', views.read_data_from_file_and_save_in_database, name='read_data_from_file_and_save_in_database'),
    path('add_new_prospect', views.AddProspect, name='add_new_prospect'),
    path('update_prospect/<int:id>/', views.UpdateProspect, name='update_prospect'),
    path('update_prospect_Ajax/<int:id>/', views.UpdateProspectAjax, name='update_prospect_Ajax'),
    path('delete_prospect/<int:pk>/', views.DeleteProspect, name='delete_prospect'),
    path('get_prospect_details/<int:id>/', views.ViewProspectDetails, name='get_prospect_details'),
    path('delete_list/<int:prospect_id>/<int:id>/', views.DeleteProspectList, name='delete_list'),
    path('delete_tag/<int:prospect_id>/<int:id>/', views.DeleteProspectTag, name='delete_tag'),

    #filter_view
    # path('get_prospectx', get_prospectx, name='get_prospectx'),
    path('filter_page', filter_view, name='filter_page'),
    path('apply_filter', apply_filters.as_view(), name='apply_filter'),
    path('save_filters', save_filters.as_view(), name='save_filters'),
    path('existing_filters', existing_filters.as_view(), name='existing_filters'),

    # make connection with els
    path('sendevent/', my_send_event.as_view(), name='my_send_event'),




    # filters_action
    path('perform_actions', perform_actions.as_view(), name='perform_actions'),



    path('run_els', run_els_query, name='run_els_query'),


    path('get_sequences', get_sequences.as_view(), name='get_sequences'),

    #test urls

    # path('bulk', prospects_bulk_indexing, name='bulk'),
    # path('single', prospects_single_indexing, name='single'),


]
