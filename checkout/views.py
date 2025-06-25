from django.shortcuts import redirect, render
from decimal import Decimal
from .forms import ShippingForm
from common.models import Country
from cart.models import Cart
from order.models import Order, OrderDetail
# Create your views here.


def shipping(request):
    session_data = request.session.get("shipping")
    cart = Cart.get_cart(request)
    initial = {}
    initial["customer_phone"] = session_data.get("customer_phone", "")
    initial["country"] = session_data.get("country", "")
    initial["city"] = session_data.get("city", "")
    initial["postal_code"] = session_data.get("postal_code", "")
    initial["address"] = session_data.get("address", "")

    if request.user.is_authenticated:
        initial["customer_email"] = request.user.email
        initial["customer_first_name"] = request.user.first_name
        initial["customer_last_name"] = request.user.last_name
    else:
        initial["customer_email"] = session_data.get("customer_email")
        initial["customer_first_name"] = session_data.get("customer_first_name")
        initial["customer_last_name"] = session_data.get("customer_last_name")
    if request.method == "POST":
        form = ShippingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.session["shipping"] = {
                "customer_email": data.get("customer_email"),
                "customer_phone": data.get("customer_phone"),
                "customer_first_name": data.get("customer_first_name"),
                "customer_last_name": data.get("customer_last_name"),
                "country": data.get("country"),
                "city": data.get("city"),
                "postal_code": data.get("postal_code"),
                "address": data.get("address"),
            }
            return redirect("checkout/payment")
        else:
            print(form.errors)
    subtotal = cart.get_total()
    vat = subtotal * Decimal(0.08)
    grand_total = subtotal + vat
    form = ShippingForm(initial=initial)
    context = {
        "step": 1,
        "form": form,
        "countries": Country.objects.all(),
        "cart": cart,
        "subtotal": subtotal,
        "vat": vat,
        "grand_total": grand_total,
    }
    return render(request, "checkout/shipping.html", context)


def payment(request):
    session_data = request.session.get("shipping")
    print(session_data)

    cart = Cart.get_cart(request)
    initial = {}
    initial["customer_phone"] = session_data.get("customer_phone", "")
    initial["country"] = session_data.get("country", "")
    initial["city"] = session_data.get("city", "")
    initial["postal_code"] = session_data.get("postal_code", "")
    initial["address"] = session_data.get("address", "")
    if request.user.is_authenticated:
        initial["customer_email"] = request.user.email
        initial["customer_first_name"] = request.user.first_name
        initial["customer_last_name"] = request.user.last_name
    else:
        initial["customer_email"] = session_data.get("customer_email")
        initial["customer_first_name"] = session_data.get("customer_first_name")
        initial["customer_last_name"] = session_data.get("customer_last_name")

    if request.method == "POST":
        return redirect("checkout/confirm")

    subtotal = cart.get_total()
    vat = subtotal * Decimal(0.08)
    grand_total = subtotal + vat
    context = {
        "step": 2,
        "countries": Country.objects.all(),
        "cart": cart,
        "subtotal": subtotal,
        "vat": vat,
        "grand_total": grand_total,
    }

    return render(request, "checkout/payment.html", context)


def confirm_review(request):
    session_data = request.session.get("shipping")
    cart = Cart.get_cart(request)
    initial = {
        "customer_phone": session_data.get("customer_phone"),
        "country": session_data.get("country"),
        "city": session_data.get("city"),
        "postal_code": session_data.get("postal_code"),
        "address": session_data.get("address"),
    }
    if request.user.is_authenticated:
        initial["customer_email"] = request.user.email
        initial["customer_first_name"] = request.user.first_name
        initial["customer_last_name"] = request.user.last_name
    else:
        initial["customer_email"] = session_data.get("customer_email")
        initial["customer_first_name"] = session_data.get("customer_first_name")
        initial["customer_last_name"] = session_data.get("customer_last_name")

    if request.method == "POST":
        return redirect("checkout/place_order")

    subtotal = cart.get_total()
    vat = subtotal * Decimal(0.08)
    grand_total = subtotal + vat
    form = ShippingForm(initial=initial)
    context = {
        "step": 3,
        "form": form,
        "countries": Country.objects.all(),
        "cart": cart,
        "subtotal": subtotal,
        "vat": vat,
        "grand_total": grand_total,
    }

    return render(request, "checkout/confirm.html", context)


def place_order(request):
    shipping_data = request.session.get("shipping")

    cart = Cart.get_cart(request)
    subtotal = cart.get_total()
    vat = subtotal * Decimal(0.08)
    grand_total = subtotal + vat
    order = Order(
        customer_first_name=shipping_data.get("customer_first_name"),
        customer_last_name=shipping_data.get("customer_last_name"),
        customer_email=shipping_data.get("customer_email"),
        customer_phone=shipping_data.get("customer_phone"),
        country=Country.objects.get(id=shipping_data.get("country")),
        total_amount=grand_total,
        city=shipping_data.get("city"),
        shipping_address=shipping_data.get("address"),
        status="Pending",
    )

    if request.user.is_authenticated:
        order.user = request.user

    order.save()

    for item in cart.get_items():
        OrderDetail.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.product.price,
        )

    cart.clear()
    return render(request, "checkout/success.html", {"order": order})
