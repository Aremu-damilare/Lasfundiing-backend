from django.contrib import admin
from .models import AccountType, Platform, PaymentMethod, OrderStage, Order, \
    OrderStatus, Coupon, Transaction, PaymentDetails
# Register your models here.

admin.site.register(AccountType)
admin.site.register(Coupon)
admin.site.register(Platform)
admin.site.register(PaymentMethod)
admin.site.register(OrderStage)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(PaymentDetails)



