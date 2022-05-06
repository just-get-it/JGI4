from django.contrib import admin
from clone.models import new_events,old_events,current
# Register your models here.
admin.site.register(new_events)
admin.site.register(old_events)
admin.site.register(current)


