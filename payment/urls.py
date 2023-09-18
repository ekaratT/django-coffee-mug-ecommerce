from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('proceed', views.payment_process, name='proceed'),
    path('checkout/', views.checkout, name='checkout'),
    path('completed/', views.payment_complete, name='completed'),
    path('canceled/', views.payment_cancel, name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='webhook'),
]
