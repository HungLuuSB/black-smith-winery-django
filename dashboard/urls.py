from django.urls import path
from . import views

# dashboard/admin -> views.admin_index
urlpatterns = [
    path("", views.index, name="dashboard/index"),
    path("admin", views.admin_index, name="dashboard/admin"),
    path("products", views.admin_products, name="dashboard/products"),
    path("products/edit/<int:product_id>", views.admin_edit_product, name="dashboard/edit-product"),
    path("AddProduct", views.add_product, name="dashboard/add_new_product"),
]
