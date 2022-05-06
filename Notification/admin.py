from django.contrib import admin

# Register your models here.



from .models import Notification_Modes,Offset




class notification_admin(admin.ModelAdmin):
	list_display=['name','turn_on']





admin.site.register(Notification_Modes,notification_admin)
# admin.site.register(Offset)