from django.urls import path
from . import views

# dashboard/admin -> views.admin_index
urlpatterns = [
    path("", views.index, name="dashboard/index"),
    path("admin", views.admin_index, name="dashboard/admin"),
    path("products", views.admin_products, name="dashboard/products"),
    path(
        "products/edit/<int:product_id>",
        views.admin_edit_product,
        name="dashboard/edit-product",
    ),
    path(
        "products/delete/<int:product_id>",
        views.admin_delete_product,
        name="dashboard/delete-product",
    ),
    path("products/add-product", views.admin_add_product, name="dashboard/add-product"),
    path("orders", views.admin_orders, name="dashboard/orders"),
]
