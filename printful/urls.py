from django.contrib import admin
from django.urls import path, include
from .views import main_func, hoo, jack, tee, tank
from django.conf.urls import url

urlpatterns = [
    path('printful/', main_func,name='printful'),
    path('printful/tee', tee, name='tee'),
    path('printful/hoodie', hoo,name='hoodie'),
    path('printful/jacket', jack, name='jacket'),
    path('printful/tank', tank, name='tank'),
    #url(r'^printful/$', views.main_func, name="index-page"),
    #url(r'^Data_Submission_Form/$', views.Data_Submission_Form, name='Data_Submission_Form'),
]