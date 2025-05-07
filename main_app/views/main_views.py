# main_app/views/main_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from datetime import date
from ..forms import CustomUserCreationForm, EditProfileForm
from ..models import Profile, Habit, HabitCheckIn, SavedRecipe, MoodEntry

# ──────────────── STATIC PAGES ────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})

def about(request): 
    return render(request, "about.html")

# ──────────────── AUTH & USER ACCOUNT VIEWS ────────────────

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)  # ensure profile is created
            login(request, user)
            return redirect('onboarding-welcome')
        else:
            error_message = 'Invalid sign up — try again.'
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'error_message': error_message
    })

def login_view(request):
    error_message = ''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid username or password.'
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {
        'form': form,
        'error_message': error_message
    })


@login_required
def profile(request):
    today = date.today()
    habits = Habit.objects.filter(user=request.user)
    checkins = HabitCheckIn.objects.filter(habit__in=habits, date=today)
    checked_ids = [checkin.habit.id for checkin in checkins]

    saved_recipes = SavedRecipe.objects.filter(user=request.user)

    return render(request, 'user/profile.html', {
        'habits': habits,
        'checked_ids': checked_ids,
        'today': today,
        'saved_recipes': saved_recipes,
    })

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.refresh_from_db() 
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'user/edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'user/confirm_delete.html')