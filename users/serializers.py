from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Currency, WithdrawalMethod, Withdrawal
from rest_framework import status
from django.urls import reverse
from django.http import HttpRequest
from rest_framework.test import APIClient
from rest_framework.generics import get_object_or_404
from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_framework import serializers
from .models import KYC


class CustomRegisterSerializer(RegisterSerializer):
    username = None    
    phone = serializers.CharField(max_length=30)        
    firstname = serializers.CharField(max_length=30)        
    lastname = serializers.CharField(max_length=30)        
    # country = serializers.CharField(max_length=40)        
    address = serializers.CharField(max_length=40)        
    
    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.phone = self.data.get('phone')        
        user.first_name = self.data.get('firstname')        
        user.last_name = self.data.get('lastname')        
        # user.country = self.data.get('country')        
        user.address = self.data.get('address')        
        
        # Get the default currency
        default_currency_code = 'NGN' 
        default_currency = Currency.objects.get(code=default_currency_code)
        user.currency = default_currency
        
        # print("self.data", self.data)
        user.save()
        
        paymentMethod = self.context['request'].data.get('paymentMethod')
        # payment_method_instance = get_object_or_404(PaymentMethod, name=paymentMethod)
        
        accountType = self.context['request'].data.get('accountType')       
        notes = self.context['request'].data.get('Notes')     
                 
        order_data = {'user': user.id, 'amount': accountType, 'paymentMethod': paymentMethod, 'notes': notes, 'currency': user.currency}
                        
        print("order_data", order_data)
        # print("self", self.context['request'])
            
        if user.id and accountType and paymentMethod and user.currency:            
            # Make a POST request to the CreateOrder view
            create_order_url = '/create_order/'                        
            
            fake_request = HttpRequest()
            fake_request.method = 'POST'

            # Send POST request to VerifyEmailView
            client = APIClient()
            create_order_response = client.post(create_order_url, data=order_data)
            print(create_order_response)

            # Check the response status code and handle it accordingly
            if create_order_response.status_code == status.HTTP_201_CREATED:
                # Order was created successfully
                # return Response("Order created successfully", status=status.HTTP_201_CREATED)
                print("Order created successfully")                
            elif create_order_response.status_code == status.HTTP_400_BAD_REQUEST:
                # Order creation failed, handle the error
                # return Response("Order creation failed", status=status.HTTP_400_BAD_REQUEST)
                print("Order creation failed", create_order_response)                
            else:
                # Handle other response status codes as needed
                # return Response("Unexpected error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
                print("Unexpected error")                
        else:
            print("deleting user..")
            user.delete()
            return None
            
        return user


class LoginSerializer(RestAuthLoginSerializer):
    username = None
    
    
class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = '__all__'
    
    


class WithdrawalMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalMethod
        fields = '__all__'
        
        
class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'