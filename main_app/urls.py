from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # ──────────────── Habit URLs ────────────────
    path('habits/', views.habit_index, name='habit-index'),
    path('habits/create/', views.habit_create, name='habit-create'),
    path('habits/<int:habit_id>/', views.habit_detail, name='habit-detail'),
    path('habits/<int:habit_id>/edit/', views.habit_edit, name='habit-edit'),
    path('habits/<int:habit_id>/delete/', views.habit_delete, name='habit-delete'),
    path('habits/<int:habit_id>/add-checkin/', views.add_checkin, name='add-checkin'),

    # ──────────────── Reflection URLs ────────────────
    path('reflections/', views.reflection_index, name='reflection-index'),
    path('reflections/create/', views.reflection_create, name='reflection-create'),
    path('reflections/<int:reflection_id>/', views.reflection_detail, name='reflection-detail'),
    path('reflections/<int:reflection_id>/edit/', views.reflection_edit, name='reflection-edit'),
    path('reflections/<int:reflection_id>/delete/', views.reflection_delete, name='reflection-delete'),

    # ──────────────── Mood URLs ────────────────
    path('moods/', views.mood_index, name='mood-index'),
    path('moods/create/', views.mood_create, name='mood-create'),
    path('moods/<int:mood_id>/', views.mood_detail, name='mood-detail'),
]