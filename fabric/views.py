from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Inhouse,Inspection,ApproveInventory,RejectInventory,order_roll
from django.urls import reverse
import random
from userdetail.models import detail
from sew.models import GenerateOB
from product.models import trims_Category
# Create your views here.
def inhouse(request):
	user=detail.objects.all().filter(vendor=True)
	ono=GenerateOB.objects.all()
	goodsop=trims_Category.objects.all()
	return render(request,'vendor/inhouse.html',{'sup':user,'gdop':goodsop,'ono':ono})

def subInhouse(request):
	if(request.method=='POST'):
		f=Inhouse()
		f.date=request.POST["date1"]
		f.po=request.POST["po"]
		f.orderNo=int(request.POST["insP"])
		f.supplier=request.POST["supplier"]
		f.lotNo=int(request.POST["lotNo"])
		f.goods=request.POST["goods"]
		f.numRolls=int(request.POST["numRolls"])
		f.qty=int(request.POST["qty"])
		f.save()
		RnumRolls = f.numRolls + 1
		org=order_roll.objects.filter(orderNo=f.orderNo).last()
		if not org:
			var=1
			for i in range(1,RnumRolls):
				print("Banadiya kyuki Nahi tha") 
				f_ob=order_roll()
				f_ob.orderNo=f.orderNo
				f_ob.rollNoop=var #Today's Change
				print(f_ob.rollNoop)
				f_ob.lotNo=f.lotNo
				var=var+1
				f_ob.status=0
				f_ob.save()
		else:
			vari=org.rollNoop
			vari=vari+1
			for i in range(1,RnumRolls):
					print("Banadiya par pehle bhi tha") 
					f_ob=order_roll()
					f_ob.orderNo=f.orderNo
					f_ob.rollNoop=vari #Today's Change
					print(f_ob.rollNoop)
					f_ob.lotNo=f.lotNo
					vari=vari+1
					f_ob.status=0
					f_ob.save()
	return HttpResponseRedirect(reverse("inhouse"))

def inhouse_summary(request):
	object=Inhouse.objects.all()
	return render(request,'vendor/inhouse_summary.html',{'f':object})


def inspection_order_select(request):
	object=Inhouse.objects.all()
	menu = list()
	for x in object:
		m = x.orderNo
		menu.append(m)
	final=list(dict.fromkeys(menu))
	return render(request,'vendor/inspection_fabric.html',{'f':object,'x':final})

def inspection_order_select(request):
	object=Inhouse.objects.all()
	menu = list()
	for x in object:
		m = x.orderNo
		menu.append(m)
	final=list(dict.fromkeys(menu))
	return render(request,'vendor/inspection_fabric.html',{'f':object,'x':final})

def inspection_order_update(request):
	print("update1")
	order_no = int(request.POST.get('orderNo',''))
	print(order_no)
	object=Inhouse.objects.all().filter(orderNo=order_no)
	print(object)
	mine=list()
	for ob in object:
		lot = ob.lotNo
		mine.append(lot)	
	print(mine)
	for ob in object:
		if ob.orderNo==order_no:
			return render(request,'vendor/inspection_fabric.html',{'f':object,"mine":mine,'f2':ob,'xd':order_no})
	return HttpResponseRedirect(reverse("inspection_fabric"))

def inspection_order_update_2(request):
	print("update2")
	order_no = int(request.POST.get('ird',''))
	lotNo = request.POST.getlist('test','')
	Nroll=0
	for x in lotNo:
		obje = Inhouse.objects.filter(orderNo=order_no, lotNo=x)
		for os in obje:
			Nroll = Nroll+os.numRolls
			print(Nroll)
	object=Inhouse.objects.filter(orderNo=order_no)
	print("kaam kar Rha hai")
	for ob in object:
		print("hello")
		if ob.orderNo==order_no:
			return render(request,'vendor/inspection_fabric.html',{'f':object,"order_no":order_no,"roll":Nroll,"lot":lotNo,'f2':ob})
	return HttpResponseRedirect(reverse("inspection_fabric"))

