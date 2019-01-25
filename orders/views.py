from django.shortcuts import render, HttpResponse, render_to_response, redirect
from .models import OrderItem, Order
from accounts.models import User
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
import json
import logging
import ast
from django.urls import reverse
from .forms import MyPayPalPaymentsForm, OrderForm
from shop.models import Product
from orwell.settings import base
from hashlib import sha256
import secrets
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .alipay_payment import AliPay
from orwell.settings.base import app_private_key_path, alipay_pub_key_path

logging.basicConfig(level=logging.NOTSET)


def order_ship_info(request):
    customer_info_form = OrderForm(request.POST or None)
    if request.method == "POST":
        session = request.session
        print(request.session.keys())
        if '_auth_user_id' in request.session.keys():
            buyer_id = session['_auth_user_id']
            buyer = User.objects.get(pk=buyer_id)
        else:
            buyer = None

        if customer_info_form.is_valid():
            customer_info_form.cleaned_data['']
            # customer_info_form.save()
            return redirect('/order/checkout/')
    context = {
        'customer_info_form': customer_info_form
    }
    return render(request, 'orders/ship_info.html', context)


@requires_csrf_token
def order_create(request):
    if request.method == "POST":
        data = request.POST
        session = request.session
        if '_auth_user_id' in request.session.keys():
            buyer_id = session['_auth_user_id']
            buyer = User.objects.get(pk=buyer_id)
        else:
            buyer = None
        cart_info_json = data.dict()['cart']  # '[{"pid":1,"quantity":3},{"pid":2,"quantity":2}]'
        cart_info = ast.literal_eval(cart_info_json)  # [{'pid': 1, 'quantity': 3}, {'pid': 2, 'quantity': 2}]
        shoppingcart_information = []
        total_price = 0
        for item in cart_info:
            # print('item: {}'.format(item))
            product_name = Product.objects.get(pk=item['pid']).name
            product_price = Product.objects.get(pk=item['pid']).price
            product_quantity = item['quantity']
            item_str = '{}&{}&{}'.format(product_name, product_quantity, product_price)
            shoppingcart_information.append(item_str)
            sub_price = product_price * item['quantity']
            total_price += sub_price

        print('shoppingcart_information: {}'.format(shoppingcart_information))
        shoppingcart_information = '|'.join(shoppingcart_information)
        print('shoppingcart_information final: {}'.format(shoppingcart_information))
        print('total_price: {}'.format(total_price))
        currency = 'HKD'
        email = base.PAYPAL_REVEIVER_EMAIL
        salt = secrets.token_hex(32)

        digest_str = currency + email + (salt + shoppingcart_information) + str(total_price)
        digest = sha256(digest_str.encode('utf-8')).hexdigest()
        print(salt)
        print(digest)
        order = Order(buyer_id=buyer,
                      currency=currency,
                      merchant_email=email,
                      salt=salt,
                      shoppingcart_information=shoppingcart_information,
                      total_price=total_price,
                      digest=digest)
        order.save()
        order_id = order.id
        for item in cart_info:
            pid = item['pid']
            quantity = item['quantity']
            order_item = OrderItem(order=Order.objects.get(pk=order_id),
                                   product=Product.objects.get(pk=pid),
                                   price=Product.objects.get(pk=pid).price,
                                   quantity=quantity)
            order_item.save()
        return_json = {'order_id': order_id, 'digest': digest}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


from decimal import Decimal


@requires_csrf_token
def checkout(request, digest):
    order_id = Order.objects.get(digest=digest).id
    print(order_id)
    order_qs = Order.objects.get(pk=order_id)
    print(order_qs.id)  # invoice
    print(order_qs.total_price)
    print(order_qs)
    print(order_qs.currency)
    print(order_qs)
    args = {}
    host = request.get_host()
    paypal_dict = {
        "cmd": "_cart",
        "upload": '1',
        "business": base.PAYPAL_REVEIVER_EMAIL,
        "custom": order_qs.digest,
        "invoice": "invoice-{}".format(order_qs.id),
        "currency_code": 'HKD',
        "notify_url": "http://{}{}".format(host, reverse('paypal-ipn')),
        "return_url": "http://{}/order/done/".format(host),
        "cancel_return": "http://{}/order/canceled/".format(host),
    }

    order_items_qs = OrderItem.objects.filter(order_id=order_id)
    for i in range(len(order_items_qs)):
        paypal_dict['item_name_{}'.format(i + 1)] = order_items_qs[i].product
        paypal_dict['quantity_{}'.format(i + 1)] = order_items_qs[i].quantity
        paypal_dict['amount_{}'.format(i + 1)] = order_items_qs[i].price
    print(paypal_dict)
    # <QuerySet [<OrderItem: 121>, <OrderItem: 122>]>
    form = MyPayPalPaymentsForm(initial=paypal_dict)
    args['form'] = form
    args['total_price'] = order_qs.total_price
    price_cny = order_qs.total_price * Decimal('0.8')
    alipay = AliPay(
        appid="2016092300579015",
        app_notify_url="https://{}{}".format(host, reverse('alipay')),
        app_private_key_path=app_private_key_path,
        alipay_public_key_path=alipay_pub_key_path,
        debug=True,
        return_url="https://{}/order/done/".format(host)
    )
    url = alipay.direct_pay(
        subject="Orwell Order",
        out_trade_no=order_id,
        total_amount=price_cny,
        return_url="https://{}/order/done/".format(host),
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    args['alipay_url'] = re_url
    args['price_cny'] = price_cny
    return render(request, 'orders/orders.html', args)


@csrf_exempt
def paypal_return(request):
    args = {'post': request.POST, 'get': request.GET}
    return render_to_response('orders/paypal_return.html', args)


def paypal_cancel(request):
    args = {'post': request.POST, 'get': request.GET}
    return render_to_response('orders/paypal_cancel.html', args)


@login_required
def purchase_history(request):
    session = request.session
    context = {}
    if '_auth_user_id' in request.session.keys():
        buyer_id = session['_auth_user_id']
        order_qs = Order.objects.filter(buyer_id=buyer_id)
        context['order_qs'] = order_qs
    return render(request, 'orders/profile.html', context)


from rest_framework.views import APIView
from rest_framework.response import Response


class AlipayView(APIView):

    def post(self, request):
        host = request.get_host()
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)
        alipay = AliPay(
            appid="2016092300579015",
            app_notify_url="https://{}{}".format(host, reverse('alipay')),
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_pub_key_path,
            debug=True,
            return_url="https://secure.s79.ierg4210.ie.cuhk.edu.hk/order/done/"
        )
        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_id = processed_dict.get('out_trade_no', None)
            order = Order.objects.get(pk=order_id)
            order.paid = True
            order.pay_method = 'Alipay'
            order.save()
            return Response('success')
