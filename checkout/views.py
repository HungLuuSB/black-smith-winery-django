from django.shortcuts import redirect, render
from django.core.mail import send_mail
from decimal import Decimal
from .forms import ShippingForm
from common.models import Country, StoreSettings
from cart.models import Cart
from order.models import Order, OrderDetail, Voucher
import time
from payos import ItemData, PaymentData, PayOS
# Create your views here.

client_id = "YOUR_CLIENT_ID"
api_key = "YOUR_API_KEY"
checksum_key = "YOUR_CHECKSUM_KEY"

payOS = PayOS(client_id, api_key, checksum_key)

def create_payment_link():
    try:
        item = ItemData(name="Mì tôm hảo hảo ly", quantity=1, price=2000)
        payment_data = PaymentData(
            orderCode=int(time.time()),
            amount=2000,
            description="Thanh toan don hang",
            items=[item],
            cancelUrl="",
            returnUrl="",
        )
        payment_link_response = payOS.createPaymentLink(payment_data)
    except Exception as e:
        return str(e)

    return payment_link_response.to_json()


def shipping(request):
    vat_rate = StoreSettings.get_solo().vat_rate / 100
    session_data = request.session.get("shipping", {})
    voucher_code = request.GET.get("voucher") or request.session.get("voucher")
    discount = Decimal(0)
    voucher = None

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
            return redirect("checkout/confirm")
        else:
            print(form.errors)
    subtotal = cart.get_total()
    vat = subtotal * vat_rate
    grand_total = subtotal + vat
    if voucher_code:
        try:
            voucher = Voucher.objects.get(code__iexact=voucher_code, active=True)
            discount = voucher.apply_discount(subtotal)
            request.session["voucher"] = voucher.code
        except Voucher.DoesNotExist:
            request.session.pop("voucher", None)
    discount_amount = (subtotal * discount / 100)
    sub_total_after_discount = subtotal - discount_amount
    vat = sub_total_after_discount * Decimal(vat_rate)
    grand_total = sub_total_after_discount + vat

    form = ShippingForm(initial=initial)
    context = {
        "step": 1,
        "form": form,
        "countries": Country.objects.all(),
        "cart": cart,
        "subtotal": subtotal,
        "vat": vat,
        "discount_amount": discount_amount,
        "discount": discount,
        "voucher": voucher,
        "voucher_code": voucher_code,
        "sub_total_after_discount": sub_total_after_discount,
        "vat_rate": vat_rate,
        "grand_total": grand_total,
    }
    return render(request, "checkout/shipping.html", context)


def payment(request):
    session_data = request.session.get("shipping")
    vat_rate = StoreSettings.get_solo().vat_rate / 100
    voucher_code = request.GET.get("voucher") or request.session.get("voucher")
    discount = Decimal(0)
    voucher = None

    cart = Cart.get_cart(request)
    initial = {}
    initial["customer_phone"] = session_data.get("customer_phone", "")
    initial["country"] = session_data.get("country", "")
    initial["city"] = session_data.get("city", "")
    initial["postal_code"] = session_data.get("postal_code", "")
    initial["address"] = session_data.get("address", "")
    initial["customer_email"] = session_data.get("customer_email")
    initial["customer_first_name"] = session_data.get("customer_first_name")
    initial["customer_last_name"] = session_data.get("customer_last_name")

    if request.method == "POST":
        return redirect("checkout/place_order")

    subtotal = cart.get_total()
    vat = subtotal * vat_rate
    grand_total = subtotal + vat
    if voucher_code:
        try:
            voucher = Voucher.objects.get(code__iexact=voucher_code, active=True)
            discount = voucher.apply_discount(subtotal)
            request.session["voucher"] = voucher.code
        except Voucher.DoesNotExist:
            request.session.pop("voucher", None)
    discount_amount = (subtotal * discount / 100)
    sub_total_after_discount = subtotal - discount_amount
    vat = sub_total_after_discount * Decimal(vat_rate)
    grand_total = sub_total_after_discount + vat

    context = {
        "step": 3,
        "countries": Country.objects.all(),
        "cart": cart,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "discount": discount,
        "voucher": voucher,
        "voucher_code": voucher_code,
        "sub_total_after_discount": sub_total_after_discount,
        "vat": vat,
        "vat_rate": vat_rate,
        "grand_total": grand_total,
    }

    return render(request, "checkout/payment.html", context)


