from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Subquery, OuterRef
from django.shortcuts import render, HttpResponse
from django.core.serializers import serialize
from django.db.models import Count
import json

from School.models import Department
from Users.models import NewUser
from .models import *

# Create your views here.

# Assigning Rooms to departments
@login_required(login_url='Users:Signin-View')
def assign_room_view(request):
    if request.method == 'POST':
        print("Creating DepartmentRoom")
        department_id = request.POST.get('department_id')
        room_id = request.POST.get('room_id')
        RoomDepartment.objects.create(Department_id=department_id, Room_id=room_id)
        return HttpResponse(status=200)
    
    departments_with_room = RoomDepartment.objects.all()
    rooms_with_departments = RoomDepartment.objects.select_related('Room', 'Department')
    department_utilization = {}
    for room_dept in rooms_with_departments:
        department = room_dept.Department
        room_capacity = room_dept.Room.capacity
        num_students = NewUser.objects.filter(Department=department, group='student').count()
        if (num_students == room_capacity):
            utilization_status = "Utilized well"
        elif (room_capacity-num_students>40 or num_students-room_capacity>40):
            utilization_status = "Not utilized well"
        else:
            utilization_status = "Utilized well"
        department_utilization[department.name] = {
            'room': room_dept.Room,
            'num_students': num_students,
            'room_capacity': room_capacity,
            'utilization_status': utilization_status
        }
    departments = Department.objects.exclude(id__in=Subquery(departments_with_room.values('Department__id')))
    context = {
        'departments': departments,
        'departments_with_room': departments_with_room,
        'department_utilization': department_utilization,
    }
    return render(request, 'assignRoom.html', context)

def get_rooms(request):
    departments_with_room = RoomDepartment.objects.all()
    rooms = Room.objects.exclude(id__in=Subquery(departments_with_room.values('Room_id')))
    rooms_obj = list(rooms.values('id', 'name', 'Building'))
    return JsonResponse(rooms_obj, safe=False)

def get_updated_departments(request):
    departments_with_room = RoomDepartment.objects.all()
    rooms = Room.objects.exclude(id__in=Subquery(departments_with_room.values('Room_id')))
    rooms_obj = list(rooms.values('id', 'name', 'Building'))
    departments = Department.objects.exclude(id__in=Subquery(departments_with_room.values('Department__id')))
    data = {
        'departments': json.loads(serialize('json', departments)),
        'departments_with_room': json.loads(serialize('json', rooms_obj)),
    }
    print(data)
    return JsonResponse(data, safe=False)