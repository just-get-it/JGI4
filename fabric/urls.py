from django.urls import path
from . import views

urlpatterns=[
	path("inhouse/",views.inhouse,name="inhouse"),
	path("subInhouse/",views.subInhouse,name="subInhouse"), 
	path("inhousesummary/",views.inhouse_summary,name="inhouse_summary"),
	path("po/",views.po,name="po"),
	path("grn/",views.grn,name="grn"),
	path("orderselect/",views.inspection_order_select,name="order_select"),
	path("inspection/",views.inspection_order_update,name="ajaxcallinsorder"),
	path("inspection_roll/",views.inspection_order_update_2,name="ajaxcallinslot"),
	path("inspection/",views.inspection,name="inspection_fabric"),
	path("update_roll/",views.update_roll,name="up_roll"),
	path("inspectiondb/",views.inspection_database_form3,name="inspectiondb"),
    path("inspectionsummary/",views.inspection_summary,name="inspectionsummary"),
	path("acceptedlotentries/",views.acceptedlotentries,name="acceptedlotentries"),
	path("acceptedlotentries_order/",views.acceptedlotentries_order,name="acceptedlotentries_order"),
	path("acceptedlotentries_request/",views.acceptedlotentries_request,name="acceptedlotentries_request"),
	path("ajaxcallinssummary/",views.inspection_order_summary,name="ajaxcallinspection12"),
	path("app_summary/",views.approve_summary,name="acceptedinventory"),
	path("reject_summry/",views.reject_summary,name="rejectedinventory"),
	path("inventory/",views.inventory,name="inventory"),
	path("inventory_request/",views.inventory_request,name="inventory_request"),
	path("fabinventoryreturnapprove/",views.fabinventoryreturnapprove,name="fabinventoryreturnapprove"),
	path("fabinventoryreturnsupplier/",views.fabinventoryreturnsupplier,name="fabinventoryreturnsupplier"),
	path("inventoryreturn/",views.inventory_return,name="inventoryreturn"),
	path("inventoryreturns/",views.inventory_r_summary,name="viewinventorystatusfab"),
	path("inventoryreturnsupplier/",views.inventoryreturnsupplier,name="inventoryreturnsupplier"),
	path("inventoryreturnapprove/",views.inventoryreturnapprove,name="inventoryreturnapprove"),
	
]