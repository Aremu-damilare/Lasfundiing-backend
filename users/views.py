from django.contrib.auth.views import  LogoutView
from django.http.response import  HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from allauth.account.admin import EmailAddress
from allauth.account.utils import send_email_confirmation
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework.test import APIClient
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import generics, permissions
from .models import KYC, WithdrawalMethod, Withdrawal
from .serializers import KYCSerializer, WithdrawalMethodSerializer, WithdrawalSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings 



User = get_user_model()

def verify_email(request, key):
    # Create a fake request object
    fake_request = HttpRequest()
    fake_request.method = 'POST'
    fake_request.data = {'key': key}

    # Send POST request to VerifyEmailView
    client = APIClient()
    response = client.post('/account-confirm-email/', data=fake_request.data)
    print(response)
    
    if response.status_code == 200:
        # Redirect user to dashboard
        return redirect('https://lasfunding.com/#/#signin/')
    else:
        # Handle error (e.g. display error message)
        # print("Returning home..........")
        return redirect('https://lasfunding.com/#/#signin/')
    

class Logout(LogoutView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class NewEmailConfirmation(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response( {'message': 'This email is already verified'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, 
                                status=status.HTTP_201_CREATED)
            except APIException:
                return Response({'message': 'This email does not exist, please create a new account'}, 
                                status=status.HTTP_403_FORBIDDEN)


class KYCListCreateView(generics.ListCreateAPIView):
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class KYCDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    
class WithdrawalMethodList(APIView):
    def get(self, request):
        withdrawal_methods = WithdrawalMethod.objects.all()
        serializer = WithdrawalMethodSerializer(withdrawal_methods, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        withdrawal_method, created = WithdrawalMethod.objects.get_or_create(user=user)

        serializer = WithdrawalMethodSerializer(withdrawal_method, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class WithdrawalMethodDetail(APIView):
    def get_object(self, user_id):
        try:
            return WithdrawalMethod.objects.get(user__id=user_id)
        except WithdrawalMethod.DoesNotExist:
            return None

    def get(self, request, user_id):
        withdrawal_method = self.get_object(user_id)
        if withdrawal_method:
            serializer = WithdrawalMethodSerializer(withdrawal_method)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        withdrawal_method = self.get_object(user_id)
        if withdrawal_method:
            serializer = WithdrawalMethodSerializer(withdrawal_method, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalList(APIView):
    def get(self, request):
        withdrawals = Withdrawal.objects.filter(user=request.user)
        serializer = WithdrawalSerializer(withdrawals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        withdrawal = Withdrawal.objects.create(user=user, amount=request.data.get('amount'))
        serializer = WithdrawalSerializer(withdrawal, data=request.data, partial=True)
        if serializer.is_valid():                        
            serializer.save()
            
             # Render the HTML email template
            email_subject_admin = "@admin: Withdrawal request Notification"
            email_body_admin = render_to_string('withdrawal/withdrawal_new.html', {'withdrawal': withdrawal,  'user': user.email})
                                
            send_mail(
            email_subject_admin,
            email_body_admin,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email address
            [settings.ADMIN_EMAILS],           # Recipient's email address (user's email)
            fail_silently=False,          # Set to True to suppress exceptions if sending fails
            html_message=email_body_admin,      # Set the HTML content here
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalDetail(APIView):
    def get_object(self, withdrawal_id):
        try:
            return Withdrawal.objects.get(id=withdrawal_id)
        except Withdrawal.DoesNotExist:
            return None

    def get(self, request, withdrawal_id):
        withdrawal = self.get_object(withdrawal_id)
        if withdrawal:
            serializer = WithdrawalSerializer(withdrawal)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, withdrawal_id):
        withdrawal = self.get_object(withdrawal_id)
        if withdrawal:
            serializer = WithdrawalSerializer(withdrawal, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, withdrawal_id):
        withdrawal = self.get_object(withdrawal_id)
        if withdrawal:
            withdrawal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
        

class KYCCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):        
        kyc = KYC.objects.get(user=self.request.user)
        return kyc

    def get(self, request):
        serializer = KYCSerializer(self.get_queryset())
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        kycs = KYC.objects.filter(user=user)

        if kycs.exists():
            for kyc in kycs:
                if kyc.status == "approved":
                    return Response("approved", status=status.HTTP_400_BAD_REQUEST)
                
            # Update existing KYC record if status is "rejected"
            kyc = kycs.first()
            serializer = KYCSerializer(kyc, data=request.data, partial=True)  # Use partial=True to allow partial updates
            if serializer.is_valid():
                serializer.save()
                
                # Render the HTML email template
                email_subject_admin = "@admin: KYC new Notification"
                email_body_admin = render_to_string('kyc/kyc_new.html', {'user': user.email})
                                    
                send_mail(
                email_subject_admin,
                email_body_admin,
                settings.DEFAULT_FROM_EMAIL,  # Sender's email address
                [settings.ADMIN_EMAILS],           # Recipient's email address (user's email)
                fail_silently=False,          # Set to True to suppress exceptions if sending fails
                html_message=email_body_admin,      # Set the HTML content here
                )
                        
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Remove "user" from the request data for new KYC creation
            request_data = request.data.copy()
            request_data.pop('user', None)

            # Create a new KYC record
            serializer = KYCSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save(user=user)
                
                # Render the HTML email template
                email_subject_admin = "@admin: KYC update Notification"
                email_body_admin = render_to_string('kyc/kyc_update.html', {'user': user.email})
                                    
                send_mail(
                email_subject_admin,
                email_body_admin,
                settings.DEFAULT_FROM_EMAIL,  # Sender's email address
                [settings.ADMIN_EMAILS],           # Recipient's email address (user's email)
                fail_silently=False,          # Set to True to suppress exceptions if sending fails
                html_message=email_body_admin,      # Set the HTML content here
                )
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
