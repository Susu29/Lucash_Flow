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

# Create your views here.
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
            messages.success(request, "Transaction updated successfully.")
            return redirect("accounting:ledger")
    else:
        form = TransactionsHeaderForm(instance=header)
        formset = TransactionsLinesFormSet(instance=header)
    return render(request, "accounting/update_transactions.html", {'form': form, 'formset' : formset})

#Financial Statements View Related

class LedgerView(ListView):
    template_name = "accounting/ledger.html"
    model = TransactionLine
    context_object_name = "ledger"

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
        

class BalanceSheetView(TemplateView):
    template_name = "accounting/balance_sheet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        an = (AccountsLink.objects.annotate(total_debit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="D")), Decimal(0)), 
                                             total_credit = Coalesce(Sum('transactionline__amount', filter=Q(transactionline__debit_credit="C")), Decimal(0)))
                                             .annotate(total_balance = F("total_debit") - F("total_credit")))
        
        context["bal"] = an.aggregate(
        # BY CLASS
        class_1=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="1")), Decimal("0.00")),
        class_2=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="2")), Decimal("0.00")),
        class_3=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="3")), Decimal("0.00")),
        class_4=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="4")), Decimal("0.00")),
        class_5=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="5")), Decimal("0.00")),
        class_6=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="6")), Decimal("0.00")),
        class_7=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="7")), Decimal("0.00")),

        ## Using basic regex from now because i don't want to copy past 1000 times
        #ASSETS
        #FIXED ASSETS
        intangible_assets=Coalesce(Sum('total_balance', filter=Q(sorting_account__regex=r'^(20|28)')), Decimal("0.00")),
        tangible_assets=Coalesce(Sum('total_balance', filter=Q(sorting_account__regex=r'^(21|22|23|29)')), Decimal("0.00")),
        financial_assets=Coalesce(Sum('total_balance', filter=Q(sorting_account__regex=r'^(25|26|27)')), Decimal("0.00")),

        # CURRENT ASSETS
        inventories=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="3")), Decimal("0.00")),
        accounts_receivable=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="41")), Decimal("0.00")),
        cash_and_equiv=Coalesce(Sum('total_balance', filter=Q(sorting_account__startswith="5")), Decimal("0.00")),

        #LIABILITIES
        #EQUITY 
        share_capital=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="101")), Decimal("0.00")),
        reserves=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="106")), Decimal("0.00")),
        retained_earnings=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="11")), Decimal("0.00")),
        net_income=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="12")), Decimal("0.00")),

        #DEBT
        financial_debt=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="16")), Decimal("0.00")),
        accounts_payable=Coalesce(-Sum('total_balance', filter=Q(sorting_account__startswith="40")), Decimal("0.00")),
        other_payables=Coalesce(-Sum('total_balance', filter=Q(sorting_account__regex=r'^(42|43|44|45|46|47)')), Decimal("0.00")),
        )

        #TOTALS & SUB-TOTALS
        context["fixed_assets"] = context["bal"]["intangible_assets"] + context["bal"]["tangible_assets"] + context["bal"]["financial_assets"]
        context["current_assets"] = context["bal"]["inventories"] + context["bal"]["accounts_receivable"] + context["bal"]["cash_and_equiv"]
        context["assets"] = context["fixed_assets"] + context["current_assets"]
        ### Not a total but calculated separately
        context["net_income"] = context["bal"]["class_7"] - context["bal"]["class_6"]
        context["other_equity"] = context["bal"]["class_1"] - context["bal"]["share_capital"] - context["bal"]["reserves"] - context["bal"]["retained_earnings"] - context["bal"]["financial_debt"]
        ### Not a total but calculated separately
        context["equity"] = context["bal"]["share_capital"] + context["bal"]["reserves"] + context["bal"]["retained_earnings"] + context["net_income"] + context["other_equity"]
        context["debt"] = context["bal"]["financial_debt"] + context["bal"]["accounts_payable"] + context["bal"]["other_payables"]
        context["liabilities"] = context["equity"] + context["debt"]

        ###EXACT DIFFERENCE = NET INCOME
        return context 
        