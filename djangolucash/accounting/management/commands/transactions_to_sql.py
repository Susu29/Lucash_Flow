from django.core.management.base import BaseCommand

from accounting.models import TransactionHeader, TransactionLine, AccountsLink
from django.conf import settings
from pathlib import Path
import pandas as pd
from django.db import transaction

### WARNING - WHILE THE LINES & HEADERS ARE VERIFIED INDIVIDUALLY, THERE IS NO VERIFICATION OF THE FORMSET.
### THE ACCOUNTING LOGIC MUST BE OK AND VERIFIED WITH SUPPLIERS_TO_SQL
class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        ### !!! MODIFY THE PATH TO AVOID DUPLICATES !!! ### 
        data = pd.read_csv(Path(settings.BASE_DIR)/ "accounting" / "data" / "transactions" / "transactions2.csv", parse_dates=['date'])


        lines = []
        submitted_headers = {}
        with transaction.atomic():
            for index, row in data.iterrows():

                transaction_number = str(row["transaction_number"]).strip()
                print(transaction_number) ### ONLY USEFULL FOR DEBUG
                if transaction_number not in submitted_headers:

                    header = TransactionHeader(
                        date = row['date'],
                        invoice = str(row['invoice']).strip(),
                        name = str(row['name']).strip(),
                    ) 
                    header.full_clean()
                    header.save()
                    submitted_headers[transaction_number] = header       
                header = submitted_headers[transaction_number]

                csv_account = str(row['account']).strip()
                account = AccountsLink.objects.get(sorting_account=csv_account)

                line = TransactionLine(
                    header = header,
                    debit_credit = str(row['debit_credit']).strip(),
                    account = account,
                    amount = str(row['amount']).strip(),
                )
                line.full_clean()
                lines.append(line)
            TransactionLine.objects.bulk_create(lines)

                
                

    #command = python3 manage.py transactions_to_sql