def confirm_review(request):
    vat_rate = StoreSettings.get_solo().vat_rate / 100
    voucher_code = request.GET.get("voucher") or request.session.get("voucher")
    discount = Decimal(0)
    voucher = None

    session_data = request.session.get("shipping", {})
    cart = Cart.get_cart(request)
    initial = {
        "customer_phone": session_data.get("customer_phone"),
        "country": session_data.get("country"),
        "city": session_data.get("city"),
        "postal_code": session_data.get("postal_code"),
        "address": session_data.get("address"),
    }

    initial["customer_email"] = session_data.get("customer_email")
    initial["customer_first_name"] = session_data.get("customer_first_name")
    initial["customer_last_name"] = session_data.get("customer_last_name")

    if request.method == "POST":
        return redirect("checkout/payment")

    subtotal = cart.get_total()
    vat = subtotal * vat_rate
    grand_total = subtotal + vat
    if voucher_code:
        try:
            voucher = Voucher.objects.get(code__iexact=voucher_code, active=True)
            discount = voucher.apply_discount(subtotal)
            request.session["voucher"] = voucher.code
        except Voucher.DoesNotExist:
            request.session.pop("voucher", None)
    discount_amount = (subtotal * discount / 100)
    sub_total_after_discount = subtotal - discount_amount
    vat = sub_total_after_discount * Decimal(vat_rate)
    grand_total = sub_total_after_discount + vat

    form = ShippingForm(initial=initial)
    context = {
        "step": 2,
        "form": form,
        "countries": Country.objects.all(),
        "cart": cart,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "discount": discount,
        "voucher": voucher,
        "voucher_code": voucher_code,
        "sub_total_after_discount": sub_total_after_discount,
        "vat": vat,
        "vat_rate": vat_rate,
        "grand_total": grand_total,
    }

    return render(request, "checkout/confirm.html", context)


def place_order(request):
    vat_rate = StoreSettings.get_solo().vat_rate / 100
    voucher_code = request.GET.get("voucher") or request.session.get("voucher")
    discount = Decimal(0)
    voucher = None

    shipping_data = request.session.get("shipping")

    cart = Cart.get_cart(request)
    subtotal = cart.get_total()
    vat = subtotal * vat_rate
    grand_total = subtotal + vat
    if voucher_code:
        try:
            voucher = Voucher.objects.get(code__iexact=voucher_code, active=True)
            discount = voucher.apply_discount(subtotal)
            request.session["voucher"] = voucher.code
        except Voucher.DoesNotExist:
            request.session.pop("voucher", None)
    discount_amount = (subtotal * discount / 100)
    sub_total_after_discount = subtotal - discount_amount
    vat = sub_total_after_discount * Decimal(vat_rate)
    grand_total = sub_total_after_discount + vat

    order = Order(
        customer_first_name=shipping_data.get("customer_first_name"),
        customer_last_name=shipping_data.get("customer_last_name"),
        customer_email=shipping_data.get("customer_email"),
        customer_phone=shipping_data.get("customer_phone"),
        country=Country.objects.get(id=shipping_data.get("country")),
        grand_total=grand_total,
        city=shipping_data.get("city"),
        shipping_address=shipping_data.get("address"),
        status="Pending",
    )

    if request.user.is_authenticated:
        order.user = request.user

    if voucher != None:
        order.voucher = voucher
        request.session.pop("voucher", None)
        voucher.active = False
        voucher.save()

    order.save()

    

    for item in cart.get_items():
        stock = item.product.stock
        if stock.quantity >= item.quantity:
            OrderDetail.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.final_price,
            )
            stock.quantity -= item.quantity
            stock.save()


    cart.clear()
    if "shipping" in request.session:
        del request.session["shipping"]
    send_mail(
        subject="BlackSmith's Winery | Order placed!",
        message=f'Your order {order.id} has been created! Wait for confirmation and it will be on your way.\nTotal: £{order.grand_total}\nTime: {order.created_at}',
        from_email='noreply@yourdomain.com',
        recipient_list=[order.customer_email],
    )
    return render(request, "checkout/success.html", {"order": order})
