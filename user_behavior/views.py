from django.shortcuts import render, get_object_or_404
from .models import ProductView
from shop.models import Product

# Create your views here.
def save_viewed_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    
    if user.is_authenticated:
        ProductView.objects.create(user=request.user, product=product)
    else:
        session_key = request.session.session_key or request.session.save()
        ProductView.objects.create(session_key=session_key, product=product)

def get_recently_viewed_products(request):
    if request.user.is_authenticated:
        views = ProductView.objects.filter(user=request.user).order_by('-timestamp')[:10]
    else:
        views = ProductView.objects.filter(session_key=request.session.session_key).order_by('-timestamp')[:10]
    
    return Product.objects.filter(id__in=[view.product.id for view in views])