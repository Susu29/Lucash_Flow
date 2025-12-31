from django.urls import path
from . import views
from .models import Suppliers, Customers
from .forms import SuppliersForm, CustomersForm, SelectSuppliersForm, SelectCustomersForm
app_name = "accounting"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/", views.AccountsView.as_view(), name="accounts"),
    path("accounts/add/", views.AddAccountsView.as_view(), name="add_accounts"),
    path("accounts/select_accounts/", views.SelectAccountsView.as_view(), name="select_accounts"),
    path("accounts/<int:pk>/delete_accounts/", views.DeleteAccountsView.as_view(), name="delete_accounts"),
    path("suppliers/", views.ThirdPartyView.as_view(model=Suppliers, party_type ="Suppliers"), name="suppliers"),
    path("customers/", views.ThirdPartyView.as_view(model=Customers, party_type ="Customers"), name="customers"),
    path("suppliers/add/", views.AddThirdPartyView.as_view(model=Suppliers, form_class=SuppliersForm, party_type="Suppliers"), name="add_suppliers"),
    path("customers/add/", views.AddThirdPartyView.as_view(model=Customers, form_class=CustomersForm, party_type="Customers"), name="add_customers"),
    path("accounts/select_suppliers/", views.SelectThirdPartyView.as_view(form_class = SelectSuppliersForm, party_type ="Suppliers", delete_url_name ="accounting:delete_suppliers"), name="select_suppliers"),
    path("accounts/select_customers/", views.SelectThirdPartyView.as_view(form_class = SelectCustomersForm, party_type ="Customers", delete_url_name ="accounting:delete_customers"), name="select_customers"),




]