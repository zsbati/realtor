import os
import sys
import subprocess
from django.core.management import execute_from_command_line
from django.conf import settings
import sqlite3

def check_database_exists():
    """Check if SQLite database exists."""
    db_path = settings.DATABASES['default']['NAME']
    return os.path.exists(db_path)

def create_database():
    """Create SQLite database if it doesn't exist."""
    db_path = settings.DATABASES['default']['NAME']
    if not os.path.exists(db_path):
        try:
            # Create empty database file
            open(db_path, 'a').close()
            print(f"Created database file at {db_path}")
            # Initialize database with basic structure
            conn = sqlite3.connect(db_path)
            conn.close()
            print("Initialized empty database")
        except Exception as e:
            print(f"Error creating database: {str(e)}")
            return False
    return True

def run_migrations():
    """Run migrations if needed."""
    try:
        # Make migrations for all apps
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        # Apply migrations for all apps
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {str(e)}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error details: {e.stderr.decode()}")
        else:
            print("No additional error details available")

def create_superuser():
    """Create a superuser if one doesn't exist."""
    try:
        # First, create the superuser with the default password
        subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c',
            f"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\n"
            f"    username='{settings.DEFAULT_SUPERUSER['username']}',\n"
            f"    email='{settings.DEFAULT_SUPERUSER['email']}',\n"
            f"    password='{settings.DEFAULT_SUPERUSER['password']}')"
        ], check=True)
        print("Superuser created successfully!")
    except subprocess.CalledProcessError as e:
        if "already exists" in str(e):
            print("Superuser already exists.")
        else:
            print(f"Error creating superuser: {str(e)}")
            if hasattr(e, 'stderr') and e.stderr:
                print(f"Error details: {e.stderr.decode()}")

def initialize_project():
    """Initialize the project with database, migrations, and superuser."""
    print("Starting project initialization...")
    
    # Check and create database if needed
    if not check_database_exists():
        if not create_database():
            print("Failed to create database. Exiting.")
            return
    
    # Run migrations for all apps
    print("Running migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {str(e)}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error details: {e.stderr.decode()}")
        return
    
    # Create superuser
    print("Creating superuser...")
    try:
        # First, create the superuser with the default password
        subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c',
            f"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\n"
            f"    username='{settings.DEFAULT_SUPERUSER['username']}',\n"
            f"    email='{settings.DEFAULT_SUPERUSER['email']}',\n"
            f"    password='{settings.DEFAULT_SUPERUSER['password']}')"
        ], check=True)
        print("Superuser created successfully!")
    except subprocess.CalledProcessError as e:
        if "already exists" in str(e):
            print("Superuser already exists.")
        else:
            print(f"Error creating superuser: {str(e)}")
            if hasattr(e, 'stderr') and e.stderr:
                print(f"Error details: {e.stderr.decode()}")
    
    print("Project initialization completed!")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor.settings')
    initialize_project()
