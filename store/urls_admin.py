
# urls.py
from django.urls import path
from .views_admin import AccountTypeViewSet, TransactionList, OrderListCreateView, OrderDetailView

urlpatterns = [
    path('create/', AccountTypeViewSet.as_view({'post': 'create'}), name='create-account-type'),
    path('transactions/', TransactionList.as_view(), name='transaction_list'),
    path('list/', AccountTypeViewSet.as_view({'get': 'list'}), name='list-account-types'),
    path('delete/<int:pk>/', AccountTypeViewSet.as_view({'delete': 'destroy'}), name='delete-account-type'),
    
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]