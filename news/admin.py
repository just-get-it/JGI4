from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import News, NewsComment

# Register your models here.
admin.site.register(News)
admin.site.register(NewsComment, MPTTModelAdmin)
