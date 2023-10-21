from rest_framework import serializers
from .models import Ticket, TicketComment

from users.models import CustomUser

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class TicketSerializer(serializers.ModelSerializer):
    # user = UsersSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'
        
        
class TicketViewSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'
        
class TicketCommentSerializer(serializers.ModelSerializer):
    # user = UsersSerializer()
    class Meta:
        model = TicketComment
        fields = '__all__'
        
class TicketCommentViewSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = TicketComment
        fields = '__all__'