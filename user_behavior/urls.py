from django.urls import path
from . import views
urlpatterns = [
    path("save-viewed-product/<int:product_id>", views.save_viewed_product, name="user_behavior/save-viewed-product")
]
