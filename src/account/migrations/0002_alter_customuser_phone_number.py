# Generated by Django 5.1.1 on 2025-01-18 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.TextField(blank=True, max_length=13, null=True),
        ),
    ]
