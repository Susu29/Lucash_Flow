from django.contrib import admin
from .models import Accounts, Suppliers, Customers, AccountsLink, TransactionHeader, TransactionLine
# Register your models here.

@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "code_class", "type")
    readonly_fields = ("code_class", "type")

admin.site.register(Suppliers)
admin.site.register(Customers)
admin.site.register(AccountsLink)
admin.site.register(TransactionHeader)
admin.site.register(TransactionLine)