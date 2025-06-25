from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout, name="order/checkout"),
    path("your_orders", views.your_orders, name="order/your_orders"),
    path("details/<int:order_id>", views.get_order_details, name="order/details"),
]