def update_roll(request):
	Rorder_no = int(request.POST.get('hid_on','')) # Order No
	RnumRolls= int(request.POST.get('numRolls','')) #No. Of Rolls
	Rins= float(request.POST.get('insP','')) # Inspection Value
	RinsPer = float(request.POST.get('hid_random','')) #Count after calculation
	loopval=int(RinsPer) # Integer Formatted Count 	
	print(loopval)
	lot= request.POST.getlist('ltno','') # lot No
	print(lot)
		
	list=[]
	inh_ob=0
	for lotn in lot:
		inh_ob=Inhouse.objects.get(orderNo=Rorder_no,lotNo=lotn)
		object=order_roll.objects.filter(orderNo=Rorder_no,lotNo=lotn,status=0) # Today's change
		for ob in object:
			RinsP=ob.rollNoop
			list.append(RinsP)
			import random
			random.shuffle(list)
			random.shuffle(list)
			random.shuffle(list)
			random.shuffle(list)
			print(list)
		del list[loopval:]
	return render(request,'vendor/inspection_fabric2.html',{'Rorder_no': Rorder_no,"list":list,"rolls":RnumRolls,'RinsP':Rins,"lottt":lot,'inh_ob':inh_ob})

def inspection_database_form3(request):
	if(request.method=='POST'):
		f=Inspection()
		f.orderNo=int(request.POST["orderNo"])
		print(f.orderNo)
		f.supplier=request.POST["supplier"]
		f.rollNo=int(request.POST["rollnum"])
		print(f.rollNo)
		val = request.POST["lotNo"]
		for x in val:
			x = order_roll.objects.filter(orderNo=f.orderNo,rollNoop=f.rollNo)
			for ln in x:
				say=ln.lotNo
		f.lotNo = int(say)
		f.totalRolls=int(request.POST["numRolls"])
		f.inspectionPer=float(request.POST["insPer"])
		f.fabrictype=request.POST["fType"]
		f.desType==request.POST["desType"]
		f.repeat_size=float(request.POST["repeat_size"])
		f.fabricshade=request.POST["fabShade"]
		f.acceptancePointYard=int(request.POST["acceptP1"])
		f.acceptancePointMeter=int(request.POST["acceptP2"])
		f.fabricWidth=float(request.POST["fWidth"])
		f.unit1=request.POST["units"]
		f.wv1=float(request.POST["wv1"])
		f.wv2=float(request.POST["wv2"])
		f.wv3=float(request.POST["wv3"])
		f.srl=float(request.POST["slength"])
		f.unit2=request.POST["units2"]
		f.arl=float(request.POST["alength"])
		f.unit3=request.POST["units3"]
		f.deviation=float(request.POST["deviation"])
		f.unit4=request.POST["units4"]
		f.nod=request.POST["idNo_hid"]
		f.lp=int(request.POST["totalPoints"])
		f.hp=int(request.POST["hp"])
		f.tp=int(request.POST["tlp"])
		f.shadeVar=request.POST["shadevar"]
		f.shadeGrade=request.POST["shadegrade"]
		f.CSV=request.POST["shadecsv"]
		f.pphuny=float(request.POST["p100"])
		f.pphunm=float(request.POST["p100m"])
		f.shrinkage=float(request.POST["shper"])
		f.fgrade=request.POST["fgrade"]
		f.result=request.POST["resultNo_hid"]
		f.test=request.POST["test"]
		f.save()
		print("success")
		list_roll=request.POST.getlist("test1","")
	listt=[]
	print(list_roll)
	for x in list_roll:
		x = int(x)
		if x==f.rollNo:
			print("Naaa")
		else:
			listt.append(x)
	print(listt)
	#Changing status of a roll number for particular order as done
	object=order_roll.objects.get(orderNo=f.orderNo,lotNo=f.lotNo,rollNoop=f.rollNo)
	object.status=1
	object.save()
	data={
			"ord":f.orderNo,
			"supp":f.supplier,
			"looot":val,
			"total":f.totalRolls,
			"insper":f.inspectionPer,
			"fab":f.fabrictype,
			"list":listt,
			"repeat":f.repeat_size,
			"shade":f.fabricshade,
			"acpy":f.acceptancePointYard,
			"acpm":f.acceptancePointMeter,
			'fwidth':f.fabricWidth,
			"unit1":f.unit1,
			"wv1":f.wv1,
			"wv2":f.wv2,
			"wv3":f.wv3,
			"sr1":f.srl,
			"unit2":f.unit2,
			"arl":f.arl,
			"unit3":f.unit3,
			"deviation":f.deviation,
			"unit4":f.unit4,
			"node":f.nod,
			"lp":f.lp,
			"hp":f.hp,
			"tp":f.tp,
			"shadevar":f.shadeVar,
			"shadeGrade":f.shadeGrade,
			"csv":f.CSV,
			"pphuny":f.pphuny,
			"pphunm":f.pphunm,
			"shrinkage":f.shrinkage,
			"fgrade":f.fgrade,
		}
	return render(request,'vendor/inspection_fabric2.html',data)
	
