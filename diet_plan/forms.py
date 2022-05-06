from django import forms
from .models import diet, diet_detail
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
    
class dietform1(forms.ModelForm): 
    class Meta:
        model =diet_detail
        fields =[
            't_periods',
            'regio',
            'seaso',
            'type',
            'disease'
        ]
        widgets ={
            't_periods':forms.TextInput(),
            'regio':forms.TextInput(),
            'seaso':forms.TextInput(),
            'type':forms.TextInput(),
            'disease':forms.TextInput(),
        }

       