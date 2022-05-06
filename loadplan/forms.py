from django import forms
from .models import Cpr

class CprForm(forms.ModelForm):
    class Meta:
        model=Cpr
        fields = [
            'orderno',
            'ltlc',
            'orderqty',
            'smv',
            'crm',
            'capd',
            'crd'
        ]
   
