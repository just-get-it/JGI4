






from django.shortcuts import render,redirect
from .models import POM,measurement,measurement_chart,size_labels,conversion_chart,conversion_chart_map
from seller_info.models import labels,fits,seasons

from userdetail.models import detail,staff_Categories
from product.models import category,sub_category,super_category,product
# Create your views here.
import json
from django.http import HttpResponse,JsonResponse
import random
from .models import inch_size_label,roman_size_label,uk_size_label
import time



def check_for_POST_data(request,user):
	if request.POST.get('measurement_ajax_label'):
		obj=labels.objects.get(slug=request.POST.get('measurement_ajax_label'))
		obj=fits.objects.filter(label=obj)
		if obj.count()>0:
			bol=True
		else:
			bol=False
		obj=list(obj.values())
		return HttpResponse(json.dumps({'data': obj,'bol':bol}), content_type="application/json")
	if request.POST.get('measurement_ajax_fit'):
		obj=labels.objects.get(slug=request.POST.get('measurement_ajax_fit_label'))
		obj1=fits.objects.get(slug=request.POST.get('measurement_ajax_fit'))
		obj2=seasons.objects.filter(fit=obj1)
		if obj2.count()>0:
			bol=True
		else:
			bol=False
		obj2=list(obj2.values())
		return HttpResponse(json.dumps({'data': obj2,'bol':bol}), content_type="application/json")

	if request.POST.get('measurement_ajax_category'):
		obj=category.objects.get(name=request.POST.get('measurement_ajax_category'))
		obj=sub_category.objects.filter(product_Category=obj)
		if obj.count()>0:
			bol=True
		else:
			bol=False
		obj=list(obj.values())
		return HttpResponse(json.dumps({'data': obj,'bol':bol}), content_type="application/json")
	if request.POST.get('measurement_ajax_subcategory'):
		obj=category.objects.get(name=request.POST.get('measurement_ajax_subcategory_category'))
		obj1=sub_category.objects.get(
			name=request.POST.get('measurement_ajax_subcategory'),
			product_Category=obj
			)
		obj2=super_category.objects.filter(product_Subcategory=obj1)
		print(obj2)
		if obj2.count()>0:
			bol=True
		else:
			bol=False
		obj2=list(obj2.values())
		return HttpResponse(json.dumps({'data': obj2,'bol':bol}), content_type="application/json")
	if request.POST.get('measurement_ajax_supercategory'):
		print("GOT here")
		obj=category.objects.get(name=request.POST.get('measurement_ajax_supercategory_category'))
		obj1=sub_category.objects.get(
			name=request.POST.get('measurement_ajax_supercategory_subcategory'),
			product_Category=obj
			)

		obj2=super_category.objects.get(product_Subcategory=obj1,
			name=request.POST.get('measurement_ajax_supercategory'))
		obj3=POM.objects.filter(product_Category=obj,
			product_Subcategory=obj1,
			product_Supercategory=obj2)
		print("SOme")
		if obj3.count()>0:
			bol=True
		else:
			bol=False
		obj3=list(obj3.values())
		return HttpResponse(json.dumps({'data': obj3,'bol':bol}), content_type="application/json")
	if request.POST.get('measurement_label'):
		label=request.POST.get('measurement_label')
		label=labels.objects.get(slug=label)
		fit=request.POST.get('measurement_fit')
		fit=fits.objects.get(slug=fit)
		season=request.POST.get('measurement_season')
		season=seasons.objects.get(slug=season)
		cate=request.POST.get('measurement_category')
		cate=category.objects.get(name=cate)
		sub=request.POST.get('measurement_subcategory')
		sub=sub_category.objects.get(name=sub,product_Category=cate)
		sup=request.POST.get('measurement_supercategory')
		sup=super_category.objects.get(name=sup,product_Subcategory=sub)
		name=int(request.POST.get('size_label'))
		attribute1=request.POST.get('attribute1')
		grading1=request.POST.get('grading1')
		tolerance1=request.POST.get('tolerance1')
		attribute2=request.POST.get('attribute2')
		grading2=request.POST.get('grading2')
		tolerance2=request.POST.get('tolerance2')
		attribute3=request.POST.get('attribute3')
		grading3=request.POST.get('grading3')
		tolerance3=request.POST.get('tolerance3')
		attribute4=request.POST.get('attribute4')
		grading4=request.POST.get('grading4')
		tolerance4=request.POST.get('tolerance4')
		attribute5=request.POST.get('attribute5')
		grading5=request.POST.get('grading5')
		tolerance5=request.POST.get('tolerance5')
		attribute6=request.POST.get('attribute6')
		grading6=request.POST.get('grading6')
		tolerance6=request.POST.get('tolerance6')
		attribute7=request.POST.get('attribute7')
		grading7=request.POST.get('grading7')
		tolerance7=request.POST.get('tolerance7')
		attribute8=request.POST.get('attribute8')
		grading8=request.POST.get('grading8')
		tolerance8=request.POST.get('tolerance8')
		attribute9=request.POST.get('attribute9')
		grading9=request.POST.get('grading9')
		tolerance9=request.POST.get('tolerance9')
		attribute10=request.POST.get('attribute10')
		grading10=request.POST.get('grading10')
		tolerance10=request.POST.get('tolerance10')
		attribute11=request.POST.get('attribute11')
		grading11=request.POST.get('grading11')
		tolerance11=request.POST.get('tolerance11')
		attribute12=request.POST.get('attribute12')
		grading12=request.POST.get('grading12')
		tolerance12=request.POST.get('tolerance12')
		attribute13=request.POST.get('attribute13')
		grading13=request.POST.get('grading13')
		tolerance13=request.POST.get('tolerance13')
		attribute14=request.POST.get('attribute14')
		grading14=request.POST.get('grading14')
		tolerance14=request.POST.get('tolerance14')
		attribute15=request.POST.get('attribute15')
		grading15=request.POST.get('grading15')
		tolerance15=request.POST.get('tolerance15')
		attribute16=request.POST.get('attribute16')
		grading16=request.POST.get('grading16')
		tolerance16=request.POST.get('tolerance16')
		attribute17=request.POST.get('attribute17')
		grading17=request.POST.get('grading17')
		tolerance17=request.POST.get('tolerance17')
		attribute18=request.POST.get('attribute18')
		grading18=request.POST.get('grading18')
		tolerance18=request.POST.get('tolerance18')
		attribute19=request.POST.get('attribute19')
		grading19=request.POST.get('grading19')
		tolerance19=request.POST.get('tolerance19')
		attribute20=request.POST.get('attribute20')
		grading20=request.POST.get('grading20')
		tolerance20=request.POST.get('tolerance20')
		attribute21=request.POST.get('attribute21')
		grading21=request.POST.get('grading21')
		tolerance21=request.POST.get('tolerance21')
		attribute22=request.POST.get('attribute22')
		grading22=request.POST.get('grading22')
		tolerance22=request.POST.get('tolerance22')
		attribute23=request.POST.get('attribute23')
		grading23=request.POST.get('grading23')
		tolerance23=request.POST.get('tolerance23')
		attribute24=request.POST.get('attribute24')
		grading24=request.POST.get('grading24')
		tolerance24=request.POST.get('tolerance24')
		attribute25=request.POST.get('attribute25')
		grading25=request.POST.get('grading25')
		tolerance25=request.POST.get('tolerance25')
		attribute26=request.POST.get('attribute26')
		grading26=request.POST.get('grading26')
		tolerance26=request.POST.get('tolerance26')
		attribute27=request.POST.get('attribute27')
		grading27=request.POST.get('grading27')
		tolerance27=request.POST.get('tolerance27')
		attribute28=request.POST.get('attribute28')
		grading28=request.POST.get('grading28')
		tolerance28=request.POST.get('tolerance28')
		attribute29=request.POST.get('attribute29')
		grading29=request.POST.get('grading29')
		tolerance29=request.POST.get('tolerance29')
		attribute30=request.POST.get('attribute30')
		grading30=request.POST.get('grading30')
		tolerance30=request.POST.get('tolerance30')
		slug="measurement_"+str(label.name)+"_"+str(fit.name)+"_"+str(season.name)+"_"+str(random.randint(1,999999999999))
		
		oj=measurement(
			user=user,
			label=label,
			fit=fit,
			season=season,
			product_Category=cate,
			product_Subcategory=sub,
			product_Supercategory=sup,
			name=name,
			attribute1=attribute1,
			grading1=grading1,
			tolerance1=tolerance1,
			attribute2=attribute2,
			grading2=grading2,
			tolerance2=tolerance2,
			attribute3=attribute3,
			grading3=grading3,
			tolerance3=tolerance3,
			attribute4=attribute4,
			grading4=grading4,
			tolerance4=tolerance4,
			attribute5=attribute5,
			grading5=grading5,
			tolerance5=tolerance5,
			attribute6=attribute6,
			grading6=grading6,
			tolerance6=tolerance6,
			attribute7=attribute7,
			grading7=grading7,
			tolerance7=tolerance7,
			attribute8=attribute8,
			grading8=grading8,
			tolerance8=tolerance8,
			attribute9=attribute9,
			grading9=grading9,
			tolerance9=tolerance9,
			attribute10=attribute10,
			grading10=grading10,
			tolerance10=tolerance10,
			attribute11=attribute11,
			grading11=grading11,
			tolerance11=tolerance11,
			attribute12=attribute12,
			grading12=grading12,
			tolerance12=tolerance12,
			attribute13=attribute13,
			grading13=grading13,
			tolerance13=tolerance13,
			attribute14=attribute14,
			grading14=grading14,
			tolerance14=tolerance14,
			attribute15=attribute15,
			grading15=grading15,
			tolerance15=tolerance15,
			attribute16=attribute16,
			grading16=grading16,
			tolerance16=tolerance16,
			attribute17=attribute17,
			grading17=grading17,
			tolerance17=tolerance17,
			attribute18=attribute18,
			grading18=grading18,
			tolerance18=tolerance18,
			attribute19=attribute19,
			grading19=grading19,
			tolerance19=tolerance19,
			attribute20=attribute20,
			grading20=grading20,
			tolerance20=tolerance20,
			attribute21=attribute21,
			grading21=grading21,
			tolerance21=tolerance21,
			attribute22=attribute22,
			grading22=grading22,
			tolerance22=tolerance22,
			attribute23=attribute23,
			grading23=grading23,
			tolerance23=tolerance23,
			attribute24=attribute24,
			grading24=grading24,
			tolerance24=tolerance24,
			attribute25=attribute25,
			grading25=grading25,
			tolerance25=tolerance25,
			attribute26=attribute26,
			grading26=grading26,
			tolerance26=tolerance26,
			attribute27=attribute27,
			grading27=grading27,
			tolerance27=tolerance27,
			attribute28=attribute28,
			grading28=grading28,
			tolerance28=tolerance28,
			attribute29=attribute29,
			grading29=grading29,
			tolerance29=tolerance29,
			attribute30=attribute30,
			grading30=grading30,
			tolerance30=tolerance30,
			slug=slug
			)
		oj.save()
		size_avail=list(map(int,request.POST.getlist('size_avail')))
		count=1
		pom=POM.objects.filter(product_Category=oj.product_Category,
			product_Subcategory=oj.product_Subcategory,
			product_Supercategory=oj.product_Supercategory)
		print(pom)
		# time.sleep(10000)
		for i in size_avail:
			diff=i-name
			count=1
			for j in pom:
				if request.POST.get('attribute'+str(count)):
					grade=float(request.POST.get('grading'+str(count)))
					attri=float(request.POST.get('attribute'+str(count)))
					val=attri+(grade*diff)
					tol=float(request.POST.get('tolerance'+str(count)))
					obj=measurement_chart(
						chart=oj,
						pom=j,
						size=i,
						value=val,
						grading=grade,
						tolerance=tol
						)
					if diff==0:
						obj.main_val=True
					obj.save()
				else:
					break
				count+=1
		if not(name in size_avail):
			count=1
			for j in pom:
				if request.POST.get('attribute'+str(count)):
					grade=float(request.POST.get('grading'+str(count)))
					attri=float(request.POST.get('attribute'+str(count)))
					tol=float(request.POST.get('tolerance'+str(count)))
					obj=measurement_chart(
						chart=oj,
						pom=j,
						size=name,
						value=attri,
						grading=grade,
						tolerance=tol
						)
					obj.main_val=True
					obj.save()
				else:
					break
				count+=1
		if request.POST.getlist('size_standard'):
			size_standard=request.POST.getlist('size_standard')
			for i in size_standard:
				if i=='roman':
					oj.roman=True
				elif i=='inch':
					oj.inch=True
				elif i=='uk':
					oj.uk=True
			oj.save()
		return redirect('/userdetail/seller_profile')


