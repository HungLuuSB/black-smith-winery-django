from django.db import models
from common.models import Category, Country, Brand
from django.utils.text import slugify
import uuid
# Create your models here.
CATEGORY_SKU_PREFIX = {
    1: 'WHT',
    2: 'RED',
    3: 'SPK',
    4: 'WSK',
    5: 'GIN',
    6: 'TEQ'
}


class Product(models.Model):
    sku = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=12)
    volume = models.PositiveIntegerField()
    abv = models.DecimalField(decimal_places=2, max_digits=5)
    vintage = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            cat_code = self.category.sku_prefix
            uid = str(uuid.uuid4().int)[:5]
            self.sku = f"{cat_code}-{uid}"

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
