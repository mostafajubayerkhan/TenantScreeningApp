from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a test tenant with a high trust score'

    def handle(self, *args, **kwargs):
        username = 'supertenant'
        password = 'password123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(username=username, email='tenant@example.com', password=password, role='tenant')
            self.stdout.write(self.style.SUCCESS(f'User {username} created'))

        # Boost Trust Score
        user.first_name = "Alex"
        user.last_name = "Tenant"
        user.phone_number = "555-0199"
        user.is_identity_verified = True
        user.has_employment_history = True
        user.has_rental_history = True
        user.background_check_clear = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Trust Score boosted for {username}'))
        self.stdout.write(self.style.SUCCESS(f'Login with: {username} / {password}'))
