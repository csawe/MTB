from django.db import models
from django.contrib.postgres.fields import ArrayField
from School.models import School, Department

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=50)
    Schools = models.ManyToManyField(School, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    Building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    capacity = models.IntegerField()
    type = models.CharField

    def __str__(self):
        return self.name
    
class RoomDepartment(models.Model):
    Room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    Department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.Room) + " -- " + str(self.Department)