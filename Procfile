web: gunicorn savings_tracker.wsgi:application
release: python manage.py collectstatic --noinput && python manage.py migrate
