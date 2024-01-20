from django.db import models
from School.models import Department
from Unit.models import Lecture

# Create your models here.
class Schedule(models.Model):
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # Lectures_ = ArrayField(Lecture)
    # Lectures = models.ManyToManyField(Lecture)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.Department.name
