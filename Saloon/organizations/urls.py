from django.urls import path

from .views import onboarding

app_name = 'organizations'

urlpatterns = [
    path('', onboarding, name='onboarding'),
]
