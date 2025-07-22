from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from dashboard.forms import AddNewProductForm, EditProductForm
from shop.models import Stock, Product
from common.models import Country, Brand, Category
from order.models import Order, OrderDetail


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
        "total_grand_total": total_grand_total,
    }
    return render(request, "dashboard/admin_index.html", context)

def admin_products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "dashboard/admin_products.html", context)

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

            product.save()

            stock_quantity = request.POST.get("stock")
            stock, _ = Stock.objects.get_or_create(product=product)
            stock.quantity = stock_quantity
            stock.save()

            context = {
                'form': EditProductForm(instance=product),
                'message': 'Product updated successfully.',
                'product': product,
                'categories': Category.objects.all(),
                'brands': Brand.objects.all(),
                'countries': Country.objects.all()
            }
            return render(request, "dashboard/admin_edit_product.html", context)
        else:
            print("Form errors:", form.errors)
            context = {
                'form': form,
                'message': 'Failed to update product.',
                'product': product,
                'categories': Category.objects.all(),
                'brands': Brand.objects.all(),
                'countries': Country.objects.all()
            }
            return render(request, "dashboard/admin_edit_product.html", context)

    context = {
        'form': EditProductForm(instance=product),
        'product': product,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'countries': Country.objects.all()
    }
    return render(request, "dashboard/admin_edit_product.html", context)

def add_product(request):
    if request.method == "POST":
        form = AddNewProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            country_name = request.POST.get("country")
            country, created = Country.objects.get_or_create(name=country_name)
            product.country = country

            brand_name = request.POST.get("brand")
            brand, created = Brand.objects.get_or_create(name=brand_name)

            product.brand = brand
            product.save()
            quantity = form.cleaned_data["stock_quantity"]
            Stock.objects.create(product=product, quantity=quantity)
            return render(request, "dashboard/index.html")
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())

    context = {
        "form": AddNewProductForm,
        "countries": Country.objects.all(),
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),
    }
    return render(request, "dashboard/add_new_product.html", context)
