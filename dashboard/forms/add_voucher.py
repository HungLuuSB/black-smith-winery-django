from django import forms
from order.models import Voucher

class AddVoucherForm(forms.ModelForm):
    min_order_total = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    class Meta:
        model = Voucher
        fields = ['discount_percent', 'min_order_total', 'valid_from', 'valid_to']