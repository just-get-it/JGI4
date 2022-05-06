from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from userdetail.models import detail
from django.urls import reverse
from .models import TrimInhouse,order_carton,TrimInspection,TrimInventoryApproved,TrimInventoryRejected
import random
# Create your views here.
def inhouse(request):
	print("Trim Inhouse")
	user=detail.objects.all().filter(vendor=True)
	return render(request,'trim/triminhouse.html',{'sup':user})
	
def inhousedb(request):
	if(request.method=='POST'):
		f=TrimInhouse()
		f.date=request.POST["date1"]
		f.po=request.POST["po"]
		f.orderNo=int(request.POST["orderNo"])
		f.supplier=request.POST["supplier"]
		f.lotNo=int(request.POST["lotNo"])
		f.cat=request.POST["category"]
		f.subcat=request.POST["subcategory"]
		f.supcat=request.POST["subcategory2"]
		f.noc=int(request.POST["noC"])
		f.tqty=int(request.POST["tqty"])
		f.save()
	return HttpResponseRedirect(reverse("triminhouse"))
	
def inhousesummary(request):
	object=TrimInhouse.objects.all().order_by('orderNo')
	return render(request,'trim/triminhouse_summary.html',{'f':object})
	
def triminspection(request):
	object=TrimInhouse.objects.all().order_by('orderNo')
	return render(request,'trim/triminspection.html',{'f':object})
	
def updateorderinspection(request):
	order_no = int(request.POST.get('orderNo',''))
	object=TrimInhouse.objects.all().order_by('orderNo')
	cartonobject=order_carton.objects.all().filter(orderNo=order_no).first()
	#for ob in cartonobject:
	#print(cartonobject.orderNo)
	for ob in object:
		if ob.orderNo==order_no:
			return render(request,'trim/triminspection.html',{'f':object,'f2':ob,'cartonobject':cartonobject})
			
def tinspection2(request):
	match=0
	Rorder_no =int(request.POST["hid_on"])
	Rtotalcartons=int(request.POST["tqty"])
	RinsPer =int(request.POST["cti"])	
	carton_list=[]
	loopval=RinsPer
	class_ob=order_carton.objects.all()
	for ob in class_ob:
		if ob.orderNo==Rorder_no:
			match=11
			break
	if match!=11:
		for i in range(1,loopval):
			opt_ran=random.randint(1,Rtotalcartons)
			if opt_ran not in carton_list:
				if opt_ran < Rtotalcartons:
					carton_list.append(opt_ran)
					f_ob=order_carton()
					f_ob.orderNo=Rorder_no
					f_ob.cartonNo=opt_ran
					f_ob.status=0;
					f_ob.supplier=request.POST["supplier"]
					f_ob.lotNo=int(request.POST["lotNo"])
					f_ob.cat=request.POST["category"]
					f_ob.subcat=request.POST["subcategory"]
					f_ob.supcat=request.POST["subcategory2"]
					f_ob.noc=int(request.POST["noC"])
					f_ob.tqty=Rtotalcartons
					f_ob.aql=float(request.POST["aql"])
					f_ob.insqty=int(request.POST["insqty"])
					f_ob.qeachbox=int(request.POST["qeachbox"])
					f_ob.inspcar=RinsPer
					f_ob.save()
		object=order_carton.objects.all().filter(orderNo=Rorder_no)
		firstob=order_carton.objects.all().filter(orderNo=Rorder_no,status=0).first()
		return render(request,'trim/triminspection2.html',{'Rorder_no': Rorder_no,'cartonobject':object,'firstob':firstob})
	else:
		object=order_carton.objects.all().filter(orderNo=Rorder_no,status=0)
		firstob=order_carton.objects.all().filter(orderNo=Rorder_no,status=0).first()
		return render(request,'trim/triminspection2.html',{'Rorder_no': Rorder_no,'cartonobject':object,'firstob':firstob})

	
def tinspectiondb(request):
	if(request.method=='POST'):
		f=TrimInspection()
		f.orderNo=int(request.POST["hid_on"])
		f.cartonNo=int(request.POST["canum"])
		f.supplier=request.POST["supplier"]
		f.lotNo=int(request.POST["lotNo"])
		f.cat=request.POST["category"]
		f.subcat=request.POST["subcategory"]
		f.supcat=request.POST["subcategory2"]
		f.noc=int(request.POST["noC"])
		f.tqty=int(request.POST["tqty"])
		f.aql=float(request.POST["aql"])
		f.insqty=int(request.POST["insqty"])
		f.qeachbox=int(request.POST["qeachbox"])
		f.inspcar=float(request.POST["cti"])
		f.accp=int(request.POST["acr"])
		f.fqty=int(request.POST["faqty"])
		f.paqty=int(request.POST["paqty"])
		f.result=request.POST["rst"]
		f.grade=request.POST["gd"]
		f.status=0
		f.save()
		#Changing status of a carton number for particular order as done
		object=order_carton.objects.get(orderNo=f.orderNo,cartonNo=f.cartonNo)
		object.status=1
		object.save()
	return HttpResponseRedirect(reverse("triminspection"))

