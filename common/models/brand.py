from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(unique=True,blank=True)
