from django.db import models

# Create your models here.
class Accounts(models.Model):

    code = models.CharField(max_length=6, unique=True)
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
            self.code_class = int(self.code[0])

    def save(self, *args, **kwargs):
        self.field_calculations()
        super().save(*args, **kwargs)
