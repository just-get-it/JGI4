from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Post, BlogComment
# Register your models here.
admin.site.register(Post)
admin.site.register(BlogComment, MPTTModelAdmin)
