from .cart import Cart

# This function need to be registered in settings.py

def get_cart_counter(request):
    cart_count = Cart(request).__len__()
    # return {'cart': Cart(request)}
    return {'cart_count': cart_count}

def get_cart_detail(request):
    return {'cart': Cart(request)}