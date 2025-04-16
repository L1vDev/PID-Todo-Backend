# Generated by Django 5.1.7 on 2025-03-26 03:33

import app_auth.utils
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID',max_length=60)),
                ('username', models.CharField(unique=True, verbose_name='Nombre de Usuario',max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=app_auth.utils.get_unique_filename, verbose_name='Foto de Perfil')),
                ('cloud_url', models.URLField(blank=True, null=True, verbose_name='Link de la Imagen')),
                ('cloud_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='ID de la Imagen')),
                ('is_email_verified', models.BooleanField(default=False, verbose_name='Email Verificado')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
    ]
