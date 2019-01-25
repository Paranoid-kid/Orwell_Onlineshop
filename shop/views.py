from django.shortcuts import render, get_object_or_404
from .models import Category


def index(request):
    return render(request, 'shop/index.html')


# from django.http import HttpResponse

# def cert(request):
#     content = '98880B42F7F0B93B0876D80F39E054E466241EC1D5E427492E66E99953D0F522\nssl.com\n0951a58e23'
#     return HttpResponse(content, content_type='text/plain')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, catid, cat_slug, id, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product})


# Create your views here.
from shop.models import Product
from shop.serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
