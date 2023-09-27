
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from django.contrib.auth import get_user_model
from store.models import Order, AccountType, Platform, PaymentMethod, Coupon, BillingDetail, Transaction
from users.models import Currency
from django.shortcuts import redirect
from users.forms import BillingForm
from .serializers import TransactionSerializer, OrderSerializer, AccountTypeSerializer, PlatformSerializer, BillingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from rest_framework import status
from users.models import CustomUser
from rest_framework import serializers


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
        serializer = OrderSerializer(orders, many=True)                
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)
        

class AccountTypeList(APIView):        
    def get(self, request):
        account_types = AccountType.objects.all()
        serializer = AccountTypeSerializer(account_types, many=True)
        return Response(serializer.data)


class PlatformsList(APIView):        
    def get(self, request):
        platform = Platform.objects.all()
        serializer = PlatformSerializer(platform, many=True)
        return Response(serializer.data)



# def OrderHistoryDetail(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     return render(request, 'order_history_detail.html', {'order': order})

# @login_required
# def ChoosePlatform(request, account_type_id):
#     account_type = AccountType.objects.get(pk=account_type_id)
#     platforms = Platform.objects.all()    
#     context = {'account_type': account_type, 'platforms': platforms}
#     return render(request, 'choose_platform.html', context)


class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # account_type_id = request.data.get('account_type')
        # print("yyyyy", request.data)
        # try:
        #     account_type = AccountType.objects.get(id=account_type_id)
        # except AccountType.DoesNotExist:
        #     return Response({'error': 'Invalid account type ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer_context = {
            'user': request.user,
            # 'account_type': account_type
        }
                
        serializer = self.get_serializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        account_types = order.account_type.all()            
        total_amount = sum(account_type.price for account_type in account_types)
        order.total_amount = total_amount
        order.save()

        return Response({'success': 'Order created successfully', 'order_id': order.id})



class BillingCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated]
    queryset = BillingDetail.objects.all()

    def post(self, request, *args, **kwargs):        
        serializer_context = {
            'user': request.user,            
        }
        print("userrr", serializer_context)
        billing_detail = BillingDetail.objects.filter(user=request.user).first()
        if billing_detail:
            # Perform update
            serializer = self.get_serializer(billing_detail, data=request.data)
        else:
            # Perform create
            serializer = self.get_serializer(data=request.data, context=serializer_context)
            
        
        serializer.is_valid(raise_exception=True)
        billing = serializer.save()

        return Response({'success': 'Billing created successfully'})
    
# @login_required
# def OrderCreationDetail(request, order_id):
#     # Retrieve the order object based on the order_id
#     order = Order.objects.get(pk=order_id)

#     # Render the order detail page with the order object
#     context = {'order': order}
#     return render(request, 'order_creation_detail.html', context)




@login_required
def ValidateCoupon(request):
    if request.method == 'POST':
        # print(request.POST)
        coupon_code = request.POST.get('coupon_code')
        order_id = request.POST.get('order_id')
        # quantity = request.POST.get('quantity')
        

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
        order.total_amount = discounted_amount
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
    

    

class CheckOutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payment_method_id = request.data.get('payment_method')
        # payment_method = PaymentMethod.objects.get(id=payment_method_id)
        payment_method = payment_method_id
                        
        order_id = request.data.get('order_id')        
        order = Order.objects.get(id=order_id)        
        billing = None
        print("oorrdderr  ",order, payment_method)
        if order_id and order:                          
            order.payment_method = str(payment_method)            
                        
            account_types = order.account_type.all()            
            total_amount = sum(account_type.price for account_type in account_types)
            order.total_amount = total_amount
            order.save()
            # if order.coupon_applied:
            #     price = order.account_type.price
            #     print("coupon applied", price)                
            # else:
            #     price = order.account_type.price
            #     print("no coupon applied", price)
            #     order.total_amount = price
            #     order.save()
                
            billing_query = BillingDetail.objects.filter(user=request.user)
            if billing_query.exists():
                billing = BillingDetail.objects.get(user=request.user)                                    
            else:            
                billing = BillingDetail.objects.create(user=request.user)                                    
                                
            billing.payment_method = payment_method            
            billing.save()
            print("xxxxxxxxx",  billing.payment_method)
            
            payment_gateway = str(billing.payment_method.lower())
            if payment_gateway == 'paystack': 
                return redirect('store:payment_paystack', order.id)
            elif payment_gateway == 'cryptocurrency':
                return redirect('store:payment_crypto', order.id)
            elif payment_gateway == 'credit-debit-card':
                return redirect('store:payment_card', order.id)
            else:
                return redirect('store:payment_bank', order.id)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

        
        
        
