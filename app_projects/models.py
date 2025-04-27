from django.db import models
from uuid import uuid4

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('stopped', 'Stopped'),
        ('planning', 'Planning'),
    ]
    id = models.CharField(primary_key=True, default=uuid4, editable=False, verbose_name="ID", max_length=60)
    user=models.ForeignKey('app_auth.User', on_delete=models.CASCADE, verbose_name="User", related_name="projects")
    name = models.CharField(max_length=100, verbose_name="Project Name")
    description = models.TextField(verbose_name="Project Desciption",null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    finished_at = models.DateTimeField(verbose_name="Finished At",null=True)
    end_date = models.DateField(verbose_name="End Date",null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='planning', verbose_name="Status")
    favorite = models.BooleanField(default=False, verbose_name="Favorite")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        unique_together = ('name', 'user')