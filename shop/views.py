from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from common.models.category import Category
from shop.models import Product
# Create your views here.

def category(request, categorySlug: str):
    category = get_object_or_404(Category, slug = categorySlug)
    products = Product.objects.filter(category=category).select_related('brand', 'country').order_by('name')
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/product_category.html', context)

def product_details(request, productSlug: str):
    return render(request, 'shop/index.html')
