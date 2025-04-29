# main_app/views.py

from django.shortcuts import render, redirect
from .forms import HabitForm 
from .models import Habit

def home(request):
    return render(request, 'home.html')

def about(request): 
    return render(request, "about.html")

def habit_index(request):
    habits = Habit.objects.all()
    return render(request, 'habits/index.html', {'habits': habits})

def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            new_habit = form.save()
            return redirect('habit-index')
    else:
        form = HabitForm()

    return render(request, 'habits/habit_form.html', {'form': form})