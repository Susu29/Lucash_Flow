from .models import Accounts, Suppliers, Customers, TransactionHeader, TransactionLine, AccountsLink
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, FormView, UpdateView
from .forms import AccountsForm, SelectAccountsForm, TransactionsHeaderForm, TransactionsLinesFormSet, SelectTransactionsForm
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce
from decimal import Decimal
from .helpers import global_data
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib.messages import get_messages

# Cache keys
TRANSACTIONS_CACHE_KEY = "transactions:cache"
LEDGER_CACHE_KEY = "ledger:cache"


# Create your views here.
### "Other Views : Home, FAQ.."

class EmptyView(TemplateView):
    pass
    
class HomeView(TemplateView):
    template_name = "accounting/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(global_data(self.request)) 
        return context


class IndexView(TemplateView):
    template_name = "accounting/index.html"

### Accounts View Related

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
    
    ### Trying a method different than thirdparty detection to not have to map multiple URL, as it would make 4 more different URLS
    # Dispatch one extract the operation_type for the URL
    def dispatch(self, request, *args, **kwargs):
        self.operation_type = kwargs["operation_type"]
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = self.operation_type
        return context

    def form_valid(self, form):
        selected = form.cleaned_data["accounts"]
        if self.operation_type == "delete":
            return redirect("accounting:delete_accounts", pk=selected.id)
        elif self.operation_type == "update":
            return redirect("accounting:update_accounts", pk=selected.id)

class DeleteAccountsView(SuccessMessageMixin, DeleteView):
    template_name = "accounting/delete_accounts.html"
    success_message = ('Account deleted successfully.')

    def get_success_url(self):
        if self.model.__name__ == "Customers":
            return reverse('accounting:customers')
        elif self.model.__name__ == "Suppliers":
            return reverse('accounting:suppliers')
        else:
            return reverse('accounting:accounts')

class UpdateAccountsView(SuccessMessageMixin, UpdateView):
    #Model passed via URL
    #form_class also passed via URL
    template_name = "accounting/update_accounts.html"
    #success_url = reverse_lazy('accounting:accounts')
    success_message = ('Account modified successfully.')

    def get_success_url(self):
        if self.model.__name__ == "Customers":
            return reverse('accounting:customers')
        elif self.model.__name__ == "Suppliers":
            return reverse('accounting:suppliers')
        else:
            return reverse('accounting:accounts')
        
### ThirdParty View Related

class ThirdPartyView(ListView):
    #Model passed via URL
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

    def dispatch(self, request, *args, **kwargs):
        self.operation_type = kwargs["operation_type"]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = self.operation_type
        context["party_type"] = self.party_type
        return context

    #Easier to make it with variables rather than 4 return redirect (2*2)
    def form_valid(self, form):
        selected = form.cleaned_data[self.party_type]
        party_url_field = self.party_type.lower()
        operation_url_field = self.operation_type

        return redirect(f"accounting:{operation_url_field}_{party_url_field}", pk=selected.id)
    
### Transactions View Related

def add_transactions(request):
    if request.method == "POST":
        form = TransactionsHeaderForm(request.POST)
        formset = TransactionsLinesFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                header = form.save()
                formset.instance = header
                formset.save()
            cache.delete_many([LEDGER_CACHE_KEY,TRANSACTIONS_CACHE_KEY])# Deleting the cache here
            messages.success(request, "Transaction created successfully.")
            return redirect("accounting:ledger")
    else:
        form = TransactionsHeaderForm()
        formset = TransactionsLinesFormSet()

    return render(request, "accounting/add_transactions.html", {'form': form, 'formset' : formset})

class TransactionsHeaderView(ListView):
    template_name = "accounting/transactions_headers.html"
    model = TransactionHeader
    context_object_name = "transactionsheader"

    def dispatch(self, request, *args, **kwargs):
        cached_response = cache.get(TRANSACTIONS_CACHE_KEY)
        if cached_response: # Return cache if exists
            return cached_response
        response = super().dispatch(request, *args, **kwargs)
        if any(get_messages(request)): # Don't cache if there's a message 
            return response
        response.render() # Starting the caching process
        cache.set(TRANSACTIONS_CACHE_KEY, response, None)
        return response


class SelectTransactionsView(FormView): 
    template_name = "accounting/select_transactions.html"
    form_class = SelectTransactionsForm

    def dispatch(self, request, *args, **kwargs):
        self.operation_type = kwargs["operation_type"]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = self.operation_type
        return context

    def form_valid(self, form):
        selected = form.cleaned_data["transactions"]
        return redirect(f"accounting:{self.operation_type}_transactions", pk=selected.id)
    
class DeleteTransactionsView(SuccessMessageMixin, DeleteView):
    template_name = "accounting/delete_transactions.html"
    success_url = reverse_lazy('accounting:ledger')
    success_message = ('Transaction deleted successfully.')

    def delete(self, request, *args, **kwargs):
        cache.delete_many([LEDGER_CACHE_KEY,TRANSACTIONS_CACHE_KEY])
        response = super().delete(request, *args, **kwargs)
        return response

def update_transactions(request,pk):

    header = TransactionHeader.objects.get(id=pk)

    # Identical to add. Should be the same verifications
    if request.method == "POST":
        form = TransactionsHeaderForm(request.POST, instance=header)
        formset = TransactionsLinesFormSet(request.POST, instance=header)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                header = form.save()
                formset.save()
            cache.delete_many([LEDGER_CACHE_KEY,TRANSACTIONS_CACHE_KEY]) # Deleting the cache here
            messages.success(request, "Transaction updated successfully.")
            return redirect("accounting:ledger")
    else:
        form = TransactionsHeaderForm(instance=header)
        formset = TransactionsLinesFormSet(instance=header, queryset=TransactionLine.objects.select_related('account'))
    return render(request, "accounting/update_transactions.html", {'form': form, 'formset' : formset})

#Financial Statements View Related
class LedgerView(ListView):
    template_name = "accounting/ledger.html"
    model = TransactionLine
    context_object_name = "ledger"

    def get_queryset(self):
        qs = TransactionLine.objects.select_related("header", "account").all()
        return qs
    
    def dispatch(self, request, *args, **kwargs):
        cached_response = cache.get(LEDGER_CACHE_KEY)
        if cached_response: # Return cache if exists
            return cached_response
        response = super().dispatch(request, *args, **kwargs)
        if any(get_messages(request)): # Don't cache if there's a message 
            return response
        response.render() # Starting the caching process
        cache.set(LEDGER_CACHE_KEY, response, None)
        return response

    
class BalanceView(ListView):
    template_name = "accounting/balance.html"
    model = AccountsLink
    context_object_name = "balance"

    def get_queryset(self):
        return (AccountsLink.objects.annotate(total_debit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="D")), Decimal(0)), 
                                             total_credit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="C")), Decimal(0)))
                                             .annotate(total_balance = F("total_debit") - F("total_credit")))

class IncomeStatementView(TemplateView):
    template_name = "accounting/income_statement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(global_data(self.request)) 

        return context 
        

class BalanceSheetView(TemplateView):
    template_name = "accounting/balance_sheet.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(global_data(self.request)) 
        return context 
        