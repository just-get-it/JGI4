from django.contrib import admin
from .models import category,sub_category,super_category,product,attribute,bestoffer,units
# Register your models here.
from .models import PFM_Components, PFM_Attributes, FabricDetails, StyleDetails,MachineType,StyleType,Fabric,WashType,product


from .models import trims_Attribute,trims_Category,trims_product,product_cate_b2b,size_color_quantity,trims_product_quantity
from .models import labels_Object,labels_Attributes,standard_fabric_blend,care_symbols,washcare_model,label_dropdowns, trims_label_attributes, garment_consumption_formula, garment_matching_parameters
from .models import label_Attributes_Values, Department,Section,subsection, garment_matching_requirements, repeat_size
from .models import *
from django.forms import CheckboxSelectMultiple
from multiselectfield import MultiSelectField
# class subcateAdmin(admin.ModelAdmin):
# 	list_display=['name','product_Category']
# 	list_filter=('product_Category',)



# class supercateAdmin(admin.ModelAdmin):
# 	list_display=['name','product_Subcategory','product_Category']
# 	list_filter=('product_Subcategory','product_Category',)


class Add_imagesAdmin(admin.TabularInline):
    model = Add_images

class productAdmin(admin.ModelAdmin):
	list_display=['title','product_code','slug','get_options']
	formfield_overrides = {
        MultiSelectField: {'widget': CheckboxSelectMultiple},
    }

	inlines = [Add_imagesAdmin,]
admin.site.register(product, productAdmin)


class product_cate_b2b_Admin(admin.ModelAdmin):
	list_display=['name','show_on_homepage']



class fabric_blend_admin(admin.ModelAdmin):
	list_display=['name','standard']
	list_filter=('standard',)


class label_dropdownsAdmin(admin.ModelAdmin):
	list_display=['attribute','attribute_value']
	list_filter=('attribute',)
	list_editable=['attribute_value',]

class label_attributesAdmin(admin.ModelAdmin):
	list_display = ['label', 'name']
	list_filter = ('label',)

class attributeAdmin(admin.ModelAdmin):
	list_display=['name','pfm_component']
	list_filter=('pfm_component',)

class repeatSizeAdmin(admin.ModelAdmin):
	list_display = ['fabric_direction', 'fabric_print_design', 'fabric_width', 'fabric_print_type', 'garment_matching_parameters']

@admin.register(sub_category)
class sub_category(admin.ModelAdmin):
	list_display=['name','id','get_product_Category' ]


admin.site.register(PFM_Components)
admin.site.register(PFM_Attributes, attributeAdmin)
admin.site.register(FabricDetails)
admin.site.register(StyleDetails)

admin.site.register(category)
# admin.site.register(sub_category)
admin.site.register(super_category)
admin.site.register(units)
# admin.site.register(product,productAdmin)
admin.site.register(attribute)
admin.site.register(product_cate_b2b,product_cate_b2b_Admin)
admin.site.register(bestoffer)
admin.site.register(trims_Attribute)
admin.site.register(trims_Category)
admin.site.register(trims_product)
admin.site.register(size_color_quantity)
admin.site.register(trims_product_quantity)
admin.site.register(labels_Object)
# admin.site.register(labels_Attributes,label_attributesAdmin)
admin.site.register(labels_Attributes)
admin.site.register(standard_fabric_blend,fabric_blend_admin)
admin.site.register(care_symbols,fabric_blend_admin)
admin.site.register(washcare_model)
admin.site.register(label_dropdowns,label_dropdownsAdmin)
admin.site.register(trims_label_attributes)
admin.site.register(MachineType)
admin.site.register(Department)
admin.site.register(Section)
admin.site.register(subsection)
admin.site.register(StyleType)
admin.site.register(WashType)
admin.site.register(Fabric)
admin.site.register(garment_consumption_formula)
admin.site.register(garment_matching_parameters)
admin.site.register(garment_matching_requirements)
admin.site.register(service_add)
admin.site.register(product_group_type)
admin.site.register(repeat_size, repeatSizeAdmin)
# admin.site.register(service_add)
admin.site.register(fabric_print_type)
admin.site.register(fabric_width)
admin.site.register(fabric_print_design)
admin.site.register(fabric_direction)
admin.site.register(Orders)
admin.site.register(history)
admin.site.register(add_wallet)
admin.site.register(remove_wallet)
admin.site.register(developer_attributes)
admin.site.register(all_units)
admin.site.register(extradetails)
admin.site.register(product_common_attribute_values)
admin.site.register(Add_images)
admin.site.register(FormAttributes)
admin.site.register(OtherBrands)
admin.site.register(OtherLabel)
admin.site.register(TermAndCondition)
admin.site.register(ProductReview)
admin.site.register(label_Attributes_Values)
admin.site.register(option_tags)