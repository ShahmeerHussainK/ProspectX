from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('report_history', login_required(views.report_history_page), name='report_history'),
    path('report_history_data', login_required(views.report_history_data), name='report_history_data'),
    path('export_to_excel/<int:id>/', login_required(views.export_to_excel), name='export_to_excel'),
    path('skipped_history/<int:id>/', login_required(views.skipped_history_page), name='skipped_history'),
]