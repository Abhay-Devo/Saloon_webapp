from django.urls import path

from .views import CustomLoginView, logout_view, register, register_business

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('business-register/', register_business, name='business_register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
