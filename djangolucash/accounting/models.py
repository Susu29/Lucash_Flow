from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
            ### INT IS THE PROBLEM HERE. I NEED TO EXTRACT THE FIRST VALUE OF AN INT
            self.code_class = int(two_digits[0])

    def save(self, *args, **kwargs):
        self.field_calculations()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}" 
    

class Suppliers(models.Model):
    code = models.CharField(unique=True, max_length=3)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(blank=True,null=True, max_length=200)
    phone = models.CharField(blank=True,null=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def field_calculations(self):
        self.code = self.code.upper() 

    def save(self, *args, **kwargs):
        self.field_calculations()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}" 
    
    
class Customers(models.Model):
    code = models.CharField(unique=True, max_length=3)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(blank=True,null=True, max_length=200)
    phone = models.CharField(blank=True,null=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}" 