from django.db import models
from django.contrib.auth.models import AbstractUser


class Currency(models.Model):
    
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code

class CustomUser(AbstractUser):        
        
    
    phone = models.CharField(max_length=30, null=True, blank=False)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.DO_NOTHING)
    
        
