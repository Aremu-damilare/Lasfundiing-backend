from rest_framework import serializers
from .models import Transaction, AccountType, Order, Platform, PaymentMethod, PaymentDetails
from rest_framework import exceptions


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['user'] = instance.user.username
    #     representation['order'] = instance.order.id
    #     representation['card_last_4_digits'] = instance.card_last_4_digits[-4:] if instance.card_last_4_digits else None
    #     representation['bank_last_4_digits'] = instance.bank_last_4_digits[-4:] if instance.bank_last_4_digits else None
    #     return representation
    

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
    # account_type = AccountTypeSerializer()
    # transaction = TransactionSerializer()
    # payment_method = PaymentMethodSerializer()
    
    class Meta:
        model = Order
        fields ='__all__'

    # def create(self, validated_data):
    #     print("qqqqqqqqq", validated_data, self.context)
    #     user = self.context['user']
    #     print("pppppppppp", self.context)
    #     validated_data['user'] = user
    #     return super().create(validated_data)
 
 
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


