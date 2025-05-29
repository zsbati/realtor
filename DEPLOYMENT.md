# Railway Deployment Guide

## Prerequisites

1. Railway account (sign up at https://railway.app)
2. Git installed on your system
3. Python 3.10 or higher

## Deployment Steps

1. Sign up for Railway at https://railway.app
2. Click "Create New Project"
3. Choose "Import from GitHub"
4. Select your repository
5. Wait for Railway to analyze your project
6. Click "Deploy"

## Environment Variables

After deployment, you'll need to set these environment variables in Railway:

1. Go to your project dashboard
2. Click on "Environment Variables"
3. Add these variables:
   - `DJANGO_SETTINGS_MODULE=realtor.settings_production`
   - `SECRET_KEY` (generate a new one)
   - `EMAIL_HOST_USER` (if using email)
   - `EMAIL_HOST_PASSWORD` (if using email)

## Database

1. Railway will automatically provision a PostgreSQL database
2. The database URL will be available as `DATABASE_URL` environment variable
3. Update your settings to use this database URL

## Static Files

1. Railway will automatically handle static files
2. Make sure your `STATIC_URL` and `STATIC_ROOT` are properly configured
3. Run `python manage.py collectstatic` during deployment

## Accessing Your Application

Once deployed, Railway will provide you with a URL to access your application.

## Troubleshooting

1. Check the logs in Railway dashboard if you encounter any issues
2. Make sure all required Python packages are listed in `requirements.txt`
3. Verify that your environment variables are correctly set

## Notes

- Railway provides a free tier that should be sufficient for demo purposes
- The deployment process is automated and should take just a few minutes
- You can scale your application up if needed in the future
