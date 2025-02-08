# Generated by Django 5.1.1 on 2025-02-08 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0011_barber"),
        ("general", "0002_remove_file_removed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="barber",
            name="pfp",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="barber_pfps",
                to="general.file",
            ),
        ),
    ]
