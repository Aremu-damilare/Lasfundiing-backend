from django.urls import path, include, re_path
from .views import  VerifyEmailSent, Logout,  CustomRegisterView
    # OrdersHistoryList,    OrderHistoryDetail
# from dj_rest_auth.registration.views import RegisterView
from . import views
from dj_rest_auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
# from dj_rest_auth.registration.views import VerifyEmailView



from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView
from .views import NewEmailConfirmation
    #ChoosePlatform, CheckOut
from .views import verify_email
    # CreateOrder, OrderCreationDetail, ValidateCoupon

app_name = 'users'

urlpatterns = [
    
    path('verify/', VerifyEmailSent.as_view(), name='verify-email'),
    # path('register/', CustomRegisterView.as_view(), name='signup'),    
    path('register/', RegisterView.as_view(), name='signup'),    
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    # path('login/', Login.as_view(), name='login'),
    # path('dashboard/', login_required(Dashboard.as_view()), name='dashboard'),    
    # path('order/<int:pk>/', login_required(OrderHistoryDetail), name='order_history_detail'),
    path('logout/', Logout.as_view(), name='logout'),
    # path('is-access-token-valid/', views.TokenValidationView.as_view(), name='is_access_token_valid'),
    
    # path('create_order/<int:account_type_id>/', CreateOrder, name='create_order'),
    # path('choose_platform/<int:account_type_id>/', ChoosePlatform, name='choose_platform'),
    # path('order_creation_detail/<int:order_id>/', OrderCreationDetail, name='order_creation_detail'),
    
    # path('coupon-check/', ValidateCoupon, name='validate_coupon'),
    # path('checkout/', CheckOut, name='checkout'),
    # # path('payment/<int:order_id>/', PaymentView, name='payment'),
    # path('payment/<int:order_id>/', views.paystack_payment, name='payment'),    
    # path('payment/crypto/<int:order_id>/', views.crypo_payment, name='payment_crypto'),
    # path('payment/card/<int:order_id>/', views.card_payment, name='payment_card'),
    
    # path('payment/callback/', views.paystack_callback, name='paystack_callback'),
    
    path('update-profile/', views.UpdateProfile, name='update_profile'),
    
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('auth/registration/account-email-verification-sent/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # path('auth/registration/account-confirm-email/<str:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),    
    # path('test-email/', test_email, name='test_email'),
    
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',  VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('resend-email/', NewEmailConfirmation.as_view(), name='resend_email_confirmation'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  
    
     path('account-email-confirm/<str:key>/', verify_email, name='verify_email'),
    ]
    