from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Currency


class CustomRegisterSerializer(RegisterSerializer):
    username = None    
    phone = serializers.CharField(max_length=30)        
    firstname = serializers.CharField(max_length=30)        
    lastname = serializers.CharField(max_length=30)        
    country = serializers.CharField(max_length=40)        
    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.phone = self.data.get('phone')        
        user.first_name = self.data.get('firstname')        
        user.last_name = self.data.get('lastname')        
        user.country = self.data.get('country')        
        
        # Get the default currency
        default_currency_code = 'NGN' 
        default_currency = Currency.objects.get(code=default_currency_code)
        user.currency = default_currency
        
        print("sssssaveeee", self.data)
        user.save()
        return user
    

from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer


class LoginSerializer(RestAuthLoginSerializer):
    username = None