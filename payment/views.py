from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
import stripe
from django.conf import settings
from orders.models import Order, OrderItem
from account.models import UserProfile
from coffee_mug.cart import Cart
from orders.forms import OrderCreateForm, UnauthenticatedOrderFrom
from django.contrib import messages



# Create stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('completed'))
        cancel_url = request.build_absolute_uri(reverse('canceled'))
        # Stripe checkout session data
        session_data = {
            'client_reference_id': order_id,
            'mode': 'payment',
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # add order items to stripe checkout session
        for item in order_items:
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.get_sub_total() * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.product_name,
                    },
                },
                'quantity': item.quantity
            })
        # Create stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        
        # Redirect to stripe payment form
        return redirect(session.url, code=303)
    context = {'order_items': order_items, 'order': order}
    return render(request, 'payment/process.html', context)

def payment_complete(request):
    order_id = request.session.get('order_id', None)
    context = {'order_id': order_id}
    return render(request, 'payment/completed.html', context)

def payment_cancel(request):
    return render(request, 'payment/canceled.html')

def checkout(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        defualt_values = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': user_profile.address,
            'country': user_profile.country,
            'state': user_profile.state,
            'city': user_profile.city,
            'pin_code': user_profile.pin_code

        }
        if cart.__len__() > 0:
            # Prepopulate form data using the default values above
            form = OrderCreateForm(initial=defualt_values)
            
        else:
            messages.warning(request, 'Your cart is empty.')
            return redirect('products')
    else:
        if cart.__len__() > 0:
            # Prepopulate form data using the default values above
            form = UnauthenticatedOrderFrom()
            
        else:
            messages.warning(request, 'Your cart is empty.')
            return redirect('products')
    context = {
                'cart_total': cart.get_total_price(),
                'grand_total': cart.get_total_plus_vat(),
                'cart_fee': cart.get_fee(),
                'cart_counter': cart.__len__(),
                'cart': cart,
                'form': form,
                'page': 'checkout'
            }
    return render(request, 'payment/checkout.html', context) 




