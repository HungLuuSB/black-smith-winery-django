from django.shortcuts import render
from dashboard.forms import AddNewProductForm
from shop.models import Stock
from common.models import Country, Brand, Category


# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")


def admin_index(request):
    context = {
        'choice': 'overview'
    }
    return render(request, "dashboard/admin.html", context)


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
