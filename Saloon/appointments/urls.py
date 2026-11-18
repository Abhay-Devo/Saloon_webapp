from django.urls import path

from .views import booking, slot_picker

app_name = 'appointments'

urlpatterns = [
    path('', booking, name='booking'),
    path('slots/', slot_picker, name='slots'),
]
