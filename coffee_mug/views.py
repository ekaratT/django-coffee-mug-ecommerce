from django.shortcuts import render, get_object_or_404
from . models import Categories, Products, CustomerComment, ProductReview
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

# Get cart data from session.
from .context_processors import get_cart_counter

from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from .cart import Cart

# Create your views here.

def categories(request):
    # categories = Categories.objects.all()
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    categories = Categories.objects.filter(
        Q(category_name__icontains=search_query)
    )
    page = request.GET.get('page')
    paginator = Paginator(categories, 3) # 3 product per page
    try:
        category_obj = paginator.page(page)
    except PageNotAnInteger:
        # IF page number is not an integer then return the first page.
        # This simply means when the user go to the product page.
        page = 1
        category_obj = paginator.page(page)
    except EmptyPage:
        # If the requested page is out of range, then return the last page.
        page = paginator.num_pages
        category_obj = paginator.page(page)
    context = {
        'category_obj': category_obj,
        'paginator': paginator,
        'search_include': True,
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'coffee_mug/categories.html', context)

def products(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    categories = Categories.objects.filter(category_name__iexact=search_query)
    products = Products.objects.filter(
        Q(product_name__icontains=search_query) | 
        Q(description__icontains=search_query) |
        Q(category__in=categories))
    page = request.GET.get('page')
    paginator = Paginator(products, 6) # 3 product per page
    try:
        pro_obj = paginator.page(page)
    except PageNotAnInteger:
        # IF page number is not an integer then return the first page.
        # This simply means when the user go to the product page.
        page = 1
        pro_obj = paginator.page(page)
    except EmptyPage:
        # If the requested page is out of range, then return the last page.
        page = paginator.num_pages
        pro_obj = paginator.page(page)
    context = {
        'pro_obj': pro_obj,
        'paginator': paginator,
        'search_query': search_query,
        'search_include': True,
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'coffee_mug/products.html', context)

def single_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    products = Products.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
        'search_include': False,
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'coffee_mug/category.html', context)

def single_product(request, product_id):
    product = Products.objects.get(id=product_id)
    prod_reviews = ProductReview.objects.filter(product=product)
    related_products = Products.objects.filter(category=product.category).exclude(id=product_id)
    context = {
        'product': product, 
        'prod_reviews': prod_reviews,
        'related_products': related_products,
        'cart_counter': get_cart_counter(request)['cart_count']
        }
    return render(request, 'coffee_mug/product.html', context)


@require_POST
def cart_add(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('qty'))
    override = request.POST.get('override')
    if override == 'false':
        override = False
    else:
        # Changing cart item qty on cart page should override qty.
        override = True

    cart.add(
        product_id=product_id,
        quantity=product_qty,
        override_quantity=override
    )
    return JsonResponse({
        'status': 'success',
        'message': 'Product is added to cart successfully.',
        'cart_counter': get_cart_counter(request),
        'cart_total_price': cart.get_total_price()
    })

@require_POST                 
def update_cart(request):
    cart = Cart(request)
    prod_id = int(request.POST.get('product_id'))
    prod_qty = int(request.POST.get('product_qty'))
    override = request.POST.get('override')
    if override == 'false':
        override = False
    else:
        # Changing cart item qty on cart page should override qty.
        override = True
    cart.add(
        product_id=prod_id,
        quantity=prod_qty,
        override_quantity=override
    )
    return JsonResponse({
        'status': 'success',
        'message': 'Cart is updated successfully.',
        'cart_counter': get_cart_counter(request),
        'cart_total': cart.get_total_price(),
        'cart_fee': cart.get_fee(),
        'grand_total': cart.get_total_plus_vat()
    })

@require_POST
def cart_remove(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    return JsonResponse({
        'status': 'success',
        'message': 'Cart is removed successfully.',
        'cart_counter': cart.__len__(),
        'cart_total': cart.get_total_price(),
        'grand_total': cart.get_total_plus_vat(),
        'cart_fee': cart.get_fee(),
    })

def customer_comment(request):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        email = request.user.email if request.user.is_authenticated else request.POST.get('email')
        comment = request.POST.get('comment')
        CustomerComment.objects.create(user=user, comment=comment, email=email)
        messages.success(request, 'Your comment is submitted.')
        return JsonResponse({'status': 'success', 'message': 'Your comment was sent successfully.'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    
def customer_comment_view(request):
    cus_comments = CustomerComment.objects.all()
    context = {
        'cus_comments': cus_comments,
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'coffee_mug/cus_comment.html', context)

def about_us(request):
    return render(request, 'coffee_mug/about_us.html')

def add_product_review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            pro_id = request.POST.get('product_id')
            product = Products.objects.get(id=pro_id)
            user = request.user
            ProductReview.objects.create(user=user, product=product, rating=rating, comment=comment)
            messages.success(request, 'Your comment has been submitted successfully.')
            return JsonResponse({'status': 'success', 'message': 'Comment added successfully.'})
        return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    return JsonResponse({'status': 'login_required', 'message': 'Please login to review product.'})


       