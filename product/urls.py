



from django.contrib import admin
from django.urls import path,include
from . import views
from .views import products,productdetails,product_edit
from .views import fetch, sub_fetch, sup_fetch,brand_fetch, specifications_fetch, fetch_page, fetch_pricerange


urlpatterns = [
   path('',products),
   path('<str:slug>/',productdetails, name="product_detail"),
   path('<str:slug>/edit',product_edit),
   path('products/update_item/', views.updateItems, name="update_item"),
   path("fetch", fetch),
   path("sub_fetch", sub_fetch),
   path("sup_fetch", sup_fetch),
   path("brand_fetch", brand_fetch),  
   path("specifications_fetch", specifications_fetch), 
   path("fetch_page", fetch_page),
   path("fetch_pricerange", fetch_pricerange),   
]   

