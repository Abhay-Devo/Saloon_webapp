from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BusinessProfileForm
from .models import BusinessProfile


@login_required
def onboarding(request):
    existing = BusinessProfile.objects.filter(owner=request.user).first()
    form = BusinessProfileForm(request.POST or None, instance=existing)

    if request.method == 'POST' and form.is_valid():
        business = form.save(commit=False)
        business.owner = request.user
        business.save()
        messages.success(request, 'Your business profile is ready.')
        return redirect('appointments:booking')

    return render(request, 'organizations/onboarding.html', {'form': form, 'business': existing})
