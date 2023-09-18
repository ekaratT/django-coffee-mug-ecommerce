from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name="register-user"),
    path('activate-account/<uidb64>/<token>/', views.activate_account, name="activate-account"),
    path('user-profile/', views.my_account, name="user-profile"),
    path('user-profile-edit/', views.edit_profile, name='user-profile-edit'),
    path('user-login/', views.user_login, name="user-login"),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('change-password/', views.change_password, name='change-password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset-password-validate'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),

    path('add-product/', views.add_product, name='add-product'),
    path('add-category/', views.add_category, name='add-category'),
    path('my-cart/', views.cart_detail, name='my-cart'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
]
