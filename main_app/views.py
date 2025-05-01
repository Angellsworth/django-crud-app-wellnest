# ──────────────── IMPORTS ────────────────

from datetime import timedelta, date
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django import forms

from .models import Habit, JournalEntry, MoodEntry 
from .forms import HabitForm, HabitCheckInForm, JournalForm, MoodForm


# ──────────────── STATIC PAGES ────────────────

def home(request):
    return render(request, 'home.html')

def about(request): 
    return render(request, "about.html")


# ──────────────── HABIT VIEWS ────────────────

def habit_index(request):
    user = User.objects.first()
    habits = Habit.objects.filter(user=user)
    return render(request, 'habits/index.html', {'habits': habits})

def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            new_habit = form.save(commit=False)
            new_habit.user = User.objects.first()
            new_habit.save()
            return redirect('habit-index')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {
        'form': form,
        'form_title': 'New Habit',
        'submit_label': 'Create Habit',
        'back_link': 'habit-index',  
    })

def habit_detail(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    show_form = request.GET.get('show_form', False)
    form = HabitCheckInForm() if show_form else None
    return render(request, 'habits/habit_detail.html', {
        'habit': habit,
        'form': form
    })

def habit_edit(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit-index')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {
        'form': form,
        'form_title': 'Edit Habit',
        'submit_label': 'Update Habit',
        'back_link': 'habit-detail',
        'habit': habit,
    })

def habit_delete(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    if request.method == 'POST':
        habit.delete()
        return redirect('habit-index')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})

def add_checkin(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        form = HabitCheckInForm(request.POST)
        if form.is_valid():
            new_checkin = form.save(commit=False)
            new_checkin.habit = habit
            new_checkin.save()
    return redirect('habit-detail', habit_id=habit.id)


# ──────────────── JOURNAL (REFLECTION) VIEWS ────────────────

def reflection_index(request):
    user = User.objects.first()
    reflections = JournalEntry.objects.filter(user=user)
    return render(request, 'reflections/index.html', {'reflections': reflections})

def reflection_create(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            new_reflection = form.save(commit=False)
            new_reflection.user = User.objects.first()
            new_reflection.save()
            return redirect('reflection-index')
    else:
        form = JournalForm()
    return render(request, 'reflections/reflections_form.html', {
        'form': form,
        'form_title': 'New Journal Entry',
        'submit_label': 'Save Entry',
        'back_link': 'reflection-index',
    })

def reflection_detail(request, reflection_id):
    reflection = get_object_or_404(JournalEntry, id=reflection_id)
    return render(request, 'reflections/reflection_detail.html', {
        'reflection': reflection
    })

def reflection_edit(request, reflection_id):
    reflection = get_object_or_404(JournalEntry, id=reflection_id)
    if request.method == 'POST':
        form = JournalForm(request.POST, instance=reflection)
        if form.is_valid():
            form.save()
            return redirect('reflection-detail', reflection_id=reflection.id)
    else:
        form = JournalForm(instance=reflection)
    return render(request, 'reflections/reflections_form.html', {
        'form': form,
        'form_title': 'Edit Journal Entry',
        'submit_label': 'Update Entry',
        'back_link': 'reflection-detail',
        'reflection': reflection,
    })

def reflection_delete(request, reflection_id):
    reflection = get_object_or_404(JournalEntry, id=reflection_id)
    if request.method == 'POST':
        reflection.delete()
        return redirect('reflection-index')
    return render(request, 'reflections/reflections_confirm_delete.html', {
        'reflection': reflection
    })


# ──────────────── MOOD VIEWS ────────────────

# Map each mood label to a numeric score for charting
MOOD_TO_SCORE = {
    'ecstatic': 10,
    'happy': 9,
    'content': 8,
    'grateful': 7,
    'hopeful': 6,
    'neutral': 5,
    'nesting': 4,
    'tired': 3,
    'lonely': 3,
    'anxious': 2,
    'sad': 2,
    'angry': 1,
    'overwhelmed': 1,
}

def mood_index(request):
    user = User.objects.first()

    # Get date range filter from query string
    allowed_ranges = [7, 30, 90, 365]
    default_range = 30
    try:
        days = int(request.GET.get('range', default_range))
        if days not in allowed_ranges:
            days = default_range
    except ValueError:
        days = default_range

    start_date = date.today() - timedelta(days=days)

    # Filter moods and prepare chart data
    moods = MoodEntry.objects.filter(user=user, date__gte=start_date).order_by('date')
    chart_labels = [m.date.strftime('%b %d') for m in moods]
    chart_data = [MOOD_TO_SCORE.get(m.mood, 5) for m in moods]

    return render(request, 'moods/index.html', {
        'moods': moods,
        'range': days,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    })

def mood_create(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            new_mood = form.save(commit=False)
            new_mood.user = User.objects.first()
            new_mood.save()
            return redirect('mood-index')
    else:
        form = MoodForm()
    return render(request, 'moods/mood_form.html', {
        'form': form,
        'form_title': 'Log a Mood',
        'submit_label': 'Save Mood',
        'back_link': 'mood-index',
    })

def mood_detail(request, mood_id):
    mood = get_object_or_404(MoodEntry, id=mood_id)
    return render(request, 'moods/mood_detail.html', {'mood': mood})

def mood_edit(request, mood_id):
    mood = get_object_or_404(MoodEntry, id=mood_id)
    if request.method == 'POST':
        form = MoodForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            return redirect('mood-detail', mood_id=mood.id)
    else:
        form = MoodForm(instance=mood)
    return render(request, 'moods/mood_form.html', {
        'form': form,
        'form_title': 'Edit Mood',
        'submit_label': 'Update Mood',
        'back_link': 'mood-detail',
        'mood': mood,
    })

def mood_delete(request, mood_id):
    mood = get_object_or_404(MoodEntry, id=mood_id)
    if request.method == 'POST':
        mood.delete()
        return redirect('mood-index')
    return render(request, 'moods/mood_confirm_delete.html', {'mood': mood})