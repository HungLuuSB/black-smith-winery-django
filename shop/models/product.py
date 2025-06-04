from django.db import models
from common.models import Category, Country, Brand
# Create your models here.
class Product(models.Model):
    sku = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=12)
    volume = models.PositiveIntegerField()
    abv = models.DecimalField(decimal_places=2, max_digits=5)
    vintage = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
