
from django.contrib import admin
from .models import labels,fits,seasons,trimcard_sections,manual_documents



# Register your models here.



admin.site.register(labels)
admin.site.register(fits)
admin.site.register(seasons)
admin.site.register(trimcard_sections)
admin.site.register(manual_documents)