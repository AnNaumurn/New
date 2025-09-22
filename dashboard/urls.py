from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dash/',views.demo,name="home"),
    path('profile/',views.profile,name="mypost"),
    
    path('login/',views.login,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('register/',views.register,name="register"),
    path('add_post/',views.add_post,name="add_post"),

    
    
]
