import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Restore the database from a SQL file'

    def add_arguments(self, parser):
        parser.add_argument('sql_file', type=str, help='The SQL file to restore the database from')

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']
        sql_file = options['sql_file']

        command = [
            'psql',
            '-U', db_user,
            '-h', db_host,
            '-p', str(db_port),
            '-d', db_name,
            '-f', sql_file
        ]

        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        subprocess.run(command, env=env)
        self.stdout.write(self.style.SUCCESS(f"Successfully restored database from {sql_file}"))
