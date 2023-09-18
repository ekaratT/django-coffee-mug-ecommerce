from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from . utils import send_email_notification
from .decorators import check_role_admin, check_role_customer
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from coffee_mug.cart import Cart
from coffee_mug.context_processors import get_cart_counter
from django.db.models import Q


from . forms import (
    CreateuserForm,
    CategoryForm,
    ProductForm,
    UserProfileForm,
    UserForm
)
from . models import User, UserProfile
from coffee_mug.models import Products, WishList, Categories
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm

# Import task
from orders import tasks


def register_user(request):
    # There are 2 way of creating user
    # 1.Using CreateuserForm
    # 2.Using create_user method from MyUser model
    form = CreateuserForm()
    if request.method == 'POST':
        form = CreateuserForm(request.POST)
        if form.is_valid():
            # 1.Using CreateuserForm
            # Getting the password from the model form.
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user = form.save(commit=False)
            # Hashing password.
            user.set_password(password)
            # From Myuser model choice
            user.role = User.CUSTOMER
            user.save()
            # Send the notification after account is created.
            # User need to click link in email to activate account.
            mail_subject = 'Activate your account'
            template = 'account/emails/acc_verification_mail.html'
            send_email_notification(request, user, mail_subject, template)
            messages.success(request,'Your account has been registered successfully.')
            return redirect('user-profile')

            # 2.Using create_user method from MyUser model
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # password = form.cleaned_data['password']
            # --- create_user --- method is from custom user model.
            # user = MyUser.object.create_user(email=email, password=password, username=username, first_name=first_name, last_name=last_name)
            # user.role = MyUser.CUSTOMER
            # user.save()

    else:
        form = CreateuserForm()
    context = {'form': form}
    return render(request, 'account/register.html', context)

def activate_account(request, uidb64, token):
    # Activate user by setting 'is_active' field in account model to be True.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully')
        return redirect('user-profile')
    else:
        messages.warning(request, 'Invalid activation link')
        return redirect('user-profile')

