# Generated by Django 4.1.5 on 2023-03-18 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_b_18', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
    ]
