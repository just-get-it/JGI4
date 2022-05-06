from django import forms
from django.contrib.admin import widgets                                       
from django.contrib.auth.models import User
from userdetail.models import pick_and_deliver_order
from cart.models import *
from django.forms import CheckboxSelectMultiple
from product.models import extradetails, product, Add_images, size_color_quantity, label_Attributes_Values
from django.forms.widgets import TextInput


class update_product_form(forms.ModelForm):
    class Meta():
        model = product
        fields = ('price', 'title', 'product_Category'
            , 'product_Subcategory', 'product_Supercategory', 'title', 'slug', 'brand', 'label'
            , 'seller', 'price', 'offer', 'bestoffers', 'image1',  'made_in', 'old_product', 'packed', 'Service'
            , 'barcode', 'gst','sold_quantity', 'available_for_subscription','B2Boffer'
                # updating work upto this
            , 'product_cate', 'privacy', 'product_tags', 'safe_stock', 'keywords', 'sale', 'salediscount'
            , 'salestartdate', 'saleenddate', 'notes', 'description', 'manufacturername', 'manufacturerno', 'length'
            , 'width', 'height', 'batteriesincluded', 'batteriesno', 'wattage', 'features', 'graphics', 'powersource',
                # work upto this
        )

class update_label_attr_form(forms.ModelForm):
    class Meta():
        model = label_Attributes_Values
        fields=('label_attribute', 'value',)
    def __init__(self, *args, **kwargs): 
        super(update_label_attr_form, self).__init__(*args, **kwargs)                       
        self.fields['label_attribute'].disabled = True
        self.fields['value'].required = False

class update_attr_form(forms.Form):
    label_attr = forms.CharField()
    attr_value = forms.CharField()

class size_color_quantity_form(forms.ModelForm):
    delete = forms.BooleanField()
    class Meta():
        model = size_color_quantity
        fields = ('size', 'unit', 'color', 'price', 'c_price', 'quantity', 'safety_stock_limit')
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
    def __init__(self, *args, **kwargs):
        super(size_color_quantity_form, self).__init__(*args, **kwargs)
        self.fields['delete'].required = False
        self.fields['size'].required = True
        self.fields['unit'].required = True
        self.fields['color'].required = True
        self.fields['price'].required = True
        self.fields['c_price'].required = True
        self.fields['quantity'].required = True
        self.fields['safety_stock_limit'].required = True

class add_images_form(forms.ModelForm):
    delete = forms.BooleanField()
    class Meta():
        model = Add_images
        fields = ('image','is_actual')
    def __init__(self, *args, **kwargs):
        super(add_images_form, self).__init__(*args, **kwargs)
        self.fields['delete'].required = False

class new_images_form(forms.ModelForm):
    class Meta():
        model = Add_images
        fields = ('image', 'prod')

class deliverycreation(forms.ModelForm):
    

    class Meta:
        model=pick_and_deliver_order
        fields='__all__'
# class editorderitem(forms.ModelForm):
#     class Meta:
#         model=OrderItem
#         fields='__all__'
# class editorderr(forms.ModelForm):
#     class Meta:
#         model=Order
#         fields='__all__'
# class editshippingaddress(forms.ModelForm):
#     class Meta:
#         model=ShippingAddress
#         fields='__all__'
# class orderform(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(orderform, self).__init__(*args, **kwargs)
#         self.fields['assigntoafterrejection'].queryset=detail.objects.filter(vendor=True)
#         self.fields['assigntoafterrejection'].widget = CheckboxSelectMultiple()
#     class Meta:
#         model = OrderItem
#         fields=['assigntoafterrejection',]

# class deliveryform(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(deliveryform, self).__init__(*args, **kwargs)
#         logi=staff_Categories.objects.filter(name="Logistic").first()
#         self.fields['deliveryassigntoafterrejection'].queryset=detail.objects.filter(staff_category=logi)
#         self.fields['deliveryassigntoafterrejection'].widget = CheckboxSelectMultiple()
#     class Meta:
#         model = pick_and_deliver_order
#         fields=['deliveryassigntoafterrejection',]

class ProductForm(forms.ModelForm):
    class Meta:
        model=product
        fields='__all__'

class ExtraDetailsForm(forms.ModelForm):
    class Meta:
        model=extradetails
        fields='__all__'

class ImageForm(forms.ModelForm):
    class Meta:
        model=Add_images
        fields='__all__'


class VariationForm(forms.ModelForm):
    class Meta:
        model=size_color_quantity
        fields='__all__'