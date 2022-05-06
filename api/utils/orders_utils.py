


from b2b.models import company_Order
from django.core import serializers



def getOrderDesc(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no)
	if order:
		data={
			"access":True,
			"order":list(order.values())
		}
		
		return data
	else:
		return {}


def getOrderStaffAllocation(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}

def getProductionOrder(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}

def getSizeAssortment(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}

def getMeasurementChart(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}

def getOrderForms(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}

def getOrderDocuments(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}

def getStaffContacts(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}

def getAssortmentPermissions(request,details,order_no):
	order=company_Order.objects.filter(order_no=order_no).first()
	if order:
		pass
	else:
		return {}
