from django.db import models
from .order import Order


class Payment(models.Model):
    order = models.OneToOneField(
        "order.Order", on_delete=models.CASCADE, related_name="payment"
    )
    method = models.CharField(
        max_length=50, choices=[("bank_transfer", "Bank Transfer")]
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed")],
        default="Pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
