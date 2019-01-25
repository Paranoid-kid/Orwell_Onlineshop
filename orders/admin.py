from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer_id', 'total_price',
                    'paid', 'pay_method', 'created', 'updated', 'digest']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
