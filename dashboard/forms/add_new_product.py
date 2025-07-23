from django import forms
from shop.models import Product
from common.models import Category

class AddProductForm(forms.ModelForm):
    stock = forms.IntegerField(min_value=0, required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    image = forms.ImageField(required=False)
    brand = forms.CharField()
    class Meta:
        model = Product
        exclude = ['sku', 'slug']
        fields = ['name', 'description', 'category', 'volume', 'country', 'abv', 'original_price', 'vintage', 'image', 'discounted_price']
