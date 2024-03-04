from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser, Student

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('username', 'email', 'first_name', 'Department')
    list_filer = ('username', 'email', 'first_name', 'is_active','is_staff', 'Department')
    ordering = ('-start_date',)
    list_display = ('username','email','first_name','is_active','is_staff', 'Department', 'day_pref', 'time_pref')
    fieldsets = (
        (None, {'fields':('username','email','first_name')}),
        ('Permissions', {'fields':('is_staff', 'is_active')}),
        ('Personal', {'fields':('Department','group', 'Year', 'day_pref', 'time_pref')}),
    )
    add_fiedsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('username', 'email', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')
        })
    )

admin.site.register(NewUser, UserAdminConfig)