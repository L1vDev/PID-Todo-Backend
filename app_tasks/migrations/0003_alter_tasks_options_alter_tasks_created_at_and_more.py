# Generated by Django 5.1.7 on 2025-04-27 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tasks', '0002_alter_tasks_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasks',
            options={'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterField(
            model_name='tasks',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='description',
            field=models.TextField(null=True, verbose_name='Task Description'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='finished_at',
            field=models.DateTimeField(null=True, verbose_name='Finished At'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Completed'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Task Name'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=20, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated At'),
        ),
    ]
