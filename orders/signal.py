from . import models
from paypal.standard.models import ST_PP_COMPLETED, PayPalStandardBase
from paypal.standard.ipn.signals import valid_ipn_received
from orwell.settings import base
from hashlib import sha256
import logging

logging.basicConfig(level=logging.DEBUG)


def payment_notfication(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        ipn_obj.verify()
        order_id = ipn_obj.invoice.split('-')[-1]
        print(order_id)
        order = models.Order.objects.get(pk=order_id)
        if ipn_obj.receiver_email != base.PAYPAL_REVEIVER_EMAIL:
            # Not a valid payment
            return
        if ipn_obj.custom != order.digest:
            # Not a valid payment
            return
        if ipn_obj.mc_gross != order.total_price or ipn_obj.mc_currency != order.currency:
            # Not a valid payment
            return
        # if PayPalStandardBase.objects.filter(txn_id=ipn_obj.txn_id) is not None:
            # Not a valid payment
            # Duplicate txn_id.
            # return
        if ipn_obj.txn_type != 'cart':
            # Not a valid payment
            return
        # order.paid = True
        # order.pay_method = 'PayPal'
        # order.save()
        # mc_gross = 3468.00 &
        # invoice = invoice - 5 &
        # business = tianchen.chen - facilitator % 40
        # protonmail.com &
        # num_cart_items = 2 &
        # payment_status = Completed &
        # custom = 2
        # fe171a722477245dcf08a1d761e9a9ee9efbc2e74e1e799ce24191095464468 &
        # item_name1 = ChromeBook &
        # item_name2 = MacBook &
        # quantity1 = 1 &
        # quantity2 = 2 &
        # mc_gross_1 = 1000.00 &
        # mc_gross_2 = 2468.00 &
        # mc_currency = HKD &
        shoppingcart_information = []
        currency = ipn_obj.mc_currency
        email = ipn_obj.receiver_email
        salt = order.salt
        for i in range(ipn_obj.num_cart_items):
            product_name = ipn_obj.item_name[i]
            product_price = ipn_obj.mc_gross[i]
            product_quantity = ipn_obj.quantity[i]
            item_str = '{}&{}&{}'.format(product_name, product_quantity, product_price)
            shoppingcart_information.append(item_str)
        total_price = ipn_obj.mc_gross
        shoppingcart_information = '|'.join(shoppingcart_information)

        digest_str = currency + email + (salt + shoppingcart_information) + str(total_price)
        digest = sha256(digest_str.encode('utf-8')).hexdigest()
        logging.INFO('currency : {}'.format(currency))
        logging.INFO('email : {}'.format(email))
        logging.INFO('salt : {}'.format(salt))
        logging.INFO('ipn_obj.cart : {}'.format(ipn_obj.cart))
        logging.INFO('digest_str : {}'.format(digest_str))
        logging.INFO('digest : {}'.format(digest))
        if digest != order.digest:
            # Not a valid payment
            return
        order.paid = True
        order.pay_method = 'PayPal'
        order.save()


valid_ipn_received.connect(payment_notfication)
