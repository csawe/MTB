from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
import json
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
        return JsonResponse({'error': 'Department ID not provided'}, status=400)

def save_lectures(request):
    submitted_lectures = []
    raw_data = json.loads(request.body.decode('utf-8'))
    lectures = raw_data.get('lectures', [])
    print("Lectures:")
    for lecture in lectures:
        semester_unit = lecture['semester_unit']
        # for submitted in submitted_lectures:
        if not any(lecture['time'] == submitted['time'] for submitted in submitted_lectures):
            if (lecture['time'] is not None):
                print("Lecture: ", lecture)
                lecture_ = {
                    "semester_unit": semester_unit,
                    "room": lecture['semester_unit'],
                    "day": lecture['day'],
                    "time": [lecture['time']]
                }
                submitted_lectures.append(lecture_)
        else:
            # Handle the extra classes...
            pass
    for lecture_to_create in submitted_lectures:
        start = lecture_to_create['time'][0]
        end = lecture_to_create['time'][1] if (len(lecture_to_create['time'])>0) else (lecture_to_create['time']+1)
        # Convert to time
        semester_unit_ = SemesterUnit.objects.get(lecture_to_create['semester_unit'])
        lecture = Lecture(
                SemesterUnit = semester_unit_,
                day=lecture_to_create['day'], 
                Department=request.user.Department,
                start = start,
                end = end,
            )
        lecture.save()
    if request.method == 'POST':
        return JsonResponse({'success': True})
    else :
        return JsonResponse({'success': False, 'error': 'Method not allowed'})