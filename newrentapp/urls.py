
from django.urls import path
from .views import *
urlpatterns = [
    path('products_on_rent/', rentProductListView, name='products_on_rent'),
    path('rent_product_detail_view/<slug>', rentProductDetailView, name='rent_product_detail'),

]

# Todo
"""
1.] See that exel sheet and add round figure that quantity and date to nearest in plan 
"""
