from django.contrib import admin
from .models import Fabric,CostingRate,Order,Plan,Measurments,Garment
# Register your models here.

admin.site.register(Fabric)
admin.site.register(CostingRate)
admin.site.register(Order)
admin.site.register(Plan)
admin.site.register(Measurments)
admin.site.register(Garment)


