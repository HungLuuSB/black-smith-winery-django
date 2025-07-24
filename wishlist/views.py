from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from account.models import CustomUser
from .models import Wishlist
# Create your views here.

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        wishlist_item.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
    