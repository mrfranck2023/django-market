from django import forms
from .models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'barcode', 'price', 'stock']
        labels = {
            'name': 'Nom du Produit',
            'barcode': 'Code-barres',
            'price': 'Prix',
            'stock': 'Stock',
        }
