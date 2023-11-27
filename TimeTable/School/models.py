from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    years = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for year in range(1, self.years+1):
            Year.objects.create(Department=self, year=year)
    
    def __str__(self):
        return self.name

class Year(models.Model):
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return self.Department.name+" Year "+str(self.year)
