# ──────────────── IMPORTS ────────────────

from datetime import timedelta, date
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Habit, JournalEntry, MoodEntry
from .forms import (
    HabitForm,
    HabitCheckInForm,
    JournalForm,
    MoodForm,
    CustomUserCreationForm,
    EditProfileForm,
)


# ──────────────── STATIC PAGES ────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})

def about(request): 
    return render(request, "about.html")


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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up — try again.'
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'error_message': error_message
    })


# ──────────────── HABIT VIEWS ────────────────

@login_required
def habit_index(request):
    user = request.user
    habits = Habit.objects.filter(user=user)
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


# ──────────────── JOURNAL (REFLECTION) VIEWS ────────────────

PROMPTS = [
    "What does \"enough\" feel like to you?",
    "What part of your life feels most aligned right now?",
    "Describe a moment you felt deeply understood.",
    "What do you want to give yourself permission to release?",
    "Who are you becoming?",
    "What do you wish others knew about your inner world?",
    "Write about a memory that makes you feel rooted.",
    "What would it look like to be radically gentle with yourself today?",
    "What fear are you ready to outgrow?",
    "What needs your attention that you have been avoiding?",
    "Where is softness showing up in your life?",
    "What have you survived that you are proud of?",
    "What would it mean to trust your timing?",
    "Describe the kind of love you want to give yourself.",
    "What are three beliefs you are ready to challenge?",
    "What do you long for more of — and how can you invite it in?",
    "What story are you telling yourself right now?",
    "What are your emotional anchors?",
    "What has your body been trying to tell you lately?",
    "If you could whisper one truth to your younger self, what would it be?",
    "What habits are nurturing the life you want?",
    "What does a peaceful day look like for you?",
    "Write a list of things you want to savor slowly.",
    "What are you unlearning right now?",
    "What does your healing voice sound like?",
    "What do you want to remember the next time you are overwhelmed?",
    "What are you proud of that no one else saw?",
    "Describe a recent moment of bravery, no matter how small.",
    "What does rest mean to you today?",
    "If your heart wrote a letter to your mind, what would it say?",
    "What does 'home' feel like in your body?",
    "What is a soft boundary you want to create?",
    "Who inspires you to grow gently?",
    "What are you holding onto that is too heavy?",
    "How do you reconnect with yourself after feeling off-center?",
    "What does spaciousness mean to you?",
    "What kind of support are you craving?",
    "What season of life are you in right now — and how can you honor it?",
    "What version of yourself are you shedding?",
    "Where is love showing up unexpectedly?",
    "What parts of you need celebration today?",
]

def get_rotating_prompt():
    index = date.today().timetuple().tm_yday % len(PROMPTS)
    return PROMPTS[index]

@login_required
def reflection_index(request):
    user = request.user
    reflections = JournalEntry.objects.filter(user=user)
    return render(request, 'reflections/index.html', {'reflections': reflections})

@login_required
def reflection_create(request):
    prompt = get_rotating_prompt()
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            new_reflection = form.save(commit=False)
            new_reflection.user = request.user
            new_reflection.save()
            return redirect('reflection-index')
    else:
        form = JournalForm()
    return render(request, 'reflections/reflections_form.html', {
        'form': form,
        'form_title': 'New Journal Entry',
        'submit_label': 'Save Entry',
        'back_link': 'reflection-index',
        'prompt': prompt,
    })

@login_required
def reflection_detail(request, reflection_id):
    reflection = get_object_or_404(JournalEntry, id=reflection_id)
    return render(request, 'reflections/reflection_detail.html', {
        'reflection': reflection
    })

@login_required
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

@login_required
def reflection_delete(request, reflection_id):
    reflection = get_object_or_404(JournalEntry, id=reflection_id)
    if request.method == 'POST':
        reflection.delete()
        return redirect('reflection-index')
    return render(request, 'reflections/reflections_confirm_delete.html', {
        'reflection': reflection
    })

def mood_index(request):
    return render(request, 'moods/index.html') 


