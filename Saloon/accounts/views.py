from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from organizations.models import BusinessProfile

from .forms import BusinessRegistrationForm, RegisterForm
from .models import UserRole


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        role = UserRole.objects.filter(user=user).first()
        if role and role.role == 'business_owner':
            return reverse_lazy('organizations:onboarding')
        return reverse_lazy('users:dashboard')


def register(request):
    if request.user.is_authenticated:
        if UserRole.objects.filter(user=request.user, role='business_owner').exists():
            return redirect('organizations:onboarding')
        return redirect('users:dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Welcome! Your customer account is ready.')
        return redirect('users:dashboard')

    return render(request, 'accounts/register.html', {'form': form})


def register_business(request):
    if request.user.is_authenticated:
        if UserRole.objects.filter(user=request.user, role='business_owner').exists():
            return redirect('organizations:onboarding')
        return redirect('users:dashboard')

    form = BusinessRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your business profile has been submitted for verification.')
        return redirect('organizations:onboarding')

    return render(request, 'accounts/business_register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:home')