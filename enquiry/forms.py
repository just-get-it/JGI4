from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from product.models import *

class enquiry_form(forms.ModelForm):
    class Meta:
        model = enquiry_port
        fields = '__all__'
