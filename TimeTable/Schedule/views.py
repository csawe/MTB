from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from School.models import Year
from Unit.models import SemesterUnit, Lecture
from .models import Schedule

# Create your views here.'
@login_required(login_url='Users:Signin-View')
def home(request):
    context = {}
    return render(request, 'home.html', context)

@login_required(login_url='Users:Signin-View')
def create_schedule(request):
    print(request.user.group)
    if request.user.group == 'lecturer':
        department = request.user.Department
        years = Year.objects.filter(Department=department)
        semesterUnits = SemesterUnit.objects.filter(Year__in=years)
        context = {
            'semester_units':semesterUnits,
        }
        return render(request, 'createschedule.html', context)
    elif request.user.group == 'student':
        schedule = Schedule.objects.get(Department=request.user.Departmemt)
        lecutures = Lecture.objects.filter(Department=schedule.Department)
        context = {
            'lectures':lecutures,
        }
        return render(request, 'schedule.html', context)