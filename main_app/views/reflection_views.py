#main_app>views>reflection_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date

from ..models import JournalEntry
from ..forms import JournalForm

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



