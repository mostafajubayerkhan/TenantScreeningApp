from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a test landlord'

    def handle(self, *args, **kwargs):
        username = 'landlord_tester'
        password = 'password123'
        
        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
            u.role = 'landlord'
            u.set_password(password)
            u.save()
            self.stdout.write(self.style.SUCCESS(f'Updated {username}'))
        else:
            User.objects.create_user(username=username, email='ll@example.com', password=password, role='landlord')
            self.stdout.write(self.style.SUCCESS(f'Created {username}'))
