from django.contrib import admin
from .models import *
# Register your models here.

class orderAdmin(admin.ModelAdmin):
    list_display = ['__str__','total']

admin.site.register(Order,orderAdmin)
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(subscriptionOrderItem)
admin.site.register(subscriptionOrder)
admin.site.register(subscriptionBill)
admin.site.register(coupons)
admin.site.register(Logistics)
admin.site.register(selected_distribution_centers)
