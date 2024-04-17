from django.db import models
from School.models import Department

class Schedule(models.Model):
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.Department.name
