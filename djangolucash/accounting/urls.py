from django.urls import path
from . import views
app_name = "accounting"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/", views.AccountsView.as_view(), name="accounts"),
    path("accounts/add/", views.AddAccountsView.as_view(), name="add_accounts"),
    path("accounts/select_accounts/", views.SelectAccountsView.as_view(), name="select_accounts"),
    path("accounts/<int:pk>/delete_accounts/", views.DeleteAccountsView.as_view(), name="delete_accounts"),

]