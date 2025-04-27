from rest_framework import serializers
from app_tasks.models import Tasks
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'name', 'description', 'created_at', 'finished_at', 'end_date', 'is_completed', 'updated_at','project', 'priority']
        read_only_fields = ['id', 'created_at', 'updated_at','project','finished_at']

    def validate_end_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("End date must be in the future.")
        return value