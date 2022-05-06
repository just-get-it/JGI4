from django.contrib import admin

from .models import TrimInhouse,TrimInspection,TrimInventoryApproved,TrimInventoryRejected
# Register your models here.

admin.site.register(TrimInhouse)
admin.site.register(TrimInspection)
admin.site.register(TrimInventoryApproved)
admin.site.register(TrimInventoryRejected)
