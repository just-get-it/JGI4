from django import forms
from .models import diet
from datetime import datetime


class dietform(forms.ModelForm): 
    class Meta:
        model =diet
        fields =[
            'copy',
            'Product',
            'type'
        ]
        widgets ={
            'copy':forms.TextInput(),
            'Product':forms.TextInput(),
            'type':forms.TextInput()
        }
    
    