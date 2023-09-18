from decimal import Decimal
from django.db import models
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, DecimalValidator

# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)
    category_picture = models.ImageField(upload_to='category_images', blank=True, null=True, default='category_images/mug-set2.jpg')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        ordering = ['-created_date']


class Products(models.Model):
    product_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_picture = models.ImageField(upload_to='product_images', blank=True, null=True, default='product_images/mug-set1.jpg')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_total_rating(self):
        return sum(review.rating for review in self.reviews.all())
    
    def get_average_rating(self):
        return self.get_total_rating() / len(self.reviews.all()) if len(self.reviews.all()) > 0 else 0
    
    class Meta:
        ordering = ['-created_date']
        

class ProductReview(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, validators=(MinValueValidator(0), MaxValueValidator(5)))
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
    
    

class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'wishlists'
        ordering = ['-created_date']

    def __str__(self):
        return str(self.products)
    

class CustomerComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.comment





    

