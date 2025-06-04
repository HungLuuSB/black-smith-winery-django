from django import forms
from shop.models import Product

class AddNewProductForm(forms.ModelForm):
    stock_quantity = forms.IntegerField()
    brand = forms.CharField()
    country = forms.CharField()
    class Meta:
        model = Product
        exclude = ['sku', 'slug']
        fields = ['name', 'description', 'category', 'volume',
                  'abv', 'price', 'vintage', 'image']
