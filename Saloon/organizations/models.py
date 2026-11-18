from django.contrib.auth.models import User
from django.db import models


class BusinessProfile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=220, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    opening_time = models.TimeField(default='09:00:00')
    closing_time = models.TimeField(default='20:00:00')
    booking_buffer_minutes = models.PositiveIntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Service(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=120)
    duration_minutes = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f'{self.business.name} - {self.name}'


class TeamMember(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, default='Stylist')
    specialty = models.CharField(max_length=180, blank=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.role})'
