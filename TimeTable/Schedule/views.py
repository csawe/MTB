from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
import datetime
import json
from School.models import Year
from Room.models import RoomDepartment, Room
from Unit.models import SemesterUnit, Lecture
from .models import Schedule

# Create your views here.'
@login_required(login_url='Users:Signin-View')
def home(request):
    if request.method == "POST":
        free_rooms = []
        day = request.POST.get('day', None)
        time_ = request.POST.get('time')
        print("Day: ", day, " at time: ", time_)
        rooms = Room.objects.all()
        for room in rooms:
            dep_room = RoomDepartment.objects.filter(Room=room).first()
            if dep_room:
                department = dep_room.Department
                lectures = Lecture.objects.filter(day=day, Department=department)
                if len(lectures) == 0:
                    free_rooms.append(room)
                # Constraint for time
            else:
                free_rooms.append(room)
        context['free_rooms'] = free_rooms
    schedule, _ = Schedule.objects.get_or_create(Department=request.user.Department)
    lectures = Lecture.objects.filter(Schedule=schedule)
    if schedule:
        context = {
            'schedule':schedule,
            'lectures': lectures,
        }
    else:
        context = {'schedule': 'No timetable'}
    return render(request, 'home.html', context)

@login_required(login_url='Users:Signin-View')
def create_schedule(request):
    if request.user.group == 'lecturer':
        """
            Get external units first
            1. Check if there are external units
            2. If they exist, get their lectures
            3. Push to table and make time slots
        """


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
    if request.method == 'POST':
        department = request.user.Department
        schedule, schedule_tuple = Schedule.objects.get_or_create(Department=department)
        submitted_lectures = []
        raw_data = json.loads(request.body.decode('utf-8'))
        lectures = raw_data.get('lectures', [])
        for lecture in lectures:
            semester_unit = lecture['semester_unit']
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
            start_time = int(lecture_to_create['time'][0])*100
            if (len(lecture_to_create['time']) > 1):
                end_time = int(lecture_to_create['time'][1])*100
            else:
                end_time = (int(lecture_to_create['time'][0])+1)*100
            start_hour, start_minute = divmod(start_time, 100)
            end_hour, end_minute = divmod(end_time, 100)
            start = datetime.time(hour = start_hour, minute=start_minute)
            end = datetime.time(hour=end_hour, minute=end_minute)
            semester_unit_ = SemesterUnit.objects.get(id=lecture_to_create['semester_unit'])
            lecture = Lecture(
                    Schedule = schedule,
                    SemesterUnit = semester_unit_,
                    day=lecture_to_create['day'], 
                    Department=request.user.Department,
                    start = start,
                    end = end,
                )
            lecture.save()
        return JsonResponse({'success': True})
    else :
        return JsonResponse({'success': False, 'error': 'Method not allowed'})