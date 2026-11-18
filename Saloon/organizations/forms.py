from django import forms

from .models import BusinessProfile


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            'name',
            'tagline',
            'address',
            'city',
            'phone',
            'email',
            'opening_time',
            'closing_time',
            'booking_buffer_minutes',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }
