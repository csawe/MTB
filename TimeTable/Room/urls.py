from django.urls import path
from .views import *

app_name = 'Room'

urlpatterns = [
    path('', assign_room_view, name="AssignRoom-View"),
    path('get_rooms/', get_rooms, name='GetRooms'),
    path('get_departments/', get_updated_departments, name='GetDepartments'),
]