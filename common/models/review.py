from django.db import models
from account.models import CustomUser


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
