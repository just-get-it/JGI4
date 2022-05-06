from django import forms
from .models import *

# class ShippingAddress(models.Model):
#     order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     user = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=100)
#     shipping_address = models.CharField(max_length=255)
#     city = models.CharField(max_length=200)
#     state = models.CharField(max_length=200)
#     pin_code = models.CharField(max_length=200)
#     is_saved = models.BooleanField(default=False)
STATE_CHOICES = (
                ('', 'Select state'),
                ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
                ('Andhra Pradesh', 'Andhra Pradesh'), #First one is the value of select option and second is the displayed value in option
                ('Arunachal Pradesh', 'Arunachal Pradesh'),
                ('Assam', 'Assam'),
                ('Bihar', 'Bihar'),
                ('Chandigarh', 'Chandigarh'),
                ('Chhattisgarh', 'Chhattisgarh'),
                ('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
                ('Daman and Diu', 'Daman and Diu'),
                ('Delhi','Delhi'),
                ('Goa', 'Goa'),
                ('Gujarat', 'Gujarat'),
                ('Haryana', 'Haryana'),
                ('Himachal Pradesh', 'Himachal Pradesh'),
                ('Jammu and Kashmir','Jammu and Kashmir'),
                ('Jharkhand', 'Jharkhand'),
                ('Karnataka', 'Karnataka'),
                ('Kerala', 'Kerala'),
                ('Ladakh', 'Ladakh'),
                ('Lakshadweep', 'Lakshadweep'),
                ('Madhya Pradesh', 'Madhya Pradesh'),
                ('Maharashtra', 'Maharashtra'),
                ('Manipur', 'Manipur'),
                ('Meghalaya', 'Meghalaya'),
                ('Mizoram', 'Mizoram'),
                ('Nagaland', 'Nagaland'),
                ('Odisha', 'Odisha'),
                ('Punjab', 'Punjab'),
                ('Puducherry','Puducherry'),
                ('Rajasthan', 'Rajasthan'),
                ('Sikkim', 'Sikkim'),
                ('Tamil Nadu', 'Tamil Nadu'),
                ('Telangana', 'Telangana'),
                ('Tripura', 'Tripura'),
                ('Uttar Pradesh', 'Uttar Pradesh'),
                ('Uttarakhand', 'Uttarakhand'),
                ('West Bengal', 'West Bengal'),
                )


class shipping_address_form(forms.ModelForm):
    class Meta():
        model = ShippingAddress
        fields = ('name','phone','shipping_address', 'city', 'state', 'pin_code')
        widgets = {
           'state': forms.Select(choices=STATE_CHOICES),
        }
        labels = {
            'name': 'Name',
            'phone': 'Phone No.',
            'shipping_address': 'Address',
            'city': 'City',
            'state': 'State / Province',
            'pin_code': 'Pincode',
        }


# class size_color_quantity_form(forms.ModelForm):
#     delete = forms.BooleanField()
#     class Meta():
#         model = size_color_quantity
#         fields = ('size', 'unit', 'color', 'price', 'c_price', 'quantity', 'safety_stock_limit')
#         widgets = {
#             'color': TextInput(attrs={'type': 'color'}),
#         }
#     def __init__(self, *args, **kwargs):
#         super(size_color_quantity_form, self).__init__(*args, **kwargs)
#         self.fields['delete'].required = False
#         self.fields['size'].required = True
#         self.fields['unit'].required = True
#         self.fields['color'].required = True
#         self.fields['price'].required = True
#         self.fields['c_price'].required = True
#         self.fields['quantity'].required = True
#         self.fields['safety_stock_limit'].required = True