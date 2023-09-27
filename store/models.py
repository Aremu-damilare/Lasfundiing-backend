from django.db import models
from users.models import CustomUser
from django.utils import timezone
import uuid



class AccountType(models.Model):
    features = models.TextField()
    description = models.CharField(max_length=1000)
    amount = models.IntegerField(default=5000)
    price = models.DecimalField (max_digits=10, decimal_places=2, default=69, null=True, blank=False)
    
    def __str__(self):
        return f'{self.amount}' 
    
    

class BillingDetail(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return str(self.user)


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return self.code

    def is_valid(self):
        return timezone.now() < self.expiry_date



class Order(models.Model):
    
    ORDER_STATUS_CHOICES = (
    ('in_progress', 'In Progress'),
    ('cancelled', 'Cancelled'),
    ('success', 'Success'),
    )

    ORDER_STAGE_CHOICES = (
        ('idle', 'Idle'),
        ('close', 'Close'),
        ('active', 'Active'),
        ('phase_2_demo', 'Phase 2 Demo'),
        ('phase_1_demo', 'Phase 1 Demo'),
    )
    
    account_type = models.ManyToManyField('AccountType')
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE)        
    order_number = models.UUIDField(default=uuid.uuid4, editable=False)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    discounted_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="in_progress", null=True)
    order_stage = models.CharField(max_length=20, choices=ORDER_STAGE_CHOICES, default="idle", null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False, blank=True, null=True)        
    coupon_applied = models.BooleanField(default=False, null=True)
    additional_notes = models.CharField(blank=True, null=True, max_length=40)
    payment_method = models.CharField(blank=True, null=True, max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

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



class Transaction(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
    ]
           
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=20, null=True, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=20)
    reference = models.CharField(max_length=20, null=True, blank=False )    
    card_type = models.CharField(max_length=20, null=True, blank=True )    
    card_last_4_digits = models.CharField(max_length=4, null=True, blank=True)
    bank_last_4_digits = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.status} - {self.payment_method} - {self.amount}"
