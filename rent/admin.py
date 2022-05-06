from django.contrib import admin
from .models import RentPlan,RentingCost,QuantityAndDuration,ProductInRentCart,RentOrder,QuantitySizeColour


admin.site.register(RentPlan)
admin.site.register(RentingCost)

admin.site.register(QuantityAndDuration)

admin.site.register(ProductInRentCart)
admin.site.register(RentOrder)
admin.site.register(QuantitySizeColour)