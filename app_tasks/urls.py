from django.urls import path
from app_tasks.views import TasksView, TasksDetailsView

urlpatterns = [
    path('<str:project_id>/tasks/', TasksView.as_view(), name='task-list-create'),
    path('<str:project_id>/tasks/<str:pk>/', TasksDetailsView.as_view(), name='task-detail'),
]