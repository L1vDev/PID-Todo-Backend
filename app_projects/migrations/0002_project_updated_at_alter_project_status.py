# Generated by Django 5.1.7 on 2025-04-18 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('active', 'Activo'), ('completed', 'Completado'), ('stopped', 'Detenido'), ('planning', 'En planificación')], default='planning', max_length=20, verbose_name='Estado'),
        ),
    ]
