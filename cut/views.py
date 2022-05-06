from django.shortcuts import render
from django.http import JsonResponse
from .forms import loadplanform, issuedets, capacleft, availcapa
from .models import CutLoadPlan, IssueDetails, TableCapacityLeft, AvailCapacity, RollOrder, Fabric
from datetime import datetime
from django.contrib import messages

# Create your views here.
#Start BABLU KUMAR's work

def rollallocation(request):
	return render(request, "rollallocation.html")

def allocation_form(request):
	return render(request, "rollallocation_form.html")


def Data_Submission_Form(request):
    print("Form has been submitted successfully!")

    #Fabric_Required = request.POST["Fabric_Required"]
    Roll_No = request.POST.get('Roll_No')
    Roll_Length = request.POST.get('Roll_Length')
    Fabric_Width = request.POST.get('Fabric_Width')
    CSV = request.POST.get('CSV')
    Shade_Grade = request.POST.get('Shade_Grade')
    Shrinkage = request.POST.get('Shrinkage')
    Lay_Length = request.POST.get('Lay_Length')

    Roll_Lay_Height = Roll_Length/Lay_Length
    Utilised_Fabric = Lay_Length*Roll_Lay_Height
    End_Bits = Roll_Length-Utilised_Fabric
    #To_be_Used = request.POST['To_be_Used']
    #Roll_Allocation_Code = request.POST['Roll_Allocation_Code']

    Roll_Order = RollOrder(#Fabric_Required = Fabric_Required,
                           Roll_No = Roll_No,
                           Roll_Length = Roll_Length,
                           Fabric_Width = Fabric_Width,
                           CSV = CSV,
                           Shade_Grade = Shade_Grade,
                           Shrinkage = Shrinkage,
                           Lay_Length = Lay_Length,
                           Roll_Lay_Height = Roll_Lay_Height,
                           Utilised_Fabric = Utilised_Fabric,
                           End_Bits = End_Bits)
    Roll_Order.save()
    return render(request, "rollallocation_form.html")

def show_allocation(request):
	data = RollOrder.objects.all().values().order_by("End_Bits")
	context = {
		"objects" : data
	}
	return render(request, 'rollallocation.html', context)


def show_allocation2(request):
	data3 = RollOrder.objects.all().values().order_by("Shade_Grade", "Shrinkage", "End_Bits")
	context3 = {
		"objects3" : data3
	}

	return render(request, 'rollallocation2.html', context3)


def sub_list(x,y):
	from collections import defaultdict
	roll_list = x
	req_fab = y
	#roll_list = [120, 102, 70, 99, 117, 110, 111, 116, 101, 50, 70, 181, 200, 102, 105, 104, 112, 136, 115, 68, 89, 101]
	#req_fab = [372, 273, 217, 212, 194]

	req_rolls = [[]]
	result = defaultdict(list)

	roll_length = len(roll_list)
	fab_length = len(req_fab)
	A = 10000
	for x in range(0, fab_length):
		for i in range(roll_length + 1):
			for j in range(i + 1, roll_length + 1):
				sub = roll_list[i:j]
				sub_filt = list(filter(None, sub))
				# print(sub, end = " ")
				if sum(sub_filt) > req_fab[x] - 1:
					if (sum(sub_filt)) < A:
						A = sum(sub_filt)

		for i in range(roll_length + 1):
			for j in range(i + 1, roll_length + 1):
				sub = roll_list[i:j]
				sub_filt = list(filter(None, sub))
				# print(sum(sub_filt), sep=' ')
				if sum(sub_filt) == A:
					result[req_fab[x]] = sub_filt
					#print(req_fab[x], ":", sub_filt)
					for sl in range(0, len(sub_filt)):
						roll_list.remove(sub_filt[sl])
					# print("Deleted item: ",sub_filt[sl])
	return list(result.keys()),list(result.values()),list(roll_list)
	#print("Unused rolls: ", roll_list)
# print(result)


