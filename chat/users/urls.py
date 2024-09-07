from django.urls import path, include
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('authentication/', include('django.contrib.auth.urls')),
    path('', lambda request: redirect('authentication/login/')),
    path('register/', views.register, name='register'),
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    path('friends/', views.show_friends_list, name='show_friends_list'),
    path('chats/', views.show_chats, name='show_chats'),
]