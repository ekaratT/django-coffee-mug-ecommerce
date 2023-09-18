from decimal import Decimal
from django.conf import settings
from .models import Products

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product_id, quantity, override_quantity=False):
        """
        Add a product to the cart or update its qty.
        """
        product = Products.objects.get(id=product_id)
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        """
        Mark session as modified to make sure it gets saved.
        """
        self.session.modified = True

    
    def remove(self, product):
        """
        Remove product from cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in cart and get products from DB.
        """
        product_ids = self.cart.keys()
        # Get product objects then add to the cart.
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_fee(self):
        if self.get_total_price() == 0:
            return 0
        # Vat 7%
        return (self.get_total_price() / 100) * 7
    
    def get_total_plus_vat(self):
        if self.get_total_price() == 0:
            return 0
        return self.get_total_price() + self.get_fee()
    

    def clear(self):
        # Remove cart from session.
        del self.session[settings.CART_SESSION_ID]
        self.save()
