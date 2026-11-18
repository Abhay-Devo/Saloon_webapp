from django.contrib.auth.models import User
from django.db import models


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer / Client'),
        ('business_owner', 'Business Owner'),
        ('staff', 'Team Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.role})'
