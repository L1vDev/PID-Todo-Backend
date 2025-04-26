from rest_framework import serializers
from app_projects.models import Project
from django.utils import timezone

class ProjectSerializer(serializers.ModelSerializer):
    completed_tasks = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()
    due_days = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'user', 'name', 'description', 'created_at', 'finished_at', 'end_date', 'status', 'updated_at','favorite','completed_tasks','total_tasks','due_days']
        read_only_fields = ['id', 'created_at','updated_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def get_completed_tasks(self, obj):
        return obj.tasks.filter(is_completed=True).count()
    
    def get_total_tasks(self, obj):
        return obj.tasks.count()
    
    def get_due_days(self, obj):
        if obj.end_date:
            delta = obj.end_date - timezone.now().date()
            return delta.days
        return None

    def validate_end_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("La fecha de finalización debe ser posterior a la fecha actual.")
        return value