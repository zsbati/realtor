import os
import sys
import sqlite3

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor.settings')

# Import Django settings after setting DJANGO_SETTINGS_MODULE
from django.conf import settings
from scripts.manage_migrations import run_migrations

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

# Using run_migrations from manage_migrations.py

def create_superuser():
    """Create a superuser if one doesn't exist."""
    try:
        # Use the create_superuser management command
        subprocess.run([
            sys.executable, 'manage.py', 'create_superuser'],
            check=True)
        print("Superuser creation completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating superuser: {str(e)}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error details: {e.stderr.decode()}")
        else:
            print("No additional error details available")

def initialize_project():
    """Initialize the project with database, migrations, and superuser."""
    print("Starting project initialization...")
    
    # Check and create database if needed
    if not check_database_exists():
        print("Database does not exist. Creating...")
        if not create_database():
            print("Database creation failed. Exiting.")
            sys.exit(1)
    
    # Run migrations
    print("\nRunning migrations...")
    run_migrations()
    
    # Create superuser
    print("Creating superuser...")
    create_superuser()
    
    print("Project initialization completed!")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor.settings')
    initialize_project()
