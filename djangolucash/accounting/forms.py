from django.forms import ModelForm
from django import forms
from django.db import models
from accounting.models import Accounts, Suppliers, Customers

class AccountsForm(ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"

class DeleteAccountsForm(ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"

class SelectAccountsForm(forms.Form):
    accounts = forms.ModelChoiceField(
        queryset=Accounts.objects.all().order_by('code'),
        label="Choose an account",
        empty_label="Select Account"
    )

class SuppliersForm(ModelForm):
    class Meta:
        model = Suppliers
        fields = "__all__"

class CustomersForm(ModelForm):
    class Meta:
        model = Customers
        fields = "__all__"

class SelectSuppliersForm(forms.Form):
    suppliers = forms.ModelChoiceField(
        queryset=Suppliers.objects.all().order_by('code'),
        label="Choose a supplier",
        empty_label="Select a supplier"
    )

class SelectCustomersForm(forms.Form):
    suppliers = forms.ModelChoiceField(
        queryset=Customers.objects.all().order_by('code'),
        label="Choose a customer",
        empty_label="Select a customer"
    )





