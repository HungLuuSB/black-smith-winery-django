from django.db import transaction
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect, render, get_object_or_404
from cart.models import Cart, CartItem
from shop.models import Product
# Create your views here.


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def get_cart_summary(request):
    cart = get_or_create_cart(request)
    items = cart.items.all()
    total_quantity = sum(item.quantity for item in items)
    total_price = sum(item.product.price * item.quantity for item in items)
    context = {
        "cart": cart,
        "total_quantity": total_quantity,
        "total_price": total_price,
    }
    return render(request, "cart/summary.html", context)


def update_cart(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.quantity += quantity
        cart_item.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if item:
        item.delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))


@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    try:
        session_key = request.session.session_key
        guest_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
        user_cart, _ = Cart.objects.get_or_create(user=user)

        with transaction.atomic():
            for item in guest_cart.items.all():
                existing = CartItem.objects.filter(
                    cart=user_cart, product=item.product
                ).first()
                if existing:
                    existing.quantity += item.quantity
                    existing.save()
                else:
                    item.cart = user_cart
                    item.save()
            guest_cart.delete()
    except Cart.DoesNotExist:
        pass
