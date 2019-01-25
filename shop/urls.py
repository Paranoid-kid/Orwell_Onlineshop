from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    # path('.well-known/pki-validation/24A3D58590365E71CCF60A9D5B92CF3A.txt', views.cert),
    path('products/', views.product_list, name='product_list'),
    path('<int:catid>-<slug:cat_slug>/<int:id>-<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]
