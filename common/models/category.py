from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    sku_prefix = models.CharField(max_length=10, null=True, blank=True)
