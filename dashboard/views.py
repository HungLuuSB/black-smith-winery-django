from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Sum
from dashboard.forms import AddProductForm, EditProductForm, AddVoucherForm
from shop.models import Stock, Product
from common.models import Country, Brand, Category
from order.models import Order, OrderDetail, Voucher
import os


# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")

def admin_index(request):
    total_grand_total = Order.objects.aggregate(total_grand_total=Sum("grand_total"))[
        "total_grand_total"
    ]
    context = {
        "choice": "overview",
        "orders": Order.objects.all(),
        "products": Product.objects.all(),
        "total_grand_total": total_grand_total,
    }
    return render(request, "dashboard/admin_index.html", context)

def admin_vouchers(request):
    context = {"vouchers": Voucher.objects.all()}
    return render(request, "dashboard/admin_vouchers.html", context)

def admin_products(request):
    context = {"products": Product.objects.all()}
    return render(request, "dashboard/admin_products.html", context)

def admin_orders(request):
    context = {"orders": Order.objects.all()}
    return render(request, "dashboard/admin_orders.html", context)

def admin_edit_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

            country_id = request.POST.get("country")
            if country_id:
                print(country_id)
                country = Country.objects.get(id=country_id)
                product.country = country

            brand_name = request.POST.get("brand")
            if brand_name:
                brand, _ = Brand.objects.get_or_create(name=brand_name)
                product.brand = brand

            if "image" in request.FILES:
                if product.image and os.path.isfile(product.image.path):
                    os.remove(product.image.path)

            product.save()

            stock_quantity = request.POST.get("stock")
            stock, _ = Stock.objects.get_or_create(product=product)
            stock.quantity = stock_quantity
            stock.save()

            context = {
                "form": EditProductForm(instance=product),
                "message": "Product updated successfully.",
                "status": "OK",
                "product": product,
                "categories": Category.objects.all(),
                "brands": Brand.objects.all(),
                "countries": Country.objects.all(),
            }
            return render(request, "dashboard/admin_edit_product.html", context)
        else:
            print("Form errors:", form.errors)
            context = {
                "form": form,
                "message": "Failed to update product.",
                "status": "FAILED",
                "product": product,
                "categories": Category.objects.all(),
                "brands": Brand.objects.all(),
                "countries": Country.objects.all(),
            }
            return render(request, "dashboard/admin_edit_product.html", context)

    context = {
        "form": EditProductForm(instance=product),
        "product": product,
        "categories": Category.objects.all(),
        "brands": Brand.objects.all(),
        "countries": Country.objects.all(),
    }
    return render(request, "dashboard/admin_edit_product.html", context)

def admin_add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            country = form.cleaned_data["country"]
            product.country = country

            brand_name = form.cleaned_data["brand"]
            brand, _ = Brand.objects.get_or_create(name=brand_name)
            product.brand = brand

            product.save()
            stock_quantity = request.POST.get("stock")
            Stock.objects.create(product=product, quantity=stock_quantity)
            context = {
                "form": AddProductForm(),
                "message": "Product added successfully.",
                "status": "OK",
                "categories": Category.objects.all(),
                "brands": Brand.objects.all(),
                "countries": Country.objects.all(),
            }
            return render(request, "dashboard/admin_add_product.html", context)
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
            context = {
                "form": AddProductForm(),
                "message": "Failed to add product.",
                "status": "FAILED",
                "categories": Category.objects.all(),
                "brands": Brand.objects.all(),
                "countries": Country.objects.all(),
            }
            return render(request, "dashboard/admin_add_product.html", context)

    context = {
        "form": AddProductForm,
        "countries": Country.objects.all(),
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),
    }
    return render(request, "dashboard/admin_add_product.html", context)

def admin_delete_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    if OrderDetail.objects.filter(product=product).exists():
        context = {"status": "FAILED", "message": "This product has been purchased."}
        return render(request, "dashboard/admin_products.html", context)

    product.delete()
    context = {"status": "OK", "message": "Product deleted successfully."}
    return render(request, "dashboard/admin_products.html", context)

def admin_add_voucher(request):
    if request.method == "POST":
        form = AddVoucherForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                "form": AddVoucherForm,
                "message": "Voucher added successfully.",
                "status": "OK",
            }
            return render(request, "dashboard/admin_add_voucher.html", context)
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
            context = {
                "form": AddVoucherForm,
                "message": "Failed to add voucher.",
                "status": "FAILED",
            }
            return render(request, "dashboard/admin_add_voucher.html", context)
    context = {
        "form": AddVoucherForm
    }
    return render(request, "dashboard/admin_add_voucher.html", context)

def admin_confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != "Pending":
        context = {
            "orders": Order.objects.all(),
            "status": "FAILED",
            "message": "Can not confirm order that had already been confirmed!"
        }
        return render(request, "dashboard/admin_orders.html", context)

    order.status = "Confirmed"
    order.save()

    send_mail(
        subject="BlackSmith's Winery | Order confirmed!",
        message=f'Your order {order.id} has been confirmed!',
        from_email='noreply@yourdomain.com',
        recipient_list=[order.customer_email],
    )

    context = {
        "orders": Order.objects.all(),
        "status": "OK",
        "message": "Order confirmed!"
    }
    return render(request, "dashboard/admin_orders.html", context)
    