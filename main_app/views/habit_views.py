#main_app>views>habit_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date
from ..models import Habit
from ..forms import (
    HabitForm,
    HabitCheckIn,
    HabitCheckInForm)

# ──────────────── HABIT VIEWS ────────────────

@login_required
def habit_index(request):
    user = request.user
    habits = Habit.objects.filter(user=user)

    today = date.today()
    checkins_today = HabitCheckIn.objects.filter(habit__in=habits, date=today)
    checked_in_ids = set(checkins_today.values_list('habit_id', flat=True))

    for habit in habits:
        habit.has_checked_in_today = habit.id in checked_in_ids

    return render(request, 'habits/index.html', {'habits': habits})

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            new_habit = form.save(commit=False)
            new_habit.user = request.user
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

@login_required
def habit_detail(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    show_form = request.GET.get('show_form', False)
    form = HabitCheckInForm() if show_form else None
    return render(request, 'habits/habit_detail.html', {
        'habit': habit,
        'form': form
    })

@login_required
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

@login_required
def habit_delete(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    if request.method == 'POST':
        habit.delete()
        return redirect('habit-index')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})

@login_required
def add_checkin(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        form = HabitCheckInForm(request.POST)
        if form.is_valid():
            new_checkin = form.save(commit=False)
            new_checkin.habit = habit
            new_checkin.save()
    return redirect('habit-detail', habit_id=habit.id)


@login_required
def toggle_checkin(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        today = date.today()
        checkin = HabitCheckIn.objects.filter(habit=habit, date=today).first()

        if checkin:
            checkin.delete()
            checked_in = False
        else:
            HabitCheckIn.objects.create(habit=habit, date=today)
            checked_in = True

        return JsonResponse({'checked_in': checked_in})


