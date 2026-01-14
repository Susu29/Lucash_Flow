from django.forms import ModelForm
from django import forms
from django.db import models
from accounting.models import Accounts, Suppliers, Customers, TransactionHeader, TransactionLine
from django.db.models.functions import Cast
from django.db.models import CharField
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.forms import TextInput


class AccountsForm(ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"


class SelectAccountsForm(forms.Form):
    accounts = forms.ModelChoiceField(
    queryset= Accounts.objects.order_by(Cast("code", CharField()).asc()),
    label="Choose an account",
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
    )

class SelectCustomersForm(forms.Form):
    Customers = forms.ModelChoiceField(
        queryset=Customers.objects.all().order_by('code'),
        label="Choose a customer",
    )

class TransactionsHeaderForm(ModelForm):
    class Meta:
        model = TransactionHeader
        fields = "__all__"
        help_texts = {
            "date" : "Format - DD/MM/YYYY"
        }

class TransactionBaseInLineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        debit = Decimal(0.00)
        credit = Decimal(0.00)
        
        for form in self.forms:
            if not form.cleaned_data:
                continue
            if self.can_delete and form.cleaned_data.get("DELETE"):
                continue
            if form.cleaned_data.get("amount") is None or form.cleaned_data.get("debit_credit") is None or form.cleaned_data.get("account") is None:
                form.add_error(None, "All fields of the line must be filled. Did you forget the amount, D/C or account ?")
                raise ValidationError("Amount must be superior to 0")
            if form.cleaned_data.get("amount") <= 0:
                form.add_error(None, "Amount must be greater than 0")
                raise ValidationError("Amount must be superior to 0")
            if form.cleaned_data.get("debit_credit") == "D":
                debit += form.cleaned_data.get("amount")
            elif form.cleaned_data["debit_credit"] == "C":
                credit += form.cleaned_data.get("amount")
        if debit != credit:
            form.add_error(None, "Debit must be equal to Credit")
            raise ValidationError("Debit must be equal to Credit")
            



TransactionsLinesFormSet = inlineformset_factory(
    TransactionHeader ,
    TransactionLine, 
    fields=["debit_credit", "account", "amount"],
    min_num=2,
    extra=5,
    can_delete=True,
    formset=TransactionBaseInLineFormSet)

class SelectTransactionsForm(forms.Form):
    transactions = forms.ModelChoiceField(
    queryset= TransactionHeader.objects.all(),
    label="Select a transaction",
    )
