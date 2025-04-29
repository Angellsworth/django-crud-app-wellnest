# main_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
     path('habits/', views.habit_index, name='habit-index'),
    path('habits/create/', views.habit_create, name='habit-create'),
]