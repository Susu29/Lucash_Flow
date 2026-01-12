from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
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
    account = models.OneToOneField(Accounts,on_delete=models.CASCADE, null=True, blank=True)
    customer = models.OneToOneField(Customers, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.OneToOneField(Suppliers, on_delete=models.CASCADE, null=True, blank=True)
    sorting_account = models.CharField(max_length = 6, editable=False, null=False, blank=False, unique=True)

    class Meta:
        ordering = ["sorting_account", "id"]

    def clean(self):
        count = sum(bool(x) for x in (self.account, self.customer, self.supplier))
        if count != 1:
            raise ValidationError("Select exactly ONE account, customer, or supplier")

    def __str__(self):

        if self.customer:
            return str(f'{self.customer.account_code} - {self.customer.name}')
        if self.supplier:
            return str(f'{self.supplier.account_code} - {self.supplier.name}')
        return str(f'{self.account.code} - {self.account.name[:100]}') # Can do the same for name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    
class TransactionHeader(models.Model):
    invoice = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def formatted_date(self):
            return self.date.strftime("%d/%m/%Y")
    

    def __str__(self):
        return f"{self.id}" 

class TransactionLine(models.Model):

    type_choices = [
    ("D", "D"),
    ("C", "C"),
    ]

    header = models.ForeignKey(TransactionHeader, on_delete=models.CASCADE)
    debit_credit = models.CharField(max_length=1, choices=type_choices, blank=False, null=False)
    account = models.ForeignKey(AccountsLink, on_delete=models.PROTECT, blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal(0.01))], blank=False, null=False)

    



