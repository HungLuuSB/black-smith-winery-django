from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from common.models import Category, Brand, Country
from shop.models import Product
from wishlist.models import Wishlist
from user_behavior.models import ProductView
# Create your views here.

def category(request, categorySlug: str):
    category = get_object_or_404(Category, slug=categorySlug)
    products = Product.objects.filter(category=category).select_related('brand', 'country').order_by('name')
    brands = Brand.objects.filter(products__category=category).distinct()

    selected_brands = list(map(int, request.GET.getlist('brands')))

    if selected_brands:
        products = products.filter(brand__id__in=selected_brands)

    context = {
        'category': category,
        'products': products,
        'brands': brands,
        'selected_brands': selected_brands
    }
    return render(request, 'shop/product_category.html', context)

def product_details(request, productSlug: str):
    product = get_object_or_404(Product, slug=productSlug)
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    user = request.user
    
    if user.is_authenticated:
        ProductView.objects.create(user=request.user, product=product)
    else:
        session_key = request.session.session_key or request.session.save()
        ProductView.objects.create(session_key=session_key, product=product)

    context = {
        'product': product,
        'in_wishlist': in_wishlist
    }
    return render(request, 'shop/product_details.html', context)

def filter_products(request, categorySlug: str):
    category = get_object_or_404(Category, slug=categorySlug)
    brand_ids = request.GET.getlist('brands')
    country_ids = request.GET.getlist('countries')
    sort = request.GET.get("sort", "id")
    order = request.GET.get("order", "asc")

    products = Product.objects.filter(category=category)

    if brand_ids:
        products = products.filter(brand__id__in=brand_ids)

    if country_ids:
        products = products.filter(country__id__in=country_ids)

    brands = Brand.objects.filter(products__category=category).distinct()
    countries = Country.objects.filter(products__category=category).distinct()
    sort_fields = {"id", "name", "original_price"}
    if sort not in sort_fields:
        sort = "id"

    order_prefix = "" if order == "asc" else "-"
    ordering = f"{order_prefix}{sort}"

    products = products.order_by(ordering)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product_list.html', {
            'products': products
        })

    return render(request, 'shop/product_category.html', {
        'category': category,
        'products': products,
        'brands': brands,
        'countries': countries,
        'selected_brands': list(map(int, brand_ids)),
        'selected_countries': list(map(int, country_ids)),
    })

def search_products(request):
    query = request.GET.get("q", "")
    if len(query) >= 3:
        products = Product.objects.filter(name__icontains=query)[:15]
        data = [
            {
                "name": p.name,
                "slug": p.slug,
                "image": p.image.url if p.image else "",
                "final_price": p.final_price,
            }
            for p in products
        ]
        return JsonResponse({"products": data})
    return JsonResponse({"products": []})