from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from website.models import Profile, UserImages
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django.urls import reverse


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
       
        # return render(request, 'user_page')
        return HttpResponseRedirect(reverse('user_page'))
    
    else:
        return render(request, 'register.html')


def LoginPage(request):

    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username = email, password=password)

        if(user is not None):
            
            auth.login(request, user)
            
            # return render(request, 'user_page')
            return HttpResponseRedirect(reverse('user_page'))
        else:
            messages.info(request, 'Invalid Email or Password')

    return render(request, 'login.html')


def UserPage(request):
    context={}
    if(request.method == 'POST'):
        
        uploaded_file = request.FILES['document']
        
        fs = FileSystemStorage(location = settings.MEDIA_ROOT+'/'+str(request.user.username)+'/'+'output')
        fs.save(uploaded_file.name, uploaded_file)

        
        fs = FileSystemStorage(location = settings.MEDIA_ROOT+'/'+str(request.user.username)+'/'+'input')
        name = fs.save(uploaded_file.name, uploaded_file)
        


        user_image = UserImages.objects.create(user=request.user, input_image = str(request.user)+'/'+'input'+'/'+name, output_image = str(request.user)+'/'+'input'+'/'+name)
        user_image.save()
        
        user_obj = {'user': request.user, 'image': user_image.output_image}
        return render(request, 'user_page.html', user_obj)
    else:
        user_obj = {'user': request.user}
        return render(request, 'user_page.html', user_obj)

