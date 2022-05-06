



from django.contrib import admin
from .models import interests
# Register your models here.
from mptt.admin import MPTTModelAdmin

from .models import *



admin.site.register(interests)
admin.site.register(post)
admin.site.register(like)
admin.site.register(interest_users)
# admin.site.register(comment)
# admin.site.register(comment_likes)
# admin.site.register(comment_reply)
# admin.site.register(comment_reply_likes)
admin.site.register(followers)
admin.site.register(friend)
admin.site.register(Comment, MPTTModelAdmin)