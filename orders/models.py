from django.db import models
from shop.models import Product
from accounts.models import User
from django.core.validators import MinValueValidator


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    pay_method = models.CharField(max_length=20, null=True)

    buyer_id = models.ForeignKey(User, related_name='user_id', null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=5)
    merchant_email = models.EmailField()
    salt = models.CharField(max_length=64)
    shoppingcart_information = models.CharField(max_length=250)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    digest = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
