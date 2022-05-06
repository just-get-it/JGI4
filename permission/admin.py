from django.contrib import admin
from .models import section,orders_permission,staff_permissions,vendor_permissions
# Register your models here.



from django.db import models
class section_admin(admin.ModelAdmin):
	list_display=['name','order_section','standard_form','standard_document']
	list_filter=('order_section','standard_form','standard_document',)

class orders_permission_admin(admin.ModelAdmin):
	list_display=['name']
	list_filter=('staff_category','seller_category','customer',)
	



admin.site.register(section,section_admin)

admin.site.register(orders_permission,orders_permission_admin)
admin.site.register(staff_permissions)
admin.site.register(vendor_permissions)