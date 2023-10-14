from rest_framework import serializers
from .models import Ticket, TicketComment


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        
class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = '__all__'