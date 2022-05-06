






from django.contrib import admin
#from .models import detail,seller_Categories,staff_Categories,brand,response_time,weekdays,list_of_holidays,access_perm
# Register your models here.
from .models import *


class detailAdmin(admin.ModelAdmin):
	list_display=['name','buisness_Customer','seller_category','staff_category','position']






admin.site.register(detail,detailAdmin)
admin.site.register(staff_Categories)
admin.site.register(seller_Categories)
admin.site.register(brand)
admin.site.register(academic)
admin.site.register(professional_pro)
admin.site.register(social)
admin.site.register(medical)
admin.site.register(diseases)
admin.site.register(age)
admin.site.register(height)
admin.site.register(weight)
admin.site.register(quantity)
admin.site.register(frequency)
admin.site.register(shift)
admin.site.register(diet_product)
admin.site.register(diet_plan)

admin.site.register(Resumes)
admin.site.register(response_time)

admin.site.register(list_of_holidays)
admin.site.register(access_perm)
admin.site.register(weekdays)

admin.site.register(productorder)
# admin.site.register(weekdays)

admin.site.register(service_certifications)
admin.site.register(serviceorder)

admin.site.register(customizeorder)
admin.site.register(order_frequency)
admin.site.register(subscriptionorder)
admin.site.register(Subscription_Order)
admin.site.register(Subscription_Stop)

admin.site.register(pick_and_deliver_order)
admin.site.register(add_degree)
admin.site.register(add_field_of_study)
admin.site.register(add_skill)
admin.site.register(add_project)
admin.site.register(add_certifications)
admin.site.register(customer_address)
admin.site.register(profile_status_update)
admin.site.register(distribution_center)
admin.site.register(staff_additional_features)
admin.site.register(seller_additional_features)
