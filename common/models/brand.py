from django.db import models
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(unique=True,blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)