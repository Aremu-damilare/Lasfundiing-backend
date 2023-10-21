from rest_framework import serializers
from .models import Transaction, AccountType, Order, Platform, PaymentMethod, PaymentDetails
from rest_framework import exceptions
from users.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id',  'platform', 'description')
      

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        

class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = '__all__'
   
   
class TransactionSerializer(serializers.ModelSerializer):
    payment_details = PaymentDetailsSerializer()
    class Meta:
        model = Transaction
        fields = '__all__'

     
        
class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'
        
    def validate(self, data):
        if not data.get('balance'):
            raise exceptions.ValidationError({'balance': 'This field is required.'})
        if not data.get('profit_target'):
            raise exceptions.ValidationError({'profit_target': 'This field is required.'})
        if not data.get('profit_share'):
            raise exceptions.ValidationError({'profit_share': 'This field is required.'})
        if not data.get('next_step_target'):
            raise exceptions.ValidationError({'next_step_target': 'This field is required.'})
        if not data.get('account_fee'):
            raise exceptions.ValidationError({'account_fee': 'This field is required.'})

        return data
    

class OrderSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer()
    transaction = TransactionSerializer()
    payment_method = PaymentMethodSerializer()
    user = UserSerializer()
    class Meta:
        model = Order
        fields ='__all__'
        
        
class OrderUpdateSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Order
        fields ='__all__'
 
 
 
class TransactionDetailSerializer(serializers.ModelSerializer):
    payment_details = PaymentDetailsSerializer()
    class Meta:
        model = Transaction
        fields = '__all__'        
   
   
class OrdersListSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer()
    transaction = TransactionDetailSerializer()
    payment_method = PaymentMethodSerializer()
    class Meta:
        model = Order
        fields ='__all__'


