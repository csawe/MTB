from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from School.models import Year
from Room.models import RoomDepartment
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
    
def get_rooms(request, semesterUnit_id):
    FIELDS = ['id', 'Room_name']
    if semesterUnit_id:
        semesterUnit = SemesterUnit.objects.get(id=semesterUnit_id)
        department = semesterUnit.Unit.Department
        rooms_ = RoomDepartment.objects.filter(Department=department)
        rooms = [{'id':room.Room.id, 'name':room.Room.name} for room in rooms_]
        return JsonResponse(rooms, safe=False)
    else:
        print("There") 
        return JsonResponse({'error': 'Department ID not provided'}, status=400)

def save_lectures(request):
    if request.method == 'POST':
        return JsonResponse({'success': True})
    else :
        return JsonResponse({'success': False, 'error': 'Method not allowed'})