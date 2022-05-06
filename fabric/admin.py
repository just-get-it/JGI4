from django.contrib import admin
from .models import Inhouse,Inspection,ApproveInventory,RejectInventory
# Register your models here.

admin.site.register(Inhouse)
admin.site.register(Inspection)
admin.site.register(ApproveInventory)
admin.site.register(RejectInventory)


