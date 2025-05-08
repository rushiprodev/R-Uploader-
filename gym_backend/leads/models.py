# gym_backend/leads/models.py

from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) # Consider making email unique if it should be
    phone = models.CharField(max_length=20) # Suitable for 10-digit numbers + potential formatting/country codes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

