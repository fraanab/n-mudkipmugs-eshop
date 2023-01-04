from django.urls import path

from .views import start_order, paypal_start_order, mercadopago_start_order

urlpatterns = [
    path('checkout_mp/', mercadopago_start_order, name='mercadopago_start_order'),
    path('start_order/', start_order, name='start_order'),
    path('paypal_start_order/', paypal_start_order, name='paypal_start_order')
]