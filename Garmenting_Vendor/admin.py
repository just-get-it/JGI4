



from django.contrib import admin




# Register your models here.
from .models import kpi,kpi_data,production_Product,production_Line,floated_orders



admin.site.register(kpi)
admin.site.register(kpi_data)
admin.site.register(production_Product)
admin.site.register(production_Line)
# admin.site.register(floated_orders)