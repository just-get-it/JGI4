from django.contrib import admin
from .models import Requisition, Vouchers, Minute, Wage, Mon_Minute, Factory_Overhead, Administrative_Expenses, Commercial_Expenses,Financial_Expenses,Direct_Wage
# Register your models here.
admin.site.register(Requisition)
admin.site.register(Vouchers)
admin.site.register(Wage)
admin.site.register(Minute)
admin.site.register(Mon_Minute)
admin.site.register(Factory_Overhead)
admin.site.register(Administrative_Expenses)
admin.site.register(Commercial_Expenses)
admin.site.register(Financial_Expenses)
admin.site.register(Direct_Wage)