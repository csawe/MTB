from django.contrib import admin
from .models import Unit, SemesterUnit, Lecture

# Register your models here.
admin.site.register(Unit)
admin.site.register(SemesterUnit)
admin.site.register(Lecture)