from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Subquery, OuterRef
from django.shortcuts import render, HttpResponse
from django.core.serializers import serialize
import json
from School.models import Department
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
    departments = Department.objects.exclude(id__in=Subquery(departments_with_room.values('Department__id')))
    context = {
        'departments': departments,
        'departments_with_room': departments_with_room
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