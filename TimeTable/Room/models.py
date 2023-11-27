from django.db import models
from django.contrib.postgres.fields import ArrayField
from School.models import School

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=50)
    Schools = models.ManyToManyField(School)

    def __str__(self):
        return self.name

class Room(models.Model):
    Building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    capacity = models.IntegerField()
    type = models.CharField

    def __str__(self):
        return self.name