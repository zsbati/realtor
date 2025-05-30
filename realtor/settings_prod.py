# Database configuration for PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'your_pythonanywhere_host',
        'PORT': '5432',
    }
}

# Static files configuration
STATIC_ROOT = '/home/zsbati/realtor/static'
STATIC_URL = '/static/'

# Security settings
DEBUG = False
SECURE_SSL_REDIRECT = False  # PythonAnywhere handles SSL
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email settings (if needed)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')