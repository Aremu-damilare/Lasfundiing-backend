from .models import AccountType, Transaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountTypeSerializer, TransactionSerializer


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

    permission_classes = [IsAuthenticated, IsAdminUser]
    def create(self, request):
        print("xxxxxxxxxxxx", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccountType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_permissions(self):
        # Check the action being performed and return appropriate permissions
        if self.action == 'list':
            return []
        return super().get_permissions()



class TransactionList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        transactions = Transaction.objects.all().order_by('-created_at')[:3]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)