# Generated by Django 5.1.1 on 2025-02-08 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0010_barbershopimage"),
        ("general", "0002_remove_file_removed"),
    ]

    operations = [
        migrations.CreateModel(
            name="Barber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Name of the barber", max_length=255),
                ),
                (
                    "info",
                    models.TextField(
                        blank=True, help_text="Information about the barber", null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "barber_shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="barbers",
                        to="account.barbershop",
                    ),
                ),
                (
                    "pfp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="barber_pfps",
                        to="general.file",
                    ),
                ),
            ],
        ),
    ]
