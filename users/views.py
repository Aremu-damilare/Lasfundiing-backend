from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import JsonResponse, HttpResponseRedirect
from django.urls import reverse
# from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import Order, AccountType, Platform, PaymentMethod, Coupon, BillingDetail, Transaction
from dj_rest_auth.registration.views import VerifyEmailView
from django.shortcuts import redirect
from .models import Currency
from django.http import HttpRequest
from rest_framework.test import APIClient
from users.forms import BillingForm

User = get_user_model()



class VerifyEmailSent(TemplateView):
    template_name = "verify.html"

    
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
from .serializers import LoginSerializer





class Logout(LogoutView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))



class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    

class NewEmailConfirmation(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response({'message': 'This email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
            except APIException:
                return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)




from django.shortcuts import redirect

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
        return redirect('http://lasfunding.com/')
    else:
        # Handle error (e.g. display error message)
        print("Returning home..........")
        return redirect('http://lasfunding.com/')

        



    
    
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import CustomerUser

@login_required
def UpdateProfile(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        current_password = request.POST['current-password']
        new_password1 = request.POST['new-password1']
        new_password2 = request.POST['new-password2']
        display_name = request.POST['display-name']
        currency_id = request.POST['currency']
        
        user = request.user
        currency = Currency.objects.get(id=currency_id)
        user.currency = currency
        user.first_name = first_name
        user.last_name = last_name

        
        user.display_name = display_name
        user.save()
        
        if current_password and new_password1 and new_password2:
            # Verify the current password
            if user.check_password(current_password):
                # Check if the new passwords match
                if new_password1 == new_password2:
                    # Update the password
                    user.set_password(new_password1)
                    user.save()
                    # Update the session authentication hash to avoid log out
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password has been updated successfully.')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Current password is incorrect.')
        
        user.save()
        messages.success(request, 'Profile has been updated successfully.')
        return redirect('users:update_profile')  
    else:
        currencies = Currency.objects.all()
        context = {'currencies': currencies}
        return render(request, 'profile.html' , context)  



from datetime import date
import requests


# def PaymentView(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)                        
#     context = {'order': order}
#     return render(request, 'payment.html', context)
    

def paystack_payment(request, order_id):
    # if request.method == 'POST':        
        order = Order.objects.get(id=order_id)             
        amount = order.total_amount
        try:
            currency_id = request.user.currency.id
        except:
            currency_id = 3
        currency = Currency.objects.get(id=currency_id)
        print(order, currency, amount)
        
        # initialize the payment on Paystack 
        # get the authorization URL
        paystack_secret_key = 'sk_test_7d62ed19dd419369ae385972349faa54bd7b4edc'
        headers = {'Authorization': f'Bearer {paystack_secret_key}'}
        payload = {
            'amount': int(amount) * 100,  # Paystack API  amount in kobo (1 NGN = 100 kobo)
            'currency': currency.code,
            'email': request.user.email,
            'callback_url': request.build_absolute_uri('/payment/callback/'),  #  callback URL to handle the payment verification
        }
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=payload)
        print("response!!", response)
        if response.status_code == 200:
            authorization_url = response.json()['data']['authorization_url']
                        
            transaction = Transaction.objects.create(
                reference = response.json()['data']['reference'],
                user=request.user,
                order = order,
                status='pending',
                payment_method='paystack',  
                amount=amount,
                currency=(currency.code),                
            )
            transaction.save()
            print("######## payment 200 ########",  response.json()['data'])                        
            return redirect(authorization_url)
        else:
            messages.error(request, 'Payment initialization failed.')
            return redirect("/checkout/?order_id={}".format(order_id))



def crypo_payment(request, order_id):
        order = Order.objects.get(id=order_id)             
        amount = order.total_amount
        try:
            currency_id = request.user.currency.id
        except:
            currency_id = 3
        currency = Currency.objects.get(id=currency_id)
        print(order, currency, amount)
                
        response = 400
        print("response!!", response)
        if response == 400:            
                        
            transaction = Transaction.objects.create(                
                user=request.user,
                order = order,
                status='canceled',
                payment_method='cryptocurrency',  
                amount=amount,
                currency=(currency.code),                
            )
            transaction.save()
                              
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Payment initialization failed.')
            return redirect("/checkout/?order_id={}".format(order_id))



def card_payment(request, order_id):
        order = Order.objects.get(id=order_id)             
        amount = order.total_amount
        try:
            currency_id = request.user.currency.id
        except:
            currency_id = 3
        currency = Currency.objects.get(id=currency_id)
        print(order, currency, amount)
                
        response = 400
        print("response!!", response)
        if response == 400:            
                        
            transaction = Transaction.objects.create(                
                user=request.user,
                order = order,
                status='canceled',
                payment_method='card',  
                amount=amount,
                currency=(currency.code),                
            )
            transaction.save()
                              
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Payment initialization failed.')
            return redirect("/checkout/?order_id={}".format(order_id))
    


    
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
            return HttpResponseRedirect(reverse('users:dashboard'))
        else:
            transaction = Transaction.objects.get(reference=reference_id)
            transaction.status = 'canceled'
            transaction.save()            
            print('Transaction verification failed')
            print(response.text)
                
    else:
        # elif event == 'charge.failed':
        #     reference = request.POST['data']['reference']
        #     transaction = Transaction.objects.get(reference=reference)
        #     transaction.status = 'canceled'
        messages.success(request, 'Payment failed.')  
        return HttpResponseBadRequest('Invalid request method')
    