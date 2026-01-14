import pandas as pd
from pathlib import Path
from django.conf import settings
from codes import codes

#Could have been less automatisation & that's obviously wayyy to much for a one-time import but i wanted a pandas refresher
#Turns out it is usefull as i need a second import to cover a wider range of account
#Actually very usefull has chatgpt isn't respecting the instructions



### !!! MAP THE APPROPRIATE CSV HERE !!! ###
df = pd.read_csv("accounting/data/transactions/transactions2.csv")

# Test to make :
#Test 1 - At least 1D, 1C for every transaction
#Test 2 - Debit = Credit, for every transaction. (If every transaction works then global too)
#Test 3 - Date = Inside 2025
#Test 4 - Accounts = All accounts are inside the DB
print("--- START OF THE TEST ---")

#Test 1 & 2
#Getting all ID of unique_transactions
equal_transaction_status = True
debit_credit_presence_status = True
unique_transaction = (df["transaction_number"].unique())

for i in unique_transaction:
    df_filtered = df[df["transaction_number"] == i]
    debit_value = round((df_filtered.loc[df_filtered["debit_credit"] == "D", "amount"].sum()),2)
    credit_value = round((df_filtered.loc[df_filtered["debit_credit"] == "C", "amount"].sum()),2)

    if debit_value <= 0:
        debit_credit_presence_status = False
        print(f'Debit of operation {i} is absent or negative.')

    if credit_value <= 0:
        debit_credit_presence_status = False
        print(f'Credit of operation {i} is absent or negative.')

    if debit_value != credit_value:
        print(f'Debit & Credit of operation {i} are not equal')
        equal_transaction_status = False

if equal_transaction_status == True:
    print("All the debits & credits are equal")
if debit_credit_presence_status == True:
    print("Each transaction contains debits & credits")
    #PRINT THE AMOUNT OF DEBIT
    #PRINT THE AMOUNT OF CREDIT



#Test 3

print(f'Range of transactions : {min(df["date"])} - {max(df["date"])}')

#Test 4

valid_accounts = True
for i in df["account"]:
    if i not in codes:
        valid_accounts = False
        print(f'Account {i} not in the code set')
    
if valid_accounts == True:
    print("All accounts are valid")

print("--- END OF THE TEST ---")