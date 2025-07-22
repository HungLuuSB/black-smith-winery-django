from django import forms
from common.models import Country, Category
from shop.models import Product

class EditProductForm(forms.ModelForm):
    stock = forms.IntegerField(min_value=0, required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Product
        exclude = ['sku', 'slug']
        fields = ['name', 'description', 'category', 'volume',
                  'abv', 'price', 'vintage', 'image']