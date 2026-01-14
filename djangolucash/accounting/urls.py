from django.urls import path
from . import views, forms
from .models import Accounts, Suppliers, Customers, TransactionHeader
app_name = "accounting"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/", views.AccountsView.as_view(), name="accounts"),
    path("accounts/add/", views.AddAccountsView.as_view(), name="add_accounts"),
    path("accounts/<int:pk>/update_accounts/", views.UpdateAccountsView.as_view(form_class = forms.AccountsForm, model=Accounts), name="update_accounts"),
    path("accounts/<str:operation_type>/select_accounts/", views.SelectAccountsView.as_view(), name ="select_accounts"),
    path("accounts/<int:pk>/delete_accounts/", views.DeleteAccountsView.as_view(model=Accounts), name="delete_accounts"),
    path("suppliers/", views.ThirdPartyView.as_view(model=Suppliers, party_type ="Suppliers"), name="suppliers"),
    path("customers/", views.ThirdPartyView.as_view(model=Customers, party_type ="Customers"), name="customers"),
    path("suppliers/add/", views.AddThirdPartyView.as_view(model=Suppliers, form_class=forms.SuppliersForm, party_type="Suppliers"), name="add_suppliers"),
    path("customers/add/", views.AddThirdPartyView.as_view(model=Customers, form_class=forms.CustomersForm, party_type="Customers"), name="add_customers"),
    path("accounts/<str:operation_type>/select_suppliers/", views.SelectThirdPartyView.as_view(form_class = forms.SelectSuppliersForm, party_type ="Suppliers", delete_url_name ="accounting:delete_suppliers"), name="select_suppliers"),
    path("accounts/<str:operation_type>/select_customers/", views.SelectThirdPartyView.as_view(form_class = forms.SelectCustomersForm, party_type ="Customers", delete_url_name ="accounting:delete_customers"), name="select_customers"),
    path("accounts/<int:pk>/delete_suppliers/", views.DeleteAccountsView.as_view(model=Suppliers), name="delete_suppliers"),
    path("accounts/<int:pk>/delete_customers/", views.DeleteAccountsView.as_view(model=Customers), name="delete_customers"),
    path("accounts/<int:pk>/update_suppliers/", views.UpdateAccountsView.as_view(form_class = forms.SuppliersForm, model=Suppliers), name="update_suppliers"),
    path("accounts/<int:pk>/update_customers/", views.UpdateAccountsView.as_view(form_class = forms.CustomersForm, model=Customers), name="update_customers"),
    path("transactions/add", views.add_transactions, name="add_transactions"),
    path("accounts/<int:pk>/update_transactions/", views.update_transactions, name="update_transactions"),
    path("transactions/headers", views.TransactionsHeaderView.as_view(), name="transactions_headers"),
    path("transactions/ledger", views.LedgerView.as_view(), name="ledger"),
    path("transactions/<str:operation_type>/select_transactions/", views.SelectTransactionsView.as_view(), name="select_transactions"),
    path("accounts/<int:pk>/delete_transactions/", views.DeleteTransactionsView.as_view(model=TransactionHeader), name="delete_transactions"),
    path("balance/", views.BalanceView.as_view(), name="balance"),
    path("income_statement/", views.IncomeStatementView.as_view(), name="income_statement"),
    path("balance_sheet/", views.BalanceSheetView.as_view(), name="balance_sheet"),


]