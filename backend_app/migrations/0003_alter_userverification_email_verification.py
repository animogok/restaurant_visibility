# Generated by Django 5.0.6 on 2024-07-11 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0002_alter_userverification_email_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userverification',
            name='email_verification',
            field=models.BooleanField(default=False),
        ),
    ]
