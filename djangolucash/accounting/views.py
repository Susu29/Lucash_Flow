from .models import Accounts
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, FormView
from .forms import AccountsForm, SelectAccountsForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.shortcuts import redirect
# Create your views here.
class IndexView(TemplateView):
    template_name = "accounting/index.html"


class AccountsView(ListView):
    template_name = "accounting/accounts.html"
    model = Accounts
    context_object_name = "Accounts"

class AddAccountsView(SuccessMessageMixin, CreateView):
    model = Accounts
    form_class = AccountsForm
    template_name = "accounting/add_accounts.html"
    success_url = reverse_lazy('accounting:accounts')
    success_message = ('Account created successfully.')

class SelectAccountsView(FormView):
    template_name = "accounting/select_accounts.html"
    form_class = SelectAccountsForm

    def form_valid(self, form):
        selected = form.cleaned_data["accounts"]
        return redirect("accounting:delete_accounts", pk=selected.id)

class DeleteAccountsView(SuccessMessageMixin, DeleteView):
    model = Accounts
    template_name = "accounting/delete_accounts.html"
    success_url = reverse_lazy('accounting:accounts')
    success_message = ('Account deleted successfully.')

