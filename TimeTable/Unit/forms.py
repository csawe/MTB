from .models import SemesterUnit
from django.forms import ModelForm

# class NewUserForm(UserCreationForm):
#     class Meta:
#         model = NewUser
#         fields = ['username', 'email', 'first_name','last_name','Department','group','password1', 'password2']
#     def save(self, commmit=True):
#         user = super(NewUserForm, self)
#         user.save()
#         return user
    
class SemesterUnitForm(ModelForm):
    class Meta:
        model = SemesterUnit
        fields = '__all__'
        