@login_required(login_url='user-login')
def my_account(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    context = {
        'user_profile': user_profile,
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'account/user_profile.html', context)

def edit_profile(request):
    user = request.user
    profile = user.userprofile
    profile_form = UserProfileForm(instance=profile)
    user_update_form = UserForm(instance=user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_update_form = UserForm(request.POST, instance=user)
        if profile_form.is_valid() and user_update_form.is_valid():
            profile_form.save()
            user_update_form.save()
            messages.success(request, 'Your account has been updated successfully.')
            return redirect('user-profile')
        else:
            profile_form = UserProfileForm(instance=profile)
            user_update_form = UserForm(instance=user)
    context = {
        'profile_form': profile_form,
        'user_update_form': user_update_form,
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'account/user_profile_edit.html', context)
    

def user_login(request):
    if request.user.is_authenticated:
        return redirect('user-profile')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are loged in successfully.')
                return redirect('user-profile')
            else:
                messages.warning(request, 'Email or password is incorrect.')
                return redirect('user-login')
        except:
            messages.error(request, 'User does not exist.')
    return render(request, 'account/login.html')

@login_required(login_url='user-login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = request.user

        # Authenticate the user with the current password before proceeding
        if not authenticate(username=user.email, password=current_password):
            messages.error(request, 'Incorrect current password. Please try again.')
            return redirect('change-password')

        # Check if the new password and confirmation match
        if new_password != confirm_new_password:
            messages.error(request, 'New password and confirmation do not match. Please try again.')
            return redirect('change-password')

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Update the user's session to avoid logout after password change
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully.')
        return redirect('change-password')
    context = {
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'account/change_password.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # check if email exist in database
        if User.objects.filter(email=email).exists():
            # Need the exact email from request here.
            user = User.objects.get(email__exact=email)
            # Send the reset password email using helper function from utils.py.
            mail_subject = 'Reset your password'
            template = 'account/emails/reset_password_email.html'
            send_email_notification(request, user, mail_subject, template)
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('user-login')
        else:
            messages.warning(request, f'The email {email} does not exist.')
            return redirect('forgot-password')
    return render(request, 'account/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate user by decoding token and user-pk.
    try:
        # get the uid after user clicked reset password link in the email.
        uid = urlsafe_base64_decode(uidb64).decode()
        # get the user by pk=uid
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # check if user is not none and this particular token belongs to this particular user.
    if user is not None and default_token_generator.check_token(user, token):
        # save uid in the session.
        request.session['uid'] = uid
        messages.info(request, 'Please enter your new password')
        return redirect('reset-password')
    else:
        messages.warning(request, 'This link is expired.')
        return redirect('user-profile')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['new_password']
        confirm_password = request.POST['confirm_new_password']
        if password == confirm_password:
            # get the pk from session variable that was stored at reset_password_validate function.
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'You password has been reset successfully.')
            return redirect('user-login')
        else:
            messages.warning(request, "Password didn't match.")
            return redirect('reset-password')
    return render(request, 'account/reset_password.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You are loged out.')
    return redirect('user-login')

@login_required(login_url='user-login')
def wish_list(request):
    context = {
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'account/wish_list.html', context)

@login_required(login_url='user-login')
@user_passes_test(check_role_admin)
def add_product(request):
    form = ProductForm()
    categories = Categories.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            categoy = form.cleaned_data['category']
            print(categoy)
            categoy, created = Categories.objects.get_or_create(category_name=categoy)
            product.category = categoy
            product.save()
            messages.success(request, 'Product has been added successfully.')
            return redirect('products')
        print(form.errors)
    context = {'form': form, 'categories': categories}
    return render(request, 'account/add_product.html', context)

@login_required(login_url='user-login')
@user_passes_test(check_role_admin)
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories')
        print(form.errors)
    else:
        form = CategoryForm(request.POST)
    context = {'form': form}
    return render(request, 'account/add_category.html', context)

@login_required(login_url='user-login')
@user_passes_test(check_role_admin)
def admin_dashboard(request):

    # For dashboard counting 
    products = Products.objects.all()
    categories = Categories.objects.all()

    revenue = 0

    # Get order IDs, products, and quantities, prices for all orders
    order_items = OrderItem.objects.select_related('order', 'product')

    page = request.GET.get('page')
    paginator = Paginator(order_items, 5) # 5 order per page
    try:
        order_obj = paginator.page(page)
    except PageNotAnInteger:
        # IF page number is not an integer then return the first page.
        # This simply means when the user go to the product page.
        page = 1
        order_obj = paginator.page(page)
    except EmptyPage:
        # If the requested page is out of range, then return the last page.
        page = paginator.num_pages
        order_obj = paginator.page(page)

    # Get revenue
    try:
        orders = Order.objects.all()
        for order in orders:
            revenue += order.get_grand_total()
    except IndexError:
        orders = None
        revenue = 0

    context = {
        'paginator': paginator,
        'order_obj': order_obj,
        'products': products,
        'categories': categories,
        'cart_counter': get_cart_counter(request)['cart_count'],
        'revenue': revenue,
        'order_items': order_items
    }
    return render(request, 'account/admin_dashboard.html', context)

def cart_detail(request):
    cart = Cart(request)
    order_form = OrderCreateForm()
    context = {
        'cart_total': cart.get_total_price(),
        'grand_total': cart.get_total_plus_vat(),
        'cart_fee': cart.get_fee(),
        'cart_counter': cart.__len__(),
        'cart': cart,
        'order_form': order_form
    }
    return render(request, 'account/cart_detail.html', context)


@login_required(login_url='user-login')
def add_to_wishlist(request, product_id):
    product = Products.objects.get(pk=product_id)
    user = request.user

    try:
        wishlist = WishList.objects.get(user=user)
    except WishList.DoesNotExist:
        wishlist = WishList(user=user)
        wishlist.save()

    wishlist.products.add(product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = Products.objects.get(pk=product_id)
    wishlist = WishList.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')

@login_required(login_url='user-login')
def view_wishlist(request):
    # wishlist_items = []
    user = request.user
    try:
        wishlist = WishList.objects.get(user=user)
        wishlist_items = wishlist.products.all()
    except WishList.DoesNotExist:
        wishlist_items = []
    
    page = request.GET.get('page')
    paginator = Paginator(wishlist_items, 5) # 3 product per page
    try:
        wish_obj = paginator.page(page)
    except PageNotAnInteger:
        # IF page number is not an integer then return the first page.
        # This simply means when the user go to the product page.
        page = 1
        wish_obj = paginator.page(page)
    except EmptyPage:
        # If the requested page is out of range, then return the last page.
        page = paginator.num_pages
        wish_obj = paginator.page(page)
    context = {
        'wish_obj': wish_obj,
        'paginator': paginator,
        'cart_counter': get_cart_counter(request)['cart_count']
    }
    return render(request, 'account/wish_list.html', context)


