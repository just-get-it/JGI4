
from django.urls import path
from .views import rentProductListView,rentProductDetailView,add_to_rent_cart,rentOrders,rentOrderDetailView
urlpatterns = [
    # path('products_on_rent/', rentProductListView, name='products_on_rent'),
    # path('rent_product_detail_view/<slug>', rentProductDetailView, name='rent_product_detail'),

    path('add_to_rent_cart/<slug>/<order_id>', add_to_rent_cart, name='add_to_rent_cart'),
    path('rentOrders/', rentOrders, name='rent_orders'),
    path('rentOrderDetailView/<order_id>', rentOrderDetailView, name='rent_order_DetailView'),
]

# Todo
"""
1.] See that exel sheet and add round figure that quantity and date to nearest in plan 
"""
