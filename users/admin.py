from django.contrib import admin
from .models import CustomUser, Currency


# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Currency)
