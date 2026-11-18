from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from organizations.models import BusinessProfile

from .models import UserRole


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserRole.objects.update_or_create(
                user=user,
                defaults={'role': 'customer'},
            )
        return user


class BusinessRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    business_name = forms.CharField(max_length=200)
    business_email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30)
    city = forms.CharField(max_length=120)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    tagline = forms.CharField(max_length=220, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'business_name', 'business_email', 'phone', 'city', 'address', 'tagline']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserRole.objects.update_or_create(
                user=user,
                defaults={'role': 'business_owner'},
            )
            BusinessProfile.objects.update_or_create(
                owner=user,
                defaults={
                    'name': self.cleaned_data['business_name'],
                    'email': self.cleaned_data['business_email'],
                    'phone': self.cleaned_data['phone'],
                    'city': self.cleaned_data['city'],
                    'address': self.cleaned_data['address'],
                    'tagline': self.cleaned_data['tagline'],
                    'status': 'pending',
                },
            )
        return user