def tinspectionsummary(request):
	object=TrimInspection.objects.all().order_by('orderNo')
	return render(request,'trim/tinspection_summary.html',{'f':object})
	
	
def triminventory(request):
	object=TrimInspection.objects.filter(status=0).order_by('orderNo')
	return render(request,'trim/triminventory.html',{'f11':object})
	
def viewinventorystatus(request):
	order_no = int(request.POST.get('orderNo',''))
	object=TrimInspection.objects.filter(orderNo=order_no,status=0)
	objectall=TrimInspection.objects.filter(status=0).order_by('orderNo')
	return render(request,'trim/triminventory.html',{'f21':object,'f11':objectall,'orno':order_no})

def tapproveinven(request):
	Rorder_no = int(request.POST.get('oNo_hid',''))
	object=TrimInspection.objects.filter(orderNo=Rorder_no,status=0)
	for obj in object:
		obj.status=1
		obj.save()
		f=TrimInventoryApproved()
		f.orderNo=obj.orderNo
		f.cartonNo=obj.cartonNo
		f.supplier=obj.supplier
		f.lotNo=obj.lotNo
		f.cat=obj.cat
		f.subcat=obj.subcat
		f.supcat=obj.supcat
		f.noc=obj.noc
		f.tqty=obj.tqty
		f.aql=obj.aql
		f.accp=obj.accp
		f.fqty=obj.fqty
		f.paqty=obj.paqty
		f.result=obj.result
		f.save()
	return HttpResponseRedirect(reverse("triminventory"))
	
def trejectinven(request):
	Rorder_no = int(request.POST.get('oNo_hid',''))
	object=TrimInspection.objects.filter(orderNo=Rorder_no,status=0)
	for obj in object:
		obj.status=1
		obj.save()
		f=TrimInventoryRejected()
		f.orderNo=obj.orderNo
		f.cartonNo=obj.cartonNo
		f.supplier=obj.supplier
		f.lotNo=obj.lotNo
		f.cat=obj.cat
		f.subcat=obj.subcat
		f.supcat=obj.supcat
		f.noc=obj.noc
		f.tqty=obj.tqty
		f.aql=obj.aql
		f.accp=obj.accp
		f.fqty=obj.fqty
		f.paqty=obj.paqty
		f.result=obj.result
		f.status="On Hold"
		f.save()
	return HttpResponseRedirect(reverse("triminventory"))
	
def triminventoryapproved(request):
	object1=TrimInventoryApproved.objects.all().order_by('orderNo')
	return render(request,'trim/acceptedinventory.html',{'f':object1})
	
def triminventoryrejected(request):
	object1=TrimInventoryRejected.objects.all().order_by('orderNo')
	return render(request,'trim/rejectedinventory.html',{'f':object1})
	
def trimiinventoryreturn(request):
	object=TrimInventoryRejected.objects.filter(status="On Hold").order_by('orderNo')
	return render(request,'trim/trim_inventory_return.html',{'f11':object})
	
def updateobj(request):
	Rorder_no = int(request.POST.get("orderNo"))
	object=TrimInventoryRejected.objects.filter(status="On Hold",orderNo=Rorder_no)
	object2=TrimInventoryRejected.objects.filter(status="On Hold").order_by('orderNo')
	return render(request,'trim/trim_inventory_return.html',{'f21':object,'f11':object2,'P_onum':Rorder_no})
	
def tinreturnapp(request):
	Rorder_no = int(request.POST.get("oNo_hid"))
	object1=TrimInventoryRejected.objects.filter(status="On Hold",orderNo=Rorder_no)
	for object in object1:
		object.status="sent to approved inven"
		object.save()
		f=TrimInventoryApproved()
		f.orderNo=object.orderNo
		f.cartonNo=object.cartonNo
		f.supplier=object.supplier
		f.lotNo=object.lotNo
		f.cat=object.cat
		f.subcat=object.subcat
		f.supcat=object.supcat
		f.noc=object.noc
		f.tqty=object.tqty
		f.aql=object.aql
		f.accp=object.accp
		f.fqty=object.fqty
		f.paqty=object.paqty
		f.result=object.result
		f.save()
	object1=TrimInventoryRejected.objects.filter(status="On Hold").order_by('orderNo')
	return render(request,'trim/trim_inventory_return.html',{'f11':object1})
	
def tinreturnsupp(request):
	Rorder_no = int(request.POST.get("oNo_hid"))
	object1=TrimInventoryRejected.objects.filter(status="On Hold",orderNo=Rorder_no)
	for object in object1:
		object.status="sent back to supplier"
		object.save()
	object1=TrimInventoryRejected.objects.filter(status="On Hold").order_by('orderNo')
	return render(request,'trim/trim_inventory_return.html',{'f11':object1})