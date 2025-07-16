from django.urls import path
from . import views
urlpatterns = [
    path('sales_chart', views.sales_chart, name='api/sales_chart')
]
