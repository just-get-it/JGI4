from django import forms
from .models import Order,Fabric,Measurments

"""
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['garment','quantity','fabric','colour','size_and_quantity']
"""


class ProductForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['garment','quantity','fabric','colour']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fabric'].queryset = Fabric.objects.none()

        if 'garment' in self.data:
            try:
                garment_id = int(self.data.get('garment'))
                self.fields['fabric'].queryset = Fabric.objects.filter(garment_id=garment_id).order_by('type')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['fabric'].queryset = self.instance.garment.fabric_set

# class ProductForm(forms.Form):
# class


class MeasurmentForm(forms.ModelForm):
    class Meta:
        model=Measurments
        fields=['small','medium','large','xl','xxl']
