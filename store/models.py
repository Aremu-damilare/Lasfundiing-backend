from django.db import models
from users.models import CustomUser
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError
import random


def default_features():
    return []

class AccountType(models.Model):        
    description = models.CharField(max_length=1000, blank=False, null=True)
    amount = models.FloatField(default=5000, blank=False, null=True)
    setup_fee = models.FloatField(default=5000, blank=False, null=True)
    starting_monthly_fee = models.FloatField(default=5000, blank=False, null=True)
    starting_balance = models.FloatField(default=5000, blank=False, null=True)
    balance = models.JSONField(default=default_features, blank=False, null=True)
    profit_target = models.JSONField(default=default_features, blank=False, null=True)
    profit_share = models.JSONField(default=default_features, blank=False, null=True)
    next_step_target = models.JSONField(default=default_features, blank=False, null=True)
    account_fee = models.JSONField(default=default_features, blank=False, null=True)
    
    
    def __str__(self):
        return f'{self.amount}' 
    
    


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return self.code

    def is_valid(self):
        return timezone.now() < self.expiry_date



class Order(models.Model):    
    def generate_unique_id():
        while True:
            unique_id = random.randint(10**11, 10**12 - 1)
            if not Order.objects.filter(id=unique_id).exists():
                return unique_id
    
    ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('cancelled', 'Cancelled'),
    ('success', 'Success'),
    ('failed', 'Failed'),
    )

    ORDER_STAGE_CHOICES = (
        ('idle', 'Idle'),
        ('close', 'Close'),
        ('active', 'Active'),
        ('phase_2_demo', 'Phase 2 Demo'),
        ('phase_1_demo', 'Phase 1 Demo'),
    )
      
    
    account_type = models.ForeignKey('AccountType',  on_delete=models.DO_NOTHING, null=True)
    platform = models.ForeignKey('Platform', on_delete=models.DO_NOTHING, blank=True, null=True)    
    id = models.PositiveIntegerField(primary_key=True, default=generate_unique_id, unique=True)
    # id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)    
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', null=True)
    stage = models.CharField(max_length=20, choices=ORDER_STAGE_CHOICES, default="idle", null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True,)
    
    coupon_applied = models.BooleanField(default=False, null=True)
    active = models.BooleanField(default=False, null=True)
    
    profit = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=True)
    
    additional_notes = models.CharField(blank=True, null=True, max_length=40)
    
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.DO_NOTHING, null=True, blank=False)
    transaction = models.ForeignKey('Transaction', on_delete=models.DO_NOTHING, null=True, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         # This block only runs when updating an existing order (not for new orders).
    #         existing_order = Order.objects.filter(
    #             user=self.user,
    #             status='success',
    #             stage='active',
    #             active=True
    #         ).exclude(id=self.id)

    #         if existing_order.exists():
    #             raise ValidationError("You can have only one active, successful order.")
        
        # super(Order, self).save(*args, **kwargs)
    def __str__(self):
        return f'Order #{self.pk}'    
    

    
    
class Platform(models.Model):
    platform = models.CharField(max_length=1000)   
    description = models.CharField(max_length=1000, null=True)
    
    def __str__(self):
        return self.platform



class OrderStage(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    
    
class OrderStatus(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return self.title
     
        
                
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name



class PaymentDetails(models.Model):
    crypto_gateway = models.CharField(max_length=20, null=True, blank=True )        
    reference = models.CharField(max_length=20, null=True, blank=True )    
    payment_proof = models.CharField(max_length=255, null=True, blank=True )
    card_type = models.CharField(max_length=20, null=True, blank=True )    
    card_last_4_digits = models.CharField(max_length=4, null=True, blank=True)
    bank_last_4_digits = models.CharField(max_length=4, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('cancelled', 'cancelled'),
        ('failed', 'Failed'),
    ]
           
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=20)
    
    payment_details = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE, null=True, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.status} - {self.amount}"
