from django.urls import path
from . import views

urlpatterns = [
    path("shipping/", views.shipping, name="checkout/shipping"),
    path("payment/", views.payment, name="checkout/payment"),
    path("confirm/", views.confirm_review, name="checkout/confirm"),
    path("place_order", views.place_order, name="checkout/place_order"),
]
