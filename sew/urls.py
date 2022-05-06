from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

	path('home', views.sew, name='sew'),
    path('sew/home', views.sew, name='sew'),
    path('generatepfm', views.generatepfm, name='generatepfm'),
    path('operations', views.operat, name='operat'),
    path('obgenerate', views.orderform, name='obgen'),
    path('obgenerateform3', views.obgenerateform3, name='obgenform3'),
    path('form4',views.form4, name='form4'),
     path('obulletin',views.show, name='show')



	# path(r'form1/', views.form1, name='form1'),
	# path(r'form2/', views.form2, name='form2'),
]
