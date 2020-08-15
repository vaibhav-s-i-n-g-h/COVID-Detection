from django.urls import path  
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from . import views


urlpatterns=[

    path('', views.HomePage, name = 'HomePage'),
    path('register/', views.RegisterPage),
    path('login/', views.LoginPage, name= 'login_page'),
    path('logout/', views.LogoutPage),
    path('user_page/', views.UserPage, name='user_page')
] + static(settings.MEDIA_URL, document_root = (settings.MEDIA_ROOT))