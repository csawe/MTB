from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import NewUser
from School.models import Department

class NewUserForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ['username', 'email', 'first_name','last_name','Department','group','password1', 'password2']
    def save(self, commmit=True):
        user = super(NewUserForm, self)
        user.save()
        return user
    
USER_TYPE_CHOICES = [
    ('lecturer', 'Lecturer'),
    ('student', 'Student'),
]

class BulkUserForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    csv_file = forms.FileField()