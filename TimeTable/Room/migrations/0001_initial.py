# Generated by Django 5.0.2 on 2024-02-10 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("School", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Building",
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
                ("name", models.CharField(max_length=50)),
                ("Schools", models.ManyToManyField(blank=True, to="School.school")),
            ],
        ),
        migrations.CreateModel(
            name="Room",
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
                ("name", models.CharField(max_length=15)),
                ("capacity", models.IntegerField()),
                (
                    "Building",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Room.building"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RoomDepartment",
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
                    "Department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="School.department",
                    ),
                ),
                (
                    "Room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="Room.room"
                    ),
                ),
            ],
        ),
    ]
