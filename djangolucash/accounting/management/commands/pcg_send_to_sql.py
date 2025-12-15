from django.core.management.base import BaseCommand

from accounting.models import Accounts
from django.conf import settings
from pathlib import Path
import pandas as pd
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = pd.read_csv(Path(settings.BASE_DIR)/ "accounting" / "data" / "pcg" / "worked_pcg.csv",)

        pcg_accounts = []
        for index, row in data.iterrows():
            acc = Accounts(
                code = str(row['number']).strip(),
                name = str(row['name']).strip()
            ) 
            acc.field_calculations()
            pcg_accounts.append(acc)

        Accounts.objects.bulk_create(pcg_accounts)