from datetime import datetime, timedelta

from django.utils import timezone

from .models import Appointment


def get_available_slots(business, service, selected_date):
    if not business or not service or not selected_date:
        return []

    today = timezone.localdate()
    if selected_date < today:
        return []

    start = timezone.make_aware(datetime.combine(selected_date, business.opening_time), timezone.get_current_timezone())
    finish = timezone.make_aware(datetime.combine(selected_date, business.closing_time), timezone.get_current_timezone())
    duration = timedelta(minutes=service.duration_minutes)

    if selected_date == today:
        now = timezone.now()
        rounded_now = now.replace(second=0, microsecond=0)
        minute = rounded_now.minute
        remainder = minute % 15
        if remainder:
            rounded_now += timedelta(minutes=15 - remainder)
        if current := start:
            if rounded_now > start:
                start = rounded_now

    slots = []
    current = start
    while current + duration <= finish:
        end_time = current + duration
        overlap = Appointment.objects.filter(
            business=business,
            status__in=['pending', 'confirmed'],
            start_time__lt=end_time,
            end_time__gt=current,
        ).exists()
        if current >= timezone.now() and not overlap:
            slots.append(current)
        current += timedelta(minutes=15)
    return slots
