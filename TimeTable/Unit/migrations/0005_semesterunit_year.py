# Generated by Django 5.0.2 on 2024-02-15 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School', '0001_initial'),
        ('Unit', '0004_lecture_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='semesterunit',
            name='Year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='School.year'),
            preserve_default=False,
        ),
    ]