def inspection_summary(request):
	object=Inhouse.objects.all()
	return render(request,'vendor/inspection_summary.html',{'f':object})


def inspection_order_summary(request):
	oer_no = int(request.POST.get('orderNo',''))
	object=Inspection.objects.all().filter(orderNo=oer_no)
	orderlist=Inhouse.objects.all()
	return render(request,'vendor/inspection_summary.html',{'f21':object,'f':orderlist})

def insert_approve_in(ob):
	f=ApproveInventory()
	f.orderNo=ob.orderNo
	f.supplier=ob.supplier
	f.lotNo=ob.lotNo
	f.rollNo=ob.rollNo
	f.fabrictype=ob.fabrictype
	f.fabricshade=ob.fabricshade
	f.arl=ob.arl
	f.unit3=ob.unit3
	f.fabricWidth=ob.fabricWidth
	f.unit1=ob.unit1
	f.wv1=ob.wv1
	f.wv2=ob.wv2
	f.wv3=ob.wv3
	f.fgrade=ob.fgrade
	f.CSV=ob.CSV
	f.shadeGrade=ob.shadeGrade
	f.shadeVar=ob.shadeVar
	f.shrinkage=ob.shrinkage
	f.save()

def approve_summary(request):
	object=ApproveInventory.objects.all()
	return render(request,'vendor/acceptedinventory.html',{'f':object})

def reject_approve_in(ob):
	f=RejectInventory()
	f.orderNo=ob.orderNo
	f.supplier=ob.supplier
	f.lotNo=ob.lotNo
	f.rollNo=ob.rollNo
	f.fabrictype=ob.fabrictype
	f.fabricshade=ob.fabricshade
	f.arl=ob.arl
	f.unit3=ob.unit3
	f.fabricWidth=ob.fabricWidth
	f.unit1=ob.unit1
	f.wv1=ob.wv1
	f.wv2=ob.wv2
	f.wv3=ob.wv3
	f.fgrade=ob.fgrade
	f.CSV=ob.CSV
	f.shadeGrade=ob.shadeGrade
	f.shadeVar=ob.shadeVar
	f.shrinkage=ob.shrinkage
	f.status="On Hold"
	f.save()

def reject_summary(request):
	object=RejectInventory.objects.all()
	return render(request,'vendor/rejectedinventory.html',{'f':object})

def inventory_return(request):
	object=RejectInventory.objects.all().filter(status="On Hold")
	return render(request,'vendor/inventory_return.html',{'f11':object})

def inventory_r_summary(request):
	Rorder_no = int(request.POST.get("orderNo"))
	object=RejectInventory.objects.all().filter(status="On Hold")
	ob=RejectInventory.objects.all().filter(orderNo=Rorder_no)
	return render(request,'vendor/inventory_return.html',{'f11': object,'f':ob,'orno':Rorder_no})


def inventoryreturnsupplier(request):
	Rorder_no = int(request.POST.get("oNo_hid"))
	#print("Received nov ",Rorder_no)
	ob=RejectInventory.objects.all().filter(orderNo=Rorder_no)
	for obj in ob:
		obj.status="sent back to supplier"
		obj.save()
	object=RejectInventory.objects.all().filter(status="On Hold")
	return render(request,'vendor/inventory_return.html',{'f11': object})

def inventoryreturnapprove(request):
	Rorder_no = int(request.POST.get("oNo_hid"))
	print("R: ",Rorder_no)
	ob=RejectInventory.objects.all().filter(orderNo=Rorder_no)
	for obj in ob:
		print("obj: ",obj.orderNo)
		obj.status="sent to approved inven"
		obj.save()
		insert_approve_in(obj)
		print("Done")
	object=RejectInventory.objects.all().filter(status="On Hold")
	return render(request,'vendor/inventory_return.html',{'f11':object})

def inventory(request):
	object=Inhouse.objects.all()
	menu = list()
	for x in object:
		m = x.orderNo
		menu.append(m)
	final=list(dict.fromkeys(menu))
	return render(request,'vendor/fabric_inventory.html',{'x':final})

