





from django.contrib import admin
from django.contrib.admin.filters import FieldListFilter
from .models import Automation_Banners, Automation_Banners_Image, Automation_Card, Automation_Cardimg, Body_image_category, Consulting_Banners, Consulting_Banners_Image, Consulting_Card, Consulting_Cardimg, HomePage_Banners,Body_image, Add_Page,Homepage_Banners_Image, Homepage_Card, Homepage_cardimg, Manufacturing_Banners, Manufacturing_Banners_Image, Manufacturing_Card, Manufacturing_Cardimg, Sourcing_Banners, Sourcing_Banners_Image, Sourcing_Card, Sourcing_Cardimg, logo,address,licence,homepage_link,homepage_crousel,discount_corousel1,discount_corousel2,message,B2B_discount_corousel1,B2B_discount_corousel2,B2B_homepage_crousel
# Register your models here.

class Homepage_cardimgAdmin(admin.ModelAdmin):
	list_display = ('name','card')
	search_fields = ['name','card']
	filter_horizontal = ()
	list_filter = ['card']
	# fieldsets = ['card']
admin.site.register(Homepage_cardimg,Homepage_cardimgAdmin)

class logoAdmin(admin.ModelAdmin):
	list_display=['name','default']


class addressAdmin(admin.ModelAdmin):
	list_display=['name','default']




	
admin.site.register(logo,logoAdmin)
admin.site.register(address,addressAdmin)
admin.site.register(licence)
admin.site.register(homepage_link)
admin.site.register(homepage_crousel)
admin.site.register(discount_corousel1)
admin.site.register(discount_corousel2)
admin.site.register(B2B_homepage_crousel)
admin.site.register(B2B_discount_corousel1)
admin.site.register(B2B_discount_corousel2)
admin.site.register(HomePage_Banners)
admin.site.register(Homepage_Banners_Image)
admin.site.register(Homepage_Card)

admin.site.register(Add_Page)
admin.site.register(Consulting_Banners)
admin.site.register(Consulting_Banners_Image)
admin.site.register(Consulting_Card)
admin.site.register(Consulting_Cardimg)
admin.site.register(Sourcing_Banners)
admin.site.register(Sourcing_Banners_Image)
admin.site.register(Sourcing_Card)
admin.site.register(Sourcing_Cardimg)
admin.site.register(Manufacturing_Banners)
admin.site.register(Manufacturing_Banners_Image)
admin.site.register(Manufacturing_Card)
admin.site.register(Manufacturing_Cardimg)
admin.site.register(Automation_Banners)
admin.site.register(Automation_Banners_Image)
admin.site.register(Automation_Card)
admin.site.register(Automation_Cardimg)
admin.site.register(Body_image_category)
admin.site.register(Body_image)

