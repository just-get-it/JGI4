from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    product_category_op = [
        ("all", "*ALL"),
        ("shirts", "Shirts"),
        ("trousers", "Trousers"),
        ("jeans", "Jeans"),
        ]
    operation_choice= [
    ('dart stitch', 'Dart Stitch'),
    ('panel attach', 'Panel Attach'),
    ('chest welt attach', 'Chest Welt Attach'),
    ('facing att', 'Facing Att'),
    ('chest canvas attach', 'Chest Canvas Attach'),
    ('side seam', 'Side Seam'),
    ]
    line_choice= [
    (1,1),(2,2),(3,3),(4,4),(5,5),
    ]
    operator_name=forms.CharField()
    operator_id=forms.CharField()
    line_no=forms.CharField(label='Select Line no',
    	widget=forms.Select(choices=line_choice))
    address=forms.CharField()
    product_category=forms.MultipleChoiceField(
            choices=product_category_op,
            initial='0',
            widget=forms.SelectMultiple(),
            required=True,
            label='Product Category',
        )
    product_sub_category=forms.CharField()
    operation=forms.CharField(label='Select Operation',
    	widget=forms.Select(choices=operation_choice))
    operation_complexity=forms.CharField()
    no_of_operation=forms.CharField()
    skill_percentage=forms.CharField()
    grade=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('operator_name','operator_id','line_no','address','product_category','product_sub_category'
        ,'operation','operation_complexity','no_of_operation','skill_percentage','grade','password')

class windowForm(forms.ModelForm):
    operation= [
    ('dart stitch', 'Dart Stitch'),
    ('panel attach', 'Panel Attach'),
    ('chest welt attach', 'Chest Welt Attach'),
    ('facing att', 'Facing Att'),
    ('chest canvas attach', 'Chest Canvas Attach'),
    ('side seam', 'Side Seam'),
    ]
    opcurrentstatus= [
    ('sewing', 'Sewing'),
    ('helping to other', 'Helping To Other'),
    ('drinking water', 'Drinking Water'),
    ('personal', 'Personal'),
    ('washroom', 'Washroom'),
    ('pressing', 'Pressing'),
    ]
    operatorcurrentstatus=forms.CharField(label='Select Current Status',
    	widget=forms.Select(choices=opcurrentstatus))
    operation=forms.CharField(label='Select Operation',
    	widget=forms.Select(choices=operation))
    class Meta():
        model=User
        fields=('operatorcurrentstatus','operation')
