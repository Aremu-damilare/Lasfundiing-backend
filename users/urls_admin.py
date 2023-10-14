from django.urls import path
from .views_admin import CustomLoginView

urlpatterns = [    
    path('custom-login/', CustomLoginView.as_view(), name='rest_login'),    
]
