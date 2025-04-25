from django.db import models
from uuid import uuid4

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('stopped', 'Detenido'),
        ('planning', 'En planificación'),
    ]
    id = models.CharField(primary_key=True, default=uuid4, editable=False, verbose_name="ID", max_length=60)
    user=models.ForeignKey('app_auth.User', on_delete=models.CASCADE, verbose_name="Usuario", related_name="projects")
    name = models.CharField(max_length=100, verbose_name="Nombre del Proyecto",unique=True)
    description = models.TextField(verbose_name="Descripción del Proyecto",null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    finished_at = models.DateTimeField(verbose_name="Fecha de Finalización",null=True)
    end_date = models.DateField(verbose_name="Fecha de Fin",null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='planning', verbose_name="Estado")
    favorite = models.BooleanField(default=False, verbose_name="Favorito")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"