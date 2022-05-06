from django.contrib import admin

from cut.models import CutLoadPlan, IssueDetails, TableCapacityLeft, AvailCapacity, RollOrder, Fabric

# Register your models here.

admin.site.register(Fabric)
admin.site.register(RollOrder)
admin.site.register(CutLoadPlan)
admin.site.register(AvailCapacity)
admin.site.register(IssueDetails)
admin.site.register(TableCapacityLeft)
