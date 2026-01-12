UPDATE accounting_accountslink
JOIN accounting_accounts ON accounting_accountslink.account_id = accounting_accounts.id
SET sorting_account = accounting_accounts.code
WHERE account_id = NOT NULL;
