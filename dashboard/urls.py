from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard/index'),
    path('AddProduct', views.add_product, name='dashboard/add_new_product')
]
