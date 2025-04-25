from rest_framework import serializers
from app_projects.models import Project
from django.utils import timezone

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'user', 'name', 'description', 'created_at', 'finished_at', 'end_date', 'status', 'updated_at','favorite']
        read_only_fields = ['id', 'created_at','updated_at','user']

    def validate_end_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("La fecha de finalización debe ser posterior a la fecha actual.")
        return value