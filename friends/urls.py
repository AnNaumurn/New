from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('friends/',views.allFriends,name="friends"),
    path('friends_req/',views.friends_page,name="friends_req"),
    path("friends/respond/<int:req_id>/", views.respond_friend_request, name="respond_friend_request"),
    path('friend_req/<int:u_id>',views.friend_req,name="send_friend_request"),
    path("friends/profile/<int:u_id>/comments/", views.profile_with_comments, name="profile_comments"),

      
]
