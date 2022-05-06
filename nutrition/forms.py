from django import forms
from django.db.models.fields import CharField
from .models import Nutrition_table

class NutritionData(forms.Form):
	class meta:
		model = Nutrition_table
		fields = '__all__'
