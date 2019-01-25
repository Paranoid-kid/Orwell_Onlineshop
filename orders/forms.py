from django.forms import ModelForm
from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html
from .models import Order


class MyPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self):
        form_open = u'''<form action="%s" method="post">''' % (self.get_endpoint())
        form_custom = u'''<form action="%s" method="post">'''.format()
        form_close = u'</form>'
        submit_elm = u'''<button class="ui black right floated button" type="submit"><i class="paypal icon"></i>PayPal Checkout</button>'''
        return format_html(form_open + self.as_p() + submit_elm + form_close)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
