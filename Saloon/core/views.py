from django.shortcuts import render

from organizations.models import BusinessProfile, Service

app_name = 'core'


def home(request):
    businesses = BusinessProfile.objects.filter(status='approved').order_by('-created_at')[:6]
    services = []
    for business in businesses:
        services.extend(list(Service.objects.filter(business=business)[:3]))

    return render(
        request,
        'core/home.html',
        {
            'businesses': businesses,
            'services': services,
            'stats': {
                'bookings': '2.4k+',
                'avg_wait': '12 mins',
                'satisfaction': '4.9/5',
            },
        },
    )