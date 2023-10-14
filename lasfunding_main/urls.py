"""lasfunding_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.views import PasswordChangeView


urlpatterns = [
    path('admin/standard/', admin.site.urls),    
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    
    path('', include('users.urls')),    
    
    path('admin/', include('users.urls_admin')),    
    path('admin/store/', include('store.urls_admin')),    
    
    path('', include('store.urls')),
    path('', include('ticket.urls'))    
    # path('', Home, name='home'),
    # path('dashboard/', login_required(Dashboard.as_view()), name='dashboard'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)