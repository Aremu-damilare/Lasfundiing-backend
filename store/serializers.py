from rest_framework import serializers
from .models import Transaction, AccountType, Order, Platform, BillingDetail, PaymentMethod

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'status', 'payment_method', 'amount', 'currency', 'reference', 'created_at', 'updated_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['order'] = instance.order.id
        representation['card_last_4_digits'] = instance.card_last_4_digits[-4:] if instance.card_last_4_digits else None
        representation['bank_last_4_digits'] = instance.bank_last_4_digits[-4:] if instance.bank_last_4_digits else None
        return representation
    

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id',  'platform', 'description')
      
        
        
class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ('id', 'features', 'description', 'price', 'amount')



class OrderSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer(many=True)
    platform = PlatformSerializer()
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'total_amount', 'coupon', 'order_status', 'order_stage', 
                   'paid', 'platform', 'account_type', 'coupon_applied', 'additional_notes', 'payment_method', 'created_at', 'updated_at')

    def create(self, validated_data):
        print("qqqqqqqqq", validated_data, self.context)
        user = self.context['user']
        print("pppppppppp", self.context)
        validated_data['user'] = user
        return super().create(validated_data)
        
   
        




class BillingSerializer(serializers.ModelSerializer):    
    class Meta:
        model = BillingDetail
        fields = ['first_name', 'last_name', 'address', 'phone', 'city', 'state', 'payment_method']
        
    def create(self, validated_data):
        print("qqqqqqqqq", validated_data, self.context)
        user = self.context['user']        
        validated_data['user'] = user
        return super().create(validated_data)

    