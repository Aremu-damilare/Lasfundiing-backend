from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'store'

urlpatterns = [    
    path('account-types/', views.AccountTypeList.as_view(), name='account_types_list'),
    path('transactions/', views.TransactionList.as_view(), name='transaction_list'),
    path('platforms/', views.PlatformsList.as_view(), name='platform'),
    path('orders/', views.OrdersHistoryList.as_view(), name='orders_history_list'),
    path('user/', views.UserDetails.as_view(), name='orders_history_list'),
    path('order/<int:order_id>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('billing/', views.BillingCreateUpdateView.as_view(), name='billing-create-update'),
    
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
    
    # path('order/<int:pk>/', login_required(views.OrderHistoryDetail), name='order_history_detail'),

    # path('choose_platform/<int:account_type_id>/', views.ChoosePlatform, name='choose_platform'),
    # path('order_creation_detail/<int:order_id>/', views.OrderCreationDetail, name='order_creation_detail'),
    
    path('coupon-check/', views.ValidateCoupon, name='validate_coupon'),
    path('checkout/', views.CheckOutAPIView.as_view(), name='checkout'),
    # path('payment/<int:order_id>/', PaymentView, name='payment'),
    path('payment/<int:order_id>/', views.paystack_payment, name='payment_paystack'),    
    path('payment/crypto/<int:order_id>/', views.crypo_payment, name='payment_crypto'),
    path('payment/card/<int:order_id>/', views.card_payment, name='payment_card'),
    path('payment/bank/<int:order_id>/', views.bank_payment, name='payment_bank'),
    
    path('payment/callback/', views.paystack_callback, name='paystack_callback'),
    
]