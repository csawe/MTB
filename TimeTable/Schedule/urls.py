from django.urls import path
from .views import *

app_name = 'Schedule'

urlpatterns = [
    path('', home, name="Home-View")
]
