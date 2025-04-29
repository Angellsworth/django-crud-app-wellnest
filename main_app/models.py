# main_app/models.py

from django.db import models

class Habit(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    frequency = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title