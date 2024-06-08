from django import forms
from .models import ProductMst, ProductSubCat

class ProductMstForm(forms.ModelForm):
    class Meta:
        model = ProductMst
        fields = ['product_name']

class ProductSubCatForm(forms.ModelForm):
    class Meta:
        model = ProductSubCat
        fields = ['product', 'product_price', 'product_image', 'product_model', 'product_ram']
