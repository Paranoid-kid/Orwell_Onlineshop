"""Orwell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, register_converter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from shop import views
from accounts import views as account_view
from django.contrib.auth import views as auth_views
from orders import views as order_view
from . import converters
from rest_framework.authtoken import views as drf_auth_views
from orders.views import AlipayView

router = DefaultRouter()
router.register(r'product', views.ProductViewSet)
register_converter(converters.DigestConverter, 'digest')

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('api-token-auth/', drf_auth_views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('e2959d87fb678ce93563e71a18ec54d135531e9a26cc55c5c3b9e22c6f83b609/', include('paypal.standard.ipn.urls'),
         name='paypal-ipn'),
    path('alipay/notify/', AlipayView.as_view(), name='alipay'),
    path('order/ship_info/', order_view.order_ship_info, name='order_ship_info'),
    path('order/checkout/', order_view.order_create, name='order_create'),
    path('order/purchase_history/', order_view.purchase_history, name='purchase_history'),
    path('order/checkout/<digest:digest>/', order_view.checkout, name='order_pay'),
    path('order/done/', order_view.paypal_return),
    path('order/canceled/', order_view.paypal_cancel),
    path('signup/', account_view.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', account_view.PasswordChange.as_view(), name='password_change'),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
