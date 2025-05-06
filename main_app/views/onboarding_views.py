from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import HabitCategory, HabitTemplate, Habit, Profile
import logging
logger = logging.getLogger(__name__)

# ──────────────── ONBOARDING STEP 1: Start with Mind Category ────────────────
@login_required
def onboarding_start(request):
    profile = request.user.profile
    if profile.has_completed_onboarding:
        return redirect('profile')

    request.session['category_index'] = 0  # Start at first category
    request.session['selected_habits'] = []
    return redirect('onboarding-habits')

def onboarding_welcome(request):
    if request.method == 'POST':
        return redirect('onboarding-start')
    return render(request, 'onboarding/welcome.html')


# ──────────────── ONBOARDING STEP 2: Habit Selection ────────────────
@login_required
def select_habits(request):
    # Define fixed order
    category_order = ['mind', 'body', 'soul', 'family']

    index = request.session.get('category_index', 0)
    print("Current index:", index)

    if index >= len(category_order):
        selected_ids = request.session.get('selected_habits', [])
        for habit_id in selected_ids:
            template = HabitTemplate.objects.get(id=habit_id)
            if not Habit.objects.filter(user=request.user, title=template.title).exists():
                Habit.objects.create(
                    user=request.user,
                    title=template.title,
                    description=template.description,
                    frequency=template.frequency,
                )

        # Clear session
        request.session.pop('category_index', None)
        request.session.pop('selected_habits', None)

        return redirect('onboarding-mood')

    # Current category
    current_slug = category_order[index]
    current_category = HabitCategory.objects.filter(slug=current_slug).first()
    if not current_category:
        return render(request, 'onboarding/missing_category.html', {'slug': current_slug})
    habit_templates = HabitTemplate.objects.filter(category=current_category)

    if request.method == 'POST':
        selected = request.POST.getlist('habits')
        existing = request.session.get('selected_habits', [])
        request.session['selected_habits'] = existing + selected
        request.session['category_index'] = index + 1
        return redirect('onboarding-habits')

    progress_percent = int((index + 1) / len(category_order) * 100)

    return render(request, 'onboarding/select_habits.html', {
        'category': current_category,
        'habit_templates': habit_templates,
        'current_step': index + 1,
        'total_steps': len(category_order),
        'progress_percent': progress_percent,
    })


# ──────────────── ONBOARDING STEP 3: Mood Check-in ────────────────
@login_required
def onboarding_mood(request):
    profile = request.user.profile
    profile.has_completed_onboarding = True
    profile.save()
    return redirect('profile')
