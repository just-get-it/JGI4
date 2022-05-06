from django.urls import path
from inputform import views

urlpatterns = [
    path('',views.home,name='home'),   
    
   
]
