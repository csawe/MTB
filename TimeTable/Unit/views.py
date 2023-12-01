from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SemesterUnit
from Users.models import NewUser

# Create your views here.
@login_required(login_url='Users:Signin-View')
def view_semester_unit(request):
    semester_units = SemesterUnit.objects.filter(Lecturer__in=NewUser.objects.filter(Department = request.user.Department))
    return render(request, 'semesterUnits.html', {'semester_units': semester_units})

@login_required(login_url='Users:Signin-View')
def add_semester_unit(request):
    return render(request, 'addSemesterUnit.html', {})
