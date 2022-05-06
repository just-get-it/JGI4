"""movintrendz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include


from .views import buisness_index,buisness_timeline,activate,buisness_profile

from .views import placeorder,buisness_order,order_update,confirm_alteration,placeenquiry,placesample,placedesign
from .views import sampling,ordering,buisness_profile_staff,consumer_profile,consumer_profile_products

from .views import activities_upload,design,buisness_order_list,buisness_profile_notifications,consumer_list,consumer_detail
from .views import consumer_request,excel_settings,buisness_packing_list,buisness_distribution_list,buisness_cummlative_list
from .views import buisness_order_po,buisness_order_invoice,buisness_products,buisness_products_detail,consumer_profile_products_detail
from .views import custom_assortment,bulk_order_upload, bulk_order_bom_upload, buisness_fabrics_id,load_sizeTable, load_style, auto_fill
from .views import calculate_total_fabric_consumption
urlpatterns = [
   path('',buisness_index),
   path('buisness_timeline/',buisness_timeline),
   path('activate',activate),
   path('products',buisness_products),
   path('products/<int:prod_id>',buisness_products_detail),
   path('buisness_profile/',buisness_profile),

   path('placeorder/<int:order_no>', placeorder),
   path('placeorder/', placeorder),
   path('loadStyle', load_style),
   path('loadTable', load_sizeTable),
   path('autoFill', auto_fill),
   path('calculate_total_fabric_consumption', calculate_total_fabric_consumption),

   path('buisness_order',buisness_order_list),
   path('buisness_order/<int:order_no>',buisness_order),
   path('order_update/<int:order_no>',order_update),
   path('confirm_alteration/',confirm_alteration),
   path('enquiry/',placeenquiry, name="business_enquiry"),
   path('design/',placedesign, name="business_design"),
   path('sampling/',placesample, name="sampling"),
   path('bulk_order_upload/',bulk_order_upload),
   path('bulk_order_bom_upload', bulk_order_bom_upload),
   path('fabrics_id', buisness_fabrics_id),
   path('buisness_order/<int:order_no>/consumer_list',consumer_list),
   path('buisness_order/<int:order_no>/custom_assortment',custom_assortment),
   path('buisness_order/<int:order_no>/consumer_list/<str:consumer_email>',consumer_detail),
   path('buisness_order/<int:order_no>/sampling',sampling),
   path('buisness_order/<int:order_no>/ordering',ordering),
   path('buisness_order/<int:order_no>/design',design),
   path('buisness_order/<int:order_no>/forms/packing_list',buisness_packing_list),
   path('buisness_order/<int:order_no>/forms/distribution_list',buisness_distribution_list),
   path('buisness_order/<int:order_no>/forms/cummlative_list',buisness_cummlative_list),
   path('buisness_order/<int:order_no>/order_documents/order_po',buisness_order_po),
   path('buisness_order/<int:order_no>/order_documents/order_invoice',buisness_order_invoice),
   path('buisness_profile/notifications',buisness_profile_notifications),
   path('buisness_profile/excel_settings',excel_settings),
   path('buisness_profile/<str:email>',buisness_profile_staff),
   path('activities_upload',activities_upload),
   path('consumer_profile',consumer_profile, name="b2b_consumer"),
   path('consumer_profile/request',consumer_request),
   path('consumer_profile/products',consumer_profile_products),
   path('consumer_profile/products/<int:order_no>',consumer_profile_products_detail),
]
