"""
WSGI configuration for PythonAnywhere deployment.
"""

import os
import sys

# Add the project root directory to the Python path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'realtor.settings_prod'

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()