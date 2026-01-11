from .models import Accounts, Suppliers, Customers
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, FormView
from .forms import AccountsForm, SelectAccountsForm, SelectSuppliersForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
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
    template_name = "accounting/delete_accounts.html"
    #success_url = reverse_lazy('accounting:accounts')
    success_message = ('Account deleted successfully.')

    def get_success_url(self):
        print(self.model)
        if self.model.__name__ == "Customers":
            return reverse('accounting:customers')
        elif self.model.__name__ == "Suppliers":
            return reverse('accounting:suppliers')

class ThirdPartyView(ListView):
    template_name = "accounting/thirdparty.html"
    context_object_name = "thirdparty"
    party_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["party_type"] = self.party_type
        return context
    
class AddThirdPartyView(SuccessMessageMixin, CreateView):
    template_name = "accounting/add_thirdparty.html"
    success_message = ('Third party created successfully.')
    party_type = None        

    def get_success_url(self):
        if self.party_type == "Customers":
            return reverse('accounting:customers')
        elif self.party_type == "Suppliers":
            return reverse('accounting:suppliers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["party_type"] = self.party_type
        return context
    #Model Passed by URL

class SelectThirdPartyView(FormView):
    template_name = "accounting/select_accounts.html"
    party_type = None
    delete_url_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["party_type"] = self.party_type
        return context

    def form_valid(self, form):
        selected = form.cleaned_data[self.party_type]
        if self.party_type == "Suppliers":
            return redirect("accounting:delete_suppliers", pk=selected.id)
        elif self.party_type == "Customers":
            return redirect("accounting:delete_customers", pk=selected.id)


