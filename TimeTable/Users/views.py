from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

import pandas as pd

from .forms import *
from .models import *

from School.models import Year

# Create your views here.
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_ = form.cleaned_data.get('username')
            password_ = form.cleaned_data.get('password')
            user = authenticate(username=username_, password=password_)
            if user is not None:
                login(request, user)
                messages.success(request, f"Sign in successfull. Welcome  {username_}")
                return redirect('Schedule:Home-View')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Enter valid details")
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'signin.html', context)

def signup(request):
    form = NewUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, f"Sign up successfull.")
        return redirect('Schedule:Home-View')
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
    
@login_required(login_url='Users:Signin-View')
def signout(request):
    logout(request)
    return redirect('Schedule:Home-View')


@login_required(login_url='User:Login-View')
def bulk_user_registration(request):
    if request.method == 'POST':
        form = BulkUserForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            department = form.cleaned_data['department']
            user_type = form.cleaned_data['user_type']
            try:
                context = {}
                error_message = None
                df = pd.read_csv(csv_file)
                columns = df.columns
                if user_type == 'lecturer':
                    required_fields = ['username', 'password', 'email', 'first_name', 'last_name', 'day_pref', 'time_pref']
                    if set(required_fields) == set(columns):
                        context['data'] = df.to_html()
                        for _, row in df.iterrows():
                            username = row['username']
                            password = row['password']
                            email = row['email']
                            first_name = row['first_name']
                            last_name = row['last_name']
                            day_pref = row['day_pref']
                            time_pref = row['time_pref']
                            user = NewUser(username=username, password=password, email=email, first_name=first_name, last_name=last_name, day_pref=day_pref, time_pref=time_pref, Department=department)
                            user.save()
                            print("User saved: ", user)
                    else:
                        error_message =  'Invalid CSV format for lecturers.'
                        context['form'] = form
                elif user_type == 'student':
                    required_fields = ['username', 'password', 'email', 'first_name', 'last_name']
                    if set(required_fields) == set(columns):
                        for _, row in df.iterrows():
                            username = row['username']
                            password = row['password']
                            email = row['email']
                            first_name = row['first_name']
                            last_name = row['last_name']
                            year = Year.objects.get(Department=department, year=1)
                            user = NewUser(username=username, password=password, email=email, first_name=first_name, last_name=last_name, Year=year, Department=department)
                            user.save()
                            print("User saved: ", user)
                        context['data'] = df.to_html()
                    else:
                        error_message =  'Invalid CSV format for students.'
                        context['form'] = form
                else:
                    error_message =  'Invalid user type.'
                    context['form'] = form
                context['error_message'] = error_message
                return render(request, 'bulkRegister.html', context)

            except Exception as e:
                error_message =  f'Error reading the CSV file: {str(e)}'
                context['form'] = form
                context['error_message'] = error_message
                return render(request, 'bulkRegister.html', context)

            
    else:
        form = BulkUserForm()
    return render(request, 'bulkRegister.html', {'form': form})