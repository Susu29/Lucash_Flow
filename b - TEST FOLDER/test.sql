-- ONE FUNCTION, MULTIPLE TRIGGERS

CREATE OR REPLACE FUNCTION update_global_accounts()
    RETURNS TRIGGER AS $$
DECLARE
field_to_modify text;
sql_query text;
BEGIN

IF TG_TABLE_NAME = 'accounting_accounts' THEN
    field_to_modify := 'account_id';
ELSIF TG_TABLE_NAME = 'accounting_customers' THEN
    field_to_modify := 'customer_id';
ELSIF TG_TABLE_NAME = 'accounting_suppliers' THEN
    field_to_modify := 'supplier_id';
END IF;

IF TG_OP IN ('INSERT', 'UPDATE') THEN
    sql_query := format('INSERT INTO accounting_accountslink (%I) VALUES ($1) ON CONFLICT DO NOTHING', field_to_modify);
    EXECUTE sql_query USING NEW.id;
ELSIF TG_OP = 'DELETE' THEN
    sql_query := format('DELETE FROM accounting_accountslink WHERE (%I) = ($1)', field_to_modify);
    EXECUTE sql_query USING OLD.id;
END IF;

RETURN NULL;

END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS accounts_update_trigger   ON accounting_accounts;
DROP TRIGGER IF EXISTS customers_update_trigger  ON accounting_customers;
DROP TRIGGER IF EXISTS suppliers_update_trigger  ON accounting_suppliers;

CREATE TRIGGER accounts_update_trigger
AFTER INSERT OR UPDATE OR DELETE 
ON accounting_accounts
FOR EACH ROW
EXECUTE FUNCTION update_global_accounts()
;

CREATE TRIGGER customers_update_trigger
AFTER INSERT OR UPDATE OR DELETE 
ON accounting_customers
FOR EACH ROW
EXECUTE FUNCTION update_global_accounts()
;

CREATE TRIGGER suppliers_update_trigger
AFTER INSERT OR UPDATE OR DELETE 
ON accounting_suppliers
FOR EACH ROW
EXECUTE FUNCTION update_global_accounts()
;
