from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q, Subquery
from django.http import JsonResponse
from django.shortcuts import render, redirect
import datetime
import json
from School.models import Year
from Room.models import RoomDepartment, Room
from Unit.models import SemesterUnit, Lecture
from .models import Schedule

# Create your views here.
@login_required(login_url='Users:Signin-View')
def home(request):
    context = {}
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
    if (request.user.Department):
        schedule = Schedule.objects.filter(Department=request.user.Department)
        context["schedule"] = schedule
        if len(schedule)>0:
            schedule = schedule[0]
            if (schedule.accepted == True):
                context["accepted"] = True
                department = request.user.Department
                if request.user.group == "student":
                    years = Year.objects.filter(Department=department)
                    # Internal
                    internal_semesterUnits = SemesterUnit.objects.filter(Year__in=years).filter(Unit__Department=request.user.Department)
                    internal_units = [unit.Unit for unit in internal_semesterUnits]
                    internal_lectures = Lecture.objects.filter(SemesterUnit__Unit__in=internal_units)
                    internal_lectures_json = json.loads(serialize('json', internal_lectures))
                    
                    # External
                    external_semesterUnits = SemesterUnit.objects.filter(Year__in=years).filter(~Q(Unit__Department=request.user.Department))
                    external_units = [unit.Unit for unit in external_semesterUnits]
                    external_lectures = Lecture.objects.filter(SemesterUnit__Unit__in=external_units)
                    external_lectures_json = json.loads(serialize('json', external_lectures))
                    context["internal_lectures"] = internal_lectures_json
                    context['external_lectures'] = external_lectures_json
                elif request.user.group == "lecturer":
                    internal_semesterUnits = SemesterUnit.objects.filter(Lecturer=request.user)
                    internal_units = [unit.Unit for unit in internal_semesterUnits]
                    internal_lectures = Lecture.objects.filter(SemesterUnit__Unit__in=internal_units)
                    internal_lectures_json = json.loads(serialize('json', internal_lectures))    
                    context["internal_lectures"] = internal_lectures_json            
            else:
                context["accepted"] = False
    return render(request, 'home.html', context)

@login_required(login_url='Users:Signin-View')
def create_schedule(request):
    if request.user.group == 'lecturer':
        schedule = Schedule.objects.filter(Department=request.user.Department)
        if (len(schedule)>0):
            return redirect("Schedule:Home-View")
        external_semester_units = SemesterUnit.objects.filter(Department=request.user.Department).filter(~Q(Unit__Department=request.user.Department))
        check = "Empty"
        for unit_ in external_semester_units:
            department_schedule = Schedule.objects.filter(Department=unit_.Unit.Department)
            if (len(department_schedule) > 0):
                if (department_schedule[0].accepted == False):
                    check = "Invalid"
                else:
                    check = "Valid"
            else:
                check = "None"
        # pass to front end
        if check == "Valid" or check == "Empty":
            department = request.user.Department
            years = Year.objects.filter(Department=department)
            semesterUnits = SemesterUnit.objects.filter(Year__in=years).filter(Unit__Department=request.user.Department)
            external_semesterUnits = SemesterUnit.objects.filter(Year__in=years).filter(~Q(Unit__Department=request.user.Department))
            external_units = [unit.Unit for unit in external_semesterUnits]
            external_lectures = Lecture.objects.filter(SemesterUnit__Unit__in=external_units)
            external_lectures_json = json.loads(serialize('json', external_lectures))
            if len(semesterUnits)>0:
                context = {
                    'semester_units':semesterUnits,
                    'external_lectures': external_lectures_json,
                }
            else:
                context = {
                    "message": "Awaiting creation of semester units"
                }
        elif check == "Invalid":
            context = {
                "message": "Awaiting approval of schedule for external units"
            }
        elif check == "None":
            context = {
                "message": "Awaiting creation and approval of schedule for external units"
            }
        return render(request, 'createschedule.html', context)
    elif request.user.group == 'student':
        return redirect("Schedule:Home-View")
    
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

def get_lecturer_time_preferebce(request, semesterUnit_id):
    if semesterUnit_id:
        semesterUnit = SemesterUnit.objects.get(id=semesterUnit_id)
        lecturer = semesterUnit.Lecturer
        preference = {'time': lecturer.time_pref, 'day': lecturer.day_pref}
        return JsonResponse(preference, safe=False)
    else:
        return JsonResponse({'error': "No lecturer passed"}, status=400)

def save_lectures(request):
    if request.method == 'POST':
        department = request.user.Department
        schedule, schedule_tuple = Schedule.objects.get_or_create(Department=department)
        submitted_lectures = []
        raw_data = json.loads(request.body.decode('utf-8'))
        lectures = raw_data.get('lectures', [])
        for lecture in lectures:
            print("Lecture: ", lecture)
            semester_unit = lecture['semester_unit']
            if not any(lecture['time'] == submitted['time'] for submitted in submitted_lectures):
                if (lecture['time'] is not None):
                    print("Lecture: ", lecture)
                    lecture_ = {
                        "semester_unit": semester_unit,
                        "room": lecture['room'],
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
            room = Room.objects.get(id=lecture_to_create['room'])
            semester_unit_ = SemesterUnit.objects.get(id=lecture_to_create['semester_unit'])
            lecture = Lecture(
                    Schedule = schedule,
                    SemesterUnit = semester_unit_,
                    day=lecture_to_create['day'], 
                    Department=request.user.Department,
                    Room=room,
                    Year = semester_unit_.Year,
                    start = start,
                    end = end,
                )
            lecture.save()
        return JsonResponse({'success': True})
    else :
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    
def get_lecture_units(request, semesterUnit_id):
    if semesterUnit_id:
        semesterUnit = SemesterUnit.objects.get(id=semesterUnit_id)
        lecture = Lecture.objects.get(SemesterUnit=semesterUnit)
        unit = {"code": semesterUnit.Unit.code, "name": semesterUnit.Unit.name, "room": lecture.Room.name}
        return JsonResponse(unit, safe=False)
    else:
        return JsonResponse({'error': "Semester Unit Id is not provided"}, status=400)

def get_free_rooms(request):
    if request.method == "POST":
        try:
            raw_data = json.loads(request.body.decode('utf-8'))
            time_data = datetime.datetime.strptime(raw_data['time'], '%H:%M').time()
            # print("Time: ", time_data)
            free_rooms = []
            departments_with_room = RoomDepartment.objects.all()
            unassigned  = Room.objects.exclude(id__in=Subquery(departments_with_room.values('Room_id')))
            rooms = Room.objects.all()
            for room in rooms:
                if (room not in unassigned):
                    lectures = Lecture.objects.filter(Room=room, day=raw_data['day'])
                    # print("Lectures: ", lectures, " with room: ", room)
                    if (len(lectures)<1):
                        # print("Appending for room: ", room)
                        free_rooms.append(room)
                    else:
                        valid = True
                        for lecture in lectures:
                            # print("====================")
                            # print("Lecture: ", lecture)
                            start = lecture.start.hour
                            end = lecture.end.hour
                            # print("Start time: ", start, " vs time checking: ", time_data.hour, "Time end: ", end, " vs time ending check: ", time_data.hour)
                            if (time_data.hour >= start):
                                if (time_data.hour < end):
                                    # print("Found lecture in time slot")
                                    valid = False
                                    break
                        if (valid == True):
                            free_rooms.append(room)
            free_rooms = json.loads(serialize('json', free_rooms))
            unassigned = json.loads(serialize('json', unassigned))
            return JsonResponse({'success': True, 'data': {'free': free_rooms, 'unassigned': unassigned}})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})