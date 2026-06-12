from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Product, Order


# Home Page
def home(request):
    products = Product.objects.all()

    return render(
        request,
        'home.html',
        {'products': products}
    )


# Product Details
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(
        request,
        'product_detail.html',
        {'product': product}
    )


# Add Product To Cart
def add_to_cart(request, id):
    cart = request.session.get('cart', [])

    cart.append(id)

    request.session['cart'] = cart

    return redirect('home')


# Cart Page
def cart(request):
    ids = request.session.get('cart', [])

    products = Product.objects.filter(id__in=ids)

    total = sum(product.price for product in products)

    return render(
        request,
        'cart.html',
        {
            'products': products,
            'total': total
        }
    )


# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# User Logout
def user_logout(request):
    logout(request)
    return redirect('home')


# Checkout / Order Processing
@login_required
def checkout(request):

    ids = request.session.get('cart', [])

    products = Product.objects.filter(id__in=ids)

    total = sum(product.price for product in products)

    Order.objects.create(
        user=request.user,
        total_amount=total
    )

    request.session['cart'] = []

    return render(
        request,
        'checkout.html',
        {
            'total': total
        }
    )