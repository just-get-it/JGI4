from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(rental_Plan)
admin.site.register(rental_Order)
admin.site.register(rental_OrderItem)