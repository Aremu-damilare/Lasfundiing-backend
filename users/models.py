from django.db import models
from django.contrib.auth.models import AbstractUser


class Currency(models.Model):
    
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code


class CustomUser(AbstractUser):                
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)    
    country = models.CharField(max_length=30, null=True, blank=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.DO_NOTHING)
    
        
class KYC(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    TYPE_CHOICES = (
        ('drivers_license', "Driver's License"),
        ('voters_card', "Voter's Card"),
        ('NIN', 'National Identification Number (NIN)'),
        ('international_passport', 'International Passport'),
    )

    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    type = models.CharField(max_length=150, choices=TYPE_CHOICES)
    file1 = models.FileField(upload_to='kyc_files/')
    file2 = models.FileField(upload_to='kyc_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'KYC for {self.user.username} - {self.status}'
    
    
class WithdrawalMethod(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE, blank=True)
    method_choices = (
        ('bank-transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('cryptocurrency', 'Cryptocurrency'),
    )
    payment_method = models.CharField(max_length=20, choices=method_choices)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    crypto_gateway = models.CharField(max_length=50, blank=True, null=True)
    crypto_address = models.CharField(max_length=50, blank=True, null=True)
    paypal_email = models.EmailField(blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Withdrawal method {self.user} - {self.payment_method} '

    def get_payment_details(self):
        if self.payment_method == 'bank-transfer':
            return {
                'account_number': self.account_number,
                'bank_name': self.bank_name
            }
        elif self.payment_method == 'paypal':
            return {
                'paypal_email': self.paypal_email
            }
        elif self.payment_method == 'cryptocurrency':
            return {
                'crypto_address': self.crypto_address,
                'crypto_gateway': self.crypto_gateway
            }
        else:
            return {}
        

class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('denied', 'Denied'),
        ('pending', 'Pending'),
    )

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # method = models.ForeignKey('WithdrawalMethod', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Withdrawal for {self.user} - {self.amount} - {self.status}'