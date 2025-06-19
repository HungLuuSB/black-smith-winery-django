from django.urls import path
from . import views


urlpatterns = [
    path("update/<int:product_id>", views.update_cart, name="cart/update"),
    path("cart/summary", views.get_cart_summary, name="cart/summary_partial"),
    path("remove/<int:item_id>", views.remove_from_cart, name="cart/remove"),
    path("details", views.get_cart_details, name="cart/details"),
]
