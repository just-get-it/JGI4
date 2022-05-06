from django.contrib import admin
from .models import Ord, Avc, Cpr, Mat, Lio

# Register your models here.

admin.site.register(Ord)
admin.site.register(Avc)
admin.site.register(Cpr)
admin.site.register(Mat)
admin.site.register(Lio)