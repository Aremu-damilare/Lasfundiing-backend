from django.urls import path
from .views import  Logout
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from .views import NewEmailConfirmation    
from .views import verify_email
from . import views


app_name = 'users'

urlpatterns = [
        
    path('register/', RegisterView.as_view(), name='signup'),        
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    # path('is-access-token-valid/', views.TokenValidationView.as_view(), name='is_access_token_valid'),                    
    # path('password-reset/', PasswordResetView.as_view()),      
    path('kyc/', views.KYCListCreateView.as_view(), name='kyc-list-create'),
    path('kyc/<int:pk>/', views.KYCDetailUpdateView.as_view(), name='kyc-detail-update'),
    
    path('withdrawalmethods/', views.WithdrawalMethodList.as_view(), name='withdrawalmethod-list'),
    path('withdrawalmethod/<int:user_id>/', views.WithdrawalMethodDetail.as_view(), name='withdrawalmethod-detail'),
    
    path('withdrawals/', views.WithdrawalList.as_view(), name='withdrawal-list'),
    path('withdrawal/<int:withdrawal_id>/', views.WithdrawalDetail.as_view(), name='withdrawal-detail'),
    
          
    path('account-confirm-email/',  VerifyEmailView.as_view(), name='account_email_verification_sent'),    
    path('resend-email/', NewEmailConfirmation.as_view(), name='resend_email_confirmation'),        
    path('account-email-confirm/<str:key>/', verify_email, name='verify_email'),
]