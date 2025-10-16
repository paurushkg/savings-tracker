from django.core.management.base import BaseCommand
from django.db import connection
from tracker.models import SavingsBox


class Command(BaseCommand):
    help = 'Setup database and initialize data'

    def handle(self, *args, **options):
        # Check if tables exist
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'tracker_savingsbox'
                );
            """)
            table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            self.stdout.write(self.style.ERROR('Database tables do not exist. Run migrations first.'))
            return
        
        # Initialize boxes if none exist
        if not SavingsBox.objects.exists():
            self.stdout.write('Initializing savings boxes...')
            SavingsBox.initialize_boxes()
            count = SavingsBox.objects.count()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {count} savings boxes')
            )
        else:
            count = SavingsBox.objects.count()
            self.stdout.write(f'Database already has {count} savings boxes')