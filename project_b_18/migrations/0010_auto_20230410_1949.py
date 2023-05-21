# Generated by Django 3.2.17 on 2023-04-10 23:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_b_18', '0009_alter_class_json_raw'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='approval_status',
            field=models.CharField(choices=[('U', 'Unsent'), ('N', 'NoResponse'), ('R', 'Rejected'), ('A', 'Approved')], default='U', max_length=1),
        ),
        migrations.AddField(
            model_name='user',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
