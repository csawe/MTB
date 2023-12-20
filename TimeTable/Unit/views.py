from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
import json
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

@login_required(login_url='Users:Signin-View')
def get_lecturers(request, department_id):
    print("Department ID is: ", department_id)
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
                print(semester_unit)
            
            # Return a success response
            return JsonResponse({'success': True})
        except Exception as e:
            # Return an error response
            return JsonResponse({'success': False, 'error': str(e)})