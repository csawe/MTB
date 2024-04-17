from django.urls import path
from .views import *

app_name = 'Users'

urlpatterns = [
    path('signin/', signin, name="Signin-View"),
    path('signup/', signup, name="Signup-View"),
    path('signout/', signout, name="Signout-View"),
    path('bulkregister/', bulk_user_registration, name='BulkRegistration-View')
]
