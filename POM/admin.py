






from django.contrib import admin
from .models import POM,measurement,size_labels,measurement_chart, size_assortment_pattern
from .models import inch_size_label,roman_size_label,uk_size_label,conversion_chart_map,conversion_chart
# Register your models here.


class POM_admin(admin.ModelAdmin):
    list_display=['label','product_Category','product_Subcategory','product_Supercategory']
    list_filter=('product_Subcategory','product_Category','product_Supercategory',)

class measurement_admin(admin.ModelAdmin):
    list_display = ['label','fit','season', 'product_Category', 'product_Supercategory']
    list_filter = ['label','fit','season', 'product_Category', 'product_Supercategory']

# admin.site.register(POM,POM_admin)
admin.site.register(POM)
admin.site.register(measurement,measurement_admin)
admin.site.register(size_labels)
admin.site.register(measurement_chart)


admin.site.register(inch_size_label)
admin.site.register(roman_size_label)
admin.site.register(uk_size_label)
admin.site.register(conversion_chart_map)
admin.site.register(conversion_chart)

class sizeAssortment(admin.ModelAdmin):
	list_display = ['sector', 'product_Category', 'product_Subcategory', 'product_Supercategory']


admin.site.register(size_assortment_pattern, sizeAssortment)

