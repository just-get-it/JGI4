




from django import forms
from product.models import category,sub_category,super_category,product


class category_form(forms.ModelForm):
	class Meta:
		model = category
		fields ='__all__'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)




class subcategory_form(forms.ModelForm):
	class Meta:
		model = sub_category
		fields ='__all__'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class supercategory_form(forms.ModelForm):
	class Meta:
		model = super_category
		fields ='__all__'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class product_form(forms.ModelForm):
	class Meta:
		model = product
		fields ='__all__'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
