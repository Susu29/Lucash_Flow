from django.core.management.base import BaseCommand

from accounting.models import Suppliers
from django.conf import settings
from pathlib import Path
import pandas as pd
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = pd.read_csv(Path(settings.BASE_DIR)/ "accounting" / "data" / "suppliers" / "suppliers.csv", sep=";")

        suppliers_accounts = []
        for index, row in data.iterrows():
            acc = Suppliers(
                code = str(row['code']).strip(),
                name = str(row['name']).strip(),
                email = str(row['email']).strip(),
                address = str(row['address']).strip(),
                phone = str(row['phone']).strip()
            ) 
            acc.field_calculations()
            suppliers_accounts.append(acc)

        Suppliers.objects.bulk_create(suppliers_accounts)

#command = python3 manage.py suppliers_to_sql
