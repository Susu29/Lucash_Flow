from django.forms import ModelForm
from django import forms
from django.db import models
from accounting.models import Accounts

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






