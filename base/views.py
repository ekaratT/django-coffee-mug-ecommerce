from django.shortcuts import render
from coffee_mug.models import Categories, Products
from coffee_mug.context_processors import get_cart_counter

def home(request):
    categories = Categories.objects.all()
    products = Products.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'page': 'home',
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'index.html', context)