from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('single-category/<int:category_id>/', views.single_category, name='single-category'),
    path('single-product/<int:product_id>/', views.single_product, name='single-product'),
    path('add-product-review/', views.add_product_review, name='add-product-review'),
    path('add-to-cart/', views.cart_add, name='add-to-cart'),
    path('update-cart/', views.update_cart, name='update-cart'),
    path('remove-cart/', views.cart_remove, name='remove-cart'),

    path('about-us', views.about_us, name='about-us'),
    path('add-cus-comment', views.customer_comment, name='add-cus-comment'),
    path('customer-comments', views.customer_comment_view, name='customer-comments'),
]

