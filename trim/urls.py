from django.urls import path
from . import views

urlpatterns=[
	path("triminhouse/",views.inhouse,name="triminhouse"),
	path("subtriminhouse/",views.inhousedb,name="subtriminhouse"),
	path("sumtriminhouse/",views.inhousesummary,name="summaryinhouse"),
	path("triminspection/",views.triminspection,name="triminspection"),
	path("tupdateinspection/",views.updateorderinspection,name="updateorderinspection"),
	path("tinspection2/",views.tinspection2,name="tinspection2"),
	path("tinspectiondb/",views.tinspectiondb,name="tinspectiondb"),
	path("tinspectionsummary/",views.tinspectionsummary,name="tinspsummary"),
	path("triminventory/",views.triminventory,name="triminventory"),
	path("triminventorystatus/",views.viewinventorystatus,name="viewinventorystatus"),
	path("tappinven/",views.tapproveinven,name="tappinven"),
	path("trejinven/",views.trejectinven,name="trejinven"),
	path("triminventoryapproved/",views.triminventoryapproved,name="triminventoryapproved"),
	path("triminventoryrejected/",views.triminventoryrejected,name="triminventoryrejected"),
	path("trimiinventoryreturn/",views.trimiinventoryreturn,name="trimiinventoryreturn"),
	path("updateobj/",views.updateobj,name="updateobj"),
	path("tinreturnapp/",views.tinreturnapp,name="tinreturnapp"),
	path("tinreturnsupp/",views.tinreturnsupp,name="tinreturnsupp"),
	
]
