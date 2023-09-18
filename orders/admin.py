from django.contrib import admin
from .models import Order, OrderItem
from account.models import User
from django.utils.safestring import mark_safe


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}"target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_payment.short_description = 'Stripe_payment'

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'state', 'city', 'country', 'pin_code', 'is_paid', order_payment]
    list_filter = ['is_paid', 'created_date', 'updated_date']
    inlines = [OrderItemInline,]

    # @admin.display(description=User)
    # def get_user_detail(self, obj):
    #     user_detail = obj.order_set.all()
    #     return ', '.join([str(item) for item in user_detail])

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
