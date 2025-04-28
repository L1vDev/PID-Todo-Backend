from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from app_tasks.models import Tasks
from app_tasks.serializers import TaskSerializer
from rest_framework.response import Response
from app_projects.models import Project
from django.utils import timezone

class TasksView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Tasks.objects.filter(project__id=project_id,project__user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs['project_id']
            project = Project.objects.filter(id=project_id, user=request.user).first()
            if not project:
                return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
            if project.status == 'completed':
                project.status='active'
                project.finished_at=None
                project.save()
            if project.status == 'stopped':
                return Response({"detail": "Cannot add tasks to a stopped project"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e), "error": "server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

class TasksDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Tasks.objects.filter(project__id=project_id,project__user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            project = instance.project
            if project.status == 'completed' and request.data.get('is_completed')==False and instance.is_completed:
                project.status='active'
                project.finished_at=None
                project.save()
            if project.status == 'stopped' and request.data.get('is_completed')==True and not instance.is_completed:
                return Response({"detail": "Cannot complete this task","error":"cant_complete_task"}, status=status.HTTP_400_BAD_REQUEST)
            
            if request.data.get('is_completed')==True and not instance.is_completed:
                instance.finished_at = timezone.now()
            
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            completed_tasks = project.tasks.filter(is_completed=True).count()
            total_tasks = project.tasks.count()
            if completed_tasks == total_tasks and project.status != 'completed':
                project.status = 'completed'
                project.finished_at = timezone.now()
                project.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e), "error": "server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
