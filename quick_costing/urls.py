
from django.urls import path
from .views import home,createOrder,orderDetail,loadFabric,measurments

urlpatterns = [
    path('', home, name='quick_costing_home'),
    path('orderDetail/<slug>',orderDetail,name='quick_costing_order_detail'),
    path('measurments/<slug>',measurments,name='quick_costing_measurments'),
    path('createOrder/',createOrder,name='quick_costing_create_order'),
    path('ajax/load-fabrics/',loadFabric, name='ajax_load_fabrics'),

]
