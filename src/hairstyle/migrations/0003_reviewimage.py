# Generated by Django 5.1.1 on 2025-01-28 06:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0002_remove_file_removed"),
        ("hairstyle", "0002_alter_serviceimage_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReviewImage",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("order", models.IntegerField(default=0)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ReviewImages",
                        to="general.file",
                    ),
                ),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Images",
                        to="hairstyle.review",
                    ),
                ),
            ],
        ),
    ]
