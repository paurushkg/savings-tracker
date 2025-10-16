from django.apps import AppConfig
from django.core.management import execute_from_command_line
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
import sys


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'
    
    def ready(self):
        # Only run migrations in production (when using gunicorn)
        if 'runserver' not in sys.argv and 'migrate' not in sys.argv:
            try:
                # Check if table exists
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM tracker_savingsbox LIMIT 1")
            except (OperationalError, ProgrammingError):
                # Table doesn't exist, run migrations
                try:
                    from django.core.management import call_command
                    call_command('migrate', verbosity=0, interactive=False)
                    
                    # Initialize boxes
                    from .models import SavingsBox
                    if not SavingsBox.objects.exists():
                        SavingsBox.initialize_boxes()
                except Exception as e:
                    print(f"Migration failed: {e}")