def temp(request):
	Fabric_Req = Fabric.objects.raw("SELECT id,Fabric_Required FROM cut_fabric")
	my_data = RollOrder.objects.all().values().order_by("Shade_Grade","Lay_No","Roll_Lay_Seq")
	tol_fabric_width = RollOrder.objects.raw("Select Fabric_Width,id FROM cut_rollorder "
											 "WHERE "
											 "Fabric_Width >= (0.0075*Fabric_Width) AND Fabric_Width <= (1.0075*Fabric_Width);")
	tol_shrinkage = RollOrder.objects.raw("Select Shrinkage FROM cut_rollorder "
											 "WHERE "
											 "Shrinkage >= (Shrinkage - 0.5) AND Shrinkage <= (Shrinkage + 0.5);")


	'''----------------------------------------DATA FOR THE FUNCTION-------------------------------------'''
	Fabric_Req_data = list(Fabric.objects.values_list("Fabric_Required", flat=True))
	Rolls_data = list(RollOrder.objects.values_list("Roll_Length", flat=True))

	final_fabrics,final_rolls,un_rolls = sub_list(Rolls_data, Fabric_Req_data)	#calling the above function and saving the required values

	for i in range(0,len(final_rolls)):
		for j in range(0, len(final_rolls[i])):
			x = final_rolls[i][j]
			#my_qry = RollOrder.objects.raw("UPDATE cut_rollorder SET Lay_No = %s WHERE Roll_Length = %s",i+1, x)
			#RollOrder.objects.raw("INSERT INTO cut_rollorder (Lay_No) VALUES = %s WHERE Roll_Length = %s", i + 1, x)
			my_qry = RollOrder.objects.filter(Roll_Length = x).update(Lay_No = i+1,Roll_Lay_Seq = j+1)

	print(un_rolls)
	'''----------------------------------------DATA FOR THE FUNCTION-------------------------------------'''

	context = {
		"fab_data" : Fabric_Req,
		"x_data" : my_data,
		"unrolls" : un_rolls
	}
	return render(request, 'temp.html', context)
#End BABLU KUMAR's work

def cut(request):
	return render(request,'hello2.html')

def dailyspreadandcut(request):
	
	return render(request, "dailyspreadandcut.html")
	
def fabricissue(request):
	
	return render(request, "fabricissue.html")

def weekfabricreq(request):
	return render(request, "weekfabricreq.html")


def availcapacity(request):
	form = availcapa(request.POST or None)

	if form.is_valid():
		print('enter loop')
		data = form.cleaned_data
		ac = AvailCapacity.objects.create(tableno=data["tableno"], tabletype=data["tabletype"], modeofspread=data["modeofspread"], modeofcut=data["modeofcut"], availcapaforspreadandcut=data["availcapaforspreadandcut"], capacityleft=data["capacityleft"], datefield=data["datefield"]);
		ac.save();
		print('done saving!')	
		messages.success(request, 'Form submission successful')

	availablecapacityobjects = AvailCapacity.objects.all().order_by("tabletype")

	context = {
		"availablecapacity" : form,
		"availablecapacityobjects" : availablecapacityobjects,
	}

	return render(request, 'availcapacity.html', context)

def capaleft(request):


	tablo = AvailCapacity.objects.all()
	orderno = CutLoadPlan.objects.all().distinct()
	capacityleftobject = TableCapacityLeft.objects.all().order_by("orderno","datefield");

	context = {
	    "orderno" : orderno,
		"tableno" : tablo,
		"capacityleftobject" : capacityleftobject, 
	}

	return render(request, 'capacityleft.html', context)

def clp(request):
	form = loadplanform(request.POST or None)
	
	if form.is_valid():
		print('enter loop')
		data = form.cleaned_data
		orn = data["orderno"]
		stn = data["styleno"]
		toq = data["totalorderquantity"]
		mp = data["markerprep"]
		tt = data["tabletype"]
		mn = data["markerno"]
		ll = data["laylength"]
		nop = data["noofplies"]
		nopie = data["noofpieces"]
		sm = data["sprsmvmanual"]
		sa = data["sprsmvautospreader"]
		cm = data["crmanual"]
		ca = data["crautospreader"]
		cs = data["cutsmvstraight"]
		cb = data["cutsmvband"]
		cnc = data["cutsmvcnc"]
		csb = data["crstraightband"]
		ccnc = data["crcnc"]
		tmm = data["totmm"]
		tma = data["totma"]
		tam = data["totam"]
		taa = data["totaa"]
		fab = data["matinhousefabric"]
		fus = data["matinhousefusing"]
		itt = data["issuetable"]

		print(data)
		clpt = CutLoadPlan.objects.create(orderno=orn, styleno=stn,totalorderquantity=toq, markerprep=mp, tabletype=tt, markerno=mn,laylength=ll, noofplies=nop, noofpieces=nopie, sprsmvmanual=sm, sprsmvautospreader=sa, crmanual=cm, crautospreader=ca, cutsmvstraight=cs, cutsmvband=cb, cutsmvcnc=cnc, crstraightband=csb, crcnc=ccnc, totmm=tmm, totma=tma, totam=tam, totaa=taa, matinhousefabric=fab, matinhousefusing=fus, issuetable=itt)
		clpt.save();
		print("ok")
		messages.success(request, 'Form submission successful')


	cutloadplanobject = CutLoadPlan.objects.all().order_by("orderno", "markerno")


	context = {
		"cutloadplan" : form,
		"cutloadplanobject" : cutloadplanobject,
	}
	return render(request, 'cutloadplan.html', context)



