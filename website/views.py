from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib import messages
from website.models import Profile


# Create your views here.


def HomePage(request):
    return render(request, 'home.html')

def RegisterPage(request):

    if (request.method == 'POST' ):

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        age = request.POST['age']
        email = request.POST['email']
        password = request.POST['password']
        

        user = User.objects.create_user(username = email, password = password, first_name= firstname, last_name = lastname)
        user.save()

        user_profile = Profile.objects.create(user=user, age=age)
        user_profile.save()

        return redirect('/')
    
    else:
        return render(request, 'register.html')


def LoginPage(request):

    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username = email, password=password)

        if(user is not None):
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Email or Password')

    return render(request, 'login.html')