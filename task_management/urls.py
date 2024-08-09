from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('create_task', login_required(CreateTask), name="create_task"),
    path('update_task', login_required(UpdateTask), name="update_task"),
    path('delete_task/<int:id>/', login_required(DeleteTask), name="delete_task"),
    path('duplicate_task/<int:id>/', DuplicateTask, name="duplicate_task"),
    path('load_calendar/', login_required(taskView), name='task_view'),
    path('load_page/', login_required(index), name='index'),
    path('all_tasks_calendar/', login_required(all_tasks_calendar), name='all_tasks_calendar'),
    path('get_task_formsets/<int:id>/', login_required(task_formsets), name='task_formsets'),
    path('get_createtask_formsets', login_required(create_task_formsets), name='create_task_formsets'),
    path('get_list_data/<str:category>/', login_required(get_list_data), name='get_list_data'),
    # path('posts/<str:ordering>/', posts, name='posts'),
    path('all_tasks_calendar/<int:pk>/', login_required(LinkTask), name='link_task'),
    path('get_linked_task/<int:id>/', login_required(LinkedTask), name='linked_task'),
    path('set_linked_task/<int:id>/', login_required(LinkedTask), name='set_linked_task'),
    path('save_link_task', login_required(SaveLinkedTask), name='save_link_task'),

    # path('upcoming_overdue_task/', login_required(upcoming_overdue_topbar), name='upcoming_overdue_task'),

]
