from django.db import models
from common.models import Category, Country, Brand
from django.utils.text import slugify
import uuid

# Create your models here.
CATEGORY_SKU_PREFIX = {1: "WHT", 2: "RED", 3: "SPK", 4: "WSK", 5: "GIN", 6: "TEQ"}


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(decimal_places=2, max_digits=12)
    volume = models.PositiveIntegerField()
    abv = models.DecimalField(decimal_places=2, max_digits=5)
    vintage = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if not is_new:
            old = Product.objects.get(pk=self.pk)
        else:
            old = None

        if is_new or (old and self.name != old.name):
            self.slug = slugify(self.name)

        if is_new or (old and (self.category != old.category or self.country != old.country)):
            cat_prefix = CATEGORY_SKU_PREFIX.get(self.category.id, "WHT")
            country_code = self.country.code
            uid = str(uuid.uuid4().int)[:5]
            self.sku = f"{cat_prefix}-{country_code}-{uid}"

        super().save(*args, **kwargs)