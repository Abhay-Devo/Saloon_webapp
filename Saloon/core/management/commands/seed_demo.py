from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserRole
from appointments.models import Appointment
from organizations.models import BusinessProfile, Service, TeamMember
from users.models import CustomerProfile


class Command(BaseCommand):
    help = 'Create demo data for the saloon booking prototype.'

    def handle(self, *args, **options):
        owner_user, _ = User.objects.get_or_create(username='owner_demo', defaults={'email': 'owner@example.com', 'is_staff': True})
        owner_user.set_password('demo1234')
        owner_user.save()
        UserRole.objects.update_or_create(user=owner_user, defaults={'role': 'business_owner'})

        customer_user, _ = User.objects.get_or_create(username='client_demo', defaults={'email': 'client@example.com'})
        customer_user.set_password('demo1234')
        customer_user.save()
        UserRole.objects.update_or_create(user=customer_user, defaults={'role': 'customer'})

        business, created = BusinessProfile.objects.get_or_create(
            owner=owner_user,
            defaults={
                'name': 'Velvet & Blade Studio',
                'tagline': 'Precision grooming for busy lifestyles.',
                'address': '21 Heavens Lane, Downtown',
                'city': 'Mumbai',
                'phone': '+91 98765 43210',
                'email': 'hello@velvetandblade.com',
                'opening_time': '09:00:00',
                'closing_time': '20:00:00',
                'status': 'approved',
            },
        )
        if not business.status:
            business.status = 'approved'
            business.save(update_fields=['status'])

        if not business.services.exists():
            haircut = Service.objects.create(
                business=business,
                name='Signature Haircut',
                duration_minutes=30,
                price=699,
                description='Precision cut + wash + style finish.',
            )
            beard = Service.objects.create(
                business=business,
                name='Beard Sculpt',
                duration_minutes=20,
                price=449,
                description='Shape, trim and oil treatment.',
            )
            grooming = Service.objects.create(
                business=business,
                name='Full Grooming Set',
                duration_minutes=60,
                price=1199,
                description='Haircut, beard and skin finish in one pass.',
            )
        else:
            haircut = business.services.first()
            beard = business.services.order_by('price').last()
            grooming = business.services.order_by('-price').first()

        if not business.team_members.exists():
            stylist = TeamMember.objects.create(
                business=business,
                name='Ariana',
                role='Senior Stylist',
                specialty='Cuts & Styling',
                bio='Known for soft fades and polished finishes.',
            )
            barber = TeamMember.objects.create(
                business=business,
                name='Daniel',
                role='Beard Expert',
                specialty='Beard shaping',
                bio='Grooming specialist for clean, precise lines.',
            )
        else:
            stylist = business.team_members.first()
            barber = business.team_members.last()

        CustomerProfile.objects.update_or_create(
            user=customer_user,
            defaults={
                'full_name': 'Riya Sharma',
                'phone': '+91 98233 22211',
                'gender': 'female',
                'preferred_services': 'Haircut, Beard Sculpt',
            },
        )

        today = date.today()
        start = timezone.make_aware(datetime.combine(today + timedelta(days=1), datetime.strptime('10:00', '%H:%M').time()), timezone.get_current_timezone())
        end = start + timedelta(minutes=haircut.duration_minutes)
        Appointment.objects.update_or_create(
            business=business,
            customer=customer_user,
            service=haircut,
            staff=stylist,
            start_time=start,
            defaults={'end_time': end, 'status': 'confirmed'},
        )

        tomorrow = timezone.make_aware(datetime.combine(today + timedelta(days=2), datetime.strptime('14:00', '%H:%M').time()), timezone.get_current_timezone())
        end_tomorrow = tomorrow + timedelta(minutes=beard.duration_minutes)
        Appointment.objects.update_or_create(
            business=business,
            customer=customer_user,
            service=beard,
            staff=barber,
            start_time=tomorrow,
            defaults={'end_time': end_tomorrow, 'status': 'pending'},
        )

        self.stdout.write(self.style.SUCCESS('Demo data created successfully.'))
