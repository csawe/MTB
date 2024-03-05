from django.urls import path
from .views import *

app_name = 'Schedule'

urlpatterns = [
    path('', home, name="Home-View"),
    path('schedule/', create_schedule, name='Schedule-View'),
    path('get_rooms/<int:semesterUnit_id>/', get_rooms, name='GetRooms-View'),
    path('get_preferebce/<int:semesterUnit_id>/', get_lecturer_time_preferebce, name="GetPreference"),
    path('save_lectures/', save_lectures, name='SaveLectures'),
    path('get_lecture_units/<int:semesterUnit_id>/', get_lecture_units, name="GetLectureUnits"),
    path('get_free_rooms/', get_free_rooms, name="GetFreeRooms"),
]
