from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import getpass

class Command(BaseCommand):
    help = 'Creates a superuser interactively if one does not exist'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Superuser already exists.')
            return

        self.stdout.write('Creating superuser...')
        
        while True:
            username = input('Username: ')
            if not username:
                self.stdout.write('Error: Username cannot be empty')
                continue
                
            if User.objects.filter(username=username).exists():
                self.stdout.write(f'Error: Username "{username}" already exists')
                continue
                
            break

        email = input('Email address: ')
        
        while True:
            password = getpass.getpass('Password: ')
            if not password:
                self.stdout.write('Error: Password cannot be empty')
                continue
                
            password_confirm = getpass.getpass('Password (again): ')
            if password != password_confirm:
                self.stdout.write('Error: Passwords do not match')
                continue
                
            break

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}"'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
