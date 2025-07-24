from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="account/login"),
    path("signup", views.register, name="account/signup"),
    path("logout", views.logout, name="account/logout"),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path("edit", views.edit, name="account/edit"),
    path("dashboard", views.dashboard, name="account/dashboard"),
    path("order-history", views.order_history, name="account/order-history"),
    path('wishlist', views.wishlist, name="account/wishlist")
    # path("address-book", views.address_book, name="account/address-book"),
    # path("payment", views.payment, name="account/payment"),
]
