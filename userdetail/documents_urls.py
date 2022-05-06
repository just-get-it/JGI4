
from django.contrib import admin
from django.urls import path,include

from .document_views import order_po,order_invoice,garment_po,garment_invoice,finishing_invoice,finishing_po



from .document_views import packing_invoice,packing_po,sewing_po,sewing_invoice,fabric_po,fabric_invoice
from .document_views import trim_card

urlpatterns=[
    path('order_po',order_po),
    path('order_invoice',order_invoice),
    path('garment_po',garment_po),
    path('garment_invoice',garment_invoice),
    path('finishing_invoice',finishing_invoice),
    path('finishing_po',finishing_po),
    path('packing_invoice',packing_invoice),
    path('packing_po',packing_po),
    path('sewing_po',sewing_po),
    path('sewing_invoice',sewing_invoice),
    path('fabrics_po',fabric_po),
    path('fabrics_invoice',fabric_invoice),
    path('trim_card',trim_card)

]
