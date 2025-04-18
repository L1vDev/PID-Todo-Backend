from datetime import timezone
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from app_projects.models import Project
from app_projects.serializers import ProjectSerializer
from rest_framework.response import Response

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            if instance.status!='planning' and request.data.get('status')=='planning':
                return Response({"detail":"No se puede cambiar el estado de un proyecto en curso a planificación","error":"cant_change_status"}, status=status.HTTP_400_BAD_REQUEST)
            if instance.status=='completed' and request.data.get('satus')!='completed':
                return Response({"detail":"No se puede cambiar el estado de un proyecto completado","error":"cant_change_status"}, status=status.HTTP_400_BAD_REQUEST)
            if request.data.get('status')=='completed' and instance.status!='completed':
                instance.finished_at = timezone.now()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e), "error": "server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
