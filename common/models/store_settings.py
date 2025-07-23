from django.db import models

class StoreSettings(models.Model):
    vat_rate = models.DecimalField(max_digits=5,decimal_places=2, default=8.00)
    shipping_fee = models.DecimalField(max_digits=5,decimal_places=2, default=10.00)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        return cls.objects.get_or_create(pk=1)[0]