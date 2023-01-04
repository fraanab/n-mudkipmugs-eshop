from django.shortcuts import render
from .cart import Cart
from django.contrib.auth.decorators import login_required
from product.models import Product
from django.conf import settings
import os
from dotenv import load_dotenv
load_dotenv()

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return render(request, 'cart/partials/menu_cart.html')

def choose_payment(request):
    return render(request, 'cart/choose_payment.html')

def cart(request):
    return render(request, 'cart/cart.html')

def update_cart(request, product_id, action):
    cart = Cart(request)
    if action == 'increment':
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)

    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    if quantity:
        quantity = quantity['quantity']
        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
                'slug': product.slug,
            },
            'total_price': (quantity * product.price) / 100,
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response

@login_required
def checkout_stripe(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    return render(request, 'cart/checkout_stripe.html', {'pub_key': pub_key})

@login_required
def checkout_mp(request):
    return render(request, 'cart/checkout_mp.html', context)

def success(request):
    return render(request, 'cart/success.html')

@login_required
def checkout_paypal(request):
    return render(request, 'cart/checkout_paypal.html')

def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')
