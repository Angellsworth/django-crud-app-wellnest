# main_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


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
    ('nesting', '🪺 Nesting'),  
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
    # mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    mood = models.IntegerField()
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

# ──────────────── User Profile Model ────────────────

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_completed_onboarding = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# ──────────────── Habit Onboarding Templates ────────────────

class HabitCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class HabitTemplate(models.Model):
    category = models.ForeignKey(HabitCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    frequency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} ({self.category.name})"
    


class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return f"{self.title} saved by {self.user.username}"

class SavedMeditation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_id = models.CharField(max_length=100)
    url = models.URLField()