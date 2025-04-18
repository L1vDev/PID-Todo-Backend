from rest_framework import serializers
from app_projects.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'user', 'name', 'description', 'created_at', 'finished_at', 'end_date', 'status', 'updated_at']
        read_only_fields = ['id', 'created_at','updated_at']