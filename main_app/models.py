# main_app/models.py

from django.db import models
from django.contrib.auth.models import User

# ──────────────── Mood Options ────────────────
MOOD_CHOICES = [
    ('ecstatic', '😄 Ecstatic'),
    ('happy', '🙂 Happy'),
    ('content', '😊 Content'),
    ('neutral', '😐 Neutral'),
    ('tired', '😴 Tired'),
    ('anxious', '😰 Anxious'),
    ('sad', '😢 Sad'),
    ('angry', '😠 Angry'),
    ('overwhelmed', '😩 Overwhelmed'),
    ('lonely', '🥺 Lonely'),
    ('grateful', '🙏 Grateful'),
    ('hopeful', '🌱 Hopeful'),
    ('nesting', '🪺 Nesting'),  # symbolic, restorative mood
]

# ──────────────── Habit Models ────────────────

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    frequency = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HabitCheckIn(models.Model):
    date = models.DateField('Check-in date')
    note = models.TextField(blank=True)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)

    def __str__(self):
        return f"Check-in for {self.habit.title} on {self.date}"

    class Meta:
        ordering = ['-date']

# ──────────────── Mood Models ────────────────

class MoodEntry(models.Model):
    date = models.DateField('Mood date')
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.mood} on {self.date}"

    class Meta:
        ordering = ['-date']

# ──────────────── Journal Models ────────────────

class JournalEntry(models.Model):
    date = models.DateField('Entry date')
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Journal on {self.date} by {self.user.username}"

    class Meta:
        ordering = ['-date']