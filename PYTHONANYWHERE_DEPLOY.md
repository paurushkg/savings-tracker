# PythonAnywhere Deployment Guide

## Prerequisites
- PythonAnywhere account (free or paid)
- This Django project ready for deployment

## Step 1: Upload Project to PythonAnywhere

### Option A: Using Git (Recommended)
1. Open a Bash console on PythonAnywhere
2. Clone your repository:
   ```bash
   git clone https://github.com/paurushkg/savings-tracker.git
   cd savings-tracker
   ```

### Option B: Upload Files
1. Use the Files tab in PythonAnywhere dashboard
2. Upload your project files to `/home/yourusername/savings-tracker/`

## Step 2: Set Up Virtual Environment

1. In the Bash console:
   ```bash
   cd ~/savings-tracker
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Step 3: Configure Database

1. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

3. Initialize savings boxes:
   ```bash
   python manage.py shell
   >>> from tracker.models import SavingsBox
   >>> SavingsBox.initialize_boxes()
   >>> exit()
   ```

## Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 5: Configure Web App

1. Go to PythonAnywhere Dashboard → Web
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Set these configurations:

### Source code:
```
/home/yourusername/savings-tracker
```

### Working directory:
```
/home/yourusername/savings-tracker
```

### WSGI configuration file:
Replace the content with the `pythonanywhere_wsgi.py` file, but update the path:
```python
import os
import sys

# Replace 'yourusername' with your actual username
path = '/home/yourusername/savings-tracker'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'savings_tracker.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Virtual environment:
```
/home/yourusername/savings-tracker/venv
```

### Static files:
- URL: `/static/`
- Directory: `/home/yourusername/savings-tracker/staticfiles/`

## Step 6: Final Steps

1. Click "Reload" on your web app
2. Visit your app URL: `https://yourusername.pythonanywhere.com`
3. Test the passcode: **bachat**

## Important Notes

- **Database**: Uses SQLite3 (automatically handled)
- **Passcode**: "bachat" (hardcoded in middleware)
- **Static Files**: Served by PythonAnywhere automatically
- **Logs**: Check error logs in the Web tab if issues occur

## Troubleshooting

### If you get import errors:
- Check that all requirements are installed in the virtual environment
- Verify the WSGI file paths are correct

### If static files don't load:
- Run `python manage.py collectstatic` again
- Check static files configuration in Web app settings

### If database errors occur:
- Run migrations again: `python manage.py migrate`
- Initialize boxes: `python manage.py shell` → `SavingsBox.initialize_boxes()`

## Updating Your App

To update your deployed app:
```bash
cd ~/savings-tracker
git pull origin main  # if using git
source venv/bin/activate
pip install -r requirements.txt  # if requirements changed
python manage.py migrate  # if models changed
python manage.py collectstatic --noinput  # if static files changed
```

Then click "Reload" in the Web tab.