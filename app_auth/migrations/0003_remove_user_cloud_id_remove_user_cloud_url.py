# Generated by Django 5.1.7 on 2025-04-27 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0002_user_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cloud_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cloud_url',
        ),
    ]
