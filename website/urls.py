from django.urls import path

from . import views


urlpatterns=[

    path('', views.HomePage, name = 'HomePage'),
    path('register/', views.RegisterPage),
    path('login/', views.LoginPage)
]