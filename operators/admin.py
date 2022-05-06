from django.contrib import admin
from .models import UserProfileInfo,OperatorWindow,User,operator_skill_matrix,line1attendence,line2attendence,line3attendence,line4attendence,line5attendence,leaveCalender
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(OperatorWindow)
admin.site.register(operator_skill_matrix)
admin.site.register(line1attendence)
admin.site.register(line2attendence)
admin.site.register(line3attendence)
admin.site.register(line4attendence)
admin.site.register(line5attendence)
admin.site.register(leaveCalender)