odn = ""
mkn = ""
tabty = ""
dt = ""
def issuedetails(request):

	orderno = CutLoadPlan.objects.all()
	tablenno = AvailCapacity.objects.all()
	issuedetailsobjects = IssueDetails.objects.all().order_by("orderno")
	context={
		"orderno" : orderno,
		"tableno" : tablenno,
		"issuedetailsobjects": issuedetailsobjects,
	}

	if request.POST.get('ordernoo'):
		global odn
		oder = request.POST.get('ordernoo')
		odn = oder
		dat = CutLoadPlan.objects.filter(orderno=oder).values_list('styleno', flat=True)
		dat_list = list(dat)
		print(dat_list)
		mark = CutLoadPlan.objects.filter(orderno=oder).values_list('markerno', flat=True)
		mark_list = list(mark) 
		print(mark_list)
		return JsonResponse({"dat_list": dat_list, "mark_list": mark_list})

	elif request.POST.get('markernoo') and request.POST.get('isdate'):
		marker = request.POST.get('markernoo')
		global mkn
		mkn = marker
		print(marker)
		maker = CutLoadPlan.objects.filter(orderno=odn, markerno=marker).values_list('noofplies', flat=True)
		maker_list = list(maker)
		print(maker_list)

		issdate = request.POST.get('isdate')
		print(issdate)
		d = datetime.strptime(issdate, "%Y-%m-%d")
		global dt
		dt = d

		

	# GET MARKER NOS IN DESCENDING ORDER
		orderdesc = CutLoadPlan.objects.all().filter(orderno=odn).order_by('-noofplies').values_list('markerno', flat=True);
		print(len(orderdesc))

	# GET TABLE TYPE

		tbty = CutLoadPlan.objects.filter(orderno=odn, markerno=mkn).values_list("tabletype", flat=True)
		tablety = tbty[0]
		global tabty
		tabty = tablety
		print(tablety)

	# GET AVAILABLE CAPACITY FOR EACH TABLE

		aa = AvailCapacity.objects.filter(tabletype=tablety, modeofspread__icontains="Auto", modeofcut__iexact="CNC").values_list('tableno', flat=True).order_by('-availcapaforspreadandcut');
		print("AA = " + str(aa))
		am = AvailCapacity.objects.filter(tabletype=tablety, modeofspread__icontains="Auto", modeofcut__iexact="Manual").values_list('tableno', flat=True).order_by('-availcapaforspreadandcut');
		print("AM = " + str(am))
		ma = AvailCapacity.objects.filter(tabletype=tablety, modeofspread__icontains="Manual", modeofcut__iexact="CNC").values_list('tableno', flat=True).order_by('-availcapaforspreadandcut');
		print("MA = " + str(ma))
		mm = AvailCapacity.objects.filter(tabletype=tablety, modeofspread__icontains="Manual", modeofcut__iexact="Manual").values_list('tableno', flat=True).order_by('-availcapaforspreadandcut');
		print("MM = " + str(mm))

		x = list(aa) + list(am) + list(ma) + list(mm);
		print(x)

	# ISSUE TABLE

		print(len(x))
		print(len(orderdesc))

		j=0
		for i in orderdesc:
			print("i: " + str(i))
			if len(x) >= 1:
				print("Table No." + str(x[j]))
				CutLoadPlan.objects.filter(markerno=str(i)).update(issuetable=str(x[j]))	
			j=j+1;
			if(j>=len(x)):
				break

		ist = CutLoadPlan.objects.filter(orderno=odn, markerno=marker).values_list('issuetable', flat=True)
		print("TABLE ISSUED")
		print(ist[0])
		ist_list = list(ist)
		print(ist_list)

		
		avc = AvailCapacity.objects.filter(tableno=ist[0], tabletype=tablety, datefield__gte=d).values_list('capacityleft', 'availcapaforspreadandcut')

		print(avc)
		if avc.count()==0:
			print("AVAILABLE CAPACITY")
			avc = AvailCapacity.objects.filter(tableno=ist[0], tabletype=tablety).values_list('availcapaforspreadandcut', flat=True)
		else:
			print("CAPACITY LEFT")
			avc = AvailCapacity.objects.filter(tableno=ist[0], tabletype=tablety).values_list('capacityleft', flat=True)

		# avc = AvailCapacity.objects.filter(tableno=ist[0]).values_list('capacityleft', flat=True)
		# print("AVAILABLE CAPACITY")
		# print(avc[0])

		avc_list = list(avc)
		print(avc_list)

		sc = AvailCapacity.objects.filter(tableno=ist[0], tabletype=tablety).values_list('modeofspread', 'modeofcut')
		print("SPREAD CUT")
		print(sc)
		print(sc[0][0] + " " + sc[0][1])

		if(sc[0][0]=="autospreader" and sc[0][1]=="cnc"):
			print("AA");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=marker).values_list('totaa', flat=True)

		elif(sc[0][0]=="autospreader" and sc[0][1]=="manual"):
			print("AM");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=marker).values_list('totam', flat=True)

		elif(sc[0][0]=="manual" and sc[0][1]=="cnc"):
			print("MA");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=marker).values_list('totma', flat=True)

		elif(sc[0][0]=="manual" and sc[0][1]=="manual"):
			print("MM");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=marker).values_list('totmm', flat=True)

		totcapareq_list = list(totcapareq)
		print(totcapareq_list)
		
		
		return JsonResponse({"maker_list": maker_list, "ist_list": ist_list, "avc_list": avc_list, "totcapareq_list": totcapareq_list})

	elif request.POST.get('istab'):

		print("ISSUE TABLE CHANGED!!")

		istab = request.POST.get('istab')
		print(istab)

		avc = AvailCapacity.objects.filter(tableno=istab, tabletype=tabty, datefield__gte=dt).values_list('capacityleft', 'availcapaforspreadandcut')

		print(avc)
		if avc.count()==0:
			print("AVAILABLE CAPACITY")
			avc = AvailCapacity.objects.filter(tableno=istab, tabletype=tabty).values_list('availcapaforspreadandcut', flat=True)
		else:
			print("CAPACITY LEFT")
			avc = AvailCapacity.objects.filter(tableno=istab, tabletype=tabty).values_list('capacityleft', flat=True)

		avc_list = list(avc)
		print(avc_list)

		sc = AvailCapacity.objects.filter(tableno=istab, tabletype=tabty).values_list('modeofspread', 'modeofcut')
		print("SPREAD CUT")
		print(sc[0][0] + " " + sc[0][1])

		if(sc[0][0]=="autospreader" and sc[0][1]=="cnc"):
			print("AA");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=mkn).values_list('totaa', flat=True)

		elif(sc[0][0]=="autospreader" and sc[0][1]=="manual"):
			print("AM");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=mkn).values_list('totam', flat=True)

		elif(sc[0][0]=="manual" and sc[0][1]=="cnc"):
			print("MA");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=mkn).values_list('totma', flat=True)

		elif(sc[0][0]=="manual" and sc[0][1]=="manual"):
			print("MM");
			totcapareq = CutLoadPlan.objects.filter(orderno=odn, markerno=mkn).values_list('totmm', flat=True)

		totcapareq_list = list(totcapareq)
		print(totcapareq_list)

		return JsonResponse({"avc_list": avc_list, "totcapareq_list": totcapareq_list})

	
	form = issuedets(request.POST or None)
	
	if form.is_valid():
		print('enter loop')
		data = form.cleaned_data
		print(data)
		isstable = data["issuetable"]
		idets = IssueDetails.objects.create(orderno=data["orderno"], styleno=data["styleno"], markerno=data["markerno"], noofplies=data["noofplies"], issuetable=data["issuetable"], availcapaforspreadandcut=data["availcapaforspreadandcut"], cutpaneldelivery=data["cutpaneldelivery"], requiredcapacity=data["requiredcapacity"], requiredday=data["requiredday"], requiredtime=data["requiredtime"], leadtime=data["leadtime"], issuedate=data["issuedate"])
		idets.save();
		print("ok")
		isstable = data["issuetable"]
		print(isstable)
		z = (data["availcapaforspreadandcut"]) - (data["requiredcapacity"])
		print(z)

		tbty = CutLoadPlan.objects.filter(orderno=data["orderno"], markerno=data["markerno"]).values_list("tabletype", flat=True)
		tablety = tbty[0]
		print(tablety)

		AvailCapacity.objects.filter(tableno=isstable, tabletype=tablety).update(capacityleft=z)
		AvailCapacity.objects.filter(tableno=isstable, tabletype=tablety).update(datefield=data["issuedate"])
		print("TABLE UPDATED")

		cld = TableCapacityLeft.objects.create(orderno=data["orderno"], tableno=data["issuetable"], tabletype=tablety, availcapaforspreadandcut=data["availcapaforspreadandcut"], capacityleft=z, datefield=data["issuedate"]);
		cld.save();
		print("CAPACITY LEFT TABLE UPDATED")

		messages.success(request, 'Form submission successful')


	return render(request, 'issuedetails.html', context)
