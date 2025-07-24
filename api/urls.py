from django.urls import path
from . import views

urlpatterns = [
    path("order-chart", views.OrderChart.as_view(), name="api/order-chart"),
    path(
        "category-chart",
        views.TopSellingCategoryChart.as_view(),
        name="api/top-category-chart",
    ),
    path("get-products", views.get_product_by_name, name="api/get-products"),
    path("get-orders", views.get_order_by_customer_name, name="api/get-orders"),
    path("get-vouchers", views.get_voucher_by_code, name="api/get-vouchers")
]
