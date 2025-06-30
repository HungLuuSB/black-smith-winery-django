from django.db import models
from .custom_user import CustomUser


class Address(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="addresses"
    )
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
