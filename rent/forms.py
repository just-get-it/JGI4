from datetime import date

from django import forms

from .models import QuantitySizeColour
class QuantitySizeColourForm(forms.ModelForm):
    class Meta:
        model=QuantitySizeColour
        fields=['quantity','size','colour']

    #TODO for product wise colour filter
    """def __init__(self,slug=None,*arg,**kwargs):
        super(QuantitySizeColourForm,self).__init__(*arg,**kwargs)
        if slug:
            self.fields['colour'].queryset=size_colour_quantity_new.objects.filter(linked_product__slug=slug)
            self.fields['size'].queryset=size_colour_quantity_new.objects.filter(linked_product__slug=slug)"""

class StartDateAndEndDateForm(forms.Form):

    start_date=forms.DateField(required=True,show_hidden_initial=date.today(),help_text="YYYY-MM-DD")
    end_date=forms.DateField(required=True,help_text="YYYY-MM-DD")
