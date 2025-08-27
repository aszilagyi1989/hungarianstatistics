from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from allauth.account.forms import LoginForm, SignupForm
from django.contrib import messages

def homepage(request):
    return render(request, 'geoApp/home.html')