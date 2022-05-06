from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.loadplan, name='loadplan'),
    path('loadplan/hello', views.loadplan, name='loadplan'),
    path('orderdetails', views.orderdetails, name='orderdetails'),
    path('availablecapacity', views.availablecapacity, name='availablecapacity'),
    path('capreqd', views.capreqd, name='capreqd'),
    path('ordtable', views.ordtable, name='ordtable'),
    path('avctable', views.avctable, name='avctable'),
    path('cprtable', views.cprtable, name='cprtable'),
    path('material', views.material, name='material'),
    path('mattable', views.mattable, name='mattable'),
    path('exp', views.exp, name='exp'),
    path('exptable', views.exptable, name='exptable'),
    path('exptable/exptable', views.exptable, name='exptable'),
    path('lg', views.lg, name='lg'),
    path('linetable', views.linetable, name='linetable')
    

]