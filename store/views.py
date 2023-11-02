
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from store.models import Order, AccountType, Platform, PaymentMethod, Coupon, Transaction, PaymentDetails
from users.models import Currency
from django.shortcuts import redirect
from .serializers import TransactionSerializer, OrderSerializer, AccountTypeSerializer, PlatformSerializer, \
    PaymentMethodSerializer, PaymentDetailsSerializer, OrdersListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages

from users.models import CustomUser
from rest_framework import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework import status
from .models import Order
from django.core.files.base import ContentFile
import base64
from django.http import Http404
from django.conf import settings 


User = get_user_model()
from rest_framework.generics import get_object_or_404

class TransactionList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:3]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] 


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):                
        user = get_object_or_404(User, id=request.user.id)
        user_serializer = CustomUserSerializer(user)
        return Response({'user': user_serializer.data})



class OrdersHistoryList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')[:3]
        serializer = OrdersListSerializer(orders, many=True)                
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrdersListSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)
 
        

class AccountTypeList(APIView):        
    def get(self, request):
        account_types = AccountType.objects.all()
        serializer = AccountTypeSerializer(account_types, many=True)
        return Response(serializer.data)


class CheckAccountType(APIView):
    def get(self, request, path):
        try:            
            account_type = AccountType.objects.get(amount=path)
            serializer = AccountTypeSerializer(account_type)
            return Response(serializer.data)
        except AccountType.DoesNotExist:
            return Response(
                {"error": "Account type not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class PlatformsList(APIView):        
    def get(self, request):
        platform = Platform.objects.all()
        serializer = PlatformSerializer(platform, many=True)
        return Response(serializer.data)







class CreateOrder(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Extract the amount and user id from the POST request data
            amount = request.data.get('amount').lower()
            user_id = request.data.get('user')
            paymentMethod = request.data.get('paymentMethod').lower()
            notes = request.data.get('notes')
            currency = request.data.get('currency')                

            # Initialize serializers
            payment_details_serializer = None
            transaction_serializer = None
            order_serializer = None

            # Try to get the PaymentMethod and AccountType objects
            payment_method = get_object_or_404(PaymentMethod, name=paymentMethod)
            account_type = get_object_or_404(AccountType, starting_balance=amount)            
            user_instance = CustomUser.objects.get(id=user_id)
            

            print("user_instance", user_instance.email)

            # Create payment details data based on paymentMethod
            if paymentMethod == 'bank-transfer':
                payment_details_data = {'payment_proof': "None"}   
            elif paymentMethod == 'cyrptocurrency':
                payment_details_data = {'crypto_gateway': "None"}   
            elif paymentMethod == 'paystack':
                payment_details_data = {'reference': "None"}   
            elif paymentMethod == 'card_type':
                payment_details_data = {'payment_proof': "None"}   
        
            # Create PaymentDetailsSerializer
            payment_details_serializer = PaymentDetailsSerializer(data=payment_details_data)

            if payment_details_serializer.is_valid():
                print("payment_details_serializer.is_valid():")
                payment_details = payment_details_serializer.save()

                transaction_data = {
                    'amount': account_type.setup_fee,
                    'currency': currency,
                    'payment_details': payment_details.id
                }            
                transaction_serializer = TransactionSerializer(data=transaction_data)
            else:
                print("payment_details_serializer.errors", payment_details_serializer.errors)
                return Response(payment_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            print(payment_details.id)

            if transaction_serializer.is_valid():
                print("transaction_serializer.is_valid():")
                transaction = transaction_serializer.save()

                order_data = {
                    'account_type': account_type.id,
                    'amount': account_type.setup_fee,
                    'user': user_id,
                    'transaction': transaction.id,
                    'payment_method': payment_method.id,
                    'additional_notes': notes            
                }

                # Create OrderSerializer
                order_serializer = OrderSerializer(data=order_data)

                if order_serializer.is_valid():   
                                 
                    order = order_serializer.save()                    
                    context = {
                            'user': user_instance.email, 'amount': account_type.starting_balance,
                            'payment_method': payment_method.name, 'setup_fee': account_type.setup_fee,
                            'status': transaction.status                        
                            }
                    
                    print(context)
                    # Render the HTML email template
                    email_subject = "New Order Notification"
                    email_body = render_to_string('order/order_confirm.html', context)
                    
                    
                    send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,  # Sender's email address
                    [order.user.email],           # Recipient's email address (user's email)
                    fail_silently=False,          # Set to True to suppress exceptions if sending fails
                    html_message=email_body,      # Set the HTML content here
                )
                    
                    # Render the HTML email template
                    email_subject_admin = "@admin: New Order Notification"
                    email_body_admin = render_to_string('order/order_confirm.html', context)
                                        
                    send_mail(
                    email_subject_admin,
                    email_body_admin,
                    settings.DEFAULT_FROM_EMAIL,  # Sender's email address
                    [settings.ADMIN_EMAILS],           # Recipient's email address (user's email)
                    fail_silently=False,          # Set to True to suppress exceptions if sending fails
                    html_message=email_body_admin,      # Set the HTML content here
                )
                    return Response(order_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    payment_details.delete()
                    transaction.delete()
                    print("order_serializer.errors", order_serializer.errors)
                    return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)                                    
            else:
                print("transaction_serializer.errors", transaction_serializer.errors)
                return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("An error occurred in EXCEPT:", str(e))
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import os
import base64
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer


class PaymentProofUploadAPIView(APIView):
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.pdf'}

    def post(self, request, order_id, format=None):
        try:
            # Retrieve the Order object based on the orderId from the URL path
            order = get_object_or_404(Order, id=order_id)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
    
        # Check if a file was uploaded in the request
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        print(request.FILES)
        
        uploaded_file = request.FILES['file']
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        file_extension = file_extension.lower()

        # Check if the file extension is allowed
        if file_extension not in self.ALLOWED_EXTENSIONS:
            return Response({'error': 'Invalid file type. Please upload a .docx, .png, .jpg, .jpeg, or .pdf file.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert the file content to a string (you may need to adjust this based on the file type)
        file_content = uploaded_file.read()
        encoded_file = base64.b64encode(file_content).decode('utf-8')
        encoded_data = f"data:{uploaded_file.content_type};base64,{encoded_file}"        

        transaction = order.transaction
        payment_details = transaction.payment_details
        payment_details.payment_proof = encoded_data
        payment_details.save()

        # Serialize the updated Order object
        serializer = OrdersListSerializer(order)
        print(order.user.email)
        
        # Render the HTML email template
        # email_subject = "Order Update Notification"
        # email_body = render_to_string('order/order_update.html', {'user': order.user, 'order': order})
        # # print(email_body)
      
        # send_mail(
        #             email_subject,
        #             email_body,
        #             settings.DEFAULT_FROM_EMAIL,  # Sender's email address
        #             [order.user.email],           # Recipient's email address (user's email)
        #             fail_silently=False,          # Set to True to suppress exceptions if sending fails
        #             html_message=email_body,      # Set the HTML content here
        #         )

        # Render the HTML email template
        email_subject_admin = "@admin: Order update Notification"
        email_body_admin = render_to_string('order/order_update.html', {'user': order.user, 'order': order})
                            
        send_mail(
        email_subject_admin,
        email_body_admin,
        settings.DEFAULT_FROM_EMAIL,  # Sender's email address
        [settings.ADMIN_EMAILS],           # Recipient's email address (user's email)
        fail_silently=False,          # Set to True to suppress exceptions if sending fails
        html_message=email_body_admin,      # Set the HTML content here
        )   
        
        return Response(serializer.data, status=status.HTTP_200_OK)

       




def ValidateCoupon(request):
    if request.method == 'POST':
        # print(request.POST)
        coupon_code = request.POST.get('coupon_code')
        order_id = request.POST.get('order_id')        
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({'error': 'Invalid coupon code'})
        
        
        if not coupon.is_valid():
            return JsonResponse({'error': 'Coupon has expired'})        
        order = Order.objects.get(id=order_id)
        
        
        account_type = AccountType.objects.get(pk=order.account_type.id)
        # print(account_type.price)
                
        # total_price = order.get_total() account_type.price        
        
        discount = coupon.discount / 100
        total_price = account_type.price
        discounted_amount = round(total_price * discount, 2)
        
        order = Order.objects.get(id=order_id)
        order.amount = discounted_amount
        # order.quantity = quantity
        order.coupon = coupon
        order.coupon_applied = True
        order.save()
        
        # discounted_price = round(total_price - discounted_amount, 2)
        # print(discounted_price)
                        
        coupon.expiry_date = timezone.now() - timedelta(days=1)  # set expiry date to a past date
        coupon.save()        
        
        # except:
        #     print("Error adding coupon to order")
        return JsonResponse({'discounted_price': discounted_amount})
    
