"""
URL configuration for ecommerce_catalogg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import JsonResponse
from catalog.admin import customer_admin
from django.contrib.auth import views as auth_views

def home_view(request):
    """Home page with API information"""
    return JsonResponse({
        'message': 'Welcome to E-commerce Product Catalog System',
        'version': '1.0.0',
        'status': 'running',
        'interfaces': {
            'customer_portal': '/customer/',
            'admin_panel': '/admin/',
            'api_endpoints': '/api/',
        },
        'customer_features': {
            'browse_products': '/customer/catalog/',
            'shopping_cart': '/customer/cart/',
            'search_and_filter': '/customer/catalog/?search=iphone',
        },
        'api_endpoints': {
            'api_info': '/api/',
            'categories': '/api/categories/',
            'products': '/api/products/',
            'variants': '/api/variants/',
            'cart': '/api/cart/',
        },
        'test_credentials': {
            'admin': 'admin / admin123',
            'user': 'testuser / testpass123'
        }
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('customer/', include('catalog.customer_urls')), # Customer portal
    path('customer-admin/', customer_admin.urls), # Admin customer portal
    path('api/', include('catalog.urls')),
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)