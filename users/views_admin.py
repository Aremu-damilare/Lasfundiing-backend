from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .serializers_admin import CustomUserSerializer, WithdrawalSerializer, KYCSerializer, UpdateUserSerializer, KYCUpdateSerializer
from .models import CustomUser, Withdrawal, KYC
from django.http import Http404
from store.models import Order



class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        # Call the parent class's post method to handle the login logic
        response = super().post(request, *args, **kwargs)

        # Check if the user is an admin
        if self.user and self.user.is_superuser:
            return response  # If admin, return the response as is

        
        return Response(
            {"detail": "Only administrators are allowed to log in."},
            status=status.HTTP_403_FORBIDDEN,
        )



class TotalCountAPIView(APIView):
    def get(self, request, format=None):
        order_count = Order.objects.count()
        withdrawal_count = Withdrawal.objects.count()

        response_data = {
            'order_count': order_count,
            'withdrawal_count': withdrawal_count,
        }

        return Response(response_data)


##
class UserListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):        
        users = CustomUser.objects.filter(is_staff=False)
        return users

    def get(self, request):
        serializer = CustomUserSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)




class UserDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        active = request.data.get("active", "false") == "true"
        is_active = active  
        print(active, is_active)
        request.data["is_active"] = is_active  
        
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



##
class WithdrawalListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):        
        users = Withdrawal.objects.all()
        return users

    def get(self, request):
        serializer = WithdrawalSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class WithdrawalDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Withdrawal.objects.get(pk=pk)
        except Withdrawal.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        withdrawals = self.get_object(pk)
        serializer = WithdrawalSerializer(withdrawals)
        return Response(serializer.data)
    
    def put(self, request, pk):
        withdrawal = self.get_object(pk)
        serializer = WithdrawalSerializer(withdrawal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


##
class KYCListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):        
        kycs = KYC.objects.all()
        return kycs

    def get(self, request):
        serializer = KYCSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    
    

class KYCDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return KYC.objects.get(pk=pk)
        except KYC.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        kyc = self.get_object(pk)
        serializer = KYCSerializer(kyc)
        return Response(serializer.data)

    def put(self, request, pk):
        kyc = self.get_object(pk)
        serializer = KYCUpdateSerializer(kyc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)