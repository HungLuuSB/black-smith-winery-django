from django.db import models
from account.models import CustomUser


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_cart(request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key or request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart

    def add_item(self, product, quantity=1):
        item, created = self.items.get_or_create(product=product)
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def remove_item(self, product):
        self.items.filter(product=product).delete()

    def clear(self):
        self.items.all().delete()

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def get_items(self):
        return self.items.all()
