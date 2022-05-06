from django.urls import path
from . import views
# SET THE NAMESPACE!
app_name = 'operators'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('home',views.index,name='index'),
    path('operators/home',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.user_login,name='user_login'),
    path('operator_window',views.window,name='operator_window'),
    path('windowreportindex',views.windowreportindex,name='windowreportindex'),
    path('windowreport',views.windowreport,name='windowreport'),
    path('reworkreport',views.reworkreport,name='reworkreport'),
    path('logout',views.logout,name='logout'),
    path('operatorskillmatrix',views.operatorskillmatrix,name='operatorskillmatrix'),
    path('takeattendence',views.takeattendence),
    path('takeleave',views.takeleave),
    path('attendreporthome',views.attendreporthome),
    path('attendreportdatewise',views.attendreportdatewise),
    path('attendencereport',views.attendencereport),
    path('leavereport',views.leavereport),
    path('dprreporthome',views.dprreporthome),
    path('dprreport',views.dprreport),
    path('operationbulletin',views.operationbulletin),
    path('maintenancereport',views.maintenancereport),
    path('smedreport',views.smedreport)
]
