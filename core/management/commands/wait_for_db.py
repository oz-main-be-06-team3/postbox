# core/management/commands/wait_for_db.py

import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    help = "Django command to wait for the database to be available"

    def handle(self, *args, **options):
        max_retries = 10
        for i in range(max_retries):
            self.stdout.write(f"Try {i + 1}/{max_retries}: Waiting for database...")
            try:
                connection = connections["default"]
                # Test the connection by getting the cursor
                connection.cursor()
                self.stdout.write(self.style.SUCCESS("PostgreSQL Database available!"))
                return
            except (Psycopg2OpError, OperationalError) as e:
                self.stdout.write(self.style.WARNING(f"Database not available: {str(e)}"))
                if i == max_retries - 1:
                    self.stdout.write(self.style.ERROR("PostgreSQL Connection Failed after maximum retries."))
                    return
                self.stdout.write("Retrying in 1 second...")
                time.sleep(1)
