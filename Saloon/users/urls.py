from django.urls import path

from .views import dashboard, profile

app_name = 'users'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
]
