from django.contrib import admin
from .models import AccountType, BillingDetail, Platform, PaymentMethod, OrderStage, Order, \
    OrderStatus, Coupon, Transaction
# Register your models here.

admin.site.register(AccountType)
admin.site.register(Coupon)
admin.site.register(BillingDetail)
admin.site.register(Platform)
admin.site.register(PaymentMethod)
admin.site.register(OrderStage)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(Transaction)



