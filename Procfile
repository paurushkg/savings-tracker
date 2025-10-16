web: gunicorn savings_tracker.wsgi:application
release: python manage.py migrate && python manage.py setup_db
