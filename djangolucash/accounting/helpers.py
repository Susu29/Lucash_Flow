from .models import Accounts, Suppliers, Customers, TransactionHeader, TransactionLine, AccountsLink
from django.views.generic import TemplateView

from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce
from decimal import Decimal

def global_data(request):
    context = {}
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


    ### P&L RELATED. #NOT MODIFYING THE CONTEXT NAME BECAUSE I DON'T FEEL LIKE CHANGING THE TEMPLATE RN. MAYBE LATER. BUT SHOULD BE NAMED PL
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


    ####################### @STATISTICS@ #######################

    # Amount of instance

    context["suppliers_amount"] = Suppliers.objects.count()
    context["customers_amount"] = Customers.objects.count()
    context["transactionheader_amount"] = TransactionHeader.objects.count()
    context["transactionline_amount"] = TransactionLine.objects.count()
    context["accounts_amount"] = Accounts.objects.count()

    return context