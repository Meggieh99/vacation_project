from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def home_page(request):
    return render(request, 'layout.html')

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def vacations_page(request):
    return render(request, 'vacations.html')

def logout_view(request):
    logout(request)
    return redirect('login')
