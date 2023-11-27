from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import is_valid_path

from .forms import *
from .models import *

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
    

def signout(request):
    pass