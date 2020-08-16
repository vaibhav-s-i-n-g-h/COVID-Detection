from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from website.models import Profile, UserImages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from subprocess import run, PIPE, Popen
from django.urls import reverse
import sys
import os
import shutil
# Create your views here.

first_name = ""
last_name = ""


def HomePage(request):
    
    if(request.user.is_authenticated):
        auth.logout(request)  
 
    user_obj = {'hello':'hello world','covid1': '/media/covid_1.png' , 'covid2': '/media/covid_2.png', 'covid3': '/media/covid_3.png'}
    return render(request, 'home.html', user_obj)

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

        first_name = firstname
        last_name = lastname

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


def LogoutPage(request):

    auth.logout(request)
    return HttpResponseRedirect(reverse('HomePage'))

def UserPage(request):
    
    if(request.user.is_authenticated):

        if(request.method == 'POST' and len(request.FILES) != 0):
            

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            shutil.rmtree(BASE_DIR+'/'+'website'+'/'+'methods'+'/'+'input'+'/'+'covid')

            uploaded_file = request.FILES['document']
            
            fs = FileSystemStorage(location = settings.MEDIA_ROOT+'/'+str(request.user.username)+'/'+'output')
            fs.save('trial', uploaded_file)
            os.remove(settings.MEDIA_ROOT+'/'+str(request.user.username)+'/'+'output/'+'trial')    
            
            fs = FileSystemStorage(location = settings.MEDIA_ROOT+'/'+str(request.user.username)+'/'+'input')
            name = fs.save(uploaded_file.name, uploaded_file)
            
            fs = FileSystemStorage(location = BASE_DIR+'/'+'website'+'/'+'methods'+'/'+'input'+'/'+'covid')
            name = fs.save(uploaded_file.name, uploaded_file)

            output_image_name_fetureMap = str(request.user)+'/'+'output'+'/'+'featureMap_'+name
            output_image_name_gradcam = str(request.user)+'/'+'output'+'/'+'gradcam_'+name
            output_image_name_fetureMap2 = str(request.user)+'/'+'output'+'/'+'featureMap2_'+name
            output_image_name_gradcam2 = str(request.user)+'/'+'output'+'/'+'gradcam2_'+name


            user_image = UserImages.objects.create(user=request.user, input_image = str(request.user)+'/'+'input'+'/'+name, output_image_featureMap = output_image_name_fetureMap, output_image_gradcam = output_image_name_gradcam, output_image_featureMap2 = output_image_name_fetureMap2, output_image_gradcam2 = output_image_name_gradcam2)
            user_image.save()
            

            #Processing from external python script    
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            out = run([sys.executable, os.path.join(BASE_DIR, 'website\methods\image_load.py'), BASE_DIR+'/'+'website'+'/'+'methods',BASE_DIR+'/'+'website'+'/'+'images/', output_image_name_fetureMap, output_image_name_gradcam, output_image_name_fetureMap2, output_image_name_gradcam2], stdout = PIPE)
            # print(out.stdout.decode())
            
            user_obj = {'user': request.user, 'featureMap1': user_image.output_image_featureMap,'featureMap2': user_image.output_image_featureMap2,'gradcam1': user_image.output_image_gradcam,'gradcam2': user_image.output_image_gradcam2,'test': out.stdout.decode(),'input_image': user_image.input_image}
            return render(request, 'user_page.html', user_obj)
        
        else:

            user_obj = {'user': request.user}
            return render(request, 'user_page.html', user_obj)
    else:
        
        return HttpResponseRedirect(reverse('login_page'))
