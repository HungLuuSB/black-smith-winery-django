from django.db import models
import string
import random
from decimal import Decimal

def generate_unique_code(length=10):
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not Voucher.objects.filter(code=code).exists():
            return code
        
class Voucher(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    min_order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        super().save(*args, **kwargs)

    def apply_discount(self, sub_total):
        if self.discount_percent:
            return min(self.discount_percent, sub_total)
        elif self.discount_percent:
            return Decimal(sub_total) * (self.discount_percent / Decimal(100))
        return Decimal(0)