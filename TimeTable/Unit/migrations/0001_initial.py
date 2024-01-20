# Generated by Django 4.2.7 on 2024-01-20 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('School', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SemesterUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=10)),
                ('labs_required', models.BooleanField()),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='School.department')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='School.year')),
            ],
        ),
    ]
