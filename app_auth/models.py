from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import cloudinary.uploader
from app_auth.utils import get_unique_filename
import uuid

class User(AbstractBaseUser):
    id=models.CharField(primary_key=True,default=uuid.uuid4, verbose_name="ID", max_length=60)
    username=models.CharField(unique=True,verbose_name="Nombre de Usuario",max_length=50)
    email=models.EmailField(unique=True,verbose_name="Email")
    picture=models.ImageField(upload_to=get_unique_filename,blank=True,null=True,verbose_name="Foto de Perfil")
    cloud_url=models.URLField(verbose_name="Link de la Imagen",null=True,blank=True)
    cloud_id=models.CharField(verbose_name='ID de la Imagen',null=True,blank=True,max_length=100)
    is_email_verified=models.BooleanField(default=False,verbose_name="Email Verificado")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creación")
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
        
    def save(self, *args, **kwargs):
        try:
            if self.pk:
                user_obj=User.objects.get(pk=self.pk)
                if user_obj.picture:
                    if self.picture and self.picture != user_obj.picture:
                        cloudinary.uploader.destroy(user_obj.cloud_id,resource_type="image")
                        upload_result = cloudinary.uploader.upload(self.picture)
                        self.cloud_id=upload_result['public_id']
                        self.cloud_url = upload_result['secure_url']
                    elif not self.picture:
                        cloudinary.uploader.destroy(user_obj.cloud_id,resource_type="image")
                        self.cloud_id=None
                        self.cloud_url=None
                else:
                    if self.picture:
                        upload_result = cloudinary.uploader.upload(self.picture)
                        self.cloud_id=upload_result['public_id']
                        self.cloud_url = upload_result['secure_url']
            else:
                if self.picture:
                    upload_result = cloudinary.uploader.upload(self.picture)
                    self.cloud_id=upload_result['public_id']
                    self.cloud_url = upload_result['secure_url']
        except Exception as e:
            print(str(e))
        super().save(*args, **kwargs)
    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"