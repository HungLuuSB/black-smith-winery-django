from django.urls import path
from . import views

urlpatterns = [
    path('<slug:categorySlug>', views.category, name='product/categorySlug'),
    path('<slug:productSlug>', views.product_details, name='product/details')
]
