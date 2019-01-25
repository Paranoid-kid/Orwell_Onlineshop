from rest_framework import serializers
from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('pid', 'category', 'name', 'price')
