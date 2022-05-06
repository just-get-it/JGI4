







from django.shortcuts import render,redirect
from .models import labels,fits,seasons,trimcard_sections, manual_documents
from .forms import trim_form, manual_docs_form
from userdetail.models import detail

from b2b.models import notifications,company_Order
# Create your views here.
from product.models import product,category,sub_category,super_category,labels_Object


from filter.models import filter_Categories,filter_Objects
from product.models import size_color_quantity
from userdetail.models import seller_Categories

from django.http import JsonResponse


def seller_label(request):
	if request.user.is_authenticated:
		oj=detail.objects.get(email=request.user.email)
		if oj.vendor:
			obj=labels.objects.filter(vendor=oj)
			data={
			'label':obj,
			'head':'Labels'
			}
			return render(request,'seller_info/seller_label.html',data)
		return redirect('/userdetail/logout')
	return redirect('/userdetail/login')




def seller_label_delete(request,slug):
	if request.user.is_authenticated:
		oj=detail.objects.get(email=request.user.email)
		if oj.vendor:
			obj=labels.objects.get(slug=slug,vendor=oj)
			if request.GET:
				obj.delete()
			if request.GET.get('next'):
				return redirect(request.GET.get('next'))
			return redirect('/userdetail/seller_profile')
		return redirect('/userdetail/logout')
	return redirect('/userdetail/login')






def seller_fit(request):
	if request.user.is_authenticated:
		oj=detail.objects.get(email=request.user.email)
		if oj.vendor:
			obj=fits.objects.filter(vendor=oj)
			data={
			'fit':obj,
			'head':'Fits'
			}
			return render(request,'seller_info/seller_label.html',data)
		return redirect('/userdetail/logout')
	return redirect('/userdetail/login')




def seller_fit_delete(request,slug):
	if request.user.is_authenticated:
		oj=detail.objects.get(email=request.user.email)
		if oj.vendor:
			obj=fits.objects.get(slug=slug,vendor=oj)
			if request.GET:
				obj.delete()
			if request.GET.get('next'):
				return redirect(request.GET.get('next'))
			return redirect('/userdetail/seller_profile')
		return redirect('/userdetail/logout')
	return redirect('/userdetail/login')





def seller_season(request):
	if request.user.is_authenticated:
		oj=detail.objects.get(email=request.user.email)
		if oj.vendor:
			obj=seasons.objects.filter(vendor=oj)
			data={
			'season':obj,
			'head':'Seasons'
			}
			return render(request,'seller_info/seller_label.html',data)
		return redirect('/userdetail/logout')
	return redirect('/userdetail/login')




def seller_season_delete(request,slug):
	if request.user.is_authenticated:
		oj=detail.objects.get(email=request.user.email)
		if oj.vendor:
			obj=seasons.objects.get(slug=slug,vendor=oj)
			if request.GET:
				obj.delete()
			if request.GET.get('next'):
				return redirect(request.GET.get('next'))
			return redirect('/userdetail/seller_profile')
		return redirect('/userdetail/logout')
	return redirect('/userdetail/login')






