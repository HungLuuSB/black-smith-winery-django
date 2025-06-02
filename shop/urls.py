from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index),
    path('<slug:categorySlug>', views.index, name='product/categorySlug')
]
