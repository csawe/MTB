from django.urls import path
from .views import *

app_name = 'Unit'

urlpatterns = [
    path('', view_semester_unit, name="SemesterUnit-View"),
    path('addSemesterUnit/',add_semester_unit, name="AddSemesterUnit-View"),
]
