# Generated by Django 5.1.1 on 2025-01-18 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="file",
            name="removed",
        ),
    ]
