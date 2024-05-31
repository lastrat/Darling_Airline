import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Backup the database to a SQL file'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']
        backup_file = f"{db_name}_backup.sql"

        command = [
            'pg_dump',
            '-U', db_user,
            '-h', db_host,
            '-p', str(db_port),
            '-F', 'p',
            '-d', db_name,
            '-f', backup_file
        ]

        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        subprocess.run(command, env=env)
        self.stdout.write(self.style.SUCCESS(f"Successfully backed up database to {backup_file}"))