def seller_profile_notifications(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details:
			noti=notifications.objects.filter(user=details).order_by('-created_on')
			no_count=notifications.objects.filter(seen=False,user=details).count()
			if request.GET.get('filter'):
				filter_noti=request.GET.get('filter')
				if filter_noti=='staff':
					pass
				elif filter_noti=='enquiry':
					noti=noti.filter(type_of_order='E')
					no_count=noti.filter(seen=False).count()
				elif filter_noti=='design':
					noti=noti.filter(type_of_order='D')
					no_count=noti.filter(seen=False).count()
				elif filter_noti=='sampling':
					noti=noti.filter(type_of_order='S')
					no_count=noti.filter(seen=False).count()
				elif filter_noti=='order':
					noti=noti.filter(type_of_order='O')
					no_count=noti.filter(seen=False).count()
			oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
			oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
			oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
			oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
			oty4=oty1+oty2+oty3+oty
			data={
			"noti":noti,
			"no_count":no_count,
			"oty":oty,
			"oty1":oty1,
			"oty2":oty2,
			"oty3":oty3,
			"oty4":oty4,
            "page":"notification"
			}
			return render(request,"seller_info/seller_info_notifications.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




def seller_profile_b2b_customer(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.vendor:
			mana=detail.objects.filter(buisness_Customer=True)
			oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
			oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
			oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
			oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
			oty4=oty1+oty2+oty3+oty
			data={
				"b2b_cust":mana,
				"oty":oty,
				"oty1":oty1,
				"oty2":oty2,
				"oty3":oty3,
				"oty4":oty4
			}
			return render(request,'seller_info/seller_info_b2b_customer.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')






def seller_profile_vendors(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.vendor:
			mana=detail.objects.filter(vendor=True)
			oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
			oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
			oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
			oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
			oty4=oty1+oty2+oty3+oty
			mana_by_cate=seller_Categories.objects.all()
			mana=[]
			for i in mana_by_cate:
				jhgty=detail.objects.filter(vendor=True,seller_category=i)
				mana.append(jhgty)
			data={
				"vend":mana,
				"oty":oty,
				"oty1":oty1,
				"oty2":oty2,
				"oty3":oty3,
				"oty4":oty4
			}
			return render(request,'seller_info/seller_info_vendors.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




def seller_profile_orders(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			orders=company_Order.objects.all().order_by('-overall_priority')
			enquiry=company_Order.objects.filter(order_type='E').order_by('-overall_priority')
			design=company_Order.objects.filter(order_type='D').order_by('-overall_priority')
			sampling=company_Order.objects.filter(order_type='S').order_by('-overall_priority')
			orders=company_Order.objects.filter(order_type='O').order_by('-overall_priority')
			data={
			"orders":orders,
			"enquiry":enquiry,
			"design":design,
			"sampling":sampling
			}
			return render(request,"seller_info/seller_profile_orders_list.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')

# CURRWORK
# def seller_profile_order(request):
# 	if request.GET.get('noti'):
# 		noti=int(request.GET.get('noti'))
# 		ogh=notifications.objects.filter(id=noti).first()
# 		if ogh:
# 			ogh.seen=True

# 			ogh.save()
# 	if request.user.is_authenticated:
# 		print('POST DICT: {}'.format(request.POST))
# 		details=detail.objects.filter(email=request.user.email).first()
# 		print(f'STAFF: {details.staff} VENDOR: {details.vendor}')
# 		if details.staff or details.vendor:
# 			print('LOGGING IN')
# 			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
# 			if details.vendor:
# 				orders=company_Order.objects.filter(order_no=order_no)
# 			if orders.count()>0:
# 				print('ORDERS EXISTING')
# 				ohj=quantity_b2b.objects.filter(order=orders.first(),production=False,is_csv=False)
# 				csv_ohj=quantity_b2b.objects.filter(order=orders.first(),production=False,is_csv=True)
# 				cum_ohj=quantity_b2b.objects.filter(order=orders.first(),production=False)
# 				order=orders.first()

# 				order_bool=False
# 				enquiry_bool=False
# 				sample_bool=False
# 				design_bool=False
# 				size_bool=False
# 				head=False
# 				manager=False
# 				staff=True
# 				if order.order_type=='O':
# 					order_bool=True
# 				elif order.order_type=='E':
# 					enquiry_bool=True
# 				elif order.order_type=='S':
# 					sample_bool=True
# 				else:
# 					design_bool=True
# 				if ohj.count()>0:
# 					size_bool=True
# 				ghj=None
# 				cum=None
# 				merch=None
# 				merch_alloted=None
# 				garment=None
# 				garment_alloted=None
# 				if details.position=='H':
# 					head=True
# 					cum=order.staffs_Allocated.filter(position='M',staff=True,staff_category=details.staff_category).first()
# 					ghj=detail.objects.filter(position='M',staff=True,staff_category=details.staff_category)
# 					merch=staff_Categories.objects.filter(name="Merchandising").first()
# 					merch=detail.objects.filter(position='H',staff=True,staff_category=merch)
# 					merch_alloted=staff_Categories.objects.filter(name="Merchandising").first()
# 					merch_alloted=order.staffs_Allocated.filter(position='H',staff=True,staff_category=merch_alloted).first()
# 				elif details.position=='M':
# 					manager=True
# 					cum=order.staffs_Allocated.filter(position='C',staff=True,staff_category=details.staff_category).first()
# 					ghj=detail.objects.filter(position='C',staff=True,staff_category=details.staff_category)
# 				ghi=staff_Categories.objects.filter(name="Merchandising").first()
# 				if details.staff_category==ghi and details.position=='H':
# 					ghi=seller_Categories.objects.filter(name="Garmenting Vendor").first()
# 					garment_alloted=order.staffs_Allocated.filter(vendor=True,seller_category=ghi).first()
# 					garment=detail.objects.filter(seller_category=ghi,vendor=True)

# 				sta1=company_Order.objects.filter(order_no=order.order_no).first()
# 				li=[]

# 				# for o in sta1.staffs_Allocated.all():
# 				# 	xfg=activities.objects.filter(user=o,order=order)
# 				# 	if xfg.count()>0:
# 				# 		li.append(xfg)
# 				li=activities.objects.filter(order=order).order_by('activity_Cate')
# 				# li=macro_Activities.objects.all()
# 				kjh=production_order.objects.filter(order=order,is_csv=False).order_by('production_no')
# 				csv_kjh = production_order.objects.filter(order=order, is_csv=True).order_by('production_no')
# 				packing_kjh = packing_list_1.objects.filter(order=order).order_by('list_no')

# 				prod=[]
# 				csv_prod=[]
# 				packing_prod=[]
# 				sizes_cum_prod=[]
# 				packing_sizes_cum_prod=[]
# 				colors_cum_prod=[]
# 				packing_colors_cum_prod=[]
# 				address_cum_prod=[]
# 				packing_address_cum_prod=[]
# 				for i in kjh:
# 					for j in i.sizes.all():
# 						if not(j.size_label in sizes_cum_prod) and j.size_label:
# 							sizes_cum_prod.append(j.size_label)
# 						if not(j.color in colors_cum_prod):
# 							colors_cum_prod.append(j.color)
# 						if not(j.address in address_cum_prod):
# 							address_cum_prod.append(j.address)
# 				for i in csv_kjh:
# 					for j in i.sizes.all():
# 						if not(j.size_label in sizes_cum_prod) and j.size_label:
# 							sizes_cum_prod.append(j.size_label)
# 						if not(j.color in colors_cum_prod):
# 							colors_cum_prod.append(j.color)
# 						if not(j.address in address_cum_prod):
# 							address_cum_prod.append(j.address)

# 				for i in packing_kjh:
# 					for j in i.sizes.all():
# 						if not(j.size_label in packing_sizes_cum_prod) and j.size_label:
# 							packing_sizes_cum_prod.append(j.size_label)
# 						if not(j.color in colors_cum_prod):
# 							packing_colors_cum_prod.append(j.color)
# 						if not(j.address in address_cum_prod):
# 							packing_address_cum_prod.append(j.address)
# 				sizes_cum_prod.sort()
# 				packing_sizes_cum_prod.sort()
# 				map_prod={}
# 				manual_cum_map_prod={}
# 				csv_cum_map_prod={}
# 				csv_map_prod={}
# 				packing_map_prod={}

# 				for i in kjh:
# 					for j in colors_cum_prod:
# 						for k in address_cum_prod:
# 							for l in sizes_cum_prod:

# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
# 								if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
# 									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
# 								elif gfb:
# 									map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
# 									for m in sizes_cum_prod:
# 										map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
# 									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity

# 				for i in kjh:
# 					for j in colors_cum_prod:
# 						for k in address_cum_prod:
# 							for l in sizes_cum_prod:

# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=False).first()
# 								if ((str(j.id)+"_"+str(k.id)) in manual_cum_map_prod) and gfb:
# 									manual_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
# 								elif gfb:
# 									manual_cum_map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
# 									for m in sizes_cum_prod:
# 										manual_cum_map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
# 									manual_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
# 				tot_horiz=[]
# 				total=0
# 				for key in manual_cum_map_prod:
# 					manual_cum_map_prod[key].append(sum(manual_cum_map_prod[key][1]))
# 					total+=manual_cum_map_prod[key][2]
# 				for i in range(len(sizes_cum_prod)):
# 					sum_each=0
# 					for key in manual_cum_map_prod:
# 						sum_each+=manual_cum_map_prod[key][1][i]
# 					tot_horiz.append(sum_each)
# 				tot_horiz.append(total)


# 				for i in csv_kjh:
# 					for j in colors_cum_prod:
# 						for k in address_cum_prod:
# 							for l in sizes_cum_prod:

# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
# 								if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
# 									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
# 								elif gfb:
# 									map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
# 									for m in sizes_cum_prod:
# 										map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
# 									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity

# 				total_mc=[]
# 				total=0
# 				for key in map_prod:
# 					map_prod[key].append(sum(map_prod[key][1]))
# 					total+=map_prod[key][2]
# 				for i in range(len(sizes_cum_prod)):
# 					sum_each=0
# 					for key in map_prod:
# 						sum_each+=map_prod[key][1][i]
# 					total_mc.append(sum_each)
# 				total_mc.append(total)

# 				for i in csv_kjh:
# 					for j in colors_cum_prod:
# 						for k in address_cum_prod:
# 							for l in sizes_cum_prod:

# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=True).first()
# 								if ((str(j.id)+"_"+str(k.id)) in csv_cum_map_prod) and gfb:
# 									csv_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
# 								elif gfb:
# 									csv_cum_map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
# 									for m in sizes_cum_prod:
# 										csv_cum_map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
# 									csv_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
				
# 				tot_horizo=[]
# 				total=0
# 				for key in csv_cum_map_prod:
# 					csv_cum_map_prod[key].append(sum(csv_cum_map_prod[key][1]))
# 					total+=csv_cum_map_prod[key][2]
# 				for i in range(len(sizes_cum_prod)):
# 					sum_each=0
# 					for key in csv_cum_map_prod:
# 						sum_each+=csv_cum_map_prod[key][1][i]
# 					tot_horizo.append(sum_each)
# 				tot_horizo.append(total)
				
# 				for i in packing_kjh:
# 					for j in packing_colors_cum_prod:
# 						for k in packing_address_cum_prod:
# 							for l in packing_sizes_cum_prod:

# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
# 								if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
# 									map_prod[(str(j.id)+"_"+str(k.id))][1][packing_sizes_cum_prod.index(l)]+=gfb.quantity
# 								elif gfb:
# 									map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
# 									for m in sizes_cum_prod:
# 										map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
# 									map_prod[(str(j.id)+"_"+str(k.id))][1][packing_sizes_cum_prod.index(l)]+=gfb.quantity


# 				# print(map_prod,sizes_cum_prod)
# 				for i in kjh:
# 					prod.append([i])
# 					sikl=[]
# 					for j in i.sizes.all():
# 						if not(j.size_label in sikl):
# 							sikl.append(j.size_label)
# 					sikl.sort()
# 					# print("\n\n\n\n",sikl)
# 					prod[-1].append(sikl)
# 					coli=[]
# 					addi=[]
# 					for j in i.sizes.all():
# 						if not(j.color in coli):
# 							coli.append(j.color)
# 						if not(j.address in addi):
# 							addi.append(j.address)
# 					tot_sikl=[0 for klj in range(len(sikl))]
# 					kjh568=[]
# 					# print(sikl)
# 					for j in coli:
# 						for k in addi:
# 							treh=[]
# 							check=False
# 							for l in sikl:
# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=False)
# 								if gfb.first():
# 									check=True
# 									treh.append(gfb.first().quantity)
# 									tot_sikl[sikl.index(l)]+=gfb.first().quantity
# 								else:
# 									treh.append(0)
# 							if check:
# 								kjh568.append([j,k,treh,sum(treh)])
# 					prod[-1].append(kjh568)
# 					prod[-1].append(tot_sikl)
# 					prod[-1].append(sum(tot_sikl))


# 				for i in csv_kjh:
# 					csv_prod.append([i])
# 					sikl=[]
# 					for j in i.sizes.all():
# 						if not(j.size_label in sikl):
# 							sikl.append(j.size_label)
# 					sikl.sort()
# 					# print("\n\n\n\n",sikl)
# 					csv_prod[-1].append(sikl)
# 					coli=[]
# 					addi=[]
# 					for j in i.sizes.all():
# 						if not(j.color in coli):
# 							coli.append(j.color)
# 						if not(j.address in addi):
# 							addi.append(j.address)
# 					tot_sikl=[0 for klj in range(len(sikl))]
# 					kjh568=[]
# 					# print(sikl)
# 					for j in coli:
# 						for k in addi:
# 							treh=[]
# 							check=False
# 							for l in sikl:
# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=True)
# 								if gfb.first():
# 									check=True
# 									treh.append(gfb.first().quantity)
# 									tot_sikl[sikl.index(l)]+=gfb.first().quantity
# 								else:
# 									treh.append(0)
# 							if check:
# 								kjh568.append([j,k,treh,sum(treh)])
# 					csv_prod[-1].append(kjh568)
# 					csv_prod[-1].append(tot_sikl)
# 					csv_prod[-1].append(sum(tot_sikl))

# 				for i in packing_kjh:
# 					packing_prod.append([i])
# 					sikl=[]
# 					for j in i.sizes.all():
# 						if not(j.size_label in sikl):
# 							sikl.append(j.size_label)
# 					sikl.sort()
# 					# print("\n\n\n\n",sikl)
# 					packing_prod[-1].append(sikl)
# 					coli=[]
# 					addi=[]
# 					for j in i.sizes.all():
# 						if not(j.color in coli):
# 							coli.append(j.color)
# 						if not(j.address in addi):
# 							addi.append(j.address)
# 					tot_sikl=[0 for klj in range(len(sikl))]
# 					kjh568=[]
# 					# print(sikl)
# 					for j in coli:
# 						for k in addi:
# 							treh=[]
# 							check=False
# 							for l in sikl:
# 								gfb=i.sizes.all().filter(color=j,address=k,size_label=l)
# 								if gfb.first():
# 									check=True
# 									treh.append(gfb.first().quantity)
# 									tot_sikl[sikl.index(l)]+=gfb.first().quantity
# 								else:
# 									treh.append(0)
# 							if check:
# 								kjh568.append([j,k,treh])
# 					packing_prod[-1].append(kjh568)
# 					packing_prod[-1].append(tot_sikl)
# 					#print(prod)



# 				color_av=order.colors_avail.all()
# 				li5=[]
# 				csv_li5=[]
# 				cum_li5=[]
# 				li1=[]
# 				csv_li1=[]
# 				cum_li1=[]
# 				li55=[]
# 				color_av=quantity_b2b.objects.filter(order=order)
# 				some_map_loc=[]
# 				for hgy in color_av:
# 					li21=[hgy.color,hgy.address]
# 					if li21 not in some_map_loc:
# 						some_map_loc.append(li21)
# 				# print(some_map_loc)
# 				for i in ohj:
# 					if i.size_label not in li1:
# 						li1.append(i.size_label)
# 				li1.sort()
# 				for i in csv_ohj:
# 					if i.size_label not in csv_li1:
# 						csv_li1.append(i.size_label)
# 				csv_li1.sort()
# 				for i in cum_ohj:
# 					if i.size_label not in cum_li1:
# 						cum_li1.append(i.size_label)
# 				cum_li1.sort()
# 				for c in some_map_loc:
# 					# oyu=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1])
# 					# for k in oyu:
# 					li2={"color":None,"size":None,"total":None}
# 					csv_li2={"color":None,"size":None,"total":None}
# 					cum_li2={"color":None,"size":None,"total":None}
# 					li3=[]
# 					csv_li3=[]
# 					cum_li3=[]
# 					some_obj=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1],production=False,is_csv=False)
# 					csv_some_obj = quantity_b2b.objects.filter(order=order, color=c[0], address=c[1], production=False,
# 														   is_csv=True)
# 					cum_some_obj=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1],production=False)
# 					li2["color"]=some_obj.first()
# 					csv_li2["color"]=csv_some_obj.first()
# 					cum_li2["color"]=cum_some_obj.first()
# 					total=0
# 					for j in li1:
# 						quan_inst=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1],production=False,size_label=j,is_csv=False).first()
# 						if quan_inst:
# 							li3.append({"quantity":quan_inst.quantity,"size":j})
# 						else:
# 							li3.append({"quantity":0,"size":j})
# 						total=total+li3[-1]["quantity"]
# 					li2["size"]=li3
# 					li2["total"]=total
# 					# print(li2)
# 					li5.append(li2)
# 					total = 0
# 					for j in csv_li1:
# 						quan_inst = quantity_b2b.objects.filter(order=order, color=c[0], address=c[1], production=False,
# 																size_label=j,is_csv=True).first()
# 						if quan_inst:
# 							csv_li3.append({"quantity": quan_inst.quantity, "size": j})
# 						else:
# 							csv_li3.append({"quantity": 0, "size": j})
# 						total = total + csv_li3[-1]["quantity"]
# 					csv_li2["size"] = csv_li3
# 					csv_li2["total"] = total
# 					# print(li2)
# 					csv_li5.append(csv_li2)

# 					total = 0
# 					for j in cum_li1:
# 						quan_inst = quantity_b2b.objects.filter(order=order, color=c[0], address=c[1], production=False,
# 																size_label=j).first()
# 						if quan_inst:
# 							cum_li3.append({"quantity": quan_inst.quantity, "size": j})
# 						else:
# 							cum_li3.append({"quantity": 0, "size": j})
# 						total = total + cum_li3[-1]["quantity"]
# 					cum_li2["size"] = cum_li3
# 					cum_li2["total"] = total
# 					# print(li2)
# 					cum_li5.append(cum_li2)
# 				# for c in color_av:
# 				# 	oyu=quantity_b2b.objects.filter(order=order,color=c)
# 				# 	for k in oyu:
# 				# 		li2={"color":None,"size":None,"total":None}
# 				# 		li3=[]
# 				# 		some_obj=quantity_b2b.objects.filter(order=order,color=k.color,address=k.address)
# 				# 		li2["color"]=k
# 				# 		total=0
# 				# 		for j in some_obj:
# 				# 			li3.append(j)
# 				# 			total=total+j.quantity
# 				# 		li2["size"]=li3
# 				# 		li2["total"]=total
# 				# 		print(li2)
# 				# 		li.append(li2)
# 				li4=[]
# 				csv_li4=[]
# 				cum_li4=[]
# 				total_overall=0
# 				for j in li1:
# 					objs=quantity_b2b.objects.filter(order=order,size_label=j,production=False,is_csv=False)
# 					total=0
# 					for k in objs:
# 						total=total+k.quantity
# 					total_overall=total_overall+total
# 					li4.append(total)
# 				li4.append(total_overall)
# 				total_overall = 0
# 				for j in csv_li1:
# 					objs=quantity_b2b.objects.filter(order=order,size_label=j,production=False,is_csv=True)
# 					total=0
# 					for k in objs:
# 						total=total+k.quantity
# 					total_overall=total_overall+total
# 					csv_li4.append(total)
# 				csv_li4.append(total_overall)
# 				total_overall = 0
# 				for j in cum_li1:
# 					objs=quantity_b2b.objects.filter(order=order,size_label=j)
# 					total=0
# 					for k in objs:
# 						total=total+k.quantity
# 					total_overall=total_overall+total
# 					cum_li4.append(total)
# 				cum_li4.append(total_overall)
# 				if request.GET.get('filter'):
# 					filter_by=request.GET.get('filter')
# 					if filter_by=="com":
# 						li=activities.objects.filter(order=order).exclude(actual_date=None)
# 					if filter_by=="tod":
# 						today=datetime.datetime.today()
# 						li=activities.objects.filter(
# 							order=order,
# 							planned_date__year=today.year,
# 							planned_date__month=today.month,
# 							planned_date__day=today.day)
# 					if filter_by=="sal":
# 						sal58=staff_Categories.objects.filter(name="Sales").first()
# 						act=activities_Category.objects.filter(staff_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="merch":
# 						sal58=staff_Categories.objects.filter(name="Merchandising").first()
# 						act=activities_Category.objects.filter(staff_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="gar":
# 						sal58=seller_Categories.objects.filter(name="Garmenting Vendor").first()
# 						act=activities_Category.objects.filter(seller_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="fab":
# 						sal58=seller_Categories.objects.filter(name="Fabric Vendor").first()
# 						act=activities_Category.objects.filter(seller_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="sew":
# 						sal58=seller_Categories.objects.filter(name="Sewing Trims Vendor").first()
# 						act=activities_Category.objects.filter(seller_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="fin":
# 						sal58=seller_Categories.objects.filter(name="Finishing Trims Vendor").first()
# 						act=activities_Category.objects.filter(seller_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="pack":
# 						sal58=seller_Categories.objects.filter(name="Packing Trims Vendor").first()
# 						act=activities_Category.objects.filter(seller_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="log":
# 						sal58=seller_Categories.objects.filter(name="Logistic Vendor").first()
# 						act=activities_Category.objects.filter(seller_category=sal58)
# 						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
# 					if filter_by=="all":
# 						pass
# 				alteration=assortment.objects.filter(~Q(alteration_cost=0),order_no=order)
# 				size_attri=POM.objects.filter(product_Category=order.product_Category,
# 					product_Supercategory=order.product_Supercategory,
# 					product_Subcategory=order.product_Subcategory)
# 				# print(alteration)
# 				forms=custom_Form.objects.filter(staff_category=details.staff_category)
# 				is_merch=False
# 				merch_obj=staff_Categories.objects.filter(name="Merchandising").first()
# 				# print(merch_obj)
# 				if details.staff_category==merch_obj:
# 					is_merch=True
# 					print(is_merch)
# 				is_sales=False
# 				sales_obj=staff_Categories.objects.filter(name="Sales").first()
# 				if details.staff_category==sales_obj:
# 					is_sales=True
# 				obj_priority=priority_of_order.objects.filter(user=details,order=order).first()
# 				if not(obj_priority):
# 					obj_priority_no=0
# 				else:
# 					obj_priority_no=obj_priority.priority_no
# 				cnt_per=None
# 				if details.staff_category==staff_Categories.objects.get(name="Sales"):
# 					cnt_per=detail.objects.filter(email=order.user_email).first()
# 				elif details.staff_category==staff_Categories.objects.get(name="Merchandising"):
# 					oij=staff_Categories.objects.filter(name="Sales").first()
# 					cnt_per=order.staffs_Allocated.filter(staff=True,position='H',staff_category=oij).first()
# 				boms_obj=bom.objects.filter(order=order).first()
# 				customer=detail.objects.filter(email=order.user_email).first()
# 				measu=None
# 				if order.fashion_Brand and order.label and order.fit and order.season:
# 					measu=measurement.objects.filter(
# 							user=order.fashion_Brand,
# 							label=order.label,
# 							fit=order.fit,
# 							season=order.season,
# 							product_Category=order.product_Category,
# 							product_Subcategory=order.product_Subcategory,
# 							product_Supercategory=order.product_Supercategory
# 						).first()
# 					if measu:
# 						measu = measu.slug
# 				is_quality=False
# 				objuyu=staff_Categories.objects.filter(name="Quality").first()
# 				if details.staff_category==objuyu:
# 					is_quality=True
# 				# macro_acti=macro_Activities.objects.all()
# 				asd=activities.objects.filter(order=order).order_by('activity_Cate')
# 				macro_acti=[]
# 				random_acti=[]
# 				for i in asd:
# 					objs458=macro_Activities.objects.filter(activities=i.activity_Cate)
# 					for j in objs458:
# 						first=i.planned_date
# 						if i.custom_date:
# 							first=i.custom_date
# 						diff=0
# 						if i.actual_date:
# 							diff=i.actual_date-first
# 							diff=diff.days
# 						if j not in random_acti:
# 							random_acti.append(j)
# 							macro_acti.append([j,[[i,diff]]])
# 						else:
# 							indi=random_acti.index(j)
# 							macro_acti[indi][1].append([i,diff])
# 				# print(macro_acti)
# 				macro_acti=sorted(macro_acti,key=lambda x:x[0].id)
# 				fab_obj=seller_Categories.objects.filter(name='Fabric Vendor').first()
# 				fab_obj=detail.objects.filter(vendor=True,seller_category=fab_obj)
# 				log_obj=seller_Categories.objects.filter(name='Logistic Vendor').first()
# 				log_obj=detail.objects.filter(vendor=True,seller_category=log_obj)
# 				pack_obj=seller_Categories.objects.filter(name='Packing Trims Vendor').first()
# 				pack_obj=detail.objects.filter(vendor=True,seller_category=pack_obj)
# 				fin_obj=seller_Categories.objects.filter(name='Finishing Trims Vendor').first()
# 				fin_obj=detail.objects.filter(vendor=True,seller_category=fin_obj)
# 				sew_obj=seller_Categories.objects.filter(name='Sewing Trims Vendor').first()
# 				sew_obj=detail.objects.filter(vendor=True,seller_category=sew_obj)
# 				logi_vendor=seller_Categories.objects.filter(name="Logistic Vendor").first()
# 				logi_vendors=detail.objects.filter(vendor=True,seller_category=logi_vendor)
# 				last_date=activities.objects.filter(order=order).order_by('-planned_date').first()
# 				# print(details.staff_category)
# 				order_section=orders_permission.objects.filter(staff_category=details.staff_category).first()
# 				if order_section:
# 					order_section=order_section.allowed_section.all().filter(order_section=True)
# 				else:
# 					order_section=['Order_Description']
# 				garvendor=order.get_garment_vendor
# 				final_kpi_data=[]
# 				for i in kpi.objects.all():
# 					obj_kpi=kpi_data_order.objects.filter(by_user=details,to_user=garvendor,order=order,
# 						kpi_val=i).first()
# 					if obj_kpi:
# 						obj_kpi=obj_kpi.rating
# 					else:
# 						obj_kpi=0
# 					final_kpi_data.append([i,obj_kpi])
# 				# print(final_kpi_data)

# 				if request.GET.get('custom_assortment'):
# 					order.custom_assortment=not(order.custom_assortment)
# 					order.save()
# 				filefrm = FileForm()
# 				csv_product= items.objects.all()
# 				sizes_opt=quantity_b2b.objects.filter(order=order)
# 				sz_ass_obj=size_assortment_1.objects.all()

# 				objjj=[]
# 				for entry in sz_ass_obj:
# 					overall_total_quantity = 0
# 					addresses=[]
# 					colors=[]
# 					size_wise_sum=[]

# 					sizes=[]
# 					for e in entry.sizes.all():
# 						if(e.address not in addresses):
# 							addresses.append(e.address)
# 						if(e.color not in colors):
# 							colors.append(e.color)
# 						if(e.size_label not in sizes):
# 							sizes.append(e.size_label)
# 						sizes.sort()

# 					for size in sizes:
# 						qua=0
# 						e=entry.sizes.all().filter(size_label=size)
# 						for i in e:
# 							qua+=i.quantity
# 						size_wise_sum.append(qua)
# 					all_rows=[]
# 					for color in colors:
# 						for address in addresses:
# 							quan=0
# 							for size in sizes:
# 								z=entry.sizes.all().filter(color=color,address=address,size_label=size)
# 								print(z)
# 								if(z.first()):
# 									quan+=z.first().quantity
# 							if(quan==0):
# 								break
# 							else:
# 								ls=[]
# 								for size in sizes:
# 									z = entry.sizes.all().filter(color=color, address=address, size_label=size)
# 									if(z.first()):
# 										ls.append(z.first().quantity)
# 									else:
# 										ls.append('-')
# 									#print(ls)

# 								overall_total_quantity += quan
# 								all_rows.append([color,address,ls,quan])
# 								print(all_rows)

# 					objjj.append([entry,sizes,all_rows,size_wise_sum,overall_total_quantity])

# 				print(objjj)

# 				size_lst=[]
# 				new_manual_size_lst=[{"name":i,"select":str(i) in order.allowed_sizes } for i in order.get_sizes]
# 				c=[]
# 				for e in new_manual_size_lst:
# 					if e['select']==True:
# 						c.append(e['name'])
# 				for e in sizes_opt:
# 					if e.size_label not in size_lst:
# 						size_lst.append(e.size_label)
# 				size_lst.sort()
# 				print('sg')
# 				szs=[]
# 				a=size_assortment_1.objects.all()
# 				for i in a:
# 					szs.append(i.assortment_no)
# 				szs.sort()
# 				orders=company_Order.objects.all().filter(order_no=order_no).values('plus_Quantity_Percentage','minus_Quantity_Percentage','sample_quantity')
# 				if orders[0]['sample_quantity']==None:
# 					sample=0
# 				else:
# 					sample=orders[0]['sample_quantity']
# 				print ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
# 				print (orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage']+sample)
# 				data={
# 					"add_percentage":(orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage']+sample),
# 					"accepted":orders[0]['plus_Quantity_Percentage'],
# 					"rejected":orders[0]['minus_Quantity_Percentage'],
# 					"stock":sample,
# 					"sizes_cum_prod":sizes_cum_prod,
# 					'products':csv_product,
# 					'sizes_lst':size_lst,
# 					'new_manual_sizes_lst':c,
# 					'manual_assortment_table':objjj,
# 					"tot_horiz":tot_horiz,
# 					"tot_horizo":tot_horizo,
# 					"total_mc":total_mc,
# 					"custom_assorts":custom_assortment_model.objects.filter(order=order),
# 					"map_prod":map_prod,
# 					"final_kpi_data":final_kpi_data,
# 					"fab_obj":fab_obj,
# 					"log_obj":log_obj,
# 					"fin_obj":fin_obj,
# 					"pack_obj":pack_obj,
# 					"sew_obj":sew_obj,
# 					"order_no":order_no,
# 					"order":order,
# 					"quan":ohj,
# 					"last_date":last_date,
# 					"enquiry_bool":enquiry_bool,
# 					"order_bool":order_bool,
# 					"sample_bool":sample_bool,
# 					"design_bool":design_bool,
# 					"size_bool":size_bool,
# 					"head":head,
# 					"manager":manager,
# 					"staff":staff,
# 					"obj":ghj,
# 					"cum":cum,
# 					"merch":merch,
# 					"merch_alloted":merch_alloted,
# 					"garment":garment,
# 					"garment_alloted":garment_alloted,
# 					"acti":li,
# 					"current":datetime.datetime.now().date,
# 					"prd":kjh,
# 					"quan_by_clr":li5,
# 					"csv_quan_by_clr":csv_li5,
# 					"cum_quan_by_clr":cum_li5,
# 					"size_by_quan":li1,
# 					"csv_size_by_quan": csv_li1,
# 					"cum_size_by_quan": cum_li1,
# 					"quan_by_sz":li4,
# 					"csv_quan_by_sz": csv_li4,
# 					"cum_quan_by_sz": cum_li4,
# 					"alteration":alteration,
# 					"size_attri":size_attri,
# 					"forms":forms,
# 					"is_merch":is_merch,
# 					"is_sales":is_sales,
# 					"obj_priority":obj_priority_no,
# 					"cnt":cnt_per,
# 					"boms_obj":boms_obj,
# 					"customer":customer,
# 					"measu":measu,
# 					"manual_size_ass_numbers":szs,
# 					"is_quality":is_quality,
# 					"macro_acti":macro_acti,
# 					"logi_vendors":logi_vendors,
# 					"details":details,
# 					"manual_cum_map_prod":manual_cum_map_prod,
# 					"csv_cum_map_prod":csv_cum_map_prod,
# 					"prod789":prod,
# 					"csv_prod789":csv_prod,
# 					"packing_prod789":packing_prod,
# 					"order_section":order_section,
# 					"fabric_blends":standard_fabric_blend.objects.filter(standard=True),
# 					"sizes_allowed":[{"name":i,"select":str(i) in order.allowed_sizes } for i in order.get_sizes],
# 					"alteration_assort":assortment.objects.filter(alteration_bool=True,order_no=order),
# 					"fileform": filefrm,
# 				}
# 				if request.GET.get('approve'):
# 					cust_obj=custom_assortment_model.objects.filter(id=int(request.GET.get('approve'))).first()
# 					if cust_obj:
# 						if cust_obj.approve:
# 							cust_obj.approve=False
# 							quants=quantity_b2b.objects.filter(order=order,size_label=cust_obj.size,color__name=cust_obj.color).first()
# 							if quants and quants.quantity:
# 								quants.quantity-=1
# 								quants.save()
# 						else:
# 							cust_obj.approve=True
# 							quants=quantity_b2b.objects.filter(order=order,size_label=cust_obj.size,color__name=cust_obj.color).first()
# 							if not(quants):
# 								col=color_model(name=cust_obj.color)
# 								col.save()
# 								quants=quantity_b2b(order=order,size_label=cust_obj.size,color=col,quantity=0)
# 							quants.quantity+=1
# 							quants.save()
# 						cust_obj.save()
# 					# print(cust_obj.approve,"khj")
# 				if request.POST.get('kpi'):
# 					for i in kpi.objects.all():
# 						print(i)
# 						if request.POST.get('kpi_'+str(i.id)):
# 							new_kpi=kpi_data_order.objects.filter(by_user=details,to_user=garvendor,order=order,
# 								kpi_val=i).first()
# 							if new_kpi:
# 								new_kpi.rating=request.POST.get('kpi_'+str(i.id))
# 								new_kpi.save()
# 							else:
# 								new_kpi=kpi_data_order(by_user=details,to_user=garvendor,order=order,
# 									kpi_val=i,rating=request.POST.get('kpi_'+str(i.id)))
# 								new_kpi.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('fabric_blend_select_ajax'):
# 					obj=standard_fabric_blend.objects.filter(id=int(request.POST.get('fabric_blend_select_ajax'))).first()
# 					washcare=washcare_model.objects.filter(blend=obj,product_Category=order.product_Category,
# 						product_Subcategory=order.product_Subcategory,product_Supercategory=order.product_Supercategory).first()
# 					data={}
# 					if washcare:
# 						data={
# 							"washcare":washcare
# 						}
# 						return render_to_response(request,"seller_info/washcare_detail_view.html",data)
# 					return JsonResponse({})
# 				if request.POST.get('fabric_blend_input'):
# 					obj=standard_fabric_blend.objects.filter(id=int(request.POST.get('fabric_blend_input'))).first()
# 					if obj:
# 						order.fabric_blend=obj
# 						washcare=washcare_model.objects.filter(blend=obj,product_Category=order.product_Category,
# 						product_Subcategory=order.product_Subcategory,product_Supercategory=order.product_Supercategory).first()
# 						if washcare:
# 							order.washcare_obj=washcare
# 						order.save()
# 				if request.POST.get('staff_to_logistics'):
# 					staff_to=detail.objects.filter(email=request.POST.get("staff_to_logistics")).first()
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Add Staff to it("+str(order_no)+") !",
# 						description="Add Staff to it",
# 						user=objs1,
# 						link="/userdetail/staff_profile/orders/"+str(order_no),
# 						type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					acti_cate=activities_Category.objects.filter(
# 						position='M',type_of_order=order.order_type,staff_category=details.staff_category)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('perm_assortment'):
# 					assortment_custom=request.POST.get('assortment_custom')
# 					assortment_size_set=request.POST.get('assortment_size_set')
# 					assortment_brand=request.POST.get('assortment_brand')
# 					assortment_per_customer=request.POST.get('assortment_per_customer')
# 					show_pom_in_assortment=request.POST.get('show_pom_in_assortment')
# 					sizes=request.POST.getlist('sizes_allowed')
# 					final=''
# 					for i in sizes:
# 						final+=i+','
# 					order.allowed_sizes=final
# 					order.save()
# 					print(order.allowed_sizes)
# 					# print(assortment_size_set)
# 					if assortment_custom:
# 						order.assortment_custom=True
# 					else:
# 						order.assortment_custom=False
# 					if assortment_size_set:
# 						order.assortment_size_set=True
# 					else:
# 						order.assortment_size_set=False
# 					if assortment_brand:
# 						order.assortment_brand=True
# 					else:
# 						order.assortment_brand=False
# 					if assortment_per_customer:
# 						order.assortment_per_customer=True
# 					else:
# 						order.assortment_per_customer=False
# 					if show_pom_in_assortment:
# 						order.show_pom_in_assortment=True
# 					else:
# 						order.show_pom_in_assortment=False
# 					order.save()
# 				if request.POST.get('color_ajax') and request.POST.get('address_cate_ajax'):
# 					color_ajax=request.POST.get('color_ajax')
# 					address_cate_ajax=request.POST.get('address_cate_ajax')
# 					size_label_ajax=request.POST.get('size_label_ajax')
# 					quantity_matter=request.POST.get('quantity_matter')
# 					color_obj=color_model.objects.filter(name=color_ajax).first()
# 					address_obj=address_model.objects.filter(id=int(address_cate_ajax)).first()
# 					obstruct_obj=quantity_b2b.objects.filter(
# 						color=color_obj,
# 						address=address_obj,
# 						size_label=int(size_label_ajax),
# 						order=order
# 					).first()
# 					obstruct_obj.quantity=int(quantity_matter)
# 					obstruct_obj.save()
# 					return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
# 				if request.POST.get('size_assort'):
# 					size_assort=int(request.POST.get('size_assort'))
# 					address=int(request.POST.get('address'))
# 					address=address_model.objects.filter(id=address).first()
# 					color=int(request.POST.get('color'))
# 					color=color_model.objects.filter(id=color).first()
# 					quantity=int(request.POST.get('quantity'))
# 					objs_size_assort=quantity_b2b.objects.filter(order=order,
# 						size_label=size_assort,
# 						color=color,
# 						address=address,
# 						production=False,
# 						is_csv=False)

# 					s=request.POST.get("where")
# 					if(s=="Old"):
# 						no=int(request.POST.get("list_no"))
# 						size_ass_obj=size_assortment_1.objects.filter(order=order,assortment_no=no).first()
# 						print(size_ass_obj)
# 						if(size_ass_obj):
# 							a=size_ass_obj.sizes.filter(size_label=size_assort,color=color,address=address,production=False,is_csv=False)
# 							if a.first():
# 								u=a.first()
# 								u.quantity+=quantity
# 								u.save()
# 								print(u.quantity)
# 							else:
# 								objs_size_assort = quantity_b2b(
# 									order=order,
# 									size_label=size_assort,
# 									address=address,
# 									color=color,
# 									quantity=quantity,
# 									production=False,
# 									is_csv=False
# 								)
# 								objs_size_assort.save()
# 								size_ass_obj.sizes.add(objs_size_assort)
# 								size_ass_obj.save()

# 						else:
# 							return HttpResponse("No such table found ... make a valid choice")
# 					elif(s=="New"):
# 						final=1
# 						size_ass_obj=size_assortment_1.objects.filter(order=order).order_by("-assortment_no")
# 						objs_size_assort = quantity_b2b(
# 							order=order,
# 							size_label=size_assort,
# 							address=address,
# 							color=color,
# 							quantity=quantity,
# 							production=False,
# 							is_csv=False
# 						)
# 						objs_size_assort.save()
# 						if(size_ass_obj.first()):
# 							final=size_ass_obj.first().assortment_no + 1
# 						d=size_assortment_1(order=order,assortment_no=final,is_csv=False)
# 						d.save()
# 						d.sizes.add(objs_size_assort)
# 						d.save()



# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))

# 				if request.POST.get('star_click_ajax'):
# 					star=int(request.POST.get('star_click_ajax'))
# 					if not(obj_priority):
# 						obj_priority=priority_of_order(
# 							user=details,
# 							order=order
# 							)
# 					else:
# 						order.priority_no=order.priority_no-obj_priority.priority_no
# 						order.priority_quantity=order.priority_quantity-1
# 					obj_priority.priority_no=star
# 					obj_priority.save()
# 					order.priority_no=order.priority_no+star
# 					order.priority_quantity=order.priority_quantity+1
# 					order.overall_priority=round(order.priority_no/order.priority_quantity,2)
# 					order.save()
# 					return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
# 				if request.POST.get('head_to_manager'):
# 					staff_to=request.POST.get('head_to_manager')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Add Staff to it("+str(order_no)+") !",
# 						description="Add Staff to it",
# 						user=objs1,
# 						link="/userdetail/staff_profile/orders/"+str(order_no),
# 						type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					acti_cate=activities_Category.objects.filter(
# 						position='M',type_of_order=order.order_type,staff_category=details.staff_category)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('manager_to_staff'):
# 					staff_to=request.POST.get('manager_to_staff')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Add Price to it("+str(order_no)+") !",
# 						description="Add Price to it",
# 						user=objs1,
# 						link="/userdetail/staff_profile/orders/"+str(order_no),type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()

# 					acti_cate=activities_Category.objects.filter(
# 						position='C',type_of_order=order.order_type,staff_category=details.staff_category)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('total_Price'):
# 					total_Price=request.POST.get('total_Price')
# 					if total_Price:
# 						order.total_Price=int(total_Price)
# 					alt_charge=request.POST.get('alt_charge')
# 					if alt_charge:
# 						order.alteration_Charge=int(alt_charge)
# 					custom_charge=request.POST.get('custom_charge')
# 					if custom_charge:
# 						order.custom_Charges=int(custom_charge)
# 					target_lead=request.POST.get('target_lead')
# 					if target_lead:
# 						order.target_lead_time=int(target_lead)
# 					target_price=request.POST.get('target_price')
# 					if target_price:
# 						order.target_price=int(target_price)
# 					tech_pack=request.FILES.get('tech_pack')
# 					if tech_pack:
# 						order.tech_pack=tech_pack
# 					specs=request.FILES.get('specs')
# 					if specs:
# 						order.specs=specs
# 					logo=request.FILES.get('logo')
# 					if logo:
# 						order.custom_logo=logo
# 					logo_placement=request.POST.get('logo_placement')
# 					if logo_placement:
# 						order.logo_placement=logo_placement
# 					quan_plus=request.POST.get('quan_plus')
# 					if quan_plus:
# 						order.plus_Quantity_Percentage=int(quan_plus)
# 					quan_negative=request.POST.get('quan_negative')
# 					if quan_negative:
# 						order.minus_Quantity_Percentage=quan_negative
# 					status_ord=request.POST.get('status')
# 					if status_ord:
# 						order.status=status_ord
# 					mode_ord=request.POST.get('mode')
# 					if mode_ord:
# 						order.mode=mode_ord
# 					route_ord=request.POST.get('route')
# 					if route_ord:
# 						order.route=route_ord
# 					order.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('head_to_merch'):
# 					staff_to=request.POST.get('head_to_merch')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Allocated to you !("+str(order_no)+") !",
# 						description="Allocate Manager to it",
# 						user=objs1,
# 						link="/userdetail/staff_profile/orders/"+str(order_no),type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					merch1=staff_Categories.objects.filter(name="Merchandising").first()
# 					acti_cate=activities_Category.objects.filter(
# 						position='H',type_of_order=order.order_type,staff_category=merch1)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					sales_other=staff_Categories.objects.filter(name="Sales").first()
# 					merch_other=staff_Categories.objects.filter(name="Merchandising").first()
# 					staffs_other=detail.objects.filter(staff=True).exclude(staff_category=sales_other).exclude(staff_category=merch_other)
# 					# staffs_other=
# 					for i in staffs_other:
# 						order.staffs_Allocated.add(i)
# 						order.save()
# 						objs1=i
# 						noti_oj=notifications(
# 							title="New Order Allocated to you !("+str(order_no)+") !",
# 							description="Allocate Manager to it",
# 							user=objs1,
# 							link="/userdetail/staff_profile/orders/"+str(order_no),type_of_order=order.order_type)
# 						noti_oj.save()
# 						noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 						noti_oj.save()
# 						merch1=staff_Categories.objects.filter(name="Merchandising").first()
# 						acti_cate=activities_Category.objects.filter(
# 							position=i.position,type_of_order=order.order_type,staff_category=i.staff_category)

# 						for j in acti_cate:
# 							lead_time=0
# 							if order.target_lead_time>=120:
# 								lead_time=j.lead_Time_for_120_Days
# 							elif order.target_lead_time<120 and order.target_lead_time>=105:
# 								lead_time=j.lead_Time_for_105_Days
# 							elif order.target_lead_time<105 and order.target_lead_time>=90:
# 								lead_time=j.lead_Time_for_90_Days
# 							elif order.target_lead_time<90 and order.target_lead_time>=75:
# 								lead_time=j.lead_Time_for_75_Days
# 							elif order.target_lead_time<75 and order.target_lead_time>=60:
# 								lead_time=j.lead_Time_for_60_Days
# 							elif order.target_lead_time<60 and order.target_lead_time>=45:
# 								lead_time=j.lead_Time_for_45_Days
# 							elif order.target_lead_time<45 and order.target_lead_time>=30:
# 								lead_time=j.lead_Time_for_30_Days
# 							elif order.target_lead_time<30 and order.target_lead_time>=15:
# 								lead_time=j.lead_Time_for_15_Days
# 							elif order.target_lead_time<15 and order.target_lead_time>=7:
# 								lead_time=j.lead_Time_for_7_Days
# 							elif order.target_lead_time<7 and order.target_lead_time>=3:
# 								lead_time=j.lead_Time_for_3_Days
# 							j.completed_in=lead_time
# 							j.save()
# 							acti=activities(
# 								user=objs1,
# 								slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 								activity_Cate=j,
# 								order=order,
# 								planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 								prev_lap=lead_time)
# 							acti.save()
# 							if j.linked_activity:
# 								acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 								order=order).first()
# 								if acti_obj_exi:
# 									previous_date_to=acti_obj_exi.planned_date
# 								else:
# 									previous_date_to=datetime.datetime.now()
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 							acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 							# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 							acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('head_to_garment'):
# 					staff_to=request.POST.get('head_to_garment')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Allocated to you !("+str(order_no)+") !",
# 						description="Allocate Different Vendors to it",
# 						user=objs1,
# 						link="/userdetail/vendor_profile/orders/"+str(order_no),type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					acti_cate=activities_Category.objects.filter(
# 						type_of_order=order.order_type,seller_category=objs1.seller_category)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))

# 				fab_obj=seller_Categories.objects.filter(name='Fabric Vendor').first()
# 				log_obj=seller_Categories.objects.filter(name='Logistic Vendor').first()
# 				pack_obj=seller_Categories.objects.filter(name='Packing Trims Vendor').first()
# 				fin_obj=seller_Categories.objects.filter(name='Finishing Trims Vendor').first()
# 				sew_obj=seller_Categories.objects.filter(name='Sewing Trims Vendor').first()
# 				if request.POST.get('gar_to_fab'):
# 					staff_to=request.POST.get('gar_to_fab')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
# 						description="Complete the Activities",
# 						user=objs1,
# 						link="/userdetail/vendor_profile/orders/"+str(order_no),
# 						type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					print("Addf",fab_obj)
# 					acti_cate=activities_Category.objects.filter(
# 						type_of_order=order.order_type,seller_category=fab_obj)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('gar_to_log'):
# 					staff_to=request.POST.get('gar_to_log')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
# 						description="Complete the Activities",
# 						user=objs1,
# 						link="/userdetail/vendor_profile/orders/"+str(order_no),
# 						type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					acti_cate=activities_Category.objects.filter(
# 						type_of_order=order.order_type,seller_category=log_obj)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('gar_to_fin'):
# 					staff_to=request.POST.get('gar_to_fin')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
# 						description="Complete the Activities",
# 						user=objs1,
# 						link="/userdetail/vendor_profile/orders/"+str(order_no),
# 						type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					acti_cate=activities_Category.objects.filter(
# 						type_of_order=order.order_type,seller_category=fin_obj)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('gar_to_sew'):
# 					staff_to=request.POST.get('gar_to_sew')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
# 						description="Complete the Activities",
# 						user=objs1,
# 						link="/userdetail/vendor_profile/orders/"+str(order_no),
# 						type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					acti_cate=activities_Category.objects.filter(
# 						type_of_order=order.order_type,seller_category=sew_obj)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				if request.POST.get('gar_to_pack'):
# 					staff_to=request.POST.get('gar_to_pack')
# 					staff_to=detail.objects.get(email=staff_to)
# 					order.staffs_Allocated.add(staff_to)
# 					order.save()
# 					objs1=staff_to
# 					noti_oj=notifications(
# 						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
# 						description="Complete the Activities",
# 						user=objs1,
# 						link="/userdetail/vendor_profile/orders/"+str(order_no),
# 						type_of_order=order.order_type)
# 					noti_oj.save()
# 					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
# 					noti_oj.save()
# 					acti_cate=activities_Category.objects.filter(
# 						type_of_order=order.order_type,seller_category=pack_obj)

# 					for j in acti_cate:
# 						lead_time=0
# 						if order.target_lead_time>=120:
# 							lead_time=j.lead_Time_for_120_Days
# 						elif order.target_lead_time<120 and order.target_lead_time>=105:
# 							lead_time=j.lead_Time_for_105_Days
# 						elif order.target_lead_time<105 and order.target_lead_time>=90:
# 							lead_time=j.lead_Time_for_90_Days
# 						elif order.target_lead_time<90 and order.target_lead_time>=75:
# 							lead_time=j.lead_Time_for_75_Days
# 						elif order.target_lead_time<75 and order.target_lead_time>=60:
# 							lead_time=j.lead_Time_for_60_Days
# 						elif order.target_lead_time<60 and order.target_lead_time>=45:
# 							lead_time=j.lead_Time_for_45_Days
# 						elif order.target_lead_time<45 and order.target_lead_time>=30:
# 							lead_time=j.lead_Time_for_30_Days
# 						elif order.target_lead_time<30 and order.target_lead_time>=15:
# 							lead_time=j.lead_Time_for_15_Days
# 						elif order.target_lead_time<15 and order.target_lead_time>=7:
# 							lead_time=j.lead_Time_for_7_Days
# 						elif order.target_lead_time<7 and order.target_lead_time>=3:
# 							lead_time=j.lead_Time_for_3_Days
# 						j.completed_in=lead_time
# 						j.save()
# 						acti=activities(
# 							user=objs1,
# 							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
# 							activity_Cate=j,
# 							order=order,
# 							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
# 							prev_lap=lead_time)
# 						acti.save()
# 						if j.linked_activity:
# 							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
# 							order=order).first()
# 							if acti_obj_exi:
# 								previous_date_to=acti_obj_exi.planned_date
# 							else:
# 								previous_date_to=datetime.datetime.now()
# 						else:
# 							previous_date_to=datetime.datetime.now()
# 						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
# 						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
# 						acti.save()
# 					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
# 				return render(request,"userdetail/staff_profile_orders.html",data)
# 			else:
# 				return redirect('/userdetail/staff_profile')
# 		else:
# 			print('LOGGING OUT')
# 			return redirect('/userdetail/logout')
# 	else:
# 		return redirect('/userdetail/login')
	# if request.user.is_authenticated:
	# 	details=detail.objects.filter(email=request.user.email).first()
	# 	if details.vendor:
			
	# 		return render(request,"seller_info/seller_profile_order.html",data)
	# 	else:
	# 		return redirect('/userdetail/logout')
	# else:
	# 	return redirect('/userdetail/login')




def seller_profile_products(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			prod=product.objects.filter(seller=details)
			tags = labels_Object.objects.all()
			filter_cate=filter_Categories.objects.get(name="Price")
			filter_price=filter_Objects.objects.filter(filter_category=filter_cate)
			filter_cate=filter_Categories.objects.get(name="Color")
			filter_color=filter_Objects.objects.filter(filter_category=filter_cate)
			products_category=category.objects.all()
			brand_cate=seller_Categories.objects.filter(name="Products Vendor").first()
			owned_by=detail.objects.filter(staff=True) | detail.objects.filter(seller_category=brand_cate)
			owned_by=owned_by.order_by('email')
			if request.GET.get('owned_by'):
				usr_owned=detail.objects.filter(email=request.GET.get('owned_by')).first()
				objs=size_color_quantity.objects.filter(owned_by=usr_owned)
				prod=None
				for i in objs:
					prod1=product.objects.filter(id=i.linked_product.id)
					if not(prod) or not(prod1):
						prod=prod1
					else:
						prod=prod | prod1
			if request.GET.get('prod_tag'):
				from_tag = labels_Object.objects.filter(id=int(request.GET.get('prod_tag'))).first()
				prod = prod.filter(product_tags=from_tag)
			if request.GET.get('prod_cate'):
				from_category=category.objects.filter(id=int(request.GET.get('prod_cate'))).first()
				prod=prod.filter(product_Category=from_category)
			if request.GET.get('prod_subcate'):
				from_category=sub_category.objects.filter(id=int(request.GET.get('prod_subcate'))).first()
				prod=prod.filter(product_Subcategory=from_category)
			if request.GET.get('prod_supcate'):
				from_category=super_category.objects.filter(id=int(request.GET.get('prod_supcate'))).first()
				prod=prod.filter(product_Supercategory=from_category)
			if request.GET.get('price_range'):
				objs_price=filter_Objects.objects.filter(id=int(request.GET.get('price_range'))).first()
				kul=[]
				print(objs_price.min_price_value)
				for i in prod:
					siz=size_color_quantity.objects.filter(linked_product=i)
					siz=siz.filter(price__gte=objs_price.min_price_value,price__lte=objs_price.max_price_value)
					for kl in siz:
						if kl.linked_product not in kul:
							kul.append(kl.linked_product)
				prod=kul
			if request.GET.get('colors'):
				colors=request.GET.getlist('colors')
				kul=[]
				for i in colors:
					for j in prod:
						siz=size_color_quantity.objects.filter(linked_product=j)
						siz=siz.filter(color=i)
						# print(i)
						for kl in siz:
							kul.append(kl.linked_product)
				prod=kul
			if request.GET.get('my_product'):
				kul=[]
				for i in prod:
					siz=size_color_quantity.objects.filter(owned_by=details)
					for kl in siz:
						if kl.linked_product not in kul:
							kul.append(kl.linked_product)
				prod=kul
			data={
				"obj":prod,
				"empty":False,
				"price":filter_price,
				"color":filter_color,
				"product_category":products_category,
				"owned_by":owned_by,
				"tags": tags
			}
			return render(request,'products/productlistview_staff.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




from seller_info.models import washcares,barcodes
from product.models import htm,product,safety_stock,category,sub_category,super_category
from POM.models import measurement,POM,measurement_chart,garment_weight
from product.models import standard_fabric_blend,care_symbols,washcare_model

from b2b.models import Layout, Dependent_attr, inDependent_attr


def seller_profile_store(request):
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		if details and details.vendor and details.activate_Seller:
			personal_labels = labels.objects.filter(vendor=details)
			product_category = category.objects.all()
			prod = product.objects.filter(seller=details)
			count = 0
			prod1 = []
			for i in prod:
				if count == 3:
					break
				prod1.append(i)
				count += 1
			safety = safety_stock.objects.filter(vendor=details)
			icons = care_symbols.objects.filter(standard=True)
			dependent = Dependent_attr.objects.all()
			Independent = inDependent_attr.objects.all()
			layouts = Layout.objects.all()
			print("Working fine")
			if (layouts.first()):
				layouts = Layout.objects.all()
			else:
				layouts = None
			tform = trim_form(initial={'seller': details})
			mform = manual_docs_form(initial={'seller':details})
			data = {
				"label": personal_labels,
				"product_category": product_category,
				"prod": prod,
				"prod1": prod1,
				"safety": safety,
				"icons": icons,
				"dependent_ats": dependent,
				"independent_ats": Independent,
				"Layouts": layouts,
				"trim_form": tform,
				"manual_form": mform,
			}

			if request.method=='POST':
				if(request.POST.get('layout') and request.POST.get('allignment') and request.POST.get('code')and request.POST.get('width') and request.POST.get('height')):
					type1 = request.POST.get('layout')
					width = int(request.POST.get('width'))
					height = int(request.POST.get('height'))
					code_type = request.POST.get('code')
					alignment = request.POST.get('allignment')
					#print(request.POST['code_dependent'])
					dep=''
					indep=''
					a=request.POST.getlist('code_independent')

					for i in a:
						indep+=str(i)+"-"
					for i in dependent:
						dep+=str(i.name)+"-"


					s = Layout(type=type1, width=width, height=height, code_type=code_type,indep_atr=indep,dep_atr=dep, alignment=alignment)
					s.save()


			if request.POST.get('fabric_blend'):
				blend = standard_fabric_blend.objects.filter(name=request.POST.get('fabric_blend')).first()
				if not (blend):
					blend = standard_fabric_blend(name=request.POST.get('fabric_blend'), standard=False)
					blend.save()
				product_Category = category.objects.filter(id=int(request.POST.get('htm_category'))).first()
				product_Subcategory = sub_category.objects.filter(id=int(request.POST.get('htm_subcategory'))).first()
				product_Supercategory = super_category.objects.filter(
					id=int(request.POST.get('htm_supercategory'))).first()
				width = request.POST.get('width')
				height = request.POST.get('height')
				margin_top = request.POST.get('margin_top')
				margin_bottom = request.POST.get('margin_bottom')
				heading = request.POST.get('washcare_label_heading')
				# print(heading,"\n\n\n\n")
				if not (heading):
					heading = False
				else:
					heading = True
				top_heads = request.POST.get('top_heads')
				bottom_heads = request.POST.get('bottom_heads')
				icons = request.POST.getlist('washcare_icons')
				obj = washcare_model(
					blend=blend,
					product_Category=product_Category,
					product_Subcategory=product_Subcategory,
					product_Supercategory=product_Supercategory,
					width=width,
					height=height,
					margin_top=margin_top,
					margin_bottom=margin_bottom,
					heading=heading,
					top_heads=top_heads,
					bottom_heads=bottom_heads,
					vendor=details
				)
				obj.save()
				li = list(icons)
				for i in li:
					inst = care_symbols.objects.filter(image=i[7:]).first()
					# print(inst)
					if inst:
						obj.care_icons.add(inst)
				obj.save()
			if request.POST.get('fabric_blend_ajax'):
				objs = standard_fabric_blend.objects.filter(name__icontains=request.POST.get('fabric_blend_ajax'),
															standard=True)
				print("here", objs)
				data = {
					"data": list(objs.values())
				}
				return JsonResponse(data)
			if request.POST.get('garment_weight_measurement_ajax'):
				meas = measurement.objects.filter(id=int(request.POST.get('garment_weight_measurement_ajax'))).first()
				poms = POM.objects.filter(product_Supercategory=meas.product_Supercategory).first()
				chart = measurement_chart.objects.filter(chart=meas, pom=poms)
				objs = []
				for i in chart:
					obj = {
						"size": i.size
					}
					objs.append(obj)
				return JsonResponse({"data": objs})
			if request.POST.get('garment_weight_supcategory_ajax'):
				supcate = super_category.objects.filter(
					id=int(request.POST.get('garment_weight_supcategory_ajax'))).first()
				meas = measurement.objects.filter(product_Supercategory=supcate)
				objs = []
				for i in meas:
					name = "Measurement_" + str(i.label) + "_" + str(i.fit) + "_" + str(i.season)
					i = i.id
					obj = {
						"name": name,
						"id": i
					}
					objs.append(obj)
				# print(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('garment_weight_measurement'):
				meas = measurement.objects.filter(id=int(request.POST.get('garment_weight_measurement'))).first()
				size = int(request.POST.get('garment_weight_size'))
				weight = int(request.POST.get('garment_weight'))
				objs = garment_weight(
					user=details,
					measurement_obj=meas,
					size=size,
					weight=weight
				)
				objs.save()
			if request.POST.get('garment_weight_objs_ajax'):
				gar_obj = garment_weight.objects.filter(user=details)
				objs = []
				count = 1
				for i in gar_obj:
					obj = {
						"index": count,
						"cate": i.measurement_obj.product_Category.name,
						"sup_cate": i.measurement_obj.product_Supercategory.name,
						"size": i.size,
						"weight": i.weight
					}
					objs.append(obj)
				return JsonResponse({"data": objs})
			if request.POST.get('safety_category'):
				sup = super_category.objects.filter(id=int(request.POST.get('safety_supercategory'))).first()
				name = request.POST.get('safety_name')
				limit = int(request.POST.get('safety_limit'))
				safe = safety_stock(
					vendor=details,
					name=name,
					limit=limit,
					product_Supercategory=sup,
					product_Category=sup.product_Category,
					product_Subcategory=sup.product_Subcategory
				)
				safe.save()
			if request.POST.get('fits_ajax'):
				obj = fits.objects.filter(vendor=details)
				objs = []
				for i in obj:
					t = {
						"name": i.name,
						"label": i.label.name,
						"slug": i.slug
					}
					objs.append(t)
				objs = list(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('safety_ajax'):
				obj = safety_stock.objects.filter(vendor=details)
				objs = []
				count = 1
				for i in obj:
					t = {
						"name": i.name,
						"index": count,
						"cate": i.product_Category.name,
						"subcate": i.product_Subcategory.name,
						"supcate": i.product_Supercategory.name,
						"limit": i.limit
					}
					objs.append(t)
				objs = list(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('labels_ajax'):
				obj = labels.objects.filter(vendor=details)
				objs = []
				count = 1
				for i in obj:
					t = {
						"name": i.name,
						"index": count,
						"slug": i.slug
					}
					objs.append(t)
					count += 1
				objs = list(objs)
				print(f'THIS IS DTA: {objs}')
				return JsonResponse({"data": objs})
			if request.POST.get('seasons_ajax'):
				obj = seasons.objects.filter(vendor=details)
				objs = []
				count = 1
				for i in obj:
					t = {
						"name": i.name,
						"index": count,
						"label": i.label.name,
						"fit": i.fit.name,
						"slug": i.slug
					}
					objs.append(t)
					count += 1
				objs = list(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('seasons_ajax'):
				obj = seasons.objects.filter(vendor=details)
				objs = []
				count = 1
				for i in obj:
					t = {
						"name": i.name,
						"index": count,
						"label": i.label.name,
						"fit": i.fit.name,
						"slug": i.slug
					}
					objs.append(t)
					count += 1
				objs = list(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('washcare_ajax'):
				obj = washcare_model.objects.filter(vendor=details)
				objs = []
				count = 1
				for i in obj:
					t = {
						"name": i.blend.name,
						"id": i.id,
						"index": count,
						"category": i.product_Category.name,
						"super_category": i.product_Supercategory.name,
						"blend": i.blend.name
					}
					objs.append(t)
					count += 1
				objs = list(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('barcode_ajax'):
				obj = barcodes.objects.filter(vendor=details)
				objs = []
				count = 1
				for i in obj:
					t = {
						"name": i.name,
						"index": count,
						"label": i.label.name,
						"fit": i.fit.name,
						"season": i.season.name
					}
					objs.append(t)
					count += 1
				objs = list(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('htm_ajax'):
				obj = htm.objects.filter(user=details)
				objs = []
				count = 1
				for i in obj:
					t = {
						"name": i.name,
						"index": count,
						"category": i.product_Category.name,
						"sub_category": i.product_Subcategory.name,
						"super_category": i.product_Supercategory.name,
						"file": i.file.url
					}
					objs.append(t)
					count += 1
				objs = list(objs)
				return JsonResponse({"data": objs})
			if request.POST.get('trims_ajax'):
				objs = ['testdata','testdata','testdata']
				return JsonResponse({"data": objs})
			print('THIS IS POST: ', request.POST)
			all_trims = trimcard_sections.objects.filter(seller=details)
			all_docs = manual_documents.objects.filter(seller=details)
			data['trims'] = all_trims
			data['manual_docs'] = all_docs
			if request.POST.get('trims_form'):
				tform = trim_form(request.POST, initial ={'seller':details})
				fabric_and_quantity_no = True if request.POST.get('fabric_and_quantity_no') == 'on' else False
				embroidary_sample_and_thread_code = True if request.POST.get('embroidary_sample_and_thread_code') == 'on' else False
				thread_brand_and_count = True if request.POST.get('thread_brand_and_count') == 'on' else False
				polybag = True if request.POST.get('polybag') == 'on' else False
				pocketing = True if request.POST.get('pocketing') == 'on' else False
				internlining = True if request.POST.get('internlining') == 'on' else False
				new_section = trimcard_sections(
					seller=details,
					name = tform.data['name'],
					product_Category_id = tform.data['product_Category'],
					product_Subcategory_id = tform.data['product_Subcategory'],
					product_Supercategory_id = tform.data['product_Supercategory'],
					fabric_and_quantity_no = fabric_and_quantity_no,
					embroidary_sample_and_thread_code = embroidary_sample_and_thread_code,
					thread_brand_and_count = thread_brand_and_count,
					polybag = polybag,
					pocketing = pocketing,
					internlining = internlining,
				)
				new_section.save()
				return redirect('seller_profile_store')
			if request.POST.get('manual_doc_form'):
				new_docs = manual_documents()
				new_docs.seller = details
				new_docs.name = request.POST.get('name')
				new_docs.product_Category_id = request.POST.get('product_Category')
				new_docs.product_Subcategory_id = request.POST.get('product_Subcategory')
				new_docs.product_Supercategory_id = request.POST.get('product_Supercategory')
				new_docs.folding_doc = request.FILES.get('folding_doc')
				new_docs.packing_doc = request.FILES.get('packing_doc')
				new_docs.packing_manual = request.FILES.get('packing_manual')
				new_docs.all_in_one = request.FILES.get('all_in_one')
				new_docs.save()
				return redirect('seller_profile_store')
			return render(request, "seller_info/seller_profile_store.html", data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


def show_Layout(request, layout_id=None):
	c = Layout.objects.filter(id=layout_id)
	return render(request, 'seller_info/Show_layout.html', {'Layout': c.first()})


from b2b.models import (budget_years,
budget_month,
budget_sectors,
sector_month_weight,
budget_model,
budget_model_sector)

def handlePostData(request,details):
	if request.POST.get('new_year'):
		new_year=budget_years.objects.filter(year=request.POST.get('new_year')).first()
		if not(new_year):
			new_year=budget_years(year=request.POST.get('new_year'))
			new_year.save()
			obj=budget_model(user=details,year=new_year,yearly_amount=request.POST.get('tearget_a'),
				yearly_amount1=request.POST.get('tearget_b'))
			obj.save()
		else:
			obj=budget_model.objects.filter(user=details,year=new_year).first()
			obj.yearly_amount=request.POST.get('tearget_a')
			obj.yearly_amount1=request.POST.get('tearget_b')
			obj.save()
		for i in budget_sectors.objects.filter(user=details):
			for j in budget_month.objects.all():
				o=sector_month_weight(user=details,sector=i,year=obj.year,month=j,weight=100//12,total_weight=100,
					weight_percent=100//12)
				o.save()
	if request.POST.get('new_sector_name'):
		prev=budget_sectors.objects.filter(user=details).first()
		if prev:
			j=prev.total_weights+int(request.POST.get('sector_weight'))
		else:
			j=int(request.POST.get('sector_weight'))
		# tot=request.POST.get('sector_weight')+budget_sectors.objects.filter(user=details).first()
		obj=budget_sectors(user=details,
			name=request.POST.get('new_sector_name'),
			sector_weight=request.POST.get('sector_weight'),
			total_weights=j,
			weight_percent=(int(request.POST.get('sector_weight'))*100)//j
			)
		obj.save()
		for i in budget_sectors.objects.filter(user=details):
			i.total_weights=j
			i.weight_percent=(i.sector_weight*100)//j
			i.save()
		for i in budget_model.objects.filter(user=details):
			for j in budget_month.objects.all():
				o=sector_month_weight(user=details,sector=obj,year=i.year,month=j,weight=100//12,total_weight=100,
					weight_percent=100//12)
				o.save()

def seller_yearly_budget(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details and details.vendor:
			handlePostData(request,details)
			sectors_monthly=[]
			for k in budget_sectors.objects.filter(user=details):
				for i in budget_model.objects.filter(user=details):
					oj=[[k,i.year],[]]
					for j in budget_month.objects.all().order_by('month'):
						oj[-1].append(sector_month_weight.objects.filter(user=details,sector=k,year=i.year,month=j).first().weight_percent)
					sectors_monthly.append(oj)
			data={
				"yearly_data":budget_model.objects.filter(user=details),
				"brand_sectors":budget_sectors.objects.filter(user=details),
				"sectors_monthly":sectors_monthly,
				"months":budget_month.objects.all().order_by('month')
			}

			return render(request,"seller_info/seller_yearly_budget.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/logout')