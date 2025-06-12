from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=3, unique=True, null=True, blank=True)
