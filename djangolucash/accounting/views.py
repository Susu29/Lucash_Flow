from .models import Accounts, Suppliers, Customers, TransactionHeader, TransactionLine, AccountsLink
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, FormView
from .forms import AccountsForm, SelectAccountsForm, SelectSuppliersForm, TransactionsHeaderForm, TransactionsLinesFormSet, SelectTransactionsForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce
from decimal import Decimal

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
        else:
            return reverse('accounting:accounts')
        

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

def add_transactions(request):
    if request.method == "POST":
        form = TransactionsHeaderForm(request.POST)
        formset = TransactionsLinesFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                header = form.save()
                formset.instance = header
                formset.save()
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



class LedgerView(ListView):
    template_name = "accounting/ledger.html"
    model = TransactionLine
    context_object_name = "ledger"


class SelectTransactionsView(FormView): ### To be deleted soon
    template_name = "accounting/select_transactions.html"
    form_class = SelectTransactionsForm

    def form_valid(self, form):
        selected = form.cleaned_data["transactions"]
        return redirect("accounting:delete_transactions", pk=selected.id)
    
class DeleteTransactionsView(SuccessMessageMixin, DeleteView):
    template_name = "accounting/delete_transactions.html"
    success_url = reverse_lazy('accounting:ledger')
    success_message = ('Transaction deleted successfully.')

class BalanceView(ListView):
    template_name = "accounting/balance.html"
    model = AccountsLink
    context_object_name = "balance"
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)



        context["total_debit"] = (AccountsLink.objects.annotate(total_debit = Sum('transactionline__amount')))
        return context
    """
    def get_queryset(self):
        return (AccountsLink.objects.annotate(total_debit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="D")), Decimal(0)), 
                                             total_credit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="C")), Decimal(0)))
                                             .annotate(total_balance = F("total_debit") - F("total_credit")))

class IncomeStatementView(TemplateView):
    template_name = "accounting/income_statement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        an = (AccountsLink.objects.annotate(total_debit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="D")), Decimal(0)), 
                                             total_credit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="C")), Decimal(0)))
                                             .annotate(total_balance = F("total_debit") - F("total_credit")))
        
        context["totals"] = an.aggregate(
        op_expenses=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="60") | Q(sorting_account__startswith="61")| Q(sorting_account__startswith="62")| Q(sorting_account__startswith="63")| Q(sorting_account__startswith="64")| Q(sorting_account__startswith="65")| Q(sorting_account__startswith="68")), Decimal("0.00")),
        fi_expenses=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="66")), Decimal("0.00")),
        ex_expenses=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="67")), Decimal("0.00")),
        op_revenues=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="70") | Q(sorting_account__startswith="71")| Q(sorting_account__startswith="72")| Q(sorting_account__startswith="73")| Q(sorting_account__startswith="74")| Q(sorting_account__startswith="75")| Q(sorting_account__startswith="78")), Decimal("0.00")),
        fi_revenues=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="76")), Decimal("0.00")),
        ex_revenues=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="77")), Decimal("0.00")),
        )
        context["grand_total_expenses"] = context["totals"]["op_expenses"] + context["totals"]["fi_expenses"] + context["totals"]["ex_expenses"]
        context["grand_total_revenues"] = context["totals"]["op_revenues"] + context["totals"]["fi_revenues"] + context["totals"]["ex_revenues"]
        context["result"] = context["grand_total_revenues"] - context["grand_total_expenses"]
        context["grand_total"] = max(context["grand_total_revenues"],context["grand_total_expenses"])


        return context 
        