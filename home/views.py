from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product
from user_behavior.models import ProductView
from common.models import Country, Brand, Category
from wishlist.models import Wishlist
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        views = ProductView.objects.filter(user=request.user).order_by('-timestamp')[:10]
        wishlist = Wishlist.objects.filter(user=request.user)[:10]
    else:
        views = ProductView.objects.filter(session_key=request.session.session_key).order_by('-timestamp')[:10]
    
    personalized_products = Product.objects.filter(id__in=[view.product.id for view in views])
    personalized_brands = Brand.objects.filter(id__in=[view.product.brand.id for view in views])
    personalized_categories = Category.objects.filter(id__in=[view.product.category.id for view in views])

    products_from_brands = Product.objects.filter(brand__in=personalized_brands)
    products_from_categories = Product.objects.filter(category__in=personalized_categories)

    combined_personalized_products = (
        personalized_products |
        products_from_brands |
        products_from_categories
    ).distinct()

    context = {
        "products": Product.objects.all()[:9],
        "personalized_products": combined_personalized_products,
        "wishlist": wishlist
    }
    return render(request, 'home/index.html', context)