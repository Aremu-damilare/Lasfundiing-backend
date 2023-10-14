from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'store'

urlpatterns = [    
    path('account-types/', views.AccountTypeList.as_view(), name='account_types_list'),
    path('check-account-type/<str:path>/', views.CheckAccountType.as_view(), name='check-accocunt-type'),
    path('transactions/', views.TransactionList.as_view(), name='transaction_list'),
    path('platforms/', views.PlatformsList.as_view(), name='platform'),
    path('orders/', views.OrdersHistoryList.as_view(), name='orders_history_list'),
    path('user/', views.UserDetails.as_view(), name='orders_history_list'),
    path('order/<str:order_id>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('update-order-proof/<str:order_id>/', views.PaymentProofUploadAPIView.as_view(), name='order-detail'),
    
    
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
    
    # path('order/<int:pk>/', login_required(views.OrderHistoryDetail), name='order_history_detail'),

    # path('choose_platform/<int:account_type_id>/', views.ChoosePlatform, name='choose_platform'),
    # path('order_creation_detail/<int:order_id>/', views.OrderCreationDetail, name='order_creation_detail'),
    
    path('coupon-check/', views.ValidateCoupon, name='validate_coupon'),   
    
]