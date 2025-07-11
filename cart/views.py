from django.db import transaction
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect, render, get_object_or_404
from cart.models import Cart, CartItem
from shop.models import Product
from decimal import Decimal
from cart.forms import UpdateCartItemForm
# Create your views here.


def get_cart_details(request):
    cart = Cart.get_cart(request)
    total_quantity = cart.get_total_quantity()
    sub_total = cart.get_total()
    vat = sub_total * Decimal(0.08)
    grand_total = vat + sub_total
    context = {
        "cart": cart,
        "sub_total": sub_total,
        "total_quantity": total_quantity,
        "vat": vat,
        "grand_total": grand_total,
    }
    return render(request, "cart/details.html", context)


def get_cart_summary(request):
    cart = Cart.get_cart(request)
    total_quantity = cart.get_total_quantity()
    total_price = cart.get_total()
    context = {
        "cart": cart,
        "total_quantity": total_quantity,
        "total_price": total_price,
    }
    return render(request, "cart/summary.html", context)


def update_cart(request, product_id):
    cart = Cart.get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 0))
        if quantity <= 0:
            quantity = 0
    except ValueError:
        quantity = 0

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


def remove_from_cart(request, product_id):
    cart = Cart.get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_item(product)

    return redirect(request.META.get("HTTP_REFERER", "/"))


def update_carts(request):
    cart = Cart.get_cart(request)
    if request.method == "POST":
        form = UpdateCartItemForm(request.POST, cart=cart)
        if form.is_valid():
            for item in cart.get_items():
                field_name = f"quantity_{item.id}"
                quantity = form.cleaned_data.get(field_name)

                if quantity == 0:
                    item.delete()
                else:
                    item.quantity = quantity
                    item.save()

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
