from django.db import models
import uuid

class Tasks(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID", max_length=60)
    project=models.ForeignKey('app_projects.Project', on_delete=models.CASCADE, verbose_name="Proyecto", related_name="tasks")
    name=models.CharField(max_length=100, verbose_name="Nombre de la Tarea")
    description=models.TextField(verbose_name="Descripción de la Tarea",null=True)
    priority=models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridad")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    finished_at = models.DateTimeField(verbose_name="Fecha de Finalización",null=True)
    end_date = models.DateField(verbose_name="Fecha de Fin",null=True)
    is_completed=models.BooleanField(default=False, verbose_name="Completada")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        unique_together = ('name', 'project')

