from django.urls import path
from . import views


urlpatterns = [
    path('details', views.details, name='cart/details'),
    path('add/<int:product_id>', views.add_to_cart, name='cart/add')
]
