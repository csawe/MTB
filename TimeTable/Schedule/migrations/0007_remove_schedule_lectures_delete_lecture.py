# Generated by Django 4.2.7 on 2023-11-25 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0006_alter_schedule_lectures'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='Lectures',
        ),
        migrations.DeleteModel(
            name='Lecture',
        ),
    ]
