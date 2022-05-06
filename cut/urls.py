from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

	path('allocation_form/', views.allocation_form, name='allocation_form'),
	path('Data_Submission_Form/', views.Data_Submission_Form, name='Data_Submission_Form'),
	path('rollallocation/', views.show_allocation, name='rollallocation'),
	path('rollallocation2/', views.show_allocation2, name='rollallocation2'),
	path('temp/', views.temp, name='temp'),
	path('cuttingloadplan', views.cut, name='cut'),
	path('clp/', views.clp, name='clp'),
	path('capaleft/', views.capaleft, name='capaleft'),
	path('availcapacity/', views.availcapacity, name='availcapacity'),
	path('issuedetails/', views.issuedetails, name='issuedetails'),
	path('dailyspreadandcut', views.dailyspreadandcut, name='dailyspreadandcut'),
	path('fabricissue', views.fabricissue, name='fabricissue'),
	path('weekfabricreq', views.weekfabricreq, name='weekfabricreq'),
]
