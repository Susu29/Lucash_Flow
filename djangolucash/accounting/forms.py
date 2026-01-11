from django.forms import ModelForm
from django import forms
from django.db import models
from accounting.models import Accounts, Suppliers, Customers, TransactionHeader, TransactionLine
from django.db.models.functions import Cast
from django.db.models import CharField
from django.forms import inlineformset_factory

class AccountsForm(ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"


class SelectAccountsForm(forms.Form):
    accounts = forms.ModelChoiceField(
    queryset= Accounts.objects.order_by(Cast("code", CharField()).asc()),
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
    Suppliers = forms.ModelChoiceField(
        queryset=Suppliers.objects.all().order_by('code'),
        label="Choose a supplier",
        empty_label="Select a supplier"
    )

class SelectCustomersForm(forms.Form):
    Customers = forms.ModelChoiceField(
        queryset=Customers.objects.all().order_by('code'),
        label="Choose a customer",
        empty_label="Select a customer"
    )

class TransactionsHeaderForm(ModelForm):
    class Meta:
        model = TransactionHeader
        fields = "__all__"

TransactionsLinesFormSet = inlineformset_factory(TransactionHeader ,TransactionLine, fields=["debit_credit", "account", "amount"])

