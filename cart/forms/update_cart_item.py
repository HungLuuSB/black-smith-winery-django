from django import forms


class UpdateCartItemForm(forms.Form):
    def __init__(self, *args, cart=None, **kwargs):
        super().__init__(*args, **kwargs)
        if cart is not None:
            for item in cart.items.all():
                field_name = f"quantity_{item.id}"
                self.fields[field_name] = forms.IntegerField(
                    label=f"{item.product.name} quantity",
                    min_value=0,
                    initial=item.quantity,
                )
