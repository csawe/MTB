from django.urls import path
from .views import *

app_name = 'Schedule'

urlpatterns = [
    path('', home, name="Home-View"),
    path('schedule/', create_schedule, name='Schedule-View'),
    path('get_rooms/<int:semesterUnit_id>/', get_rooms, name='GetRooms-View'),
    path('save_lectures/', save_lectures, name='SaveLectures'),
]
