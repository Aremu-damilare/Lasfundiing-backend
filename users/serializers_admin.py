from rest_framework import serializers
from .models import CustomUser, Withdrawal, KYC


class CustomUserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CustomUser
        fields ='__all__'
        


class WithdrawalSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Withdrawal
        fields ='__all__'
        

class KYCSerializer(serializers.ModelSerializer):  
    class Meta:
        model = KYC
        fields ='__all__'
        

class UpdateUserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CustomUser
        fields ='__all__'
        extra_kwargs = {
            'password': {'required': False},
            'username': {'required': False},
            'currency': {'required': False},
        }
        
class KYCUpdateSerializer(serializers.ModelSerializer):  
    class Meta:
        model = KYC
        fields ='__all__'
        extra_kwargs = {
            'type': {'required': False},
            'file1': {'required': False},
            'file2': {'required': False},
        }