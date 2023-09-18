from django.db import models

# Create your models here.
from account.models import User
from coffee_mug.models import Products
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.conf import settings
from django.contrib.sessions.models import Session


class Order(models.Model):
    # The shipping address could be different from user profile address.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    session_key = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return str(self.id)
    
    def get_sub_total(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_fee(self):
        return sum(item.get_fee() for item in self.items.all())
    
    def get_grand_total(self):
        return sum(item.item_grand_total() for item in self.items.all())
    
    def get_stripe_url(self):
        if not self.stripe_id:
            # No payment
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # stripe path for test payments
            path = '/test/'
        else:
            # This is the path for real payment
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    
    def get_fee(self):
        return (self.get_cost() / 100) * 7
    
    def get_sub_total(self):
        return self.price + (self.price / 100) * 7
    
    def item_grand_total(self):
        return self.get_cost() + self.get_fee()
    

    

