#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput

# Migrate database
python manage.py migrate

# Create superuser (if needed)
# python manage.py createsuperuser

# Restart the web app
pythonanywhere restart
