from django.contrib.auth.models import User
from django.db import models


class CustomerProfile(models.Model):
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('non_binary', 'Non-binary'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=24, choices=GENDER_CHOICES, default='prefer_not_to_say')
    date_of_birth = models.DateField(blank=True, null=True)
    preferred_services = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.user.username
