from django.db import models
import uuid

class Tasks(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID", max_length=60)
    project=models.ForeignKey('app_projects.Project', on_delete=models.CASCADE, verbose_name="Proyecto", related_name="tasks")
    name=models.CharField(max_length=100, verbose_name="Task Name")
    description=models.TextField(verbose_name="Task Description",null=True)
    priority=models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Priority")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    finished_at = models.DateTimeField(verbose_name="Finished At",null=True)
    end_date = models.DateField(verbose_name="End Date",null=True)
    is_completed=models.BooleanField(default=False, verbose_name="Completed")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = ('name', 'project')

