"""Diet_plan URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from . import views

from app1 import views as vs
from nutrition import views
from .views import healthy_diet,index,diet_plan,user_health_profile,check_nutri,update_view,update_pla,updt_diet1,check_csv,diet_csv,diet_csv1,otherdiet
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="home"),
    path('healthy_diet/',healthy_diet,name="healthy_diet"),
    path('diet_plan/',diet_plan,name="diet_plan"),
    path('user_health_profile/',user_health_profile,name="user_health_profile"),
    path('check_nutri/',check_nutri,name="check_nutri"),
    path('check_csv/',check_csv,name="check_csv"),
    path('diet_csv/',diet_csv,name="diet_csv"),
    path('nutrition/', views.AllProduct,name="nutrition"),
    path('livesearch', views.livesearch, name='livesearch'),
    # re_path(r'^product?$', views.product, name='product'),
    path('nutrient', views.nutrient, name='nutrient'),
    # re_path(r'^ajax_calls/search/', views.autocompleteModel),
    path('updt/<int:pk>',update_view,name="updt_diet"),
    path('updtdietp/<int:pk>',update_pla,name="updt_diet2"),
    path('updt1/<int:id>',updt_diet1,name="updt_diet1"),
    path('diet_csv1/',diet_csv1,name="diet_csv1"),
    path('otherdiet/<int:id>',otherdiet,name="otherdiet")
]