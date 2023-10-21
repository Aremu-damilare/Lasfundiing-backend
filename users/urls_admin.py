from django.urls import path
from .views_admin import CustomLoginView, UserListCreateView, UserDetailView, WithdrawalListCreateView, WithdrawalDetailView, \
    KYCListCreateView, KYCDetailView, TotalCountAPIView


urlpatterns = [    
    path('login/', CustomLoginView.as_view(), name='rest_login'),   
     
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    path('withdrawals/', WithdrawalListCreateView.as_view(), name='withdrawal-list-create'),
    path('withdrawal/<int:pk>/', WithdrawalDetailView.as_view(), name='withdrawal-detail'),
    
    path('total_count/', TotalCountAPIView.as_view(), name='total-count-api'),
    
    path('kycs/', KYCListCreateView.as_view(), name='kyc-list-create'),
    path('kyc/<int:pk>/', KYCDetailView.as_view(), name='kyc-detail'),
]
