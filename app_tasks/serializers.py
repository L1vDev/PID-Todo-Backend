from rest_framework import serializers
from app_tasks.models import Tasks

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'name', 'description', 'created_at', 'finished_at', 'end_date', 'is_completed', 'updated_at','project', 'priority']
        read_only_fields = ['id', 'created_at', 'updated_at','project','finished_at']