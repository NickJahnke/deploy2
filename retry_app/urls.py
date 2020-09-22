from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    #redirect
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('create_thought',views.create_thought),
    path('like_thought/<thought_id>',views.like_thought),
    path('unlike_thought/<thought_id>',views.unlike_thought),
    path('remove_thought/<thought_id>',views.remove_thought),
    


    #render
    path('thoughts',views.show_thoughts),
    path('thoughts/<thought_id>',views.show_details),
]