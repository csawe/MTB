# Generated by Django 5.0.2 on 2024-02-10 13:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Unit", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="unit",
            name="Year",
        ),
    ]