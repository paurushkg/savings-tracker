# WSGI config for PythonAnywhere deployment
import os
import sys

# Add your project directory to the sys.path
# Replace 'yourusername' with your actual PythonAnywhere username
path = '/home/yourusername/savings-tracker'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'savings_tracker.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()