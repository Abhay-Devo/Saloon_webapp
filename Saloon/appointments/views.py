from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from organizations.models import BusinessProfile, Service

from .models import Appointment
from .utils import get_available_slots


@login_required
def booking(request):
    approved_businesses = BusinessProfile.objects.filter(status='approved').order_by('-created_at')
    selected_business = approved_businesses.first()
    selected_business_id = request.GET.get('business') or (selected_business.id if selected_business else None)
    if selected_business_id:
        selected_business = approved_businesses.filter(pk=selected_business_id).first() or selected_business

    services = Service.objects.filter(business=selected_business) if selected_business else []
    selected_service = services.first() if services else None
    selected_service_id = request.GET.get('service')
    if selected_service_id:
        selected_service = Service.objects.filter(pk=selected_service_id, business=selected_business).first() or selected_service

    today = date.today()
    selected_date = request.GET.get('date') or str(today)

    try:
        selected_date_obj = date.fromisoformat(selected_date)
        if selected_date_obj < today:
            selected_date = str(today)
    except ValueError:
        selected_date = str(today)

    if request.method == 'POST':
        service_id = request.POST.get('service')
        business_id = request.POST.get('business')
        chosen_slot = request.POST.get('slot')
        selected_business_for_booking = approved_businesses.filter(pk=business_id).first() if business_id else selected_business
        if service_id and chosen_slot and selected_business_for_booking:
            service = Service.objects.filter(pk=service_id, business=selected_business_for_booking).first()
            if service:
                try:
                    start = datetime.strptime(chosen_slot, '%Y-%m-%dT%H:%M')
                except ValueError:
                    messages.error(request, 'That time slot is invalid. Please choose a valid slot.')
                    return redirect('appointments:booking')

                start = timezone.make_aware(start, timezone.get_current_timezone())
                if start < timezone.now():
                    messages.error(request, 'You cannot book an appointment in the past.')
                    return redirect('appointments:booking')

                end = start + timedelta(minutes=service.duration_minutes)
                staff = service.business.team_members.first()
                if not staff:
                    staff = service.business.team_members.create(
                        name='Ariana',
                        role='Senior Stylist',
                        specialty='Cuts & Styling',
                        bio='Available for booking today.',
                    )
                Appointment.objects.create(
                    business=service.business,
                    customer=request.user,
                    service=service,
                    staff=staff,
                    start_time=start,
                    end_time=end,
                    status='pending',
                )
                messages.success(request, 'Your appointment request has been created.')
                return redirect('users:dashboard')

    slots = []
    if selected_business and selected_service:
        slots = get_available_slots(selected_business, selected_service, date.fromisoformat(selected_date))

    return render(
        request,
        'appointments/booking.html',
        {
            'businesses': approved_businesses,
            'business': selected_business,
            'services': services,
            'selected_service': selected_service,
            'selected_date': selected_date,
            'slots': slots,
            'today': today.isoformat(),
        },
    )


@login_required
def slot_picker(request):
    approved_businesses = BusinessProfile.objects.filter(status='approved').order_by('-created_at')
    business_id = request.GET.get('business')
    business = approved_businesses.filter(pk=business_id).first() if business_id else approved_businesses.first()
    service_id = request.GET.get('service')
    selected_service = Service.objects.filter(pk=service_id, business=business).first() if service_id and business else None
    today = date.today()
    selected_date = request.GET.get('date') or str(today)

    try:
        selected_date_obj = date.fromisoformat(selected_date)
        if selected_date_obj < today:
            selected_date = str(today)
    except ValueError:
        selected_date = str(today)

    slots = []
    if business and selected_service:
        slots = get_available_slots(business, selected_service, date.fromisoformat(selected_date))

    return render(
        request,
        'appointments/partials/slots.html',
        {
            'business': business,
            'service': selected_service,
            'slots': slots,
            'selected_date': selected_date,
        },
    )
