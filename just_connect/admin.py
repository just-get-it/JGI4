from django.contrib import admin
from .models import *

class ProductBookingInline(admin.TabularInline):
    model = ProductBooking
    extra = 2 #How many rows to show

class PostProductPricingAdmin(admin.ModelAdmin):
    inlines = (ProductBookingInline,)

#inline project tags  
class ProjectTagsInline(admin.TabularInline):
    model = ProjectTags

#creating Project model admin for projectTagsinline
class ProjectTagsConfiguration(admin.ModelAdmin):
    inlines = [ProjectTagsInline,]



admin.site.register(User)
admin.site.register(PostPollPoints)
admin.site.register(Bookmark)
admin.site.register(PostType)
admin.site.register(Post)
admin.site.register(PostPoll)
admin.site.register(PostComment)
admin.site.register(CommercialProductPoints)
admin.site.register(PostProductPricing,PostProductPricingAdmin)
admin.site.register(Image)
admin.site.register(Album)
admin.site.register(Ad)
admin.site.register(Group)
admin.site.register(Page)
admin.site.register(Events)
admin.site.register(Report)
admin.site.register(News)
admin.site.register(NewsComment)
admin.site.register(Portfolio_Project,ProjectTagsConfiguration)
admin.site.register(ProjectCategory)