def inventory_request(request):
	objt=Inhouse.objects.all()
	menu = list()
	for x in objt:
		m = x.orderNo
		menu.append(m)
	final=list(dict.fromkeys(menu))
	object=Inhouse.objects.all()
	Rorder_no = int(request.POST.get("orderNo"))
	print(Rorder_no)
	ob=Inspection.objects.all().filter(orderNo=Rorder_no,test="Accept")
	print(ob)
	if not ob:
		print("Khaali")
		return render(request,'vendor/fabric_inventory.html',{'x':object,'f':ob,'orno':Rorder_no})
	else:
		acy = 0
		acm=0
		pphuny=0
		pphunm=0
		count=0
		var = 0
		for x in ob:
			if x.orderNo==Rorder_no:
				acy = acy + int(x.acceptancePointYard)
				acm = acm + int(x.acceptancePointMeter)
				pphuny = pphuny + float(x.pphuny)
				pphunm = pphunm + float(x.pphunm)
				count=count+1
		acy = acy/count
		acm = acm/count
		pphuny = pphuny/count
		pphunm = pphunm/count
		print(acy)
		print(acm)
		print(pphuny)
		print(pphunm)
		print(count)
		z = count+1
		if pphuny<=acy:
			var = "Accepted"
		else:
			var = "Not Accepted"
		return render(request,'vendor/fabric_inventory.html',{"objt":final,'x':object,'f':ob,"z":z,"acy":acy,"acm":acm,"pphuny":pphuny,"pphunm":pphunm,'orno':Rorder_no,"var":var})

def fabinventoryreturnapprove(request):
	object=Inhouse.objects.all()
	Rorder_no = int(request.POST.get("oNo_hid"))
	print("R: ",Rorder_no)
	ob=Inspection.objects.all().filter(test="Accept")
	for obj in ob:
		print("obj: ",obj.orderNo)
		print("hello")
		obj.status="sent to approved inven"
		obj.result="Accepted"
		obj.test="Dont Accept"
		obj.save()
		insert_approve_in(obj)
		print("Done")
	return render(request,'vendor/fabric_inventory.html',{"x":object})

def fabinventoryreturnsupplier(request):
	object=Inhouse.objects.all()
	Rorder_no = int(request.POST.get("oNo_hid"))
	print("R: ",Rorder_no)
	ob=Inspection.objects.all().filter(test="Accept")
	for obj in ob:
		print("obj: ",obj.orderNo)
		print("hello")
		obj.status="sent to Supplier"
		obj.test="Dont Accept"
		obj.save()
		reject_approve_in(obj)
		print("Done")
	return render(request,'vendor/fabric_inventory.html',{"x":object})

def acceptedlotentries(request):
	object=Inhouse.objects.all()
	menu = list()
	for x in object:
		m = x.orderNo
		menu.append(m)
	final=list(dict.fromkeys(menu))
	return render(request,'vendor/accepted_lots_fabric.html',{'x':final})

def acceptedlotentries_order(request):
	Rorder_no = int(request.POST.get("orderNo"))
	object=Inhouse.objects.filter(orderNo=Rorder_no)
	return render(request,'vendor/accepted_lots_fabric.html',{'object':object,'rorno':Rorder_no})


def acceptedlotentries_request(request):
	objt=Inhouse.objects.all()
	menu = list()
	for x in objt:
		m = x.orderNo
		menu.append(m)
	final=list(dict.fromkeys(menu))
	lot = int(request.POST.get("lot",""))
	print(lot)
	Rorder_no = int(request.POST.get("hide",""))
	print(Rorder_no)
	print(lot)
	object=Inhouse.objects.filter(orderNo=Rorder_no,lotNo=lot)
	object1=order_roll.objects.filter(orderNo=Rorder_no,lotNo=lot,status=0)
	ob=Inspection.objects.all().filter(orderNo=Rorder_no,lotNo=lot)
	return render(request,'vendor/accepted_lots_fabric.html',{'xr':object,"xx":final,"lot":lot,"ob1":object1,'f':ob,'orno':Rorder_no})



def po(request):
    return render(request,'vendor/po.html')

def po(request):
    return render(request,'vendor/po.html')

def inspection(request):
	return render(request,'vendor/inspection_fabric.html')


def acceptedInventory(request):
    return render(request,'vendor/acceptedInventory.html')


def rejectedInventory(request):
    return render(request,'vendor/rejectedInventory.html')

def grn(request):
    return render(request,'vendor/grn.html')
