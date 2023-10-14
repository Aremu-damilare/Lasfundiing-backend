from django.contrib import admin
from .models import CustomUser, Currency, Withdrawal, WithdrawalMethod


# Register your models here.


admin.site.register(CustomUser)
admin.site.register(WithdrawalMethod)
admin.site.register(Withdrawal)
admin.site.register(Currency)
