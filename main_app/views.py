#main_app>views.py
# ──────────────── IMPORTS ────────────────

from datetime import timedelta, date
import json

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import JournalEntry, MoodEntry
from .forms import (
    JournalForm,
    MoodForm,
    CustomUserCreationForm,
    EditProfileForm,
)

# ──────────────── AUTH & DASHBOARD ────────────────

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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


# ──────────────── USER ACCOUNT VIEWS ────────────────


@login_required
def profile(request):
    return render(request, 'user/profile.html')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
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


