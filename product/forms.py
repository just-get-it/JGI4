from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import product


class FormForRenting(forms.Form):
    is_rent=forms.BooleanField(required=False)
    is_heavy=forms.BooleanField(required=False)
    is_garment=forms.BooleanField(required=False)


class UploadProductForm(ModelForm):
    
    class Meta:
        model = product
        # fields = ['product_Category', 'product_Subcategory', 
        #         'product_Supercategory', 'title', 'price', 'offer', 'B2Boffer',  
        #         'privacy', 'bestoffers', 'product_cate', 'brand', 'label', 'fit', 
        #         'season', 'washcare', 'barcode', 'terms', 'product_tags', 'sold_quantity',
        #         'image1', 'manufacturername', 'manufacturerno', 'volume', 'weight', 
        #         'batteriesincluded']
        exclude = ['slug']