# from users.models import CustomUser  
      

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated      
      
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])  
def paystack_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    amount = order.total_amount

    currency = request.user.currency
    print(order, currency, amount, currency.code)

    # initialize the payment on Paystack
    # get the authorization URL
    paystack_secret_key = 'sk_test_7d62ed19dd419369ae385972349faa54bd7b4edc'
    headers = {'Authorization': f'Bearer {paystack_secret_key}'}
    payload = {
        'amount': int(amount) * 100,  # Paystack API  amount in kobo (1 NGN = 100 kobo)
        'currency': str(currency.code),
        'email': request.user.email,
        'callback_url': request.build_absolute_uri('/payment/callback/'),  #  callback URL to handle the payment verification
    }
    response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=payload)
    print("response!!", response, request)
    if response.status_code == 200:
        authorization_url = response.json()['data']['authorization_url']

        transaction = Transaction.objects.create(
            reference=response.json()['data']['reference'],
            user=request.user,
            order=order,
            status='pending',
            payment_method='paystack',
            amount=amount,
            currency=(currency.code),
        )
        transaction.save()
        print("######## payment 200 ########", response.json()['data'])
        return Response({'authorization_url': authorization_url})
    else:
        print("######## payment !200 ########", response.json())
        return Response({'error': 'Payment initialization failed.'}, status=400)



@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])  
def crypo_payment(request, order_id):
    order = Order.objects.get(id=order_id)             
    amount = order.total_amount        
    currency_id = request.user.currency.id        
    currency = Currency.objects.get(id=currency_id)
    print(order, currency, amount)
                
    response_code = 400
    print("response code:", response_code)
    
    if response_code == 400:            
        transaction = Transaction.objects.create(                
            user=request.user,
            order=order,
            status='canceled',
            payment_method='cryptocurrency',  
            amount=amount,
            currency=(currency.code),                
        )
        transaction.save()                              
        return JsonResponse({'status': 'failure', 'message': 'Payment initialization failed.'})
    else:
        return JsonResponse({'status': 'success'})


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])  
def bank_payment(request, order_id):
        order = Order.objects.get(id=order_id)             
        amount = order.total_amount        
        currency_id = request.user.currency.id        
        currency = Currency.objects.get(id=currency_id)
        print(order, currency, amount)
                
        response = 300
        print("response!!", response)
        if response == 300:            
                        
            transaction = Transaction.objects.create(                
                user=request.user,
                order = order,
                status='pending',
                payment_method='bank',  
                amount=amount,
                currency=(currency.code),                
            )
            transaction.save()
                              
            return JsonResponse({'status': 'failure', 'message': 'Payment initialization failed.'})
        else:
            return JsonResponse({'status': 'success'})


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])  
def card_payment(request, order_id):
        order = Order.objects.get(id=order_id)             
        amount = order.total_amount
        try:
            currency_id = request.user.currency.id
        except:
            currency_id = 3
        currency = Currency.objects.get(id=currency_id)
        print(order, currency, amount)
                
        response = 200
        print("response!!", response)
        if response == 200:            
                        
            transaction = Transaction.objects.create(                
                user=request.user,
                order = order,
                status='completed',
                payment_method='card',  
                amount=amount,
                currency=(currency.code),                
            )
            transaction.save()                              
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Payment initialization failed.'})
    


from django.http.response import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
@csrf_exempt  
def paystack_callback(request):
    if request.method == 'GET':
        reference_id = request.GET.get('reference')
        url = f'https://api.paystack.co/transaction/verify/{reference_id}'
        paystack_secret_key = 'sk_test_7d62ed19dd419369ae385972349faa54bd7b4edc'
        headers = {'Authorization': f'Bearer {paystack_secret_key}'}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()['data']
            # print(data)
            # print(request.GET)
            amount = response.json()['data']['amount'] / 100  
            transaction = Transaction.objects.get(reference=reference_id)
            transaction.status = 'completed'
            transaction.amount = amount            
            transaction.card_last_4_digits = response.json()['data']['authorization']['last4']
            transaction.save()
            print("xxxxxx", transaction.order)
            order = Order.objects.get(id=transaction.order.id)
            order.paid = True
            order.order_stage = 'active'
            order.order_status = 'success'
            order.save()
            print(order)                        
            messages.success(request, 'Payment completed.')
            # return JsonResponse({'status': 'success', 'message': 'Payment completed.'})
            return redirect('http://lasfunding.com/user/dashboard.html')
        else:
            transaction = Transaction.objects.get(reference=reference_id)
            transaction.status = 'canceled'
            transaction.save()            
            print('Transaction verification failed')
            print(response.text)
            # return JsonResponse({'status': 'error', 'message': 'Payment failed.'})
            return redirect('http://lasfunding.com/user/dashboard.html')
                
    else:
        # elif event == 'charge.failed':
        #     reference = request.POST['data']['reference']
        #     transaction = Transaction.objects.get(reference=reference)
        #     transaction.status = 'canceled'
        messages.success(request, 'Payment failed.')  
        # return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
        return redirect('http://lasfunding.com/user/dashboard.html')
    