def measurements_form(request):
	if request.user.is_authenticated:
		user=detail.objects.get(email=request.user.email)
		print(user)
		if user.vendor and user.activate_Seller:
			obj_label=labels.objects.filter(vendor=user)
			obj_category=category.objects.all()
			pom=POM.objects.all()
			sizes_avail=size_labels.objects.all()
			data={
			"obj_label":obj_label,
			"obj_category":obj_category,
			"pom":pom,
			"sizes":sizes_avail
			}
			if request.POST:
				return check_for_POST_data(request,user)
			return render(request,'POM/measurement_form.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def duplicate_measurements(request,slug):
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.vendor and details.activate_Seller:
			meas=measurement.objects.filter(slug=slug).first()
			meas_deta=measurement_chart.objects.filter(main_val=True,chart=meas)
			meas_data=measurement_chart.objects.filter(chart=meas)
			# print(meas_deta)
			obj_label=labels.objects.filter(vendor=details)
			obj_category=category.objects.all()
			pom=POM.objects.all()
			sizes_avail=size_labels.objects.all()
			data={
				"obj_label":obj_label,
				"obj_category":obj_category,
				"pom":pom,
				"sizes":sizes_avail,
				"meas":meas,
				"meas_data":meas_data,
				"meas_deta":meas_deta,
			}
			if request.POST:
				return check_for_POST_data(request,details)
			return render(request,'POM/duplicate_measurements.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def measurement_delete(request,slug):
	if request.user.is_authenticated:
		obj=detail.objects.get(email=request.user.email)
		if obj.vendor:
			if obj.activate_Seller:
				meas=measurement.objects.filter(slug=slug,user=obj)
				if meas.count()>0:
					meas=meas.first()
					meas.delete()
				return redirect('/userdetail/seller_profile')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def measurements(request):
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.vendor and details.activate_Seller:
			objs=measurement.objects.filter(user=details)
			data={
			"meas":objs
			}
			return render(request,'userdetail/measurements.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




from copy import deepcopy



def measurements_detail(request,slug):
	if request.user.is_authenticated:
		obj=detail.objects.get(email=request.user.email)
		objs=staff_Categories.objects.filter(name="Merchandising").first()
		objs=measurement.objects.filter(slug=slug).first()
		# else:
			# objs=measurement.objects.filter(user=obj,slug=slug).first()
		sl=POM.objects.filter(product_Category=objs.product_Category,
			product_Subcategory=objs.product_Subcategory,
			product_Supercategory=objs.product_Supercategory)
		# objs1=list(objs1.values())
		li=[]
		oj=measurement_chart.objects.filter(chart=objs,pom=sl.first()).order_by('size')
		for i in oj:
			li.append(i.size)
		li10=[li]
		li11=[]
		li12=[]
		li13=[]
		for i in li:
			otr=conversion_chart.objects.filter(user=obj).first()
			if not(otr):
				otr=conversion_chart.objects.filter(main=True).first()
			cm=size_labels.objects.filter(name=i).first()
			ama=otr.mapping.all().filter(cm=cm).first()
			if ama and ama.inch and ama.inch.name:
				li11.append([ama.inch.name,i])
			else:
				li11.append([None,i])
			if ama and ama.roman and ama.roman.name:
				li12.append([ama.roman.name,i])
			else:
				li12.append([None,i])
			if ama and ama.uk and ama.uk.name:
				li13.append([ama.uk,i])
			else:
				li13.append([None,i])
		li10.append(li11)
		li10.append(li12)
		li10.append(li13)
		li1=[]
		for i in sl:
			li1.append([i])
			li2=[]
			for j in oj:
				obj=measurement_chart.objects.filter(chart=objs,pom=i,size=j.size).first()
				li2.append(obj)
			li1[-1].append(li2)
		# print(li1)
		li2=[]
		for i in sl:
			obj=measurement_chart.objects.filter(chart=objs,pom=i,main_val=True).first()
			li2.append(obj)
		details=detail.objects.filter(email=request.user.email).first()
		conv_chart=conversion_chart.objects.filter(user=details).first()
		if not(conv_chart):
			conv_chart=conversion_chart.objects.filter(main=True).first()
			cd=conversion_chart(user=details,main=False)
			cd.save()
			for i in conv_chart.mapping.all():
				new_obj_map=conversion_chart_map(
						cm=i.cm,
						inch=i.inch,
						roman=i.roman,
						uk=i.uk
					)
				new_obj_map.save()
				cd.mapping.add(new_obj_map)
			cd.save()

		cm_size=size_labels.objects.all()
		inch_size=inch_size_label.objects.all()
		roman_size=roman_size_label.objects.all()
		uk_size=uk_size_label.objects.all()
		hides=[]
		if objs.hides:
			hides=list(objs.hides.strip().split(","))
		# print("hides - ",hides)
		data={
		"data":detail.objects.get(email=request.user.email),
		"meas":objs,
		"default":li2,
		"sizes_cm":li10[0],
		"sizes_inch":li10[1],
		"sizes_roman":li10[2],
		"sizes_uk":li10[3],
		"chart":li1,
		"conv_chart":conv_chart,
		"cm_size":cm_size,
		"roman_size":roman_size,
		"inch_size":inch_size,
		"uk_size":uk_size,
		"hides":hides
		}
		if request.POST.get('update_hidden'):
			val=request.POST.get('val_for_ajax')
			objs.hides=val
			objs.save()
			return JsonResponse({"some":True})
		if request.POST.get('from_conv_chart'):
			to_which=conversion_chart_map.objects.filter(id=int(request.POST.get('id_for_ajax'))).first()
			in_which=request.POST.get('for_which_ajax')
			if in_which=="cm":
				up_val=size_labels.objects.filter(name=int(request.POST.get('val_for_ajax'))).first()
				to_which.cm=up_val
			elif in_which=="inch":
				up_val=inch_size_label.objects.filter(name=int(request.POST.get('val_for_ajax'))).first()
				to_which.inch=up_val
			elif in_which=="roman":
				up_val=roman_size_label.objects.filter(name=str(request.POST.get('val_for_ajax'))).first()
				to_which.roman=up_val
			elif in_which=="uk":
				up_val=uk_size_label.objects.filter(name=int(request.POST.get('val_for_ajax'))).first()
				to_which.uk=up_val
			to_which.save()
			return JsonResponse({"some":True})
		if request.POST.get('meas'):
			for i in li2:
				i.value=float(request.POST.get('value_'+str(i.id)))
				i.grading=float(request.POST.get('grading_'+str(i.id)))
				i.tolerance=float(request.POST.get('tolerance_'+str(i.id)))
				i.save()
			# print("Done Saved IT !!")
			name=li2[0].size
			grade=li2[0].grading
			tol=li2[0].tolerance
			for i in oj:
				diff=i.size-name
				for j in sl:
					obj=measurement_chart.objects.filter(chart=objs,pom=j,size=i.size).first()
					obj1=measurement_chart.objects.filter(chart=objs,pom=j,size=name).first()
					obj.grading=obj1.grading
					obj.tolerance=obj1.tolerance
					obj.value=obj1.value+(obj1.grading*diff)
					obj.save()
			return redirect('/userdetail/seller_profile/measurements/'+str(objs.slug))
		if request.POST.get('from_chart'):
			for_which=int(request.POST.get('id_for_ajax'))
			for_which=measurement_chart.objects.filter(id=for_which).first()
			for_which.value=float(request.POST.get('val_for_ajax'))
			for_which.save()
			return JsonResponse({"done":True})
		if request.GET.get('duplicate'):
			new_charts=measurement_chart.objects.filter(chart=objs)
			objs.pk=None
			slug_new=list(objs.slug.strip().split("_"))
			new=int(slug_new[-1])+1
			nw=""
			for i in slug_new:
				nw+=i
			nw+="_"+str(new)
			objs.slug=nw
			objs.save()
			# objs.save()
			for i in new_charts:
				j=deepcopy(i)
				j.pk=None
				j.save()
				j.chart=objs
				j.save()
			return redirect('/userdetail/seller_profile')
		return render(request,'POM/measurements_detail.html',data)

	else:
		return redirect('/userdetail/login')





def measurements_compare(request):
	if request.GET.get('first'):
		details=detail.objects.filter(email=request.user.email).first()
		meas=measurement.objects.filter(slug=request.GET.get('first')).first()
		other_meas=measurement.objects.filter(user=details)
		if meas:
			data={
				"other_meas":other_meas,
				"meas":meas
			}
			if request.GET.get('second'):
				meas1=measurement.objects.filter(slug=request.GET.get('second')).first()
				data["meas1"]=meas1
				size_labels=[]
				charts=measurement_chart.objects.filter(chart=meas)
				charts1=measurement_chart.objects.filter(chart=meas1)
				for i in charts:
					if not(i.size in size_labels):
						size_labels.append(i.size)
				for i in charts1:
					if not(i.size in size_labels):
						size_labels.append(i.size)
				data["sizes"]=size_labels
				labels=POM.objects.filter(product_Supercategory=meas.product_Supercategory)
				labels1=POM.objects.filter(product_Supercategory=meas.product_Supercategory)
				final_labels=[]
				for i in labels:
					if not(i in final_labels):
						final_labels.append(i)
				for i in labels1:
					if not(i in final_labels):
						final_labels.append(i)
				chart=[]
				size_labels.sort()
				for i in final_labels:
					chart.append([i])
					li2=[]
					for j in size_labels:
						obj=measurement_chart.objects.filter(chart=meas,pom=i,size=j).first()
						obj1=measurement_chart.objects.filter(chart=meas1,pom=i,size=j).first()
						
						li2.append([obj,obj1])
					chart[-1].append(li2)
				data["chart"]=chart
			return render(request,"POM/measurements_compare.html",data)
		else:
			return redirect('/userdetail/seller_profile')
	else:
		return redirect('/userdetail/seller_profile')