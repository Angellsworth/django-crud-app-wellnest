# main_app/views/mood_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import json

from ..models import MoodEntry
from ..forms import MoodForm

# ──────────────── MOOD VIEWS ────────────────

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

@login_required
def mood_index(request):
    user = request.user
    allowed_ranges = [7, 30, 90, 365]
    default_range = 30
    try:
        days = int(request.GET.get('range', default_range))
        if days not in allowed_ranges:
            days = default_range
    except ValueError:
        days = default_range

    start_date = date.today() - timedelta(days=days)
    moods = MoodEntry.objects.filter(user=user, date__gte=start_date).order_by('date')
    chart_labels = [m.date.strftime('%b %d') for m in moods]
    chart_data = [MOOD_TO_SCORE.get(m.mood, 5) for m in moods]

    return render(request, 'moods/index.html', {
        'moods': moods,
        'range': days,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    })

@login_required
def mood_create(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            new_mood = form.save(commit=False)
            new_mood.user = request.user
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

@login_required
def mood_detail(request, mood_id):
    mood = get_object_or_404(MoodEntry, id=mood_id)
    return render(request, 'moods/mood_detail.html', {'mood': mood})

@login_required
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

@login_required
def mood_delete(request, mood_id):
    mood = get_object_or_404(MoodEntry, id=mood_id)
    if request.method == 'POST':
        mood.delete()
        return redirect('mood-index')
    return render(request, 'moods/mood_confirm_delete.html', {'mood': mood})

