from django.contrib import admin
from .models import Nutrient, Nutrition_table,Diet_sheet

# Register your models here.


@admin.register(Nutrition_table)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('Product','Quantity','Unit','Kcal','Protein','Carbs','Fat','Vit_A','Vit_B1','Vit_B2','Vit_B3','Vit_B5','Vit_B6','Vit_B9','Vit_B12','Vit_C','Vit_D','Vit_E','Vit_K','Choline','Calcium','Copper','Iron','Magnesium','Manganese','Phosphorus','Potassium',
'Selenium','Sodium','Zinc','Water','Fiber','Cholesterol','Saturated_fat','MonoUns_fat','PolyUns_fat','Sugars','Glycemic_Index','Comments','Translation_product_name','Price')

@admin.register(Nutrient)
class nutrientAdmin(admin.ModelAdmin):
    list_display = ("NutrientName", "Nutrient_key", "Nutrient_unit")



@admin.register(Diet_sheet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_name','Preferrence','protein','carbs','fat')

