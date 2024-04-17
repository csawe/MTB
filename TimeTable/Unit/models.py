from django.db import models
from Room.models import Room
from Schedule.models import Schedule
from School.models import Department, Year
from Users.models import NewUser

# Create your models here.
class Unit(models.Model):
    name = models.CharField(max_length=30)
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    labs_required = models.BooleanField()
    
    def __str__(self):
        return self.name
    
class SemesterUnit(models.Model):
    Unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING)
    Lecturer = models.ForeignKey(NewUser, on_delete=models.DO_NOTHING, limit_choices_to={'group':'lecturer'})
    Department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    Year = models.ForeignKey(Year, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.Unit.code + " " + self.Unit.name
    
class Lecture(models.Model):
    Schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start = models.TimeField()
    end = models.TimeField()
    Department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    Room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    SemesterUnit = models.ForeignKey(SemesterUnit, on_delete=models.CASCADE)
    Year = models.ForeignKey(Year, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.SemesterUnit.Unit.name