from django.urls import path
from app_projects.views import ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<str:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]