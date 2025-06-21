from django.shortcuts import render, get_object_or_404
from .models import Order, OrderDetail
from .forms.checkout import CheckoutForm
from common.models import Country
from cart.models import Cart
# Create your views here.


def get_order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    order_details = order.order_details.all()

    context = {"order": order, "order_details": order_details}

    return render(request, "order/detail.html", context)


def get_orders(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser or user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)

    return Order.objects.none()


def your_orders(request):
    orders = get_orders(request)
    context = {
        "orders": orders,
    }
    return render(request, "order/your_orders.html", context)


def checkout(request):
    cart = Cart.get_cart(request)
    inital_data = {}
    if request.user.is_authenticated:
        inital_data = {
            "customer_email": request.user.email,
            "customer_first_name": request.user.first_name,
            "customer_last_name": request.user.last_name,
        }

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart = Cart.get_cart(request)
            order = Order(
                customer_first_name=form.cleaned_data["customer_first_name"],
                customer_last_name=form.cleaned_data["customer_last_name"],
                customer_email=form.cleaned_data["customer_email"],
                customer_phone=form.cleaned_data["customer_phone"],
                country=Country.objects.get(id=form.cleaned_data["country"]),
                total_amount=cart.get_total(),
                city=form.cleaned_data["city"],
                shipping_address=form.cleaned_data["shipping_address"],
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
            return render(request, "home/index.html", {"order": order})
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())

    context = {
        "form": CheckoutForm(initial=inital_data),
        "countries": Country.objects.all(),
        "cart": cart,
        "total_price": cart.get_total(),
    }

    return render(request, "order/checkout.html", context)
