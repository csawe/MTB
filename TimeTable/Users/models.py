from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from School.models import Department, Year
# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, username, first_name, password, **other_fields):
        #other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        
        return self.create_user(email, username, first_name, password, **other_fields)

GROUP = (
    ('student','Student'),
    ('lecturer','Lecturer'),
)

class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    Department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=None, null=True)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE, default=None, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    group = models.CharField(max_length=9, choices=GROUP, default="student")
    start_date = models.DateTimeField(default=timezone.now)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name']
    
    def __str__(self):
        return self.username
    
class Student(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    
