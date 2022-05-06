from django.urls import path
from output_reports import views

urlpatterns=[
    path('reports',views.outputreports,name='reports'),

] 