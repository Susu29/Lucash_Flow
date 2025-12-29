from django.contrib import admin
from .models import Accounts
# Register your models here.

@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "code_class", "type")
    readonly_fields = ("code_class", "type")