# ──────────────── HABIT VIEWS ────────────────

@login_required
def habit_index(request):
    user = request.user
    habits = Habit.objects.filter(user=user)
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


# ──────────────── JOURNAL (REFLECTION) VIEWS ────────────────
PROMPTS = [
    "What does \"enough\" feel like to you?",
    "What part of your life feels most aligned right now?",
    "Describe a moment you felt deeply understood.",
    "What do you want to give yourself permission to release?",
    "Who are you becoming?",
    "What do you wish others knew about your inner world?",
    "Write about a memory that makes you feel rooted.",
    "What would it look like to be radically gentle with yourself today?",
    "What fear are you ready to outgrow?",
    "What needs your attention that you have been avoiding?",
    "Where is softness showing up in your life?",
    "What have you survived that you are proud of?",
    "What would it mean to trust your timing?",
    "Describe the kind of love you want to give yourself.",
    "What are three beliefs you are ready to challenge?",
    "What do you long for more of — and how can you invite it in?",
    "What story are you telling yourself right now?",
    "What are your emotional anchors?",
    "What has your body been trying to tell you lately?",
    "If you could whisper one truth to your younger self, what would it be?",
    "What habits are nurturing the life you want?",
    "What does a peaceful day look like for you?",
    "Write a list of things you want to savor slowly.",
    "What are you unlearning right now?",
    "What does your healing voice sound like?",
    "What do you want to remember the next time you are overwhelmed?",
    "What are you proud of that no one else saw?",
    "Describe a recent moment of bravery, no matter how small.",
    "What does rest mean to you today?",
    "If your heart wrote a letter to your mind, what would it say?",
    "What does 'home' feel like in your body?",
    "What is a soft boundary you want to create?",
    "Who inspires you to grow gently?",
    "What are you holding onto that is too heavy?",
    "How do you reconnect with yourself after feeling off-center?",
    "What does spaciousness mean to you?",
    "What kind of support are you craving?",
    "What season of life are you in right now — and how can you honor it?",
    "What version of yourself are you shedding?",
    "Where is love showing up unexpectedly?",
    "What parts of you need celebration today?",
]

@login_required
def reflection_index(request):
    user = request.user
    reflections = JournalEntry.objects.filter(user=user)
    return render(request, 'reflections/index.html', {'reflections': reflections})

def get_rotating_prompt():
    index = date.today().timetuple().tm_yday % len(PROMPTS)
    return PROMPTS[index]

@login_required
def reflection_create(request):
    prompt = get_rotating_prompt()

    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            new_reflection = form.save(commit=False)
            new_reflection.user = request.user
            new_reflection.save()
            return redirect('reflection-index')
    else:
        form = JournalForm()

    return render(request, 'reflections/reflections_form.html', {
        'form': form,
        'form_title': 'New Journal Entry',
        'submit_label': 'Save Entry',
        'back_link': 'reflection-index',
        'prompt': prompt,  # ← this is new!
    })

@login_required
def reflection_detail(request, reflection_id):
    reflection = get_object_or_404(JournalEntry, id=reflection_id)
    return render(request, 'reflections/reflection_detail.html', {
        'reflection': reflection
    })

@login_required
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

@login_required
def reflection_delete(request, reflection_id):
    reflection = get_object_or_404(JournalEntry, id=reflection_id)
    if request.method == 'POST':
        reflection.delete()
        return redirect('reflection-index')
    return render(request, 'reflections/reflections_confirm_delete.html', {
        'reflection': reflection
    })


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


# ──────────────── AUTH & DASHBOARD ────────────────

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up — try again.'
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {
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


# ──────────────── RESOURCE VIEWS ────────────────

def resource_index(request):
    return render(request, 'resources/resource_index.html')

def find_therapist(request):
    return render(request, 'resources/find_therapist.html')


# ──────────────── HEADSPACE VIEWS ────────────────

def headspace_index(request):
    return render(request, 'resources/headspace_index.html')

def headspace_meditations(request):
    return render(request, 'resources/headspace_meditations.html')



