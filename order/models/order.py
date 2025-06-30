from django.db import models
from common.models import Country
from account.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=11)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    shipping_address = models.CharField(max_length=255)
    grand_total = models.DecimalField(decimal_places=2, max_digits=12)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
