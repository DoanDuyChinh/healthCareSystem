from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the database by dropping all tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_true',
            help='Do not prompt the user for input of any kind.',
        )

    def handle(self, *args, **options):
        if options['noinput']:
            self._drop_tables()
        else:
            confirm = input("Are you sure you want to drop all tables? (y/N): ")
            if confirm.lower() == 'y':
                self._drop_tables()
            else:
                self.stdout.write(self.style.ERROR('Database reset cancelled.'))

    def _drop_tables(self):
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
            cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
            cursor.execute("GRANT ALL ON SCHEMA public TO public;")
        
        self.stdout.write(self.style.SUCCESS('All tables have been dropped successfully.'))
