# Deployment Guide

This guide covers how to deploy the Savings Tracker Django application to various platforms.

## Prerequisites

- Python 3.11+
- Git repository
- Environment variables configured

## Deployment Options

### 1. Heroku Deployment

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create your-savings-tracker-app
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY="your-secure-secret-key"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   ```

4. **Add PostgreSQL database**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy**:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push heroku main
   ```

6. **Run migrations**:
   ```bash
   heroku run python manage.py migrate
   ```

### 2. Railway Deployment

1. **Connect your GitHub repository** to Railway
2. **Set environment variables**:
   - `SECRET_KEY`: Your secure secret key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app.railway.app
   - `DATABASE_URL`: (automatically provided by Railway PostgreSQL)

3. **Add PostgreSQL database** from Railway dashboard

4. **Deploy** automatically triggers on git push

### 3. Render Deployment

1. **Create a new Web Service** on Render
2. **Connect your repository**
3. **Set environment variables**:
   - `SECRET_KEY`: Your secure secret key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app.onrender.com

4. **Add PostgreSQL database** from Render dashboard

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@localhost:5432/database_name
```

## Local Testing with Production Settings

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export DEBUG=False
   export SECRET_KEY="your-secret-key"
   export ALLOWED_HOSTS="127.0.0.1,localhost"
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Test with Gunicorn**:
   ```bash
   gunicorn savings_tracker.wsgi:application
   ```

## Post-Deployment

1. **Initialize savings boxes** (first time only):
   - Visit your deployed app
   - The app will automatically initialize boxes on first load

2. **Create admin user** (optional):
   ```bash
   python manage.py createsuperuser
   ```

## Troubleshooting

- **Static files not loading**: Ensure `STATIC_ROOT` is set and `collectstatic` was run
- **Database connection errors**: Verify `DATABASE_URL` environment variable
- **500 errors**: Check application logs and ensure `DEBUG=False` with proper error logging
- **CSRF errors**: Verify `ALLOWED_HOSTS` includes your domain

## Security Checklist

- ✅ SECRET_KEY set via environment variable
- ✅ DEBUG=False in production
- ✅ ALLOWED_HOSTS configured
- ✅ HTTPS enforced (platform-dependent)
- ✅ Static files served via WhiteNoise
- ✅ Database URL configured via environment variable