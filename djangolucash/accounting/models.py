from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Accounts(models.Model):

    code = models.IntegerField(unique=True, validators=[MinValueValidator(100), MaxValueValidator(999999)])
    name = models.CharField(max_length=200)
    code_class = models.IntegerField(editable=False) # Updated with Save
    type = models.CharField(editable=False, max_length=1) # Updated with Save

    def field_calculations(self):
        if self.code:
            two_digits = str(self.code)[:2]
            if two_digits == '40':
                self.type = 'S'
            elif two_digits == '41':
                self.type = 'C'
            else:
                self.type = 'G'
            self.code_class = int(two_digits[0])

    def save(self, *args, **kwargs):
        self.field_calculations()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}" 
    

class Suppliers(models.Model):
    code = models.CharField(unique=True, max_length=3, validators=[MinLengthValidator(3)])
    account_code = models.CharField(unique=True, max_length=6, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(blank=True,null=True, max_length=200)
    phone = models.CharField(blank=True,null=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def field_calculations(self):     
        if self.code:
            self.code = self.code.upper()
            self.account_code = "401" + self.code

    def save(self, *args, **kwargs):
        self.field_calculations()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}" 
    
    
class Customers(models.Model):
    code = models.CharField(unique=True, max_length=3, validators=[MinLengthValidator(3)])
    account_code = models.CharField(unique=True, max_length=6, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(blank=True,null=True, max_length=200)
    phone = models.CharField(blank=True,null=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def field_calculations(self):     
        if self.code:
            self.code = self.code.upper()
            self.account_code = "411" + self.code

    def save(self, *args, **kwargs):
        self.field_calculations()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.code} - {self.name}" 

class AccountsLink(models.Model):
    # For this model :
    # The existing accounts have been sync with a SQL request directly into the DB
    # For the new accounts, a SQL trigger function has been incorported to the migration #7.
    # Seems like it was the only solution that apply both to django modification and to direct SQL injection.
    account = models.ForeignKey(Accounts,on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, null=True, blank=True)
    sorting_account = models.CharField(max_length = 6, unique=True, editable=False)

    class Meta:
        sorting = ["sort_code", "id"]

    def clean(self):
        count = sum(bool(x) for x in (self.account, self.customer, self.supplier))
        if count != 1:
            raise ValidationError("Select exactly ONE account, customer, or supplier")

    def __str__(self):
        if self.customer:
           return self.customer.account_code 
        if self.supplier:
            return self.supplier.account_code
        return str(self.account.code)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    
class TransactionHeader(models.Model):
    invoice = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TransactionLine(models.Model):

    type_choices = [
    ("D", "D"),
    ("C", "C"),
    ]

    header = models.ForeignKey(TransactionHeader, on_delete=models.CASCADE)
    debit_credit = models.CharField(max_length=1, choices=type_choices)
    account = models.ForeignKey(AccountsLink, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)


    




