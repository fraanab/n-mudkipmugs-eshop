from .models import Order, OrderItem
from product.models import Product
from cart.cart import Cart
from order.models import Order, OrderItem
import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import mercadopago
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

load_dotenv()

mpat = os.getenv('MPAT')
sdk = mercadopago.SDK(mpat)


@login_required
def get_preference(request):
  product = Product(request)
  cart = Cart(request)
  total_price = 0
  for item in cart:
    product = item['product']
    total_price += (product.price * int(item['quantity']) / 100) * 320
    preference_data = {
      "items": [
        {
          "title": product.name,
          "quantity": item['quantity'],
          "unit_price": total_price
        },
      ]
    }
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
  return JsonResponse(preference)


@login_required
def mercadopago_start_order(request):
  cart = Cart(request)
  total_price = 0
  for item in cart:
    product = item['product']
    total_price += (product.price * int(item['quantity']) / 100) * 320
  if request.method == 'POST':
    user = request.user
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    address = request.POST['address']
    zipcode = request.POST['zipcode']
    place = request.POST['place']
    phone = request.POST['phone']
    paid = True
    paid_amount = total_price
    order = Order(user=user,
                  first_name=first_name,
                  last_name=last_name,
                  email=email,
                  address=address,
                  zipcode=zipcode,
                  place=place,
                  phone=phone,
                  paid=paid,
                  paid_amount=paid_amount)
    order.save()

    for item in cart:
      product = item['product']
      quantity = int(item['quantity'])
      price = product.price * quantity
      new_item = OrderItem(order=order,
                           product=product,
                           price=price,
                           quantity=quantity)
      new_item.save()

# return redirect('')

  mppk = os.getenv('MPPK')
  context = {
    'mppk': mppk,
  }
  return render(request, 'cart/checkout_mp.html', context)


@login_required
def paypal_start_order(request):
  cart = Cart(request)
  total_price = 0
  for item in cart:
    product = item['product']
    # total_price += product.price * int(item['quantity'])
    total_price += (product.price * int(item['quantity']) / 100)

  if request.method == 'POST':
    user = request.user
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    address = request.POST['address']
    zipcode = request.POST['zipcode']
    place = request.POST['place']
    phone = request.POST['phone']
    paid = True
    paid_amount = total_price

    order = Order(user=user,
                  first_name=first_name,
                  last_name=last_name,
                  email=email,
                  address=address,
                  zipcode=zipcode,
                  place=place,
                  phone=phone,
                  paid=paid,
                  paid_amount=paid_amount)
    order.save()

    for item in cart:
      product = item['product']
      quantity = int(item['quantity'])
      price = product.price * quantity
      new_item = OrderItem(order=order,
                           product=product,
                           price=price,
                           quantity=quantity)
      new_item.save()

  return render(request, 'cart/checkout_paypal.html', {})


@login_required
def start_order(request):
  cart = Cart(request)
  data = json.loads(request.body)
  total_price = 0

  items = []

  for item in cart:
    product = item['product']
    total_price += (product.price * int(item['quantity']) / 100)

    items.append({
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': product.name,
        },
        'unit_amount': product.price,
      },
      'quantity': item['quantity']
    })

  stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=items,
    mode='payment',
    success_url='http://127.0.0.1:8000/cart/success/',
    cancel_url='http://127.0.0.1:8000/cart/')
  payment_intent = session.payment_intent

  order = Order.objects.create(
    user=request.user,
    first_name=data['first_name'],
    last_name=data['last_name'],
    email=data['email'],
    phone=data['address'],
    address=data['zipcode'],
    zipcode=data['place'],
    place=data['phone'],
    # payment_intent=payment_intent,
    # paid_amount=total_price,
    # paid=True
  )
  order.payment_intent = payment_intent
  order.paid_amount = total_price
  order.paid = True
  order.save()

  for item in cart:
    product = item['product']
    quantity = int(item['quantity'])
    price = product.price * quantity
    item = OrderItem.objects.create(order=order,
                                    product=product,
                                    price=price,
                                    quantity=quantity)

  # cart.clear()

  return JsonResponse({'session': session, 'order': payment_intent})
