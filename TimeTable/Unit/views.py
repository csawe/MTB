from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
import json
from School.models import Year
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
    units = Unit.objects.all().order_by('Department')
    external_units = Unit.objects.filter(~Q(Department=request.user.Department))
    print("External units: ", external_units)
    user = request.user
    years = user.Department.years
    return render(request, 'addSemesterUnit.html', {'form': form, 'units':units, 'years':range(1,years+1),})

@login_required(login_url='Users:Signin-View')
def get_lecturers(request, department_id):
    if department_id:
        FIELDS = ['id', 'username', 'first_name', 'last_name']
        lecturers = serializers.serialize("json", NewUser.objects.filter(Department__id=department_id, group='lecturer'), fields=FIELDS)
        return JsonResponse(lecturers, safe=False)
    else:
        print("There") 
        return JsonResponse({'error': 'Department ID not provided'}, status=400)

@login_required(login_url='Users:Signin-View')  
def save_semester_units(request):
    if request.method == 'POST':
        try:
            raw_data = json.loads(request.body.decode('utf-8'))
            print("Raw Data: ", raw_data)
            semester_units = raw_data.get('semesterUnits', [])
            for semester_unit in semester_units:
                if len(semester_unit['units']) > 0:
                    print("Year: ", semester_unit['Year'])
                    for unit in semester_unit['units']:
                        unit_temp = Unit.objects.get(id=unit['unitId'])
                        lecturer_temp = NewUser.objects.get(id=unit['lecturerId'])
                        dep_temp = request.user.Department
                        year_temp = Year.objects.get(Department=dep_temp, year=semester_unit['Year'])
                        print("Unit ", unit_temp, "Lec: ", lecturer_temp, "year: ", year_temp)
                        semester_unit_obj = SemesterUnit(Unit=unit_temp, Lecturer=lecturer_temp, Department=dep_temp ,Year=year_temp)
                        semester_unit_obj.save()
                else:
                    return JsonResponse({'success': False, 'error': "Some years are blank"})
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})