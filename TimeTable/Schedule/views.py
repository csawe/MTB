from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from School.models import Year
from Unit.models import SemesterUnit

# Create your views here.'
@login_required(login_url='Users:Signin-View')
def home(request):
    context = {}
    return render(request, 'home.html', context)

@login_required(login_url='Users:Signin-View')
def create_schedule(request):
    department = request.user.Department
    years = Year.objects.filter(Department=department)
    semesterUnits = SemesterUnit.objects.filter(Year__in=years)
    context = {
        'semester_units':semesterUnits,
    }
    return render(request, 'schedule.html', context)