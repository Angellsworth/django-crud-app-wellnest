from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Habit, HabitCheckIn, JournalEntry, MoodEntry


# ──────────────── User Forms ────────────────

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']
        labels = {
            'first_name': 'Your Name',
        }


# ──────────────── Habit Forms ────────────────

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'frequency']


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


# ──────────────── Journal (Reflection) Form ────────────────

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
                attrs={'type': 'date'}
            ),
            'note': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Optional thoughts or notes...'
            }),
        }