from django import forms


class ShippingForm(forms.Form):
    customer_first_name = forms.CharField(max_length=100, required=True)
    customer_last_name = forms.CharField(max_length=100, required=True)
    customer_email = forms.EmailField(required=True)
    customer_phone = forms.CharField(max_length=11, required=True)
    country = forms.CharField()
    city = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=255, required=True)
