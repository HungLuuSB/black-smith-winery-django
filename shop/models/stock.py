from django.db import models
from .product import Product

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
