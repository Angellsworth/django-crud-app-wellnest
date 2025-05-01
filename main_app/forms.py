from django import forms
from .models import Habit, HabitCheckIn, JournalEntry, MoodEntry

# ──────────────── Habit Forms ────────────────
class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'frequency']

# ──────────────── Habit Check-In Form ────────────────
class HabitCheckInForm(forms.ModelForm):
    class Meta:
        model = HabitCheckIn
        fields = ['date', 'note']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'note': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Optional notes about this check-in...'
            })
        }

# ──────────────── Reflection / Journal Form ────────────────
class JournalForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['date', 'content']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your thoughts here...'
            })
        }
# ──────────────── Mood Entry Form ────────────────
class MoodForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['date', 'mood', 'note']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}  # this gives the browser calendar input
            ),
            'note': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Optional thoughts or notes...'
            }),
        }