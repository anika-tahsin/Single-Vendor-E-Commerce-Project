from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from products.models import Product

from .models import Cart, CartProduct
from .utils import get_session_key
from django.urls import reverse



def add_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    user = request.user if request.user.is_authenticated else None
    session_key = get_session_key(request)

    cart, created = Cart.objects.get_or_create(
        session_key=session_key,
        defaults={'user': user},
    )
    # If cart exists but user just logged in, update user field
    if user and cart.user is None:
        cart.user = user
        cart.save()

    cart_product, created = CartProduct.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={'quantity': 0},
    )
    cart_product.quantity += 1
    cart_product.save()

    messages.success(request, f"Added {product.name} to cart!")
    return redirect(reverse("cart:cart_detail"))
  

def remove_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        cart = get_object_or_404(Cart, session_key=get_session_key(request))

    cart_product = get_object_or_404(CartProduct, product=product, cart=cart)

    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    else:
        cart_product.delete()
    
    # return redirect(reverse("cart:cart_detail"))
#
    url = request.META.get("HTTP_REFERER")
    if url:
        return redirect(url)
    else:
        return redirect("cart:cart_detail")  


def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=get_session_key(request)).first()

    if not cart:
        # Empty cart case
        cart_products = []
        total = 0
        quantity = 0
    else:
        cart_products = CartProduct.objects.filter(cart=cart).select_related("product")
        total = sum(cp.product.regular_price * cp.quantity for cp in cart_products)
        quantity = sum(cp.quantity for cp in cart_products)

    context = {
        "cart_total": total,
        "quantity": quantity,
        "cart_items": cart_products,
        "grand_total": total + settings.DELIVERY_CHARGE,
    }
    return render(request, "cart/cart.html", context)
