from django.db import models
from account.models import CustomUser


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField(max_length=200)
