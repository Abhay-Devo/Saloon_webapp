from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import UserRole
from appointments.models import Appointment
from organizations.models import BusinessProfile

from .forms import CustomerProfileForm
from .models import CustomerProfile


@login_required
def dashboard(request):
    user_role = UserRole.objects.filter(user=request.user).first()
    profile = CustomerProfile.objects.filter(user=request.user).first()
    business = BusinessProfile.objects.filter(status='approved').order_by('-created_at').first()
    upcoming = Appointment.objects.filter(customer=request.user).order_by('start_time')[:5]

    return render(
        request,
        'users/dashboard.html',
        {
            'user_role': user_role,
            'profile': profile,
            'business': business,
            'upcoming': upcoming,
        },
    )


@login_required
def profile(request):
    profile = CustomerProfile.objects.filter(user=request.user).first()
    form = CustomerProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        saved = form.save(commit=False)
        saved.user = request.user
        saved.save()
        messages.success(request, 'Your profile has been updated.')
        return redirect('users:dashboard')

    return render(request, 'users/profile.html', {'form': form, 'profile': profile})
