from django.contrib import admin
from .models import Categories, Products, WishList, ProductReview, CustomerComment

# Register your models here.

class CustomerCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_date']


class ProductReviewAdmid(admin.ModelAdmin):
    list_display = ['user', 'rating', 'comment', 'created_date']
    


admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(WishList)
admin.site.register(ProductReview, ProductReviewAdmid)
admin.site.register(CustomerComment, CustomerCommentAdmin)
