from django.shortcuts import render, redirect
from product.models import Product, Category
from django.contrib.auth import get_user_model
from order.models import Order, OrderItem
from .models import Contact
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
import re
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import OrderForm
from django.http import HttpResponse

def frontpage(request):
	products = Product.objects.all()
	return render(request, 'core/frontpage.html', {'products': products})
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			user = form.save()

			login(request, user)
			
			return redirect('/')
	else:
		form = SignUpForm()

	return render(request, 'core/signup.html', {'form': form})
def login_old(request):
	return render(request, 'core/login.html')
@login_required
def myaccount(request):
	if request.user.is_superuser:
		# order_model = Order(request)
		User = get_user_model()
		product = Product.objects.all()
		product_count = product.count()
		orders = Order.objects.all()
		order_count = orders.count()
		order_item = OrderItem.objects.all()
		order_item_count = order_item.count()
		customer = User.objects.all()
		customer_count = customer.count() - 1 #the admin is excluded
		mails = Contact.objects.all()
		mails_count = mails.count()
		total_earnt = 0
		for item in order_item:
				total_earnt += item.price
		total_earnt = total_earnt / 100
		
		context = {
			'orders':orders,
			'product': product,
			'product_count': product_count,
			'order_count': order_count,
			'order_item': order_item,
			'order_item_count': order_item_count,
			'customer_count': customer_count,
			'mails': mails,
			'mails_count': mails_count,
			'total_earnt': total_earnt
		}
		return render(request, 'core/admin_dashboard.html', context)
	else:
		return render(request, 'core/myaccount.html')

@login_required
def updateOrder(request, pk):
	if request.user.is_superuser:

		orderid = Order.objects.get(id=pk)
		orderform = OrderForm(instance=orderid)
		
		if request.method == 'POST':
			orderform = OrderForm(request.POST, instance=orderid)
			if orderform.is_valid():
				orderform.save()
				# return redirect('/myaccount/')
				return HttpResponse('<script>window.close()</script>')
			else:
				print('form isnt valid')
				return redirect('/')
		
		context = {
			'orderform': orderform,
		}
		return render(request, 'core/admin_dashboard_form.html', context)
	else:
		return redirect('/')

@login_required
def edit_myaccount(request):
	if request.method == 'POST':
		user = request.user
		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')
		user.email = request.POST.get('email')
		user.username = request.POST.get('username')
		user.save()
		return redirect('myaccount')
	return render(request, 'core/edit_myaccount.html')

def contact(request):
	if request.method == 'POST':
		message = request.POST['message']
		from_email = request.POST['email']
		subject = request.POST['subject']
		contactForm = Contact(message=message, from_email=from_email, subject=subject)
		contactForm.save()
	return render(request, 'core/contact.html')