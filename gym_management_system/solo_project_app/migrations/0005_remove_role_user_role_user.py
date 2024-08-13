# Generated by Django 5.0.7 on 2024-08-12 05:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solo_project_app', '0004_remove_role_user_role_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='user',
        ),
        migrations.AddField(
            model_name='role',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='solo_project_app.user'),
        ),
    ]