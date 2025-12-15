from django.conf import settings
from pathlib import Path
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(f'Path : {Path(settings.BASE_DIR) / "accounting" / "data" / "pcg"}')