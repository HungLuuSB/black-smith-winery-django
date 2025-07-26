from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<slug:categorySlug>/', views.filter_products, name='product/categorySlug'),
    path('search-products', views.search_products, name='product/search'),
    re_path(r"^details/(?P<productSlug>[\w-]+)$", views.product_details, name="product/details")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
