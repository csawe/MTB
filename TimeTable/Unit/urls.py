from django.urls import path
from .views import *

app_name = 'Unit'

urlpatterns = [
    path('', view_semester_unit, name="SemesterUnit-View"),
    path('addSemesterUnit/',add_semester_unit, name="AddSemesterUnit-View"),
    path('get_lecturers/<int:department_id>/', get_lecturers, name='GetLecturers-View'),
    path('saveSemesterUnit', save_semester_units, name='SaveSemesterUnit'),
    path('getSemesterYearValidity', get_semester_year_validity, name='GetSemesterYear')
]
