



from django.contrib import admin
from .models import company_detail,company_Order,quantity_b2b,assortment,address_model,color_model
# Register your models here.
from .models import activities,notifications,activities_Category,bom,quality_deflection,quality_evaluation


from .models import custom_Form_Attribute,custom_Form,custom_Form_Data,design_theme,packing_list,color_model,packing_list_1,new_pl,plqty
from .models import carton,macro_Activities,costing,Carton_new,size_color_quantity,list_types,warehouse_list,logistic_list,dispatch_list,distribution_list_1
from .models import cartons_list,esclation_home,consumer_Order_Quantity,budget_month,Dependent_attr,inDependent_attr
from .models import coloums,excel,trims_orders,order_status,size_status,manuals,budget_sectors,sector_run_rate
from .models import (budget_years,
budget_month,
budget_sectors,
sector_month_weight,
budget_model,
budget_model_sector)
from import_export import resources
from import_export.admin import ImportExportModelAdmin
admin.site.register(size_color_quantity)
admin.site.register(Carton_new)
admin.site.register(new_pl)
admin.site.register(list_types)
admin.site.register(warehouse_list)
admin.site.register(dispatch_list)
admin.site.register(distribution_list_1)
admin.site.register(logistic_list)
admin.site.register(Dependent_attr)
admin.site.register(inDependent_attr)
admin.site.register(plqty)
class sizeAdmin(admin.ModelAdmin):
	list_display=['brand','size']

# admin.site.register(color_model)
admin.site.register(size_status)
admin.site.register(packing_list_1)
admin.site.register(order_status)
class comapany_detail_Admin(admin.ModelAdmin):
	search_fields=('name',)
admin.site.register(company_detail,comapany_detail_Admin)
admin.site.register(address_model)
admin.site.register(color_model)


class CompanyOrderResource(resources.ModelResource):
	class Meta:
		model = company_Order
		fields = (
			'user_email','quantity','dispatch_Address','billing_Address',
			'quoted_Price','alteration_Charge','single_unit_Price','order_no','order_type',
			'target_lead_time','target_price','logo_placement','description'
		)
		export_order = ('user_email','quantity','dispatch_Address','billing_Address',
			'quoted_Price','alteration_Charge','single_unit_Price','order_no','order_type',
			'target_lead_time','target_price','logo_placement','description')



class comapany_Order_Admin(ImportExportModelAdmin):
	resource_class = CompanyOrderResource
	search_fields = ('order_no',)
admin.site.register(company_Order,comapany_Order_Admin)
# admin.site.register(size_Data,sizeAdmin)
# admin.site.register(brand)
# admin.site.register(production_Order)

class quantity_b2b_Admin(admin.ModelAdmin):
	search_fields=('quantity',)


admin.site.register(quantity_b2b,quantity_b2b_Admin)


class assortment_Admin(admin.ModelAdmin):
	search_fields=('order_no',)

admin.site.register(assortment,assortment_Admin)



class macro_Activities_Admin(admin.ModelAdmin):
	search_fields=('title',)
admin.site.register(macro_Activities,macro_Activities_Admin)


class carton_Admin(admin.ModelAdmin):
	search_fields=('maximum_quantity',)



admin.site.register(carton,carton_Admin)

class activities_Admin(admin.ModelAdmin):
	search_fields=('slug',)

admin.site.register(activities,activities_Admin)

admin.site.register(notifications)
admin.site.register(design_theme)
admin.site.register(quality_deflection)
admin.site.register(quality_evaluation)


admin.site.register(cartons_list)
# class acti_cateAdmin(admin.ModelAdmin):
# 	list_display=['title','staff_category','seller_category','position','type_of_order']
#
#
#
# admin.site.register(activities_Category,acti_cateAdmin)


# from core.models import Book

class BookResource(resources.ModelResource):

	class Meta:
		model = activities_Category
		fields = (
			'id','sequence', 'title',
			'description','seller_category',
			'position', 'type_of_order',
			'Increment_or_Decrement', 'lead_Time_for_120_Days',
			'lead_Time_for_105_Days', 'lead_Time_for_90_Days',
			'lead_Time_for_75_Days', 'lead_Time_for_60_Days',
			'lead_Time_for_45_Days', 'lead_Time_for_30_Days',
			'lead_Time_for_15_Days', 'lead_Time_for_7_Days',
			'lead_Time_for_3_Days', 'escalation_Time_for_Executive',
			'escalation_Time_for_Manager', 'escalation_Time_for_Head'
		)
		export_order = ('id','sequence', 'title', 'description','seller_category', 'position', 'type_of_order', 'Increment_or_Decrement', 'lead_Time_for_120_Days', 'lead_Time_for_105_Days', 'lead_Time_for_90_Days', 'lead_Time_for_75_Days', 'lead_Time_for_60_Days', 'lead_Time_for_45_Days', 'lead_Time_for_30_Days', 'lead_Time_for_15_Days', 'lead_Time_for_7_Days', 'lead_Time_for_3_Days', 'escalation_Time_for_Executive', 'escalation_Time_for_Manager', 'escalation_Time_for_Head')

from .models import activities_Category


class BookAdmin(ImportExportModelAdmin):
	resource_class = BookResource
	list_display=['title','staff_category','seller_category','position','type_of_order']

admin.site.register(activities_Category, BookAdmin)



admin.site.register(bom)

class custom_Form_Attribute_Admin(admin.ModelAdmin):
	filter_horizontal=('staff_Category_Edit_Permissions','seller_Category_Edit_Permissions',
	'individual_User_Edit_Permissions','staff_Category_View_Permissions',
	'seller_Category_View_Permissions','individual_User_View_Permissions')



admin.site.register(custom_Form_Attribute,custom_Form_Attribute_Admin)
admin.site.register(custom_Form)
admin.site.register(custom_Form_Data)
admin.site.register(packing_list)



admin.site.register(esclation_home)
admin.site.register(consumer_Order_Quantity)
admin.site.register(coloums)
admin.site.register(excel)
admin.site.register(trims_orders)
admin.site.register(manuals)

admin.site.register(costing)



admin.site.register(budget_sectors)
admin.site.register(sector_run_rate)


admin.site.register(budget_month)

admin.site.register(budget_years)
admin.site.register(sector_month_weight)
admin.site.register(budget_model)
admin.site.register(budget_model_sector)
