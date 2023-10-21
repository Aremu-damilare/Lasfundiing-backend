from .models import AccountType, Transaction, Order
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers_admin import AccountTypeSerializer, TransactionSerializer, OrderSerializer, OrderUpdateSerializer
from django.http import Http404


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
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        transactions = Transaction.objects.all().order_by('-created_at')[:3]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    



class OrderListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):        
        orders = Order.objects.all()
        return orders

    def get(self, request):
        serializer = OrderSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

 

class OrderDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def put(self, request, pk):
        order = self.get_object(pk)
        
        # Convert the "active" field to a boolean value
        active = request.data.get("active", "false") == "true"
                
        transaction = order.transaction
                
        transaction_status = request.data.get("transactionStatus", transaction.status)
                
        transaction.status = transaction_status
        transaction.save()
                
        data = {
            "status": request.data.get("status", order.status),            
            "stage": request.data.get("stage", order.stage),
            "profit": request.data.get("profit", order.profit),
            "active": active,
            "transaction": transaction.id,  
        }
        
        serializer = OrderUpdateSerializer(order, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)