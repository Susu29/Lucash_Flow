from django.core.management.base import BaseCommand

from accounting.models import Customers
from django.conf import settings
from pathlib import Path
import pandas as pd
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = pd.read_csv(Path(settings.BASE_DIR)/ "accounting" / "data" / "customers" / "customers.csv")

        customers_accounts = []
        for index, row in data.iterrows():
            acc = Customers(
                code = str(row['code']).strip(),
                name = str(row['name']).strip(),
                email = str(row['email']).strip(),
                address = str(row['address']).strip(),
                phone = str(row['phone']).strip()
            ) 
            acc.field_calculations()
            customers_accounts.append(acc)

#command = python3 manage.py customers_to_sql
