#main_app>urls.py
from django.urls import path
from . import views
from .views import login_view, resource_views, mood_views, onboarding_views




urlpatterns = [
    # ──────────────── Static Pages ────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # ──────────────── User Account ────────────────
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/login/', login_view, name='login'),

    # ──────────────── Habit URLs ────────────────
    path('habits/', views.habit_index, name='habit-index'),
    path('habits/create/', views.habit_create, name='habit-create'),
    path('habits/<int:habit_id>/', views.habit_detail, name='habit-detail'),
    path('habits/<int:habit_id>/edit/', views.habit_edit, name='habit-edit'),
    path('habits/<int:habit_id>/delete/', views.habit_delete, name='habit-delete'),
    path('habits/<int:habit_id>/add-checkin/', views.add_checkin, name='add-checkin'),

    # ──────────────── Reflection (Journal) URLs ────────────────
    path('reflections/', views.reflection_index, name='reflection-index'),
    path('reflections/create/', views.reflection_create, name='reflection-create'),
    path('reflections/<int:reflection_id>/', views.reflection_detail, name='reflection-detail'),
    path('reflections/<int:reflection_id>/edit/', views.reflection_edit, name='reflection-edit'),
    path('reflections/<int:reflection_id>/delete/', views.reflection_delete, name='reflection-delete'),

    # ──────────────── Mood URLs ────────────────
    path('moods/', views.mood_index, name='mood-index'),
    path('moods/create/', views.mood_create, name='mood-create'),
    path('moods/<int:mood_id>/', views.mood_detail, name='mood-detail'),
    path('moods/<int:mood_id>/edit/', views.mood_edit, name='mood-edit'),
    path('moods/<int:mood_id>/delete/', views.mood_delete, name='mood-delete'),
    path('api/mood-data/', mood_views.mood_data_api, name='mood-data-api'),

    # ──────────────── Resource Pages ────────────────
    path('resources/', views.resource_index, name='resource-index'),
    path('resources/find-therapist/', views.find_therapist, name='find-therapist'),
    path('resources/headspace/', views.headspace_index, name='headspace-index'),
    path('resources/headspace/recipes/', resource_views.headspace_recipes, name='headspace-recipes'),
    path('resources/headspace/meditations/', resource_views.headspace_meditations, name='headspace-meditations'),
    path('save-recipe/', resource_views.save_recipe, name='save-recipe'),
    path('delete-recipe/<int:recipe_id>/', resource_views.delete_saved_recipe, name='delete-recipe'),

    # ──────────────── Onboarding Pages ────────────────
    path('onboarding/welcome/', onboarding_views.onboarding_welcome, name='onboarding-welcome'),
    path('onboarding/', views.onboarding_start, name='onboarding-start'),
    path('onboarding/habits/', views.select_habits, name='onboarding-habits'),
    path('onboarding/mood/', views.onboarding_mood, name='onboarding-mood'),


    path('habits/<int:habit_id>/toggle-checkin/', views.toggle_checkin, name='toggle-checkin'),
]