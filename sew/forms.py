from django import forms
from django.forms import ModelForm

#from .models import Category, SubCategory, SuperCategory,AddOperations
from .models import AddOperations# Attributes, Components, OrderDetails,Obgenerate
from .admin import *
from product.models import FabricDetails, StyleDetails


class pfm(forms.ModelForm):

    class Meta:
        model = FabricDetails
        fields = '__all__'
        fields_order = ['pfmno','Fabric', 'WashType', 'category', 'subcategory', 'supercategory', 'StyleType']




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class operations(forms.ModelForm):
    
    class Meta:
        model = AddOperations
        fields = '__all__'
        fields_order = ['pfmno', 'component', 'component_type', 'department', 'section', 'sub_section', 'operations', 'spi', 'stitch_length', 'thread_consumption', 'machine_auto', 'work_aid', 'spi_factor', 'shade', 'grade','asmv', 'psmv', 'thread_spec', 'pick_time', 'main_time', 'turn_time','dispose_time','operation_complexity', 'spi_complexity', 'stitch_complexity', 'personal','fatique', 'delay', 'psam', 'typee', 'pct', 'mpall', 'name', 'oph', 'act']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



# class orders(forms.ModelForm):
#     class Meta:
#         model = OrderDetails
#         fields = '__all__'
#         fields_order = ['orderno', 'stno', 'lineno', 'order_quantity', 'mins_shift', 'capacity', 'expected_skill_level',
#                         'target', 'fabric', 'wash', 'category', 'subcategory', 'supercategory', 'styletype', 'comp',
#                         'attribute']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


# class obgen(forms.ModelForm):
#     class Meta:
#         model = Obgenerate
#         fields = ['orderno','styleno','operations', 'complexity', 'spi', 'stitch_length', 'thread_consumption', 'machine_auto', 'work_aid',
#                   'smv', 'allowance', 'sam', 'ct', 'grade', 'mpno', 'mpalloc', 'Name', 'oph', 'oph']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


