from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def HomePage(request):
    return render(request, 'home.html')

def RegisterPage(request):
    return render(request, 'register.html')

def LoginPage(request):
    return render(request, 'login.html')