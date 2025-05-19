import os
import subprocess
import sys

def run_migrations():
    """Run Django migrations."""
    print("Running migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()
