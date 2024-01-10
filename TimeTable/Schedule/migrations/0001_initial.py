# Generated by Django 4.2.7 on 2024-01-10 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('School', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='School.department')),
            ],
        ),
    ]
