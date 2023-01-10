from django.urls import path
from .views import cart, checkout_mp, checkout_stripe, checkout_paypal, success, add_to_cart, update_cart, choose_payment, hx_menu_cart, hx_cart_total
from order.views import get_preference, mercadopago_start_order
# from product.views import product

urlpatterns = [
    path('', cart, name='cart'),
    path('choose_payment/', choose_payment, name="choose_payment"),
    path('checkout_mp/mppreference/', get_preference, name='get_preference'),
    # path('checkout_mp/', mercadopago_start_order, name='mercadopago_start_order'),
    path('checkout_stripe/', checkout_stripe, name='checkout_stripe'),
    path('checkout_paypal/', checkout_paypal, name='checkout_paypal'),
    path('success/', success, name='success'),

    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/<str:action>/', update_cart, name='update_cart'),

    path('hx_menu_cart/', hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total/', hx_cart_total, name='hx_cart_total'),
]