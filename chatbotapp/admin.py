from django.contrib import admin


from chatbotapp.models import Complaint, Rating


# Register your models here.
admin.site.register(Complaint)
admin.site.register(Rating)
