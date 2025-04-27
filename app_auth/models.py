from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from app_auth.utils import get_unique_filename
import uuid

class User(AbstractBaseUser):
    id=models.CharField(primary_key=True,default=uuid.uuid4, verbose_name="ID", max_length=60)
    username=models.CharField(unique=True,verbose_name="Nombre de Usuario",max_length=50)
    email=models.EmailField(unique=True,verbose_name="Email")
    picture=models.ImageField(upload_to=get_unique_filename,blank=True,null=True,verbose_name="Foto de Perfil")
    is_email_verified=models.BooleanField(default=False,verbose_name="Email Verificado")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creación")
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"