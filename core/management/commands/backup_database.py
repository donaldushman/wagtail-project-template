import os
import subprocess
import tempfile
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core.storage import S3BackupStorage


class Command(BaseCommand):
    help = "Back up the PostgreSQL database to private S3 storage."

    def handle(self, *args, **options):
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise CommandError("DATABASE_URL is required.")

        retention_days = settings.DATABASE_BACKUP_RETENTION
        if retention_days < 1:
            raise CommandError("DATABASE_BACKUP_RETENTION must be at least 1 day.")

        timestamp = timezone.now().strftime("%Y%m%d-%H%M%S")
        filename = f"database-{timestamp}.dump"
        storage = S3BackupStorage()

        with tempfile.TemporaryDirectory() as temp_dir:
            backup_path = Path(temp_dir) / filename

            try:
                subprocess.run(
                    [
                        "pg_dump",
                        "--format=custom",
                        "--no-owner",
                        "--no-acl",
                        "--file",
                        str(backup_path),
                        database_url,
                    ],
                    check=True,
                )
            except FileNotFoundError as exc:
                raise CommandError("pg_dump is not installed or is not on PATH.") from exc
            except subprocess.CalledProcessError as exc:
                raise CommandError(f"pg_dump failed with exit code {exc.returncode}.") from exc

            with backup_path.open("rb") as backup_file:
                saved_name = storage.save(filename, backup_file)

        self.stdout.write(self.style.SUCCESS(f"Uploaded database backup: {saved_name}"))

        cutoff = timezone.now() - timedelta(days=retention_days)
        deleted = 0

        try:
            _, names = storage.listdir("")
        except Exception as exc:
            raise CommandError(f"Backup uploaded, but retention cleanup failed: {exc}") from exc

        for name in names:
            if not name.startswith("database-") or not name.endswith(".dump"):
                continue

            try:
                modified = storage.get_modified_time(name)
                if modified < cutoff:
                    storage.delete(name)
                    deleted += 1
            except Exception as exc:
                raise CommandError(
                    f"Backup uploaded, but retention cleanup failed for {name}: {exc}"
                ) from exc

        self.stdout.write(f"Deleted {deleted} expired backup(s).")
