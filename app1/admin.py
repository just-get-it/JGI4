from django.contrib import admin
from django.contrib import admin

# Register your models here.
from app1.models import NutritionModel,diet,diet_detail,Nutrition_item

#@admin.register(diet)
#@admin.register(diet_details)
admin.site.register(Nutrition_item)
admin.site.register(diet_detail)
admin.site.register(diet)
admin.site.register(NutritionModel)

#class ChannelsAdmin(admin.ModelAdmin):
#    list_display = ('Product','Quantity','Unit','Kcal','Protein','Carbs','Fat','type')

