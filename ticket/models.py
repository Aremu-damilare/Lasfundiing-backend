from django.db import models
from users.models import CustomUser

class Ticket(models.Model):
    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('normal', 'Normal'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('close', 'Close'),
    )
    
    DEPT_CHOICES = (
        ('account-type', 'account-type'),        
        ('enquiry', 'Enquiry'),
        ('funding', 'Funding'),
        ('withdrawal', 'Withdrawal'),
        ('order', 'Order'),
        ('payment-method', 'Payment-method'),
    )

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, default="open",)
    department = models.CharField(max_length=40, choices=DEPT_CHOICES, default="enquiry", null=True, blank=False)
    subject = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment on {self.ticket.subject}"
