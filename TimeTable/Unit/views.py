from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Users.models import NewUser
from .models import SemesterUnit, Unit
from .forms import SemesterUnitForm

# Create your views here.
@login_required(login_url='Users:Signin-View')
def view_semester_unit(request):
    semester_units = SemesterUnit.objects.filter(Lecturer__in=NewUser.objects.filter(Department = request.user.Department))
    return render(request, 'semesterUnits.html', {'semester_units': semester_units})

@login_required(login_url='Users:Signin-View')
def add_semester_unit(request):
    form = SemesterUnitForm()
    units = Unit.objects.all()
    return render(request, 'addSemesterUnit.html', {'form': form, 'units':units,})
