from django.contrib import admin
from .models import Habit, HabitCheckIn, MoodEntry, JournalEntry
from .models import HabitTemplate

admin.site.register(HabitTemplate)
admin.site.register(Habit)
admin.site.register(HabitCheckIn)
admin.site.register(MoodEntry)
admin.site.register(JournalEntry)