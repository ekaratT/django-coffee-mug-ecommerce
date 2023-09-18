from django.shortcuts import render
from django.urls import reverse
from orders.models import Order, OrderItem
from coffee_mug.cart import Cart
from django.http import JsonResponse
from orders.forms import OrderCreateForm
from django.shortcuts import render, redirect
from . import tasks


def create_order(request):
    cart = Cart(request)
    order = Order()
    if request.method == 'POST' and cart.__len__() > 0:
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order.user = request.user if request.user.is_authenticated else None
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.email = form.cleaned_data['email']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.country = form.cleaned_data['country']
            order.pin_code = form.cleaned_data['pin_code']
            order.session_key = request.session.session_key
            order.payment_method = 'stripe'
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            # Launch asynchronous task
            tasks.order_created.delay(order.id)
            # Set the order in session
            request.session['order_id'] = order.id
            return redirect(reverse('proceed'))
            
        else:
            # This will show the error
            form = OrderCreateForm()
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})