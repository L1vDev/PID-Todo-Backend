# Generated by Django 5.1.7 on 2025-04-25 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0003_alter_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='favorite',
            field=models.BooleanField(default=False, verbose_name='Favorito'),
        ),
    ]
