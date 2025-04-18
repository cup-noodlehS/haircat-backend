# Generated by Django 5.1.1 on 2025-02-08 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0009_barbershop_specialist_barber_shop"),
        ("general", "0002_remove_file_removed"),
    ]

    operations = [
        migrations.CreateModel(
            name="BarberShopImage",
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
                ("order", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "barber_shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="account.barbershop",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="barber_shop_images",
                        to="general.file",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]
