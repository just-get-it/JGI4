
from django.conf import settings
from b2b.models import Layout


from django.db.models import Q


from django.core import serializers
from django.shortcuts import render,redirect,render
from django.contrib.auth import authenticate,login,logout,get_user_model
# Create your views here.
from .models import detail,seller_Categories,staff_Categories, items, rating_users, distribution_center
import random
import json
from b2b.models import notifications,company_Order,activities,balance_quantity_b2b,quantity_b2b,activities_Category,production_order,packing_list_1,new_pl,plqty
from b2b.models import color_model,address_model,Carton_new,balance_list_2
from b2b.models import size_color_quantity as scl
from .models import brand
from POM.models import measurement

from product.models import product,labels_Object,units, extradetails, Add_images, recently_viewed, TermAndCondition, super_category

from cartnew.models import *
from cartnew.views import *
from seller_info.models import labels,fits,seasons, trimcard_sections, manual_documents
from seller_info.forms import trim_form, manual_docs_form
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import datetime
from .models import *
from django.utils import timezone
from django.utils.dateparse import parse_date
from .models import response_time

from product.models import category,sub_category,super_category,label_Attributes_Values
from Garmenting_Vendor.models import production_Product,production_Line
from product.models import trims_product,trims_Category,trims_Attribute

from b2b.models import bom
from POM.models import POM
from b2b.models import assortment
from b2b.models import messages_head,chats_head

from b2b.models import esclation_home,mom_model
from product.models import trims_product_quantity


from userdetail.forms import *
from .dates_custom import getPlannedDate
from userdetail.utils import send_email,generateOTP6digit,randomStringDigits
from movintrendz.settings import EMAIL_HOST_USER
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from . import forms
from .forms import FileForm
from . import models
from django.core.files.storage import FileSystemStorage
import csv

##########imports of RESUME PARSER#########
import re
import filetype
#from userdetail.convertforms import *
import nltk
#import spacy
#from spacy.matcher import Matcher
from userdetail.skills import *
from userdetail.imageprocess import *

from datetime import datetime, date
##########################################


User=get_user_model()

def login_page(request):
	data={
	"invalid":False
	}
	redirect_to = request.GET.get('next', '')
	data['redirects_url'] = redirect_to	
	if request.POST:
		postData = json.loads(request.body)
		email=postData['email']
		password=postData['password']
		# cart=postData['cart']
		user=authenticate(username=email,password=password)
		# if not Customer.objects.filter(email=email).exists():
		# 	a = Customer(name=email, email=email)
		# 	a.save()
		if user is not None:
		# 	cus_id = Customer.objects.filter(email=email).values('id')[0]['id']
		# 	order, created = Order.objects.get_or_create(customer_id=cus_id, complete=False)
		# 	if cart:
		# 		for productId in cart:
		# 			productitem = product.objects.get(product_code=productId)
		# 			orderItem, created = OrderItem.objects.get_or_create(order=order, product=productitem)
					
		# 			orderItem.quantity = (orderItem.quantity + cart[productId][0])
		# 			orderItem.save()

		# 			if orderItem.quantity <= 0:
		# 				orderItem.delete()

		# 			cartItems = order.get_cart_items
		# 			carts, created = CartItems.objects.get_or_create(email=email)
		# 			if created:
		# 				CartItems.objects.filter(email=email).update(items=cartItems)
		# 			else:
		# 				CartItems.objects.filter(email=email).update(items=cartItems)

			login(request,user)
			user=detail.objects.filter(email=request.user.email)
			if user.count()>0:
				user=user.first()
				if request.GET.get('next'):
					nurl=request.GET.get('next')
					if request.GET.get('carton'):
						nurl=nurl+"?carton="+request.GET.get("carton")
					if request.GET.get("size"):
						nurl=nurl+"&size="+request.GET.get("size")
					data['url'] = '/'+nurl+'/'
					return HttpResponse(json.dumps(data), content_type='application/json')
				if user.buisness_Customer:
					if user.info_update:
						data['url'] = '/buisness/buisness_profile/'
						return HttpResponse(json.dumps(data), content_type='application/json')
					else:
						data['url'] = '/buisness/buisness_timeline/'
						return HttpResponse(json.dumps(data), content_type='application/json')
					data['url'] = '/buisness/'
					return HttpResponse(json.dumps(data), content_type='application/json')
				elif user.vendor:
					if user.info_update:
						obj=seller_Categories.objects.filter(name="Products Vendor").first()
						if user.seller_category==obj:
							data['url'] = '/userdetail/seller_profile/'
							return HttpResponse(json.dumps(data), content_type='application/json')
						else:
							data['url'] = '/userdetail/vendor_profile/'
							return HttpResponse(json.dumps(data), content_type='application/json')
					else:
						data['url'] = '/userdetail/seller_profile_update/'
						return HttpResponse(json.dumps(data), content_type='application/json')
				elif user.b2b_order:
					data['url'] = '/buisness/consumer_profile'
					# data['url'] = '/userdetail/profile/'
					return HttpResponse(json.dumps(data), content_type='application/json')
				elif user.staff:
					if user.info_update:
						data['url'] = '/userdetail/staff_profile/'
						return HttpResponse(json.dumps(data), content_type='application/json')
					else:
						data['url'] = '/userdetail/staff_profile_update/'
						return HttpResponse(json.dumps(data), content_type='application/json')
				elif user.student:
						data['url'] = '/channels/planner/'
						return HttpResponse(json.dumps(data), content_type='application/json')
			if postData.get('redirect_url'):
				data['url'] = postData['redirect_url']
			else:
				data['url'] = '/'
			return HttpResponse(json.dumps(data), content_type='application/json')
		else:
			data['invalid'] = True
			data['url'] = '/userdetail/login'
			return HttpResponse(json.dumps(data), content_type='application/json')
	return render(request,"userdetail/login.html",data)




def register_page(request):
	data={
	"exist":False
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		if user.count()>0:
			data={
			"exist":True
			}
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=True,
				vendor=False,
				buisness_Customer=False,
				staff=False
			)
			user1.save()
			return redirect('/userdetail/login')

	return render(request,"userdetail/register.html",data)






def consumer_register(request):
	data={
	"exist":False
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		if user.count()>0:
			data={
			"exist":True
			}
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=False,
				buisness_Customer=False,
				staff=False,
				b2b_order=True
			)
			user1.save()
			return redirect('/userdetail/login')

	return render(request,"userdetail/register.html",data)

def new_seller_register(request):
	query=seller_Categories.objects.all()
	features = seller_additional_features.objects.all()
	data={
	"exist":False,
	"query":query,
	"features":list(features),
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		seller_cate=request.POST.get('seller_cate')
		seller_cate=seller_Categories.objects.get(name=seller_cate)
		
		if user.count()>0:
			data["exist"]=True
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=True,
				buisness_Customer=False,
				staff=False,
				seller_category=seller_cate,
			)
			user1.save()
			
			obj=staff_Categories.objects.filter(name="Merchandising").first()
			objs=detail.objects.filter(staff=True,position='H',staff_category=obj)
			for i in objs:
				noti_j=notifications(
					title="New Vendor Please Verify and Activate it !",
					description="New Vendor is Here please Activate his Account Soon !",
					link="/userdetail/seller_profile/"+str(email),
					user=i
					)
				noti_j.save()
				noti_j.link=noti_j.link+"?noti="+str(noti_j.id)
				noti_j.save()
			return redirect('/userdetail/login')
	return render(request,"userdetail/new_seller_register.html",data)

def seller_register(request):
	query=seller_Categories.objects.all()
	data={
	"exist":False,
	"query":query
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		seller_cate=request.POST.get('seller_cate')
		seller_cate=seller_Categories.objects.get(name=seller_cate)
		if user.count()>0:
			data["exist"]=True
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=True,
				buisness_Customer=False,
				staff=False,
				seller_category=seller_cate
			)
			user1.save()
			obj=staff_Categories.objects.filter(name="Merchandising").first()
			objs=detail.objects.filter(staff=True,position='H',staff_category=obj)
			for i in objs:
				noti_j=notifications(
					title="New Vendor Please Verify and Activate it !",
					description="New Vendor is Here please Activate his Account Soon !",
					link="/userdetail/seller_profile/"+str(email),
					user=i
					)
				noti_j.save()
				noti_j.link=noti_j.link+"?noti="+str(noti_j.id)
				noti_j.save()




			return redirect('/userdetail/login')
	return render(request,"userdetail/seller_register.html",data)

def manufacturer_register(request):
	query=seller_Categories.objects.filter(vendor=True)
	data={
	"exist":False,
	"query":query
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		seller_cate=request.POST.get('seller_cate')
		seller_cate=seller_Categories.objects.get(name=seller_cate)
		if user.count()>0:
			data["exist"]=True
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=True,
				buisness_Customer=False,
				staff=False,
				seller_category=seller_cate
			)
			user1.save()
			obj=staff_Categories.objects.filter(name="Merchandising").first()
			objs=detail.objects.filter(staff=True,position='H',staff_category=obj)
			for i in objs:
				noti_j=notifications(
					title="New Vendor Please Verify and Activate it !",
					description="New Vendor is Here please Activate his Account Soon !",
					link="/userdetail/seller_profile/"+str(email),
					user=i
					)
				noti_j.save()
				noti_j.link=noti_j.link+"?noti="+str(noti_j.id)
				noti_j.save()




			return redirect('/userdetail/login')
	return render(request,"userdetail/manufacturer_register.html",data)


def brand_register(request):
	data={
	"exist":False
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		if user.count()>0:
			data["exist"]=True
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=True,
				buisness_Customer=False,
				staff=False
			)
			user1.save()
			obj=staff_Categories.objects.filter(name="Merchandising").first()
			objs=detail.objects.filter(staff=True,position='H',staff_category=obj)
			for i in objs:
				noti_j=notifications(
					title="New Vendor Please Verify and Activate it !",
					description="New Vendor is Here please Activate his Account Soon !",
					link="/userdetail/seller_profile/"+str(email),
					user=i
					)
				noti_j.save()
				noti_j.link=noti_j.link+"?noti="+str(noti_j.id)
				noti_j.save()




			return redirect('/userdetail/login')
	return render(request,"userdetail/brand_registration.html",data)





def buisness_register(request):
	data={
	"exist":False
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		if user.count()>0:
			data={
			"exist":True
			}
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=False,
				buisness_Customer=True,
				staff=False
			)
			user1.save()
			objs1=staff_Categories.objects.filter(name="Sales").first()
			objs=detail.objects.filter(
				staff=True,
				staff_category=objs1
				)
			for i in objs:
				oj=notifications(title="New Buisness Account Registered Activate it !",
					description="A New Buisness A/C is Registered please verify it and Activate its Account",
					link="/buisness/buisness_profile/"+str(email),
					user=i)
				oj.save()
				oj.link=oj.link+"?noti="+str(oj.id)
				oj.save()
			return redirect('/userdetail/login')
	return render(request,"userdetail/buisness_register.html",{})

#### STUDENT REGISTRATION #######
def student_register(request):
	data={
	"exist":False
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		user=User.objects.filter(email=email)
		if user.count()>0:
			data={
			"exist":True
			}
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=False,
				buisness_Customer=False,
				staff=False,
				student=True,
			)
			user1.save()
			return redirect('/userdetail/login')
	return render(request,"userdetail/student_register.html",{})


####################################Start of RESUME PARSER FUNCTIONS##################################################


def inpositions(text):
	positions=["Representative","Designer","Engineer","Technician","Developer","Mentor","Assistant","Counselor","Secretary","Manager","Leader"]
	for p in positions:
		if text.find(p)!=-1:
			return True
	return False

def MakeForm(text):
	length=len(text)
	dictionary={}
	flag=0
	count=0
	lines=text.splitlines()
	lines = [x for x in lines if x != '' and x != ' ' and x!='• '] 
	text=text.replace(',','\n')
	#print('start')
	#print(lines)
	#print(text)
	#dictionary['basicdetails']=text
	dictionary['Address']=""
	dictionary['Email']="hello"
	dictionary['Name']=None
	dictionary['Phone']=""
	
	dictionary['Email']=None
	if dictionary['Phone']==None:
		dictionary['Phone']="000000000"
	if dictionary['Email']==None:
		dictionary['Email']="abc@gmail.com"
	if dictionary['Name']==None:
		dictionary['Name']="xyz"
	dictionary['marital']="unmarried"
	edu={}
	education=[]
	inter={}
	internship=[]
	pro={}
	project=[]
	skills=[]
	trainings=0
	trainings=[]
	train={}
	skillmode=0
	no=0
	no_edu=0
	flag1=0
	flag2=0
	flag3=0
	flag4=0
	flag5=0

	for line in lines:
		check_line=line.lower()
		line=re.sub(r"[^a-zA-Z0-9%-.@:\'\"$+/]"," ",line)
		#print('line=',line,flag,count,skillmode)
		#print(check_line)
		#print('t')

		if check_line.find(" ")!=-1:
			#print('name')
			if dictionary['Name']=="xyz":
				#print('done')
				dictionary["Name"]=line
				if line.find("Name")!=-1:
					liner=line.find(' ')
					#print('hi9')
					leng=len(line)
					line=line[liner:leng]
					dictionary["Name"]=line


		if check_line.find("+91")!=-1:
			print('name')
			dictionary["Phone"]=line

			#if line>1000000000:
				#print('phone')
				#dictionary["Phone"]=line
		if line.find("Phone")!=-1:
			#print('phone')
			liner=line.find(' ')
			#print('hi9')
			leng=len(line)
			line=line[liner:leng]
			dictionary["Phone"]=line

		if line.find("Gender")!=-1:
			liner=line.find(' ')
			#print('hi9')
			leng=len(line)
			line=line[liner:leng]
			dictionary["Gender"]=line

		if line.find("Hobbies")!=-1:
			liner=line.find(' ')
			#print('hi9')
			leng=len(line)
			line=line[liner:leng]
			dictionary["Hobbies"]=line

		if line.find('ress')!=-1:
			liner=line.find('Address')+8
			#print('hi9')
			leng=len(line)
			line=line[liner:leng]
			#print(check_line)
			#print('end')
			dictionary["Address"]=line
			
		if line.find('skill')!=-1 or line.find('C++')!=-1 or line.find('python')!=-1 or line.find('Django')!=-1:
			flag4=1

		if flag4 !=0:
			if isskill(check_line)==True:
				line=line.replace("[^a-zA-Z0-9]", " ")
				skills.append(line)

		#print(skillmode)
		#print(check_line)

		if skillmode==0:
			#print(check_line)
			#print(line)
			#print(flag1)
			if line.find('education')!=-1 or line.find('Education')!=-1 or line.find('EDUCATION')!=-1 or line.find('ACADEMIC')!=-1 :
				flag1=1
				flag4=0
			if flag1==1:
				line=line.replace("[^a-zA-Z0-9]", " ")
				education.append(line)
		
		if skillmode==1:
			#print(check_line)
			if line.find('training')!=-1 or line.find('Training')!=-1 or line.find('TRAINING')!=-1 or line.find('TRAIN')!=-1:
				flag3=1
				flag4=0
			if flag3==1:
				line=line.replace("[^a-zA-Z0-9]", " ")
				trainings.append(line)

		if skillmode==1:
			if line.find('project')!=-1 or line.find('Project')!=-1 or line.find('PROJECT')!=-1 or line.find('PROJECTS')!=-1:
				flag2=1
				flag4=0
			if flag2==1:
				line=line.replace("[^a-zA-Z0-9]", " ")
				project.append(line)

		if skillmode==1:
			if line.find('intern')!=-1 or line.find('Intern')!=-1 or line.find('INTERN')!=-1:
				flag5=1
				flag4=0
			if flag5==1:
				line=line.replace("[^a-zA-Z0-9]", " ")
				internship.append(line)

		if check_line.find("github.com")!=-1:
			liner=line.find('github.com')
			#print('hi')
			leng=len(line)
			line=line[liner:leng]
			#print(liner)
			append_str = 'https://'
			line=append_str+line
			dictionary["github"]=line
			continue
			

		if check_line.find("@")!=-1:
			#print('email.ch')
			#print(check_line)
			dictionary["Email"]=check_line
			if check_line.find(" ")!=-1:
				#print('hi')
				#print(line)
				liner=check_line.find('@')-15
				line=check_line[liner:liner+25]
				dictionary["Email"]=line
			continue

		if check_line.find("linkedin")!=-1:
			liner=line.find('linkedin.com')
			#print('hi')
			leng=len(line)
			line=line[liner:leng]
			#print(liner)
			append_str = 'https://'
			line=append_str+line
			dictionary["linkedin"]=line
			continue

		if  bool(re.search(r'\s{0,2}skills\s{0,2}$', check_line)) ==True or line.find("Skills")!=-1 or line.find("SKILLS")!=-1:
			skillmode=1
			flag=0
			count=0
			continue

		if 'responsibility' in check_line or 'education' in check_line  or dictionary['Name'] in line or dictionary['Phone'] in line or dictionary['Email'] in line:
			continue
		
		if line =="  ":
			flag=0
			count=0
		if(check_line.find('internships')!=-1) or bool(re.search(r'\s{0,2}experience\s{0,2}$', check_line)) ==True or (check_line.find('employment history')!=-1):
			#print(line)
			flag=2
			count=0
			skillmode=0
			continue
		if bool(re.search(r'\s{0,2}Projects\s{0,2}', line)) ==True or  bool(re.search(r'\s{0,2}project\s{0,2}$', check_line)) ==True or bool(re.search(r'\s{0,2}projects\s{0,2}$', check_line)) ==True:
			flag=3
			count=0
			skillmode=0
			continue

		if(check_line.find('trainings')!=-1)  or (check_line.find('certifications')!=-1):
			#print(line)
			flag=4
			count=0
			skillmode=0
			continue

		if flag==2:
				#print('intern',count)
				if bool(re.search(r'[0-9]{4}', check_line))==True and count==0:
						inter['Date']=line
						count=0
						continue

				#print(line)
				employment_type=find_emp_type(check_line)
				if employment_type !=None:
					inter['EmpType']=employment_type
				if count==3 :
					
					if len(line)>=20:
						if bool(re.search(r'.\s*$', check_line)) ==True:
							if no==0:
								inter['Description']=line
								#print('final')
								#print(line)
							else:
								des+=line
								inter['Description']=des

							no=0
						else:
							if no==0:
								des=""
							no=no+1
							des+=line+" "
							#print(des)
							#inter['Description']=des
							continue
					else:
						inter['Description']=" "

					if 'EmpType' not in inter.keys():
						inter['EmpType']="Internship"
					if 'Date' not in inter.keys():
						inter['Date']="2000-01-01"
					if 'EndDate' not in inter.keys():
						inter['EndDate']="2000-01-01"
					internship.append(inter)
					#obj=Internship(email=email,position=inter['Position'],company=inter['Company'],date=inter['Date'],desc=inter['Description'])
					#obj.save()
					inter={}
					count=0
				elif count==2 :
					if 'Date' not in inter.keys():
						if bool(re.search(r'[0-9]{4}', check_line))==True :
							l=re.findall(r'[0-9]{4}', check_line)
							if len(l)==1:
								start_date=l[0]+"-01-01"
								edu['Date']=start_date
								end_date="2000-01-01"
								edu['EndDate']=end_date
							if len(l)==2:
								start_date=l[0]+"-01-01"
								edu['Date']=start_date
								end_date=l[1]+"-01-01"
								edu['EndDate']=end_date
							count=3
							continue
						else:
							inter['Date']="2000-01-01"
					else:
						count=3
				elif count==1 :
					if bool(re.search(r'\d', check_line)) ==False :
						line=re.sub(r"[^a-zA-Z0-9]"," ",line)
						inter['Company']=line
						count=2
						continue
					else:
						inter['Company']=" "
				elif count==0 :
					if bool(re.search(r'\d', check_line)) ==False and inpositions(line):
						line=re.sub(r"[^a-zA-Z]"," ",line)
						inter['Position']=line
						count=1
						continue

		if flag==3:
				#print('project',count)
				#print(line)
				if count==3 :
					#if bool(re.search(r'\d', check_line)) ==False :
					if len(line)>=30:
						pro['Description']=line
						count=0
						if 'Link' not in pro.keys():
							pro['Link']="https://"

						project.append(pro)
						pro={}
					else:
						if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
							pro['Description']=" "
							if 'Link' not in pro.keys():
								pro['Link']="https://"
							if 'Date' not in pro.keys():
								pro['Date']="2000-01-01"
							project.append(pro)
							pro={}
							pro['Name']=line
							count=1

					
					#obj=Project(email=email,name=pro['Name'],date=pro['Date'],link=pro['Link'],desc=pro['Description'])
					#obj.save()
					#pro={}
					
				elif count==2 :
					if(line.find("https://")!=-1):
						pro['Link']=line
						count=3
					
				elif count==1 :
					if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date="2000-01-01"
							pro['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date=l[1]+"-01-01"
							pro['EndDate']=end_date
						#print(line)
						count=2
					else:
						if(line.find("https://")!=-1):
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=line
							count=3
				elif count==0 :
					if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
						line=re.sub(r"[^a-zA-Z0-9]"," ",line)
						pro['Name']=line
						count=1
		if flag==4:
			if count==0:
				if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['Title']=line
					count=1

			elif count==1:
				if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['organization']=line
					count=2
				elif bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
					l=re.findall(r'[0-9]{4}', check_line)
					#print(l)
					if len(l)==1:
						start_date=l[0]+"-01-01"
						train['Date']=start_date
						#print(line)
					count=1

			elif count==2:
				if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1 and 'Date' not in train.keys():
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							train['Date']=start_date
						#print(line)
						count=3
				if 'Date' in train.keys():
					count=3
					continue

			elif count==3:
				if len(line)<=50 and bool(re.search(r'\d', check_line)) ==True or  line.find("https://")==-1:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['credentials']=line
					if 'Date' not in train.keys():
						train['Date']="2000-01-01"
					trainings.append(train)
					train={}
					count=0
				elif bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['Title']=line
					train['credentials']="undefined"
					if 'Date' not in train.keys():
						train['Date']="2000-01-01"
					trainings.append(train)
					train={}
					count=0


	if 'degrees' in dictionary.keys():
		degrees=dictionary['degrees']	
	else:
		no_edu=1	
	
	word_tokens = nltk.word_tokenize(text) 
	
	if no_edu ==0:
		for deg in degrees:
			flag=0
			if deg=="x":
				deg+=" "
			edu={}
			for line in lines:
				check_line=line.lower()
				if check_line.find(deg)!=-1 :
					line=re.sub(r"[^a-zA-Z]"," ",line)
					edu['Degree']=line
					field_of_study=find_fields(check_line)
					if field_of_study!=None and 'field_of_study' not in edu:
						edu['field_of_study']=field_of_study
					flag=1
				elif flag==1:
				#print(line)
					if bool(re.search(r'\d', check_line)) ==False and 'Institution' not in edu:
						edu['Institution']=line
					if  bool(re.search(r'[0-9]{4}', check_line))==True and 'Date' not in edu:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							edu['Date']=start_date
							end_date="2000-01-01"
							edu['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							edu['Date']=start_date
							end_date=l[1]+"-01-01"
							edu['EndDate']=end_date
						#edu['Date']=line

					if check_line.find("grade")!=-1 or check_line.find("gpa")!=-1 or check_line.find("cgpa")!=-1 or check_line.find("%")!=-1 and 'Grade' not in edu:
						line=re.sub(r"[^0-9.%]"," ",line)
						edu['Grade']=line
					field_of_study=find_fields(check_line)
					if field_of_study!=None and 'field_of_study' not in edu:
						edu['field_of_study']=field_of_study
			education.append(edu)

	dictionary['Trainings']=trainings
	dictionary["Education"]=education
	dictionary["Internships"]=internship
	dictionary['Projects']=project
	dictionary['Skills']=skills
	#print(skills)
	#print(dictionary)
	
	return dictionary

def handlefile(myfile,email):
	resume=Resumes.objects.filter(email=email)[0]
	r_path=resume.files.path
	kind = filetype.guess(r_path)
	#if kind is None:
		#print('Cannot guess file type!')

	#print('File extension: %s' % kind.extension)
	#print('File MIME type: %s' % kind.mime)

	try:
		if(kind.extension=="pdf"):
			from pdfminer3.layout import LAParams, LTTextBox
			from pdfminer3.pdfpage import PDFPage
			from pdfminer3.layout import LAParams, LTTextBox
			from pdfminer3.pdfpage import PDFPage
			from pdfminer3.pdfinterp import PDFResourceManager
			from pdfminer3.pdfinterp import PDFPageInterpreter
			from pdfminer3.converter import PDFPageAggregator
			from pdfminer3.converter import TextConverter
			import io

			resource_manager = PDFResourceManager()
			fake_file_handle = io.StringIO()
			codec='utf-8'
			converter = TextConverter(resource_manager, fake_file_handle,codec=codec, laparams=LAParams())
			page_interpreter = PDFPageInterpreter(resource_manager, converter)

			with open(r_path, 'rb') as fh:

				for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
				
					page_interpreter.process_page(page)
					text = fake_file_handle.getvalue()

			converter.close()
			fake_file_handle.close()
			#print(text)
			if text=="":
				return HttpResponse('Please check your PDF indentation')
	except:
		return HttpResponse('Please check your PDF indentation')

	if(kind.extension=="png" or kind.extension=="jpg" or kind.extension=="webp"):
		from PIL import Image, ImageFilter, ImageChops
		import pytesseract
		from pytesseract import image_to_string
		import cv2
		filename=r_path
		imgcv = cv2.imread(filename, 0)
		imp = Image.open(filename)
		text=image_to_string(imp)
		#text = main_fun(imgcv,imp,kind.extension)
		#text=main_fun(im)
		#print(text)
		

	dictionary=MakeForm(text)
	#os.remove(r_path)
	#dictionary.replace('"', "'")
	#print(dictionary)
	return dictionary

def handle_uploaded_file(f):  
	with open('static_mtz/upload/'+f.name, 'wb+') as destination:  
		for chunk in f.chunks():  
			destination.write(chunk) 


def save_extracted(request):
	if request.method=="POST":
		name=request.POST.get('Name')
		email=request.POST.get('Email')
		phone=request.POST.get('Phone')
		if email=="abc@gmail.com" or phone=="000000000":
			return HttpResponse("You need to fill correct Phone number and Email id!")
		#add=request.POST.get('Address')
		request.session['email']=email
		dict=request.POST
		github=""
		linkedin=""
		address=""
		gender=""
		dob=""
		hobbies=""
		marital=""
		#print(dict)
		if 'github' in dict.keys():
			github=request.POST.get('github')

		if 'linkedin' in dict.keys():
			linkedin=request.POST.get('linkedin')

		if 'Address' in dict.keys():
			address=request.POST.get('Address')

		if 'gender' in dict.keys():
			gender=request.POST.get('gender')

		if 'DOB' in dict.keys():
			dob=request.POST.get('DOB')

		if 'Hobbies' in dict.keys():
			hobbies=request.POST.get('Hobbies')

		if 'Marital' in dict.keys():
			marital=request.POST.get('Marital')

		obj=social(email = email,dob=dob,gender=gender,martial=marital,hometown=address,hobbies=hobbies,mobile_number=phone,linkedin_profile=linkedin,facebook_profile=github)
		obj.save()

		if 'eDegree1' not in dict.keys():
			return HttpResponse("You need to add atleast one education field!")
		else:
			total=request.POST.get('edutotal')
			#print(total)
			total=(int(total))
			for i in range(1,total+1):
				deg='eDegree'+ str(i)
				date='eDate'+str(i)
				inst='eInstitution'+str(i)
				grade='eGrade'+str(i)
				field='efield'+str(i)
				if request.POST.get(deg)== None:
					continue
				field_of_study=request.POST.get(field)
				degree=request.POST.get(deg)
				#place for field of study
				count_degree=add_degree.objects.filter(name=degree).count()
				count_field=add_field_of_study.objects.filter(name=field_of_study).count()
				if count_degree==0:
					obj=add_degree(name=degree)
					obj.save()
				if count_field==0:
					obj=add_field_of_study(name=field_of_study)
					obj.save()
				degree_id=add_degree.objects.filter(name=degree).values('id')[0]['id']
				field_of_study_id=add_field_of_study.objects.filter(name=field_of_study).values('id')[0]['id']
				#field_of_study_id=add_field_of_study.objects.filter(name=field_of_study).values('id')
				obj=academic(name=name,email=email,school_or_college=request.POST.get(inst),degree_id=degree_id,field_of_study_id=field_of_study_id,start_date=request.POST.get(date),end_date="2020-01-01",grade=request.POST.get(grade))
				obj.save()
				#academic_obj=academic.objects.filter(email=email).all()

		if 'iPosition1' not in dict.keys():
			return HttpResponse("You need to add atleast one internship field!")
		else:
			total=request.POST.get('intertotal')
			#print(total)
			total=(int(total))
			
			for i in range(1,int(total)+1):
				pos='iPosition'+ str(i)
				comp='iCompany'+ str(i)
				date='iDate'+ str(i)
				idesc='iDescription'+ str(i)
				checker='icheck'+str(i)
				emptype='EmpType'+str(i)
				iloc='iLocation'+str(i)
				ienddate='iEndDate'+ str(i)
				title=request.POST.get(pos)
				if title==None:
					continue
				emp_type=request.POST.get(emptype)
				company=request.POST.get(comp)
				location=request.POST.get(iloc)
				start_date=request.POST.get(date)
				#end_date=request.POST.get(ienddate)
				desc=request.POST.get(idesc)
				check=request.POST.get(checker)
				if check=='on':
					end_date=datetime.datetime.now()
					check=True
				else:
					end_date=request.POST.get(ienddate)
					check=False

			
				a=professional_pro(name=name,email=request.user.email,title=title,
				employment_type=emp_type,company=company,current_company=check,
				location=location,start_date=start_date,end_date=end_date,description=desc)
				a.save()

		if 'pName1' not in dict.keys():
			return HttpResponse("You need to add atleast one project field!")
		else:
			total=request.POST.get('prototal')
			#print(total)
			total=(int(total))
			
			for i in range(1,int(total)+1):
				pos='pName'+ str(i)
				#comp='i'+ str(i)
				pdate='pDate'+ str(i)
				pdesc='pDescription'+ str(i)
				link='pLink'+str(i)
				penddate='pEndDate'+ str(i)

				name=request.POST.get(pos)
				if name==None:
					continue
				start_date=request.POST.get(date)
				description=request.POST.get(pdesc)
				plink=request.POST.get(link)
				end_date=request.POST.get(penddate)

				a=add_project(email=email,project_name=name,
				start_date=start_date,end_date=end_date,description=description,project_url=plink)
				a.save()

		if 'skill1' not in dict.keys():
			return HttpResponse("You need to add atleast one skill field!")
		else:
			total=request.POST.get('skilltotal')
			total=(int(total))
			#print(total)
			for i in range(1,int(total)+1):
				skillname='skill'+ str(i)
				if skillname==None:
					continue
				if skillname in dict.keys():
					skill=request.POST.get(skillname)
				obj=add_skill(email=email,name=skill)
				obj.save()	

		if 'tTitle1' in dict.keys():
			total=request.POST.get('traintotal')
			#print(total)
			total=(int(total))
			
			for i in range(1,int(total)+1):
				title='tTitle'+ str(i)
				#comp='i'+ str(i)
				organ='tOrga'+ str(i)
				tDate='tDate'+ str(i)
				tcred='tcred'+str(i)
				#penddate='pEndDate'+ str(i)

				ttitle=request.POST.get(title)
				if ttitle==None:
					continue
				start_date=request.POST.get(tDate)
				organization=request.POST.get(organ)
				credentials=request.POST.get(tcred)

				a=add_certifications(email=email,title=ttitle,
				organization=organization,issued_date=start_date,issued_id=credentials)
				a.save()


		return redirect('academic_profile')


########################################### end of RESUME PARSER FUNCTIONS##################################
#############################################################################################################

def save_user_current_location(request):		
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		print(details)
		user_address = json.loads(request.body)['cur_address_coords']
		print(user_address)
		user_address_coord = user_address
		address_coords = user_address_coord.split(',')
		address_coords.reverse()
		print(address_coords)
		details.current_loc_coord = ",".join(address_coords)
		details.save()
	return JsonResponse({'result': 'ok'})
	# return render(request, 'index.html')


def profile(request):
	if request.user.is_authenticated:
		# Check all subscriprtions have event or not
		# allSubscriptions = Subscription_Order.objects.all()
		# for subscription in allSubscriptions:
		# 	transaction_id = subscription.transaction_id
		# 	events = Event.objects.filter(sub_transaction_id = transaction_id)
		# 	if len(events) == 0:
		# 		createEvents(subscription)
		
		email=request.user.email
		print('here')
		if request.method == 'POST':
			student = StudentForm(request.POST, request.FILES)  
			if student.is_valid():  
				#handle_uploaded_file(request.FILES['file'])
				file=request.FILES['file']  
				kind = filetype.guess(file)
				#obj=Resumes(email=email,files=request.FILES['file'])
				#obj.save()
				try:
					if(kind.extension=="pdf"):
						from pdfminer3.layout import LAParams, LTTextBox
						from pdfminer3.pdfpage import PDFPage
						from pdfminer3.layout import LAParams, LTTextBox
						from pdfminer3.pdfpage import PDFPage
						from pdfminer3.pdfinterp import PDFResourceManager
						from pdfminer3.pdfinterp import PDFPageInterpreter
						from pdfminer3.converter import PDFPageAggregator
						from pdfminer3.converter import TextConverter
						import io

						resource_manager = PDFResourceManager()
						fake_file_handle = io.StringIO()
						codec='utf-8'
						converter = TextConverter(resource_manager, fake_file_handle,codec=codec, laparams=LAParams())
						page_interpreter = PDFPageInterpreter(resource_manager, converter)

						for page in PDFPage.get_pages(file,caching=True,check_extractable=True):
							page_interpreter.process_page(page)
							text = fake_file_handle.getvalue()

						converter.close()
						fake_file_handle.close()

				except:
					return HttpResponse('Please check your PDF indentation')

				if(kind.extension=="png" or kind.extension=="jpg" or kind.extension=="webp"):
					from PIL import Image, ImageFilter, ImageChops
					import pytesseract
					from pytesseract import image_to_string
					import cv2
					#filename=r_path
					#imgcv = cv2.imread(filename, 0)
					#pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'
					imp = Image.open(file)
					text=image_to_string(imp)

				dictionary=MakeForm(text)
				degree=add_degree.objects.all()
				field_of_study=add_field_of_study.objects.all()
				return render(request,'userdetail/check_uploaded_details.html',{'table':dictionary,'email':email,'degree':degree,'fields':field_of_study})
		student = StudentForm() 
		return render(request,"userdetail/profile.html",{'email':email,'form':student})
	
	else:
		return redirect('/userdetail/login')


def recover(request):
	data={
	"invalid":False
	}
	if request.POST.get('email') or request.user.is_authenticated:
		if request.POST.get('email'):
			user=User.objects.filter(email=request.POST.get('email')).first()
			deta=detail.objects.filter(email=request.POST.get('email')).first()
		else:
			user=User.objects.filter(email=request.user.email).first()
			deta=detail.objects.filter(email=request.user.email).first()
		if user and deta:
			# subject,message,from_email,to_list
			subject="Password Recovery !"
			otp=generateOTP6digit()
			deta.user_otp=otp
			deta.user_otp_time=datetime.datetime.now()
			key=randomStringDigits()
			deta.user_otp_key=key
			deta.save()
			message="Hey "+deta.name+"\n\n\nYour OTP verification code is "+str(otp)+"\n\n\nThanks & Regards\nRaymond Institutional Team"
			from_email=EMAIL_HOST_USER
			to_list=[deta.email]
			send_email(subject,message,from_email,to_list)
			return redirect('/userdetail/recover/otp?c='+str(key))
		else:
			data["invalid"]=True
	return render(request,"userdetail/recover.html",data)

import pytz
from django.utils import timezone
from .utils import *
def recover_password(request,key):
	utc=pytz.UTC
	deta=detail.objects.filter(user_otp_key=key).first()
	if deta:
		if deta.user_otp_verify:
			start_time=deta.user_otp_verify
			end_time=start_time + datetime.timedelta(minutes=5)
			cur_time=timezone.now()
			if cur_time>start_time and cur_time<end_time:
				data={
					"invalid":False
				}
				if request.POST.get('new_password') and request.POST.get('confirm_password'):
					new=request.POST.get('new_password')
					confirm=request.POST.get('confirm_password')
					if new!=confirm:
						data["invalid"]=True
						return render(request,"userdetail/recover_password.html",data)
					else:
						user=User.objects.filter(email=deta.email).first()
						if user:
							user.set_password(new)
							user.save()
							deta.password=new
							deta.save()
							return redirect('/')
						else:
							return redirect('/')
				return render(request,"userdetail/recover_password.html",data)
			else:
				return redirect('/')
		else:
			return redirect('/')
	else:
		return redirect('/')


def recover_otp(request):
	check=False
	utc=pytz.UTC
	if request.GET.get('c') or request.POST.get('c'):
		if request.GET.get('c'):
			deta=detail.objects.filter(user_otp_key=request.GET.get('c')).first()
			if deta:
				check=True
		elif request.POST.get('c'):
			deta=detail.objects.filter(user_otp_key=request.GET.get('c')).first()
			if deta:
				check=True
	if check:
		data={
			"invalid":False
		}
		if request.POST.get('c') and request.POST.get('otp'):
			key=deta.user_otp_key
			start_time=deta.user_otp_time
			end_time=start_time + datetime.timedelta(minutes=5)
			cur_time=timezone.now()
			otp=request.POST.get('otp')
			if cur_time>start_time and cur_time<end_time and deta.user_otp==otp:
				deta.user_otp_verify=datetime.datetime.now()
				key=randomStringDigits()
				deta.user_otp_key=key
				deta.save()
				return redirect('/userdetail/recover/new_password/'+str(key))
			else:
				data["invalid"]=True
		return render(request,"userdetail/recover_otp.html",data)
	else:
		return redirect('/')


def logout_page(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('login_page')


def staff_register(request):
	obj=staff_Categories.objects.all()
	#
	seller_data = seller_Categories.objects.all()
	vendor_data = detail.objects.filter(vendor=True)
	#
	data={
	"exist":False,
	"obj":obj, 
	"seller_data": seller_data, #
	'vendor_data': vendor_data, #
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		category=request.POST.get('category')
		category=staff_Categories.objects.filter(name=category).first()
		position=request.POST.get('position')
		seller = request.POST.get('seller')
		seller = seller_Categories.objects.filter(name=seller).first()
		vendor = request.POST.get('vendor')
		user=User.objects.filter(email=email)
		if user.count()>0:
			data={
			"exist":True
			}
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=False,
				buisness_Customer=False,
				staff=True,
				staff_category=category,
				position=position,
				seller_category=seller,
				vendor_name=vendor
			)
			user1.save()
			objs=detail.objects.filter(
				staff=True,
				position='H',
				staff_category=category
				)
			objs1=detail.objects.filter(
				staff=True,
				position='M',
				staff_category=category
				)
			for i in objs:
				oj=notifications(title="New Staff Registered Activate it !",
					description="A New Staff is Registered please verify it and Activate its Account",
					link="/userdetail/staff_profile/"+str(email),
					user=i)
				oj.save()
				oj.link=oj.link+"?noti="+str(oj.id)
				oj.save()
			for i in objs1:
				oj=notifications(title="New Staff Registered Activate it !",
					description="A New Staff is Registered please verify it and Activate its Account",
					link="/userdetail/staff_profile/"+str(email),
					user=i)
				oj.save()
				oj.link=oj.link+"?noti="+str(oj.id)
				oj.save()
			return redirect('/userdetail/login')
	return render(request,"userdetail/staff_register.html",data)


from seller_info.models import washcares,barcodes
from product.models import htm

def seller_dashboard(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		label=labels.objects.filter(vendor=details)
		fit=fits.objects.filter(vendor=details)
		season=seasons.objects.filter(vendor=details)
		meas=measurement.objects.filter(user=details)[:5]
		pro=product.objects.filter(seller=details)
		if pro.count()>0:
			order_bool=True
		else:
			order_bool=False
		washcare=washcares.objects.filter(vendor=details)
		barcode=barcodes.objects.filter(vendor=details)
		product_cate=category.objects.all()
		htm_objects=htm.objects.filter(user=details)
		data={
			"deactivated":True,
			"data":details,
			"label":label,
			"fit":fit,
			"season":season,
			"season_fit":None,
			"meas":meas,
			"orders":pro,
			"order_bool":order_bool,
			"washcare":washcare,
			"barcode":barcode,
			"product_category":product_cate,
			"htm":htm_objects
		}
		if details.vendor:
			if details.activate_Seller:
				data["deactivated"]=False
			if request.POST.get('htm_category_ajax'):
				obj=category.objects.filter(id=int(request.POST.get('htm_category_ajax'))).first()
				obj1=sub_category.objects.filter(product_Category=obj)
				bol=False
				if obj1.count():
					bol=True
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('htm_subcategory_ajax'):
				obj=sub_category.objects.filter(id=int(request.POST.get('htm_subcategory_ajax'))).first()
				obj1=super_category.objects.filter(product_Subcategory=obj)
				bol=False
				if obj1.count():
					bol=True
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('htm_category'):
				cate=category.objects.filter(id=int(request.POST.get('htm_category'))).first()
				sub_cate=sub_category.objects.filter(id=int(request.POST.get('htm_subcategory'))).first()
				super_cate=super_category.objects.filter(id=int(request.POST.get('htm_supercategory'))).first()
				htm_name=request.POST.get('htm')

				htm_file=request.FILES.get('htm_file')
				obj=htm(
						user=details,
						product_Category=cate,
						product_Subcategory=sub_cate,
						product_Supercategory=super_cate,
						name=htm_name,
						file=htm_file
					)
				obj.save()

				return redirect('/userdetail/seller_profile')
			if request.POST.get('washcare'):
				label_obj=labels.objects.filter(slug=request.POST.get('washcare_label')).first()
				season_obj=seasons.objects.filter(slug=request.POST.get('washcare_season')).first()
				fit_obj=fits.objects.filter(slug=request.POST.get('washcare_fit')).first()
				name=request.POST.get('washcare')
				file=request.FILES.get('washcare_file')
				obj=washcares(
					name=name,
					label=label_obj,
					fit=fit_obj,
					season=season_obj,
					file=file,
					vendor=details
				)
				obj.save()
				return redirect('/userdetail/seller_profile')
			if request.POST.get('barcode'):
				label_obj=labels.objects.filter(slug=request.POST.get('barcode_label')).first()
				season_obj=seasons.objects.filter(slug=request.POST.get('barcode_season')).first()
				fit_obj=fits.objects.filter(slug=request.POST.get('barcode_fit')).first()
				name=request.POST.get('barcode')
				file=request.FILES.get('barcode_file')
				obj=barcodes(
					name=name,
					label=label_obj,
					fit=fit_obj,
					season=season_obj,
					file=file,
					vendor=details
				)
				obj.save()
				return redirect('/userdetail/seller_profile')
			if request.POST.get('label') and request.is_ajax:
				# print("here")
				slug="label_"+str(details.id)+"_"+request.POST.get('label')+"_"+str(random.randint(1,999999999999))
				obj=labels(
					name=request.POST.get('label'),
					vendor=details,
					slug=slug)
				obj.save()
				label=labels.objects.filter(vendor=details)
				data["label"]=label
			if request.POST.get('fit'):
				obj1=labels.objects.get(slug=request.POST.get('fit_label'))
				slug="fit_"+str(details.id)+"_"+request.POST.get('fit')+"_"+str(random.randint(1,999999999999))
				obj=fits(
					name=request.POST.get('fit'),
					vendor=details,
					label=obj1,
					slug=slug)
				obj.save()
				fit=fits.objects.filter(vendor=details)
				data["fit"]=fit
			if request.POST.get('season_ajax_label'):
				obj1=labels.objects.get(slug=request.POST.get('season_ajax_label'))
				obj1=fits.objects.filter(label=obj1)
				if obj1.count():
					bol=True
				else:
					bol=False
				print(obj1)
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('barcode_ajax_fit'):
				obj1=fits.objects.filter(slug=request.POST.get('barcode_ajax_fit')).first()
				obj1=seasons.objects.filter(fit=obj1)
				if obj1.count():
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('season'):
				obj1=labels.objects.get(slug=request.POST.get('season_label'))
				obj2=fits.objects.get(slug=request.POST.get('season_fit'))
				slug="season_"+str(details.id)+"_"+request.POST.get('season')+"_"+str(random.randint(1,999999999999))
				obj=seasons(
					name=request.POST.get('season'),
					vendor=details,
					label=obj1,
					fit=obj2,
					slug=slug)
				obj.save()
			return render(request,'userdetail/seller_profile.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def seller_info(request):
	data={
	}
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		try:
			details=detail.objects.get(email=request.user.email)
		except:
			return redirect('/userdetail/logout')
		if details.vendor:
			data={
				"user":details
			}
			if request.POST.get('desc') or request.FILES:
				desc=request.POST.get('desc')
				mission=request.POST.get('mission')
				image=request.FILES.get('image')
				name=request.POST.get('name')
				contact=int(request.POST.get('contact'))
				# bran=request.POST.get('brand')
				# obj=brand.objects.filter(name=bran).first()
				# if obj is None:
				# 	obj=brand(name=bran)
				# 	obj.save()
				# 	objf=staff_Categories.objects.filter(name="Merchandising").first()
				# 	objs=detail.objects.filter(staff=True,staff_category=objf,position='H')
				# 	for i in objs:
				# 		noti_i=notifications(
				# 			title="New Brand Created Activate It Please.",
				# 			description="New Brand is Registered with Name "+str(bran),
				# 			link="/userdetail/activate_brand/"+str(bran),
				# 			user=i
				# 			)
				# 		noti_i.save()
				# details.seller_brand=obj
				details.description=desc
				details.mission=mission
				details.contact=contact
				details.name=name
				if image:
					details.image=image
				details.address=request.POST.get('address')
				addresss=request.POST.get('address')
				a=customer_address(email=request.user.email,address=addresss,permanent=True)
				a.save()
				details.t_and_c=request.POST.get('t_and_c')
				details.info_update=True
				details.save()
				obj_prod=seller_Categories.objects.filter(name="Products Vendor").first()
				if details.seller_category==obj_prod:
					return redirect('/userdetail/seller_profile')
				else:
					return redirect('/userdetail/vendor_profile')
			if request.POST.get('brand_ajax_select'):
				objs=brand.objects.filter(name__icontains=request.POST.get('brand_ajax_select'))
				bol=False
				if objs.count()>0:
					bol=True
				obj1=list(objs.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			return render(request,'userdetail/seller_info.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')







def staff_info(request):
	data={
	}
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		try:
			details=detail.objects.get(email=request.user.email)
		except:
			return redirect('/userdetail/logout')
		if details.staff:
			data={
				"user":details
			}
			if request.POST or request.FILES:
				name=request.POST.get('name')
				contact=int(request.POST.get('contact'))
				desc=request.POST.get('desc')
				mission=request.POST.get('mission')
				image=request.FILES.get('image')
				details.description=desc
				details.mission=mission
				details.name=name
				details.contact=contact
				if image:
					details.image=image
				details.info_update=True
				details.address=request.POST.get('address')
				details.save()
				return redirect('/userdetail/staff_profile')
			return render(request,'userdetail/staff_info.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



from .models import profile_status
from b2b.models import budget_sectors,sector_run_rate
from b2b.models import (budget_years,
budget_month,
budget_sectors,
sector_month_weight,
budget_model,
budget_model_sector)

def staff_profile(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		noti_today=notifications.objects.filter(title="Todays Activity - ")
		for i in noti_today:
			i.delete()
		noti_today=notifications.objects.filter(title="Late Activity - ")
		for i in noti_today:
			i.delete()
		acti_month=str(datetime.datetime.now().month)
		acti_day=str(datetime.datetime.now().day)
		if datetime.datetime.now().day<10:
			acti_day='0'+acti_day
		if datetime.datetime.now().month<10:
			acti_month='0'+acti_month
		acti_year=str(datetime.datetime.now().year)
		acti_date=acti_year+"-"+acti_month+"-"+acti_day
		acti1=activities.objects.filter(planned_date=acti_date,user=details,actual_date=None)
		for i in acti1:
			ojk=notifications(
				title="Todays Activity - ",
				description="Complete this Activity ASAP",
				user=details,
				link="/userdetail/staff_profile/activity/"+str(i.slug)
				)
			ojk.save()
			ojk.link=ojk.link+"?noti="+str(ojk.id)
			ojk.save()
		start_date=datetime.date(1900,1,1)
		end_date=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
		acti1=activities.objects.filter(planned_date__range=[start_date,end_date],user=details,actual_date=None)
		for i in acti1:
			ojk=notifications(
				title="Late Activity - ",
				description="Complete this Activity ASAP",
				user=details,
				link="/userdetail/staff_profile/activity/"+str(i.slug)
				)
			ojk.save()
			ojk.link=ojk.link+"?noti="+str(ojk.id)
			ojk.save()
		noti=notifications.objects.filter(user=details).order_by('-created_on')[:10]
		orders=company_Order.objects.filter(staffs_Allocated=details)
		acti=activities.objects.filter(user=details)
		li=[]
		for o in orders:
			hgf_acti=activities.objects.filter(user=details,order=o,actual_date=None)
			if hgf_acti.count()>0:
				li.append(hgf_acti)
		sales=False
		merchan=False
		mer=staff_Categories.objects.filter(name="Merchandising").first()
		sal=staff_Categories.objects.filter(name="Sales").first()
		if details.staff_category==mer:
			merchan=True
		elif details.staff_category==sal:
			sales=True
		ore=company_Order.objects.filter(staffs_Allocated__email=details.email)
		ui=[]
		ui2=[]
		ui3=[]
		dic={}
		for o in ore:
			ui.append(o.product_Supercategory)
		for u in ui:
			if u not in ui2:
				dic={"label":None,"count":None}
				dic["label"]=u
				ui2.append(u)
				dic["count"]=company_Order.objects.filter(product_Supercategory=u).count()
				ui3.append(dic)
		total=0
		for u in ui3:
			total=total+u["count"]
		for u in ui3:
			u["count"]=round((u["count"])*(100/total),2)
		# print(ui3)
		months=None
		if request.GET.get('profile_perform_filter'):
			a=request.GET.get('profile_perform_filter')
			if a=='o':
				ore=company_Order.objects.filter(staffs_Allocated__email=details.email)
				ui=[]
				ui2=[]
				ui3=[]
				dic={}
				e=ore.filter(order_type='E').count()
				d=ore.filter(order_type='D').count()
				s=ore.filter(order_type='S').count()
				o=ore.filter(order_type='O').count()
				total=e+d+s+o
				if total==0:
					total=1
				ui3=[{"count":round((e*100)/total,2),"label":"Enquiry"},
					{"count":round((d*100)/total,2),"label":"Design"},
					{"count":round((s*100)/total,2),"label":"Sampling"},
					{"count":round((o*100)/total,2),"label":"Order"}]
			elif a=='catr':
				ui=[]
				ui2=[]
				ui3=[]
				dic={}
				for o in ore:
					ui.append(o.product_Supercategory)
				for u in ui:
					if u not in ui2:
						dic={"label":None,"count":None}
						dic["label"]=u
						ui2.append(u)
						kljh=company_Order.objects.filter(product_Supercategory=u)
						for ytr in kljh:
							if ytr.total_Price:
								if ytr.quantity:
									cost=ytr.total_Price*ytr.quantity
								else:
									cost=ytr.total_Price
							elif ytr.target_price:
								if ytr.quantity:
									cost=ytr.target_price*ytr.quantity
								else:
									cost=ytr.target_price
							else:
								cost=0
						dic["count"]=cost
						ui3.append(dic)
				total=0
				for u in ui3:
					total=total+u["count"]
				for u in ui3:
					try:
						u["count"]=round((u["count"])*(100/total),2)
					except:
						u["count"]=0
			elif a=='cusr':
				ui=[]
				ui2=[]
				ui3=[]
				dic={}
				for o in ore:
					ytr=o
					if ytr.total_Price:
						if ytr.quantity:
							cost=ytr.total_Price*ytr.quantity
						else:
							cost=ytr.total_Price
					elif ytr.target_price:
						if ytr.quantity:
							cost=ytr.target_price*ytr.quantity
						else:
							cost=ytr.target_price
					else:
						cost=0
					for asdf in ui3:
						if asdf["label"]==o.user_email:
							asdf["count"]=cost
							break
					else:
						dic["label"]=o.user_email
						dic["count"]=cost
						ui3.append(dic)
				total=0
				for u in ui3:
					total=total+u["count"]
				for u in ui3:
					try:
						u["count"]=round((u["count"])*(100/total),2)
					except:
						u["count"]=0
			elif a=='pr':
				pass
			elif a=='hitr':
				all_orders=company_Order.objects.filter(staffs_Allocated=details).order_by('order_date_time')
				months=[]
				for i in all_orders:
					a=str(i.order_date_time.strftime("%b"))+"_"+str(i.order_date_time.year)
					b=str(i.order_date_time.month)+"_"+str(i.order_date_time.year)
					if [a,b] not in months:
						months.append([a,b])
				per_ord=company_Order.objects.filter(staffs_Allocated=details)
				hit_e_to_d=0
				hit_e_to_s=0
				hit_e_to_o=0
				hit_d_to_s=0
				hit_d_to_o=0
				hit_s_to_o=0
				total=0
				for ikjh in per_ord:
					if ikjh.from_enquiry and ikjh.order_type=='D':
						total+=1
						hit_e_to_d+=1
					elif ikjh.from_enquiry and ikjh.order_type=='S':
						hit_e_to_s+=1
						total+=1
					elif ikjh.from_enquiry and ikjh.order_type=='O':
						hit_e_to_o+=1
						total+=1
					elif ikjh.from_design and ikjh.order_type=='S':
						hit_d_to_s+=1
						total+=1
					elif ikjh.from_design and ikjh.order_type=='O':
						hit_d_to_o+=1
						total+=1
					elif ikjh.from_sample and ikjh.order_type=='O':
						hit_s_to_o+=1
						total+=1
				if total==0:
					total=1
				ui3=[{"label":"Enquiry to Design","count":round(((hit_e_to_d*100)/total),2)},
					{"label":"Enquiry to Sample","count":round(((hit_e_to_s*100)/total),2)},
					{"label":"Enquiry to Order","count":round(((hit_e_to_o*100)/total),2)},
					{"label":"Design to Sample","count":round(((hit_d_to_s*100)/total),2)},
					{"label":"Design to Order","count":round(((hit_d_to_o*100)/total),2)},
					{"label":"Sample to Order","count":round(((hit_s_to_o*100)/total),2)}]
				if request.GET.get('type'):
					ab=request.GET.get('type')
					if ab=='e_to_d':
						for_hit_rat=company_Order.objects.filter(staffs_Allocated=details,order_type='E').count()
						for_hit_rat1=company_Order.objects.filter(staffs_Allocated=details,order_type='D',from_enquiry=True).count()
						total=for_hit_rat+for_hit_rat1
						tot=total
						if total==0:
							tot=0
							total=1
						ui3=[{"label":"Enquiry","count":round(((for_hit_rat*100)/total),2),"color":"#989479","total":tot},
						{"label":"Design","count":round(((for_hit_rat1*100)/total),2),"color":"#d1a683"}]
					elif ab=='e_to_s':
						for_hit_rat=company_Order.objects.filter(staffs_Allocated=details,order_type='E').count()
						for_hit_rat1=company_Order.objects.filter(staffs_Allocated=details,order_type='S',from_enquiry=True).count()
						total=for_hit_rat+for_hit_rat1
						tot=total
						if total==0:
							tot=0
							total=1
						ui3=[{"label":"Enquiry","count":round(((for_hit_rat*100)/total),2),"color":"#f1e0d6","total":tot},
						{"label":"Sample","count":round(((for_hit_rat1*100)/total),2),"color":"#bf988f"}]
					elif ab=="e_to_o":
						for_hit_rat=company_Order.objects.filter(staffs_Allocated=details,order_type='E').count()
						for_hit_rat1=company_Order.objects.filter(staffs_Allocated=details,order_type='O',from_enquiry=True).count()
						total=for_hit_rat+for_hit_rat1
						tot=total
						if total==0:
							tot=0
							total=1
						ui3=[{"label":"Enquiry","count":round(((for_hit_rat*100)/total),2),"color":"#f28a30","total":tot},
						{"label":"Order","count":round(((for_hit_rat1*100)/total),2),"color":"#6465a5"}]
					elif ab=="d_to_s":
						for_hit_rat=company_Order.objects.filter(staffs_Allocated=details,order_type='D').count()
						for_hit_rat1=company_Order.objects.filter(staffs_Allocated=details,order_type='S',from_design=True).count()
						total=for_hit_rat+for_hit_rat1
						tot=total
						if total==0:
							tot=0
							total=1
						ui3=[{"label":"Design","count":round(((for_hit_rat*100)/total),2),"color":"#a79674","total":tot},
						{"label":"Sample","count":round(((for_hit_rat1*100)/total),2),"color":"#0584f2"}]
					elif ab=="d_to_o":
						for_hit_rat=company_Order.objects.filter(staffs_Allocated=details,order_type='D').count()
						for_hit_rat1=company_Order.objects.filter(staffs_Allocated=details,order_type='O',from_design=True).count()
						total=for_hit_rat+for_hit_rat1
						tot=total
						if total==0:
							tot=0
							total=1
						ui3=[{"label":"Design","count":round(((for_hit_rat*100)/total),2),"color":"#6a8a82","total":tot},
						{"label":"Order","count":round(((for_hit_rat1*100)/total),2),"color":"#a7414a"}]
					elif ab=="s_to_o":
						for_hit_rat=company_Order.objects.filter(staffs_Allocated=details,order_type='S').count()
						for_hit_rat1=company_Order.objects.filter(staffs_Allocated=details,order_type='O',from_sample=True).count()
						total=for_hit_rat+for_hit_rat1
						tot=total
						if total==0:
							tot=0
							total=1
						ui3=[{"label":"Sample","count":round(((for_hit_rat*100)/total),2),"color":"#f18904","total":tot},
						{"label":"Order","count":round(((for_hit_rat1*100)/total),2),"color":"#36688d"}]
				if request.GET.get('month'):
					month_for_find=request.GET.get('month')
					amao=request.GET.get('type')
					try:
						month_ord,year_ord=map(int,month_for_find.strip().split("_"))
						for_hit_pat=company_Order.objects.filter(order_date_time__month=month_ord,order_date_time__year=year_ord)
					except:
						amao=None
					if amao:
						ab=request.GET.get('type')
						if ab=='e_to_d':
							for_hit_rat=for_hit_pat.filter(staffs_Allocated=details,order_type='E').count()
							for_hit_rat1=for_hit_pat.filter(staffs_Allocated=details,order_type='D',from_enquiry=True).count()
							total=for_hit_rat+for_hit_rat1
							tot=total
							if total==0:
								tot=0
								total=1
							ui3=[{"label":"Enquiry","count":round(((for_hit_rat*100)/total),2),"color":"#989479","total":tot},
							{"label":"Design","count":round(((for_hit_rat1*100)/total),2),"color":"#d1a683"}]
						elif ab=='e_to_s':
							for_hit_rat=for_hit_pat.filter(staffs_Allocated=details,order_type='E').count()
							for_hit_rat1=for_hit_pat.filter(staffs_Allocated=details,order_type='S',from_enquiry=True).count()
							total=for_hit_rat+for_hit_rat1
							tot=total
							if total==0:
								tot=0
								total=1
							ui3=[{"label":"Enquiry","count":round(((for_hit_rat*100)/total),2),"color":"#f1e0d6","total":tot},
							{"label":"Sample","count":round(((for_hit_rat1*100)/total),2),"color":"#bf988f"}]
						elif ab=="e_to_o":
							for_hit_rat=for_hit_pat.filter(staffs_Allocated=details,order_type='E').count()
							for_hit_rat1=for_hit_pat.filter(staffs_Allocated=details,order_type='O',from_enquiry=True).count()
							total=for_hit_rat+for_hit_rat1
							tot=total
							if total==0:
								tot=0
								total=1
							ui3=[{"label":"Enquiry","count":round(((for_hit_rat*100)/total),2),"color":"#f28a30","total":tot},
							{"label":"Order","count":round(((for_hit_rat1*100)/total),2),"color":"#6465a5"}]
						elif ab=="d_to_s":
							for_hit_rat=for_hit_pat.filter(staffs_Allocated=details,order_type='D').count()
							for_hit_rat1=for_hit_pat.filter(staffs_Allocated=details,order_type='S',from_design=True).count()
							total=for_hit_rat+for_hit_rat1
							tot=total
							if total==0:
								tot=0
								total=1
							ui3=[{"label":"Design","count":round(((for_hit_rat*100)/total),2),"color":"#a79674","total":tot},
							{"label":"Sample","count":round(((for_hit_rat1*100)/total),2),"color":"#0584f2"}]
						elif ab=="d_to_o":
							for_hit_rat=for_hit_pat.filter(staffs_Allocated=details,order_type='D').count()
							for_hit_rat1=for_hit_pat.filter(staffs_Allocated=details,order_type='O',from_design=True).count()
							total=for_hit_rat+for_hit_rat1
							tot=total
							if total==0:
								tot=0
								total=1
							ui3=[{"label":"Design","count":round(((for_hit_rat*100)/total),2),"color":"#6a8a82","total":tot},
							{"label":"Order","count":round(((for_hit_rat1*100)/total),2),"color":"#a7414a"}]
						elif ab=="s_to_o":
							for_hit_rat=for_hit_pat.filter(staffs_Allocated=details,order_type='S').count()
							for_hit_rat1=for_hit_pat.filter(staffs_Allocated=details,order_type='O',from_sample=True).count()
							total=for_hit_rat+for_hit_rat1
							tot=total
							if total==0:
								tot=0
								total=1
							ui3=[{"label":"Sample","count":round(((for_hit_rat*100)/total),2),"color":"#f18904","total":tot},
							{"label":"Order","count":round(((for_hit_rat1*100)/total),2),"color":"#36688d"}]
		todays_resp=response_time.objects.filter(user=details,
			date__day=datetime.datetime.now().day,
			date__month=datetime.datetime.now().month,
			date__year=datetime.datetime.now().year)
		last_few_resp=response_time.objects.filter(user=details).order_by("-date")[:15]
		if todays_resp.count()>0:
			todays_resp=todays_resp.first().response_tm
		else:
			todays_resp=0
		target_resp=details.target_response_time
		print(last_few_resp)
		oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
		oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
		oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
		oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
		oty4=oty1+oty2+oty3+oty
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		obj_check=esclation_home.objects.filter(active=True).first()
		if obj_check:
			fgh=datetime.datetime.now()
			# cur_dat=datetime.date(fgh.date.year,fgh.date.month,fgh.date.day)
			fgh1=obj_check.last_check
			fgh1=datetime.datetime(year=fgh1.year,month=fgh1.month,day=fgh1.day,hour=fgh1.hour,minute=fgh1.minute)

			# last_check_dat=datetime.date(fgh1.date.year,fgh1.date.month,fgh1.date.day)
			diffi=fgh-fgh1
			diffi=diffi.total_seconds()/3600
			if diffi>23:
				acti=activities.objects.all()
				for ik in acti:
					if ik.custom_date is None:
						d1=datetime.datetime(ik.planned_date.year,
							ik.planned_date.month,
							ik.planned_date.day)
					else:
						d1=datetime.datetime(ik.custom_date.year,
							ik.custom_date.month,
							ik.custom_date.day)
					if ik.upto_head:
						pass
					elif ik.upto_manager:

						d1=d1+datetime.timedelta(days=ik.activity_Cate.escalation_Time_for_Executive)
						d2=datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,
							datetime.datetime.now().day)
						if d1>d2:
							to_be_staff=ik.order.staffs_Allocated.all().filter(position='H')
							for jk in to_be_staff:
								ik.esclated_user.add(jk)
								obj3=notifications.objects.filter(description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") (Activity Slug - "+str(ik.slug)+")",
									user=jk)
								if obj3.count()==0:
									obj3=notifications(
										title="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+")",
										description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") (Activity Slug - "+str(ik.slug)+")",
										user=jk,
										link="/userdetail/staff_profile/activity/"+str(ik.slug),
										type_of_order=ik.order.order_type
										)
									obj3.save()
									obj3.link=obj3.link+"?noti="+str(obj3.id)
									obj3.save()
						ik.upto_head=True
						ik.save()
					else:

						d1=d1+datetime.timedelta(days=ik.activity_Cate.escalation_Time_for_Manager)
						d2=datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,
							datetime.datetime.now().day)
						if d1>d2:
							to_be_staff=ik.order.staffs_Allocated.all().filter(position='M')
							for jk in to_be_staff:
								ik.esclated_user.add(jk)
								obj3=notifications.objects.filter(description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") (Activity Slug - "+str(ik.slug)+")",
									user=jk)
								if obj3.count()==0:
									obj3=notifications(
										title="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+")",
										description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") (Activity Slug - "+str(ik.slug)+")",
										user=jk,
										link="/userdetail/staff_profile/activity/"+str(ik.slug),
										type_of_order=ik.order.order_type
										)
									obj3.save()
									obj3.link=obj3.link+"?noti="+str(obj3.id)
									obj3.save()
						ik.upto_manager=True
						ik.save(

)
				obj_check.last_check=datetime.datetime.now()
				obj_check.save()

		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		brand=detail.objects.filter(email="raymond@raymond.in").first()

		current_year=datetime.datetime.now().year
		if request.GET.get('budget_year'):
			current_year=int(request.GET.get('budget_year'))
		months_wise_budget=[]
		for i in range(1,13):
			orders=company_Order.objects.filter(order_date_time__year=current_year,order_date_time__month=i)
			val=0
			for j in orders:
				val+=j.get_billing_amount
			months_wise_budget.append(val)
		cur_year_run=datetime.datetime.now().year
		custom_filter=[{"val":cur_year_run-2,"name":cur_year_run-2,"s":0},{"val":cur_year_run-1,"name":cur_year_run-1,"s":0},
		{"val":cur_year_run,"name":cur_year_run,"s":1},{"val":cur_year_run+1,"name":cur_year_run+1,"s":0},
		{"val":cur_year_run+2,"name":cur_year_run+2,"s":0}]
		if details.run_rate:
			tot_rev_m=round(details.run_rate/12)
		else:
			tot_rev_m=1
		m_wise_run_act=[]
		m_wise_run_exp=[]
		for i in range(1,13):
			orders=company_Order.objects.filter(order_date_time__year=cur_year_run,order_date_time__month=i)
			val=0
			for j in orders:
				val+=j.get_billing_amount
			m_wise_run_act.append([val,{"year":cur_year_run,"month":i}])
			m_wise_run_exp.append([tot_rev_m,{"year":cur_year_run,"month":i}])
		min_run={"year":cur_year_run-1,"month":12}
		max_run={"year":cur_year_run,"month":11}
		# print(m_wise_run_act)
		sector=budget_sectors.objects.filter(user=brand).first()
		bud_mod=budget_model.objects.filter(user=brand).first()
		per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
		cur_year=bud_mod.year
		check_run=[]
		for i in range(1,13):
			orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
			val=0
			for j in orders:
				val+=j.get_billing_amount
			check_run.append(val)
		data={
			"check_run":check_run,
			"cur_year":cur_year,
			"per_month":per_month,
			"m_wise_run_exp":m_wise_run_exp,
			"m_wise_run_act":m_wise_run_act,
			"min_run":min_run,
			"max_run":max_run,
			"custom_filter":custom_filter,
			"sectors":budget_sectors.objects.filter(user=brand),
			"budget_years":budget_model.objects.filter(user=brand),
			"months_wise_budget":months_wise_budget,
			"current_year":current_year,
			"deactivated":True,
			"data":details,
			"obj":None,
			"head":False,
			"staff":False,
			"manager":False,
			"noti":noti,
			"ord":orders,
			"acti":li,
			"current":datetime.datetime.now().date,
			"merch":merchan,
			"sales":sales,
			"vend":detail.objects.filter(vendor=True),
			"b2b_cust":detail.objects.filter(buisness_Customer=True),
			"ui2":ui2,
			"ui3":ui3,
			"dic":dic,
			"todays_resp":todays_resp,
			"target_resp":target_resp,
			"up_resp_fail":False,
			"last_few_resp":last_few_resp,
			"oty":oty,
			"oty1":oty1,
			"oty2":oty2,
			"oty3":oty3,
			"oty4":oty4,
			"months":months
		}
		if details.staff:
			if details.activate_Staff:
				data["deactivated"]=False

			if details.position=='H':
				obj=detail.objects.filter(staff=True,staff_category=details.staff_category,position='M')[:5]
				obj_Head="Managers"
				data["obj"]=obj
				data["head"]=True
			if details.position=='M':
				obj=detail.objects.filter(staff=True,staff_category=details.staff_category,position='C')[:5]
				obj_Head="Staff"
				data["obj"]=obj
				data["manager"]=True
			if request.POST.get('up_resp'):
				details.target_response_time=int(request.POST.get('up_resp'))
				if details.last_target is not None:
					d0=datetime.date(details.last_target.year,details.last_target.month,details.last_target.day)
					d1=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
					delta=d0-d1
					if delta.days>15:
						details.last_target=details.last_target1
						details.last_target1=details.last_target2
						details.last_target2=timezone.now().date()
						data["target_resp"]=details.target_response_time
						details.save()
					else:
						data["up_resp_fail"]=True
				else:
					details.last_target=details.last_target1
					details.last_target1=details.last_target2
					print()
					details.last_target2=timezone.now().date()
					data["target_resp"]=details.target_response_time
					details.save()
			if request.POST.get('up_budget'):
				details.budget_hit_rate=request.POST.get('up_budget')
				details.save()
			if request.POST.get('profile_status_ajax'):
				profile_obj=profile_status.objects.filter(date_update__month=datetime.datetime.now().month,
					date_update__year=datetime.datetime.now().year,
					date_update__day=datetime.datetime.now().day,user=details).first()
				if not(profile_obj):
					profile_obj=profile_status(date_update=datetime.datetime.now(),user=details)
				profile_obj.status=request.POST.get('profile_status_ajax')
				profile_obj.save()
				return JsonResponse({"done":True})
			if request.POST.get('sector_update_ajax'):
				sector=budget_sectors.objects.filter(id=request.POST.get('sector_update_ajax')).first()
				bud_mod=budget_model.objects.filter(user=brand).first()
				per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
				cur_year=bud_mod.year
				expected_run=[]
				actual_run=[]
				for i in range(1,13):
					orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
					val=0
					for j in orders:
						val+=j.get_billing_amount
					expected_run.append({"year":cur_year.year,"month":i-1,"day":0,"val":per_month})
					actual_run.append({"year":cur_year.year,"month":i-1,"day":0,"val":val})
				ajax_data={
					"format":"MMM",
					"min_year":cur_year.year,
					"min_month":0,
					"min_day":0,
					"max_year":cur_year.year,
					"max_month":11,
					"max_day":0,
					"expected_run":expected_run,
					"actual_run":actual_run
				}
				return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
			if request.POST.get('sector_year_ajax'):
				sector=budget_sectors.objects.filter(id=request.POST.get('sector_year_update_ajax')).first()
				yea=budget_years.objects.filter(year=request.POST.get('sector_year_ajax')).first()
				bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
				per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
				cur_year=bud_mod.year
				expected_run=[]
				actual_run=[]
				for i in range(1,13):
					orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
					val=0
					for j in orders:
						val+=j.get_billing_amount
					expected_run.append({"year":cur_year.year,"month":i-1,"day":0,"val":per_month})
					actual_run.append({"year":cur_year.year,"month":i-1,"day":0,"val":val})
				ajax_data={
					"format":"MMM",
					"min_year":cur_year.year,
					"min_month":0,
					"min_day":0,
					"max_year":cur_year.year,
					"max_month":11,
					"max_day":0,
					"expected_run":expected_run,
					"actual_run":actual_run
				}
				return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
			if request.POST.get('sector_mode_ajax'):
				if request.POST.get('sector_mode_ajax')=="yearly":
					sector=budget_sectors.objects.filter(id=request.POST.get('sector_mode_update_ajax')).first()
					yea=budget_years.objects.filter(year=request.POST.get('sector_mode_year_ajax')).first()
					bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
					per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
					cur_year=bud_mod.year
					expected_run=[]
					actual_run=[]
					for i in range(1,13):
						orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
						val=0
						for j in orders:
							val+=j.get_billing_amount
						expected_run.append({"year":cur_year.year,"month":i-1,"day":0,"val":per_month})
						actual_run.append({"year":cur_year.year,"month":i-1,"day":0,"val":val})
					ajax_data={
						"format":"MMM",
						"min_year":cur_year.year,
						"min_month":0,
						"min_day":0,
						"max_year":cur_year.year,
						"max_month":11,
						"max_day":0,
						"expected_run":expected_run,
						"actual_run":actual_run
					}
					return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
				elif request.POST.get('sector_mode_ajax')=="half":
					sector=budget_sectors.objects.filter(id=request.POST.get('sector_mode_update_ajax')).first()
					yea=budget_years.objects.filter(year=request.POST.get('sector_mode_year_ajax')).first()
					bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
					per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
					cur_year=bud_mod.year
					expected_run=[]
					actual_run=[]
					for i in range(1,7):
						orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
						val=0
						for j in orders:
							val+=j.get_billing_amount
						expected_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":per_month})
						actual_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":val})
					ajax_data={
						"format":"MMM",
						"min_year":cur_year.year,
						"min_month":0,
						"min_day":1,
						"max_year":cur_year.year,
						"max_month":5,
						"max_day":1,
						"expected_run":expected_run,
						"actual_run":actual_run
					}
					return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
				elif request.POST.get('sector_mode_ajax')=="quart":
					sector=budget_sectors.objects.filter(id=request.POST.get('sector_mode_update_ajax')).first()
					yea=budget_years.objects.filter(year=request.POST.get('sector_mode_year_ajax')).first()
					bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
					per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
					cur_year=bud_mod.year
					expected_run=[]
					actual_run=[]
					for i in range(1,4):
						orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
						val=0
						for j in orders:
							val+=j.get_billing_amount
						expected_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":per_month})
						actual_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":val})
					ajax_data={
						"format":"MMM",
						"min_year":cur_year.year,
						"min_month":0,
						"min_day":1,
						"max_year":cur_year.year,
						"max_month":2,
						"max_day":1,
						"expected_run":expected_run,
						"actual_run":actual_run
					}
					return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
				elif request.POST.get('sector_mode_ajax')=="month":
					sector=budget_sectors.objects.filter(id=request.POST.get('sector_mode_update_ajax')).first()
					yea=budget_years.objects.filter(year=request.POST.get('sector_mode_year_ajax')).first()
					bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
					per_month=((bud_mod.yearly_amount*sector.weight_percent/100)//12)//31
					cur_year=bud_mod.year
					expected_run=[]
					actual_run=[]
					for i in range(1,32):
						orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=1,order_date_time__day=i)
						val=0
						for j in orders:
							val+=j.get_billing_amount
						expected_run.append({"year":cur_year.year,"month":0,"day":i,"val":per_month})
						actual_run.append({"year":cur_year.year,"month":0,"day":i,"val":val})
					ajax_data={
						"format":"D MMM",
						"min_year":cur_year.year,
						"min_month":0,
						"min_day":1,
						"max_year":cur_year.year,
						"max_month":0,
						"max_day":31,
						"expected_run":expected_run,
						"actual_run":actual_run
					}
					return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
			if request.POST.get('sector_mode_custom_ajax'):
				if request.POST.get('sector_mode_custom_ajax')=="yearly":
					return JsonResponse({"sub":[]})
				elif request.POST.get('sector_mode_custom_ajax')=="half":
					return JsonResponse({"sub":["H1","H2"]})
				elif request.POST.get('sector_mode_custom_ajax')=="quart":
					return JsonResponse({"sub":["Q1","Q2","Q3","Q4"]})
				elif request.POST.get('sector_mode_custom_ajax')=="month":
					return JsonResponse({"sub":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]})
			if request.POST.get('sector_custom_ajax'):
				if request.POST.get('sector_custom_mode_ajax')=="yearly":
					pass
				elif request.POST.get('sector_custom_mode_ajax')=="half":
					if request.POST.get('sector_custom_ajax')=="H1":
						start=1
						end=7
					else:
						start=7
						end=13
					sector=budget_sectors.objects.filter(id=request.POST.get('sector_custom_update_ajax')).first()
					yea=budget_years.objects.filter(year=request.POST.get('sector_custom_year_ajax')).first()
					bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
					per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
					cur_year=bud_mod.year
					expected_run=[]
					actual_run=[]
					for i in range(start,end):
						orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
						val=0
						for j in orders:
							val+=j.get_billing_amount
						expected_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":per_month})
						actual_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":val})
					ajax_data={
						"format":"MMM",
						"min_year":cur_year.year,
						"min_month":start-1,
						"min_day":1,
						"max_year":cur_year.year,
						"max_month":end-2,
						"max_day":1,
						"expected_run":expected_run,
						"actual_run":actual_run
					}
					return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
				elif request.POST.get('sector_custom_mode_ajax')=="quart":
					if request.POST.get('sector_custom_ajax')=="Q1":
						start=1
						end=4
					elif request.POST.get('sector_custom_ajax')=="Q2":
						start=4
						end=7
					elif request.POST.get('sector_custom_ajax')=="Q3":
						start=7
						end=10
					else:
						start=10
						end=13
					sector=budget_sectors.objects.filter(id=request.POST.get('sector_custom_update_ajax')).first()
					yea=budget_years.objects.filter(year=request.POST.get('sector_custom_year_ajax')).first()
					bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
					per_month=(bud_mod.yearly_amount*sector.weight_percent/100)//12
					cur_year=bud_mod.year
					expected_run=[]
					actual_run=[]
					for i in range(start,end):
						orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=i)
						val=0
						for j in orders:
							val+=j.get_billing_amount
						expected_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":per_month})
						actual_run.append({"year":cur_year.year,"month":i-1,"day":1,"val":val})
					ajax_data={
						"format":"MMM",
						"min_year":cur_year.year,
						"min_month":start-1,
						"min_day":1,
						"max_year":cur_year.year,
						"max_month":end-2,
						"max_day":1,
						"expected_run":expected_run,
						"actual_run":actual_run
					}
					return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
				elif request.POST.get('sector_custom_mode_ajax')=="month":
					no=31
					if request.POST.get('sector_custom_ajax')=="Jan":
						n=1
					elif request.POST.get('sector_custom_ajax')=="Feb":
						n=2
						no=28
					elif request.POST.get('sector_custom_ajax')=="Mar":
						n=3
					elif request.POST.get('sector_custom_ajax')=="Apr":
						n=4
						no=30
					elif request.POST.get('sector_custom_ajax')=="May":
						n=5
					elif request.POST.get('sector_custom_ajax')=="Jun":
						n=6
						no=30
					elif request.POST.get('sector_custom_ajax')=="Jul":
						n=7
					elif request.POST.get('sector_custom_ajax')=="Aug":
						n=8
						no=30
					elif request.POST.get('sector_custom_ajax')=="Sep":
						n=9
					elif request.POST.get('sector_custom_ajax')=="Oct":
						n=10
					elif request.POST.get('sector_custom_ajax')=="Nov":
						n=11
						no=30
					elif request.POST.get('sector_custom_ajax')=="Dec":
						n=12
					sector=budget_sectors.objects.filter(id=request.POST.get('sector_custom_update_ajax')).first()
					yea=budget_years.objects.filter(year=request.POST.get('sector_custom_year_ajax')).first()
					bud_mod=budget_model.objects.filter(user=brand,year=yea).first()
					per_month=((bud_mod.yearly_amount*sector.weight_percent/100)//12)//no
					cur_year=bud_mod.year
					expected_run=[]
					actual_run=[]
					for i in range(1,no+1):
						orders=company_Order.objects.filter(order_date_time__year=cur_year.year,order_date_time__month=n,order_date_time__day=i)
						val=0
						for j in orders:
							val+=j.get_billing_amount
						expected_run.append({"year":cur_year.year,"month":n-1,"day":i,"val":per_month})
						actual_run.append({"year":cur_year.year,"month":n-1,"day":i,"val":val})
					ajax_data={
						"format":"D MMM",
						"min_year":cur_year.year,
						"min_month":n-1,
						"min_day":1,
						"max_year":cur_year.year,
						"max_month":n-1,
						"max_day":no,
						"expected_run":expected_run,
						"actual_run":actual_run
					}
					return render(request,"ajax_response/userdetail/budget_run_rate.html",ajax_data)
			return render(request,'userdetail/staff_profile.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




def vendor_profile_orders_lay(request,order_no=None,*args,**kwargs):
		order=company_Order.objects.get(order_no=order_no)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		colors_cum_prod=[]
		address_cum_prod=[]
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
						if not (j.color in colors_cum_prod):
								colors_cum_prod.append(j.color)
						if not (j.address in address_cum_prod):
								address_cum_prod.append(j.address)
		sizes_cum_prod.sort()
		map_prod={}
		for i in kjh:
				for j in colors_cum_prod:
						for k in address_cum_prod:
								for l in sizes_cum_prod:
										gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
										if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
												map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.14)
										elif gfb:
												map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												for m in sizes_cum_prod:
														map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
												map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.14)
		print(map_prod)
		print(sizes_cum_prod)
		return render(request,'vendor/vendor_profile_orders_lay.html',{'order':order,'map_prod':map_prod,'sizes_cum_prod':sizes_cum_prod})

def cutting(request):
		return render(request,'vendor/cutting.html',{})


def vendor_profile_orders_cut(request,order_no=None,*args,**kwargs):
		order=company_Order.objects.get(order_no=order_no)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		colors_cum_prod=[]
		address_cum_prod=[]
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
						if not (j.color in colors_cum_prod):
								colors_cum_prod.append(j.color)
						if not (j.address in address_cum_prod):
								address_cum_prod.append(j.address)
		sizes_cum_prod.sort()
		map_prod={}
		extra_prod={}
		stock={}
		for i in kjh:
				for j in colors_cum_prod:
						for k in address_cum_prod:
								for l in sizes_cum_prod:
										gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
										if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
												map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
												extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.04)
												stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.1)
										elif gfb:
												map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												extra_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												stock[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												for m in sizes_cum_prod:
														map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
														extra_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
														stock[(str(j.id)+"_"+str(k.id))][1].append(0)
												map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
												extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.04)
												stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.1)
		print(map_prod)
		print(sizes_cum_prod)
		return render(request,'vendor/vendor_profile_orders_cut.html',{'order':order,'map_prod':map_prod,'sizes_cum_prod':sizes_cum_prod,'extra_prod':extra_prod,'stock':stock})

def lay_detail_view2(request,order_no,color):
		order=company_Order.objects.get(order_no=order_no)
		print(color)
		def check2(bal):
				for i in bal:
						if(i[1]!=0):
								return True
				return False
		def getlay2(l,red,t,y,g):
				siz=len(red)
				bal=[]
				for i in red:
						f=[]
						f.append(i[0])
						f.append(i[1])
						bal.append(f)
				while(check2(red)):
						red.sort(key=lambda x:x[1])
						s=0
						j=0
						tee=4
						u=[]
						for j in range(0,siz):
								if(red[j][1]>0):
										s=red[j][1]
										red[j][1]=0
										u.append(red[j][0])
										tee=tee-1
										break
						red.sort(key=lambda x:x[0])
						for i in range(0,siz):
								if(red[i][1]%s==0):
										while((tee>0) and (red[i][1])>0):
												red[i][1]=red[i][1]-s
												u.append(red[i][0])
												tee=tee-1
						for i in range(0,siz):
								if(red[i][1]>0 and tee>0):
										red[i][1]=red[i][1]-s
										u.append(red[i][0])
										tee=tee-1
						l.append(s)
						c=[]
						red.sort(key=lambda x:x[0])
						for i in bal:
								c.append(i[1])
						y.append(c)
						bal=[]
						d=[]
						for i in red:
								d.append(i[1])
								f=[]
								f.append(i[0])
								f.append(i[1])
								bal.append(f)
						t.append(d)
						u.sort()
						g.append(u)
				print(l)
				print(t)
				print(y)
				print(g)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
		sizes_cum_prod.sort()
		map_prod={}
		cl=color_model.objects.get(name=color)
		for i in kjh:
				for l in sizes_cum_prod:
						gfb=i.sizes.all().filter(color=cl,size_label=l).first()
						if (gfb in map_prod):
								map_prod[l]+=int(gfb.quantity*1.14)
						elif gfb:
								map_prod[l]=0
								map_prod[l]+=int(gfb.quantity*1.14)
						else:
								map_prod[l]=0
		print(map_prod)
		red=[]
		for l in sizes_cum_prod:
				f=[]
				f.append(l)
				f.append(map_prod[l])
				red.append(f)       
		l=[]
		t=[]
		y=[]
		g=[]
		getlay2(l,red,t,y,g)
		te=[]
		it=1
		for i in l:
				te.append(it)
				it=it+1
		u=zip(l,t,y,g,te)
		return render(request, 'vendor/lay_detail.html', {'data': u,'order':order,'sizes':sizes_cum_prod,'color':color})

def lay_detail_view3(request,order_no,color):
		order=company_Order.objects.get(order_no=order_no)
		print(color)
		def check3(bal):
				for i in bal:
						if(i[1]!=0):
								return True
				return False
		def getlay3(l,red,t,y,g):
				siz=len(red)
				bal=[]
				for i in red:
						f=[]
						f.append(i[0])
						f.append(i[1])
						bal.append(f)
				while(check3(red)):
						red.sort(key=lambda x:x[1])
						s=10
						j=0
						tee=4
						u=[]
						se=set()
						for j in range(0,siz):
								if(red[j][1]>0):
										se.add((red[j][1]))
						se= list(se)
						se.sort()
						leng=len(se)
						if(leng%2==0):
								uee=int(leng/2)
								print(uee)
								print(se[uee])
								if(se[uee]>se[uee-1]):
										s=se[uee-1]
								else:
										s=se[uee]
						else:
								uee=int(leng/2)
								s=se[uee]
						red.sort(key=lambda x:x[0])
						for i in range(0,siz):
								if(red[i][1]%s==0):
										while((tee>0) and (red[i][1])>0):
												red[i][1]=red[i][1]-s
												u.append(red[i][0])
												tee=tee-1
						for i in range(0,siz):
								if(red[i][1]>s and tee>0):
										red[i][1]=red[i][1]-s
										u.append(red[i][0])
										tee=tee-1
						l.append(s)
						c=[]
						red.sort(key=lambda x:x[0])
						for i in bal:
								c.append(i[1])
						y.append(c)
						bal=[]
						d=[]
						for i in red:
								d.append(i[1])
								f=[]
								f.append(i[0])
								f.append(i[1])
								bal.append(f)
						t.append(d)
						u.sort()
						g.append(u)
				print(l)
				print(t)
				print(y)
				print(g)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
		sizes_cum_prod.sort()
		map_prod={}
		cl=color_model.objects.get(name=color)
		for i in kjh:
				for l in sizes_cum_prod:
						gfb=i.sizes.all().filter(color=cl,size_label=l).first()
						if (gfb in map_prod):
								map_prod[l]+=int(gfb.quantity*1.14)
						elif gfb:
								map_prod[l]=0
								map_prod[l]+=int(gfb.quantity*1.14)
						else:
								map_prod[l]=0
		print(map_prod)
		red=[]
		for l in sizes_cum_prod:
				f=[]
				f.append(l)
				f.append(map_prod[l])
				red.append(f)       
		l=[]
		t=[]
		y=[]
		g=[]
		getlay3(l,red,t,y,g)
		te=[]
		it=1
		for i in l:
				te.append(it)
				it=it+1
		u=zip(l,t,y,g,te)
		return render(request, 'vendor/lay_detail.html', {'data': u,'order':order,'sizes':sizes_cum_prod,'color':color})

def lay_detail_view4(request,order_no,color):
		order=company_Order.objects.get(order_no=order_no)
		print(color)
		def check4(bal):
				for i in bal:
					if(i[1]>2):
						return True
				return False
		def getlay4(l,red,t,y,g):
				siz=len(red)
				bal=[]
				for i in red:
					f=[]
					f.append(i[0])
					f.append(i[1])
					bal.append(f)
				while(check4(red)):
					red.sort(reverse=True,key=lambda x:x[1])
					ti=False
					s=0
					for j in range(0,siz-1):
						if(red[j][1]==red[j+1][1] and red[j][1]>3):
							s=red[j][1]
							ti=True
							break
					if(ti==True):
						l.append(s)
						c=[]
						u=[]
						for i in range(0,siz):
							if(red[i][1]>=s):
								red[i][1]=red[i][1]-s
								u.append(red[i][0])
						red.sort(key=lambda x:x[0])
						for i in bal:
							c.append(i[1])
						y.append(c)
						bal=[]
						d=[]
						for i in red:
							d.append(i[1])
							f=[]
							f.append(i[0])
							f.append(i[1])
							bal.append(f)
						t.append(d)
						u.sort()
						g.append(u)
					else:
						red.sort(reverse=True,key=lambda x:x[1])
						st=red[0][1]
						yt=int(st/10)
						ytt=yt+1
						yt=yt*10
						ytt=ytt*10
						se=set()
						for i in range(0,siz):
							if(red[i][1]<ytt and red[i][1]>=yt):
								se.add(red[i][1])
						se=list(se)
						se.sort()
						leng=len(se)
						ue=int(leng/2)
						s=se[ue]
						l.append(s)
						u=[]
						for i in range(0,siz):
							if(red[i][1]<ytt and red[i][1]>=yt and red[i][1]>0):
								if(s>10):
									red[i][1]=red[i][1]-s
									u.append(red[i][0])
								else:
									while(red[i][1]>2):
										red[i][1]=red[i][1]-s
										u.append(red[i][0])      
						c=[]
						red.sort(key=lambda x:x[0])
						for i in bal:
							c.append(i[1])
						y.append(c)
						bal=[]
						d=[]
						for i in red:
							d.append(i[1])
							f=[]
							f.append(i[0])
							f.append(i[1])
							bal.append(f)
						t.append(d)
						u.sort()
						g.append(u)
				print(l)
				print(t)
				print(y)
				print(g)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
		sizes_cum_prod.sort()
		map_prod={}
		cl=color_model.objects.get(name=color)
		for i in kjh:
				for l in sizes_cum_prod:
						gfb=i.sizes.all().filter(color=cl,size_label=l).first()
						if (gfb in map_prod):
								map_prod[l]+=int(gfb.quantity*1.14)
						elif gfb:
								map_prod[l]=0
								map_prod[l]+=int(gfb.quantity*1.14)
						else:
								map_prod[l]=0
		print(map_prod)
		red=[]
		for l in sizes_cum_prod:
				f=[]
				f.append(l)
				f.append(map_prod[l])
				red.append(f)       
		l=[]
		t=[]
		y=[]
		g=[]
		getlay4(l,red,t,y,g)
		te=[]
		it=1
		for i in l:
				te.append(it)
				it=it+1
		u=zip(l,t,y,g,te)
		return render(request, 'vendor/lay_detail.html', {'data': u,'order':order,'sizes':sizes_cum_prod,'color':color})

def lay_detail_view5(request,order_no,color):
		order=company_Order.objects.get(order_no=order_no)
		print(color)
		def check5(bal):
				for i in bal:
						if(i[1]>2):
								return True
				return False
		def getlay5(l,red,t,y,g):
				siz=len(red)
				bal=[]
				for i in red:
						f=[]
						f.append(i[0])
						f.append(i[1])
						bal.append(f)
				while(check5(red)):
						j=0
						s=1
						u=[]
						se= set()
						for j in range(0,siz):
								if(red[j][1]>2):
										se.add(red[j][1])
						se = list(se)
						se.sort()
						leng=len(se)
						if(leng>1):
								if(leng%2==0):
										uee=int(leng/2)
										s=se[uee-1]
								else:
										uee=int(leng/2)
										s=se[uee]
								if s>=5:
										for i in range(0,siz):
												if(red[i][1]>=s):
														red[i][1]=red[i][1]-s
														u.append(red[i][0])
								else:
										for i in range(0,siz):
												if(red[i][1]>1):
														red[i][1]=red[i][1]-s
														u.append(red[i][0])
						else:
								st=se[0]
								if(st>5):
										s=int(st/4)
										stt=st/4
										if(stt-s>0.5):
												s=s+1
										for i in range(0,siz):
												if(red[i][1]==st):
														red[i][1]=red[i][1]-s*4
														u.append(red[i][0])
								else:
										if(st%2==0):
												s=int(st/2)
										else:
												s=st
										for i in range(0,siz):
												if(red[i][1]==st):
														red[i][1]=0
														u.append(red[i][0])
						l.append(s)
						c=[]
						red.sort(key=lambda x:x[0])
						for i in bal:
								c.append(i[1])
						y.append(c)
						bal=[]
						d=[]
						for i in red:
								d.append(i[1])
								f=[]
								f.append(i[0])
								f.append(i[1])
								bal.append(f)
						t.append(d)
						u.sort()
						g.append(u)
				print(l)
				print(t)
				print(y)
				print(g)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
		sizes_cum_prod.sort()
		map_prod={}
		cl=color_model.objects.get(name=color)
		for i in kjh:
				for l in sizes_cum_prod:
						gfb=i.sizes.all().filter(color=cl,size_label=l).first()
						if (gfb in map_prod):
								map_prod[l]+=int(gfb.quantity*1.14)
						elif gfb:
								map_prod[l]=0
								map_prod[l]+=int(gfb.quantity*1.14)
						else:
								map_prod[l]=0
		print(map_prod)
		red=[]
		for l in sizes_cum_prod:
				f=[]
				f.append(l)
				f.append(map_prod[l])
				red.append(f)       
		l=[]
		t=[]
		y=[]
		g=[]
		getlay5(l,red,t,y,g)
		te=[]
		it=1
		for i in l:
				te.append(it)
				it=it+1
		u=zip(l,t,y,g,te)
		return render(request, 'vendor/lay_detail.html', {'data': u,'order':order,'sizes':sizes_cum_prod,'color':color})

		
def lay_detail_view1(request,order_no,color):
		order=company_Order.objects.get(order_no=order_no)
		print(color)
		def check1(bal):
				for i in bal:
						if(i[1]!=0):
								return True
				return False
		def getlay1(l,red,t,y,g):
				siz=len(red)
				bal=[]
				for i in red:
						f=[]
						f.append(i[0])
						f.append(i[1])
						bal.append(f)
				while(check1(red)):
						red.sort(reverse=True,key=lambda x:x[1])
						s=0
						i=0
						u=[]
						for i in range(min(3,siz-1),-1,-1):
								if(red[i][1]!=0):
										s=red[i][1]
										break
						l.append(s)
						for j in range(0,i+1):
								u.append(red[j][0])
								red[j][1]=red[j][1]-s
						c=[]
						red.sort(key=lambda x:x[0])
						for i in bal:
								c.append(i[1])
						y.append(c)
						bal=[]
						d=[]
						for i in red:
								d.append(i[1])
								f=[]
								f.append(i[0])
								f.append(i[1])
								bal.append(f)
						t.append(d)
						u.sort()
						g.append(u)
				print(l)
				print(t)
				print(y)
				print(g)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
		sizes_cum_prod.sort()
		map_prod={}
		cl=color_model.objects.get(name=color)
		for i in kjh:
				for l in sizes_cum_prod:
						gfb=i.sizes.all().filter(color=cl,size_label=l).first()
						if (gfb in map_prod):
								map_prod[l]+=int(gfb.quantity*1.14)
						elif gfb:
								map_prod[l]=0
								map_prod[l]+=int(gfb.quantity*1.14)
						else:
								map_prod[l]=0
		print(map_prod)
		red=[]
		for l in sizes_cum_prod:
				f=[]
				f.append(l)
				f.append(map_prod[l])
				red.append(f)       
		l=[]
		t=[]
		y=[]
		g=[]
		getlay1(l,red,t,y,g)
		te=[]
		it=1
		for i in l:
				te.append(it)
				it=it+1
		u=zip(l,t,y,g,te)

		print(u)
		return render(request, 'vendor/lay_detail.html', {'data': u,'order':order,'sizes':sizes_cum_prod,'color':color})




def show_other_staff(request,email):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			obj=detail.objects.filter(email=email).first()
			orders=company_Order.objects.filter(staffs_Allocated=obj)
			acti=activities.objects.filter(user=obj)
			li=[]
			for o in orders:
				li.append(activities.objects.filter(user=obj,order=o))
			data={
			"data":obj,
			"head":False,
			"manager":False,
			"staff":False,
			"acti":li,
			"current":datetime.datetime.now().date,
			}
			if details.position=='H':
				data["head"]=True
			elif details.position=='M':
				data["manager"]=True
			elif details.position=='C':
				data["staff"]=True
			if request.POST:
				if request.POST.get("activate")=="on":
					obj.activate_Staff=True
				obj.save()
				return redirect('/userdetail/staff_profile')
			return render(request,'userdetail/staff_other_staff.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')






def staff_profile_manager(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff and details.activate_Staff:
			obj=detail.objects.filter(
				staff=True,
				position='M',
				staff_category=details.staff_category
				)
			data={
			"obj":obj
			}
			return render(request,'userdetail/staff_profile_manager.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



from b2b.models import priority_of_order,macro_Activities,custom_assortment_model
from permission.models import section,orders_permission
from product.models import standard_fabric_blend,washcare_model
from Garmenting_Vendor.models import kpi,kpi_data,kpi_data_order

from b2b.models import size_assortment_1
def staff_profile_orders(request,order_no=None,*args,**kwargs):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True

			ogh.save()
	if request.user.is_authenticated:
		print('POST DICT: {}'.format(request.POST)) #CURRWORK
		details=detail.objects.filter(email=request.user.email).first()
		# print(f'STAFF: {details.staff} VENDOR: {details.vendor}')
		if details.staff or details.vendor:
			# print('LOGGING IN')
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if details.vendor:
				orders=company_Order.objects.filter(order_no=order_no)
			if orders.count()>0:
				print('ORDERS EXISTING')
				ohj=quantity_b2b.objects.filter(order=orders.first(),production=False,is_csv=False)
				csv_ohj=quantity_b2b.objects.filter(order=orders.first(),production=False,is_csv=True)
				cum_ohj=quantity_b2b.objects.filter(order=orders.first(),production=False)
				order=orders.first()

				order_bool=False
				enquiry_bool=False
				sample_bool=False
				design_bool=False
				size_bool=False
				head=False
				manager=False
				staff=True
				if order.order_type=='O':
					order_bool=True
				elif order.order_type=='E':
					enquiry_bool=True
				elif order.order_type=='S':
					sample_bool=True
				else:
					design_bool=True
				if ohj.count()>0:
					size_bool=True
				ghj=None
				cum=None
				merch=None
				merch_alloted=None
				garment=None
				garment_alloted=None
				if details.position=='H':
					head=True
					cum=order.staffs_Allocated.filter(position='M',staff=True,staff_category=details.staff_category).first()
					ghj=detail.objects.filter(position='M',staff=True,staff_category=details.staff_category)
					merch=staff_Categories.objects.filter(name="Merchandising").first()
					merch=detail.objects.filter(position='H',staff=True,staff_category=merch)
					merch_alloted=staff_Categories.objects.filter(name="Merchandising").first()
					merch_alloted=order.staffs_Allocated.filter(position='H',staff=True,staff_category=merch_alloted).first()
				elif details.position=='M':
					manager=True
					cum=order.staffs_Allocated.filter(position='C',staff=True,staff_category=details.staff_category).first()
					ghj=detail.objects.filter(position='C',staff=True,staff_category=details.staff_category)
				ghi=staff_Categories.objects.filter(name="Merchandising").first()
				if details.staff_category==ghi and details.position=='H':
					ghi=seller_Categories.objects.filter(name="Garmenting Vendor").first()
					garment_alloted=order.staffs_Allocated.filter(vendor=True,seller_category=ghi).first()
					garment=detail.objects.filter(seller_category=ghi,vendor=True)

				sta1=company_Order.objects.filter(order_no=order.order_no).first()
				li=[]

				# for o in sta1.staffs_Allocated.all():
				# 	xfg=activities.objects.filter(user=o,order=order)
				# 	if xfg.count()>0:
				# 		li.append(xfg)
				li=activities.objects.filter(order=order).order_by('activity_Cate')
				# li=macro_Activities.objects.all()
				kjh=production_order.objects.filter(order=order,is_csv=False).order_by('production_no')
				csv_kjh = production_order.objects.filter(order=order, is_csv=True).order_by('production_no')
				packing_kjh = packing_list_1.objects.filter(order=order).order_by('list_no')

				prod=[]
				csv_prod=[]
				packing_prod=[]
				sizes_cum_prod=[]
				packing_sizes_cum_prod=[]
				colors_cum_prod=[]
				packing_colors_cum_prod=[]
				address_cum_prod=[]
				packing_address_cum_prod=[]
				for i in kjh:
					for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
							sizes_cum_prod.append(j.size_label)
						if not(j.color in colors_cum_prod):
							colors_cum_prod.append(j.color)
						if not(j.address in address_cum_prod):
							address_cum_prod.append(j.address)
				for i in csv_kjh:
					for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
							sizes_cum_prod.append(j.size_label)
						if not(j.color in colors_cum_prod):
							colors_cum_prod.append(j.color)
						if not(j.address in address_cum_prod):
							address_cum_prod.append(j.address)

				for i in packing_kjh:
					for j in i.sizes.all():
						if not(j.size_label in packing_sizes_cum_prod) and j.size_label:
							packing_sizes_cum_prod.append(j.size_label)
						if not(j.color in colors_cum_prod):
							packing_colors_cum_prod.append(j.color)
						if not(j.address in address_cum_prod):
							packing_address_cum_prod.append(j.address)
				sizes_cum_prod.sort()
				packing_sizes_cum_prod.sort()
				map_prod={}
				manual_cum_map_prod={}
				csv_cum_map_prod={}
				csv_map_prod={}
				packing_map_prod={}

				for i in kjh:
					for j in colors_cum_prod:
						for k in address_cum_prod:
							for l in sizes_cum_prod:

								gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
								if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
								elif gfb:
									map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
									for m in sizes_cum_prod:
										map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity

				for i in kjh:
					for j in colors_cum_prod:
						for k in address_cum_prod:
							for l in sizes_cum_prod:

								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=False).first()
								if ((str(j.id)+"_"+str(k.id)) in manual_cum_map_prod) and gfb:
									manual_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
								elif gfb:
									manual_cum_map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
									for m in sizes_cum_prod:
										manual_cum_map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
									manual_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
				tot_horiz=[]
				total=0
				for key in manual_cum_map_prod:
					manual_cum_map_prod[key].append(sum(manual_cum_map_prod[key][1]))
					total+=manual_cum_map_prod[key][2]
				for i in range(len(sizes_cum_prod)):
					sum_each=0
					for key in manual_cum_map_prod:
						sum_each+=manual_cum_map_prod[key][1][i]
					tot_horiz.append(sum_each)
				tot_horiz.append(total)


				for i in csv_kjh:
					for j in colors_cum_prod:
						for k in address_cum_prod:
							for l in sizes_cum_prod:

								gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
								if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
								elif gfb:
									map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
									for m in sizes_cum_prod:
										map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
									map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity

				total_mc=[]
				total=0
				for key in map_prod:
					map_prod[key].append(sum(map_prod[key][1]))
					total+=map_prod[key][2]
				for i in range(len(sizes_cum_prod)):
					sum_each=0
					for key in map_prod:
						sum_each+=map_prod[key][1][i]
					total_mc.append(sum_each)
				total_mc.append(total)

				for i in csv_kjh:
					for j in colors_cum_prod:
						for k in address_cum_prod:
							for l in sizes_cum_prod:

								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=True).first()
								if ((str(j.id)+"_"+str(k.id)) in csv_cum_map_prod) and gfb:
									csv_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
								elif gfb:
									csv_cum_map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
									for m in sizes_cum_prod:
										csv_cum_map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
									csv_cum_map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
				
				tot_horizo=[]
				total=0
				for key in csv_cum_map_prod:
					csv_cum_map_prod[key].append(sum(csv_cum_map_prod[key][1]))
					total+=csv_cum_map_prod[key][2]
				for i in range(len(sizes_cum_prod)):
					sum_each=0
					for key in csv_cum_map_prod:
						sum_each+=csv_cum_map_prod[key][1][i]
					tot_horizo.append(sum_each)
				tot_horizo.append(total)
				
				for i in packing_kjh:
					for j in packing_colors_cum_prod:
						for k in packing_address_cum_prod:
							for l in packing_sizes_cum_prod:

								gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
								if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
									map_prod[(str(j.id)+"_"+str(k.id))][1][packing_sizes_cum_prod.index(l)]+=gfb.quantity
								elif gfb:
									map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
									for m in sizes_cum_prod:
										map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
									map_prod[(str(j.id)+"_"+str(k.id))][1][packing_sizes_cum_prod.index(l)]+=gfb.quantity


				# print(map_prod,sizes_cum_prod)
				for i in kjh:
					prod.append([i])
					sikl=[]
					for j in i.sizes.all():
						if not(j.size_label in sikl):
							sikl.append(j.size_label)
					sikl.sort()
					# print("\n\n\n\n",sikl)
					prod[-1].append(sikl)
					coli=[]
					addi=[]
					for j in i.sizes.all():
						if not(j.color in coli):
							coli.append(j.color)
						if not(j.address in addi):
							addi.append(j.address)
					tot_sikl=[0 for klj in range(len(sikl))]
					kjh568=[]
					# print(sikl)
					for j in coli:
						for k in addi:
							treh=[]
							check=False
							for l in sikl:
								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=False)
								if gfb.first():
									check=True
									treh.append(gfb.first().quantity)
									tot_sikl[sikl.index(l)]+=gfb.first().quantity
								else:
									treh.append(0)
							if check:
								kjh568.append([j,k,treh,sum(treh)])
					prod[-1].append(kjh568)
					prod[-1].append(tot_sikl)
					prod[-1].append(sum(tot_sikl))


				for i in csv_kjh:
					csv_prod.append([i])
					sikl=[]
					for j in i.sizes.all():
						if not(j.size_label in sikl):
							sikl.append(j.size_label)
					sikl.sort()
					# print("\n\n\n\n",sikl)
					csv_prod[-1].append(sikl)
					coli=[]
					addi=[]
					for j in i.sizes.all():
						if not(j.color in coli):
							coli.append(j.color)
						if not(j.address in addi):
							addi.append(j.address)
					tot_sikl=[0 for klj in range(len(sikl))]
					kjh568=[]
					# print(sikl)
					for j in coli:
						for k in addi:
							treh=[]
							check=False
							for l in sikl:
								gfb=i.sizes.all().filter(color=j,address=k,size_label=l,is_csv=True)
								if gfb.first():
									check=True
									treh.append(gfb.first().quantity)
									tot_sikl[sikl.index(l)]+=gfb.first().quantity
								else:
									treh.append(0)
							if check:
								kjh568.append([j,k,treh,sum(treh)])
					csv_prod[-1].append(kjh568)
					csv_prod[-1].append(tot_sikl)
					csv_prod[-1].append(sum(tot_sikl))

				for i in packing_kjh:
					packing_prod.append([i])
					sikl=[]
					for j in i.sizes.all():
						if not(j.size_label in sikl):
							sikl.append(j.size_label)
					sikl.sort()
					# print("\n\n\n\n",sikl)
					packing_prod[-1].append(sikl)
					coli=[]
					addi=[]
					for j in i.sizes.all():
						if not(j.color in coli):
							coli.append(j.color)
						if not(j.address in addi):
							addi.append(j.address)
					tot_sikl=[0 for klj in range(len(sikl))]
					kjh568=[]
					# print(sikl)
					for j in coli:
						for k in addi:
							treh=[]
							check=False
							for l in sikl:
								gfb=i.sizes.all().filter(color=j,address=k,size_label=l)
								if gfb.first():
									check=True
									treh.append(gfb.first().quantity)
									tot_sikl[sikl.index(l)]+=gfb.first().quantity
								else:
									treh.append(0)
							if check:
								kjh568.append([j,k,treh])
					packing_prod[-1].append(kjh568)
					packing_prod[-1].append(tot_sikl)
					#print(prod)



				color_av=order.colors_avail.all()
				li5=[]
				csv_li5=[]
				cum_li5=[]
				li1=[]
				csv_li1=[]
				cum_li1=[]
				li55=[]
				color_av=quantity_b2b.objects.filter(order=order)
				some_map_loc=[]
				for hgy in color_av:
					li21=[hgy.color,hgy.address]
					if li21 not in some_map_loc:
						some_map_loc.append(li21)
				# print(some_map_loc)
				for i in ohj:
					if i.size_label not in li1:
						li1.append(i.size_label)
				li1.sort()
				for i in csv_ohj:
					if i.size_label not in csv_li1:
						csv_li1.append(i.size_label)
				csv_li1.sort()
				for i in cum_ohj:
					if i.size_label not in cum_li1:
						cum_li1.append(i.size_label)
				cum_li1.sort()
				for c in some_map_loc:
					# oyu=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1])
					# for k in oyu:
					li2={"color":None,"size":None,"total":None}
					csv_li2={"color":None,"size":None,"total":None}
					cum_li2={"color":None,"size":None,"total":None}
					li3=[]
					csv_li3=[]
					cum_li3=[]
					some_obj=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1],production=False,is_csv=False)
					csv_some_obj = quantity_b2b.objects.filter(order=order, color=c[0], address=c[1], production=False,
														   is_csv=True)
					cum_some_obj=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1],production=False)
					li2["color"]=some_obj.first()
					csv_li2["color"]=csv_some_obj.first()
					cum_li2["color"]=cum_some_obj.first()
					total=0
					for j in li1:
						quan_inst=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1],production=False,size_label=j,is_csv=False).first()
						if quan_inst:
							li3.append({"quantity":quan_inst.quantity,"size":j})
						else:
							li3.append({"quantity":0,"size":j})
						total=total+li3[-1]["quantity"]
					li2["size"]=li3
					li2["total"]=total
					# print(li2)
					li5.append(li2)
					total = 0
					for j in csv_li1:
						quan_inst = quantity_b2b.objects.filter(order=order, color=c[0], address=c[1], production=False,
																size_label=j,is_csv=True).first()
						if quan_inst:
							csv_li3.append({"quantity": quan_inst.quantity, "size": j})
						else:
							csv_li3.append({"quantity": 0, "size": j})
						total = total + csv_li3[-1]["quantity"]
					csv_li2["size"] = csv_li3
					csv_li2["total"] = total
					# print(li2)
					csv_li5.append(csv_li2)

					total = 0
					for j in cum_li1:
						quan_inst = quantity_b2b.objects.filter(order=order, color=c[0], address=c[1], production=False,
																size_label=j).first()
						if quan_inst:
							cum_li3.append({"quantity": quan_inst.quantity, "size": j})
						else:
							cum_li3.append({"quantity": 0, "size": j})
						total = total + cum_li3[-1]["quantity"]
					cum_li2["size"] = cum_li3
					cum_li2["total"] = total
					# print(li2)
					cum_li5.append(cum_li2)
				# for c in color_av:
				# 	oyu=quantity_b2b.objects.filter(order=order,color=c)
				# 	for k in oyu:
				# 		li2={"color":None,"size":None,"total":None}
				# 		li3=[]
				# 		some_obj=quantity_b2b.objects.filter(order=order,color=k.color,address=k.address)
				# 		li2["color"]=k
				# 		total=0
				# 		for j in some_obj:
				# 			li3.append(j)
				# 			total=total+j.quantity
				# 		li2["size"]=li3
				# 		li2["total"]=total
				# 		print(li2)
				# 		li.append(li2)
				li4=[]
				csv_li4=[]
				cum_li4=[]
				total_overall=0
				for j in li1:
					objs=quantity_b2b.objects.filter(order=order,size_label=j,production=False,is_csv=False)
					total=0
					for k in objs:
						total=total+k.quantity
					total_overall=total_overall+total
					li4.append(total)
				li4.append(total_overall)
				total_overall = 0
				for j in csv_li1:
					objs=quantity_b2b.objects.filter(order=order,size_label=j,production=False,is_csv=True)
					total=0
					for k in objs:
						total=total+k.quantity
					total_overall=total_overall+total
					csv_li4.append(total)
				csv_li4.append(total_overall)
				total_overall = 0
				for j in cum_li1:
					objs=quantity_b2b.objects.filter(order=order,size_label=j)
					total=0
					for k in objs:
						total=total+k.quantity
					total_overall=total_overall+total
					cum_li4.append(total)
				cum_li4.append(total_overall)
				if request.GET.get('filter'):
					filter_by=request.GET.get('filter')
					if filter_by=="com":
						li=activities.objects.filter(order=order).exclude(actual_date=None)
					if filter_by=="tod":
						today=datetime.datetime.today()
						li=activities.objects.filter(
							order=order,
							planned_date__year=today.year,
							planned_date__month=today.month,
							planned_date__day=today.day)
					if filter_by=="sal":
						sal58=staff_Categories.objects.filter(name="Sales").first()
						act=activities_Category.objects.filter(staff_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="merch":
						sal58=staff_Categories.objects.filter(name="Merchandising").first()
						act=activities_Category.objects.filter(staff_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="gar":
						sal58=seller_Categories.objects.filter(name="Garmenting Vendor").first()
						act=activities_Category.objects.filter(seller_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="fab":
						sal58=seller_Categories.objects.filter(name="Fabric Vendor").first()
						act=activities_Category.objects.filter(seller_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="sew":
						sal58=seller_Categories.objects.filter(name="Sewing Trims Vendor").first()
						act=activities_Category.objects.filter(seller_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="fin":
						sal58=seller_Categories.objects.filter(name="Finishing Trims Vendor").first()
						act=activities_Category.objects.filter(seller_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="pack":
						sal58=seller_Categories.objects.filter(name="Packing Trims Vendor").first()
						act=activities_Category.objects.filter(seller_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="log":
						sal58=seller_Categories.objects.filter(name="Logistic Vendor").first()
						act=activities_Category.objects.filter(seller_category=sal58)
						li=activities.objects.filter(order=order,activity_Cate__in=act).order_by('activity_Cate')
					if filter_by=="all":
						pass
				alteration=assortment.objects.filter(~Q(alteration_cost=0),order_no=order)
				size_attri=POM.objects.filter(product_Category=order.product_Category,
					product_Supercategory=order.product_Supercategory,
					product_Subcategory=order.product_Subcategory)
				# print(alteration)
				forms=custom_Form.objects.filter(staff_category=details.staff_category)
				is_merch=False
				merch_obj=staff_Categories.objects.filter(name="Merchandising").first()
				# print(merch_obj)
				if details.staff_category==merch_obj:
					is_merch=True
					print(is_merch)
				is_sales=False
				sales_obj=staff_Categories.objects.filter(name="Sales").first()
				if details.staff_category==sales_obj:
					is_sales=True
				obj_priority=priority_of_order.objects.filter(user=details,order=order).first()
				if not(obj_priority):
					obj_priority_no=0
				else:
					obj_priority_no=obj_priority.priority_no
				cnt_per=None
				if details.staff_category==staff_Categories.objects.get(name="Sales"):
					cnt_per=detail.objects.filter(email=order.user_email).first()
				elif details.staff_category==staff_Categories.objects.get(name="Merchandising"):
					oij=staff_Categories.objects.filter(name="Sales").first()
					cnt_per=order.staffs_Allocated.filter(staff=True,position='H',staff_category=oij).first()
				boms_obj=bom.objects.filter(order=order).first()
				customer=detail.objects.filter(email=order.user_email).first()
				measu=None
				if order.fashion_Brand and order.label and order.fit and order.season:
					measu=measurement.objects.filter(
							user=order.fashion_Brand,
							label=order.label,
							fit=order.fit,
							season=order.season,
							product_Category=order.product_Category,
							product_Subcategory=order.product_Subcategory,
							product_Supercategory=order.product_Supercategory
						).first()
					if measu:
						measu = measu.slug
				is_quality=False
				objuyu=staff_Categories.objects.filter(name="Quality").first()
				if details.staff_category==objuyu:
					is_quality=True
				# macro_acti=macro_Activities.objects.all()
				asd=activities.objects.filter(order=order).order_by('activity_Cate')
				macro_acti=[]
				random_acti=[]
				for i in asd:
					objs458=macro_Activities.objects.filter(activities=i.activity_Cate)
					for j in objs458:
						first=i.planned_date
						if i.custom_date:
							first=i.custom_date
						diff=0
						if i.actual_date:
							diff=i.actual_date-first
							diff=diff.days
						if j not in random_acti:
							random_acti.append(j)
							macro_acti.append([j,[[i,diff]]])
						else:
							indi=random_acti.index(j)
							macro_acti[indi][1].append([i,diff])
				# print(macro_acti)
				macro_acti=sorted(macro_acti,key=lambda x:x[0].id)
				fab_obj=seller_Categories.objects.filter(name='Fabric Vendor').first()
				fab_obj=detail.objects.filter(vendor=True,seller_category=fab_obj)
				log_obj=seller_Categories.objects.filter(name='Logistic Vendor').first()
				log_obj=detail.objects.filter(vendor=True,seller_category=log_obj)
				pack_obj=seller_Categories.objects.filter(name='Packing Trims Vendor').first()
				pack_obj=detail.objects.filter(vendor=True,seller_category=pack_obj)
				fin_obj=seller_Categories.objects.filter(name='Finishing Trims Vendor').first()
				fin_obj=detail.objects.filter(vendor=True,seller_category=fin_obj)
				sew_obj=seller_Categories.objects.filter(name='Sewing Trims Vendor').first()
				sew_obj=detail.objects.filter(vendor=True,seller_category=sew_obj)
				logi_vendor=seller_Categories.objects.filter(name="Logistic Vendor").first()
				logi_vendors=detail.objects.filter(vendor=True,seller_category=logi_vendor)
				last_date=activities.objects.filter(order=order).order_by('-planned_date').first()
				# print(details.staff_category)
				order_section=orders_permission.objects.filter(staff_category=details.staff_category).first()
				if order_section:
					order_section=order_section.allowed_section.all().filter(order_section=True)
				else:
					order_section=['Order_Description']
				garvendor=order.get_garment_vendor
				final_kpi_data=[]
				for i in kpi.objects.all():
					obj_kpi=kpi_data_order.objects.filter(by_user=details,to_user=garvendor,order=order,
						kpi_val=i).first()
					if obj_kpi:
						obj_kpi=obj_kpi.rating
					else:
						obj_kpi=0
					final_kpi_data.append([i,obj_kpi])
				# print(final_kpi_data)

				if request.GET.get('custom_assortment'):
					order.custom_assortment=not(order.custom_assortment)
					order.save()
				filefrm = FileForm()
				csv_product= items.objects.all()
				sizes_opt=quantity_b2b.objects.filter(order=order)
				sz_ass_obj=size_assortment_1.objects.all()

				objjj=[]
				for entry in sz_ass_obj:
					overall_total_quantity = 0
					addresses=[]
					colors=[]
					size_wise_sum=[]

					sizes=[]
					for e in entry.sizes.all():
						if(e.address not in addresses):
							addresses.append(e.address)
						if(e.color not in colors):
							colors.append(e.color)
						if(e.size_label not in sizes):
							sizes.append(e.size_label)
						sizes.sort()

					for size in sizes:
						qua=0
						e=entry.sizes.all().filter(size_label=size)
						for i in e:
							qua+=i.quantity
						size_wise_sum.append(qua)
					all_rows=[]
					for color in colors:
						for address in addresses:
							quan=0
							for size in sizes:
								z=entry.sizes.all().filter(color=color,address=address,size_label=size)
								print(z)
								if(z.first()):
									quan+=z.first().quantity
							if(quan==0):
								break
							else:
								ls=[]
								for size in sizes:
									z = entry.sizes.all().filter(color=color, address=address, size_label=size)
									if(z.first()):
										ls.append(z.first().quantity)
									else:
										ls.append('-')
									#print(ls)

								overall_total_quantity += quan
								all_rows.append([color,address,ls,quan])
								print(all_rows)

					objjj.append([entry,sizes,all_rows,size_wise_sum,overall_total_quantity])

				print(objjj)

				size_lst=[]
				new_manual_size_lst=[{"name":i,"select":str(i) in order.allowed_sizes } for i in order.get_sizes]
				c=[]
				for e in new_manual_size_lst:
					if e['select']==True:
						c.append(e['name'])
				for e in sizes_opt:
					if e.size_label not in size_lst:
						size_lst.append(e.size_label)
				size_lst.sort()
				print('sg')
				szs=[]
				a=size_assortment_1.objects.all()
				for i in a:
					szs.append(i.assortment_no)
				szs.sort()
				orders=company_Order.objects.all().filter(order_no=order_no).values('plus_Quantity_Percentage','minus_Quantity_Percentage','sample_quantity')
				if orders[0]['sample_quantity']==None:
					sample=0
				else:
					sample=orders[0]['sample_quantity']
				print ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
				print (orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage']+sample)
				data={
					"add_percentage":(orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage']+sample),
					"accepted":orders[0]['plus_Quantity_Percentage'],
					"rejected":orders[0]['minus_Quantity_Percentage'],
					"stock":sample,
					"sizes_cum_prod":sizes_cum_prod,
					'products':csv_product,
					'sizes_lst':size_lst,
					'new_manual_sizes_lst':c,
					'manual_assortment_table':objjj,
					"tot_horiz":tot_horiz,
					"tot_horizo":tot_horizo,
					"total_mc":total_mc,
					"custom_assorts":custom_assortment_model.objects.filter(order=order),
					"map_prod":map_prod,
					"final_kpi_data":final_kpi_data,
					"fab_obj":fab_obj,
					"log_obj":log_obj,
					"fin_obj":fin_obj,
					"pack_obj":pack_obj,
					"sew_obj":sew_obj,
					"order_no":order_no,
					"order":order,
					"quan":ohj,
					"last_date":last_date,
					"enquiry_bool":enquiry_bool,
					"order_bool":order_bool,
					"sample_bool":sample_bool,
					"design_bool":design_bool,
					"size_bool":size_bool,
					"head":head,
					"manager":manager,
					"staff":staff,
					"obj":ghj,
					"cum":cum,
					"merch":merch,
					"merch_alloted":merch_alloted,
					"garment":garment,
					"garment_alloted":garment_alloted,
					"acti":li,
					"current":datetime.datetime.now().date,
					"prd":kjh,
					"quan_by_clr":li5,
					"csv_quan_by_clr":csv_li5,
					"cum_quan_by_clr":cum_li5,
					"size_by_quan":li1,
					"csv_size_by_quan": csv_li1,
					"cum_size_by_quan": cum_li1,
					"quan_by_sz":li4,
					"csv_quan_by_sz": csv_li4,
					"cum_quan_by_sz": cum_li4,
					"alteration":alteration,
					"size_attri":size_attri,
					"forms":forms,
					"is_merch":is_merch,
					"is_sales":is_sales,
					"obj_priority":obj_priority_no,
					"cnt":cnt_per,
					"boms_obj":boms_obj,
					"customer":customer,
					"measu":measu,
					"manual_size_ass_numbers":szs,
					"is_quality":is_quality,
					"macro_acti":macro_acti,
					"logi_vendors":logi_vendors,
					"details":details,
					"manual_cum_map_prod":manual_cum_map_prod,
					"csv_cum_map_prod":csv_cum_map_prod,
					"prod789":prod,
					"csv_prod789":csv_prod,
					"packing_prod789":packing_prod,
					"order_section":order_section,
					"fabric_blends":standard_fabric_blend.objects.filter(standard=True),
					"sizes_allowed":[{"name":i,"select":str(i) in order.allowed_sizes } for i in order.get_sizes],
					"alteration_assort":assortment.objects.filter(alteration_bool=True,order_no=order),
					"fileform": filefrm,
				}
				
				if request.GET.get('approve'):
					cust_obj=custom_assortment_model.objects.filter(id=int(request.GET.get('approve'))).first()
					if cust_obj:
						if cust_obj.approve:
							cust_obj.approve=False
							quants=quantity_b2b.objects.filter(order=order,size_label=cust_obj.size,color__name=cust_obj.color).first()
							if quants and quants.quantity:
								quants.quantity-=1
								quants.save()
						else:
							cust_obj.approve=True
							quants=quantity_b2b.objects.filter(order=order,size_label=cust_obj.size,color__name=cust_obj.color).first()
							if not(quants):
								col=color_model(name=cust_obj.color)
								col.save()
								quants=quantity_b2b(order=order,size_label=cust_obj.size,color=col,quantity=0)
							quants.quantity+=1
							quants.save()
						cust_obj.save()
					# print(cust_obj.approve,"khj")
				if request.POST.get('kpi'):
					for i in kpi.objects.all():
						print(i)
						if request.POST.get('kpi_'+str(i.id)):
							new_kpi=kpi_data_order.objects.filter(by_user=details,to_user=garvendor,order=order,
								kpi_val=i).first()
							if new_kpi:
								new_kpi.rating=request.POST.get('kpi_'+str(i.id))
								new_kpi.save()
							else:
								new_kpi=kpi_data_order(by_user=details,to_user=garvendor,order=order,
									kpi_val=i,rating=request.POST.get('kpi_'+str(i.id)))
								new_kpi.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('fabric_blend_select_ajax'):
					obj=standard_fabric_blend.objects.filter(id=int(request.POST.get('fabric_blend_select_ajax'))).first()
					washcare=washcare_model.objects.filter(blend=obj,product_Category=order.product_Category,
						product_Subcategory=order.product_Subcategory,product_Supercategory=order.product_Supercategory).first()
					data={}
					if washcare:
						data={
							"washcare":washcare
						}
						return render_to_response(request,"seller_info/washcare_detail_view.html",data)
					return JsonResponse({})
				if request.POST.get('fabric_blend_input'):
					obj=standard_fabric_blend.objects.filter(id=int(request.POST.get('fabric_blend_input'))).first()
					if obj:
						order.fabric_blend=obj
						washcare=washcare_model.objects.filter(blend=obj,product_Category=order.product_Category,
						product_Subcategory=order.product_Subcategory,product_Supercategory=order.product_Supercategory).first()
						if washcare:
							order.washcare_obj=washcare
						order.save()
				if request.POST.get('staff_to_logistics'):
					staff_to=detail.objects.filter(email=request.POST.get("staff_to_logistics")).first()
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Add Staff to it("+str(order_no)+") !",
						description="Add Staff to it",
						user=objs1,
						link="/userdetail/staff_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						position='M',type_of_order=order.order_type,staff_category=details.staff_category)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('perm_assortment'):
					assortment_custom=request.POST.get('assortment_custom')
					assortment_size_set=request.POST.get('assortment_size_set')
					assortment_brand=request.POST.get('assortment_brand')
					assortment_per_customer=request.POST.get('assortment_per_customer')
					show_pom_in_assortment=request.POST.get('show_pom_in_assortment')
					sizes=request.POST.getlist('sizes_allowed')
					final=''
					for i in sizes:
						final+=i+','
					order.allowed_sizes=final
					order.save()
					print(order.allowed_sizes)
					# print(assortment_size_set)
					if assortment_custom:
						order.assortment_custom=True
					else:
						order.assortment_custom=False
					if assortment_size_set:
						order.assortment_size_set=True
					else:
						order.assortment_size_set=False
					if assortment_brand:
						order.assortment_brand=True
					else:
						order.assortment_brand=False
					if assortment_per_customer:
						order.assortment_per_customer=True
					else:
						order.assortment_per_customer=False
					if show_pom_in_assortment:
						order.show_pom_in_assortment=True
					else:
						order.show_pom_in_assortment=False
					order.save()
				if request.POST.get('color_ajax') and request.POST.get('address_cate_ajax'):
					color_ajax=request.POST.get('color_ajax')
					address_cate_ajax=request.POST.get('address_cate_ajax')
					size_label_ajax=request.POST.get('size_label_ajax')
					quantity_matter=request.POST.get('quantity_matter')
					color_obj=color_model.objects.filter(name=color_ajax).first()
					address_obj=address_model.objects.filter(id=int(address_cate_ajax)).first()
					obstruct_obj=quantity_b2b.objects.filter(
						color=color_obj,
						address=address_obj,
						size_label=int(size_label_ajax),
						order=order
					).first()
					obstruct_obj.quantity=int(quantity_matter)
					obstruct_obj.save()
					return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
				if request.POST.get('size_assort'):
					size_assort=int(request.POST.get('size_assort'))
					address=int(request.POST.get('address'))
					address=address_model.objects.filter(id=address).first()
					color=int(request.POST.get('color'))
					color=color_model.objects.filter(id=color).first()
					quantity=int(request.POST.get('quantity'))
					objs_size_assort=quantity_b2b.objects.filter(order=order,
						size_label=size_assort,
						color=color,
						address=address,
						production=False,
						is_csv=False)

					s=request.POST.get("where")
					if(s=="Old"):
						no=int(request.POST.get("list_no"))
						size_ass_obj=size_assortment_1.objects.filter(order=order,assortment_no=no).first()
						print(size_ass_obj)
						if(size_ass_obj):
							a=size_ass_obj.sizes.filter(size_label=size_assort,color=color,address=address,production=False,is_csv=False)
							if a.first():
								u=a.first()
								u.quantity+=quantity
								u.save()
								print(u.quantity)
							else:
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=size_assort,
									address=address,
									color=color,
									quantity=quantity,
									production=False,
									is_csv=False
								)
								objs_size_assort.save()
								size_ass_obj.sizes.add(objs_size_assort)
								size_ass_obj.save()

						else:
							return HttpResponse("No such table found ... make a valid choice")
					elif(s=="New"):
						final=1
						size_ass_obj=size_assortment_1.objects.filter(order=order).order_by("-assortment_no")
						objs_size_assort = quantity_b2b(
							order=order,
							size_label=size_assort,
							address=address,
							color=color,
							quantity=quantity,
							production=False,
							is_csv=False
						)
						objs_size_assort.save()
						if(size_ass_obj.first()):
							final=size_ass_obj.first().assortment_no + 1
						d=size_assortment_1(order=order,assortment_no=final,is_csv=False)
						d.save()
						d.sizes.add(objs_size_assort)
						d.save()



					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))

				if request.POST.get('star_click_ajax'):
					star=int(request.POST.get('star_click_ajax'))
					if not(obj_priority):
						obj_priority=priority_of_order(
							user=details,
							order=order
							)
					else:
						order.priority_no=order.priority_no-obj_priority.priority_no
						order.priority_quantity=order.priority_quantity-1
					obj_priority.priority_no=star
					obj_priority.save()
					order.priority_no=order.priority_no+star
					order.priority_quantity=order.priority_quantity+1
					order.overall_priority=round(order.priority_no/order.priority_quantity,2)
					order.save()
					return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
				if request.POST.get('head_to_manager'):
					staff_to=request.POST.get('head_to_manager')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Add Staff to it("+str(order_no)+") !",
						description="Add Staff to it",
						user=objs1,
						link="/userdetail/staff_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						position='M',type_of_order=order.order_type,staff_category=details.staff_category)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('manager_to_staff'):
					staff_to=request.POST.get('manager_to_staff')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Add Price to it("+str(order_no)+") !",
						description="Add Price to it",
						user=objs1,
						link="/userdetail/staff_profile/orders/"+str(order_no),type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()

					acti_cate=activities_Category.objects.filter(
						position='C',type_of_order=order.order_type,staff_category=details.staff_category)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('total_Price'):
					total_Price=request.POST.get('total_Price')
					if total_Price:
						order.total_Price=int(total_Price)
					alt_charge=request.POST.get('alt_charge')
					if alt_charge:
						order.alteration_Charge=int(alt_charge)
					custom_charge=request.POST.get('custom_charge')
					if custom_charge:
						order.custom_Charges=int(custom_charge)
					target_lead=request.POST.get('target_lead')
					if target_lead:
						order.target_lead_time=int(target_lead)
					target_price=request.POST.get('target_price')
					if target_price:
						order.target_price=int(target_price)
					tech_pack=request.FILES.get('tech_pack')
					if tech_pack:
						order.tech_pack=tech_pack
					specs=request.FILES.get('specs')
					if specs:
						order.specs=specs
					logo=request.FILES.get('logo')
					if logo:
						order.custom_logo=logo
					logo_placement=request.POST.get('logo_placement')
					if logo_placement:
						order.logo_placement=logo_placement
					quan_plus=request.POST.get('quan_plus')
					if quan_plus:
						order.plus_Quantity_Percentage=int(quan_plus)
					quan_negative=request.POST.get('quan_negative')
					if quan_negative:
						order.minus_Quantity_Percentage=quan_negative
					status_ord=request.POST.get('status')
					if status_ord:
						order.status=status_ord
					mode_ord=request.POST.get('mode')
					if mode_ord:
						order.mode=mode_ord
					route_ord=request.POST.get('route')
					if route_ord:
						order.route=route_ord
					order.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('head_to_merch'):
					staff_to=request.POST.get('head_to_merch')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Allocated to you !("+str(order_no)+") !",
						description="Allocate Manager to it",
						user=objs1,
						link="/userdetail/staff_profile/orders/"+str(order_no),type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					merch1=staff_Categories.objects.filter(name="Merchandising").first()
					acti_cate=activities_Category.objects.filter(
						position='H',type_of_order=order.order_type,staff_category=merch1)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					sales_other=staff_Categories.objects.filter(name="Sales").first()
					merch_other=staff_Categories.objects.filter(name="Merchandising").first()
					staffs_other=detail.objects.filter(staff=True).exclude(staff_category=sales_other).exclude(staff_category=merch_other)
					# staffs_other=
					for i in staffs_other:
						order.staffs_Allocated.add(i)
						order.save()
						objs1=i
						noti_oj=notifications(
							title="New Order Allocated to you !("+str(order_no)+") !",
							description="Allocate Manager to it",
							user=objs1,
							link="/userdetail/staff_profile/orders/"+str(order_no),type_of_order=order.order_type)
						noti_oj.save()
						noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
						noti_oj.save()
						merch1=staff_Categories.objects.filter(name="Merchandising").first()
						acti_cate=activities_Category.objects.filter(
							position=i.position,type_of_order=order.order_type,staff_category=i.staff_category)

						for j in acti_cate:
							lead_time=0
							if order.target_lead_time>=120:
								lead_time=j.lead_Time_for_120_Days
							elif order.target_lead_time<120 and order.target_lead_time>=105:
								lead_time=j.lead_Time_for_105_Days
							elif order.target_lead_time<105 and order.target_lead_time>=90:
								lead_time=j.lead_Time_for_90_Days
							elif order.target_lead_time<90 and order.target_lead_time>=75:
								lead_time=j.lead_Time_for_75_Days
							elif order.target_lead_time<75 and order.target_lead_time>=60:
								lead_time=j.lead_Time_for_60_Days
							elif order.target_lead_time<60 and order.target_lead_time>=45:
								lead_time=j.lead_Time_for_45_Days
							elif order.target_lead_time<45 and order.target_lead_time>=30:
								lead_time=j.lead_Time_for_30_Days
							elif order.target_lead_time<30 and order.target_lead_time>=15:
								lead_time=j.lead_Time_for_15_Days
							elif order.target_lead_time<15 and order.target_lead_time>=7:
								lead_time=j.lead_Time_for_7_Days
							elif order.target_lead_time<7 and order.target_lead_time>=3:
								lead_time=j.lead_Time_for_3_Days
							j.completed_in=lead_time
							j.save()
							acti=activities(
								user=objs1,
								slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
								activity_Cate=j,
								order=order,
								planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
								prev_lap=lead_time)
							acti.save()
							if j.linked_activity:
								acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
								order=order).first()
								if acti_obj_exi:
									previous_date_to=acti_obj_exi.planned_date
								else:
									previous_date_to=datetime.datetime.now()
							else:
								previous_date_to=datetime.datetime.now()
							acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
							# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
							acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('head_to_garment'):
					staff_to=request.POST.get('head_to_garment')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Allocated to you !("+str(order_no)+") !",
						description="Allocate Different Vendors to it",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=objs1.seller_category)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))

				fab_obj=seller_Categories.objects.filter(name='Fabric Vendor').first()
				log_obj=seller_Categories.objects.filter(name='Logistic Vendor').first()
				pack_obj=seller_Categories.objects.filter(name='Packing Trims Vendor').first()
				fin_obj=seller_Categories.objects.filter(name='Finishing Trims Vendor').first()
				sew_obj=seller_Categories.objects.filter(name='Sewing Trims Vendor').first()
				if request.POST.get('gar_to_fab'):
					staff_to=request.POST.get('gar_to_fab')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					print("Addf",fab_obj)
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=fab_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('gar_to_log'):
					staff_to=request.POST.get('gar_to_log')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=log_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('gar_to_fin'):
					staff_to=request.POST.get('gar_to_fin')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=fin_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('gar_to_sew'):
					staff_to=request.POST.get('gar_to_sew')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=sew_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				if request.POST.get('gar_to_pack'):
					staff_to=request.POST.get('gar_to_pack')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=pack_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
					# Currwork
				# data['pom_form'] = pom_form(instance=order)
				if request.POST.get('pom_values[]'):
					pom_ids = request.POST.getlist('pom_values[]')
					print('THESE ARE POMIDS: {}'.format(pom_ids))
					order.poms_keys.clear()
					order.poms_keys.add(*pom_ids)
				data['currUser'] = details
				pom_options = POM.objects.filter(product_Category=order.product_Category, product_Subcategory=order.product_Subcategory, product_Supercategory=order.product_Supercategory)
				pom_keys =  order.poms_keys.all()
				pom_data = []
				for option in pom_options:
					if option in pom_keys:
						pom_data.append([option, True])
					else:
						pom_data.append([option, False])
				
				data['pom_options'] = pom_data
				print(f'POM DATA: {pom_data}\n'*10)
				print(f'DATA: {data}')
				mdocs_order = manual_documents.objects.filter(order=order).first()
				mdocs = manual_documents.objects.filter(seller=order.fashion_Brand, product_Category=order.product_Category, product_Subcategory=order.product_Subcategory, product_Supercategory=order.product_Supercategory).first()
				if mdocs_order:
					data['mdocs']= mdocs_order
				else:
					data['mdocs'] = mdocs
				#CURRWORK
				print(f'DATA: {data}')
				return render(request,"userdetail/staff_profile_orders.html",data)
			else:
				return redirect('/userdetail/staff_profile')
		else:
			print('LOGGING OUT')
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')

def manual_docs_add(request, order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		order = company_Order.objects.filter(order_no=order_no).first()
		if request.POST.get('manual_doc_form'):
			docsinstance = manual_documents()
			docsinstance.seller = details
			docsinstance.order = order
			docsinstance.name = request.POST.get('name')
			docsinstance.product_Category_id = request.POST.get('product_Category')
			docsinstance.product_Subcategory_id = request.POST.get('product_Subcategory')
			docsinstance.product_Supercategory_id = request.POST.get('product_Supercategory')
			docsinstance.folding_doc = request.FILES.get('folding_doc')
			docsinstance.packing_doc = request.FILES.get('packing_doc')
			docsinstance.packing_manual = request.FILES.get('packing_manual')
			docsinstance.all_in_one = request.FILES.get('all_in_one')
			docsinstance.save()
			return redirect('staff_profile_orders', order_no=order_no)
		mform = manual_docs_form(initial={'seller':details})
		return render(request, 'userdetail/manual_documents_edit.html', {'manual_form': mform, 'order_based':True})
	else:
		return redirect('login_page')

def manual_docs_edit(request, manual_docs_id):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		docsinstance = manual_documents.objects.filter(pk=manual_docs_id).first()
		if docsinstance and docsinstance.seller == details:
			if request.POST.get('manual_doc_form'):
				docsinstance.name = request.POST.get('name')
				docsinstance.product_Category_id = request.POST.get('product_Category')
				docsinstance.product_Subcategory_id = request.POST.get('product_Subcategory')
				docsinstance.product_Supercategory_id = request.POST.get('product_Supercategory')
				docsinstance.folding_doc = request.FILES.get('folding_doc')
				docsinstance.packing_doc = request.FILES.get('packing_doc')
				docsinstance.packing_manual = request.FILES.get('packing_manual')
				docsinstance.all_in_one = request.FILES.get('all_in_one')
				docsinstance.save()
				return redirect('seller_profile_store')
			if request.POST.get('delete_manual_docs'):
				docsinstance.delete()
				return redirect('seller_profile_store')
			mform = manual_docs_form(instance=docsinstance)
			return render(request, 'userdetail/manual_documents_edit.html', {'manual_form': mform})
		else:
			return HttpResponse('Sorry, This Documents does not exist')
	else:
		return redirect('login_page')


def trim_section_edit(request, trim_section_id):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		tinstance = trimcard_sections.objects.filter(pk=trim_section_id).first()
		if tinstance and tinstance.seller == details:
			if request.POST.get('trims_form'):
				fabric_and_quantity_no = True if request.POST.get('fabric_and_quantity_no') == 'on' else False
				embroidary_sample_and_thread_code = True if request.POST.get('embroidary_sample_and_thread_code') == 'on' else False
				thread_brand_and_count = True if request.POST.get('thread_brand_and_count') == 'on' else False
				polybag = True if request.POST.get('polybag') == 'on' else False
				pocketing = True if request.POST.get('pocketing') == 'on' else False
				internlining = True if request.POST.get('internlining') == 'on' else False
				tinstance.name = request.POST.get('name')
				tinstance.product_Category_id = request.POST.get('product_Category')
				tinstance.product_Subcategory_id = request.POST.get('product_Subcategory')
				tinstance.product_Supercategory_id = request.POST.get('product_Supercategory')
				tinstance.fabric_and_quantity_no = fabric_and_quantity_no
				tinstance.embroidary_sample_and_thread_code = embroidary_sample_and_thread_code
				tinstance.thread_brand_and_count = thread_brand_and_count
				tinstance.polybag = polybag
				tinstance.pocketing = pocketing
				tinstance.internlining = internlining
				tinstance.save()
				return redirect('seller_profile_store')
			if request.POST.get('delete_trim_section'):
				tinstance.delete()
				return redirect('seller_profile_store')
			tform = trim_form(instance=tinstance)
			return render(request, 'userdetail/trim_section_edit.html', {'trim_form': tform})
		else:
			return HttpResponse('Sorry, This trim card does not exist')
	else:
		return redirect('login_page')



# sanskars code
def generate_qr(request,order_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				details=detail.objects.get(email="raymond@raymond.in")
				if(not order.layout):
					return HttpResponse("Please select a layout first")

				carton_list = Carton_new.objects.filter(order=order)
				print(carton_list)
				color_list = []
				sizes_list = []
				for carton in carton_list:
					for i in carton.sizes.all():
						if (i.color not in color_list):
							color_list.append(i.color)
						if (i.size not in sizes_list):
							sizes_list.append(i.size)

				sizes_list.sort()
				for carton in carton_list:
					colors = []
					sizes = []
					qr=""
					total=0
					for color in color_list:
						count = 0
						for i in carton.sizes.all():
							if i.color == color:
								count += i.quantity
						colors.append([color.name, count])
						total+=count

					for size in sizes_list:
						count = 0

						for i in carton.sizes.all():
							if i.size == size:
								u=i.size
								count += i.quantity
						sizes.append([size,count])



					qr+="Carton"+'-'
					qr+=str(order.order_no) + '-'
					qr+=str(carton.id)+'-'
					qr+=str(carton.address.address)+'-'
					qr+=str(colors)+'-'
					qr+=str(sizes)+'-'
					j=order.layout.indep_atr.split('-')
					if('Brand Name' in j):
						qr+="Raymond"+'-'
					if ('Label Name' in j):
						qr+= str(order.label)+'-'
					if ('Category' in j):
						qr+=str(order.product_Category)+'-'
					if ('Super category' in j):
						qr += str(order.product_Supercategory)+'-'
					if ('Style' in j):
						qr+= "Raymond"+'-'
					if ('Size' in j):
						qr+= str(sizes_list)+'-'
					if ('Colour' in j):
						qr+= str(color_list)+'-'
					if ('Net qty' in j):
						qr+= str(order.quantity)+'-'
					if('Pkd' in j):
						qr+= str(order.order_date_time)+'-'
					if ('Blend' in j):
						qr += "Polywool" +'-'
					if('MRP' in j):
						qr=str(order.total_Price)+'-'
					if ('Address' in j):

						qr += str(details.address)+'-'
					if ('Contact' in j):
						qr+=str(details.contact)+'-'
					if ('Email' in j):
						qr+="raymond@raymond.in" +'-'
					if('Website' in j):
						qr+="website"+'-'
					if('t&c' in j):
						qr+=str(details.t_and_c)+'-'
					carton.qr=str(qr)
					carton.save()
				return redirect('/userdetail/staff_profile/show_all_packing/'+str(order.order_no))

def view_qr(request,order_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()

				carton_list = Carton_new.objects.filter(order=order)

				return render(request,'userdetail/All_qrs.html',{'cartons_links':carton_list,'order':order})

def Packing_list(request,order_no=None,*args,**kwargs):

	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				if request.method == 'POST':
					sizes_opt = quantity_b2b.objects.filter(order=order)
					size_lst = []
					for e in sizes_opt:
						if e.size_label not in size_lst:
							size_lst.append(e.size_label)
					size_lst.sort()
					address = int(request.POST.get('address'))
					address = address_model.objects.filter(id=address).first()
					color = int(request.POST.get('color'))
					color = color_model.objects.filter(id=color).first()
					quantity=0
					for i in size_lst:
						if(request.POST[str(i)]):

							quantity+=int(request.POST[str(i)])

					packing=new_pl(order=order,address=address,color=color,quantity=quantity)
					packing.save()
					s=request.POST
					print(size_lst)


					for i in size_lst:
						print('yes')

						print(s[str(i)])
						if s[str(i)]:
							print('yes')
							size_assort = int(s[str(i)])
							packing_size_qty = plqty(size=i, quantity=size_assort, leftquantity=size_assort,
													 order=order)
							packing_size_qty.save()
							packing.sizes.add(packing_size_qty)




							objs_size_assort = balance_quantity_b2b.objects.filter(order=order,
																	   size_label=i,
																	   color=color,
																	   address=address,
																		production=True,
																		   packing=True
																		)
							print(objs_size_assort)



							pk_obj=balance_list_2.objects.all().filter(order=order,sizes=objs_size_assort.first()).first()
							print(pk_obj)
							if(not pk_obj):
								packing_size_qty.delete()
								return(HttpResponse('please make a valid choice'))

							no_error=True
							a=None
							for x in pk_obj.sizes.all():
								if x==objs_size_assort.first():

									print("No")
									a=x
									if(a.quantity<size_assort or size_assort<0):
										no_error=False
							if(no_error):

								for x in pk_obj.sizes.all():
									if x == objs_size_assort.first():

										print("No")
										a = x

										a.quantity -= size_assort
										a.save()
										break
							else:
								packing.delete()
								return (HttpResponse("please make a valid choice"))






					return redirect('/userdetail/staff_profile/orders/' + str(order.order_no))
				else:
					details = detail.objects.filter(email=request.user.email).first()
					orders = company_Order.objects.filter(staffs_Allocated=details, order_no=order_no)
					order = orders.first()

					packing_kjh = packing_list_1.objects.filter(order=order).order_by('list_no')
					balance_kjh= balance_list_2.objects.filter(order=order).order_by('list_no')
					print(balance_kjh)
					prod = []
					csv_prod = []
					packing_prod = []
					balance_prod=[]
					sizes_cum_prod = []
					sizes_opt = quantity_b2b.objects.filter(order=order)
					size_lst = []
					packing_sizes_cum_prod = []
					colors_cum_prod = []
					packing_colors_cum_prod = []
					address_cum_prod = []
					packing_address_cum_prod = []
					for e in sizes_opt:
						if e.size_label not in size_lst:
							size_lst.append(e.size_label)
					size_lst.sort()

					for i in packing_kjh:
						for j in i.sizes.all():
							if not (j.size_label in packing_sizes_cum_prod) and j.size_label:
								packing_sizes_cum_prod.append(j.size_label)
							if not (j.color in colors_cum_prod):
								packing_colors_cum_prod.append(j.color)
							if not (j.address in address_cum_prod):
								packing_address_cum_prod.append(j.address)

					for i in balance_kjh:
						for j in i.sizes.all():
							if not (j.size_label in packing_sizes_cum_prod) and j.size_label:
								packing_sizes_cum_prod.append(j.size_label)
							if not (j.color in colors_cum_prod):
								packing_colors_cum_prod.append(j.color)
							if not (j.address in address_cum_prod):
								packing_address_cum_prod.append(j.address)

					sizes_cum_prod.sort()
					packing_sizes_cum_prod.sort()
					map_prod = {}
					packing_map_prod = {}

					for i in packing_kjh:
						packing_prod.append([i])
						sikl = []
						for j in i.sizes.all():
							if not (j.size_label in sikl):
								sikl.append(j.size_label)
						sikl.sort()
						# print("\n\n\n\n",sikl)
						packing_prod[-1].append(sikl)
						coli = []
						addi = []
						for j in i.sizes.all():
							if not (j.color in coli):
								coli.append(j.color)
							if not (j.address in addi):
								addi.append(j.address)
						tot_sikl = [0 for klj in range(len(sikl))]
						kjh568 = []
						# print(sikl)
						for j in coli:
							for k in addi:
								treh = []
								check = False
								for l in sikl:
									gfb = i.sizes.all().filter(color=j, address=k, size_label=l)
									if gfb.first():
										check = True
										treh.append(gfb.first().quantity)
										tot_sikl[sikl.index(l)] += gfb.first().quantity
									else:
										treh.append(0)
								if check:
									kjh568.append([j, k, treh])
						packing_prod[-1].append(kjh568)
						packing_prod[-1].append(tot_sikl)


					for i in balance_kjh:
						balance_prod.append([i])
						sikl = []
						for j in i.sizes.all():
							if not (j.size_label in sikl):
								sikl.append(j.size_label)
						sikl.sort()
						# print("\n\n\n\n",sikl)
						balance_prod[-1].append(sikl)
						coli = []
						addi = []
						for j in i.sizes.all():
							if not (j.color in coli):
								coli.append(j.color)
							if not (j.address in addi):
								addi.append(j.address)
						tot_sikl = [0 for klj in range(len(sikl))]
						kjh568 = []
						# print(sikl)
						for j in coli:
							for k in addi:
								treh = []
								check = False
								for l in sikl:
									gfb = i.sizes.all().filter(color=j, address=k, size_label=l)
									if gfb.first():
										check = True
										treh.append(gfb.first().quantity)
										tot_sikl[sikl.index(l)] += gfb.first().quantity
									else:
										treh.append(0)
								if check:
									kjh568.append([j, k, treh])
						balance_prod[-1].append(kjh568)
						balance_prod[-1].append(tot_sikl)

					return render(request, 'userdetail/packing_list.html', {'balance_packingprod789':balance_prod,'packing_prod789': packing_prod,'order':order,'sizes_lst':size_lst})


#details = detail.objects.filter(email=request.user.email).first()
	#orders = company_Order.objects.filter(staffs_Allocated=details, order_no=order_no)

def show_carton_list(request,order_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				carton_list=Carton_new.objects.filter(order=order)
				print(carton_list)
				color_list=[]
				sizes_list=[]
				for carton in carton_list:
					for i in carton.sizes.all():
						if(i.color not in color_list):
							color_list.append(i.color)
						if(i.size not in sizes_list):
							sizes_list.append(i.size)


				sizes_list.sort()

				for carton in carton_list:
					sum=0
					for i in carton.sizes.all():
						sum+=i.quantity

					carton.row_wise_sum=sum
				universal_color=[]
				universal_size=[]
				all_address=[]
				for carton in carton_list:
					all_address.append(carton.address)
				for carton in carton_list:
					colors=[]
					sizes=[]
					for color in color_list:
						count=0
						for i in carton.sizes.all():
							if i.color==color:
								count+=i.quantity
						colors.append([color,count])

					carton.clr=colors
					for size in sizes_list:
						count=0
						for i in carton.sizes.all():
							if i.size==size:
								count+=i.quantity
						sizes.append([count])
					carton.sz=sizes

				layouts=Layout.objects.all()
				for carton in carton_list:
					print(carton.sz)

				if(request.method=='POST'):
					print("Layout request")
					print(request.POST)
					print(request.POST.get('Layout'))
					s=int(request.POST.get('Layout'))
					print(s)
					print("sg")
					v=Layout.objects.filter(id=s)
					order.layout=v.first()
					print(order.layout)
					order.save()
					return HttpResponseRedirect('/userdetail/staff_profile/orders/' + str(order_no)+'/forms/packing_list')

				print(order.layout)
				data={'Layouts':layouts,'current_layout':order.layout,'color_quan':universal_color,'size_quan':universal_size,'order':order,'color_lists':color_list,'size_lists':sizes_list,'address':all_address,'cartons':carton_list}
				return render(request,'userdetail/carton_list.html',data)

def view_all_qr(request,order_no=None,carton_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				c=Carton_new.objects.all().filter(order=order)
				print(c)
				if(c):
					return render(request,'userdetail/View_all_carton_qr.html',{'Carton':c})


def print_all_pieces_qr(request,order_no=None,carton_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				c=Carton_new.objects.all().filter(order=order,id=carton_no).first()
				qrs=[]
				print(c.sizes)
				for x in c.sizes.all():
					for i in range(x.quantity):
						qrs.append("Size:- "+str(x.size)+" quantity"+str(1))

				print(c)
				if(c):
					return render(request,'userdetail/View_all_carton_qr.html',{'Carton':c,'Qrs':qrs})



def show_pieces_in_individual(request,order_no=None,carton_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				c=Carton_new.objects.all().filter(order=order,id=carton_no).first()
				qrs=[]
				print(c.sizes)
				for x in c.sizes.all():
					for i in range(x.quantity):
						qrs.append("Size:-"+str(x.size)+"color"+str(x.color)+"quantity"+str(1))

				print(c)
				if(c):
					return render(request,'userdetail/print_individual_pieces_qr.html',{'Carton':c,'Qrs':qrs})

def print_pieces_in_individual_carton(request,q=None,*args,**kwargs):
	return render(request,'userdetail/qr.html',{'data':q})



def inside_carton(request,order_no=None,carton_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				c=Carton_new.objects.all().filter(order=order,id=carton_no).first()
				print(c)
				if(c):
					return render(request,'userdetail/inside_carton.html',{'Carton':c})
def print_individual_carton(request,order_no=None,carton_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()

				if (not order.layout):
					return HttpResponse("Please select a layout first")
				layout = order.layout
				print(layout)
				c = Carton_new.objects.all().filter(order=order, id=carton_no).first()
				carton_list = Carton_new.objects.filter(order=order)
				print(carton_list)
				color_list = []
				sizes_list = []
				for i in c.sizes.all():
					if (i.color not in color_list):
						color_list.append(i.color)
					if (i.size not in sizes_list):
						sizes_list.append(i.size)


				sizes_list.sort()
				colors = []
				sizes = []
				qr = {}
				for color in color_list:
					count = 0
					for i in c.sizes.all():
						if i.color == color:
							count += i.quantity
					colors.append([color.name, count])

				for size in sizes_list:
					count = 0

					for i in c.sizes.all():
						if i.size == size:
							u = i.size
							count += i.quantity
					sizes.append([size, count])



				j = order.layout.indep_atr.split('-')

				qr['Brand_Name'] = "Raymond"

				qr['Label_Name'] = order.label

				qr['Category'] = order.product_Category

				qr['SuperCategory'] = order.product_Supercategory

				qr['Style'] = "Raymond"

				qr['Size'] = str(sizes_list)

				qr['Colour'] = str(color_list)

				qr['Net_Qty'] = order.quantity

				qr['pkd_date'] = order.order_date_time

				qr['Blend'] = "Polywool"

				qr['MRP'] = order.total_Price

				qr['address'] = details.address

				qr['contact'] = details.contact

				qr['Email'] = "raymond@raymond.in"

				qr['Website'] = "website"

				qr['TandC'] = details.t_and_c
				print(qr)

				if(c):
					print(c.qr)
					return render(request,'userdetail/individual_carton.html',{'Carton':c,'Layout':layout,'detail':qr})
				else:
					return HttpResponse("no such carton exists")


def generate_carton_list(request,order_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				packing_obj=new_pl.objects.filter(order=order,is_packed=False)
				left_over=[]
				sizes = []
				print(sizes)
				for item in packing_obj:

					for s in item.sizes.all():
						if s.size not in sizes:
							sizes.append(s.size)
				carton_max = ca.objects.filter(product_Category=order.product_Category,
												product_Subcategory=order.product_Subcategory,
												product_Supercategory=order.product_Supercategory).first().maximum_quantity
				sizes.sort()
				print(carton_max)
				for item in packing_obj:
					no_of_cartons=0
					if(item.quantity!=0):
						no_of_cartons=int(item.quantity/carton_max)+1
					ct=[]
					for i in range(no_of_cartons):
						carton=Carton_new(name="Carton",address=item.address,order=order,is_filled=False,left_capacity=carton_max)
						carton.save()
						ct.append(carton)

					for carton in ct:
						if(carton.left_capacity):
							for size in sizes:
								a=item.sizes.all().filter(size=size)
								a=a.first()
								print(a)
								if(a):
									while(a.leftquantity!=0):
										if(a.leftquantity<carton.left_capacity):
											carton.left_capacity-=a.leftquantity

											sz=scl(order=order,size=size,color=item.color,quantity=a.leftquantity)
											sz.save()
											carton.packing_list=item
											carton.save()
											carton.sizes.add(sz)
											a.leftquantity = 0
											a.save()
										else:
											sz=scl(order=order,size=size,color=item.color,quantity=carton.leftcapacity)
											sz.save()

											carton.packing_list=item
											carton.save()
											carton.sizes.add(sz)
											a.leftquantity-=carton.left_capacity
											carton.left_capacity = 0
											a.save()


				for item in packing_obj:
					item.is_packed=True
					item.save()

				return redirect('/userdetail/staff_profile/orders/' + str(order.order_no))


def ShowPacking(request,order_no=None,*args,**kwargs):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				order = orders.first()
				data=new_pl.objects.all().filter(order=order)
				return render(request,'userdetail/showpacking.html',{'plists':data,'order':order})


def Carton_details(request,carton):
	products=models.Carton.objects.all().filter(carton_no=carton)
	return render(request,'userdetail/carton_details.html',{'product':products})





def ShowPage(request,order_no=None,*arg,**kwargs):
	frm = forms.FileForm()

	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				ohj=quantity_b2b.objects.filter(order=orders.first(),production=False)
				order = orders.first()
				if (request.method == 'POST'):

					form = forms.FileForm(request.POST, request.FILES)
					if form.is_valid():
						s = form.cleaned_data['doc']
						fs = FileSystemStorage()
						name = fs.save(s.name, s)
						c = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
						print(fs.url(name))
						# print(s.read)

						# with open('C:/Users/sgbhidu.LAPTOP-QSE5SAAV/Desktop/internship/internship/media/sg.csv', newline='') as File:

						with open(settings.MEDIA_ROOT + "/"+ name, newline='') as File:
							reader = csv.DictReader(File)

							for row in reader:
								s = {}
								product = models.items()
								cl=row['COLOR']
								color = models.Color.objects.all().filter(name=cl.lower())
								c=color_model.objects.filter(name=cl.lower())
								print(c)
								if c:
									if color:
										product.color = color[0]
									#c=color_model(name=row['COLOR'])
									else:
										a=models.Color(name=cl.lower())
										a.save()
										product.color=a

									#c.save()
									color=c
								else:
									c = models.Color()
									e = color_model(name=cl.lower())
									e.save()
									c.name = row['COLOR']
									c.save()
									g = models.Color.objects.all().filter(name=cl.lower())
									color=color_model.objects.filter(id=e.id)
									product.color = g[0]
								product.Brand_name = row['Brand Name']
								product.Categories = row['Categories']
								product.Super_categories = row['Super categories']
								product.total = int(row['TOTAL'])
								product.address = row['ADDRESS']
								product.ts24 = int(row['24'])
								address=address_model.objects.filter(address=row['ADDRESS'])
								if(address):
									address=address[0]
								else:
									address=address_model(address=row['ADDRESS'])
									address.save()
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=24,
									address=address,
									color=color.first(),
									quantity=product.ts24,
									production=False,
									is_csv=True
								)
								objs_size_assort.save()
								product.ts28 = int(row['28'])
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=28,
									address=address,
									color=color[0],
									quantity=product.ts28,
									production=False,
									is_csv=True
								)
								objs_size_assort.save()
								product.ts30 = int(row['30'])
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=30,
									address=address,
									color=color[0],
									quantity=product.ts30,
									production=False,
									is_csv=True
								)
								objs_size_assort.save()
								product.ts32 = int(row['32'])
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=32,
									address=address,
									color=color[0],
									quantity=product.ts32,
									production=False,
									is_csv=True
								)
								objs_size_assort.save()
								product.ts34 = int(row['34'])
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=34,
									address=address,
									color=color[0],
									quantity=product.ts34,
									production=False,
									is_csv=True

								)
								objs_size_assort.save()
								product.ts36 = int(row['36'])
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=36,
									address=address,
									color=color[0],
									quantity=product.ts36,
									production=False,
									is_csv=True
								)
								objs_size_assort.save()
								product.ts38 = int(row['38'])
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=38,
									address=address,
									color=color[0],
									quantity=product.ts38,
									production=False,
									is_csv=True
								)
								objs_size_assort.save()
								product.ts40 = int(row['40'])
								objs_size_assort = quantity_b2b(
									order=order,
									size_label=40,
									address=address,
									color=color[0],
									quantity=product.ts40,
									production=False,
									is_csv=True
								)
								objs_size_assort.save()
								product.fs30 = int(row['30'])
								product.fs32 = int(row['32'])
								product.fs34 = int(row['34'])
								product.fs36 = int(row['36'])
								product.fs38 = int(row['38'])
								product.fs40 = int(row['40'])
								product.fs24 = int(row['24'])
								product.fs28 = int(row['28'])
								product.packed_on = row['Packed on']
								product.Fit = row['Fit']
								product.Description = row['Product discription']
								product.Style = row['Style']

								s['color'] = row['COLOR']

								s['24'] = row['24']
								s['28'] = row['28']
								s['30'] = row['30']
								s['32'] = row['32']
								s['34'] = row['34']
								s['36'] = row['36']
								s['38'] = row['38']
								s['40'] = row['40']
								s['TOTAL'] = row['TOTAL']

								s['packed_on'] = row['Packed on']
								s['Fit'] = row['Fit']
								s['Description'] = row['Product discription']
								s['Style'] = row['Style']

								product.barcode = str(s)

								product.save()
						fs.delete(name)

					return redirect('/userdetail/staff_profile')




			return render(request, 'userdetail/normal.html', {'forms': frm})


def UpdateCsv(request, order_no=None, *arg, **kwargs):
	frm = forms.FileForm()

	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders = company_Order.objects.filter(staffs_Allocated=details, order_no=order_no)
			if orders.count() > 0:
				ohj = quantity_b2b.objects.filter(order=orders.first(), production=False)
				order = orders.first()
				if (request.method == 'POST'):

					form = forms.FileForm(request.POST, request.FILES)
					if form.is_valid():
						s = form.cleaned_data['doc']
						fs = FileSystemStorage()
						name = fs.save(s.name, s)
						c = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
						print(fs.url(name))
						with open(c + fs.url(name), newline='') as File:
							reader = csv.DictReader(File)

							for row in reader:
								s = {}
								product = models.items()
								color = models.Color.objects.all().filter(name=row['COLOR'])
								c = color_model.objects.filter(name=row['COLOR'])
								print(c[0])

								product.color = color.first()
								product.Brand_name = row['Brand Name']
								product.Categories = row['Categories']
								product.Super_categories = row['Super categories']
								product.total = int(row['TOTAL'])
								product.address = row['ADDRESS']
								product.ts24 = int(row['24'])
								address = address_model.objects.filter(address=row['ADDRESS'])
								print(address.first())


								if (row['24']):
									objs_size_assort = quantity_b2b.objects.filter(
										order = order,
										size_label=24,
										address=address.first(),

										color=c[0],

										production=False,
										is_csv=True
									)

									print(objs_size_assort.first())
									co=objs_size_assort.first()
									co.quantity += int(row['24'])
									co.save()
								if (row['28']):
									objs_size_assort = quantity_b2b.objects.filter(
										order=order,
										size_label=28,
										address=address.first(),
										color=c[0],

										production=False,
										is_csv=True
									)
									co = objs_size_assort.first()
									co.quantity += int(row['28'])
									co.save()
								product.ts28 = int(row['28'])
								if (row['30']):
									objs_size_assort = quantity_b2b.objects.filter(
										order=order,
										size_label=30,
										address=address.first(),
										color=c[0],

										production=False,
										is_csv=True
									)
									co = objs_size_assort.first()
									co.quantity += int(row['30'])
									co.save()
								product.ts30 = int(row['30'])
								if (row['32']):
									objs_size_assort = quantity_b2b.objects.filter(
										order=order,
										size_label=32,
										address=address.first(),
										color=c[0],

										production=False,
										is_csv=True
									)
									co = objs_size_assort.first()
									co.quantity += int(row['32'])
									co.save()

								product.ts32 = int(row['32'])
								if (row['34']):
									objs_size_assort = quantity_b2b.objects.filter(
										order=order,
										size_label=34,
										address=address.first(),
										color=c[0],

										production=False,
										is_csv=True
									)
									co = objs_size_assort.first()
									co.quantity += int(row['34'])
									co.save()
								product.ts34 = int(row['34'])
								if (row['36']):
									objs_size_assort = quantity_b2b.objects.filter(
										order=order,
										size_label=36,
										address=address.first(),
										color=c[0],

										production=False,
										is_csv=True
									)
									co = objs_size_assort.first()
									co.quantity += int(row['36'])
									co.save()
								product.ts36 = int(row['36'])
								if (row['38']):
									objs_size_assort = quantity_b2b.objects.filter(
										order=order,
										size_label=38,
										address=address.first(),
										color=c[0],

										production=False,
										is_csv=True
									)
									co = objs_size_assort.first()
									co.quantity += int(row['38'])
									co.save()

								product.ts38 = int(row['38'])

								if (row['40']):
									objs_size_assort = quantity_b2b.objects.filter(
										order=order,
										size_label=40,
										address=address.first(),
										color=c[0],

										production=False,
										is_csv=True
									)
									co = objs_size_assort.first()
									co.quantity += int(row['40'])
									co.save()
								product.ts40 = int(row['40'])

								product.fs30 = int(row['30'])
								product.fs32 = int(row['32'])
								product.fs34 = int(row['34'])
								product.fs36 = int(row['36'])
								product.fs38 = int(row['38'])
								product.fs40 = int(row['40'])
								product.fs24 = int(row['24'])
								product.fs28 = int(row['28'])
								product.packed_on = row['Packed on']
								product.Fit = row['Fit']
								product.Description = row['Product discription']
								product.Style = row['Style']

								s['color'] = row['COLOR']

								s['24'] = row['24']
								s['28'] = row['28']
								s['30'] = row['30']
								s['32'] = row['32']
								s['34'] = row['34']
								s['36'] = row['36']
								s['38'] = row['38']
								s['40'] = row['40']
								s['TOTAL'] = row['TOTAL']

								s['packed_on'] = row['Packed on']
								s['Fit'] = row['Fit']
								s['Description'] = row['Product discription']
								s['Style'] = row['Style']

								product.barcode = str(s)

								product.save()


						return redirect('/userdetail/staff_profile')


				return render(request, 'userdetail/normal.html', {'forms': frm})



def Forminput(request):
	s=forms.CartonForm()
	return render(request,'userdetail/takecapacity.html',{'form':s})



def GeneratePackingList(request):
	#form=forms.CartonForm()
	if request.method=='POST':
		form=forms.CartonForm(request.POST)
		if form.is_valid():
			capacity=form.cleaned_data['capacity']

			products = models.items.objects.all()

			for p in products:
				if p.fs24<capacity:
					continue
				elif p.fs24!=0:

					n=int(p.fs24/capacity)
					for i in range(n):
						carton=models.Carton()
						carton.capacity=capacity
						carton.leftcapacity=capacity
						carton.address=p.address
						carton.ts24=capacity



						carton.qrcode="dw"
						carton.save()


						p.fs24-=capacity
						p.save()
						s={}
						s['Capacity']=capacity
						s['Address']=p.address
						s['Color']=p.color
						s['24']=carton.ts24
						s['28']=carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode=str(s)
						carton.save()
						carton.colors.add(p.color)

			for p in products:
				if p.fs28 < capacity:
					continue
				elif p.fs28 != 0:
					n=int(p.fs28/capacity)
					for i in range(n):
						carton = models.Carton()
						carton.capacity = capacity
						carton.leftcapacity = capacity
						carton.address = p.address
						carton.ts28 = capacity

						carton.qrcode = "dw"
						carton.save()
						p.fs28 -= capacity
						p.save()

						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = p.color
						s['24'] = carton.ts24
						s['28'] = carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode = str(s)
						carton.save()
						carton.colors.add(p.color)

			for p in products:
				if p.fs30 < capacity:
					continue
				elif p.fs30 != 0:
					n=int(p.fs30/capacity)
					for i in range(n):
						carton = models.Carton()
						carton.capacity = capacity
						carton.leftcapacity = capacity
						carton.address = p.address
						carton.ts30 = capacity

						carton.qrcode = "dw"
						carton.save()
						p.fs30 -= capacity
						p.save()

						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = p.color
						s['24'] = carton.ts24
						s['28'] = carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode = str(s)
						carton.save()
						carton.colors.add(p.color)



			for p in products:
				if p.fs32 < capacity:
					continue
				elif p.fs32 != 0:
					n=int(p.fs32/capacity)
					for i in range(n):
						carton = models.Carton()
						carton.capacity = capacity
						carton.leftcapacity = capacity
						carton.address = p.address
						carton.ts32 = capacity

						carton.qrcode = "dw"
						carton.save()
						p.fs32 -= capacity
						p.save()
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = p.color
						s['24'] = carton.ts24
						s['28'] = carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode = str(s)
						carton.save()
						carton.colors.add(p.color)



			for p in products:
				if p.fs34 < capacity:
					continue
				elif p.fs34 != 0:
					n=int(p.fs34/capacity)
					for i in range(n):
						carton = models.Carton()
						carton.capacity = capacity
						carton.leftcapacity = capacity
						carton.address = p.address
						carton.ts34 = capacity

						carton.qrcode = "dw"
						carton.save()
						p.fs34 -= capacity
						p.save()
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = p.color
						s['24'] = carton.ts24
						s['28'] = carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode = str(s)
						carton.save()
						carton.colors.add(p.color)

			for p in products:
				if p.fs36 < capacity:
					continue
				elif p.fs36 != 0:
					n=int(p.fs36/capacity)
					for i in range(n):
						carton = models.Carton()
						carton.capacity = capacity
						carton.leftcapacity = capacity
						carton.address = p.address
						carton.ts36 = capacity

						carton.qrcode = "dw"
						carton.save()
						p.fs36 -= capacity
						p.save()
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = p.color
						s['24'] = carton.ts24
						s['28'] = carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode = str(s)
						carton.save()
						carton.colors.add(p.color)


			for p in products:
				if p.fs38 < capacity:
					continue
				elif p.fs38 != 0:
					n=int(p.fs38/capacity)
					for i in range(n):
						carton = models.Carton()
						carton.capacity = capacity
						carton.leftcapacity = capacity
						carton.address = p.address
						carton.ts38 = capacity
						carton.qrcode = "dw"
						carton.save()
						p.fs38 -= capacity
						p.save()
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = p.color
						s['24'] = carton.ts24
						s['28'] = carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode = str(s)
						carton.save()
						carton.colors.add(p.color)

			for p in products:
				if p.fs40 < capacity:
					continue
				elif p.fs40 != 0:
					n=int(p.fs40/capacity)
					for i in range(n):
						carton = models.Carton()
						carton.capacity = capacity
						carton.leftcapacity = capacity
						carton.address = p.address
						carton.ts40 = capacity
						carton.qrcode = "dw"
						carton.save()
						p.fs40 -= capacity
						p.save()
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = p.color
						s['24'] = carton.ts24
						s['28'] = carton.ts28
						s['30'] = carton.ts30
						s['32'] = carton.ts32
						s['34'] = carton.ts34
						s['36'] = carton.ts36
						s['38'] = carton.ts38
						s['40'] = carton.ts40
						carton.qrcode = str(s)
						carton.save()
						carton.colors.add(p.color)



			count=0
			for p in products:
				count+=p.fs24
				count+=p.fs28
				count+=p.fs30
				count+=p.fs32
				count+=p.fs34
				count+=p.fs36
				count+=p.fs38
				count+=p.fs40

			car=[]
			for i in range(int(count/capacity)+1):
				a=models.Carton()
				a.capacity=capacity
				a.leftcapacity=capacity
				a.save()
				car.append(a)


			for c in car:
				for p in products:
					if (c.leftcapacity != 0):
						if (c.leftcapacity <= p.fs24):

							c.ts24 += c.leftcapacity
							p.fs24 -= c.leftcapacity
							c.leftcapacity = 0


						else:
							c.ts24 += p.fs24
							c.leftcapacity -= p.fs24
							p.fs24 = 0
						c.address = p.address




						c.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()
						p.save()


				for p in products:
					if (c.leftcapacity != 0):
						if (c.leftcapacity <= p.fs28):

							c.ts28 += c.leftcapacity
							p.fs28 -= c.leftcapacity
							c.leftcapacity = 0


						else:
							c.ts28 += p.fs28
							c.leftcapacity -= p.fs28
							p.fs28 = 0
						c.address = p.address

						c.save()
						p.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()

				for p in products:
					if (c.leftcapacity != 0):
						if (c.leftcapacity <= p.fs30):

							c.ts30 += c.leftcapacity
							p.fs30 -= c.leftcapacity
							c.leftcapacity = 0


						else:
							c.ts30 += p.fs30
							c.leftcapacity -= p.fs30
							p.fs30 = 0
						c.address = p.address

						c.save()
						p.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()

				for p in products:
					if (c.leftcapacity != 0):
						if (c.leftcapacity <= p.fs32):

							c.ts32 += c.leftcapacity
							p.fs32 -= c.leftcapacity
							c.leftcapacity = 0


						else:
							c.ts32 += p.fs32
							c.leftcapacity -= p.fs32
							p.fs32 = 0
						c.address = p.address

						c.save()
						p.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()

				for p in products:
					if (c.leftcapacity != 0):
						if (c.leftcapacity <= p.fs34):

							c.ts34 += c.leftcapacity
							p.fs34 -= c.leftcapacity
							c.leftcapacity = 0


						else:
							c.ts34 += p.fs34
							c.leftcapacity -= p.fs34
							p.fs34 = 0
						c.address = p.address

						c.save()
						p.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()

				for p in products:
					if (c.leftcapacity != 0):
						if (c.leftcapacity <= p.fs36):

							c.ts36 += c.leftcapacity
							p.fs36 -= c.leftcapacity
							c.leftcapacity = 0


						else:
							c.ts36 += p.fs36
							c.leftcapacity -= p.fs36
							p.fs36 = 0
						c.address = p.address

						c.save()
						p.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()

				for p in products:
					if (c.leftcapacity != 0):
						if (c.leftcapacity <= p.fs38):

							c.ts38 += c.leftcapacity
							p.fs38 -= c.leftcapacity
							c.leftcapacity = 0


						else:
							c.ts38 += p.fs38
							c.leftcapacity -= p.fs38
							p.fs38 = 0
						c.address = p.address

						c.save()
						p.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()



				for p in products:
					if(c.leftcapacity != 0):
						if(c.leftcapacity<=p.fs40):

							c.ts40+=c.leftcapacity

							p.fs40 -= c.leftcapacity
							c.leftcapacity = 0

						else:
							c.ts40+=p.fs40
							c.leftcapacity-=p.fs40
							p.fs40=0
						c.address=p.address

						c.save()
						p.save()
						c.colors.add(p.color)
						s = {}
						s['Capacity'] = capacity
						s['Address'] = p.address
						s['Color'] = c.colors
						s['24'] = c.ts24
						s['28'] = c.ts28
						s['30'] = c.ts30
						s['32'] = c.ts32
						s['34'] = c.ts34
						s['36'] = c.ts36
						s['38'] = c.ts38
						s['40'] = c.ts40
						c.qrcode = str(s)
						c.save()












			return HttpResponse("Task Done")










def PackingList(request):
	carton= models.Carton.objects.all()

	for i in carton:
		s=models.order.objects.all().filter(carton=i)
		#i.address=s[0].address
	return(render(request,'userdetail/packinglist.html',{'cartons':carton}))











def sizeAssortment(request):
	s=models.items.objects.all()
	return(render(request,'userdetail/sa.html',{'products':s}))


#end of sanskar's code








def staff_notifications(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
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
			"oty4":oty4
			}
			return render(request,"userdetail/staff_notifications.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


def activity_custom_lap_update(activity,custom_lap,order):
	activity.lap=custom_lap
	activity.custom_date=activity.created_on+datetime.timedelta(days=custom_lap)
	activity.save()
	owq=activities_Category.objects.filter(linked_activity=activity.activity_Cate)
	print("These are Activities ",owq,activity.activity_Cate)
	for i in owq:
		owqt=activities.objects.filter(activity_Cate=i,order=order)
		if owqt.count()>0:
			owqt=owqt.first()
			if owqt.lap is None:
				owqt.lap=0
			lap=custom_lap+owqt.activity_Cate.Increment_or_Decrement
			activity_custom_lap_update(owqt,lap,order)
	return True





# def activity_tentative_date_update(activity,order,tentative_lap=None):
# 	owq=activities_Category.objects.filter(linked_activity=activity.activity_Cate)
# 	if tentative_lap:
# 		activity.tentative_date=activity.created_on+datetime.timedelta(days=tentative_lap)
# 		activity.save()
# 	actual_date=activity.actual_date
# 	if not(actual_date):
# 		actual_date=activity.tentative_date
# 	created_date=activity.created_on
# 	d1=datetime.date(actual_date.year,actual_date.month,actual_date.day)
# 	d2=datetime.date(created_date.year,created_date.month,created_date.day)
# 	lap=d1-d2
# 	lap=lap.days
# 	for i in owq:
# 		owqt=activities.objects.filter(activity_Cate=i,order=order)
# 		if owqt.count()>0:
# 			owqt=owqt.first()
# 			lap2=lap+owqt.activity_Cate.Increment_or_Decrement
# 			# print(lap2)
# 			activity_tentative_date_update(owqt,order,lap2)
# 	return True

def activity_tentative_date_update(activity,order):
	owq=activities_Category.objects.filter(linked_activity=activity.activity_Cate)
	for o in owq:
		oyu=activities.objects.filter(activity_Cate=o,order=order)
		for j in oyu:
			if activity.actual_date:
				prev_lap=activity.actual_date
			else:
				prev_lap=activity.tentative_date
			if not(prev_lap):
				continue
			j.tentative_date=getPlannedDate(j.user,prev_lap,j.prev_lap)
			# j.tentative_date=prev_lap+datetime.timedelta(days=j.prev_lap)
			j.save()
			activity_tentative_date_update(j,order)
	return True


def custom_date_check(activity,order,lap):
	activity1=activities.objects.filter(activity_Cate=activity,
	order=order).first()
	linked=activity.linked_activity
	if linked:
		linked=activities.objects.filter(activity_Cate=linked,
		order=order).first()
	if linked:
		prev_date=linked.custom_date
		if not(prev_date):
			prev_date=linked.planned_date
		if not(prev_date):
			prev_date=order.created_on
	else:
		prev_date=order.order_date_time
	if activity1:
		if lap:
			activity1.lap=lap
			activity1.custom_date=prev_date+datetime.timedelta(days=lap)
		else:
			activity1.lap=activity1.prev_lap
			activity1.custom_date=prev_date+datetime.timedelta(days=activity1.prev_lap)
		activity1.save()
	to_others=activities_Category.objects.filter(linked_activity=activity)
	for i in to_others:
		custom_date_check(i,order,lap=None)
	return True


def staff_profile_activity(request,activity_slug):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.staff:
			obj=activities.objects.filter(slug=activity_slug).first()
			day=str(datetime.datetime.now().day)
			month=str(datetime.datetime.now().month)
			if (datetime.datetime.now().day<10):
				day='0'+str(datetime.datetime.now().day)
			if (datetime.datetime.now().month<10):
				month='0'+str(datetime.datetime.now().month)
			oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
			oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
			oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
			oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
			oty4=oty1+oty2+oty3+oty
			data={
				"obj":obj,
				"current":datetime.datetime.now().date,
				"cur":str(datetime.datetime.now().year)+"-"+month+"-"+day,
				"oty":oty,
				"oty1":oty1,
				"oty2":oty2,
				"oty3":oty3,
				"oty4":oty4
			}
			if request.POST.get('date'):
				date=parse_date(request.POST.get('date'))
				obj.actual_date=date
				tentative_date=request.POST.get('tentative_date')
				# if tentative_date:
				# 	obj.tentative_date=tentative_date
				status=request.POST.get('status')
				if status:
					obj.status=status
				obj.save()
				out=activity_tentative_date_update(activity=obj,
				order=obj.order)
				# if out:
					# print("\hn\n\n\n\n\n\n\nHere it Works")
				query=detail.objects.filter(staff=True,position='H',staff_category=details.staff_category)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
				query=detail.objects.filter(staff=True,position='M',staff_category=details.staff_category)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
				return redirect("/userdetail/staff_profile/activity/"+str(activity_slug))
			if request.POST.get('status'):
				status=request.POST.get('status')
				if obj.status is None:
					oer=response_time.objects.filter(user=details,date__day=datetime.datetime.now().day,
						date__month=datetime.datetime.now().month,
						date__year=datetime.datetime.now().year)
					d0=datetime.date(obj.created_on.year,obj.created_on.month,obj.created_on.day)
					d1=datetime.date(datetime.datetime.now().year,
						datetime.datetime.now().month,
						datetime.datetime.now().day)
					delta=d1-d0
					if oer.count()>0:
						oer=oer.first()
						oer.response_tm=(oer.response_tm_total+int(delta.days))/(oer.response_var+1)
						oer.response_var=oer.response_var+1
						oer.response_tm_total=oer.response_tm_total+int(delta.days)
						oer.save()
					else:
						oer=response_time(
							user=details,
							response_tm=int(delta.days),
							response_tm_total=int(delta.days),
							response_var=1)
						oer.save()
				obj.status=status
				obj.save()
				query=detail.objects.filter(staff=True,position='H',staff_category=details.staff_category)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
				query=detail.objects.filter(staff=True,position='M',staff_category=details.staff_category)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
			if request.POST.get('custom_lap'):
				custom_lap=int(request.POST.get('custom_lap'))
				obj=activities.objects.filter(slug=activity_slug).first()
				out=custom_date_check(obj.activity_Cate,obj.order,lap=custom_lap)
				# obj.lap=int(request.POST.get('custom_lap'))
				# obj.custom_date=obj.created_on+datetime.timedelta(days=obj.lap)
				# owq=activities_Category.objects.filter(linked_activity=obj.activity_Cate)
				# print(owq)
				# for o in owq:
				# 	owqt=activities.objects.filter(user=details,activity_Cate=o,order=obj.order)
				# 	print(owqt)
				# 	if owqt.count()>0:
				# 		owqt=owqt.first()
				# 		if owqt.lap is None:
				# 			owqt.lap=0
				# 		owqt.lap=obj.lap+owqt.activity_Cate.Increment_or_Decrement
				# 		owqt.custom_date=owqt.created_on+datetime.timedelta(days=owqt.lap)
				# 		owqt.save()
				# obj.save()
				if out:
					print("\n\n\n\n\n\n\n\n\n\nHere Our Code Works")
				return redirect("/userdetail/staff_profile/activity/"+str(activity_slug))

			return render(request,"userdetail/staff_profile_activity.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')








def sample(request):
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.staff:
			pass
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')






def show_other_seller(request,email):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		sf=staff_Categories.objects.filter(name="Merchandising").first()
		if (details.staff and details.staff_category==sf and details.position=='H') or details.vendor:
			details=detail.objects.get(email=email)
			label=labels.objects.filter(vendor=details)
			fit=fits.objects.filter(vendor=details)
			season=seasons.objects.filter(vendor=details)
			meas=measurement.objects.filter(user=details)[:5]
			pro=product.objects.filter(seller=details)
			activate_account=False
			if not(details.activate_Seller):
				activate_account=True
			data={
			"deactivated":False,
			"data":details,
			"label":label,
			"fit":fit,
			"season":season,
			"season_fit":None,
			"meas":meas,
			"orders":pro,
			"activate":activate_account
			}
			if request.POST:
				if request.POST.get("activate")=="on":
					details.activate_Seller=True
				details.save()
				return redirect('/userdetail/staff_profile')
			return render(request,'userdetail/show_other_seller.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')






def activities_order(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		sales=staff_Categories.objects.filter(name='Sales').first()
		if details.staff and details.staff_category==sales:
			data={
				'activities':activities_Category.objects.all().order_by('sequence')
			}
			if request.POST.get('acti_ajax_moveup'):
				acti_id=int(request.POST.get('acti_ajax_moveup'))
				objs=activities_Category.objects.filter(sequence=acti_id).first()
				if acti_id<=1:
					pass
				else:
					objs1=activities_Category.objects.filter(sequence=acti_id-1).first()
					objs.sequence=acti_id-1
					objs1.sequence=acti_id
					objs.save()
					objs1.save()
				objs=activities_Category.objects.all().order_by('sequence')
				bol=False
				if objs.count()>0:
					bol=True
				obj1=list(objs.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('acti_ajax_movedown'):
				acti_id=int(request.POST.get('acti_ajax_movedown'))
				objs=activities_Category.objects.filter(sequence=acti_id).first()
				objd=activities_Category.objects.all().count()
				if acti_id>=objd:
					pass
				else:
					objs1=activities_Category.objects.filter(sequence=acti_id+1).first()
					objs.sequence=acti_id+1
					objs1.sequence=acti_id
					objs.save()
					objs1.save()
				objs=activities_Category.objects.all().order_by('sequence')
				bol=False
				if objs.count()>0:
					bol=True
				obj1=list(objs.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			return render(request,'userdetail/activities_order.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


















def create_production(request,order_no):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		stf=staff_Categories.objects.filter(name="Merchandising").first()
		if details.staff and details.position=='H' and details.staff_category==stf:
			order=company_Order.objects.filter(order_no=order_no)
			if order.count()>0:
				order=order.first()
				objs=production_order.objects.filter(order=order).order_by('-production_no')
				final=1
				if objs.count()>0:
					final=objs.first().production_no+1
				obj=production_order(
					order=order,
					production_no=final,
					is_csv=False,
					time=timezone.now(),
					)
				obj.save()
				objf=quantity_b2b.objects.filter(order=order,production=False,is_csv=False)
				for i in objf:
					i.production=True
					i.save()
					obj.sizes.add(i)
				obj.save()
				return redirect('/userdetail/staff_profile/orders/'+str(order_no))
			else:
				return redirect('/userdetail/staff_profile')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


def csv_create_production(request,order_no):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		stf=staff_Categories.objects.filter(name="Merchandising").first()
		if details.staff and details.position=='H' and details.staff_category==stf:
			order=company_Order.objects.filter(order_no=order_no)
			if order.count()>0:
				order=order.first()
				objs=production_order.objects.filter(order=order).order_by('-production_no')
				final=1
				if objs.count()>0:
					final=objs.first().production_no+1
				obj=production_order(
					order=order,
					production_no=final,
					is_csv=True,
					time=timezone.now(),
					)
				obj.save()
				objf=quantity_b2b.objects.filter(order=order,production=False,is_csv=True)
				for i in objf:
					i.production=True
					i.save()
					obj.sizes.add(i)
				obj.save()
				return redirect('/userdetail/staff_profile/orders/'+str(order_no))
			else:
				return redirect('/userdetail/staff_profile')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


'''def cum_create_production(request,order_no):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		stf=staff_Categories.objects.filter(name="Merchandising").first()
		if details.staff and details.position=='H' and details.staff_category==stf:
			order=company_Order.objects.filter(order_no=order_no)
			if order.count()>0:
				order=order.first()
				objs=production_order.objects.filter(order=order).order_by('-production_no')
				final=1
				if objs.count()>0:
					final=objs.first().production_no+1
				obj=production_order(
					order=order,
					production_no=final
					)
				obj.save()
				objf=quantity_b2b.objects.filter(order=order,production=False)
				for i in objf:
					i.production=True
					i.save()
					obj.sizes.add(i)
				obj.save()
				return redirect('/userdetail/staff_profile/orders/'+str(order_no))
			else:
				return redirect('/userdetail/staff_profile')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')'''


from b2b.models import custom_Form_Attribute,custom_Form,custom_Form_Data



def create_packinglist(request,order_no):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		stf=staff_Categories.objects.filter(name="Merchandising").first()
		if details.staff and details.position=='H' and details.staff_category==stf:
			order=company_Order.objects.filter(order_no=order_no)
			if order.count()>0:
				order=order.first()
				objs=packing_list_1.objects.filter(order=order).order_by('-list_no')
				objs1=balance_list_2.objects.filter(order=order).order_by('-list_no')
				final=1
				balance_final=1
				if objs.count()>0:
					final=objs.first().list_no+1
				if objs1.count()>0:
					balance_final=objs1.first().list_no+1
				obj=packing_list_1(
					order=order,
					list_no=final,

					)
				obj1 = balance_list_2(
					order=order,
					list_no=balance_final,

				)
				obj.save()
				obj1.save()
				objf=quantity_b2b.objects.filter(order=order,production=True,packing=False)
				for i in objf:
					s=balance_quantity_b2b(order=i.order,size_label=i.size_label,quantity=i.quantity,production=True,packing=False,color=i.color,address=i.address)
					s.save()

				balance_objf=balance_quantity_b2b.objects.filter(order=order,production=True,packing=False)
				for i in objf:

					i.packing=True
					i.save()
					obj.sizes.add(i)


				for i in balance_objf:

					i.packing=True
					i.save()

					obj1.sizes.add(i)
				obj.save()
				obj1.save()
				return redirect('/userdetail/staff_profile/orders/'+str(order_no))
			else:
				return redirect('/userdetail/staff_profile')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def vendor_profile_orders(request,order_no=None,*args,**kwargs):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			orders=company_Order.objects.filter(staffs_Allocated=details,order_no=order_no)
			if orders.count()>0:
				ohj=quantity_b2b.objects.filter(order=orders.first(),production=False)
				order=orders.first()
				order_bool=False
				enquiry_bool=False
				sample_bool=False
				design_bool=False
				size_bool=False
				head=False
				manager=False
				staff=True
				if order.order_type=='O':
					order_bool=True
				elif order.order_type=='E':
					enquiry_bool=True
				elif order.order_type=='S':
					sample_bool=True
				else:
					design_bool=True
				if ohj.count()>0:
					size_bool=True
				ghj=None
				cum=None
				merch=None
				merch_alloted=None
				garment=None
				garment_alloted=None

				sta1=company_Order.objects.filter(order_no=order.order_no).first()
				li=[]
				for o in sta1.staffs_Allocated.all():
					xfg=activities.objects.filter(user=o,order=order)
					if xfg.count()>0:
						li.append(xfg)
				kjh=production_order.objects.filter(order=order).order_by('production_no')
				fab_obj=seller_Categories.objects.filter(name='Fabric Vendor').first()
				fab_obj=detail.objects.filter(vendor=True,seller_category=fab_obj)
				log_obj=seller_Categories.objects.filter(name='Logistic Vendor').first()
				log_obj=detail.objects.filter(vendor=True,seller_category=log_obj)
				pack_obj=seller_Categories.objects.filter(name='Packing Trims Vendor').first()
				pack_obj=detail.objects.filter(vendor=True,seller_category=pack_obj)
				fin_obj=seller_Categories.objects.filter(name='Finishing Trims Vendor').first()
				fin_obj=detail.objects.filter(vendor=True,seller_category=fin_obj)
				sew_obj=seller_Categories.objects.filter(name='Sewing Trims Vendor').first()
				sew_obj=detail.objects.filter(vendor=True,seller_category=sew_obj)
				is_gare=False
				oyu=seller_Categories.objects.filter(name="Garmenting Vendor").first()
				boms_obj=None
				if details.seller_category==oyu:
					is_gare=True
					boms_obj=bom.objects.filter(order=order).first()
				forms=custom_Form.objects.filter(seller_category=details.seller_category)
				obj_priority=priority_of_order.objects.filter(user=details,order=order).first()
				if not(obj_priority):
					obj_priority_no=0
				else:
					obj_priority_no=obj_priority.priority_no
				cnt_per=None
				if details.seller_category==seller_Categories.objects.filter(name="Garmenting Vendor").first():
					oij=staff_Categories.objects.filter(name="Merchandising").first()
					cnt_per=order.staffs_Allocated.filter(staff=True,position='H',staff_category=oij).first()
				else:
					oij=seller_Categories.objects.filter(name="Garmenting Vendor").first()
					cnt_per=order.staffs_Allocated.filter(vendor=True,seller_category=oij).first()
				# oij=staff_Categories.objects.filter(name="Sales").first()
				# cnt_per=order.staffs_Allocated.filter(staff=True,position='C',staff_category=oij).first()
				customer=detail.objects.filter(email=order.user_email).first()
				measu=None
				if order.fashion_Brand and order.label and order.fit and order.season:
					measu=measurement.objects.filter(
							user=order.fashion_Brand,
							label=order.label,
							fit=order.fit,
							season=order.season
						).first().slug
				li=activities.objects.filter(order=order).order_by('activity_Cate')
				asd=activities.objects.filter(order=order).order_by('activity_Cate')
				macro_acti=[]
				random_acti=[]
				for i in asd:
					objs458=macro_Activities.objects.filter(activities=i.activity_Cate)
					for j in objs458:
						if j not in random_acti:
							random_acti.append(j)
							macro_acti.append([j,[i]])
						else:
							indi=random_acti.index(j)
							macro_acti[indi][1].append(i)
				macro_acti=sorted(macro_acti,key=lambda x:x[0].id)
				order_section=orders_permission.objects.filter(staff_category=details.staff_category).first()
				if order_section:
					order_section=order_section.allowed_section.all().filter(order_section=True)
				else:
					order_section=['Order_Description']
				data={
					"order_no":order_no,
					"order":order,
					"quan":ohj,
					"enquiry_bool":enquiry_bool,
					"order_bool":order_bool,
					"sample_bool":sample_bool,
					"design_bool":design_bool,
					"size_bool":size_bool,
					"head":head,
					"manager":manager,
					"staff":staff,
					"obj":ghj,
					"cum":cum,
					"merch":merch,
					"merch_alloted":merch_alloted,
					"garment":garment,
					"garment_alloted":garment_alloted,
					"acti":li,
					"current":datetime.datetime.now().date,
					"prd":kjh,
					"fab_obj":fab_obj,
					"log_obj":log_obj,
					"fin_obj":fin_obj,
					"sew_obj":sew_obj,
					"pack_obj":pack_obj,
					"is_gare":is_gare,
					"boms_obj":boms_obj,
					"forms":forms,
					"obj_priority":obj_priority_no,
					"cnt":cnt_per,
					"customer":customer,
					"measu":measu,
					"macro_acti":macro_acti,
					"details":details,
					"order_section":order_section
				}
				if details.is_logistics_vendor:
					print("khghfg")
					sel_c=seller_Categories.objects.filter(name="Logistics Driver").first()
					logi_driver=detail.objects.filter(seller_category=sel_c)
					data["logi_driver"]=logi_driver
				if details.is_driver:
					acti_logi=activities_Category.objects.filter(title="Logistics Pickup").first()
					activ=activities.objects.filter(activity_Cate=acti_logi,order=order)
					data["activ"]=activ
				if request.POST.get('star_click_ajax'):
					star=int(request.POST.get('star_click_ajax'))
					if not(obj_priority):
						obj_priority=priority_of_order(
							user=details,
							order=order
							)
					else:
						order.priority_no=order.priority_no-obj_priority.priority_no
						order.priority_quantity=order.priority_quantity-1
					obj_priority.priority_no=star
					obj_priority.save()
					order.priority_no=order.priority_no+star
					order.priority_quantity=order.priority_quantity+1
					order.overall_priority=round(order.priority_no/order.priority_quantity,2)
					order.save()
					return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
				fab_obj=seller_Categories.objects.filter(name='Fabric Vendor').first()
				log_obj=seller_Categories.objects.filter(name='Logistic Vendor').first()
				pack_obj=seller_Categories.objects.filter(name='Packing Trims Vendor').first()
				fin_obj=seller_Categories.objects.filter(name='Finishing Trims Vendor').first()
				sew_obj=seller_Categories.objects.filter(name='Sewing Trims Vendor').first()
				if request.POST.get('logi_to_driver'):
					staff_to=request.POST.get('logi_to_driver')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=fab_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/vendor_profile')
				if request.POST.get('gar_to_fab'):
					staff_to=request.POST.get('gar_to_fab')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=fab_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/vendor_profile')
				if request.POST.get('gar_to_log'):
					staff_to=request.POST.get('gar_to_log')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=log_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/vendor_profile')
				if request.POST.get('gar_to_fin'):
					staff_to=request.POST.get('gar_to_fin')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=fin_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/vendor_profile')
				if request.POST.get('gar_to_sew'):
					staff_to=request.POST.get('gar_to_sew')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=sew_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/vendor_profile')
				if request.POST.get('gar_to_pack'):
					staff_to=request.POST.get('gar_to_pack')
					staff_to=detail.objects.get(email=staff_to)
					order.staffs_Allocated.add(staff_to)
					order.save()
					objs1=staff_to
					noti_oj=notifications(
						title="New Order Placed Please Complete the Activities("+str(order_no)+") !",
						description="Complete the Activities",
						user=objs1,
						link="/userdetail/vendor_profile/orders/"+str(order_no),
						type_of_order=order.order_type)
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						type_of_order=order.order_type,seller_category=pack_obj)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=objs1,
							slug=str(objs1)+"_"+str(j)+"_"+str(order_no),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=j.completed_in),
							prev_lap=lead_time)
						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(objs1,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()
					return redirect('/userdetail/vendor_profile')
				if request.POST.get('color_ajax_label'):
					obj1=color_model.objects.filter(name__icontains=request.POST.get('color_ajax_label'))
					if obj1.count()>0:
						bol=True
					else:
						bol=False
					obj1=list(obj1.values())
					return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
				if request.POST.get('colo'):
					obj1=color_model.objects.filter(name=request.POST.get('colo'))
					if obj1.count()>0:
						order.colors_avail.add(obj1.first())
					else:
						obj1=color_model(
							name=request.POST.get('colo')
							)
						obj1.save()
						order.colors_avail.add(obj1)
					order.save()

				return render(request,"vendor/vendor_profile_orders.html",data)
			else:
				return redirect('/userdetail/staff_profile')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



from Garmenting_Vendor.models import production_Product,production_Line,production_Daily_Update
from calendar import monthrange



def vendor_profile(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		try:
			details=detail.objects.get(email=request.user.email)
		except:
			return redirect('/?unauth=True')
		sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
		if details.vendor and not(details.seller_category==sel_cate):
			deactivated=True
			if details.activate_Seller:
				deactivated=False
			noti=notifications.objects.filter(user=details).order_by('-created_on')
			acti=activities.objects.filter(user=details)
			orders=company_Order.objects.filter(staffs_Allocated=details)
			li=[]
			for o in orders:
				li.append(activities.objects.filter(user=details,order=o,actual_date=None))
			other=False
			sele_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
			sele_cate1=seller_Categories.objects.filter(name='Logistic Vendor').first()
			if details.seller_category!=sele_cate and details.seller_category!=sele_cate1:
				other=True
			# print(other)
			prod=trims_product.objects.filter(seller=details)
			is_gare=False
			if details.seller_category==sele_cate1:
				is_gare=True
			qwe=floated_orders.objects.filter(to_user=details)
			oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
			oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
			oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
			oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
			oty4=oty1+oty2+oty3+oty
			current_year=datetime.datetime.now().year
			if request.GET.get('budget_year'):
				current_year=int(request.GET.get('budget_year'))
			months_wise_budget=[]
			for i in range(1,13):
				orders=company_Order.objects.filter(order_date_time__year=current_year,order_date_time__month=i)
				val=0
				for j in orders:
					val+=j.get_billing_amount
				months_wise_budget.append(val)
			pr_line=[]
			for i in production_Product.objects.filter(user=details):
				pr_line.append([i.id,i.product_Category.name+" "+i.product_Supercategory.name])
			pr_obj=production_Product.objects.filter(user=details).first()
			if request.GET.get('dpr_filter'):
				pr_obj=production_Product.objects.filter(id=request.GET.get('dpr_filter')).first()
			start_date,end_date=monthrange(datetime.datetime.now().year,datetime.datetime.now().month)
			print(start_date)
			pro_graph=[]
			for i in range(1,end_date+1):
				obj=production_Daily_Update.objects.filter(date_update__day=i,date_update__month=datetime.datetime.now().month,
					date_update__year=datetime.datetime.now().year,production_obj=pr_obj,user=details).last()
				if obj and obj.quantity:
					pro_graph.append(obj.quantity)
				else:
					pro_graph.append(0)
			print(pro_graph)
			data={
				"pro_graph":pro_graph,
				"pro_obj":pr_obj,
				"end_date":end_date,
				"month":datetime.datetime.now().month,
				"year":datetime.datetime.now().year,
				"pr_lines":pr_line,
				"current_year":current_year,
				"months_wise_budget":months_wise_budget,
				"data":details,
				"deactivated":deactivated,
				"noti":noti,
				"acti":li,
				"ord":orders,
				"oth":other,
				"prod":prod,
				"is_gare":is_gare,
				"qwe":qwe,
				"oty":oty,
				"oty1":oty1,
				"oty2":oty2,
				"oty3":oty3,
				"oty4":oty4
			}

			if request.POST.get('up_budget'):
				details.budget_hit_rate=request.POST.get('up_budget')
				details.save()
			if request.POST.get('up_dpr'):
				pro_obj=production_Product.objects.filter(id=request.POST.get('production_line')).first()
				if pro_obj:
					pro_update=production_Daily_Update.objects.filter(date_update=datetime.datetime.now(),
						production_obj=pro_obj,user=details).last()
					if not(pro_update):
						pro_update=production_Daily_Update(date_update=datetime.datetime.now(),production_obj=pro_obj,
							user=details)
					print(datetime.datetime.now())
					pro_update.quantity=request.POST.get('up_dpr')
					pro_update.save()
			return render(request,'vendor/vendor_profile.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')







def vendor_notifications(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			noti=notifications.objects.filter(user=details).order_by('-created_on')

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
			"oty":oty,
			"oty1":oty1,
			"oty2":oty2,
			"oty3":oty3,
			"oty4":oty4
			}
			return render(request,"vendor/vendor_notifications.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')








def vendor_profile_activity(request,activity_slug):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.vendor:
			obj=activities.objects.filter(slug=activity_slug).first()
			day=str(datetime.datetime.now().day)
			month=str(datetime.datetime.now().month)
			if (datetime.datetime.now().day<10):
				day='0'+str(datetime.datetime.now().day)
			if (datetime.datetime.now().month<10):
				month='0'+str(datetime.datetime.now().month)
			data={
			"obj":obj,
			"current":datetime.datetime.now().date,
			"cur":str(datetime.datetime.now().year)+"-"+month+"-"+day,
			"logistic":False
			}
			sel_cate=seller_Categories.objects.filter(name="Logistic Vendor").first()
			if details.seller_category==sel_cate:
				data["logistic"]=True
			if request.POST.get('date'):
				date=parse_date(request.POST.get('date'))
				obj.actual_date=date
				obj.save()
				merch=staff_Categories.objects.filter(name="Merchandising").first()
				query=detail.objects.filter(staff=True,position='H',staff_category=merch)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
				return redirect('/userdetail/vendor_profile')
			if request.POST.get('status'):
				obj.status=request.POST.get('status')
				obj.save()
				merch=staff_Categories.objects.filter(name="Merchandising").first()
				query=detail.objects.filter(staff=True,position='H',staff_category=merch)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
				return redirect('/userdetail/vendor_profile')
			if request.POST.get('custom_lap'):
				obj.lap=int(request.POST.get('custom_lap'))
				print(obj.custom_date)
				obj.custom_date=obj.created_on+datetime.timedelta(days=obj.lap)
				print(obj.custom_date)
				obj.save()
				return redirect('/userdetail/vendor_profile')

			return render(request,"userdetail/staff_profile_activity.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




from b2b.models import activity_sub_status



def vendor_profile_activity_by_id(request,activity_slug):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.vendor:
			obj=activities.objects.filter(id=int(activity_slug)).first()
			day=str(datetime.datetime.now().day)
			month=str(datetime.datetime.now().month)
			if (datetime.datetime.now().day<10):
				day='0'+str(datetime.datetime.now().day)
			if (datetime.datetime.now().month<10):
				month='0'+str(datetime.datetime.now().month)
			data={
			"obj":obj,
			"current":datetime.datetime.now().date,
			"cur":str(datetime.datetime.now().year)+"-"+month+"-"+day,
			"logistic":False,
			"details":details
			}
			if details.is_driver and request.POST.get('sub_status'):
				status=activity_sub_status(user=details,acti=obj,sub_status=request.POST.get('sub_status'))
				status.save()
				return redirect('/userdetail/vendor_profile/activity/'+str(activity_slug))
			sel_cate=seller_Categories.objects.filter(name="Logistic Vendor").first()
			if details.seller_category==sel_cate:
				data["logistic"]=True
			if request.POST.get('date'):
				date=parse_date(request.POST.get('date'))
				obj.actual_date=date
				obj.save()
				merch=staff_Categories.objects.filter(name="Merchandising").first()
				query=detail.objects.filter(staff=True,position='H',staff_category=merch)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
				return redirect('/userdetail/vendor_profile')
			if request.POST.get('status'):
				obj.status=request.POST.get('status')
				obj.save()
				merch=staff_Categories.objects.filter(name="Merchandising").first()
				query=detail.objects.filter(staff=True,position='H',staff_category=merch)
				query=query.exclude(email=details.email)
				for i in query:
					a=notifications(
						title="Activity is Updated by"+str(details.name),
						description="This Activity is updated by the user("+str(details.email)+")",
						user=i,
						link="/userdetail/staff_profile/activity/"+str(activity_slug)
						)
					a.save()
					a.link=a.link+"?noti="+str(a.id)
					a.save()
				return redirect('/userdetail/vendor_profile')
			if request.POST.get('custom_lap'):
				obj.lap=int(request.POST.get('custom_lap'))
				print(obj.custom_date)
				obj.custom_date=obj.created_on+datetime.timedelta(days=obj.lap)
				print(obj.custom_date)
				obj.save()
				return redirect('/userdetail/vendor_profile')

			return render(request,"userdetail/staff_profile_activity.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')







def custom_date_check(activity,order,lap):
	activity1=activities.objects.filter(activity_Cate=activity,order=order).first()
	linked=activity.linked_activity
	if linked:
		linked=activities.objects.filter(activity_Cate=linked,
		order=order).first()
	if linked:
		prev_date=linked.custom_date
		if not(prev_date):
			prev_date=linked.planned_date
		if not(prev_date):
			prev_date=order.created_on
	else:
		prev_date=order.order_date_time
	if activity1:
		if lap:
			activity1.lap=lap
			activity1.custom_date=getPlannedDate(activity1.user,prev_date,lap)
			# activity1.custom_date=prev_date+datetime.timedelta(days=lap)
		else:
			activity1.lap=activity1.prev_lap
			activity1.custom_date=getPlannedDate(activity1.user,prev_date,activity1.prev_lap)
			# activity1.custom_date=prev_date+datetime.timedelta(days=activity1.prev_lap)
		activity1.save()
	to_others=activities_Category.objects.filter(linked_activity=activity)
	for i in to_others:
		custom_date_check(i,order,lap=None)
	return True







def activities_page(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		orders=company_Order.objects.filter(staffs_Allocated=details)
		acti=activities.objects.filter(user=details)
		li=[]
		logi_per=False
		if details.staff_category.name=="Logistic":
			logi_per=True
		acti_obj=activities_Category.objects.filter(title="Logistics Pickup").first()
		# print(logi_per,acti_obj.title)
		for o in orders:
			hgf_acti=activities.objects.filter(user=details,order=o)
			length=0
			breadth=0
			height=0
			vol=0
			if logi_per:
				hgf_acti=activities.objects.filter(activity_Cate=acti_obj,order=o)
				car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
				length=car.length
				breadth=car.breadth
				height=car.heigth
				vol=length*breadth*height
				if hgf_acti.count()>0:
					li.append([hgf_acti,length,breadth,height,vol])
			else:
				if hgf_acti.count()>0:
					li.append(hgf_acti)
		# print(li)
		oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
		oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
		oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
		oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
		oty4=oty1+oty2+oty3+oty
		print(oty4)
		data={
			"deactivated":True,
			"data":details,
			"obj":None,
			"head":False,
			"staff":False,
			"manager":False,
			"acti":li,
			"current":datetime.datetime.now().date,
			"oty":oty,
			"oty1":oty1,
			"oty2":oty2,
			"oty3":oty3,
			"oty4":oty4,
			"logistics":logi_per
		}
		if details.staff or details.vendor:
			if details.activate_Staff and not(details.vendor):
				data["deactivated"]=False
			if request.GET.get('filter'):
				filter_by=request.GET.get('filter')
				if filter_by=='today':
					li=[]
					for o in orders:
						hgf_acti=activities.objects.filter(user=details,order=o,planned_date__day=datetime.datetime.now().day,
							planned_date__month=datetime.datetime.now().month,
							planned_date__year=datetime.datetime.now().year)
						if hgf_acti.count()>0:
							li.append(hgf_acti)
					data["acti"]=li
				if filter_by=='pending':
					li=[]
					for o in orders:
						hgf_acti=activities.objects.filter(user=details,order=o,planned_date__day__lt=datetime.datetime.now().day,
							planned_date__month=datetime.datetime.now().month,
							planned_date__year=datetime.datetime.now().year)
						if hgf_acti.count()>0:
							li.append(hgf_acti)
					data["acti"]=li
				if filter_by=='enquiry':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='E')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						if hgf_acti.count()>0:
							li.append(hgf_acti)
					data["acti"]=li
				if filter_by=='sampling':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='S')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						if hgf_acti.count()>0:
							li.append(hgf_acti)
					data["acti"]=li
				if filter_by=='design':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='D')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						if hgf_acti.count()>0:
							li.append(hgf_acti)
					data["acti"]=li
				if filter_by=='order':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='O')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						if hgf_acti.count()>0:
							li.append(hgf_acti)
					data["acti"]=li
			if request.POST.get('lap_activity_ajax'):
				lap=int(request.POST.get('lap_activity_ajax'))
				acti=int(request.POST.get('activity_ajax_cate'))
				obj=activities.objects.filter(id=acti).first()
				# obj.lap=lap
				# obj.custom_date=obj.created_on+datetime.timedelta(days=obj.lap)
				# owq=activities_Category.objects.filter(linked_activity=obj.activity_Cate)
				# for o in owq:
				# 	owqt=activities.objects.filter(user=details,activity_Cate=o,order=obj.order)
				# 	# print(owqt)
				# 	if owqt.count()>0:
				# 		owqt=owqt.first()
				# 		if owqt.lap is None:
				# 			owqt.lap=0
				# 		owqt.lap=obj.lap+owqt.activity_Cate.Increment_or_Decrement
				# 		owqt.custom_date=owqt.created_on+datetime.timedelta(days=owqt.lap)
				# 		owqt.save()
				# obj.save()
				custom_date_check(activity=obj.activity_Cate,order=obj.order,lap=lap)
				return HttpResponse(json.dumps({"bol":True}), content_type="application/json")
			if request.POST.get('actual_date_activity_ajax'):
				actual_date=parse_date(request.POST.get('actual_date_activity_ajax'))
				acti=int(request.POST.get('activity_ajax_cate'))
				obj=activities.objects.filter(id=acti).first()
				obj.actual_date=actual_date
				obj.save()
				out=activity_tentative_date_update(activity=obj,
				order=obj.order)
				oer=response_time.objects.filter(user=details,date__day=datetime.datetime.now().day,
					date__month=datetime.datetime.now().month,
					date__year=datetime.datetime.now().year)
				d0=datetime.date(obj.created_on.year,obj.created_on.month,obj.created_on.day)
				d1=datetime.date(datetime.datetime.now().year,
					datetime.datetime.now().month,
					datetime.datetime.now().day)
				delta=d1-d0
				if oer.count()>0:
					oer=oer.first()
					oer.response_tm=(oer.response_tm_total+int(delta.days))/(oer.response_var+1)
					oer.response_var=oer.response_var+1
					oer.response_tm_total=oer.response_tm_total+int(delta.days)
					oer.save()
				else:
					oer=response_time(
						user=details,
						response_tm=int(delta.days),
						response_tm_total=int(delta.days),
						response_var=1)
					oer.save()
			if request.POST.get('lr_activity_ajax'):
				lr=int(request.POST.get('lr_activity_ajax'))
				acti=int(request.POST.get('activity_ajax_cate'))
				obj=activities.objects.filter(id=acti).first()
				obj.lr_number=lr
				obj.save()
				return HttpResponse(json.dumps({"bol":True}), content_type="application/json")
				# if out:
					# print("\hn\n\n\n\n\n\n\nHere it Works")
				# query=detail.objects.filter(staff=True,position='H',staff_category=details.staff_category)
				# query=query.exclude(email=details.email)
				# for i in query:
				# 	a=notifications(
				# 		title="Activity is Updated by"+str(details.name),
				# 		description="This Activity is updated by the user("+str(details.email)+")",
				# 		user=i,
				# 		link="/userdetail/staff_profile/activity/"+str(obj.slug)
				# 		)
				# 	a.save()
				# 	a.link=a.link+"?noti="+str(a.id)
				# 	a.save()
				# query=detail.objects.filter(staff=True,position='M',staff_category=details.staff_category)
				# query=query.exclude(email=details.email)
				# for i in query:
				# 	a=notifications(
				# 		title="Activity is Updated by"+str(details.name),
				# 		description="This Activity is updated by the user("+str(details.email)+")",
				# 		user=i,
				# 		link="/userdetail/staff_profile/activity/"+str(activity_slug)
				# 		)
				# 	a.save()
				# 	a.link=a.link+"?noti="+str(a.id)
				# 	a.save()
				return HttpResponse(json.dumps({"bol":True}), content_type="application/json")
			return render(request,'userdetail/activities_page.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


# if request.POST.get('custom_lap'):
# 				obj.lap=int(request.POST.get('custom_lap'))
# 				obj.custom_date=obj.created_on+datetime.timedelta(days=obj.lap)
# 				owq=activities_Category.objects.filter(linked_activity=obj.activity_Cate)
# 				print(owq)
# 				for o in owq:
# 					owqt=activities.objects.filter(user=details,activity_Cate=o,order=obj.order)
# 					print(owqt)
# 					if owqt.count()>0:
# 						owqt=owqt.first()
# 						if owqt.lap is None:
# 							owqt.lap=0
# 						owqt.lap=obj.lap+owqt.activity_Cate.Increment_or_Decrement
# 						owqt.custom_date=owqt.created_on+datetime.timedelta(days=owqt.lap)
# 						owqt.save()
# 				obj.save()



def staffs_under_page(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.staff:
			staff_cate=details.staff_category
			mana=detail.objects.filter(staff=True,staff_category=staff_cate,position='M')
			staf=detail.objects.filter(staff=True,staff_category=staff_cate,position='C')
			oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
			oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
			oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
			oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
			oty4=oty1+oty2+oty3+oty
			data={
				"obj":mana,
				"obj1":staf,
				"oty":oty,
				"oty1":oty1,
				"oty2":oty2,
				"oty3":oty3,
				"oty4":oty4
			}
			print(data)
			return render(request,'userdetail/staffs_under_page.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def b2b_customer_staff(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.staff:
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
			return render(request,'userdetail/b2b_customer_staff.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def vendor_staff(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		if details.staff:
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
			return render(request,'userdetail/vendor_staff.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def orders_clubbed_filter(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			b2b_cust=detail.objects.filter(buisness_Customer=True)
			sales_filter=staff_Categories.objects.filter(name="Sales").first()
			merch_filter=staff_Categories.objects.filter(name="Merchandising").first()
			gmt_filter=seller_Categories.objects.filter(name="Garmenting Vendor").first()
			fab_filter=seller_Categories.objects.filter(name="Fabric Vendor").first()

			billing_months=[]
			months={
				1:"Jan",
				2:"Feb",
				3:"Mar",
				4:"Apr",
				5:"May",
				6:"Jun",
				7:"Jul",
				8:"Aug",
				9:"Sep",
				10:"Oct",
				11:"Nov",
				12:"Dec"
			}
			orders5=company_Order.objects.filter(staffs_Allocated=details).order_by('order_date_time')
			for i in orders5:
				# obj=activities.objects.filter(order=i).order_by('-planned_date').first()
				obj=i.get_billing_month()
				if obj:
					if not((str(months[obj.month])+" "+str(obj.year)) in billing_months):
						billing_months.append(str(months[obj.month])+" "+str(obj.year))
			# print(billing_months)
			data={
				"b2b_cust":detail.objects.filter(buisness_Customer=True),
				"sales":detail.objects.filter(staff=True,staff_category=sales_filter),
				"merchant":detail.objects.filter(staff=True,staff_category=merch_filter),
				"gmt":detail.objects.filter(vendor=True,seller_category=gmt_filter),
				"fab_vendor":detail.objects.filter(vendor=True,seller_category=fab_filter),
				"bill":billing_months
			}
			return render(request,'userdetail/orders_clubbed_filter.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')






def orders_clubbed(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			acti_cate=activities_Category.objects.all()
			orders=company_Order.objects.filter(staffs_Allocated=details).order_by('order_date_time')
			li=[]
			li1=[]
			li2=[]
			macro_Acti=macro_Activities.objects.all()
			if request.GET:
				orders=company_Order.objects.filter(staffs_Allocated=details).order_by('order_date_time')
				if request.GET.get('b2b'):
					orders=orders.filter(user_email=request.GET.get('b2b')).order_by('order_date_time')
				if request.GET.get('sales'):
					sales_hji=detail.objects.filter(email=request.GET.get('sales')).first()
					orders=orders.filter(staffs_Allocated=sales_hji)
				if request.GET.get('merchant'):
					merchant_hji=detail.objects.filter(email=request.GET.get('merchant')).first()
					orders=orders.filter(staffs_Allocated=merchant_hji)
				if request.GET.get('gmt'):
					gmt_hji=detail.objects.filter(email=request.GET.get('gmt')).first()
					orders=orders.filter(staffs_Allocated=gmt_hji)
				if request.GET.get('fab_vendor'):
					fab_vendor_hji=detail.objects.filter(email=request.GET.get('fab_vendor')).first()
					orders=orders.filter(staffs_Allocated=fab_vendor_hji)
				if request.GET.get('status'):
					pass
				if request.GET.get('order_type'):
					orders=orders.filter(order_type=request.GET.get('order_type'))
					macro_Acti=macro_Acti.filter(type_of_activity=request.GET.get('order_type'))
				if request.GET.get('bill'):
					reverse_month={
					"Jan":1,
					"Feb":2,
					"Mar":3,
					"Apr":4,
					"May":5,
					"Jun":6,
					"Jul":7,
					"Aug":8,
					"Sep":9,
					"Oct":10,
					"Nov":11,
					"Dec":12
					}

					bill=request.GET.get('bill')
					month,year=map(str,bill.split(" "))
					month=reverse_month[month]
					year=int(year)
					ord=[]
					for i in orders:
						# obj=activities.objects.filter(order=i).order_by('-planned_date').first()
						obj=i.get_billing_month()
						if obj:
							if obj.month==month and obj.year==year:
								ord.append(i)
					orders=ord
			# for i in orders:
			# 	li=[]
			# 	for j in acti_cate:
			# 		obj=activities.objects.filter(activity_Cate=j,order=i).first()
			# 		if obj is not None:
			# 			obj=obj.planned_date
			# 		li.append(obj)
			# 	li1.append(li)
			# li2=zip(orders,li1)
			b2b_cust=detail.objects.filter(buisness_Customer=True)
			sales_filter=staff_Categories.objects.filter(name="Sales").first()
			merch_filter=staff_Categories.objects.filter(name="Merchandising").first()
			gmt_filter=seller_Categories.objects.filter(name="Garmenting Vendor").first()
			fab_filter=seller_Categories.objects.filter(name="Fabric Vendor").first()

			li1=[]
			for i in orders:
				li=[]
				for j in macro_Acti:
					cumao=j.activities.all()
					obj5=activities.objects.filter(activity_Cate=cumao.last(),order=i).first()
					if obj5:
						# li.append({
						# # "custom":obj5.custom_date,
						# # "planned":obj5.planned_date,
						# # "actual":obj5.actual_date,
						# # "tentative":obj5.tentative_date
						# })
						li.append(None)
					else:
						li.append(None)
					for k in j.activities.all():
						obj=activities.objects.filter(activity_Cate=k,order=i).first()

						if obj is not None:
							# obj=obj.planned_date
							li.append({"custom":obj.custom_date,
								"planned":obj.planned_date,
								"actual":obj.actual_date,
								"tentative":obj.tentative_date,
								"micro_id":j.id
							})
						else:
							li.append({"custom":None,
								"planned":None,
								"micro_id":j.id
							})
				li1.append({"order":i,"acti_dates":li})
			billing_months=[]
			months={
				1:"Jan",
				2:"Feb",
				3:"Mar",
				4:"Apr",
				5:"May",
				6:"Jun",
				7:"Jul",
				8:"Aug",
				9:"Sep",
				10:"Oct",
				11:"Nov",
				12:"Dec"
			}
			orders5=company_Order.objects.filter(staffs_Allocated=details).order_by('order_date_time')
			for i in orders5:
				# obj=activities.objects.filter(order=i).order_by('-planned_date').first()
				obj=i.get_billing_month()
				if obj:
					if (str(months[obj.month])+" "+str(obj.year)) not in billing_months:
						billing_months.append(str(months[obj.month])+" "+str(obj.year))
			# print(billing_months)
			data={
				'acti_cate':acti_cate,
				'orders':orders,
				'li':li1,
				"b2b_cust":b2b_cust,
				"sales":detail.objects.filter(staff=True,staff_category=sales_filter),
				"merchant":detail.objects.filter(staff=True,staff_category=merch_filter),
				"gmt":detail.objects.filter(vendor=True,seller_category=gmt_filter),
				"fab_vendor":detail.objects.filter(vendor=True,seller_category=fab_filter),
				"macro":macro_Acti,
				"bill":billing_months
			}
			if request.POST.get('mom_activity_ajax'):
				mom=request.POST.get('mom_activity_ajax')
				act=request.POST.get('activity_ajax_cate')
				obj=company_Order.objects.filter(order_no=int(act)).first()
				# obj.mom=mom
				mom_obj=mom_model(
						order=obj,user=details,message=mom
					)
				mom_obj.save()
				obj.save()
			if request.POST.get('mom_show_ajax'):
				act=request.POST.get('activity_ajax_cate')
				obj=company_Order.objects.filter(order_no=int(act)).first()
				mom_objs=mom_model.objects.filter(order=obj).order_by('time')
				moms=[]
				for i in mom_objs:
					moms.append({
						"name":i.user.name,
						"email":i.user.email,
						"message":i.message,
						"time":str(i.time.year)+"-"+str(i.time.month)+"-"+str(i.time.day)+"  "+str(i.time.hour)+":"+str(i.time.minute)
						})
				# print(moms)
				return JsonResponse({"mom":moms})
			return render(request,'userdetail/orders_clubbed.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




def staff_profile_message(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email)
		if details.count()>0:
			details=details.first()
		else:
			return redirect('/userdetail/logout')
		if details:
			chats=chats_head.objects.filter(user1=details)
			chats1=chats_head.objects.filter(user2=details)
			chats= chats | chats1
			chats.order_by('-last_message_time')
			# print(chats)
			staff_cate=staff_Categories.objects.all()
			data={
			"chats":chats,
			"staff_cate":staff_cate,
			"details":details,
			"chat_id":None,
			"cur":datetime.datetime.now()
			}
			if request.GET.get('user_to') and request.GET.get('message'):
				to_open_chat=request.GET.get('user_to')
				to_open_chat=detail.objects.filter(email=to_open_chat).first()
				if to_open_chat:
					objyut=chats_head.objects.filter(user1=details,user2=to_open_chat).first()
					if not(objyut):
						objyut=chats_head.objects.filter(user1=to_open_chat,user2=details).first()
						if not(objyut):
							objyut=chats_head(user1=details,user2=to_open_chat,
							last_message=request.GET.get('message'),
							last_message_time=datetime.datetime.now())
							objyut.save()
					objyut.last_message=request.GET.get('message')
					objyut.last_message_time=datetime.datetime.now()
					objyut.save()
					sydty=messages_head(chat=objyut,
					message=request.GET.get('message'))
					if objyut.user1==to_open_chat:
						sydty.sent_by_user1=False
						sydty.sent_by_user2=True
					else:
						sydty.sent_by_user1=True
						sydty.sent_by_user2=False
					sydty.save()
					data["chat_id"]=objyut.id
			if request.POST.get('position_ajax_staff'):
				staff_ajax_cate=request.POST.get('staff_ajax_cate')
				position_ajax_staff=request.POST.get('position_ajax_staff')
				if staff_ajax_cate is None:
					obj1=detail.objects.filter(position=position_ajax_staff,staff=True)
				else:
					ort=staff_Categories.objects.filter(name=staff_ajax_cate).first()
					obj1=detail.objects.filter(staff_category=ort,position=position_ajax_staff,staff=True)

				if obj1.count()>0:
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol},default=str), content_type="application/json")

			if request.POST.get('message_ajax'):
				chat_id=request.POST.get('chats_ajax');
				message=request.POST.get('message_ajax')
				chats=chats_head.objects.filter(id=chat_id).first()

				obj1=messages_head(
						chat=chats,
						message=message,
						sent_by_user1=False,
						sent_by_user2=False
					)
				chats.last_message=message
				chats.last_message_time=datetime.datetime.now()
				if chats.user1==details:
					obj1.sent_by_user1=True
				else:
					obj1.sent_by_user2=True
				obj1.save()
				bol=True
				return HttpResponse(json.dumps({'data': obj1,'bol':bol},default=str), content_type="application/json")
			if request.POST.get('message') and request.POST.get('staff'):
				to_email=request.POST.get('staff')
				message=request.POST.get('message')
				to_email=detail.objects.filter(email=to_email).first()
				obj=chats_head(
						user1=details,
						user2=to_email,
						last_message=message,
						last_message_time=datetime.datetime.now()

					)
				obj.save()
				obj1=messages_head(
						chat=obj,
						message=message,
						sent_by_user1=True,
						sent_by_user2=False
					)
				obj1.save()
				return redirect('/userdetail/staff_profile/message')
			if request.POST.get('chats_ajax_id'):
				obj1=messages_head.objects.filter(chat=chats_head.objects.get(id=int(request.POST.get('chats_ajax_id')))).order_by('created_on')
				print(obj1.count())
				if obj1.count()>0:
					bol=True
				else:
					bol=False
				li1=[]
				for a in obj1:
					li={}
					li["message"]=a.message
					li["sent_by_user1"]=a.sent_by_user1
					li["sent_by_user2"]=a.sent_by_user2
					li["created_on"]=a.created_on
					li["user1"]=a.chat.user1.email
					li["user2"]=a.chat.user2.email
					li1.append(li)
				obj1=li1
				return HttpResponse(json.dumps({'data': obj1,'bol':bol},default=str), content_type="application/json")

			return render(request,'userdetail/staff_profile_message.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')







def create_noti_vendor(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			cate=staff_Categories.objects.all()
			data={
				"cate":cate
			}
			return render(request,'userdetail/create_noti_vendor.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def create_noti_staff(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email)
		if details.staff:
			cate=seller_Categories.objects.all()
			data={
				"cate":cate
			}
			return render(request,'userdetail/create_noti_staff.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


from b2b.models import trims_bom


def vendor_profile_bom(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		sel_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		order=company_Order.objects.filter(order_no=order_no).first()
		if (details.vendor and (details.seller_category==sel_cate)) or details.staff and order:
			fabric=trims_product.objects.filter(
				category=trims_Category.objects.filter(fabric=True).first()
			)
			packing=trims_product.objects.filter(
				category=trims_Category.objects.filter(packing=True).first()
			)
			sewing=trims_product.objects.filter(
				category=trims_Category.objects.filter(sewing=True).first()
			)
			finishing=trims_product.objects.filter(
				category=trims_Category.objects.filter(finishing=True).first()
			)
			std_items=trims_product.objects.filter(standard=True,product_Supercategory=order.product_Supercategory)
			data={
				"fabric":fabric,
				"packing":packing,
				"sewing":sewing,
				"finishing":finishing,
				"std_items":std_items
			}
			if request.POST.get('fabric1'):
				obj=bom(
						user=details,
						order=order,
						cutmake_consum=int(request.POST.get('cutmake_cosum')),
						cutmake_rate=int(request.POST.get('cutmake_rate')),
						cutmake_cost=int(request.POST.get('cutmake_cosum'))*int(request.POST.get('cutmake_rate')),
						profit_percentage=int(request.POST.get('profit'))
					)
				obj.save()
				for i in range(1,11):
					if request.POST.get('fabric'+str(i)):
						new_obj=trims_product.objects.filter(id=int(request.POST.get('fabric'+str(i)))).first()
						new_bom=trims_bom(
							trim=new_obj,
							order=order,
							description=request.POST.get('description_fabric'+str(i)),
							consumption=int(request.POST.get('consumption_fabric'+str(i))),
							wastage=int(request.POST.get('wastage_fabric'+str(i))),
							rate=int(request.POST.get('rate_fabric'+str(i))),
							specification=request.POST.get('specification_fabric'+str(i)),
							fabric=True,
							uom=request.POST.get('uom_fabric'+str(i))
						)
						new_bom.save()
						obj.products.add(new_obj)
						obj.trims_used.add(new_bom)
					if request.POST.get('packing'+str(i)):
						new_obj=trims_product.objects.filter(id=int(request.POST.get('packing'+str(i)))).first()
						new_bom=trims_bom(
							trim=new_obj,
							order=order,
							description=request.POST.get('description_packing'+str(i)),
							consumption=int(request.POST.get('consumption_packing'+str(i))),
							wastage=int(request.POST.get('wastage_packing'+str(i))),
							rate=int(request.POST.get('rate_packing'+str(i))),
							specification=request.POST.get('specification_packing'+str(i)),
							packing=True,
							uom=request.POST.get('uom_packing'+str(i))
						)
						new_bom.save()
						obj.products.add(new_obj)
						obj.trims_used.add(new_bom)
					if request.POST.get('sewing'+str(i)):
						new_obj=trims_product.objects.filter(id=int(request.POST.get('sewing'+str(i)))).first()
						new_bom=trims_bom(
							trim=new_obj,
							order=order,
							description=request.POST.get('description_sewing'+str(i)),
							consumption=int(request.POST.get('consumption_sewing'+str(i))),
							wastage=int(request.POST.get('wastage_sewing'+str(i))),
							rate=int(request.POST.get('rate_sewing'+str(i))),
							specification=request.POST.get('specification_sewing'+str(i)),
							sewing=True,
							uom=request.POST.get('uom_sewing'+str(i))
						)
						new_bom.save()
						obj.products.add(new_obj)
						obj.trims_used.add(new_bom)
					if request.POST.get('finishing'+str(i)):
						new_obj=trims_product.objects.filter(id=int(request.POST.get('finishing'+str(i)))).first()
						new_bom=trims_bom(
							trim=new_obj,
							order=order,
							description=request.POST.get('description_finishing'+str(i)),
							consumption=int(request.POST.get('consumption_finishing'+str(i))),
							wastage=int(request.POST.get('wastage_finishing'+str(i))),
							rate=int(request.POST.get('rate_finishing'+str(i))),
							specification=request.POST.get('specification_finishing'+str(i)),
							finishing=True,
							uom=request.POST.get('uom_finishing'+str(i))
						)
						new_bom.save()
						obj.products.add(new_obj)
						obj.trims_used.add(new_bom)

				order=company_Order.objects.filter(order_no=order_no).first()
				obj.order=order
				obj.save()
				staff_merch=staff_Categories.objects.filter(name="Merchandising").first()
				staff_to=order.staffs_Allocated.all().filter(staff_category=staff_merch)
				for i in staff_to:
					obj_noti=notifications(
						title="BOM & Costing is Uploaded by Garment Vendor ("+str(order_no)+")",
						description="BOM & Costing is Uploaded by Garment Vendor ("+str(order_no)+")",
						user=i,
						link="/userdetail/vendor_profile/orders/"+str(order_no)+"/forms/bom/"+str(obj.id),
						type_of_order=order.order_type
						)
					obj_noti.save()
				return redirect('/userdetail/vendor_profile/orders/'+str(order_no))

			return render(request,"vendor/vendor_profile_bom.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def vendor_profile_bom_details(request,order_no,bom_id):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		sel_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		if (details.vendor and details.seller_category==sel_cate) or details.staff:
			obj=bom.objects.filter(id=bom_id).first()
			order=company_Order.objects.filter(order_no=order_no).first()
			data={}
			fabric=list(obj.products.all().filter(category=trims_Category.objects.filter(fabric=True).first()).values())
			sewing=list(obj.products.all().filter(category=trims_Category.objects.filter(sewing=True).first()).values())
			packing=list(obj.products.all().filter(category=trims_Category.objects.filter(packing=True).first()).values())
			finishing=list(obj.products.all().filter(category=trims_Category.objects.filter(finishing=True).first()).values())
			data['order_no']=order_no
			data['bom_id']=bom_id
			data['cutmake_consum']=obj.cutmake_consum
			data['cutmake_rate']=obj.cutmake_rate
			data['cutmake_cost']=obj.cutmake_cost
			data['profit_percentage']=obj.profit_percentage
			data['total_cost']=obj.total_cost_vendor
			if details.staff:
				# total_cost=obj.total_cost+obj.merchandising_cost+obj.warehouse_cost+obj.freight_charges+obj.primary_pack_cost+obj.sampling_cost+obj.barcode_cost
				data['total_cost']=obj.total_cost_staff
			data['total_bom']=obj
			data['options']=bom.objects.filter(order=order)
			if details.staff:
				data['is_staff_user']=True
			if request.POST.get('merch_cost'):
				obj.merchandising_cost=int(request.POST.get('merch_cost'))
				if request.POST.get('warehouse')=='light':
					obj.warehouse_cost=4
				elif request.POST.get('warehouse')=='medium':
					obj.warehouse_cost=8
				elif request.POST.get('warehouse')=='heavy':
					obj.warehouse_cost=12
				obj.freight_charges=int(request.POST.get('freight'))
				obj.primary_pack_cost=int(request.POST.get('primary'))
				obj.sampling_cost=int(request.POST.get('sampling'))
				obj.barcode_cost=int(request.POST.get('barcode'))
				obj.save()

				staff_sales=staff_Categories.objects.filter(name="Sales").first()
				staffs_to=order.staffs_Allocated.all().filter(staff_category=staff_sales,position='H')
				if details.staff_category==staff_sales:
					order.total_Price=int(obj.total_cost_staff)
					order.quoted_Price=int(obj.total_cost_staff)
					order.save()
				else:
					for i in staffs_to:
						obj_noti=notifications(
							title="BOM & Merchandising Cost is Uploaded ("+str(order.order_no)+")",
							description="BOM & Merchandising Cost is Uploaded ("+str(order.order_no)+")",
							user=i,
							link='/userdetail/vendor_profile/orders/'+str(order_no)+'/forms/bom/'+str(bom_id),
							type_of_order=order.order_type
							)
						obj_noti.save()

				return redirect('/userdetail/vendor_profile/orders/'+str(order_no)+'/forms/bom/'+str(bom_id))
			# print(data)
			return render(request,"vendor/vendor_profile_bom_details.html",data)

		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



from b2b.models import trims_orders

from django.shortcuts import render

def vendor_profile_compare_bom(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		order=company_Order.objects.filter(order_no=order_no).first()
		if details and order:
			data={
				"options":bom.objects.filter(order=order),
				"order":order,
				"details":details
			}
			if request.POST.get('bom1_un_ajax'):
				ajax_data={
					"bom1":bom.objects.filter(id=int(request.POST.get('bom1_un_ajax'))).first(),
					"bom2":bom.objects.filter(id=int(request.POST.get('bom2_un_ajax'))).first()
				}
				return render(request,"ajax_response/vendor/compare_bom.html",ajax_data)
			return render(request,"vendor/vendor_profile_compare_bom.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/logout')



def vendor_profile_bom_ordering(request,order_no,bom_id):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		sel_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		if (details.vendor and details.seller_category==sel_cate) or details.staff:
			order=company_Order.objects.filter(order_no=order_no).first()
			bom_obj=bom.objects.filter(id=bom_id).first()
			if order and bom_obj:
				trims_users=[]
				for i in bom_obj.trims_used.all():
					users=trims_product_quantity.objects.filter(to_product=i.trim)
					floated=trims_orders.objects.filter(trim_bom=i,order=order,floated=True)
					act_order=trims_orders.objects.filter(trim_bom=i,order=order,floated=False)
					trims_users.append([i,users,floated,act_order])
				data={
					"order":order,
					"bom_obj":bom_obj,
					"trims_users":trims_users,
					"bom_id":bom_id,
				}
				if request.POST.get('float_to_user'):
					trims_bom_obj=trims_bom.objects.filter(id=int(request.POST.get('trims_bom'))).first()
					float_to_user=detail.objects.filter(email=request.POST.get('float_to_user')).first()
					trims_orders_obj=trims_orders.objects.filter(placed_to=float_to_user,trim_bom=trims_bom_obj).first()
					if not(trims_orders_obj):
						trims_orders_obj=trims_orders(placed_by=details,placed_to=float_to_user,
						trim_bom=trims_bom_obj,order=order,floated=True)
						trims_orders_obj.save()
						obj3=notifications(
							title="New Order Floated to you for update in custom price & MOQ.",
							description="New Order Floated to you for update in custom price. By -"+details.email,
							user=float_to_user,
							link="/userdetail/vendor_profile/trims_floated_orders/"+str(trims_orders_obj.id),
							type_of_order=order.order_type
							)
						obj3.save()
					return redirect('/userdetail/vendor_profile/orders/'+str(order_no)+'/forms/bom/'+str(bom_id)+'/ordering')
				if request.POST.get('trim_order'):
					trim_order_obj=trims_orders.objects.filter(id=int(request.POST.get('trim_order'))).first()
					trim_order_obj.trim_bom.rate=trim_order_obj.rate
					trim_order_obj.trim_bom.save()
					trim_order_obj.floated=False
					trim_order_obj.order.staffs_Allocated.add(trim_order_obj.placed_to)
					trim_order_obj.order.save()
					trim_order_obj.quantity=int(request.POST.get('trim_quantity'))
					trim_order_obj.save()
					return redirect('/userdetail/vendor_profile/orders/'+str(order_no)+'/forms/bom/'+str(bom_id))
				return render(request,"vendor/vendor_profile_bom_ordering.html",data)
			else:
				return redirect('/userdetail/logout')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def vendor_trims_floated_orders(request,trims_orders_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		trims_order_obj=trims_orders.objects.filter(id=trims_orders_no).first()
		if (details.vendor and trims_order_obj):
			data={
				"trims_order":trims_order_obj
			}
			if request.POST.get('rate'):
				rate=int(request.POST.get('rate'))
				moq=int(request.POST.get('moq'))
				lead_time=int(request.POST.get('lead_time'))
				trims_order_obj.rate=rate
				trims_order_obj.moq=moq
				trims_order_obj.lead_time=lead_time
				trims_order_obj.save()
				return redirect('/userdetail/vendor_profile')
			return render(request,"vendor/vendor_trims_floated_orders.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def vendor_custom_form(request,order_no,form_id):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor or details.staff:
			order=company_Order.objects.filter(order_no=order_no).first()
			form=custom_Form.objects.filter(id=form_id).first()
			form_data=custom_Form_Data.objects.filter(form=form).first()
			li=form.attributes.all()
			li1=[]
			for i in li:
				if (details in i.individual_User_Edit_Permissions.all()):
					li1.append([i,0])
				elif (details in i.individual_User_View_Permissions.all()):
					li1.append([i,1])
				elif details.staff:
					if (details.staff_category in i.staff_Category_Edit_Permissions.all()):
						li1.append([i,0])
					elif details.staff_category in i.staff_Category_View_Permissions.all():
						li1.append([i,1])
				elif details.vendor:
					if (details.seller_category in i.seller_Category_Edit_Permissions.all()):
						li1.append([i,0])
					elif details.seller_category in i.seller_Category_View_Permissions.all():
						li1.append([i,1])
			act=activities_Category.objects.filter(request_Forms=form).last()
			print(form_data)
			data={
			"form_name":form.name,
			"form":li1,
			"form_data":form_data,
			"order":order,
			"form_id":form_id,
			"act":act,
			"form45":form
			}
			if request.POST.get('data1') or request.POST.get('data2') or request.POST.get('data3') or request.POST.get('data4'):
				if form_data is None:
					form_data=custom_Form_Data(
						user=details,form=form
						)
				files_count=1
				form=li1
				length=len(form)
				if length>=1:
					if form[0][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data1')
						elif files_count==2:
							form_data.file2=request.FILES.get('data1')
						elif files_count==3:
							form_data.file3=request.FILES.get('data1')
						files_count=files_count+1
					else:
						form_data.data1=request.POST.get('data1')
					if form[0][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data1')
					elif form[0][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data1')
					elif form[0][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data1')
					order.save()
				if length>=2:
					if form[1][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data2')
						elif files_count==2:
							form_data.file2=request.FILES.get('data2')
						elif files_count==3:
							form_data.file3=request.FILES.get('data2')
						files_count=files_count+1
					else:
						form_data.data2=request.POST.get('data2')
					if form[1][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data2')
					elif form[1][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data2')
					elif form[1][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data2')
					order.save()
				if length>=3:
					if form[2][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data3')
						elif files_count==2:
							form_data.file2=request.FILES.get('data3')
						elif files_count==3:
							form_data.file3=request.FILES.get('data3')
						files_count=files_count+1
					else:
						form_data.data3=request.POST.get('data3')
					if form[2][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data3')
					elif form[2][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data3')
					elif form[2][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data3')
					order.save()
				if length>=4:
					if form[3][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data4')
						elif files_count==2:
							form_data.file2=request.FILES.get('data4')
						elif files_count==3:
							form_data.file3=request.FILES.get('data4')
						files_count=files_count+1
					else:
						form_data.data4=request.POST.get('data4')
					if form[3][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data4')
					elif form[3][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data4')
					elif form[3][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data4')
					order.save()
				if length>=5:
					if form[4][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data5')
						elif files_count==2:
							form_data.file2=request.FILES.get('data5')
						elif files_count==3:
							form_data.file3=request.FILES.get('data5')
						files_count=files_count+1
					else:
						form_data.data5=request.POST.get('data5')
					if form[4][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data5')
					elif form[4][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data5')
					elif form[4][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data5')
					order.save()
				if length>=6:
					if form[5][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data6')
						elif files_count==2:
							form_data.file2=request.FILES.get('data6')
						elif files_count==3:
							form_data.file3=request.FILES.get('data6')
						files_count=files_count+1
					else:
						form_data.data6=request.POST.get('data6')
					if form[5][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data6')
					elif form[5][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data6')
					elif form[5][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data6')
					order.save()
				if length>=7:
					if form[6][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data7')
						elif files_count==2:
							form_data.file2=request.FILES.get('data7')
						elif files_count==3:
							form_data.file3=request.FILES.get('data7')
						files_count=files_count+1
					else:
						form_data.data7=request.POST.get('data7')
					if form[6][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data7')
					elif form[6][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data7')
					elif form[6][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data7')
					order.save()
				if length>=8:
					if form[7][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data8')
						elif files_count==2:
							form_data.file2=request.FILES.get('data8')
						elif files_count==3:
							form_data.file3=request.FILES.get('data8')
						files_count=files_count+1
					else:
						form_data.data8=request.POST.get('data8')
					if form[7][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data8')
					elif form[7][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data8')
					elif form[7][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data8')
					order.save()
				if length>=9:
					if form[8][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data9')
						elif files_count==2:
							form_data.file2=request.FILES.get('data9')
						elif files_count==3:
							form_data.file3=request.FILES.get('data9')
						files_count=files_count+1
					else:
						form_data.data9=request.POST.get('data9')
					if form[8][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data9')
					elif form[8][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data9')
					elif form[8][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data9')
					order.save()
				if length>=10:
					if form[9][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data10')
						elif files_count==2:
							form_data.file2=request.FILES.get('data10')
						elif files_count==3:
							form_data.file3=request.FILES.get('data10')
						files_count=files_count+1
					else:
						form_data.data10=request.POST.get('data10')
					if form[9][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data10')
					elif form[9][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data10')
					elif form[9][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data10')
					order.save()
				if length>=11:
					if form[10][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data11')
						elif files_count==2:
							form_data.file2=request.FILES.get('data11')
						elif files_count==3:
							form_data.file3=request.FILES.get('data11')
						files_count=files_count+1
					else:
						form_data.data11=request.POST.get('data11')
					if form[10][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data11')
					elif form[10][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data11')
					elif form[10][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data11')
					order.save()
				if length>=12:
					if form[11][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data12')
						elif files_count==2:
							form_data.file2=request.FILES.get('data12')
						elif files_count==3:
							form_data.file3=request.FILES.get('data12')
						files_count=files_count+1
					else:
						form_data.data12=request.POST.get('data12')
					if form[11][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data12')
					elif form[11][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data12')
					elif form[11][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data12')
					order.save()
				if length>=13:
					if form[12][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data13')
						elif files_count==2:
							form_data.file2=request.FILES.get('data13')
						elif files_count==3:
							form_data.file3=request.FILES.get('data13')
						files_count=files_count+1
					else:
						form_data.data13=request.POST.get('data13')
					if form[12][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data13')
					elif form[12][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data13')
					elif form[12][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data13')
					order.save()
				if length>=14:
					if form[13][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data14')
						elif files_count==2:
							form_data.file2=request.FILES.get('data14')
						elif files_count==3:
							form_data.file3=request.FILES.get('data14')
						files_count=files_count+1
					else:
						form_data.data14=request.POST.get('data14')
					if form[13][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data14')
					elif form[13][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data14')
					elif form[13][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data14')
					order.save()
				if length>=15:
					if form[14][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data15')
						elif files_count==2:
							form_data.file2=request.FILES.get('data15')
						elif files_count==3:
							form_data.file3=request.FILES.get('data15')
						files_count=files_count+1
					else:
						form_data.data15=request.POST.get('data15')
					if form[14][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data15')
					elif form[14][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data15')
					elif form[14][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data15')
					order.save()
				if length>=16:
					if form[15][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data16')
						elif files_count==2:
							form_data.file2=request.FILES.get('data16')
						elif files_count==3:
							form_data.file3=request.FILES.get('data16')
						files_count=files_count+1
					else:
						form_data.data16=request.POST.get('data16')
					if form[15][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data16')
					elif form[15][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data16')
					elif form[15][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data16')
					order.save()
				if length>=17:
					if form[16][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data17')
						elif files_count==2:
							form_data.file2=request.FILES.get('data17')
						elif files_count==3:
							form_data.file3=request.FILES.get('data17')
						files_count=files_count+1
					else:
						form_data.data17=request.POST.get('data17')
					if form[16][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data17')
					elif form[16][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data17')
					elif form[16][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data17')
					order.save()
				if length>=18:
					if form[17][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data18')
						elif files_count==2:
							form_data.file2=request.FILES.get('data18')
						elif files_count==3:
							form_data.file3=request.FILES.get('data18')
						files_count=files_count+1
					else:
						form_data.data18=request.POST.get('data18')
					if form[17][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data18')
					elif form[17][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data18')
					elif form[17][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data18')
					order.save()
				if length>=19:
					if form[18][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data19')
						elif files_count==2:
							form_data.file2=request.FILES.get('data19')
						elif files_count==3:
							form_data.file3=request.FILES.get('data19')
						files_count=files_count+1
					else:
						form_data.data19=request.POST.get('data19')
					if form[18][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data19')
					elif form[18][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data19')
					elif form[18][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data19')
					order.save()
				if length>=20:
					if form[19][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data20')
						elif files_count==2:
							form_data.file2=request.FILES.get('data20')
						elif files_count==3:
							form_data.file3=request.FILES.get('data20')
						files_count=files_count+1
					else:
						form_data.data20=request.POST.get('data20')
					if form[19][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data20')
					elif form[19][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data20')
					elif form[19][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data20')
					order.save()
				if length>=21:
					if form[20][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data21')
						elif files_count==2:
							form_data.file2=request.FILES.get('data21')
						elif files_count==3:
							form_data.file3=request.FILES.get('data21')
						files_count=files_count+1
					else:
						form_data.data21=request.POST.get('data21')
					if form[20][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data21')
					elif form[20][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data21')
					elif form[20][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data21')
					order.save()
				if length>=22:
					if form[21][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data22')
						elif files_count==2:
							form_data.file2=request.FILES.get('data22')
						elif files_count==3:
							form_data.file3=request.FILES.get('data22')
						files_count=files_count+1
					else:
						form_data.data22=request.POST.get('data22')
					if form[21][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data22')
					elif form[21][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data22')
					elif form[21][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data22')
					order.save()
				if length>=23:
					if form[22][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data23')
						elif files_count==2:
							form_data.file2=request.FILES.get('data23')
						elif files_count==3:
							form_data.file3=request.FILES.get('data23')
						files_count=files_count+1
					else:
						form_data.data23=request.POST.get('data23')
					if form[22][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data23')
					elif form[22][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data23')
					elif form[22][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data23')
					order.save()
				if length>=24:
					if form[23][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data24')
						elif files_count==2:
							form_data.file2=request.FILES.get('data24')
						elif files_count==3:
							form_data.file3=request.FILES.get('data24')
						files_count=files_count+1
					else:
						form_data.data24=request.POST.get('data24')
					if form[23][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data24')
					elif form[23][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data24')
					elif form[23][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data24')
					order.save()
				if length>=25:
					if form[24][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data25')
						elif files_count==2:
							form_data.file2=request.FILES.get('data25')
						elif files_count==3:
							form_data.file3=request.FILES.get('data25')
						files_count=files_count+1
					else:
						form_data.data25=request.POST.get('data25')
					if form[24][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data25')
					elif form[24][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data25')
					elif form[24][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data25')
					order.save()
				if length>=26:
					if form[25][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data26')
						elif files_count==2:
							form_data.file2=request.FILES.get('data26')
						elif files_count==3:
							form_data.file3=request.FILES.get('data26')
						files_count=files_count+1
					else:
						form_data.data26=request.POST.get('data26')
					if form[25][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data26')
					elif form[25][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data26')
					elif form[25][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data26')
					order.save()
				if length>=27:
					if form[26][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data27')
						elif files_count==2:
							form_data.file2=request.FILES.get('data27')
						elif files_count==3:
							form_data.file3=request.FILES.get('data27')
						files_count=files_count+1
					else:
						form_data.data27=request.POST.get('data27')
					if form[26][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data27')
					elif form[26][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data27')
					elif form[26][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data27')
					order.save()
				if length>=28:
					if form[27][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data28')
						elif files_count==2:
							form_data.file2=request.FILES.get('data28')
						elif files_count==3:
							form_data.file3=request.FILES.get('data28')
						files_count=files_count+1
					else:
						form_data.data28=request.POST.get('data28')
					if form[27][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data28')
					elif form[27][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data28')
					elif form[27][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data28')
					order.save()
				if length>=29:
					if form[28][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data29')
						elif files_count==2:
							form_data.file2=request.FILES.get('data29')
						elif files_count==3:
							form_data.file3=request.FILES.get('data29')
						files_count=files_count+1
					else:
						form_data.data29=request.POST.get('data29')
					if form[28][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data29')
					elif form[28][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data29')
					elif form[28][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data29')
					order.save()
				if length>=30:
					if form[29][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data30')
						elif files_count==2:
							form_data.file2=request.FILES.get('data30')
						elif files_count==3:
							form_data.file3=request.FILES.get('data30')
						files_count=files_count+1
					else:
						form_data.data30=request.POST.get('data30')
					if form[29][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data30')
					elif form[29][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data30')
					elif form[29][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data30')
					order.save()
				if length>=31:
					if form[30][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data31')
						elif files_count==2:
							form_data.file2=request.FILES.get('data31')
						elif files_count==3:
							form_data.file3=request.FILES.get('data31')
						files_count=files_count+1
					else:
						form_data.data31=request.POST.get('data31')
					if form[30][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data31')
					elif form[30][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data31')
					elif form[30][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data31')
					order.save()
				if length>=32:
					if form[31][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data32')
						elif files_count==2:
							form_data.file2=request.FILES.get('data32')
						elif files_count==3:
							form_data.file3=request.FILES.get('data32')
						files_count=files_count+1
					else:
						form_data.data32=request.POST.get('data32')
					if form[31][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data32')
					elif form[31][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data32')
					elif form[31][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data32')
					order.save()
				if length>=33:
					if form[32][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data33')
						elif files_count==2:
							form_data.file2=request.FILES.get('data33')
						elif files_count==3:
							form_data.file3=request.FILES.get('data33')
						files_count=files_count+1
					else:
						form_data.data33=request.POST.get('data33')
					if form[32][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data33')
					elif form[32][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data33')
					elif form[32][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data33')
					order.save()
				if length>=34:
					if form[33][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data34')
						elif files_count==2:
							form_data.file2=request.FILES.get('data34')
						elif files_count==3:
							form_data.file3=request.FILES.get('data34')
						files_count=files_count+1
					else:
						form_data.data34=request.POST.get('data34')
					if form[33][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data34')
					elif form[33][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data34')
					elif form[33][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data34')
					order.save()
				if length>=35:
					if form[34][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data35')
						elif files_count==2:
							form_data.file2=request.FILES.get('data35')
						elif files_count==3:
							form_data.file3=request.FILES.get('data35')
						files_count=files_count+1
					else:
						form_data.data35=request.POST.get('data35')
					if form[34][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data35')
					elif form[34][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data35')
					elif form[34][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data35')
					order.save()
				if length>=36:
					if form[35][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data36')
						elif files_count==2:
							form_data.file2=request.FILES.get('data36')
						elif files_count==3:
							form_data.file3=request.FILES.get('data36')
						files_count=files_count+1
					else:
						form_data.data36=request.POST.get('data36')
					if form[35][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data36')
					elif form[35][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data36')
					elif form[35][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data36')
					order.save()
				if length>=37:
					if form[36][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data37')
						elif files_count==2:
							form_data.file2=request.FILES.get('data37')
						elif files_count==3:
							form_data.file3=request.FILES.get('data37')
						files_count=files_count+1
					else:
						form_data.data37=request.POST.get('data37')
					if form[36][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data37')
					elif form[36][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data37')
					elif form[36][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data37')
					order.save()
				if length>=38:
					if form[37][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data38')
						elif files_count==2:
							form_data.file2=request.FILES.get('data38')
						elif files_count==3:
							form_data.file3=request.FILES.get('data38')
						files_count=files_count+1
					else:
						form_data.data38=request.POST.get('data38')
					if form[37][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data38')
					elif form[37][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data38')
					elif form[37][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data38')
					order.save()
				if length>=39:
					if form[38][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data39')
						elif files_count==2:
							form_data.file2=request.FILES.get('data39')
						elif files_count==3:
							form_data.file3=request.FILES.get('data39')
						files_count=files_count+1
					else:
						form_data.data39=request.POST.get('data39')
					if form[38][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data39')
					elif form[38][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data39')
					elif form[38][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data39')
					order.save()
				if length>=40:
					if form[39][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data40')
						elif files_count==2:
							form_data.file2=request.FILES.get('data40')
						elif files_count==3:
							form_data.file3=request.FILES.get('data40')
						files_count=files_count+1
					else:
						form_data.data40=request.POST.get('data40')
					if form[39][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data40')
					elif form[39][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data40')
					elif form[39][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data40')
					order.save()
				if length>=41:
					if form[40][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data41')
						elif files_count==2:
							form_data.file2=request.FILES.get('data41')
						elif files_count==3:
							form_data.file3=request.FILES.get('data41')
						files_count=files_count+1
					else:
						form_data.data41=request.POST.get('data41')
					if form[40][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data41')
					elif form[40][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data41')
					elif form[40][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data41')
					order.save()
				if length>=42:
					if form[41][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data42')
						elif files_count==2:
							form_data.file2=request.FILES.get('data42')
						elif files_count==3:
							form_data.file3=request.FILES.get('data42')
						files_count=files_count+1
					else:
						form_data.data42=request.POST.get('data42')
					if form[41][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data42')
					elif form[41][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data42')
					elif form[41][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data42')
					order.save()
				if length>=43:
					if form[42][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data43')
						elif files_count==2:
							form_data.file2=request.FILES.get('data43')
						elif files_count==3:
							form_data.file3=request.FILES.get('data43')
						files_count=files_count+1
					else:
						form_data.data43=request.POST.get('data43')
					if form[42][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data43')
					elif form[42][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data43')
					elif form[42][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data43')
					order.save()
				if length>=44:
					if form[43][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data44')
						elif files_count==2:
							form_data.file2=request.FILES.get('data44')
						elif files_count==3:
							form_data.file3=request.FILES.get('data44')
						files_count=files_count+1
					else:
						form_data.data44=request.POST.get('data44')
					if form[43][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data44')
					elif form[43][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data44')
					elif form[43][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data44')
					order.save()
				if length>=45:
					if form[44][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data45')
						elif files_count==2:
							form_data.file2=request.FILES.get('data45')
						elif files_count==3:
							form_data.file3=request.FILES.get('data45')
						files_count=files_count+1
					else:
						form_data.data45=request.POST.get('data45')
					if form[44][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data45')
					elif form[44][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data45')
					elif form[44][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data45')
					order.save()
				if length>=46:
					if form[45][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data46')
						elif files_count==2:
							form_data.file2=request.FILES.get('data46')
						elif files_count==3:
							form_data.file3=request.FILES.get('data46')
						files_count=files_count+1
					else:
						form_data.data46=request.POST.get('data46')
					if form[45][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data46')
					elif form[45][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data46')
					elif form[45][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data46')
					order.save()
				if length>=47:
					if form[46][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data47')
						elif files_count==2:
							form_data.file2=request.FILES.get('data47')
						elif files_count==3:
							form_data.file3=request.FILES.get('data47')
						files_count=files_count+1
					else:
						form_data.data47=request.POST.get('data47')
					if form[46][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data47')
					elif form[46][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data47')
					elif form[46][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data47')
					order.save()
				if length>=48:
					if form[47][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data48')
						elif files_count==2:
							form_data.file2=request.FILES.get('data48')
						elif files_count==3:
							form_data.file3=request.FILES.get('data48')
						files_count=files_count+1
					else:
						form_data.data48=request.POST.get('data48')
					if form[47][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data48')
					elif form[47][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data48')
					elif form[47][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data48')
					order.save()
				if length>=49:
					if form[48][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data49')
						elif files_count==2:
							form_data.file2=request.FILES.get('data49')
						elif files_count==3:
							form_data.file3=request.FILES.get('data49')
						files_count=files_count+1
					else:
						form_data.data49=request.POST.get('data49')
					if form[48][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data49')
					elif form[48][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data49')
					elif form[48][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data49')
					order.save()
				if length>=50:
					if form[49][0].field_Type=='F':
						if files_count==1:
							form_data.file1=request.FILES.get('data50')
						elif files_count==2:
							form_data.file2=request.FILES.get('data50')
						elif files_count==3:
							form_data.file3=request.FILES.get('data50')
						files_count=files_count+1
					else:
						form_data.data50=request.POST.get('data50')
					if form[49][0].attribute_Link_To=='htm':
						order.htm=request.FILES.get('data50')
					elif form[49][0].attribute_Link_To=='pack_manual':
						order.packing_manual=request.FILES.get('data50')
					elif form[49][0].attribute_Link_To=='wash_care':
						order.washcare=request.FILES.get('data50')
					order.save()
				# form_data.data1=request.POST.get('data1')
				# form_data.data2=request.POST.get('data2')
				# form_data.data3=request.POST.get('data3')
				# form_data.data4=request.POST.get('data4')
				# form_data.data5=request.POST.get('data5')
				# form_data.data6=request.POST.get('data6')
				# form_data.data7=request.POST.get('data7')
				# form_data.data8=request.POST.get('data8')
				# form_data.data9=request.POST.get('data9')
				# form_data.data10=request.POST.get('data10')
				form_data.save()
				print(form_data)
				if details.staff:
					return redirect('/userdetail/staff_profile/orders/'+str(order.order_no))
				return redirect('/userdetail/vendor_profile/orders/'+str(order.order_no))

			return render(request,'vendor/vendor_custom_form.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



# for i in range(1,51):
# 	print("""				if length>="""+str(i+1)+""":
# 					if form["""+str(i)+"""].field_Type=='F':
# 						if files_count==1:
# 							form_data.file1=request.FILES.get('data"""+str(i+1)+"""')
# 						elif files_count==2:
# 							form_data.file2=request.FILES.get('data"""+str(i+1)+"""')
# 						elif files_count==3:
# 							form_data.file3=request.FILES.get('data"""+str(i+1)+"""')
# 						files_count=files_count+1
# 					else:
# 						form_data.data"""+str(i+1)+"""=request.POST.get('data"""+str(i+1)+"""')
# 					if form["""+str(i)+"""].attribute_Link_To=='htm':
# 						order.htm=request.FILES.get('data"""+str(i+1)+"""')
# 					elif form["""+str(i)+"""].attribute_Link_To=='pack_manual':
# 						order.packing_manual=request.FILES.get('data"""+str(i+1)+"""')
# 					elif form["""+str(i)+"""].attribute_Link_To=='wash_care':
# 						order.washcare=request.FILES.get('data"""+str(i+1)+"""')
# 					order.save()""")


#
# for i in range(1,51):
# 	print("""			{% if form."""+str(i-1)+""".0 %}
# 			<div class="col-6 my-3">
# 				<label style="font-family: 'Cabin',sans-serif;font-size: .9em;padding: .5vw;">{{form."""+str(i-1)+""".0.name}}</label>
# 				{% ifequal form."""+str(i-1)+""".0.field_Type 'C' %}
# 				<input type="text" {% if form."""+str(i-1)+""".1 %}readonly{% endif %} name="data"""+str(i)+"""" value="{{form_data.data"""+str(i)+"""}}" placeholder="{{form."""+str(i-1)+""".0.name}}" required class="input_attribute">
# 				{% endifequal %}
# 				{% ifequal form."""+str(i-1)+""".0.field_Type 'I' %}
# 				<input type="number" {% if form."""+str(i-1)+""".1 %}readonly{% endif %} name="data"""+str(i)+"""" value="{{form_data.data"""+str(i)+"""}}" placeholder="{{form."""+str(i-1)+""".0.name}}" required class="input_attribute">
# 				{% endifequal %}
# 				{% ifequal form."""+str(i-1)+""".0.field_Type 'F' %}
# 				<input type="file" name="data"""+str(i)+"""" value="{{form_data.data"""+str(i)+"""}}" placeholder="{{form."""+str(i-1)+""".0.name}}" required class="input_attribute" style="border-bottom: none;">
# 				{% endifequal %}
# 				{% ifequal form."""+str(i-1)+""".0.field_Type 'D' %}
# 				<select name="data"""+str(i)+"""" class="input_attribute" {% if form."""+str(i-1)+""".1 %}readonly{% endif %}>
# 					{% if form."""+str(i-1)+""".0.dropdown_Data1 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data1}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data1 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data1}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data2 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data2}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data2 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data2}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data3 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data3}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data3 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data3}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data4 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data4}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data4 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data4}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data5 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data5}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data5 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data5}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data6 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data6}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data6 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data6}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data7 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data7}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data7 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data7}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data8 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data8}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data8 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data8}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data9 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data9}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data9 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data9}}</option>
# 					{% endif %}
# 					{% if form."""+str(i-1)+""".0.dropdown_Data10 %}
# 					<option value="{{form."""+str(i-1)+""".0.dropdown_Data10}}"{% ifequal form."""+str(i-1)+""".0.dropdown_Data10 form_data.data"""+str(i)+""" %}selected{% endifequal %}>{{form."""+str(i-1)+""".0.dropdown_Data10}}</option>
# 					{% endif %}
# 				</select>
# 				{% endifequal %}
# 			</div>
# 			{% endif %}""")






def staff_profile_orders_list(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			orders=company_Order.objects.filter(staffs_Allocated=details).order_by('-overall_priority')
			enquiry=company_Order.objects.filter(staffs_Allocated=details,order_type='E').order_by('-overall_priority')
			design=company_Order.objects.filter(staffs_Allocated=details,order_type='D').order_by('-overall_priority')
			sampling=company_Order.objects.filter(staffs_Allocated=details,order_type='S').order_by('-overall_priority')
			orders=company_Order.objects.filter(staffs_Allocated=details,order_type='O').order_by('-overall_priority')
			data={
			"orders":orders,
			"enquiry":enquiry,
			"design":design,
			"sampling":sampling
			}
			return render(request,"userdetail/staff_profile_orders_list.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def vendor_profile_orders_list(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			orders=company_Order.objects.filter(staffs_Allocated=details,personal_order=False).order_by('-overall_priority')
			per_orders=company_Order.objects.filter(staffs_Allocated=details,personal_order=True).order_by('-overall_priority')
			obj=seller_Categories.objects.filter(name="Garmenting Vendor").first()
			gar=False
			if details.seller_category==obj:
				gar=True
			data={
			"orders":orders,
			"gar":gar,
			"per_orders":per_orders
			}
			return render(request,"vendor/vendor_profile_orders_list.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')

def lay_list(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			orders=company_Order.objects.filter(staffs_Allocated=details,personal_order=False).order_by('-overall_priority')
			per_orders=company_Order.objects.filter(staffs_Allocated=details,personal_order=True).order_by('-overall_priority')
			obj=seller_Categories.objects.filter(name="Garmenting Vendor").first()
			gar=False
			if details.seller_category==obj:
				gar=True
			data={
			"orders":orders,
			"gar":gar,
			"per_orders":per_orders
			}
			return render(request,"vendor/lay_list.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')

def cut_list(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			orders=company_Order.objects.filter(staffs_Allocated=details,personal_order=False).order_by('-overall_priority')
			per_orders=company_Order.objects.filter(staffs_Allocated=details,personal_order=True).order_by('-overall_priority')
			obj=seller_Categories.objects.filter(name="Garmenting Vendor").first()
			gar=False
			if details.seller_category==obj:
				gar=True
			data={
			"orders":orders,
			"gar":gar,
			"per_orders":per_orders
			}
			return render(request,"vendor/cut_list.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def create_production_products(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		sel_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		print(details.vendor,details.seller_category,sel_cate)
		if details.vendor and details.seller_category==sel_cate:
			prod_objs=production_Product.objects.filter(user=details)
			li=[]
			for i in prod_objs:
				li1={}
				objs_line=production_Line.objects.filter(production_product=i)
				li1['prod']=i
				li1['lines']=objs_line
				li.append(li1)
			# print(li)
			data={
				"cate":category.objects.all(),
				"prod_obj":li,
				"user":details
			}
			if request.POST.get('prod_ajax'):
				quantity=request.POST.get('quantity_ajax_prod')
				cost=request.POST.get('cost_ajax_prod')
				work=request.POST.get('work_ajax_prod')
				prod_ajax=request.POST.get('prod_ajax')
				prod_ajax=production_Product.objects.filter(id=int(prod_ajax)).first()
				if prod_ajax.user == details:
					prod_ajax.quantity=int(quantity)
					prod_ajax.cost=int(cost)
					details.no_of_working=int(work)
					details.save()
					prod_ajax.save()
				return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
			if request.POST.get('line_name_ajax'):
				line_name=request.POST.get('line_name_ajax')
				line_quan=request.POST.get('line_quan_ajax')
				line_deta=request.POST.get('line_deta_ajax')
				objs_li=production_Line.objects.filter(id=int(line_deta)).first()
				if objs_li.production_product.user==details:
					objs_li.name=line_name
					objs_li.quantity=line_quan
					objs_li.save()
				return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
			if request.GET.get('del'):
				prod_id=request.GET.get('del')
				obj_prod=production_Product.objects.filter(id=int(prod_id)).first()
				obj_lines=production_Line.objects.filter(production_product=obj_prod)
				for i in obj_lines:
					i.delete()
				obj_prod.delete()
				return redirect('/userdetail/vendor_profile/create_production_products')
			if request.POST.get('category'):
				cate=category.objects.filter(name=request.POST.get('category')).first()
				sub_cate=sub_category.objects.filter(product_Category=cate,name=request.POST.get('sub_category')).first()
				sup_cate=super_category.objects.filter(product_Category=cate,
					product_Subcategory=sub_cate,
					name=request.POST.get('super_category')).first()
				quantity=int(request.POST.get('quantity'))
				num_work_month=int(request.POST.get('num_work_month'))
				details.no_of_working=num_work_month
				details.save()
				obj=production_Product(
						product_Category=cate,
						product_Subcategory=sub_cate,
						product_Supercategory=sup_cate,
						quantity=quantity,
						user=details,
						cost=int(request.POST.get('cost'))
					)
				obj.save()
				if request.POST.get('line1_name'):
					line1=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line1_name'),
							quantity=int(request.POST.get('line1_quantity'))
						)
					line1.save()
				if request.POST.get('line2_name'):
					line2=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line2_name'),
							quantity=int(request.POST.get('line2_quantity'))
						)
					line2.save()
				if request.POST.get('line3_name'):
					line3=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line3_name'),
							quantity=int(request.POST.get('line3_quantity'))
						)
					line3.save()
				if request.POST.get('line4_name'):
					line4=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line4_name'),
							quantity=int(request.POST.get('line4_quantity'))
						)
					line4.save()
				if request.POST.get('line5_name'):
					line5=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line5_name'),
							quantity=int(request.POST.get('line5_quantity'))
						)
					line5.save()
				if request.POST.get('line6_name'):
					line6=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line6_name'),
							quantity=int(request.POST.get('line6_quantity'))
						)
					line6.save()
				if request.POST.get('line7_name'):
					line7=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line7_name'),
							quantity=int(request.POST.get('line7_quantity'))
						)
					line7.save()
				if request.POST.get('line8_name'):
					line8=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line8_name'),
							quantity=int(request.POST.get('line8_quantity'))
						)
					line8.save()
				if request.POST.get('line9_name'):
					line9=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line9_name'),
							quantity=int(request.POST.get('line9_quantity'))
						)
					line9.save()
				if request.POST.get('line10_name'):
					line10=production_Line(
							production_product=obj,
							user=details,
							name=request.POST.get('line10_name'),
							quantity=int(request.POST.get('line10_quantity'))
						)
					line10.save()
				return redirect('/userdetail/vendor_profile')


			return render(request,'vendor/create_production_products.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





# for i in range(1,11):
# 	print("""				if request.POST.get('line"""+str(i)+"""_name'):
# 					line"""+str(i)+"""=production_Line(
# 							production_product=obj,
# 							user=details,
# 							name=request.POST.get('line"""+str(i)+"""_name'),
# 							quantity=int(request.POST.get('line"""+str(i)+"""_quantity'))
# 						)
# 					line"""+str(i)+""".save()""")


from Garmenting_Vendor.models import floated_orders
import math

def staff_profile_allocate_garment(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		staff_cate=staff_Categories.objects.filter(name="Merchandising").first()
		if details.staff and details.staff_category==staff_cate:
			order=company_Order.objects.filter(order_no=int(order_no)).first()
			obj=production_Product.objects.filter(product_Category=order.product_Category,
				product_Subcategory=order.product_Subcategory,
				product_Supercategory=order.product_Supercategory)
			li=list(obj.values())
			li2=[]
			for i in obj:
				obj1=floated_orders.objects.filter(
					to_user=i.user,
					from_user=details.email,
					order=order
					).first()
				obj5=activities.objects.filter(
					user=i.user
					).order_by('-planned_date').first()
				if obj5:
					d1=datetime.datetime(obj5.planned_date.year,obj5.planned_date.month,obj5.planned_date.day)
					obj6=datetime.datetime.now()
					d2=datetime.datetime(obj6.year,obj6.month,obj6.day)
					# print(math.floor(order.quantity/i.quantity))
					expected_days=math.ceil(order.quantity/i.quantity)
					sel_gar=seller_Categories.objects.filter(name="Garmenting Vendor").first()
					acti_cate=activities_Category.objects.filter(seller_category=sel_gar,
					factory_Completion_Activity=False)
					maxi_start_date=None
					for kjh in acti_cate:
						obj=activities.objects.filter(user=i.user,activity_Cate=kjh)
						for kl in obj:
							curio=datetime.date(kl.planned_date.year,kl.planned_date.month,
							kl.planned_date.day)
							if maxi_start_date==None:
								maxi_start_date=curio
							else:
								if maxi_start_date<curio:
									maxi_start_date=curio
					if not(maxi_start_date):
						maxi_start_date=datetime.date(datetime.datetime.now().year,
						datetime.datetime.now().month,
						datetime.datetime.now().day)
					if maxi_start_date<datetime.date(datetime.datetime.now().year,
					datetime.datetime.now().month,
					datetime.datetime.now().day):
						maxi_start_date=datetime.date(datetime.datetime.now().year,
						datetime.datetime.now().month,
						datetime.datetime.now().day)
					expected_dispatch=maxi_start_date+datetime.timedelta(days=expected_days)
					order_Date=order.order_date_time
					# print(order_Date.year)
					leadi=order.target_lead_time
					if not(order.target_lead_time):
						leadi=0
					actual_dipatch=datetime.date(order_Date.year,order_Date.month,
					order_Date.day)+datetime.timedelta(days=leadi)
					if (actual_dipatch - expected_dispatch).days>=0:
						color="green"
					elif (actual_dipatch - expected_dispatch).days >=-5:
						color="yellow"
					else:
						color="red"
					li2.append({"0":i,"1":obj1,"2":abs(d2-d1),"3":expected_days,"start_date":maxi_start_date,
					"expected_dispatch":expected_dispatch,
					"actual_dipatch":actual_dipatch,
					"color":color})
				else:
					expected_days=math.ceil(order.quantity/i.quantity)
					sel_gar=seller_Categories.objects.filter(name="Garmenting Vendor").first()
					acti_cate=activities_Category.objects.filter(seller_category=sel_gar,
					factory_Completion_Activity=False)
					maxi_start_date=None
					for kjh in acti_cate:
						obj=activities.objects.filter(user=i.user,activity_Cate=kjh)
						for kl in obj:
							curio=datetime.date(kl.planned_date.year,kl.planned_date.month,
							kl.planned_date.day)
							if maxi_start_date==None:
								maxi_start_date=curio
							else:
								if maxi_start_date<curio:
									maxi_start_date=curio
					if not(maxi_start_date):
						maxi_start_date=datetime.date(datetime.datetime.now().year,
						datetime.datetime.now().month,
						datetime.datetime.now().day)
					if maxi_start_date<datetime.date(datetime.datetime.now().year,
					datetime.datetime.now().month,
					datetime.datetime.now().day):
						maxi_start_date=datetime.date(datetime.datetime.now().year,
						datetime.datetime.now().month,
						datetime.datetime.now().day)
					expected_dispatch=maxi_start_date+datetime.timedelta(days=expected_days)
					order_Date=order.order_date_time
					# print(order_Date.year)
					leadi=order.target_lead_time
					if not(order.target_lead_time):
						leadi=0
					actual_dipatch=datetime.date(order_Date.year,order_Date.month,
					order_Date.day)+datetime.timedelta(days=leadi)
					if (actual_dipatch - expected_dispatch).days>=0:
						color="green"
					elif (actual_dipatch - expected_dispatch).days >=-5:
						color="yellow"
					else:
						color="red"
					li2.append({"0":i,"1":obj1,"2":0,"3":expected_days,"start_date":maxi_start_date,
					"expected_dispatch":expected_dispatch,
					"actual_dipatch":actual_dipatch,
					"color":color})
			data={
			"objs":li2,
			"order":order
			}
			if request.POST.get('email_ajax_float'):
				to_be_added=detail.objects.filter(email=request.POST.get('email_ajax_float')).first()
				obj1=floated_orders.objects.filter(to_user=to_be_added,from_user=details.email,order=order)
				if not(obj1.count()>0):
					obj=floated_orders(
							to_user=to_be_added,
							from_user=details.email,
							order=order,
						)
					obj.save()
					obj3=notifications(
						title="New Order Floated to you for update in custom price.",
						description="New Order Floated to you for update in custom price. By -"+details.email,
						user=to_be_added,
						link="/userdetail/vendor_profile/floated_orders/"+str(order.order_no),
						type_of_order=order.order_type
						)
					obj3.save()
					obj3.link=obj3.link+"?noti="+str(obj3.id)
					obj3.save()
					bol=True
				else:
					bol=False
				return HttpResponse(json.dumps({'bol':bol}), content_type="application/json")
			return render(request,'vendor/staff_profile_allocate_garment.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')









def vendor_floated_orders(request,order_no):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.vendor:
			order=company_Order.objects.filter(order_no=int(order_no)).first()
			oxh=floated_orders.objects.filter(to_user=details,order=order).first()
			data={
				"order":oxh.order,
				"cust":oxh
			}
			if request.POST.get('custom_price'):
				price=int(request.POST.get('custom_price'))
				oxh.updated_price=price
				oxh.save()
				objs=notifications(
					title="Price Added by the "+str(details.name)+" to the order "+str(order.order_no),
					description="Price Added by the "+str(details.name)+" to the order "+str(order.order_no),
					type_of_order=order.order_type,
					user=detail.objects.filter(email=oxh.from_user).first(),
					link="/userdetail/staff_profile/orders/"+str(order.order_no)+"/allocate_garment"
					)
				objs.save()
				return redirect('/userdetail/vendor_profile')
			return render(request,"vendor/vendor_floated_orders.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





from b2b.models import packing_list,cartons_list,distribution_list,quantity_color_map
from b2b.models import carton as ca





def staff_profile_packing_list(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		sel_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		staff_cate=staff_Categories.objects.filter(name="Merchandising").first()
		if details.staff_category==staff_cate or details.seller_category==sel_cate:
			order=company_Order.objects.filter(order_no=order_no).first()
			pack_obj=packing_list.objects.filter(order=order).first()
			if request.GET.get('generate'):
				carton=None
				if pack_obj:
					carton=pack_obj.cartons.all()
				for i in carton:
					i.delete()
				pack_obj.delete()
				pack_obj=None
				order.packing_generated=False
				order.save()
			if order.packing_generated==False:
				carton=None
				if pack_obj:
					carton=pack_obj.cartons.all()
				else:
					pack_obj=packing_list(order=order)
					pack_obj.save()
					carton=pack_obj.cartons.all()
				over_quan=0
	# for i in range(24,53,2):
	# 	print("""				if car.quantity_"""+str(i)+""":
	# 					over_quan=over_quan+car.quantity_"""+str(i)+)
				for car in carton:
					if car.quantity_24:
						over_quan=over_quan+car.quantity_24
					if car.quantity_26:
						over_quan=over_quan+car.quantity_26
					if car.quantity_28:
						over_quan=over_quan+car.quantity_28
					if car.quantity_30:
						over_quan=over_quan+car.quantity_30
					if car.quantity_32:
						over_quan=over_quan+car.quantity_32
					if car.quantity_34:
						over_quan=over_quan+car.quantity_34
					if car.quantity_36:
						over_quan=over_quan+car.quantity_36
					if car.quantity_38:
						over_quan=over_quan+car.quantity_38
					if car.quantity_40:
						over_quan=over_quan+car.quantity_40
					if car.quantity_42:
						over_quan=over_quan+car.quantity_42
					if car.quantity_44:
						over_quan=over_quan+car.quantity_44
					if car.quantity_46:
						over_quan=over_quan+car.quantity_46
					if car.quantity_48:
						over_quan=over_quan+car.quantity_48
					if car.quantity_50:
						over_quan=over_quan+car.quantity_50
					if car.quantity_52:
						over_quan=over_quan+car.quantity_52
				quna=quantity_b2b.objects.filter(order=order,production=True)
				expected_quan=0
				carton_max=ca.objects.filter(product_Category=order.product_Category,
							product_Subcategory=order.product_Subcategory,
							product_Supercategory=order.product_Supercategory).first().maximum_quantity
				left_over=[]
				# print(quna)
				for q in quna:
					# expected_quan=expected_quan+q.quantity
					cur=0
					while cur<q.quantity:
						 cart_list_obj=cartons_list(
							name="Carton",
							address=q.address
						 )
						 to_size=int((q.quantity-cur)/carton_max)
						 if to_size==0:
							 to_size=q.quantity-cur
							 left_over.append([q.address,to_size,q.size_label,q])
							 break
						 else:
							 to_size=carton_max

						 if q.size_label==24:
							 cart_list.quantity_28=to_size
						 elif q.size_label==26:
							 cart_list_obj.quantity_26=to_size
						 elif q.size_label==28:
							 cart_list_obj.quantity_28=to_size
						 elif q.size_label==30:
							 cart_list_obj.quantity_30=to_size
						 elif q.size_label==32:
							 cart_list_obj.quantity_32=to_size
						 elif q.size_label==34:
							 cart_list_obj.quantity_34=to_size
						 elif q.size_label==36:
							 cart_list_obj.quantity_36=to_size
						 elif q.size_label==38:
							 cart_list_obj.quantity_38=to_size
						 elif q.size_label==40:
							 cart_list_obj.quantity_40=to_size
						 elif q.size_label==42:
							 cart_list_obj.quantity_42=to_size
						 elif q.size_label==44:
							 cart_list_obj.quantity_44=to_size
						 elif q.size_label==46:
							 cart_list_obj.quantity_46=to_size
						 elif q.size_label==48:
							 cart_list_obj.quantity_48=to_size
						 elif q.size_label==50:
							 cart_list_obj.quantity_50=to_size
						 elif q.size_label==52:
							 cart_list_obj.quantity_52=to_size
						 cart_list_obj.total_quantity=to_size
						 cart_list_obj.save()
						 new_map_for_color=quantity_color_map(quantity_key=q,quantity=to_size)
						 new_map_for_color.save()
						 cart_list_obj.map_for_color.add(new_map_for_color)
						 cart_list_obj.save()
						 cur=cur+to_size
						 pack_obj.cartons.add(cart_list_obj)
						 pack_obj.save()
				# print(left_over)
				for jhg in left_over:
					cart_that_allocated=cartons_list.objects.filter(
						address=jhg[0],
						fully_filled=False
					)
					for sin_cart in cart_that_allocated:
						# print(sin_cart.total_quantity,jhg[1]*.5)
						if (carton_max-sin_cart.total_quantity) >= jhg[1]:
							if jhg[2]==24:
								if sin_cart.quantity_24:
									sin_cart.quantity_24=sin_cart.quantity_24+jhg[1]
								else:
									sin_cart.quantity_24=jhg[1]
							elif jhg[2]==26:
								if sin_cart.quantity_26:
									sin_cart.quantity_26=sin_cart.quantity_26+jhg[1]
								else:
									sin_cart.quantity_26=jhg[1]
							elif jhg[2]==28:
								if sin_cart.quantity_28:
									sin_cart.quantity_28=sin_cart.quantity_28+jhg[1]
								else:
									sin_cart.quantity_28=jhg[1]
							elif jhg[2]==30:
								if sin_cart.quantity_30:
									sin_cart.quantity_30=sin_cart.quantity_30+jhg[1]
								else:
									sin_cart.quantity_30=jhg[1]
							elif jhg[2]==32:
								if sin_cart.quantity_32:
									sin_cart.quantity_32=sin_cart.quantity_32+jhg[1]
								else:
									sin_cart.quantity_32=jhg[1]
							elif jhg[2]==34:
								if sin_cart.quantity_34:
									sin_cart.quantity_34=sin_cart.quantity_34+jhg[1]
								else:
									sin_cart.quantity_34=jhg[1]
							elif jhg[2]==36:
								if sin_cart.quantity_36:
									sin_cart.quantity_36=sin_cart.quantity_36+jhg[1]
								else:
									sin_cart.quantity_36=jhg[1]
							elif jhg[2]==38:
								if sin_cart.quantity_38:
									sin_cart.quantity_38=sin_cart.quantity_38+jhg[1]
								else:
									sin_cart.quantity_38=jhg[1]
							elif jhg[2]==40:
								if sin_cart.quantity_40:
									sin_cart.quantity_40=sin_cart.quantity_40+jhg[1]
								else:
									sin_cart.quantity_40=jhg[1]
							elif jhg[2]==42:
								if sin_cart.quantity_42:
									sin_cart.quantity_42=sin_cart.quantity_42+jhg[1]
								else:
									sin_cart.quantity_42=jhg[1]
							elif jhg[2]==44:
								if sin_cart.quantity_44:
									sin_cart.quantity_44=sin_cart.quantity_44+jhg[1]
								else:
									sin_cart.quantity_44=jhg[1]
							elif jhg[2]==46:
								if sin_cart.quantity_46:
									sin_cart.quantity_46=sin_cart.quantity_46+jhg[1]
								else:
									sin_cart.quantity_46=jhg[1]
							elif jhg[2]==48:
								if sin_cart.quantity_48:
									sin_cart.quantity_48=sin_cart.quantity_48+jhg[1]
								else:
									sin_cart.quantity_48=jhg[1]
							elif jhg[2]==50:
								if sin_cart.quantity_50:
									sin_cart.quantity_50=sin_cart.quantity_50+jhg[1]
								else:
									sin_cart.quantity_50=jhg[1]
							elif jhg[2]==52:
								if sin_cart.quantity_52:
									sin_cart.quantity_52=sin_cart.quantity_52+jhg[1]
								else:
									sin_cart.quantity_52=jhg[1]
							sin_cart.total_quantity=sin_cart.total_quantity+jhg[1]
							if sin_cart.total_quantity==carton_max:
								sin_cart.fully_filled=True
							sin_cart.save()
							new_map_for_color=quantity_color_map(quantity_key=jhg[3],quantity=jhg[1])
							new_map_for_color.save()
							sin_cart.map_for_color.add(new_map_for_color)
							sin_cart.save()
							break
						else:
							obj=cartons_list(
								name="Carton",
								address=jhg[0],
								fully_filled=False,
								total_quantity=jhg[1]
							)
							if jhg[2]==24:
								obj.quantity_24=jhg[1]
							elif jhg[2]==26:
								obj.quantity_26=jhg[1]
							elif jhg[2]==28:
								obj.quantity_28=jhg[1]
							elif jhg[2]==30:
								obj.quantity_30=jhg[1]
							elif jhg[2]==32:
								obj.quantity_32=jhg[1]
							elif jhg[2]==34:
								obj.quantity_34=jhg[1]
							elif jhg[2]==36:
								obj.quantity_36=jhg[1]
							elif jhg[2]==38:
								obj.quantity_38=jhg[1]
							elif jhg[2]==40:
								obj.quantity_40=jhg[1]
							elif jhg[2]==42:
								obj.quantity_42=jhg[1]
							elif jhg[2]==44:
								obj.quantity_44=jhg[1]
							elif jhg[2]==46:
								obj.quantity_46=jhg[1]
							elif jhg[2]==48:
								obj.quantity_48=jhg[1]
							elif jhg[2]==50:
								obj.quantity_50=jhg[1]
							elif jhg[2]==52:
								obj.quantity_52=jhg[1]
							obj.save()
							new_map_for_color=quantity_color_map(quantity_key=jhg[3],quantity=jhg[1])
							new_map_for_color.save()
							obj.map_for_color.add(new_map_for_color)
							obj.save()
							pack_obj.cartons.add(obj)
							pack_obj.save()
							break
					else:
						obj=cartons_list(
							name="Carton",
							address=jhg[0],
							fully_filled=False,
							total_quantity=jhg[1]
						)
						if jhg[2]==24:
							obj.quantity_24=jhg[1]
						elif jhg[2]==26:
							obj.quantity_26=jhg[1]
						elif jhg[2]==28:
							obj.quantity_28=jhg[1]
						elif jhg[2]==30:
							obj.quantity_30=jhg[1]
						elif jhg[2]==32:
							obj.quantity_32=jhg[1]
						elif jhg[2]==34:
							obj.quantity_34=jhg[1]
						elif jhg[2]==36:
							obj.quantity_36=jhg[1]
						elif jhg[2]==38:
							obj.quantity_38=jhg[1]
						elif jhg[2]==40:
							obj.quantity_40=jhg[1]
						elif jhg[2]==42:
							obj.quantity_42=jhg[1]
						elif jhg[2]==44:
							obj.quantity_44=jhg[1]
						elif jhg[2]==46:
							obj.quantity_46=jhg[1]
						elif jhg[2]==48:
							obj.quantity_48=jhg[1]
						elif jhg[2]==50:
							obj.quantity_50=jhg[1]
						elif jhg[2]==52:
							obj.quantity_52=jhg[1]
						obj.save()
						new_map_for_color=quantity_color_map(quantity_key=jhg[3],quantity=jhg[1])
						new_map_for_color.save()
						obj.map_for_color.add(new_map_for_color)
						obj.save()
						pack_obj.cartons.add(obj)
						pack_obj.save()
			order.packing_generated=True
			order.save()
			carton=None
			if pack_obj:
				carton=pack_obj.cartons.all()
			address=order.dispatch_Address.all()
			totals_of_quan=[0]*15
			for kjh in carton:
				if kjh.quantity_24:
					totals_of_quan[0]+=kjh.quantity_24
				if kjh.quantity_26:
					totals_of_quan[1]+=kjh.quantity_26
				if kjh.quantity_28:
					totals_of_quan[2]+=kjh.quantity_28
				if kjh.quantity_30:
					totals_of_quan[3]+=kjh.quantity_30
				if kjh.quantity_32:
					totals_of_quan[4]+=kjh.quantity_32
				if kjh.quantity_34:
					totals_of_quan[5]+=kjh.quantity_34
				if kjh.quantity_36:
					totals_of_quan[6]+=kjh.quantity_36
				if kjh.quantity_38:
					totals_of_quan[7]+=kjh.quantity_38
				if kjh.quantity_40:
					totals_of_quan[8]+=kjh.quantity_40
				if kjh.quantity_42:
					totals_of_quan[9]+=kjh.quantity_42
				if kjh.quantity_44:
					totals_of_quan[10]+=kjh.quantity_44
				if kjh.quantity_46:
					totals_of_quan[11]+=kjh.quantity_46
				if kjh.quantity_48:
					totals_of_quan[12]+=kjh.quantity_48
				if kjh.quantity_50:
					totals_of_quan[13]+=kjh.quantity_50
				if kjh.quantity_52:
					totals_of_quan[14]+=kjh.quantity_52

			# print(carton)



# for i in range(26,53,2):
# 	print("""						elif jhg[2]=="""+str(i)+""":
# 							if sin_cart.quantity_"""+str(i)+""":
# 								sin_cart.quantity_"""+str(i)+"""=sin_cart.quantity_"""+str(i)+"""+jhg[1]
# 							else:
# 								sin_cart.quantity_"""+str(i)+"""=jhg[1]""")
# for i in range(26,53,2):
# 	print("""				elif jhg[2]=="""+str(i)+""":
# 					cart_that_allocated.filter(quantity_"""+str(i)+"""_lt=carton_max)""")
			# act=activities_Category.objects.filter(request_Forms=form).last()

			data={
				"pack_obj":pack_obj,
				"address":address,
				"order":order,
				"carton":carton,
				"totals":totals_of_quan
			}
			if request.POST.get('quantity_ajax_per_carton'):
				quantity_ajax=request.POST.get('quantity_ajax_per_carton')
				quantity_label_ajax=request.POST.get('quantity_label_ajax')
				carton_id_ajax=request.POST.get('carton_id_ajax')
				carton_obj_per_add=cartons_list.objects.filter(id=int(carton_id_ajax)).first()
				if quantity_label_ajax=='24':
					jk=carton_obj_per_add.quantity_24
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_24=quantity_ajax
				elif quantity_label_ajax=='26':
					jk=carton_obj_per_add.quantity_26
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_26=quantity_ajax
				elif quantity_label_ajax=='28':
					jk=carton_obj_per_add.quantity_28
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_28=quantity_ajax
				elif quantity_label_ajax=='30':
					jk=carton_obj_per_add.quantity_30
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_30=quantity_ajax
				elif quantity_label_ajax=='32':
					jk=carton_obj_per_add.quantity_32
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_32=quantity_ajax
				elif quantity_label_ajax=='34':
					jk=carton_obj_per_add.quantity_34
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_34=quantity_ajax
				elif quantity_label_ajax=='36':
					jk=carton_obj_per_add.quantity_36
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_36=quantity_ajax
				elif quantity_label_ajax=='38':
					jk=carton_obj_per_add.quantity_38
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_38=quantity_ajax
				elif quantity_label_ajax=='40':
					jk=carton_obj_per_add.quantity_40
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_40=quantity_ajax
				elif quantity_label_ajax=='42':
					jk=carton_obj_per_add.quantity_42
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_42=quantity_ajax
				elif quantity_label_ajax=='44':
					jk=carton_obj_per_add.quantity_44
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_44=quantity_ajax
				elif quantity_label_ajax=='46':
					jk=carton_obj_per_add.quantity_46
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_46=quantity_ajax
				elif quantity_label_ajax=='48':
					jk=carton_obj_per_add.quantity_48
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_48=quantity_ajax
				elif quantity_label_ajax=='50':
					jk=carton_obj_per_add.quantity_50
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_50=quantity_ajax
				elif quantity_label_ajax=='52':
					jk=carton_obj_per_add.quantity_52
					if not(jk):
						jk=0
					carton_obj_per_add.total_quantity+=(int(quantity_ajax)-int(jk))
					carton_obj_per_add.quantity_52=quantity_ajax
				carton_obj_per_add.save()
				return HttpResponse(json.dumps({"bol":True}), content_type="application/json")
			if request.POST.get('no_of_carton'):
				if pack_obj:
					obj=pack_obj
				else:
					obj=packing_list(
						name="Packing("+str(order.order_no)+")",
						order=order
						)
					obj.save()
				no_of_carton=int(request.POST.get('no_of_carton'))
				for i in range(1,no_of_carton+1):
					addr=address_model.objects.filter(id=int(request.POST.get('address'+str(i)))).first()
					obj1=cartons_list(
						name=request.POST.get('name'+str(i)),
						address=addr
						)
					if request.POST.get('size28_'+str(i)):
						obj1.quantity_28=int(request.POST.get('size28_'+str(i)))
					if request.POST.get('size30_'+str(i)):
						obj1.quantity_30=int(request.POST.get('size30_'+str(i)))
					if request.POST.get('size32_'+str(i)):
						obj1.quantity_32=int(request.POST.get('size32_'+str(i)))
					if request.POST.get('size34_'+str(i)):
						obj1.quantity_34=int(request.POST.get('size34_'+str(i)))
					if request.POST.get('size36_'+str(i)):
						obj1.quantity_36=int(request.POST.get('size36_'+str(i)))
					if request.POST.get('size38_'+str(i)):
						obj1.quantity_38=int(request.POST.get('size38_'+str(i)))
					if request.POST.get('size40_'+str(i)):
						obj1.quantity_40=int(request.POST.get('size40_'+str(i)))
					if request.POST.get('size42_'+str(i)):
						obj1.quantity_42=int(request.POST.get('size42_'+str(i)))
					obj1.save()
					obj.cartons.add(obj1)
					obj.save()
			return render(request,"staff/staff_profile_packing_list.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





def staff_profile_distribution_list(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		staff_cate=staff_Categories.objects.filter(name="Merchandising").first()
		staff_cate1=staff_Categories.objects.filter(name="Sales").first()
		if details.staff_category==staff_cate or details.staff_category==staff_cate1:
			order=company_Order.objects.filter(order_no=order_no).first()
			distri_obj=distribution_list.objects.filter(order=order)
			if distri_obj:
				pass
			addr=order.dispatch_Address.all()
			data={
				"distri_obj":distri_obj,
				"order":order,
				"address":addr
			}
			if request.POST.get('no_of_carton'):
				no_of_carton=int(request.POST.get('no_of_carton'))
				for i in range(1,no_of_carton+1):
					addr=address_model.objects.filter(id=int(request.POST.get('address'+str(i)))).first()
					obj=distribution_list(
						address=addr,
						order=order,
						name=request.POST.get('name'+str(i))
						)
					if request.POST.get('size28_'+str(i)):
						obj.quantity_28=int(request.POST.get('size28_'+str(i)))
					if request.POST.get('size30_'+str(i)):
						obj.quantity_30=int(request.POST.get('size30_'+str(i)))
					if request.POST.get('size32_'+str(i)):
						obj.quantity_32=int(request.POST.get('size32_'+str(i)))
					if request.POST.get('size34_'+str(i)):
						obj.quantity_34=int(request.POST.get('size34_'+str(i)))
					if request.POST.get('size36_'+str(i)):
						obj.quantity_36=int(request.POST.get('size36_'+str(i)))
					if request.POST.get('size38_'+str(i)):
						obj.quantity_38=int(request.POST.get('size38_'+str(i)))
					if request.POST.get('size40_'+str(i)):
						obj.quantity_40=int(request.POST.get('size40_'+str(i)))
					if request.POST.get('size42_'+str(i)):
						obj.quantity_42=int(request.POST.get('size42_'+str(i)))
					obj.save()
				data["distri_obj"]=distribution_list.objects.filter(order=order)

			return render(request,"staff/staff_profile_distribution_list.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')








def staff_profile_cummlative(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		staff_cate=staff_Categories.objects.filter(name="Merchandising").first()
		staff_cate1=staff_Categories.objects.filter(name="Sales").first()
		sel_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		if details.staff_category==staff_cate or details.staff_category==staff_cate1 or details.seller_category==sel_cate:
			order=company_Order.objects.filter(order_no=order_no).first()
			pack_obj=packing_list.objects.filter(order=order).first()
			carton=None
			if pack_obj:
				carton=pack_obj.cartons.all()
				quantity_28=0
				quantity_30=0
				quantity_32=0
				quantity_34=0
				quantity_36=0
				quantity_38=0
				quantity_40=0
				quantity_42=0
				for i in carton:
					if i.quantity_28:
						quantity_28=quantity_28+i.quantity_28
					if i.quantity_30:
						quantity_30=quantity_30+i.quantity_30
					if i.quantity_32:
						quantity_32=quantity_32+i.quantity_32
					if i.quantity_34:
						quantity_34=quantity_34+i.quantity_34
					if i.quantity_36:
						quantity_36=quantity_36+i.quantity_36
					if i.quantity_38:
						quantity_38=quantity_38+i.quantity_38
					if i.quantity_40:
						quantity_40=quantity_40+i.quantity_40
					if i.quantity_42:
						quantity_42=quantity_42+i.quantity_42
			li=[quantity_28,quantity_30,quantity_32,quantity_34,quantity_36,quantity_38,quantity_40,quantity_42]
			distri_obj=distribution_list.objects.filter(order=order)
			li1=[0,0,0,0,0,0,0,0]
			for i in distri_obj:
				if i.quantity_28:
					li1[0]=li1[0]+i.quantity_28
				if i.quantity_30:
					li1[1]=li1[1]+i.quantity_30
				if i.quantity_32:
					li1[2]=li1[2]+i.quantity_32
				if i.quantity_34:
					li1[3]=li1[3]+i.quantity_34
				if i.quantity_36:
					li1[4]=li1[4]+i.quantity_36
				if i.quantity_38:
					li1[5]=li1[5]+i.quantity_38
				if i.quantity_40:
					li1[6]=li1[6]+i.quantity_40
				if i.quantity_42:
					li1[7]=li1[7]+i.quantity_42
			quan_obj=quantity_b2b.objects.filter(order=order,production=True)
			li2=[0,0,0,0,0,0,0,0]
			for i in quan_obj:
				if i.size_label==28:
					li2[0]=li2[0]+i.quantity
				elif i.size_label==30:
					li2[1]=li2[1]+i.quantity
				elif i.size_label==32:
					li2[2]=li2[2]+i.quantity
				elif i.size_label==34:
					li2[3]=li2[3]+i.quantity
				elif i.size_label==36:
					li2[4]=li2[4]+i.quantity
				elif i.size_label==38:
					li2[5]=li2[5]+i.quantity
				elif i.size_label==40:
					li2[6]=li2[6]+i.quantity
				elif i.size_label==42:
					li2[7]=li2[7]+i.quantity
			pack_short=[li2[0]-li[0],li2[1]-li[1],li2[2]-li[2],li2[3]-li[3],li2[4]-li[4],li2[5]-li[5],li2[6]-li[6],li2[7]-li[7]]
			over_short=[li2[0]-li1[0],li2[1]-li1[1],li2[2]-li1[2],li2[3]-li1[3],li2[4]-li1[4],li2[5]-li1[5],li2[6]-li1[6],li2[7]-li1[7]]
			pack_total=0
			distri_total=0
			size_assort=0
			pack_short_total=0
			over_short_total=0
			for i in li:
				pack_total=pack_total+i
			for i in li1:
				distri_total=distri_total+i
			for i in li2:
				size_assort=size_assort+i
			for i in pack_short:
				pack_short_total=pack_short_total+i
			for i in over_short:
				over_short_total=over_short_total+i
			data={
			"li":li,
			"li1":li1,
			"li2":li2,
			"pack_short":pack_short,
			"over_short":over_short,
			"order":order,
			"pack_total":pack_total,
			"distri_total":distri_total,
			"size_assort":size_assort,
			"pack_short_total":pack_short_total,
			"over_short_total":over_short_total
			}
			return render(request,"staff/cummlative.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')






def staff_profile_basic_order(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff or details.vendor:
			order=company_Order.objects.filter(order_no=order_no).first()
			data={
				"order":order
			}
			return render(request,'staff/staff_profile_basic_order.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')






from b2b.models import carton





def vendor_activities_page(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.get(email=request.user.email)
		orders=company_Order.objects.filter(staffs_Allocated=details)
		acti=activities.objects.filter(user=details)
		li=[]
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		for ik in acti:
			if details.position=='C':
				if ik.custom_date is None:
					d1=datetime.datetime(ik.planned_date.year,
						ik.planned_date.month,
						ik.planned_date.day)
				else:
					d1=datetime.datetime(ik.custom_date.year,
						ik.custom_date.month,
						ik.custom_date.day)
				d1=d1+datetime.timedelta(days=ik.activity_Cate.escalation_Time_for_Executive)
				d2=datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,
					datetime.datetime.now().day)
				if d1>d2:
					to_be_staff=ik.order.staffs_Allocated.all().filter(position='M')
					for jk in to_be_staff:
						ik.esclated_user.add(jk)
						obj3=notifications.objects.filter(description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") (Activity Slug - "+str(ik.slug)+")",
							user=jk)
						if obj3.count()==0:
							obj3=notifications(
								title="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+")",
								description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") (Activity Slug - "+str(ik.slug)+")",
								user=jk,
								link="/userdetail/staff_profile/activity/"+str(ik.slug),
								type_of_order=ik.order.order_type
								)
							obj3.save()
							obj3.link=obj3.link+"?noti="+str(obj3.id)
							obj3.save()
			elif details.position=='M':
				if ik.custom_date is None:
					d1=datetime.datetime(ik.planned_date.year,
						ik.planned_date.month,
						ik.planned_date.day)
				else:
					d1=datetime.datetime(ik.custom_date.year,
						ik.custom_date.month,
						ik.custom_date.day)
				d1=d1+datetime.timedelta(days=ik.activity_Cate.escalation_Time_for_Manager)
				d2=datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,
					datetime.datetime.now().day)
				if d1>d2:
					to_be_staff=ik.order.staffs_Allocated.all().filter(position='H')
					for jk in to_be_staff:
						ik.esclated_user.add(jk)
						obj3=notifications.objects.filter(description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") "+"(Activity Slug - "+str(ik.slug)+")",
							user=jk)
						if obj3.count()==0:
							obj3=notifications(
								title="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+")",
								description="New Activity Escalated to you (Order No. - "+str(ik.order.order_no)+") "+"(Activity Slug - "+str(ik.slug)+")",
								user=jk,
								link="/userdetail/staff_profile/activity/"+str(ik.slug),
								type_of_order=ik.order.order_type
								)
							obj3.save()
							obj3.link=obj3.link+"?noti="+str(obj3.id)
							obj3.save()
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		#######################################Escalating Activity ##########################
		orders_filter=[]
		pickup_address=[]
		delivery_address=[]
		for o in orders:
			hgf_acti=activities.objects.filter(user=details,order=o)
			car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
			length=car.length
			breadth=car.breadth
			height=car.heigth
			vol=length*breadth*height
			if hgf_acti.count()>0:
				li.append([hgf_acti,length,breadth,height,vol])
				orders_filter.append(o)
				for i in hgf_acti:
					if i.logistics_pickup_user not in pickup_address:
						pickup_address.append(i.logistics_pickup_user)
					if i.logistics_delivery_user not in delivery_address:
						delivery_address.append(i.logistics_delivery_user)
		# print(li)
		oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
		oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
		oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
		oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
		oty4=oty1+oty2+oty3+oty
		# print(oty4)
		oyu=seller_Categories.objects.filter(name="Logistic Vendor").first()
		logi=False
		if details.seller_category==oyu:
			logi=True
		ogt=company_Order.objects.filter(order_no=2019000008).first()
		# print("here",ogt.packing_list_set.all().first().cartons)
		data={
			"deactivated":True,
			"data":details,
			"obj":None,
			"head":False,
			"staff":False,
			"manager":False,
			"acti":li,
			"current":datetime.datetime.now().date,
			"oty":oty,
			"oty1":oty1,
			"oty2":oty2,
			"oty3":oty3,
			"oty4":oty4,
			"logistics":logi,
			"orders_filter":orders_filter,
			"pickup_address":pickup_address,
			"delivery_address":delivery_address
		}
		if details.vendor:
			if details.activate_Seller:
				data["deactivated"]=False
			if request.GET.get('order') and request.GET.get('order')!="":
				# print("Wrong")
				order_no=int(request.GET.get('order'))
				orderkl=company_Order.objects.filter(order_no=order_no).first()
				li=[]
				hgf_acti=activities.objects.filter(user=details,order=orderkl)
				car=carton.objects.filter(product_Supercategory=orderkl.product_Supercategory).first()
				length=car.length
				breadth=car.breadth
				height=car.heigth
				vol=length*breadth*height
				if hgf_acti.count()>0:
					li.append([hgf_acti,length,breadth,height,vol])
				data["acti"]=li
			if request.GET.get('pickup_add') and request.GET.get('pickup_add')!="":
				pickup=detail.objects.filter(email=request.GET.get('pickup_add')).first()
				li=[]
				for i in data["acti"]:
					li1=[]
					for j in i[0]:
						if j.logistics_pickup_user==pickup:
							li1.append(j)
					car=carton.objects.filter(product_Supercategory=j.order.product_Supercategory)
					length=car.length
					breadth=car.breadth
					height=car.heigth
					vol=length*breadth*height
					if li1!=[]:
						li.append([li1,length,breadth,height,vol])
				data["acti"]=li
			if request.GET.get('delivery_add') and request.GET.get('delivery_add')!="":
				delivery=detail.objects.filter(email=request.GET.get('delivery_add')).first()
				li=[]
				for i in data["acti"]:
					li1=[]
					for j in i[0]:
						if j.logistics_delivery_user==delivery:
							li1.append(j)
					car=carton.objects.filter(product_Supercategory=j.order.product_Supercategory).first()
					length=car.length
					breadth=car.breadth
					height=car.heigth
					vol=length*breadth*height
					if li1!=[]:
						li.append([li1,length,breadth,height,vol])
				data["acti"]=li
			if request.GET.get('pickup_date') and request.GET.get('pickup_date')!="":
				pickup_date=datetime.datetime.strptime(request.GET.get('pickup_date'),"%Y-%m-%d")
				# pickup_date=pickup_date.date
				li=[]
				for i in data["acti"]:
					li1=[]
					for j in i[0]:
						ojk=datetime.datetime.strptime(str(j.planned_date.year)+str(j.planned_date.month)+str(j.planned_date.day),"%Y%m%d")
						if ojk==pickup_date:
							li1.append(j)
					car=carton.objects.filter(product_Supercategory=j.order.product_Supercategory).first()
					length=car.length
					breadth=car.breadth
					height=car.heigth
					vol=length*breadth*height
					if li1!=[]:
						li.append([li1,length,breadth,height,vol])
				data["acti"]=li
			if request.GET.get('delivery_date') and request.GET.get('delivery_date')!="":
				delivery_date=datetime.datetime.strptime(request.GET.get('delivery_date'),"%Y-%m-%d")
				li=[]
				for i in data["acti"]:
					li1=[]
					for j in i[0]:
						ojk=datetime.datetime.strptime(str(j.logistics_delivery_date.year)+str(j.logistics_delivery_date.month)+str(j.logistics_delivery_date.day),"%Y%m%d")
						if ojk==delivery_date:
							li1.append(j)
					car=carton.objects.filter(product_Supercategory=j.order.product_Supercategory).first()
					length=car.length
					breadth=car.breadth
					height=car.heigth
					vol=length*breadth*height
					if li1!=[]:
						li.append([li1,length,breadth,height,vol])
				data["acti"]=li
			if request.GET.get('request_date') and request.GET.get('request_date')!="":
				request_date=datetime.datetime.strptime(request.GET.get('request_date'),"%Y-%m-%d")
				li=[]
				for i in data["acti"]:
					li1=[]
					for j in i[0]:
						ojk=datetime.datetime.strptime(str(j.created_on.year)+str(j.created_on.month)+str(j.created_on.day),"%Y%m%d")
						if ojk==request_date:
							li1.append(j)
					car=carton.objects.filter(product_Supercategory=j.order.product_Supercategory).first()
					length=car.length
					breadth=car.breadth
					height=car.heigth
					vol=length*breadth*height
					if li1!=[]:
						li.append([li1,length,breadth,height,vol])
				data["acti"]=li

			if request.GET.get('filter'):
				filter_by=request.GET.get('filter')
				if filter_by=='today':
					li=[]
					for o in orders:
						hgf_acti=activities.objects.filter(user=details,order=o,planned_date__day=datetime.datetime.now().day,
							planned_date__month=datetime.datetime.now().month,
							planned_date__year=datetime.datetime.now().year)
						car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
						length=car.length
						breadth=car.breadth
						height=car.heigth
						vol=length*breadth*height
						if hgf_acti.count()>0:
							li.append([hgf_acti,length,breadth,height,vol])
					data["acti"]=li
				if filter_by=='pending':
					li=[]
					for o in orders:
						hgf_acti=activities.objects.filter(user=details,order=o,planned_date__day__lt=datetime.datetime.now().day,
							planned_date__month=datetime.datetime.now().month,
							planned_date__year=datetime.datetime.now().year)
						car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
						length=car.length
						breadth=car.breadth
						height=car.heigth
						vol=length*breadth*height
						if hgf_acti.count()>0:
							li.append([hgf_acti,length,breadth,height,vol])
					data["acti"]=li
				if filter_by=='enquiry':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='E')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
						length=car.length
						breadth=car.breadth
						height=car.heigth
						vol=length*breadth*height
						if hgf_acti.count()>0:
							li.append([hgf_acti,length,breadth,height,vol])
					data["acti"]=li
				if filter_by=='sampling':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='S')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
						length=car.length
						breadth=car.breadth
						height=car.heigth
						vol=length*breadth*height
						if hgf_acti.count()>0:
							li.append([hgf_acti,length,breadth,height,vol])
					data["acti"]=li
				if filter_by=='design':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='D')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
						length=car.length
						breadth=car.breadth
						height=car.heigth
						vol=length*breadth*height
						if hgf_acti.count()>0:
							li.append([hgf_acti,length,breadth,height,vol])
					data["acti"]=li
				if filter_by=='order':
					li=[]
					for o in orders:
						ohj=activities_Category.objects.filter(type_of_order='O')
						hgf_acti=activities.objects.filter(user=details,order=o,
							activity_Cate__in=ohj)
						car=carton.objects.filter(product_Supercategory=o.product_Supercategory).first()
						length=car.length
						breadth=car.breadth
						height=car.heigth
						vol=length*breadth*height
						if hgf_acti.count()>0:
							li.append([hgf_acti,length,breadth,height,vol])
					data["acti"]=li
			if request.POST.get('lap_activity_ajax'):
				lap=int(request.POST.get('lap_activity_ajax'))
				acti=int(request.POST.get('activity_ajax_cate'))
				obj=activities.objects.filter(id=acti).first()
				# obj.lap=lap
				# obj.custom_date=obj.created_on+datetime.timedelta(days=obj.lap)
				# owq=activities_Category.objects.filter(linked_activity=obj.activity_Cate)
				# for o in owq:
				# 	owqt=activities.objects.filter(user=details,activity_Cate=o,order=obj.order)
				# 	# print(owqt)
				# 	if owqt.count()>0:
				# 		owqt=owqt.first()
				# 		if owqt.lap is None:
				# 			owqt.lap=0
				# 		owqt.lap=obj.lap+owqt.activity_Cate.Increment_or_Decrement
				# 		owqt.custom_date=owqt.created_on+datetime.timedelta(days=owqt.lap)
				# 		owqt.save()
				# obj.save()
				custom_date_check(activity=obj.activity_Cate,order=obj.order,lap=lap)
				return HttpResponse(json.dumps({"bol":True}), content_type="application/json")
			if request.POST.get('lr_activity_ajax'):
				lr=int(request.POST.get('lr_activity_ajax'))
				acti=int(request.POST.get('activity_ajax_cate'))
				obj=activities.objects.filter(id=acti).first()
				obj.lr_number=lr
				obj.save()
				return HttpResponse(json.dumps({"bol":True}), content_type="application/json")
			if request.POST.get('actual_date_activity_ajax'):
				actual_date=parse_date(request.POST.get('actual_date_activity_ajax'))
				acti=int(request.POST.get('activity_ajax_cate'))
				obj=activities.objects.filter(id=acti).first()
				obj.actual_date=actual_date
				obj.save()
				out=activity_tentative_date_update(activity=obj,
				order=obj.order)
				# if out:
					# print("\hn\n\n\n\n\n\n\nHere it Works")
				# query=detail.objects.filter(staff=True,position='H',staff_category=details.staff_category)
				# query=query.exclude(email=details.email)
				# for i in query:
				# 	a=notifications(
				# 		title="Activity is Updated by"+str(details.name),
				# 		description="This Activity is updated by the user("+str(details.email)+")",
				# 		user=i,
				# 		link="/userdetail/staff_profile/activity/"+str(obj.slug)
				# 		)
				# 	a.save()
				# 	a.link=a.link+"?noti="+str(a.id)
				# 	a.save()
				# query=detail.objects.filter(staff=True,position='M',staff_category=details.staff_category)
				# query=query.exclude(email=details.email)
				# for i in query:
				# 	a=notifications(
				# 		title="Activity is Updated by"+str(details.name),
				# 		description="This Activity is updated by the user("+str(details.email)+")",
				# 		user=i,
				# 		link="/userdetail/staff_profile/activity/"+str(activity_slug)
				# 		)
				# 	a.save()
				# 	a.link=a.link+"?noti="+str(a.id)
				# 	a.save()
				return HttpResponse(json.dumps({"bol":True}), content_type="application/json")
			return render(request,'vendor/vendor_activities_page.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



		vendor_profile_vendors








def vendor_profile_vendors(request):
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
			data={
				"vend":mana,
				"oty":oty,
				"oty1":oty1,
				"oty2":oty2,
				"oty3":oty3,
				"oty4":oty4
			}
			return render(request,'vendor/vendor_profile_vendors.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')










def logistic_request(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		staf_cate=staff_Categories.objects.filter(name="Merchandising").first()
		sel_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		if details.staff_category==staf_cate or details.seller_category==sel_cate:
			order=company_Order.objects.filter(order_no=order_no).first()
			data={
				"order":order
			}
			if request.POST.get('pickup'):
				pickup_user=detail.objects.filter(email=request.POST.get('pickup')).first()
				delivery_user=detail.objects.filter(email=request.POST.get('delivery')).first()
				pickup_date=datetime.datetime.strptime(request.POST.get('pickup_date'), "%Y-%m-%d").date()
				delivery_date=datetime.datetime.strptime(request.POST.get('delivery_date'), "%Y-%m-%d").date()
				sel_cate=seller_Categories.objects.filter(name="Logistic Vendor").first()
				user_to=order.staffs_Allocated.all().filter(seller_category=sel_cate).first()
				if user_to:
					acti_cate=activities_Category.objects.filter(title="Logistics Pickup").first()
					# print(user_to)
					obj=activities(
							user=user_to,
							activity_Cate=acti_cate,
							slug=str(user_to.email)+"_"+str(acti_cate)+"_"+str(order.order_no),
							planned_date=pickup_date,
							logistics_delivery_date=delivery_date,
							order=order,
							logistics_pickup_address=pickup_user.address,
							logistics_delivery_address=delivery_user.address
						)
					obj.save()
					obj.slug=str(obj.slug)+str(obj.id)
					obj.logistics_pickup_user=pickup_user
					obj.logistics_delivery_user=delivery_user
					acti_final=activities_Category.objects.filter(title="Garment Final Inspection").first()
					acti_final=activities.objects.filter(activity_Cate=acti_final,order=order).first()
					if acti_final:
						acti_final=acti_final.actual_date
					else:
						acti_final=datetime.datetime.now()
					obj.logistics_invoice_date=acti_final
					obj.save()
					acti_marked=activities_Category.objects.filter(factory_Dispatch_Activity=True)
					for i in acti_marked:
						act=activities.objects.filter(order=order,activity_Cate=i).first()
						if act:
							act.actual_date=datetime.datetime.now()
							act.save()
							out=activity_tentative_date_update(activity=act,order=order)
					# print(obj.planned_date,obj.logistics_delivery_date)
					if details.staff:
						return redirect('/userdetail/staff_profile')
					else:
						return redirect('/userdetail/vendor_profile')
				else:
					data["vendor_not"]=True
			return render(request,"staff/logistics_request.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




from b2b.models import quality_evaluation as qe
from b2b.models import quality_deflection



def quality_evaluation(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		quality_cate=staff_Categories.objects.filter(name="Quality").first()
		garment_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		quality=False
		garment=False
		if details and details.staff_category==quality_cate:
			quality=True
		elif details and details.seller_category==garment_cate:
			garment=True
		if details.staff_category==quality_cate or details.seller_category==garment_cate:
			order=company_Order.objects.filter(order_no=order_no).first()
			sizes_avail=quantity_b2b.objects.filter(order=order)
			sizes=[]
			for i in sizes_avail:
				if not(i.size_label in sizes):
					sizes.append(i.size_label)
			# print(sizes)
			if quality:
				qesd=qe.objects.filter(order=order,by_quality=True)
			else:
				qesd=qe.objects.filter(order=order,by_factory=True)
			li={}
			li1=[]
			for klj in qesd:
				if klj.label in li:
					li[klj.label].append(klj)
				else:
					li1.append(klj.label)
					li[klj.label]=[klj]
			li2=[]
			for klj in li1:
				li2.append(li[klj])

			pom_obj=POM.objects.filter(product_Category=order.product_Category,
				product_Subcategory=order.product_Subcategory,
				product_Supercategory=order.product_Supercategory)
			pom=[]
			for i in pom_obj:
				pom.append(i.label)
			print(li2)
			data={
				"order":order,
				"sizes":sizes,
				"qe":li2,
				"pom":pom
			}
			if request.POST.get('quality_ajax_size') and request.POST.get('quality_ajax_eval'):
				size_label=int(request.POST.get('quality_ajax_size'))
				pom_obj=POM.objects.filter(product_Category=order.product_Category,
					product_Subcategory=order.product_Subcategory,
					product_Supercategory=order.product_Supercategory)
				pom=[]
				for i in pom_obj:
					pom.append(i.label)
				meas_obj=measurement.objects.filter(
						label=order.label,
						fit=order.fit,
						season=order.season,
						product_Category=order.product_Category,
						product_Subcategory=order.product_Subcategory,
						product_Supercategory=order.product_Supercategory
					).first()
				times=size_label-meas_obj.name
				attribute1=None
				attribute2=None
				attribute3=None
				attribute4=None
				attribute5=None
				attribute6=None
				attribute7=None
				attribute8=None
				attribute9=None
				attribute10=None
				attribute11=None
				attribute12=None
				attribute13=None
				attribute14=None
				attribute15=None
				attribute16=None
				attribute17=None
				attribute18=None
				attribute19=None
				attribute20=None
				attribute21=None
				attribute22=None
				attribute23=None
				attribute24=None
				attribute25=None
				attribute26=None
				attribute27=None
				attribute28=None
				attribute29=None
				attribute30=None
				if meas_obj.attribute1:
					attribute1=meas_obj.attribute1+(times*meas_obj.grading1)
				if meas_obj.attribute2:
					attribute2=meas_obj.attribute2+(times*meas_obj.grading2)
				if meas_obj.attribute3:
					attribute3=meas_obj.attribute3+(times*meas_obj.grading3)
				if meas_obj.attribute4:
					attribute4=meas_obj.attribute4+(times*meas_obj.grading4)
				if meas_obj.attribute5:
					attribute5=meas_obj.attribute5+(times*meas_obj.grading5)
				if meas_obj.attribute6:
					attribute6=meas_obj.attribute6+(times*meas_obj.grading6)
				if meas_obj.attribute7:
					attribute7=meas_obj.attribute7+(times*meas_obj.grading7)
				if meas_obj.attribute8:
					attribute8=meas_obj.attribute8+(times*meas_obj.grading8)
				if meas_obj.attribute9:
					attribute9=meas_obj.attribute9+(times*meas_obj.grading9)
				if meas_obj.attribute10:
					attribute10=meas_obj.attribute10+(times*meas_obj.grading10)
				if meas_obj.attribute11:
					attribute11=meas_obj.attribute11+(times*meas_obj.grading11)
				if meas_obj.attribute12:
					attribute12=meas_obj.attribute12+(times*meas_obj.grading12)
				if meas_obj.attribute13:
					attribute13=meas_obj.attribute13+(times*meas_obj.grading13)
				if meas_obj.attribute14:
					attribute14=meas_obj.attribute14+(times*meas_obj.grading14)
				if meas_obj.attribute15:
					attribute15=meas_obj.attribute15+(times*meas_obj.grading15)
				if meas_obj.attribute16:
					attribute16=meas_obj.attribute16+(times*meas_obj.grading16)
				if meas_obj.attribute17:
					attribute17=meas_obj.attribute17+(times*meas_obj.grading17)
				if meas_obj.attribute18:
					attribute18=meas_obj.attribute18+(times*meas_obj.grading18)
				if meas_obj.attribute19:
					attribute19=meas_obj.attribute19+(times*meas_obj.grading19)
				if meas_obj.attribute20:
					attribute20=meas_obj.attribute20+(times*meas_obj.grading20)
				if meas_obj.attribute21:
					attribute21=meas_obj.attribute21+(times*meas_obj.grading21)
				if meas_obj.attribute22:
					attribute22=meas_obj.attribute22+(times*meas_obj.grading22)
				if meas_obj.attribute23:
					attribute23=meas_obj.attribute23+(times*meas_obj.grading23)
				if meas_obj.attribute24:
					attribute24=meas_obj.attribute24+(times*meas_obj.grading24)
				if meas_obj.attribute25:
					attribute25=meas_obj.attribute25+(times*meas_obj.grading25)
				if meas_obj.attribute26:
					attribute26=meas_obj.attribute26+(times*meas_obj.grading26)
				if meas_obj.attribute27:
					attribute27=meas_obj.attribute27+(times*meas_obj.grading27)
				if meas_obj.attribute28:
					attribute28=meas_obj.attribute28+(times*meas_obj.grading28)
				if meas_obj.attribute29:
					attribute29=meas_obj.attribute29+(times*meas_obj.grading29)
				if meas_obj.attribute30:
					attribute30=meas_obj.attribute30+(times*meas_obj.grading30)
				ajax_data={
					"pom":pom,
					'attribute1':attribute1,
					"tolerance1":meas_obj.tolerance1,
					'attribute2':attribute2,
					"tolerance2":meas_obj.tolerance2,
					'attribute3':attribute3,
					"tolerance3":meas_obj.tolerance3,
					'attribute4':attribute4,
					"tolerance4":meas_obj.tolerance4,
					'attribute5':attribute5,
					"tolerance5":meas_obj.tolerance5,
					'attribute6':attribute6,
					"tolerance6":meas_obj.tolerance6,
					'attribute7':attribute7,
					"tolerance7":meas_obj.tolerance7,
					'attribute8':attribute8,
					"tolerance8":meas_obj.tolerance8,
					'attribute9':attribute9,
					"tolerance9":meas_obj.tolerance9,
					'attribute10':attribute10,
					"tolerance10":meas_obj.tolerance10,
					'attribute11':attribute11,
					"tolerance11":meas_obj.tolerance11,
					'attribute12':attribute12,
					"tolerance12":meas_obj.tolerance12,
					'attribute13':attribute13,
					"tolerance13":meas_obj.tolerance13,
					'attribute14':attribute14,
					"tolerance14":meas_obj.tolerance14,
					'attribute15':attribute15,
					"tolerance15":meas_obj.tolerance15,
					'attribute16':attribute16,
					"tolerance16":meas_obj.tolerance16,
					'attribute17':attribute17,
					"tolerance17":meas_obj.tolerance17,
					'attribute18':attribute18,
					"tolerance18":meas_obj.tolerance18,
					'attribute19':attribute19,
					"tolerance19":meas_obj.tolerance19,
					'attribute20':attribute20,
					"tolerance20":meas_obj.tolerance20,
					'attribute21':attribute21,
					"tolerance21":meas_obj.tolerance21,
					'attribute22':attribute22,
					"tolerance22":meas_obj.tolerance22,
					'attribute23':attribute23,
					"tolerance23":meas_obj.tolerance23,
					'attribute24':attribute24,
					"tolerance24":meas_obj.tolerance24,
					'attribute25':attribute25,
					"tolerance25":meas_obj.tolerance25,
					'attribute26':attribute26,
					"tolerance26":meas_obj.tolerance26,
					'attribute27':attribute27,
					"tolerance27":meas_obj.tolerance27,
					'attribute28':attribute28,
					"tolerance28":meas_obj.tolerance28,
					'attribute29':attribute29,
					"tolerance29":meas_obj.tolerance29,
					'attribute30':attribute30,
					"tolerance30":meas_obj.tolerance30,
				}
				return HttpResponse(json.dumps({'data': ajax_data}), content_type="application/json")
			if request.POST.get('size'):
				# print(request.POST)
				size_label=request.POST.get('size')
				no_eval=int(request.POST.get('no_eval'))
				pom_obj=POM.objects.filter(product_Category=order.product_Category,
					product_Subcategory=order.product_Subcategory,
					product_Supercategory=order.product_Supercategory)
				pom=[]
				for i in pom_obj:
					pom.append(i.label)
				for i in range(1,no_eval+1):
					osf=qe(
						order=order,
						label=size_label,
					)
					if quality:
						osf.by_quality=True
					else:
						osf.by_factory=True
					osf.save()
					c=1
					for j in pom:
						obj=POM.objects.filter(label=j,product_Category=order.product_Category,
							product_Subcategory=order.product_Subcategory,
							product_Supercategory=order.product_Supercategory).first()
						defle=request.POST.get('deflection_'+j.replace('"','')+'_'+str(i))
						# print('deflection_'+j.replace('"','')+'_'+str(i))
						# print(defle)
						reme=request.POST.get('remark_'+j.replace('"','')+'_'+str(c))
						# print('remark_'+j.replace('"','')+'_'+str(i),reme)
						# print(request.POST)
						oiu=quality_deflection(
								pom=obj,
								deflection=float(defle),
								remark=reme
							)
						c+=1
						oiu.save()
						osf.poms.add(oiu)
						osf.save()
				return redirect('/userdetail/staff_profile/orders/'+str(order_no)+'/forms/quality_evaluation')
			return render(request,"staff/quality_evaluation.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




def quality_evaluation_by_size(request,order_no,size_label):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		quality_cate=staff_Categories.objects.filter(name="Quality").first()
		garment_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		quality=False
		garment=False
		if details and details.staff_category==quality_cate:
			quality=True
		elif details and details.seller_category==garment_cate:
			garment=True
		order=company_Order.objects.filter(order_no=order_no).first()
		if details.staff_category==quality_cate or details.seller_category==garment_cate:
			sizes_avail=quantity_b2b.objects.filter(order=order)
			sizes=[]
			for i in sizes_avail:
				if i.size_label not in sizes:
					sizes.append(i.size_label)
			# print(sizes)
			if quality or request.GET.get('show')=="brand":
				qesd=qe.objects.filter(order=order,label=size_label,by_quality=True)
			else:
				qesd=qe.objects.filter(order=order,label=size_label,by_factory=True)
			li={}
			li1=[]
			for klj in qesd:
				if klj.label in li:
					li[klj.label].append(klj)
				else:
					li1.append(klj.label)
					li[klj.label]=[klj]
			li2=[]
			for klj in li1:
				li2.append(li[klj])

			pom_obj=POM.objects.filter(product_Category=order.product_Category,
				product_Subcategory=order.product_Subcategory,
				product_Supercategory=order.product_Supercategory)
			pom=[]
			for i in pom_obj:
				pom.append(i.label)
			print(li2)
			data={
				"order":order,
				"sizes":sizes,
				"qe":li2,
				"pom":pom
			}
			return render(request,"staff/quality_evaluation_by_size.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')

from POM.models import measurement_chart

def quality_evaluation_clubbed(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		order=company_Order.objects.filter(order_no=order_no).first()
		quality_cate=staff_Categories.objects.filter(name="Quality").first()
		garment_cate=seller_Categories.objects.filter(name="Garmenting Vendor").first()
		quality=False
		garment=False
		if details and details.staff_category==quality_cate:
			quality=True
		elif details and details.seller_category==garment_cate:
			garment=True
		if details and details.staff_category == quality_cate or details.seller_category==garment_cate:
			qes=qe.objects.filter(order=order)
			pom_obj=POM.objects.filter(product_Supercategory=order.product_Supercategory)
			meas=measurement.objects.filter(user=order.fashion_Brand,season=order.season,product_Supercategory=order.product_Supercategory).first()
			sizes_avail=[]
			for i in qes:
				if not(i.label in sizes_avail):
					sizes_avail.append(i.label)
			total_data=[]
			for i in pom_obj:
				tol=measurement_chart.objects.filter(chart=meas,pom=i,main_val=True).first().tolerance
				total_data.append([i,tol])
				for j in sizes_avail:
					qual_average=0
					fact_average=0
					uy=qe.objects.filter(order=order,label=j,by_quality=True)
					count=0
					for k in uy:
						defe=k.poms.all().filter(pom=i).first().deflection
						count+=1
						qual_average+=defe
					if not(count):
						count=1
					qual_average=round(qual_average/count,2)
					count=0
					uy=qe.objects.filter(order=order,label=j,by_factory=True)
					for k in uy:
						defe=k.poms.all().filter(pom=i).first().deflection
						count+=1
						fact_average+=defe
					if not(count):
						count=1
					fact_average=round(fact_average/count,2)
					fact_bool=False
					qual_bool=False
					if qual_average>=tol:
						qual_bool=True
					if fact_average>=tol:
						fact_bool=True
					total_data[-1].append([qual_average,fact_average,qual_bool,fact_bool])
			data={
				"order":order,
				"sizes":sizes_avail,
				"total_data":total_data
			}
			return render(request,"staff/quality_evaluation_clubbed.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



# for i in range(1,31):
# 	print("""					'attribute"""+str(i)+"""':attribute"""+str(i)+""",
# 					"tolerance"""+str(i)+"""":meas_obj.tolerance"""+str(i)+""",""")


# ghjlkk=activities_Category.objects.filter(position='H')
# ghj=activities_Category.objects.filter(position='M')
# for i in ghjlkk:
# 	i.delete()
# for j in ghj:
# 	j.delete()
# 	print("YES")

# for i in range(1,31):
# 	print("""				if meas_obj.attribute"""+str(i)+""":
# 					attribute"""+str(i)+"""=meas_obj.attribute"""+str(i)+"""+(times*meas_obj.grading"""+str(i)+""")""")




# for i in range(1,31):
# 	print("""attribute"""+str(i)+"""=None""")





# for i in range(1,31):
# 	print("""if (data.data.attribute"""+str(i)+"""){
# 					$('#attribute"""+str(i)+"""').html(data.data.attribute"""+str(i)+""");
# 					$('#tolerance"""+str(i)+"""').html(data.data.tolerance"""+str(i)+""");
# 				}""")




from filter.models import filter_Categories,filter_Objects
from product.models import size_color_quantity

def staff_profile_products(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			prod=product.objects.all()
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


from copy import deepcopy
from product.models import product_requests,product_common_attribute_values


def staff_profile_product_detail(request,slug):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff or details.vendor:
			query=product.objects.get(slug=slug)
			x=query.product_Supercategory.all()
			query1=None
			for i in x:
				print("HELLO WORLD ",i.id)
				query1=super_category.objects.get(id=i.id).attributes.all()
			li=[]
			li1=[]
			for i in query1:
				li1.append(i)
				li.append(deepcopy(li1))
				li1.pop()
			query2=[]
			length=len(li)
			# query2.append(query.atrribute1)
			# query2.append(query.atrribute2)
			# query2.append(query.atrribute3)
			# query2.append(query.atrribute4)
			# query2.append(query.atrribute5)
			# query2.append(query.atrribute6)
			# query2.append(query.atrribute7)
			# query2.append(query.atrribute8)
			# query2.append(query.atrribute9)
			# query2.append(query.atrribute10)
			# query2.append(query.atrribute11)
			# query2.append(query.atrribute12)
			# query2.append(query.atrribute13)
			# query2.append(query.atrribute14)
			# query2.append(query.atrribute15)
			# query2.append(query.atrribute16)
			# query2.append(query.atrribute17)
			# query2.append(query.atrribute18)
			# query2.append(query.atrribute19)
			# query2.append(query.atrribute20)
			# query2.append(query.atrribute21)
			# query2.append(query.atrribute22)
			# query2.append(query.atrribute23)
			# query2.append(query.atrribute24)
			# query2.append(query.atrribute25)
			# query2.append(query.atrribute26)
			# query2.append(query.atrribute27)
			# query2.append(query.atrribute28)
			# query2.append(query.atrribute29)
			# query2.append(query.atrribute30)
			# query2.append(query.atrribute31)
			# query2.append(query.atrribute32)
			# query2.append(query.atrribute33)
			# query2.append(query.atrribute34)
			# query2.append(query.atrribute35)
			# query2.append(query.atrribute36)
			# query2.append(query.atrribute37)
			# query2.append(query.atrribute38)
			# query2.append(query.atrribute39)
			# query2.append(query.atrribute40)
			# query2.append(query.atrribute41)
			# query2.append(query.atrribute42)
			# query2.append(query.atrribute43)
			# query2.append(query.atrribute44)
			# query2.append(query.atrribute45)
			# query2.append(query.atrribute46)
			# query2.append(query.atrribute47)
			# query2.append(query.atrribute48)
			# query2.append(query.atrribute49)
			# query2.append(query.atrribute50)
			# query2.append(query.atrribute51)
			# query2.append(query.atrribute52)
			# query2.append(query.atrribute53)
			# query2.append(query.atrribute54)
			# query2.append(query.atrribute55)
			# query2.append(query.atrribute56)
			# query2.append(query.atrribute57)
			# query2.append(query.atrribute58)
			# query2.append(query.atrribute59)
			# query2.append(query.atrribute60)
			# query2.append(query.atrribute61)
			# query2.append(query.atrribute62)
			# query2.append(query.atrribute63)
			# query2.append(query.atrribute64)
			# query2.append(query.atrribute65)
			# query2.append(query.atrribute66)
			# query2.append(query.atrribute67)
			# query2.append(query.atrribute68)
			# query2.append(query.atrribute69)
			# query2.append(query.atrribute70)
			# query2.append(query.atrribute71)
			# query2.append(query.atrribute72)
			# query2.append(query.atrribute73)
			# query2.append(query.atrribute74)
			# query2.append(query.atrribute75)
			# query2.append(query.atrribute76)
			# query2.append(query.atrribute77)
			# query2.append(query.atrribute78)
			# query2.append(query.atrribute79)
			# query2.append(query.atrribute80)
			# query2.append(query.atrribute81)
			# query2.append(query.atrribute82)
			# query2.append(query.atrribute83)
			# query2.append(query.atrribute84)
			# query2.append(query.atrribute85)
			# query2.append(query.atrribute86)
			# query2.append(query.atrribute87)
			# query2.append(query.atrribute88)
			# query2.append(query.atrribute89)
			# query2.append(query.atrribute90)
			# query2.append(query.atrribute91)
			# query2.append(query.atrribute92)
			# query2.append(query.atrribute93)
			# query2.append(query.atrribute94)
			# query2.append(query.atrribute95)
			# query2.append(query.atrribute96)
			# query2.append(query.atrribute97)
			# query2.append(query.atrribute98)
			# query2.append(query.atrribute99)
			# query2.append(query.atrribute100)
			# for i in range(length):
			# 	li[i].append(query2[i])
			# query5=product.objects.all().exclude(slug=slug)[:6]
			# query5=random.choices(list(query5.values()),k=6)
			sizes=[]
			for i in query.size_color_quantity_set.all():
				if not(i.size in sizes):
					sizes.append(i.size)
			# print(li)
			# couni=product.objects.count()
			# query5=product.objects.all().exclude(slug=slug)[:6]
			# query5=random.choices(list(query5.values()),k=6)
			siz=size_color_quantity.objects.filter(linked_product=query)
			from_user=[]
			colors=[]
			sizees=[]
			for i in siz:
				if i.owned_by not in from_user:
					from_user.append(i.owned_by)
				if i.color not in colors:
					colors.append(i.color)
				if i.size not in sizees:
					sizees.append(i.size)
			label_attr = [[l_attr.label_attribute.name, l_attr.value] for l_attr in label_Attributes_Values.objects.filter(prod=query.pk)]
			com_attributes = [[com_attr.attribute, com_attr.value] for com_attr in product_common_attribute_values.objects.filter(prod=query.pk)]
			attributes = com_attributes + [['Brand', query.brand], ["label", query.label], ["fit", query.fit]] + label_attr
			data={
				"obj":query,
				"data":li,
				"from_user":from_user,
				"colors":colors,
				"size":sizees,
				"sizes":sizes,
				"attributes": attributes
			}
			if request.POST.get('sizes_ajax'):
				objs=query.size_color_quantity_set.all().filter(size=request.POST.get('sizes_ajax'))
				cols=[]
				for i in objs:
					if i.quantity and not(i in cols):
						cols.append(i.color)
				# print(cols)
				return JsonResponse({"data":cols})
			if request.POST.get('from_user'):
				from_usr=detail.objects.filter(email=request.POST.get('from_user')).first()
				price_at=request.POST.get('price_at')
				if price_at:
					price_at=int(price_at)
				quantity=request.POST.get('quantity')
				if quantity:
					quantity=int(quantity)
				address=request.POST.get('delivery')
				size=request.POST.get('size')
				if size:
					size=int(size)
				c=request.POST.get('color')
				color=c
				obj=product_requests(
				to_product=query,
				price=price_at,
				quantity=quantity,
				delivery=address,
				to_user=from_usr,
				size=size,
				color=color,
				from_user=details
				)
				obj.save()
				noti_j=notifications(
					title="New Staff Requested a Product",
					description="New Staff Requested a Product",
					link="/userdetail/staff_profile/requested_product/"+slug+"/"+str(obj.id),
					user=from_usr
					)
				noti_j.save()
				noti_j.link=noti_j.link+"?noti="+str(noti_j.id)
				noti_j.save()
				return redirect('/userdetail/staff_profile')
			return render(request,"staff/staff_profile_product_detail.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def staff_profile_requested_product(request,slug,id):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff or details.vendor:
			query=product.objects.get(slug=slug)
			query1=query.product_Supercategory.attributes.all()
			li=[]
			li1=[]
			for i in query1:
				li1.append(i)
				li.append(deepcopy(li1))
				li1.pop()
			query2=[]
			length=len(li)
			query2.append(query.atrribute1)
			query2.append(query.atrribute2)
			query2.append(query.atrribute3)
			query2.append(query.atrribute4)
			query2.append(query.atrribute5)
			query2.append(query.atrribute6)
			query2.append(query.atrribute7)
			query2.append(query.atrribute8)
			query2.append(query.atrribute9)
			query2.append(query.atrribute10)
			query2.append(query.atrribute11)
			query2.append(query.atrribute12)
			query2.append(query.atrribute13)
			query2.append(query.atrribute14)
			query2.append(query.atrribute15)
			query2.append(query.atrribute16)
			query2.append(query.atrribute17)
			query2.append(query.atrribute18)
			query2.append(query.atrribute19)
			query2.append(query.atrribute20)
			query2.append(query.atrribute21)
			query2.append(query.atrribute22)
			query2.append(query.atrribute23)
			query2.append(query.atrribute24)
			query2.append(query.atrribute25)
			query2.append(query.atrribute26)
			query2.append(query.atrribute27)
			query2.append(query.atrribute28)
			query2.append(query.atrribute29)
			query2.append(query.atrribute30)
			query2.append(query.atrribute31)
			query2.append(query.atrribute32)
			query2.append(query.atrribute33)
			query2.append(query.atrribute34)
			query2.append(query.atrribute35)
			query2.append(query.atrribute36)
			query2.append(query.atrribute37)
			query2.append(query.atrribute38)
			query2.append(query.atrribute39)
			query2.append(query.atrribute40)
			query2.append(query.atrribute41)
			query2.append(query.atrribute42)
			query2.append(query.atrribute43)
			query2.append(query.atrribute44)
			query2.append(query.atrribute45)
			query2.append(query.atrribute46)
			query2.append(query.atrribute47)
			query2.append(query.atrribute48)
			query2.append(query.atrribute49)
			query2.append(query.atrribute50)
			query2.append(query.atrribute51)
			query2.append(query.atrribute52)
			query2.append(query.atrribute53)
			query2.append(query.atrribute54)
			query2.append(query.atrribute55)
			query2.append(query.atrribute56)
			query2.append(query.atrribute57)
			query2.append(query.atrribute58)
			query2.append(query.atrribute59)
			query2.append(query.atrribute60)
			query2.append(query.atrribute61)
			query2.append(query.atrribute62)
			query2.append(query.atrribute63)
			query2.append(query.atrribute64)
			query2.append(query.atrribute65)
			query2.append(query.atrribute66)
			query2.append(query.atrribute67)
			query2.append(query.atrribute68)
			query2.append(query.atrribute69)
			query2.append(query.atrribute70)
			query2.append(query.atrribute71)
			query2.append(query.atrribute72)
			query2.append(query.atrribute73)
			query2.append(query.atrribute74)
			query2.append(query.atrribute75)
			query2.append(query.atrribute76)
			query2.append(query.atrribute77)
			query2.append(query.atrribute78)
			query2.append(query.atrribute79)
			query2.append(query.atrribute80)
			query2.append(query.atrribute81)
			query2.append(query.atrribute82)
			query2.append(query.atrribute83)
			query2.append(query.atrribute84)
			query2.append(query.atrribute85)
			query2.append(query.atrribute86)
			query2.append(query.atrribute87)
			query2.append(query.atrribute88)
			query2.append(query.atrribute89)
			query2.append(query.atrribute90)
			query2.append(query.atrribute91)
			query2.append(query.atrribute92)
			query2.append(query.atrribute93)
			query2.append(query.atrribute94)
			query2.append(query.atrribute95)
			query2.append(query.atrribute96)
			query2.append(query.atrribute97)
			query2.append(query.atrribute98)
			query2.append(query.atrribute99)
			query2.append(query.atrribute100)
			for i in range(length):
				li[i].append(query2[i])
			# print(li)
			# couni=product.objects.count()
			# query5=product.objects.all().exclude(slug=slug)[:6]
			# query5=random.choices(list(query5.values()),k=6)
			siz=size_color_quantity.objects.filter(linked_product=query)
			from_user=[]
			colors=[]
			sizees=[]
			for i in siz:
				if i.owned_by not in from_user:
					from_user.append(i.owned_by)
				if i.color not in colors:
					colors.append(i.color)
				if i.size not in sizees:
					sizees.append(i.size)
			prod_req=product_requests.objects.filter(id=id).first()

			data={
				"obj":query,
				"data":li,
				"from_user":from_user,
				"colors":colors,
				"size":sizees,
				"prod_req":prod_req
			}
			# print(request.POST.get('approve'))
			if request.POST.get('approve'):
				price_at=request.POST.get('price_at')
				if price_at:
					price_at=int(price_at)
				quantity=request.POST.get('quantity')
				if quantity:
					quantity=int(quantity)
				address=request.POST.get('delivery')
				size=request.POST.get('size')
				if size:
					size=int(size)
				c=request.POST.get('color')
				color=c
				prod_req.price=price_at
				prod_req.quantity=quantity
				prod_req.delivery=address
				prod_req.size=size
				prod_req.color=color
				objjk=size_color_quantity.objects.filter(size=size,color=color,quantity__gte=quantity,
				owned_by=details,linked_product=query).first()
				print(objjk)
				if objjk:
					prod_req.approved=True
					prod_req.save()
					if objjk.quantity-quantity == 0:
						objjk.delete()
					else:
						objjk.quantity-=quantity
						objjk.save()
					noti_j=notifications(
						title="Your Requested Product Approved",
						description="Your Requested Product Approved",
						link="/userdetail/staff_profile/products/"+slug,
						user=prod_req.from_user
						)
					noti_j.save()
					noti_j.link=noti_j.link+"?noti="+str(noti_j.id)
					noti_j.save()
					return redirect('/userdetail/staff_profile')
			return render(request,"staff/staff_profile_requested_product.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




from product.models import category as cat

def staff_profile_placeorder(request):
	sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
	brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
	cate=cat.objects.all()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.buisness_Customer or details.vendor or details.staff:
			if request.POST and request.FILES:
				brand=request.POST.get('brand')
				brand=detail.objects.get(id=brand)
				label=request.POST.get('label')
				label=labels.objects.get(slug=label)
				fit=request.POST.get('fit')
				fit=fits.objects.get(slug=fit)
				season=request.POST.get('season')
				season=seasons.objects.get(slug=season)
				category=request.POST.get('category')
				category=cat.objects.get(name=category)
				sub_cate=request.POST.get('sub_category')
				sub_cate=sub_category.objects.get(name=sub_cate,product_Category=category)
				super_cate=request.POST.get('super_category')
				super_cate=super_category.objects.get(name=super_cate,product_Subcategory=sub_cate)
				quantity=request.POST.get('quantity')
				dispatch=request.POST.get('dispatch')
				billing=request.POST.get('billing')
				sample=request.FILES.get('sample')
				excel=request.FILES.get('excel')
				allorder=company_Order.objects.all().order_by('-order_no')
				if allorder.count()>0:
					order_n=allorder.first().order_no+1
				else:
					x=str(datetime.datetime.now().year)
					order_n=int(x+"000001")
				ofd=address_model(
					address=dispatch,
					title="Location1"
					)
				ofd.save()
				target_lead_time=request.POST.get('target_lead_time')

				target_price=request.POST.get('target_price')
				if not(target_lead_time):
					target_lead_time=0
				if not(target_price):
					target_price=0
				tech_pack=request.FILES.get('tech_pack')
				description=request.POST.get('description')
				specs=request.FILES.get('specs')
				colors=request.POST.get('colors')
				sizes=request.POST.get('sizes')
				logo_place=request.POST.get('logo_place')
				if not(target_lead_time):
					target_lead_time=0
				if not(target_price):
					target_price=0
				order=company_Order(
						fashion_Brand=brand,
						label=label,
						fit=fit,
						season=season,
						product_Category=category,
						product_Subcategory=sub_cate,
						product_Supercategory=super_cate,
						quantity=quantity,
						image=sample,
						excel=excel,
						billing_Address=billing,
						order_no=order_n,
						user_email=request.user.email,
						order_type='O',
						target_lead_time=int(target_lead_time),
						target_price=int(target_price),
						tech_pack=tech_pack,
						specs=specs,
						logo_placement=logo_place,
						description=description,
						sizes=sizes
					)
				order.save()
				if request.GET.get('order'):
					from_ord=int(request.GET.get('order'))
					orty=company_Order.objects.filter(order_no=from_ord).first()
					if orty.order_type=='E':
						order.from_enquiry=True
					elif orty.order_type=='D':
						order.from_design=True
					elif orty.order_type=='S':
						order.from_sample=True
					order.from_order_no=from_ord
				order.dispatch_Address.add(ofd)
				order.save()
				staff_cate=staff_Categories.objects.filter(name="Sales").first()
				objs1=detail.objects.filter(
					staff=True,
					staff_category=staff_cate,
					position='H')
				order.save()
				if colors:
					colors=list(colors.split(','))
				else:
					colors=[]
				for tyu in colors:
					owqe=color_model.objects.filter(name=tyu)
					if owqe.count()==0:
						owqe=color_model(
							name=tyu
							)
						owqe.save()
					else:
						owqe=owqe.first()
					order.colors_avail.add(owqe)
				for i in objs1:
					order.staffs_Allocated.add(i)
					noti_oj=notifications(
						title="New Order Placed Please Add Manager to it("+str(order_n)+") !",
						description="Add manager to it",
						user=i,
						link="/userdetail/staff_profile/orders/"+str(order_n),
						type_of_order='O')
					noti_oj.save()
					noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
					noti_oj.save()
					acti_cate=activities_Category.objects.filter(
						position='H',type_of_order='O',staff_category=staff_cate)

					for j in acti_cate:
						lead_time=0
						if order.target_lead_time>=120:
							lead_time=j.lead_Time_for_120_Days
						elif order.target_lead_time<120 and order.target_lead_time>=105:
							lead_time=j.lead_Time_for_105_Days
						elif order.target_lead_time<105 and order.target_lead_time>=90:
							lead_time=j.lead_Time_for_90_Days
						elif order.target_lead_time<90 and order.target_lead_time>=75:
							lead_time=j.lead_Time_for_75_Days
						elif order.target_lead_time<75 and order.target_lead_time>=60:
							lead_time=j.lead_Time_for_60_Days
						elif order.target_lead_time<60 and order.target_lead_time>=45:
							lead_time=j.lead_Time_for_45_Days
						elif order.target_lead_time<45 and order.target_lead_time>=30:
							lead_time=j.lead_Time_for_30_Days
						elif order.target_lead_time<30 and order.target_lead_time>=15:
							lead_time=j.lead_Time_for_15_Days
						elif order.target_lead_time<15 and order.target_lead_time>=7:
							lead_time=j.lead_Time_for_7_Days
						elif order.target_lead_time<7 and order.target_lead_time>=3:
							lead_time=j.lead_Time_for_3_Days
						j.completed_in=lead_time
						j.save()
						acti=activities(
							user=i,
							slug=str(i)+"_"+str(j)+"_"+str(order_n)+"_"+str(staff_cate),
							activity_Cate=j,
							order=order,
							planned_date=datetime.datetime.now()+datetime.timedelta(days=lead_time),
							prev_lap=lead_time)

						acti.save()
						if j.linked_activity:
							acti_obj_exi=activities.objects.filter(activity_Cate=j.linked_activity,
							order=order).first()
							if acti_obj_exi:
								previous_date_to=acti_obj_exi.planned_date
							else:
								previous_date_to=datetime.datetime.now()
						else:
							previous_date_to=datetime.datetime.now()
						acti.planned_date=getPlannedDate(i,previous_date_to,lead_time)
						# acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
						acti.save()


				order.save()
				if order.excel:
					data_read=csv.reader(open(BASE_DIR+order.excel.url[6:],"r"), delimiter=',', quotechar='"')
					count=0
					for row in data_read:
						name=row[1]
						email=row[2]
						password=row[3]
						max_quantity=int(row[4])
						count=count+1
						try:
							obj=User.objects.create_user(username=email,email=email,password=password)
							obj.save()
						except:
							continue
						obj=detail(
								name=name,
								email=email,
								password=password,
								b2b_order=True,
								b2b_order_no=order_n,
								customer=True,
								vendor=False,
								buisness_Customer=False,
								activate_Seller=False,
								activate_Buisness=False,
								buisness_Timeline=False,
								vendor_Timeline=False,
								max_quantity=max_quantity
							)
						obj.save()
				return redirect('/userdetail/staff_profile')
			if request.POST.get('placeorder_ajax_brand'):
				obj=detail.objects.get(id=request.POST.get('placeorder_ajax_brand'))
				obj1=labels.objects.filter(vendor=obj)
				print(obj1)
				if obj1.count()>0:
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('placeorder_ajax_label'):
				obj=labels.objects.get(slug=request.POST.get('placeorder_ajax_label'))
				obj1=fits.objects.filter(label=obj)
				if obj1.count()>0:
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('placeorder_ajax_fit'):
				obj=fits.objects.get(slug=request.POST.get('placeorder_ajax_fit'))
				obj1=seasons.objects.filter(fit=obj)
				print(obj1)
				if obj1.count()>0:
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('placeorder_ajax_category'):
				obj=cat.objects.get(name=request.POST.get('placeorder_ajax_category'))
				obj1=sub_category.objects.filter(product_Category=obj)
				print(obj1)
				if obj1.count()>0:
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('placeorder_ajax_sub_category'):
				ooj=cat.objects.get(name=request.POST.get('placeorder_ajax_sub_category_category'))
				obj=sub_category.objects.get(name=request.POST.get('placeorder_ajax_sub_category'),product_Category=ooj)
				obj1=super_category.objects.filter(product_Subcategory=obj)
				print(obj1)
				if obj1.count()>0:
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			data={"brand":brands,"cate":cate,"depend":None}
			if request.GET.get('order'):
				try:
					su=int(request.GET.get('order'))
				except:
					su=0
				data["depend"]=company_Order.objects.filter(order_no=su).first()
			return render(request,'b2b/placeorder.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')





from product.models import product_cate_b2b




def staff_profile_upload_product(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			cate=category.objects.all()
			prod_cate=product_cate_b2b.objects.all()
			sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
			brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
			data={
			"cate":cate,
			"prod_cate":prod_cate,
			"brands":brands
			}
			if request.POST.get('id_ajax_cate'):
				id1=request.POST.get('id_ajax_cate')
				obj1=category.objects.filter(id=id1).first()
				obj1=sub_category.objects.filter(product_Category=obj1)
				if obj1.count():
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('id_ajax_subcate'):
				id1=request.POST.get('id_ajax_subcate')
				obj1=sub_category.objects.filter(id=id1).first()
				obj1=super_category.objects.filter(product_Subcategory=obj1)
				if obj1.count():
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('id_ajax_supcate'):
				id1=request.POST.get('id_ajax_supcate')
				obj1=super_category.objects.filter(id=id1).first()
				obj1=obj1.attributes.all()
				print(obj1)
				if obj1.count():
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
			if request.POST.get('slug_ajax_prod'):
				slug=request.POST.get('slug_ajax_prod')
				obj1=product.objects.filter(slug=slug)

				if obj1.count()>0:
					bol=False
				else:
					bol=True
				return HttpResponse(json.dumps({'bol':bol}), content_type="application/json")
			if request.POST.get('title'):
				cate=category.objects.filter(id=int(request.POST.get('cate'))).first()
				subcate=sub_category.objects.filter(id=int(request.POST.get('sub_cate'))).first()
				supcate=super_category.objects.filter(id=int(request.POST.get('sup_cate'))).first()
				b2b_cate=product_cate_b2b.objects.filter(id=int(request.POST.get('b2b_cate'))).first()
				obj=product(
						product_Category=cate,
						product_Subcategory=subcate,
						product_Supercategory=supcate,
						title=request.POST.get('title'),
						slug=request.POST.get('slug'),
						notes=request.POST.get('notes'),
						seller=details,
						description=request.POST.get('description'),
						image1=request.FILES.get('image1'),
						image2=request.FILES.get('image2'),
						image3=request.FILES.get('image3'),
						image4=request.FILES.get('image4'),
						image5=request.FILES.get('image5'),
						atrribute1=request.POST.get('attribute1'),
						atrribute2=request.POST.get('attribute2'),
						atrribute3=request.POST.get('attribute3'),
						atrribute4=request.POST.get('attribute4'),
						atrribute5=request.POST.get('attribute5'),
						atrribute6=request.POST.get('attribute6'),
						atrribute7=request.POST.get('attribute7'),
						atrribute8=request.POST.get('attribute8'),
						atrribute9=request.POST.get('attribute9'),
						atrribute10=request.POST.get('attribute10'),
						atrribute11=request.POST.get('attribute11'),
						atrribute12=request.POST.get('attribute12'),
						atrribute13=request.POST.get('attribute13'),
						atrribute14=request.POST.get('attribute14'),
						atrribute15=request.POST.get('attribute15'),
						atrribute16=request.POST.get('attribute16'),
						atrribute17=request.POST.get('attribute17'),
						atrribute18=request.POST.get('attribute18'),
						atrribute19=request.POST.get('attribute19'),
						atrribute20=request.POST.get('attribute20'),
						atrribute21=request.POST.get('attribute21'),
						atrribute22=request.POST.get('attribute22'),
						atrribute23=request.POST.get('attribute23'),
						atrribute24=request.POST.get('attribute24'),
						atrribute25=request.POST.get('attribute25'),
						atrribute26=request.POST.get('attribute26'),
						atrribute27=request.POST.get('attribute27'),
						atrribute28=request.POST.get('attribute28'),
						atrribute29=request.POST.get('attribute29'),
						atrribute30=request.POST.get('attribute30'),
						atrribute31=request.POST.get('attribute31'),
						atrribute32=request.POST.get('attribute32'),
						atrribute33=request.POST.get('attribute33'),
						atrribute34=request.POST.get('attribute34'),
						atrribute35=request.POST.get('attribute35'),
						atrribute36=request.POST.get('attribute36'),
						atrribute37=request.POST.get('attribute37'),
						atrribute38=request.POST.get('attribute38'),
						atrribute39=request.POST.get('attribute39'),
						atrribute40=request.POST.get('attribute40'),
						atrribute41=request.POST.get('attribute41'),
						atrribute42=request.POST.get('attribute42'),
						atrribute43=request.POST.get('attribute43'),
						atrribute44=request.POST.get('attribute44'),
						atrribute45=request.POST.get('attribute45'),
						atrribute46=request.POST.get('attribute46'),
						atrribute47=request.POST.get('attribute47'),
						atrribute48=request.POST.get('attribute48'),
						atrribute49=request.POST.get('attribute49'),
						atrribute50=request.POST.get('attribute50'),
						atrribute51=request.POST.get('attribute51'),
						atrribute52=request.POST.get('attribute52'),
						atrribute53=request.POST.get('attribute53'),
						atrribute54=request.POST.get('attribute54'),
						atrribute55=request.POST.get('attribute55'),
						atrribute56=request.POST.get('attribute56'),
						atrribute57=request.POST.get('attribute57'),
						atrribute58=request.POST.get('attribute58'),
						atrribute59=request.POST.get('attribute59'),
						atrribute60=request.POST.get('attribute60'),
						atrribute61=request.POST.get('attribute61'),
						atrribute62=request.POST.get('attribute62'),
						atrribute63=request.POST.get('attribute63'),
						atrribute64=request.POST.get('attribute64'),
						atrribute65=request.POST.get('attribute65'),
						atrribute66=request.POST.get('attribute66'),
						atrribute67=request.POST.get('attribute67'),
						atrribute68=request.POST.get('attribute68'),
						atrribute69=request.POST.get('attribute69'),
						atrribute70=request.POST.get('attribute70'),
						atrribute71=request.POST.get('attribute71'),
						atrribute72=request.POST.get('attribute72'),
						atrribute73=request.POST.get('attribute73'),
						atrribute74=request.POST.get('attribute74'),
						atrribute75=request.POST.get('attribute75'),
						atrribute76=request.POST.get('attribute76'),
						atrribute77=request.POST.get('attribute77'),
						atrribute78=request.POST.get('attribute78'),
						atrribute79=request.POST.get('attribute79'),
						atrribute80=request.POST.get('attribute80'),
						atrribute81=request.POST.get('attribute81'),
						atrribute82=request.POST.get('attribute82'),
						atrribute83=request.POST.get('attribute83'),
						atrribute84=request.POST.get('attribute84'),
						atrribute85=request.POST.get('attribute85'),
						atrribute86=request.POST.get('attribute86'),
						atrribute87=request.POST.get('attribute87'),
						atrribute88=request.POST.get('attribute88'),
						atrribute89=request.POST.get('attribute89'),
						atrribute90=request.POST.get('attribute90'),
						atrribute91=request.POST.get('attribute91'),
						atrribute92=request.POST.get('attribute92'),
						atrribute93=request.POST.get('attribute93'),
						atrribute94=request.POST.get('attribute94'),
						atrribute95=request.POST.get('attribute95'),
						atrribute96=request.POST.get('attribute96'),
						atrribute97=request.POST.get('attribute97'),
						atrribute98=request.POST.get('attribute98'),
						atrribute99=request.POST.get('attribute99'),
						atrribute100=request.POST.get('attribute100')
					)
				obj.price=int(request.POST.get('price1'))
				obj.save()
				obj.product_cate.add(b2b_cate)
				# B2BCHECKBOX
				# if request.POST.get('b2b_product'):
				# 	obj.b2b_product=True
				# if request.POST.get('b2c_product'):
				# 	obj.b2c_product=True
				# if request.POST.get('sample_product'):
				# 	obj.sample_product=True
				obj.save()
				obj1=size_color_quantity(linked_product=obj,
				size=request.POST.get('size1'),
				color=request.POST.get('color1'),
				quantity=request.POST.get('quantity1'),
				price=request.POST.get('price1'),
				owned_by=details)
				obj1.save()
				if request.POST.get('size2'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size2')),
					color=request.POST.get('color2'),
					quantity=int(request.POST.get('quantity2')),
					price=int(request.POST.get('price2')))
					obj1.save()
				if request.POST.get('size3'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size3')),
					color=request.POST.get('color3'),
					quantity=int(request.POST.get('quantity3')),
					price=int(request.POST.get('price3')))
					obj1.save()
				if request.POST.get('size4'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size4')),
					color=request.POST.get('color4'),
					quantity=int(request.POST.get('quantity4')),
					price=int(request.POST.get('price4')))
					obj1.save()
				if request.POST.get('size5'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size5')),
					color=request.POST.get('color5'),
					quantity=int(request.POST.get('quantity5')),
					price=int(request.POST.get('price5')))
					obj1.save()
				if request.POST.get('size6'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size6')),
					color=request.POST.get('color6'),
					quantity=int(request.POST.get('quantity6')),
					price=int(request.POST.get('price6')))
					obj1.save()
				if request.POST.get('size7'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size7')),
					color=request.POST.get('color7'),
					quantity=int(request.POST.get('quantity7')),
					price=int(request.POST.get('price7')))
					obj1.save()
				if request.POST.get('size8'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size8')),
					color=request.POST.get('color8'),
					quantity=int(request.POST.get('quantity8')),
					price=int(request.POST.get('price8')))
					obj1.save()
				if request.POST.get('size9'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size9')),
					color=request.POST.get('color9'),
					quantity=int(request.POST.get('quantity9')),
					price=int(request.POST.get('price9')))
					obj1.save()
				if request.POST.get('size10'):
					obj1=size_color_quantity(linked_product=obj,
					size=int(request.POST.get('size10')),
					color=request.POST.get('color10'),
					quantity=int(request.POST.get('quantity10')),
					price=int(request.POST.get('price10')))
					obj1.save()
				return redirect('/userdetail/staff_profile')

			return render(request,'products/upload_product.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


from .models import list_of_holidays
import calendar



def staff_profile_holidays(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details:
			if details.staff or details.vendor:
				months={1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",
				10:"October",11:"November",12:"December"}
				cur_year=datetime.datetime.now().year
				cur_month=datetime.datetime.now().month
				cur_date=datetime.datetime.now().month
				days=calendar.monthcalendar(cur_year,cur_month)
				week_days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
				colors=['#db7f7a', '#db847a','#db8d7a','#db8d7a','#db917a','#db967a', '#db9a7a', '#db9a7a','#db9f7a','#dba37a', '#dba87a','#dbac7a', '#dbb07a', '#dbb57a', '#dbbe7a', '#dbc27a', '#dbc77a', '#dbd07a', '#dbd47a', '#dbd97a', '#d9db7a', '#d0db7a', '#cbdb7a', '#c7db7a', '#c2db7a', '#bedb7a', '#b9db7a', '#b5db7a','#acdb7a', '#a7db7a', '#a3db7a','#9adb7a','#96db7a', '#91db7a', '#8ddb7a', '#88db7a', '#7fdb7a',	'#7bdb7a', '#7adb7e', '#7adb82', '#7adb87', '#7adb90', '#7adb9d', '#7adba6', '#7adbaf', '#7adbb3', '#7adbb8', '#7adbc1', '#7adbce', '#7adbd3','#7adbd7', '#7adadb', '#7ad6db', '#7ad1db', '#7acddb', '#7ac8db', '#7ac4db','#7abfdb', '#7ab6db']
				holidays=[]
				for i in days:
					for j in i:
						if j:
							c_date=j
							date_obj=datetime.date(cur_year,cur_month,c_date)
							obj=list_of_holidays.objects.filter(users=details,date_of_holiday=date_obj).first()
							if obj:
								holidays.append(j)
				# print(holidays)
				data={
					"user":details,
					"cur_month":[cur_month,months[cur_month]],
					"cur_year":cur_year,
					"days":days,
					"cur_date":str(cur_year)+"-"+str(cur_month)+"-"+str(cur_date),
					"week_days":week_days,
					"colors":colors,
					"holidays":holidays
				}
				if request.POST.get('holiday_ajax'):
					holiday=request.POST.get('holiday_ajax')
					year,month,day=map(int,holiday.strip().split("-"))
					date_obj=datetime.date(year,month,day)
					obj=list_of_holidays.objects.filter(date_of_holiday=date_obj).first()
					if not(obj):
						obj=list_of_holidays(date_of_holiday=date_obj)
						obj.save()
					obj.users.add(details)
					obj.save()
					return JsonResponse({"data":True})
				if request.POST.get('holiday_staff_ajax'):
					holiday=request.POST.get('holiday_staff_ajax')
					year,month,day=map(int,holiday.strip().split("-"))
					date_obj=datetime.date(year,month,day)
					obj=list_of_holidays.objects.filter(date_of_holiday=date_obj).first()
					if not(obj):
						obj=list_of_holidays(date_of_holiday=date_obj)
						obj.save()
					user_to=[]
					if details.staff:
						user_to=detail.objects.filter(staff_category=details.staff_category)
					elif details.vendor:
						user_to=detail.objects.filter(seller_category=details.seller_category)
					for j in user_to:
						obj.users.add(j)
					obj.save()
					return JsonResponse({"data":True})
				if request.POST.get('original_dates'):
					dates=request.POST.get('original_dates')
					dates=map(str,dates.strip().split(','))
					for i in dates:
						try:
							year,month,day=map(int,i.strip().split('-'))
						except:
							continue
						date_obj=datetime.date(year,month,day)
						obj=list_of_holidays(date_of_holiday=date_obj)
						obj.save()
						user_to=detail.objects.filter(staff=True)
						for j in user_to:
							obj.users.add(j)
						user_to=detail.objects.filter(vendor=True)
						for j in user_to:
							obj.users.add(j)
						obj.save()
					return redirect('/userdetail/staff_profile')
				return render(request,"staff/staff_profile_holidays.html",data)
			else:
				return redirect('/userdetail/logout')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


from product.models import washcare_model


def washcare_detail_view(request,washcare_id):
	washcare=washcare_model.objects.filter(id=washcare_id).first()
	if washcare:
		link="http://raymondinstitutional.justgetit.in/userdetail/seller_profile/washcare/"+str(washcare.id)
		data={
			"washcare":washcare,
			"link":link
		}
		return render(request,"seller_info/washcare_detail_view.html",data)
	else:
		return redirect('/')





def staff_address_details(request,order_no):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		order=company_Order.objects.filter(order_no=order_no).first()
		if details and order and details in order.staffs_Allocated.all():
			data={

			}
			if request.POST.get('location'):
				lat=float(request.POST.get('lat_input'))
				lng=float(request.POST.get('lng_input'))
				loc=request.POST.get('location')
				if loc=="pickup":
					order.pickup_lat=lat
					order.pickup_lng=lng
				else:
					order.delivery_lat=lat
					order.delivery_lng=lng
				order.save()
				return redirect('/userdetail/staff_profile')
			return render(request,"userdetail/staff_address_details.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/logout')




from .models import access_perm

def login_other_profile(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details:
			acc=access_perm.objects.filter(user=details).first()
			users=[]
			for i in acc.staff_category.all():
				users.append(detail.objects.filter(staff_category=i))
			for i in acc.seller_category.all():
				users.append(detail.objects.filter(seller_category=i))
			data={
				"details":details,
				"users":users
			}
			# print(users)
			if request.GET.get('user_login'):
				user_to=detail.objects.filter(email=request.GET.get('user_login')).first()
				if user_to and (user_to.staff_category in acc.staff_category.all() or user_to.seller_category in acc.seller_category.all()):
					user=authenticate(username=user_to.email,password=user_to.password)
					if user is not None:
						login(request,user)
						user=detail.objects.filter(email=request.user.email)
						if user.count()>0:
							user=user.first()
							if request.GET.get('next'):
								nurl=request.GET.get('next')
								if request.GET.get('carton'):
									nurl=nurl+"?carton="+request.GET.get("carton")
								if request.GET.get("size"):
									nurl=nurl+"&size="+request.GET.get("size")
								return redirect('/'+nurl)
							if user.buisness_Customer:
								if user.info_update:
									return redirect('/buisness/buisness_profile')
								else:
									return redirect('/buisness/buisness_timeline')
								return redirect('/buisness')
							elif user.vendor:
								if user.info_update:
									obj=seller_Categories.objects.filter(name="Products Vendor").first()
									if user.seller_category==obj:
										return redirect('/userdetail/seller_profile')
									else:
										return redirect('/userdetail/vendor_profile')
								else:
									return redirect('/userdetail/seller_profile_update')
							elif user.b2b_order:
								return redirect('/buisness/consumer_profile')
							elif user.staff:
								if user.info_update:
									return redirect('/userdetail/staff_profile')
								else:
									return redirect('/userdetail/staff_profile_update')
						return redirect('/')

			return render(request,"userdetail/login_other_profile.html",data)

		else:
			return redirect('/userdetail/login')
	else:
		return redirect('/userdetail/login')


from b2b.models import budget_sectors,sector_run_rate
def fun_accept_rate(request,m,w,obj):
	obj=sector_run_rate.objects.filter(id=obj).first()
	if m:
		print(m=="3","afghilk,",w)
		if m=="1":
			obj.w_month1=w
		elif m=="2":
			obj.w_month2=w
		elif m=="3":
			obj.w_month3=w
		elif m=="4":
			obj.w_month4=w
		elif m=="5":
			obj.w_month5=w
		elif m=="6":
			obj.w_month6=w
		elif m=="7":
			obj.w_month7=w
		elif m=="8":
			obj.w_month8=w
		elif m=="9":
			obj.w_month9=w
		elif m=="10":
			obj.w_month10=w
		elif m=="11":
			obj.w_month11=w
		elif m=="12":
			obj.w_month12=w
		obj.save()
		print(obj.w_month3,obj.w_month1)





def staff_profile_run_rate(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details and details.staff:
			brand=detail.objects.filter(email='raymond@raymond.in').first()
			normal=[]
			variance=[]
			next_year=[]
			budg_mod=budget_model.objects.filter(user=brand).first()
			year_amount=budg_mod.yearly_amount
			year_amount1=budg_mod.yearly_amount1
			cur_year=budg_mod.year
			act_amount=0
			for i in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year):
				act_amount+=i.get_billing_amount
			for i in budget_sectors.objects.filter(user=brand):
				dicti={
					"sector_name":i.name,
					"planned_a":round(year_amount*(i.weight_percent/100),2),
					"planned_b":round(year_amount1*(i.weight_percent/100),2),
					"actual":round(act_amount*(i.weight_percent/100),2),
					"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
				}
				dicti1={
					"planned_vis":dicti["actual"]-dicti["total"],
					"hit":round((dicti["actual"]*100)/dicti["total"],2)
				}
				dicti2={
					"normal_year":dicti["total"],
					"required":dicti["total"]-dicti["actual"]+dicti["total"]
				}
				normal.append(dicti)
				variance.append(dicti1)
				next_year.append(dicti2)
			data={
				"years":budget_model.objects.filter(user=brand),
				"normal":normal,
				"variance":variance,
				"next_year":next_year
			}
			if request.POST.get('year_mode_ajax') and not(request.POST.get('get_sub_year')):
				if request.POST.get('year_mode_ajax')=="year":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount
					year_amount1=budg_mod.yearly_amount1
					cur_year=budg_mod.year
					act_amount=0
					for i in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year):
						act_amount+=i.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					year_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year
					}
					return render(request,"ajax_response/userdetail/yearly_response.html",year_data)
				elif request.POST.get('year_mode_ajax')=="half":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount//2
					year_amount1=budg_mod.yearly_amount1//2
					cur_year=budg_mod.year
					act_amount=0
					for i in range(1,7):
						for j in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year,order_date_time__month=i):
							act_amount+=j.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					half_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year,
						"n":1
					}
					return render(request,"ajax_response/userdetail/half_yearly_response.html",half_data)
				elif request.POST.get('year_mode_ajax')=="quart":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount//4
					year_amount1=budg_mod.yearly_amount1//4
					cur_year=budg_mod.year
					act_amount=0
					for i in range(1,4):
						for j in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year,order_date_time__month=i):
							act_amount+=j.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					quart_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year,
						"n":1
					}
					return render(request,"ajax_response/userdetail/quart_response.html",quart_data)
				elif request.POST.get('year_mode_ajax')=="month":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount//12
					year_amount1=budg_mod.yearly_amount1//12
					cur_year=budg_mod.year
					act_amount=0
					for j in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year,order_date_time__month=1):
						act_amount+=j.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					month_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year,
						"n":1
					}
					return render(request,"ajax_response/userdetail/monthly_response.html",month_data)
			if request.POST.get('get_sub_year'):
				if request.POST.get('year_mode_ajax')=="year":
					return JsonResponse({"sub":[]})
				elif request.POST.get('year_mode_ajax')=="half":
					return JsonResponse({"sub":["H1","H2"]})
				elif request.POST.get('year_mode_ajax')=="quart":
					return JsonResponse({"sub":["Q1","Q2","Q3","Q4"]})
				elif request.POST.get('year_mode_ajax')=="month":
					return JsonResponse({"sub":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]})
			if request.POST.get('years_ajax'):
				normal=[]
				variance=[]
				next_year=[]
				yea=budget_years.objects.filter(year=request.POST.get('years_ajax')).first()
				budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
				year_amount=budg_mod.yearly_amount
				year_amount1=budg_mod.yearly_amount1
				cur_year=budg_mod.year
				act_amount=0
				for i in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year):
					act_amount+=i.get_billing_amount
				for i in budget_sectors.objects.filter(user=brand):
					dicti={
						"sector_name":i.name,
						"planned_a":round(year_amount*(i.weight_percent/100),2),
						"planned_b":round(year_amount1*(i.weight_percent/100),2),
						"actual":round(act_amount*(i.weight_percent/100),2),
						"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
					}
					dicti1={
						"planned_vis":dicti["actual"]-dicti["total"],
						"hit":round((dicti["actual"]*100)/dicti["total"],2)
					}
					dicti2={
						"normal_year":dicti["total"],
						"required":dicti["total"]-dicti["actual"]+dicti["total"]
					}
					normal.append(dicti)
					variance.append(dicti1)
					next_year.append(dicti2)
				year_data={
					"years":budget_model.objects.filter(user=brand),
					"normal":normal,
					"variance":variance,
					"next_year":next_year
				}
				return render(request,"ajax_response/userdetail/yearly_response.html",year_data)
			if request.POST.get('sub_years_ajax'):
				if request.POST.get('sub_years_mode_ajax')=="year":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('sub_years_year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount
					year_amount1=budg_mod.yearly_amount1
					cur_year=budg_mod.year
					act_amount=0
					for i in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year):
						act_amount+=i.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					year_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year
					}
					return render(request,"ajax_response/userdetail/yearly_response.html",year_data)
				elif request.POST.get('sub_years_mode_ajax')=="half":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('sub_years_year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount//2
					year_amount1=budg_mod.yearly_amount1//2
					cur_year=budg_mod.year
					act_amount=0
					if request.POST.get('sub_years_ajax')=="H1":
						start=1
						end=7
						n=1
					else:
						start=7
						end=13
						n=2
					for i in range(start,end):
						for j in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year,order_date_time__month=i):
							act_amount+=j.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					half_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year,
						"n":n
					}
					return render(request,"ajax_response/userdetail/half_yearly_response.html",half_data)
				elif request.POST.get('sub_years_mode_ajax')=="quart":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('sub_years_year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount//4
					year_amount1=budg_mod.yearly_amount1//4
					cur_year=budg_mod.year
					act_amount=0
					start=1
					end=4
					n=1
					if request.POST.get('sub_years_ajax')=="Q1":
						start=1
						end=4
						n=1
					elif request.POST.get('sub_years_ajax')=="Q2":
						start=4
						end=7
						n=2
					elif request.POST.get('sub_years_ajax')=="Q3":
						start=7
						end=10
						n=3
					elif request.POST.get('sub_years_ajax')=="Q4":
						start=10
						end=13
						n=4
					for i in range(start,end):
						for j in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year,order_date_time__month=i):
							act_amount+=j.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					quart_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year,
						"n":n
					}
					return render(request,"ajax_response/userdetail/quart_response.html",quart_data)
				elif request.POST.get('sub_years_mode_ajax')=="month":
					normal=[]
					variance=[]
					next_year=[]
					yea=budget_years.objects.filter(year=request.POST.get('sub_years_year_ajax')).first()
					budg_mod=budget_model.objects.filter(user=brand,year=yea).first()
					year_amount=budg_mod.yearly_amount//12
					year_amount1=budg_mod.yearly_amount1//12
					cur_year=budg_mod.year
					act_amount=0
					m=1
					if request.POST.get('sub_years_ajax')=="Jan":
						m=1
					elif request.POST.get('sub_years_ajax')=="Feb":
						m=2
					elif request.POST.get('sub_years_ajax')=="Mar":
						m=3
					elif request.POST.get('sub_years_ajax')=="Apr":
						m=4
					elif request.POST.get('sub_years_ajax')=="May":
						m=5
					elif request.POST.get('sub_years_ajax')=="Jun":
						m=6
					elif request.POST.get('sub_years_ajax')=="Jul":
						m=7
					elif request.POST.get('sub_years_ajax')=="Aug":
						m=8
					elif request.POST.get('sub_years_ajax')=="Sep":
						m=9
					elif request.POST.get('sub_years_ajax')=="Oct":
						m=10
					elif request.POST.get('sub_years_ajax')=="Nov":
						m=11
					elif request.POST.get('sub_years_ajax')=="Dec":
						m=12
					for j in company_Order.objects.filter(order_date_time__year=datetime.datetime.now().year,order_date_time__month=m):
						act_amount+=j.get_billing_amount
					for i in budget_sectors.objects.filter(user=brand):
						dicti={
							"sector_name":i.name,
							"planned_a":round(year_amount*(i.weight_percent/100),2),
							"planned_b":round(year_amount1*(i.weight_percent/100),2),
							"actual":round(act_amount*(i.weight_percent/100),2),
							"total":round(year_amount*(i.weight_percent/100),2)+round(year_amount1*(i.weight_percent/100),2)
						}
						dicti1={
							"planned_vis":dicti["actual"]-dicti["total"],
							"hit":round((dicti["actual"]*100)/dicti["total"],2)
						}
						dicti2={
							"normal_year":dicti["total"],
							"required":dicti["total"]-dicti["actual"]+dicti["total"]
						}
						normal.append(dicti)
						variance.append(dicti1)
						next_year.append(dicti2)
					month_data={
						"years":budget_model.objects.filter(user=brand),
						"normal":normal,
						"variance":variance,
						"next_year":next_year,
						"n":m
					}
					return render(request,"ajax_response/userdetail/monthly_response.html",month_data)
			return render(request,"userdetail/staff_profile_run_rate.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')


from .models import profile_status_update


def staff_profile_status(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details and details.staff:
			heads=profile_status_update.objects.filter(user__position='H',user__staff_category=details.staff_category)
			managers=profile_status_update.objects.filter(user__position='M',user__staff_category=details.staff_category)
			staffs=profile_status_update.objects.filter(user__position='C',user__staff_category=details.staff_category)
			# heads=detail.objects.filter(position='H',staff_category=details.staff_category)
			# managers=detail.objects.filter(position='M',staff_category=details.staff_category)
			# staffs=detail.objects.filter(position='C',staff_category=details.staff_category)
			data={
				"details":details,
				"heads":heads,
				"managers":managers,
				"staffs":staffs
			}
			# print(request.POST)
			if request.POST.get('my_status_text_ajax'):
				status_obj=profile_status_update(
						status_text=request.POST.get('my_status_text_ajax'),
						daily_achi=request.POST.get('my_status_achi_ajax'),
						daily_hurd=request.POST.get('my_status_hurd_ajax'),
						order_no=request.POST.get('my_status_order_ajax'),
						color=request.POST.get('color_my_status_ajax'),
						user=details,
						date=request.POST.get('my_status_date_ajax'),
						time=request.POST.get('my_status_time_ajax'),
					)
				status_obj.save()
				print("done")
				return JsonResponse({"done":True})
			if request.POST.get('user_email_ajax'):
				user_details=detail.objects.filter(email=request.POST.get('user_email_ajax')).first()
				status_obj=profile_status_update.objects.filter(user=user_details).last()
				data={
					"color":status_obj.color,
					"achi":status_obj.daily_achi,
					"hurd":status_obj.daily_hurd,
					"status_text":status_obj.status_text,
					"order":status_obj.order_no,
					"updated":status_obj.updated_on
				}
				return JsonResponse(data)
			from datetime import datetime,date
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			co = company_Order.objects.filter(staffs_Allocated=details)

			return render(request,"staff/staff_profile_status.html",{"co":co, "current_time":current_time, "data":data})
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')

def staff_profile_status_view_statuses(request):
	print("hello")
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if request.method=="POST":
			from datetime import datetime,date
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			co = company_Order.objects.filter(staffs_Allocated=details)
			module = request.POST.getlist("checkbox[]")
			date = request.POST.get("date_update","")
			order = request.POST.get("order_no","-")
			print(date)
			print(order)
			print(module)
			mine = []
			if "daily_hurd" in module:
				heads=profile_status_update.objects.filter(user__position='H',user__staff_category=details.staff_category,daily_achi="",date=date,order_no=order)
				managers=profile_status_update.objects.filter(user__position='M',user__staff_category=details.staff_category,daily_achi="",date=date,order_no=order)
				staffs=profile_status_update.objects.filter(user__position='S',user__staff_category=details.staff_category,daily_achi="",date=date,order_no=order)
				mine = mine + list(heads) + list(managers) + list(staffs) 
				print(mine)
			if "daily_achi" in module:
				heads=profile_status_update.objects.filter(user__position='H',user__staff_category=details.staff_category,daily_hurd="",date=date,order_no=order)
				managers=profile_status_update.objects.filter(user__position='M',user__staff_category=details.staff_category,daily_hurd="",date=date,order_no=order)
				staffs=profile_status_update.objects.filter(user__position='S',user__staff_category=details.staff_category,daily_hurd="",date=date,order_no=order)			
				mine = mine + list(heads)
				# print(mine)
			return render(request,"staff/staff_profile_statuses.html",{"co":co,"mine":mine,"isPost":True})
		from datetime import datetime
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		currentDT=datetime.now()
		date=currentDT.strftime("%Y-%m-%d")
		lay=[]
		heads=profile_status_update.objects.filter(user__position='H',user__staff_category=details.staff_category,date=date)
		managers=profile_status_update.objects.filter(user__position='M',user__staff_category=details.staff_category,date=date)
		staffs=profile_status_update.objects.filter(user__position='S',user__staff_category=details.staff_category,date=date,)
		lay = lay + list(heads) + list(managers) + list(staffs)
		print(lay)
		co = company_Order.objects.filter(staffs_Allocated=details)
		return render(request,"staff/staff_profile_statuses.html",{"co":co, "lay":lay, "isPost":False})
	else:
		return redirect('/userdetail/login')

def alteration_assortment(request,order_no,email):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details and detail.staff:
			order=company_Order.objects.filter(order_no=order_no).first()
			if order:
				assort=assortment.objects.filter(order_no=order,user=email).first()
				if assort:
					data={
						"assort":assort
					}
					return render(request,"userdetail/alteration_assortment.html",data)
				else:
					return redirect('/userdetail/logout')
			else:
				return redirect('/userdetail/logout')
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')



def staff_profile_orders_cutemp(request,order_no=None,*args,**kwargs):
		search=kwargs.get('NavValue')
		print ("NAVVALUE:  "+str(search))
		order=company_Order.objects.get(order_no=order_no)
		orders=company_Order.objects.all().filter(order_no=order_no).values('plus_Quantity_Percentage','minus_Quantity_Percentage','sample_quantity')
		print ("HELLO")
		print (orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage'])
		if orders[0]['sample_quantity']==None:
			sample=0
		else:
			sample=orders[0]['sample_quantity']
		differ=search-(orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage']+sample)
		print (differ,sample)
		extra=(100+orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage'])/100
		sam_perc=(100+sample+differ)/100
		#diff_perc=(100+differ)/100
		#print (diff_perc,sam_perc)
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		colors_cum_prod=[]
		address_cum_prod=[]
		
		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
						if not (j.color in colors_cum_prod):
								colors_cum_prod.append(j.color)
						if not (j.address in address_cum_prod):
								address_cum_prod.append(j.address)
		sizes_cum_prod.sort()
		map_prod={}
		extra_prod={}
		stock={}
		for i in kjh:
				for j in colors_cum_prod:
						for k in address_cum_prod:
								for l in sizes_cum_prod:
										gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
										if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
												if (differ==0):
													map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
													extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*extra)
													stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*sam_perc)
												else:
													map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
													extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*extra)
													stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*(sam_perc))
													#stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*(diff_perc))
													print (stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)])
										elif gfb:
												map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												extra_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												stock[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												for m in sizes_cum_prod:
														map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
														extra_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
														stock[(str(j.id)+"_"+str(k.id))][1].append(0)
												if (differ==0):
													map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
													extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*extra)
													stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*sam_perc)
												else:
													map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
													extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*extra)
													stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*(sam_perc))
													#stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*(diff_perc))
													print (stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)])
												#map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
												#extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.04)
												#stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*1.1)
		print(map_prod)
		print(sizes_cum_prod)
		return render(request,'vendor/vendor_profile_orders_cut.html',{'order':order,'map_prod':map_prod,'sizes_cum_prod':sizes_cum_prod,'extra_prod':extra_prod,'stock':stock})

def staff_profile_orders_cut(request,order_no=None,*args,**kwargs):
		conc_percent=kwargs.get('conc')
		#order_n=request.GET.get('order_n')
		#print ("search:  "+str(search))
		accepted=list(conc_percent)[0]
		rejected=list(conc_percent)[1]
		stock=list(conc_percent)[2]
		
		order=company_Order.objects.get(order_no=order_no)
		orders=company_Order.objects.all().filter(order_no=order_no).values('plus_Quantity_Percentage','minus_Quantity_Percentage','sample_quantity')
		print ("HELLO")
		print (orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage'])
		if orders[0]['sample_quantity']==None:
			sample=0
		else:
			sample=orders[0]['sample_quantity']
		if (orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage']+sample<int(accepted)+int(rejected)+int(stock)):
			whole_percent=(100+int(accepted)+int(rejected)+int(stock))/100
			accepted=int(accepted)
			rejected=int(rejected)
			stock_no=int(stock)
		else:
			whole_percent=(100+orders[0]['plus_Quantity_Percentage']+orders[0]['minus_Quantity_Percentage']+sample)/100
			accepted=int(orders[0]['plus_Quantity_Percentage'])
			rejected=int(orders[0]['minus_Quantity_Percentage'])
			stock_no=int(sample)
		print ("ACCEPTED", accepted)
		print ("REJECTED", rejected)
		print ("STOCK", stock)
		print ("PERCENT: "+str(whole_percent))
		
		kjh=production_order.objects.filter(order=order).order_by('production_no')
		prod=[]
		sizes_cum_prod=[]
		colors_cum_prod=[]
		address_cum_prod=[]

		for i in kjh:
				for j in i.sizes.all():
						if not(j.size_label in sizes_cum_prod) and j.size_label:
								sizes_cum_prod.append(j.size_label)
						if not (j.color in colors_cum_prod):
								colors_cum_prod.append(j.color)
						if not (j.address in address_cum_prod):
								address_cum_prod.append(j.address)
		sizes_cum_prod.sort()
		map_prod={}
		extra_prod={}
		stock={}
		for i in kjh:
				for j in colors_cum_prod:
						for k in address_cum_prod:
								for l in sizes_cum_prod:
										gfb=i.sizes.all().filter(color=j,address=k,size_label=l).first()
										if ((str(j.id)+"_"+str(k.id)) in map_prod) and gfb:
												map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
												extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity)
												stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*whole_percent)
												
										elif gfb:
												map_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												extra_prod[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												stock[(str(j.id)+"_"+str(k.id))]=[[j,k],[]]
												for m in sizes_cum_prod:
														map_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
														extra_prod[(str(j.id)+"_"+str(k.id))][1].append(0)
														stock[(str(j.id)+"_"+str(k.id))][1].append(0)
												
												map_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=gfb.quantity
												extra_prod[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity)
												stock[(str(j.id)+"_"+str(k.id))][1][sizes_cum_prod.index(l)]+=int(gfb.quantity*whole_percent)
												
												
		
		print(map_prod)
		print(sizes_cum_prod)
		return render(request,'vendor/vendor_profile_orders_cut.html',{'order':order,'map_prod':map_prod,'sizes_cum_prod':sizes_cum_prod,'extra_prod':extra_prod,'stock':stock,'order_no':order_no,'accepted':accepted,'rejected':rejected,'stock_no':stock_no})

from .forms import *

def academic_profile(request):
	if request.user.is_authenticated:
		info=academic.objects.filter(email=request.user.email).first()
		form=AcadForm(instance=info)
		if request.method=='POST':
			form=AcadForm(request.POST,instance=info)
			print(form.is_valid())
			print(form.errors)
			if form.is_valid():
				name=request.POST.get('name')
				school=request.POST.get('school')
				degree=request.POST.get('degree')
				field_of_study=request.POST.get('field_of_study')
				start_date=request.POST.get('start')
				end_date=request.POST.get('end')
				grade=request.POST.get('grade')
				a=form.save(commit=False)
				a.email=request.user.email
				a.save()
			return redirect('academic_profile')
	return render(request,'userdetail/academic_profile.html',{'form':form})
	
import datetime
def professional_profile(request):
	if request.user.is_authenticated:
		info=professional_pro.objects.filter(email=request.user.email).first()
		form=ProfessionalForm(instance=info)
		pro_info=add_project.objects.filter(email=request.user.email).first()
		pro_form=ProjectForm(instance=pro_info)
		skill_info=add_skill.objects.filter(email=request.user.email).first()
		skill_form=SkillForm(instance=skill_info)
		cert_info=add_certifications.objects.filter(email=request.user.email).first()
		cert_form=CertForm(instance=cert_info)
		if request.method=='POST' and 'submit_exp' in request.POST:
			form=ProfessionalForm(request.POST,instance=info)
			print('exp form',form.is_valid())
			print(form.errors)
			if form.is_valid():
				name=request.POST.get('name')
				title=request.POST.get('title')
				employment_type=request.POST.get('employment_type')
				company=request.POST.get('company')
				current_company=request.POST.get('current_company')
				location=request.POST.get('location')
				start_date=request.POST.get('start_date')
				description=request.POST.get('description')
				if current_company=='on':
					end_date=None
					check=True
				else:
					end_date=request.POST.get('end_date')
					check=False
				a=form.save(commit=False)
				a.email=request.user.email
				a.save()
				return redirect('professional_profile')

		elif request.method=='POST' and 'submit_skill' in request.POST:
			skill_form=SkillForm(request.POST,instance=skill_info)
			print('skill form',skill_form.is_valid())
			print(skill_form.errors)
			if skill_form.is_valid():
				name=request.POST.get('name')
				sf=skill_form.save(commit=False)
				sf.email=request.user.email
				sf.save()
		elif request.method=='POST'and 'submit_project' in request.POST:
			pro_form=ProjectForm(request.POST,instance=pro_info)
			print('project',pro_form.is_valid())
			print(pro_form.errors)
			if pro_form.is_valid():
				project_name=request.POST.get('project_name')
				start_date=request.POST.get('start_date')
				end_date=request.POST.get('end_date')
				description=request.POST.get('description')
				project_url=request.POST.get('project_url')
				pf=pro_form.save(commit=False)
				pf.email=request.user.email
				pf.save()
				return redirect('professional_profile')

		elif request.method=='POST'and 'submit_cert' in request.POST:
			cert_form=CertForm(request.POST,instance=cert_info)
			print('cert',cert_form.is_valid())
			print(cert_form.errors)
			if cert_form.is_valid():
				title=request.POST.get('title')
				organization=request.POST.get('organization')
				issued_date=request.POST.get('issued_date')
				issued_id=request.POST.get('issued_id')
				cf=cert_form.save(commit=False)
				cf.email=request.user.email
				cf.save()
				return redirect('professional_profile')
	return render(request,'userdetail/professional_profile.html',{'form':form,'skill_form':skill_form,'pro_form':pro_form,'cert_form':cert_form})
def social_profile(request):
	if request.user.is_authenticated:
		info=social.objects.filter(email=request.user.email).first()
		form=SocialForm(instance=info)
		if request.method=='POST':
			form=SocialForm(request.POST,instance=info)
			print(form.is_valid())
			print(form.errors)
			if form.is_valid():
				dob=request.POST.get('dob')
				gender=request.POST.get('gender')
				marital=request.POST.get('marital')
				hometown=request.POST.get('hometown')
				hobbies=request.POST.get('hobbies')
				mobile_number=request.POST.get('mobile_number')
				a=form.save(commit=False)
				a.email=request.user.email
				a.save()
				return redirect('social_profile')
	return render(request,'userdetail/social_profile.html',{'form':form})
def medical_profile(request):
	if request.user.is_authenticated:
		info=medical.objects.filter(email=request.user.email).first()
		form=MedForm(instance=info)
		if request.method=='POST':
			form=MedForm(request.POST,instance=info)
			if form.is_valid():
				age=request.POST.get('age')
				height=request.POST.get('height')
				weight=request.POST.get('weight')
				blood_group=request.POST.get('blood_group')
				disability=request.POST.get('disability')
				medical_issues=request.POST.get('medical_issues')
				diseases=request.POST.get('diseases')
				a=form.save(commit=False)
				a.email=request.user.email
				a.save()
			return redirect('medical_profile')
	return render(request,'userdetail/medical_profile.html')		






def product_order(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			email=request.user.email
			product_name=request.POST['product']
			supercategory=super_category.objects.filter(service=False)
			cus_address=customer_address.objects.filter(email=email).all()
			custom_address=detail.objects.filter(email=request.user.email).values('address')[0]['address']
			pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
			if units.objects.filter(supercategory_id=pro_id).exists():
				att=True
				unit=units.objects.filter(supercategory_id=pro_id).all()
				return render(request,'userdetail/product_order.html',{'supercategory':supercategory,'product_name':product_name,'att':att,'unit':unit,
					'email':email,'cus_address':cus_address,'customer_address':cus_address,'customer_address':custom_address})
			else:
				att=False
				
				return render(request,'userdetail/product_order.html',{'supercategory':supercategory,'product_name':product_name,'att':att,'email':email,'cus_address':cus_address,
					'customer_address':custom_address})

		else:
			email=request.user.email
			supercategory=super_category.objects.filter(service=False)
			att=False
			lt2=[]
			custom_address=detail.objects.filter(email=request.user.email).values('address')[0]['address']
			cus_address=customer_address.objects.filter(email=email).all()
			return render(request,'userdetail/product_order.html',{'supercategory':supercategory,'att':att,'email':email,
				'cus_address':cus_address,'customer_address':custom_address})
	else:
		return redirect('login_page')

def order_product(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			email=request.user.email
			product_name=request.GET.get('product_name')
			quantity=request.POST['quantity']
			cus_address=customer_address.objects.filter(email=email).all()
			custom_address=detail.objects.filter(email=request.user.email).values('address')[0]['address']

			pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
			seller_ids=units.objects.filter(supercategory_id=pro_id,unit=quantity).values('seller_id').all()
			seller_lt=[]
			att=True

			unit=units.objects.filter(supercategory_id=pro_id).all()
			supercategory=super_category.objects.filter(service=False)
			for i in seller_ids:
				seller_lt.append(i['seller_id'])
			seller_name=[]
			for i in seller_lt:
				a=detail.objects.filter(id=i).values('email').all()
				for j in a:
					seller_name.append(j['email'])
			return render(request,'userdetail/product_order.html',{'supercategory':supercategory,'seller_name':seller_name,'pro_id':pro_id,'quantity':quantity,'unit':unit,'att':att,
				'email':request.user.email,'product_name':product_name,'cus_address':cus_address,'customer_address':custom_address})


		
		
		



	
def seller_filter(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			email=request.user.email
			pro_id=request.GET.get('pro_id')
			cus_address=customer_address.objects.filter(email=email).all()
			quantity=request.GET.get('quantity')
			seller_ids=units.objects.filter(supercategory_id=pro_id,unit=quantity).values('seller_id').all()
			seller_lt=[]
			att=True
			unit=units.objects.filter(supercategory_id=pro_id).all()
			supercategory=super_category.objects.filter(service=False)
			for i in seller_ids:
				seller_lt.append(i['seller_id'])
			seller_name=[]
			for i in seller_lt:
				a=detail.objects.filter(id=i).values('email').all()
				for j in a:
					seller_name.append(j['email'])
			seller=request.POST['seller']
			supercategory=super_category.objects.filter(service=False)
			#pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
			unit=units.objects.filter(supercategory_id=pro_id).all()
			att=True
			seller_address=detail.objects.filter(email=seller).values('address')[0]['address']
			custom_address=detail.objects.filter(email=request.user.email).values('address')[0]['address']
			seller_landmark=detail.objects.filter(email=seller).values('Landmark')[0]['Landmark']
			return render(request,'userdetail/product_order.html',{'supercategory':supercategory,'att':att,'pro_id':pro_id,
				'quantity':quantity,'seller':seller,'unit':unit,'seller_address':seller_address,'seller_landmark':
				seller_landmark,'email':request.user.email,'seller_name':seller_name,'cus_address':cus_address,
				'customer_address':custom_address})
		
from .models import productorder
def final_product_order(request):
	if request.user.is_authenticated:
		pro_id=request.GET.get('pro_id')
		details=detail.objects.filter(email=request.user.email).first()
		product_name=super_category.objects.filter(id=pro_id).values('name')[0]['name']
		quantity=request.GET.get('quantity')
		seller=request.GET.get('seller')
		no_of_quantity=request.POST['no_of_quantity']
		specifications=request.POST['specifications']
		vendor_address=request.POST['vendor_address']
		vendor_landmark=request.POST['vendor_landmark']
		customer_address=request.POST['cus_address']
		customer_landmark=request.POST['cus_landmark']
		customer_id=request.POST['customer_id']
		email=request.user.email
		user_id=detail.objects.filter(email=email).values('id')[0]['id']
		date=d=datetime.datetime.now().strftime('%H:%M:%S')
		price=product.objects.filter(product_Supercategory_id=pro_id).values('price')[0]['price']
		transaction_id=str(user_id)+str(pro_id)+str(''.join(list(date.split(':'))))
		a=productorder(transaction_id=transaction_id,product_id=pro_id,product_name=product_name,specifications=specifications,
			quantity=quantity,no_of_quantity=no_of_quantity,vendor=seller,vendor_address=vendor_address,vendor_landmark=vendor_landmark,
			customer_drop_address=customer_address,customer_landmark=customer_landmark,customer_id=customer_id,price=price)
		a.save()
		
		if details.staff:
			return redirect('/userdetail/staff_profile')
		elif details.vendor and details.seller_category.name=="Products Vendor":
			return redirect('/userdetail/seller_profile')
		elif details.vendor:
			return redirect('/userdetail/vendor_profile')
		elif details.buisness_Customer:
			return redirect('/buisness/buisness_profile')
		else:
			return HttpResponse('saved')
def services(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			supercategory=super_category.objects.filter(service=True)
			return render(request,'userdetail/services.html',{'supercategory':supercategory,'email':request.user.email})
		else:
			supercategory=super_category.objects.filter(service=True)

			return render(request,'userdetail/services.html',{'supercategory':supercategory,'email':request.user.email})
	else:
		return redirect('login_page')

'''def save_book(request):
	x=request.GET['name']
	supercategory=super_category.objects.all()
	pro_id=super_category.objects.filter(name=x).values('id')[0]['id']
	if units.objects.filter(supercategory_id=pro_id).exists():
		att=True
		unit=units.objects.filter(supercategory_id=pro_id).all()
		#return render(request,'userdetail/product_order.html',{'supercategory':supercategory,'product_name':product_name,'att':att,'unit':unit})
	else:
		att=False
	
		#return render(request,'userdetail/product_order.html',{'supercategory':supercategory,'product_name':product_name,'att':att})
#	return HttpResponse(json.dumps({"supercategory":supercategory}), content_type="application/json")
	#SomeModel_json = serializers.serialize("json", super_category.objects.all())
	#data = {"SomeModel_json": SomeModel_json}
	#print(data)
	#return HttpResponse(json.dumps({'data':data}), content_type="application/json")
	#return JsonResponse(supercategory)	
	data=units.objects.all()
	data_obj=list(data.values())
	print(data_obj)
	return HttpResponse(data_obj)
	#return HttpResponse(json.dumps({'data': data_obj}), content_type="application/json")'''

from product.models import service_add
def service_order(request):
	if request.user.is_authenticated:
		product_name=request.POST['service_name']
		supercategory=super_category.objects.filter(service=True)
		pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
			
		service=service_add.objects.filter(supercategory_id=pro_id).all()
		att=True
		certifications=service_certifications.objects.all()
		print(product_name)
		print(service)
		return render(request,'userdetail/services.html',{'supercategory':supercategory,'product_name':product_name,'service':service,'att':att,
			'certifications':certifications,'email':request.user.email})
		

def order_service(request):
	if request.user.is_authenticated:
		product_name=request.GET.get('service_name')
		price_range=request.POST['price_range']
		pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
		seller_ids=service_add.objects.filter(supercategory_id=pro_id,price_range=price_range).values('seller_id').all()
		seller_lt=[]
		att=True
		certifications=service_certifications.objects.all()
		service=service_add.objects.filter(supercategory_id=pro_id).all()
		supercategory=super_category.objects.filter(service=True)
		for i in seller_ids:
			seller_lt.append(i['seller_id'])
		seller_name=[]
		for i in seller_lt:
			a=detail.objects.filter(id=i).values('email').all()
			for j in a:
				seller_name.append(j['email'])
		return render(request,'userdetail/services.html',{'supercategory':supercategory,'seller_name':seller_name,'pro_id':pro_id,'price_range':price_range,'service':service,
			'certifications':certifications,'email':request.user.email})



def final_service(request):
	if request.user.is_authenticated:
		pro_id=request.GET.get('pro_id')
		product_name=super_category.objects.filter(id=pro_id).values('name')[0]['name']
		price_range=request.GET.get('price_range')
		seller=request.POST['vendor']
		service_date=request.POST['service_date']
		service_time=request.POST['service_time']
		service_rating=request.POST['rating']
		certi=request.POST['certifications']
		certifications=service_certifications.objects.filter(name=certi).values('id')[0]['id']
		terms=request.POST['terms_and_condition']
		customer_id=request.POST['customer_id']
		user_id=detail.objects.filter(email=request.user.email).values('id')[0]['id']
		date=d=datetime.datetime.now().strftime('%H:%M:%S')
		transaction_id=str(user_id)+str(pro_id)+str(''.join(list(date.split(':'))))
		a=serviceorder(transaction_id=transaction_id,service_id=pro_id,service_name=product_name,price_range=price_range,
			vendor=seller,service_date=service_date,service_time=service_time,
			service_rating=service_rating,certifications_id=certifications,
			terms_and_conditions=terms,customer_id=customer_id)

		a.save()
		
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			return redirect('/userdetail/staff_profile')
		elif details.vendor and details.seller_category.name=="Products Vendor":
			return redirect('/userdetail/seller_profile')
		elif details.vendor:
			return redirect('/userdetail/vendor_profile')
		elif details.buisness_Customer:
			return redirect('/buisness/buisness_profile')
		
		

def customize(request):
	if request.user.is_authenticated:
		email=request.user.email

		return render(request,'userdetail/customize.html',{'email':email})
	else:
		return redirect('login_page')
def customize_service(request):
	if request.user.is_authenticated:
		requirement=request.POST['requirement']
		service_date=request.POST['service_date']
		service_time=request.POST['service_time']
		customer_id=request.POST['customer_id']
		a=customizeorder(requirement=requirement,service_time=service_time,
			service_date=service_date,customer_id=customer_id)
		
		a.save()
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			return redirect('/userdetail/staff_profile')
		elif details.vendor and details.seller_category.name=="Products Vendor":
			return redirect('/userdetail/seller_profile')
		elif details.vendor:
			return redirect('/userdetail/vendor_profile')
		elif details.buisness_Customer:
			return redirect('/buisness/buisness_profile')
		
		
def subscription(request):
	"""
		For Quick subscription
	"""
	if request.user.is_authenticated:
		from json import dumps

		products = product.objects.filter(available_for_subscription=True)
		products_mapping = {}
		for prod in products:
			discount = prod.subscription_discount
			price = prod.price*((100 - discount)/100)
			product_details = {
								'title': prod.title,
								'manufacturer': prod.manufacturername,
							 	'price': price,
								 'unit_of_measurement': prod.unit_of_measurement
							  }
			products_mapping[prod.slug] = product_details
		
		# is_service=False
		products_json = dumps(products_mapping)
		current_date = datetime.date.today()
		return render(request,'userdetail/quickSubscription.html',
					context={'products': products_mapping,
							 'order_frequency': frequency,
							 'current_date': current_date,
							 'product_json': products_json})
	else:
		return redirect('login_page')

def newSubscription(request):
	'''
		New method for subscription
		changes routing of subscription/ in urls.py
	'''
	if request.user.is_authenticated:
		products = product.objects.filter(available_for_subscription=True)
		print(products)
		products_mapping = {}
		for prod in products:
			product_details = {'title': prod.title, 'manufacturer': prod.manufacturername, 'price': prod.price, 'image': prod.image1, 'prod': prod}
			products_mapping[prod.slug] = product_details
		print(products_mapping)
		return render(request, 'userdetail/subscription.html', context={'products': products_mapping})
	else:
		return redirect('login_page')

def subscriptionSearch(request):
	query = request.GET.get('query')

	products = product.objects.filter(available_for_subscription=True, title__icontains=query)
	if len(products) == 0:
		return HttpResponse("<h1>No Product Found</h1>")
	products_mapping = {}
	for prod in products:
		product_details = {'title': prod.title, 'manufacturer': prod.manufacturername, 'price': prod.price, 'prod': prod}
		print(prod.image1)
		products_mapping[prod.slug] = product_details
	return render(request, 'userdetail/subscription.html', context={'products': products_mapping})

def productSubscribe(request, slug):
	'''
		Method to redirect to specific product details
	'''
	query=product.objects.get(slug=slug)
	query1=query.product_Supercategory.get().attributes.all()
	frequency=order_frequency.objects.all()
	#   For the supermarket :- subcategory display in the navbar
	product_quan=product.objects.all()
	marketid =[]
	product_market_id=[]
	product_market_name=[]
	electronic = None
	market = None
	
	for item in product_quan:
		x = item.product_Category.all()
		for i in x:
			print("hello  ",i.id)
			if i not in product_market_id:
				product_market_id.append(i.id)
	for i in product_market_id:
		pro_name=category.objects.filter(id=i).values('name')[0]['name']
		market =(product.objects.filter(product_Category=i).distinct('product_Subcategory'))

		if pro_name == 'Supermarket':
			marketid.append(i)
			market =(product.objects.filter(product_Category=i).distinct('product_Subcategory'))

		elif(pro_name == 'Electronics'):
			electronic = (product.objects.filter(product_Category=i).distinct('product_Subcategory'))	
	li=[]
	li1=[]
	for i in query1:
		li1.append(i)
		li.append(deepcopy(li1))
		li1.pop()
	query2=[]
	length=len(li)

	query2.append(query.manufacturername)
	query2.append(query.manufacturerno)
	query2.append(query.volume)
	query2.append(query.weight)
	query2.append(query.batteriesincluded)
	query2.append(query.batteriesno)
	query2.append(query.wattage)
	query2.append(query.dangerousgood)
	query2.append(query.shape)
	query2.append(query.length)
	query2.append(query.width)
	query2.append(query.height)
	query2.append(query.countryorigin)
	query2.append(query.pattern)
	query2.append(query.shafttype)
	query2.append(query.features)
	query2.append(query.style)
	query2.append(query.graphics)
	query2.append(query.powersource)
	query2.append(query.occasion)
	query2.append(query.noofitems)
	query2.append(query.sale)
	query2.append(query.salestartdate)
	query2.append(query.saleenddate)
	query2.append(query.salediscount)
	query2.append(query.allparts)
	query2.append(query.specifications)
	query2.append(query.keywords)
 ####3End of the added attris############
	query2.append(query.atrribute29)
	query2.append(query.atrribute30)
	query2.append(query.atrribute31)
	query2.append(query.atrribute32)
	query2.append(query.atrribute33)
	query2.append(query.atrribute34)
	query2.append(query.atrribute35)
	query2.append(query.atrribute36)
	query2.append(query.atrribute37)
	query2.append(query.atrribute38)
	query2.append(query.atrribute39)
	query2.append(query.atrribute40)
	query2.append(query.atrribute41)
	query2.append(query.atrribute42)
	query2.append(query.atrribute43)
	query2.append(query.atrribute44)
	query2.append(query.atrribute45)
	query2.append(query.atrribute46)
	query2.append(query.atrribute47)
	query2.append(query.atrribute48)
	query2.append(query.atrribute49)
	query2.append(query.atrribute50)
	query2.append(query.atrribute51)
	query2.append(query.atrribute52)
	query2.append(query.atrribute53)
	query2.append(query.atrribute54)
	query2.append(query.atrribute55)
	query2.append(query.atrribute56)
	query2.append(query.atrribute57)
	query2.append(query.atrribute58)
	query2.append(query.atrribute59)
	query2.append(query.atrribute60)
	query2.append(query.atrribute61)
	query2.append(query.atrribute62)
	query2.append(query.atrribute63)
	query2.append(query.atrribute64)
	query2.append(query.atrribute65)
	query2.append(query.atrribute66)
	query2.append(query.atrribute67)
	query2.append(query.atrribute68)
	query2.append(query.atrribute69)
	query2.append(query.atrribute70)
	query2.append(query.atrribute71)
	query2.append(query.atrribute72)
	query2.append(query.atrribute73)
	query2.append(query.atrribute74)
	query2.append(query.atrribute75)
	query2.append(query.atrribute76)
	query2.append(query.atrribute77)
	query2.append(query.atrribute78)
	query2.append(query.atrribute79)
	query2.append(query.atrribute80)
	query2.append(query.atrribute81)
	query2.append(query.atrribute82)
	query2.append(query.atrribute83)
	query2.append(query.atrribute84)
	query2.append(query.atrribute85)
	query2.append(query.atrribute86)
	query2.append(query.atrribute87)
	query2.append(query.atrribute88)
	query2.append(query.atrribute89)
	query2.append(query.atrribute90)
	query2.append(query.atrribute91)
	query2.append(query.atrribute92)
	query2.append(query.atrribute93)
	query2.append(query.atrribute94)
	query2.append(query.atrribute95)
	query2.append(query.atrribute96)
	query2.append(query.atrribute97)
	query2.append(query.atrribute98)
	query2.append(query.atrribute99)
	query2.append(query.atrribute100)
	for i in range(length):
		li[i].append(query2[i])
	
	# print(li)
	# couni=product.objects.count()
	query5=product.objects.all().exclude(slug=slug)[:6]
	# query5=random.choices(list(query5.values()),k=6)
	sizes=[]
	#dispsize=[]
	for i in query.size_color_quantity_set.all():
		if not(i.size in sizes):
			if i.unit != None:
				disp= str(i.size)+" "+ str(i.unit)
			else:
				disp=i.size
			sizes.append(disp)

			#dispsize.append(disp)
	re=[]
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details:
			oj=recently_viewed.objects.filter(user=details,prod=query).first()
			if oj:
				oj.time=datetime.datetime.now()
			else:
				oj=recently_viewed(user=details,prod=query,time=datetime.datetime.now())
			oj.save()
			re=recently_viewed.objects.filter(user=details).order_by('-time')[:6]
		else:
			re=[]
	x=""+str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)
	if str(query.last_trending) == x:
		product.objects.filter(slug=slug).update(trending_view=query.trending_view+1)
	else:
		product.objects.filter(slug=slug).update(trending_view=1)
	tred=product.objects.all().order_by('-trending_view')[:6]
	label_attr = [[l_attr.label_attribute.name, l_attr.value] for l_attr in label_Attributes_Values.objects.filter(prod=query.pk)]
	com_attributes = [[com_attr.attribute, com_attr.value] for com_attr in product_common_attribute_values.objects.filter(prod=query.pk)]
	extraatts=extradetails.objects.filter(prod=query.pk)
	#ex_attr=[]
	#index=1
	#print(extraatts)
	extraattributes=[]
	if len(extraatts) !=0:
		#print(extraatts.values())
		for i in extraatts.values():
			ex_attr=i
		
		for index in range(1,21):
			atri="attribute"+str(index)
			val="value"+str(index)
			if ex_attr[atri]=="Product Tax Code" or ex_attr[atri]=="Release Date":
				continue
			if ex_attr[atri]=="" and ex_attr[val]=="" or ex_attr[val]==None:
				break
			if ex_attr[val]=="":
				continue
			lt=[ex_attr[atri],ex_attr[val]]
			extraattributes.append(lt)

		print(extraattributes)


	extraattributes.append(['Made in',query.made_in])
	if query.packed!=None:
		extraattributes.append(['Packed',query.packed])
	if query.old_product!=None:
		extraattributes.append(['Old Product',query.old_product])

	list_opt=[['Brand', query.brand]]
	if query.label!=None:
		print('label',query.label)
		list_opt.append(['Label',query.label])
	if query.fit !=None:
		list_opt.append(['Fit',query.fit])
	if query.season !=None:
		list_opt.append(['Season',query.season])

	if query.washcare!=None:
		list_opt.append(['WashCare',query.washcare])

	attributes = com_attributes + list_opt  + label_attr + extraattributes
	print(attributes)

	prod_id=product.objects.filter(slug=slug)[0].product_code
	wish="false"
	items=0
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		items=OrderItem.objects.filter(customer=currUser)
		if items:
			items=OrderItem.objects.filter(customer=currUser).values('quantity')[0]['quantity']
		else: 
			items = 0

	#print(prod_id)
		obj=wishlist.objects.filter(customer=currUser,product=product.objects.get(product_code=prod_id))
		if obj:
			wish="true"
		else:
			wish="false"

	objimg=Add_images.objects.filter(prod=query)
	images=[]
	print(objimg.values())
	for i in objimg:
		images.append(i)
	
	## For service quantity:
	# product_name = product.objects.filter(slug=slug).first().title
	# pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
	# if super_category.objects.filter(name=product_name,service=True):
	# 	service_unit=service_add.objects.filter(supercategory_id=pro_id).all()
	# 	is_service=True
	# else:
	# 	service_unit=units.objects.filter(supercategory_id=pro_id).all()
	# 	is_service=False

	data={
		"obj":query,
		"data":li,
		"similiar":query5,
		"sizes":sizes,
		"recent":re,
		"tred":tred,
		"attributes":attributes,
		"product_code":prod_id,
		"cartItems":items,
		"wishlist":wish,
		"images":images,
		"market":market, 
		'electronic':electronic,
		'frequency': frequency,
	}
	import re
	if request.POST.get('sizes_ajax'):
		val=request.POST.get('sizes_ajax')
		#print(val)
		output = int(re.findall(r'\d+', val)[0])
		unit=re.findall(r'\D+', val)
		if len(unit)>0:
			unit=unit[0].replace(" ","")
		else:
			unit=None
		if unit !=None:
			objs=query.size_color_quantity_set.all().filter(size=output,unit=unit)
		else:
			objs=query.size_color_quantity_set.all().filter(size=output)
		#print(objs.values())
		cols=[]
		for i in objs:
			if i.quantity!=None and not(i in cols):
				cols.append(i.color)
		
		#print(cols)
		return JsonResponse({"data":cols})
	current_date = datetime.date.today()
	data['current_date'] = current_date

	# product_price(base_price for quantity = 1)
	product_instance = product.objects.filter(slug=slug).first()
	data['discount'] = product_instance.subscription_discount
	data['amount'] = data['base_price'] = product_instance.price*((100 - data['discount'])/100)
	data['unit_of_measurement'] = product_instance.unit_of_measurement
	return render(request,'userdetail/subscriptionDetails.html',context=data)

# def subscriptionCart(request):
# 	'''
# 		Method used to save subscriptions in cart i.e. isPaid = False
# 	'''
# 	print('******* request rec *********')
# 	quantity = request.GET.get('quantity')
# 	amount = request.GET.get('amount')
# 	start_date = request.GET.get('start_date')
# 	end_date = request.GET.get('end_date')
# 	interval = request.GET.get('interval')
# 	shift = request.GET.get('shift')
# 	remark = request.GET.get('remark')
# 	slug = request.GET.get('slug')
# 	print('*******************', slug)
# 	customer_email = request.user
# 	isPaid = False
	
# 	prod = product.objects.filter(slug=slug).first()
# 	product_name = prod.title
# 	vendor = prod.seller

# 	transaction_id = str(request.user.id) + slug + "".join(str(start_date).split("-")) + "0" # O for identification of unpaid items

# 	a = Subscription_Order(
# 			transaction_id = transaction_id,
# 			product_slug = slug,
# 			product_name = product_name,
# 			quantity = quantity,
# 			amount = amount,
# 			interval = interval,
# 			start_date = start_date,
# 			end_date = end_date,
# 			shifts = shift,
# 			remark = remark,
# 			customer_email = customer_email,
# 			vendor_email = vendor,
# 			isPaid = isPaid
# 			)
# 	a.save()
# 	print('*********** SAVED IN SUB CART ***********')
# 	data = {
# 		'message': 'success',
# 		'product_name': product_name,
# 		'quantity': quantity,
# 		'amount': amount,
# 		'interval': interval,
# 		'start_date': start_date,
# 		'end_date': end_date,
# 		'shifts': shift,
# 		'transaction_id': transaction_id
# 	}
# 	return JsonResponse(data)


def subscriptionFinal(request):
	if request.user.is_authenticated:
		data = {}
		data['message'] = 'success'

		# Checking is item already present in cart if yes remove it:
		if request.GET.get('src'):
			transaction_id = request.GET.get('transaction_id')
			
			# delete the item from cart:
			Subscription_Order.objects.filter(transaction_id=transaction_id, isPaid=False).delete()
		
		# Fetching data about the product
		data['quantity'] = request.GET.get('quantity')
		data['start_date'] = request.GET.get('start_date')
		data['end_date'] = request.GET.get('end_date')
		data['remark'] = request.GET.get('remark', '').replace(' ', '-')
		data['slug'] = request.GET.get('slug')
		data['interval'] = request.GET.get('interval', 0)
		data['shift'] = request.GET.get('shift')

		# Fetching data of customer.
		user_email = request.user
		user = detail.objects.filter(email=user_email).first()
		full_name = user.name
		address = user.address

		# adding user data in data
		data['full_name'] = full_name
		data['address'] = address
		data['email'] = str(user_email)
		return JsonResponse(data)
	else:
		return redirect('login_page')

def payForSubscription(request):
	'''
		Demo app to see data transfer
	'''
	if request.user.is_authenticated:
		# Extract user data from previous page:
		email = request.user

		# Extract product data from prev. page.
		slug = request.POST.get('slug')
		quantity = request.POST.get('quantity')
		amount = request.POST.get('amount')
		interval = request.POST.get('interval')
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')
		remarks = request.POST.get('remark')
		shift = request.POST.get('shift')

		transaction_id = str(request.user.id) + slug + "".join(str(start_date).split("-"))

		## data processing to store in subscriptionorder table
		prod = product.objects.filter(slug=slug).first()
		product_name = prod.title
		vendor = prod.seller
		
		# frequency = order_frequency.objects.filter(id=frequency_id).first()
		print(
			transaction_id,
			slug,
			product_name,
			quantity,
			frequency,
			interval,
			shift,
			start_date,
			end_date,
			vendor,
			amount
		)
		# Saving the data:
		a = Subscription_Order(
			transaction_id = transaction_id,
			product_slug = slug,
			product_name = product_name,
			quantity = quantity,
			amount = amount,
			interval = interval,
			start_date = start_date,
			end_date = end_date,
			shifts = shift,
			remark = remarks,
			customer_email = email,
			vendor_email = vendor
			)
		a.save()
		# Adding events for calendar.
		createEvents(a)
		return HttpResponse('Payment')
	else:
		return redirect('login_page')

from product.models import history
def subPayWithWallet(request, slug):
	todays_date = datetime.date.today()
	if slug == 'all':
		# Update Events:
		
		allSubscriptions = Subscription_Order.objects.filter(customer_email = request.user, isPaid=True)
		for subscription in allSubscriptions:
			transaction_id = subscription.transaction_id
			# extract all last unpaid events of this transaction_id
			unpaidEvents = Event.objects.filter(sub_transaction_id=transaction_id, isPaidForEvent = False, start_time__lte = todays_date)
			unpaidEvents.update(isPaidForEvent = True)
		
		amount = request.POST.get('amount')
		hist = history(ordertype="Send", order_id="allSubscriptions", email=request.user.email, total_amount=amount)
		hist.save()
	else:
		transaction_id = slug
		unpaidEvents = Event.objects.filter(sub_transaction_id=transaction_id, isPaidForEvent = False, start_time__lte = todays_date)
		unpaidEvents.update(isPaidForEvent = True)

		amount = request.POST.get('amount')
		hist = history(ordertype="Send", order_id="allSubscriptions", email=request.user.email, total_amount=amount)
		hist.save()
	return redirect('cart')

def subscriptionCheckout(request):
	transaction = request.POST.get('transaction')
	terms = TermAndCondition.objects.all().order_by('-version').first().subscriptionTerms
	customer_email = request.user
	user = detail.objects.filter(email=customer_email).first()
	if transaction == "allcheckout":
		subscriptions = Subscription_Order.objects.filter(customer_email=request.user, isPaid=False)
		maps = {}
		totalAmount = 0
		for subscription in subscriptions:
			maps[subscription.transaction_id] = {
					'product_name': subscription.product_name,
					'quantity': subscription.quantity,
					'amount': subscription.amount
			}
			totalAmount += subscription.amount
		maps_json = json.dumps(maps)
		return render(request, 'userdetail/subscriptionCheckout.html', context={'maps': maps, 'totalPrice': totalAmount, 'maps_json': maps_json, 'terms': terms, 'subs': True, 'user': user})
	else:
		if transaction == 'payForAll':
			todays_date = datetime.date.today()
			# get all subscriptions
			allSubscriptions = Subscription_Order.objects.filter(customer_email = request.user, isPaid=True)
			maps = {}
			totalAmount = 0
			noContent = False
			for subscription in allSubscriptions:
				transaction_id = subscription.transaction_id
				# extract all last unpaid events of this transaction_id
				unpaidEvents = Event.objects.filter(sub_transaction_id=transaction_id, isPaidForEvent = False, start_time__lte = todays_date, isStopped=False)
				if len(unpaidEvents) != 0:
					numberOfUnpaidEvents = len(unpaidEvents)
					priceOfOneEvent = subscription.amount
					amount = numberOfUnpaidEvents * priceOfOneEvent
					maps[transaction_id] = {
							'product_name': subscription.product_name,
							'quantity': subscription.quantity,
							'amount': subscription.amount
					}
					totalAmount += amount
				else:
					noContent = True
			maps_json = json.dumps(maps)
			return render(request, 'userdetail/subscriptionCheckout.html', context={'maps': maps, 'totalPrice': totalAmount, 'maps_json': maps_json, 'alreadySubscribed': True, 'transaction': transaction, 'terms': terms, 'subs': True, 'user': user})
			
		else:
			amount = request.POST.get('amount', 0)
			subscription = Subscription_Order.objects.filter(transaction_id = transaction, isPaid=True).first()
			maps = {}
			maps[transaction] = {
					'product_name': subscription.product_name,
					'quantity': subscription.quantity,
					'amount': amount
					}
			totalAmount = amount
			maps_json = json.dumps(maps)
			return render(request, 'userdetail/subscriptionCheckout.html', context={'maps': maps, 'totalPrice': totalAmount, 'maps_json': maps_json, 'alreadySubscribed': True, 'transaction': transaction, 'terms': terms,  'subs': True, 'user': user})

from PayTm import Checksum
MERCHANT_KEY = 'ewNvWo7IsK3#qZSA'

import razorpay
client = razorpay.Client(
	auth=("rzp_live_ditQLxTKtYPFdI", "StJvU3tFjtD6Eg7Uhz2QxhW4"))
def subscriptionPayment(request):
	'''
		Checkout for customers
	'''
	if request.method == 'POST':
		print('***************************')
		items_json = request.POST.get('items_json', '')
		amount = float(request.POST.get('amount', 0))
		amount = round(amount, 2)

		name = request.POST.get('name')
		email = request.POST.get('email')
		address = request.POST.get('address')
		city = request.POST.get('city')
		state = request.POST.get('state')
		zip_code = request.POST.get('zip')
		phone = request.POST.get('phone')
		alreadySubscribed = request.POST.get('alreadySubscribed')
		subs = request.POST.get("subs")

		if 'RAZORBTN' in request.POST:

			context = {}
			order_currency = 'INR'
			order_receipt = 'order_rcptid_11'
			notes = {
			'Shipping address': 'Bommanahalli, Bangalore'}
			amount = max(1, round(amount))
			response = client.order.create(
				dict(
					amount=int(amount)*100,
					currency=order_currency,
					receipt=order_receipt,
					notes=notes,
					payment_capture='0'
					)
				)
			order_id = response['id']
			print('********************************')
			print('RAZORPAY')
			print(order_id)
			order_status = response['status']

			if order_status == 'created':
				context['product_id'] = product
				context['price'] = int(amount)
				context['name'] = name
				context['phone'] = phone
				context['email'] = email
				context['address'] = address
				context['city'] = city
				context['subs'] = subs
				context['items_json'] = items_json

				request.session['name'] = name
				request.session['phone'] = phone
				request.session['email'] = email
				request.session['address'] = address
				request.session['city'] = city
				
				context['order_id'] = order_id

				order = SubscriptionPayment(
					items_json = items_json,
					amount = amount,
					name = name,
					email = email,
					address = address,
					city = city,
					state = state,
					zip_code = zip_code,
					phone = phone
				)
				order.save()
				if alreadySubscribed:
					todays_date = datetime.date.today()
					transaction_id = request.POST.get('transaction')
					if transaction_id == 'payForAll':
						allSubscriptions = Subscription_Order.objects.filter(customer_email=request.user, isPaid=True)
						for subscription in allSubscriptions:
							t_id = subscription.transaction_id
							unpaidEvents = Event.objects.filter(sub_transaction_id=t_id, isPaidForEvent = False, start_time__lte = todays_date, isStopped = False)
							if len(unpaidEvents)!=0:
								print(subscription.product_name)
								unpaidEvents.update(isPaidForEvent=True)
					else:
						unpaidEvents = Event.objects.filter(sub_transaction_id=transaction_id, isPaidForEvent = False, start_time__lte = todays_date, isStopped = False)
						unpaidEvents.update(isPaidForEvent = True)
				else:
					# update all Subscription Orders:
					print('//////////checkout////////////////')
					subscriptions = Subscription_Order.objects.filter(customer_email=request.user, isPaid=False)
					for subscription in subscriptions:
						createEvents(subscription)
					subscriptions.update(isPaid=True)
				if request.user.is_authenticated:
					return render(request, 'checkout/confirm_order.html', context)
				else:
					context = {'cart': True}
					return render(request, 'userdetail/login.html', context)

		########### PAYTM ############
		''' NOT IN USE  '''
		host = "http://"+request.META['HTTP_HOST']+"/handlerequest/"
		param_dict = {
			'MID': 'LaxLMj03444256041341',
			'ORDER_ID': "subscription"+str(order.payment_id),
			'TXN_AMOUNT': str(amount),
			'CUST_ID': email,
			'INDUSTRY_TYPE_ID': 'Retail',
			'WEBSITE': 'WEBSTAGING',
			'CHANNEL_ID': 'WEB',
			'CALLBACK_URL': host,  # payment successfull msg by paytm
		}
		param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
			param_dict, MERCHANT_KEY)
		return render(request, 'checkout/paytm.html', {'param_dict': param_dict})


def updateSubscription(request):
	'''
		Update Subscription.
	'''
	import datetime

	transaction_id = request.POST.get('transaction_id')
	subscription_instance = Subscription_Order.objects.filter(transaction_id=transaction_id)
	quantity = request.POST.get('quantity')
	amount = request.POST.get('amount')
	start_date = request.POST.get('start_date')
	end_date = request.POST.get('end_date')
	interval = request.POST.get('interval')
	shift = request.POST.get('shift')
	remarks = request.POST.get('remark')
	stop_next = request.POST.get('stop_next')
	user = request.user

	print(
		transaction_id,
		quantity,
		start_date,
		end_date,
		interval,
		remarks,
		stop_next,
		sep='\n'
	)

	## seeing changes:
	if stop_next == 'c':
		next_stop = False # continue, NO stop
	else:
		next_stop = True # stop

	if subscription_instance[0].stop_next != next_stop:
		# Updating Subscription_Stop table:
		if next_stop == True:  # stop all the next:
			s = Subscription_Stop(
				user = user,
				transaction_id = transaction_id
			)
			s.save()
		else:   # user wants to continue:
			# extract the last record
			obj = Subscription_Stop.objects.filter(transaction_id = transaction_id, user=user, end_date = '9999-12-31')
			obj.update(end_date = datetime.datetime.today())
	
	# is start_date changed:
	isStartDateChanged = False
	isEndDateChanged = 0
	isIntervalChanged = False

	s_year, s_month, s_day = [int(x) for x in start_date.split('-')]
	e_year, e_month, e_day = [int(x) for x in end_date.split('-')]

	start_date = datetime.date(year = s_year, month=s_month, day=s_day)
	end_date = datetime.date(year=e_year, month=e_month, day=e_day)

	interval = int(interval)
	
	if start_date != subscription_instance[0].start_date:
		# This will be allowed if start_date > today_date:
		isStartDateChanged = True
	
	if end_date != subscription_instance[0].end_date:
		if end_date > subscription_instance[0].end_date:
			isEndDateChanged = 1
		else:
			isEndDateChanged = -1
	
	if interval != subscription_instance[0].interval:
		isIntervalChanged = True

	#Updating:
	subscription_instance.update(quantity=quantity)
	subscription_instance.update(amount=amount)
	subscription_instance.update(start_date=start_date)
	subscription_instance.update(end_date=end_date)
	subscription_instance.update(interval=interval)
	subscription_instance.update(remark=remarks)
	subscription_instance.update(stop_next=next_stop)
	subscription_instance.update(shifts=shift)
	# Updating Event table.
	updateEvent(subscription_instance, isStartDateChanged, isEndDateChanged, isIntervalChanged)

	return redirect('cart')

def deleteSubscription(request):
	transaction_id = request.POST.get('transaction_id')
	mode = request.POST.get('mode')
	user = request.user
	subscription_instance = Subscription_Order.objects.filter(transaction_id = transaction_id, isPaid = True)
	subscription_instance.delete()
	deleteEvent(transaction_id, user)
	if mode == 'AJAX':
		return JsonResponse({'amount': 1})
	return redirect('cart')

# def unit_quantity_filter(request):
# 	if request.user.is_authenticated:
# 		product_name=request.POST['product']
# 		pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
# 		if super_category.objects.filter(name=product_name,service=True):
# 			service_unit=service_add.objects.filter(supercategory_id=pro_id).all()
# 			is_service=True
# 		else:
# 			service_unit=units.objects.filter(supercategory_id=pro_id).all()
# 			is_service=False

# 		super_cat=super_category.objects.filter(available_for_subscription=True)
		
# 		frequency=order_frequency.objects.all()
# 		return render(request,'userdetail/subscription.html',{'super_cat':super_cat,'product_name':product_name,'is_service':is_service,
# 			'service_unit':service_unit,'order_frequency':frequency,'email':request.user.email})

# def subscription_vendor_filter(request):
# 	if request.user.is_authenticated:
# 		product_name=request.GET.get('product_name')
# 		unit_quantity=request.POST['unit_quantity']
# 		pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
# 		if super_category.objects.filter(name=product_name,service=True):
# 			seller_ids=service_add.objects.filter(supercategory_id=pro_id,price_range=unit_quantity).values('seller_id').all()
# 			is_service=True
# 			service_unit=service_add.objects.filter(supercategory_id=pro_id).all()
# 			seller_lt=[]
# 			for i in seller_ids:
# 				seller_lt.append(i['seller_id'])
# 			seller_name=[]
# 			for i in seller_lt:
# 				a=detail.objects.filter(id=i).values('email').all()
# 				for j in a:
# 					seller_name.append(j['email'])
# 		else:
# 			seller_ids=units.objects.filter(supercategory_id=pro_id,unit=unit_quantity).values('seller_id').all()
# 			seller_lt=[]
# 			is_service=False
# 			service_unit=units.objects.filter(supercategory_id=pro_id).all()
# 			for i in seller_ids:
# 				seller_lt.append(i['seller_id'])
# 			seller_name=[]
# 			for i in seller_lt:
# 				a=detail.objects.filter(id=i).values('email').all()
# 				for j in a:
# 					seller_name.append(j['email'])


# 		super_cat=super_category.objects.filter(available_for_subscription=True)
# 		frequency=order_frequency.objects.all()
		
# 		return render(request,'userdetail/subscription.html',{'super_cat':super_cat,'product_name':product_name,'is_service':is_service,
# 			'service_unit':service_unit,'unit_quantity':unit_quantity,'seller_name':seller_name,
# 			'order_frequency':frequency,'email':request.user.email})
# def final_subscription(request):
# 	if request.user.is_authenticated:
# 		product_name=request.GET.get('product_name')
# 		unit_quantity=request.GET.get('unit_quantity')
# 		vendor=request.POST['vendor']
# 		quantity=request.POST['quantity']
# 		order_frequency_name=request.POST.get('order_freq')
# 		times=request.POST.get('time_sch')
# 		dates=request.POST['schedule']
# 		remark=request.POST['remark']
# 		customer_id=request.POST['customer_id']
# 		pro_id=super_category.objects.filter(name=product_name).values('id')[0]['id']
# 		frequency_id=order_frequency.objects.filter(name=order_frequency_name).values('id')[0]['id']
# 		user_id=detail.objects.filter(email=email).values('id')[0]['id']
# 		date=d=datetime.datetime.now().strftime('%H:%M:%S')
# 		transaction_id=str(user_id)+str(pro_id)+str(''.join(list(date.split(':'))))
# 		a=subscriptionorder(transaction_id=transaction_id,name=product_name,product_id=pro_id,vendor=vendor,
# 			unit_of_quantity=unit_quantity,order_frequency_id=frequency_id,quantity=quantity,
# 			delivery_schedule=times,start_date=dates,remark=remark,customer_id=customer_id)
		
# 		a.save()
		# details=detail.objects.filter(email=request.user.email).first()
		# if details.staff:
		# 	return redirect('/userdetail/staff_profile')
		# elif details.vendor and details.seller_category.name=="Products Vendor":
		# 	return redirect('/userdetail/seller_profile')
		# elif details.vendor:
		# 	return redirect('/userdetail/vendor_profile')
		# elif details.buisness_Customer:
		# 	return redirect('/buisness/buisness_profile')

def pick_and_deliver(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			product=request.POST['product']
			other=request.POST['other']
			instruction=request.POST['instruction']
			pick_contact=request.POST['pick_contact_number']
			pick_person=request.POST['pick_person']
			pick_date=request.POST['date']
			pick_time=request.POST['time']
			pick_address=request.POST['pick_address']
			pick_landmark=request.POST['pick_landmark']
			delivery_contact=request.POST['delivery_contact_number']
			delivery_person=request.POST['delivery_contact_person']
			delivery_date=request.POST['delivery_date']
			delivery_time=request.POST['delivery_time']
			delivery_address=request.POST['delivery_address']
			delivery_landmark=request.POST['delivery_landmark']
			distance=request.POST['distance']
			moq=request.POST['moq']
			charge_paid=request.POST['charge_paid']
			other_charge=request.POST['other_charge']
			customer_id=request.POST['customer_id']
			if product=='Other':
				product=other
			if charge_paid=='Other':
				charge_paid=other_charge
			pro_id=super_category.objects.filter(name=product).values('id')[0]['id']
			
			user_id=detail.objects.filter(email=request.user.email).values('id')[0]['id']
			date=d=datetime.datetime.now().strftime('%H:%M:%S')
			transaction_id=str(user_id)+str(pro_id)+str(''.join(list(date.split(':'))))
			a=pick_and_deliver_order(transaction_id=transaction_id,product_name=product,packing_instruction=instruction
				,pickup_contact=pick_contact,pickup_person=pick_person,pickup_date=pick_date,
				pickup_time=pick_time,pickup_address=pick_address,pickup_landmark=pick_landmark,
				delivery_contact=delivery_contact,delivery_person=delivery_person,delivery_date=delivery_date,
				delivery_time=delivery_time,delivery_address=delivery_address,delivery_landmark=delivery_landmark,
				service_charge_paid_at=charge_paid,customer_id=customer_id)
			a.save()
			details=detail.objects.filter(email=request.user.email).first()
			if details.staff:
				return redirect('/userdetail/staff_profile')
			elif details.vendor and details.seller_category.name=="Products Vendor":
				return redirect('/userdetail/seller_profile')
			elif details.vendor:
				return redirect('/userdetail/vendor_profile')
			elif details.buisness_Customer:
				return redirect('/buisness/buisness_profile')
			else: 
				return HttpResponse('saved')
		
		else:
			super_cat=super_category.objects.filter(service=False)
			cus_address=customer_address.objects.filter(email=request.user.email).all()
			return render(request,'userdetail/pick_and_deliver.html',{'super_cat':super_cat,
				'email':request.user.email,'cus_address':cus_address})
	else:
		return redirect('login_page')
def project_add(request):
	if request.user.is_authenticated:
		email=request.user.email
		project_name=request.POST['pro_name']
		start_date=request.POST['start_date']
		end_date=request.POST['end_date']
		desc=request.POST['desc']
		project_url=request.POST['url']
		a=add_project(email=email,project_name=project_name,
			start_date=start_date,end_date=end_date,description=desc,project_url=project_url)
		a.save()
		return redirect('professional_profile')
def skill_add(request):
	if request.user.is_authenticated:
		skill=request.POST.get('skill')
		a=add_skill(email=request.user.email,name=skill)
		a.save()
		return redirect('professional_profile')
def certification_add(request):
	if request.user.is_authenticated:
		title=request.POST['title_certi']
		organization=request.POST['organization']
		issue_date=request.POST['issue_date']
		cer_id=request.POST['cer_id']
		a=add_certifications(email=request.user.email,title=title,
			organization=organization,issued_date=issue_date,issued_id=cer_id)
		a.save()
		return redirect('professional_profile')

def add_address(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			email=request.user.email
			lati = request.POST.dict()
			print(lati)
			pick_lat=lati.get("latitude")
			pick_lon=lati.get("longitude")
			address=request.POST.get("address")
			primary=request.POST.get("primary")
			if primary=="on":
				primary=True
			else:
				primary=False
			a=customer_address.objects.create(email=email,address=address,permanent=primary,pick_lat=pick_lat,pick_lon=pick_lon)
			return redirect('/')
		else:
			email=request.user.email
			cus_address=customer_address.objects.filter(email=email).all()
			return render(request,'userdetail/add_address.html',{'email':email,'cus_address':cus_address})



def customer_rating_form(request, order_no):
	if request.user.is_authenticated:
		email=request.user.email
		print(email)
		user = detail.objects.get(email=request.user.email)
		if request.POST.get('buyer_stars'):
			rating = rating_users()
			rating.stars = request.POST.get('buyer_stars')
			rating.review = request.POST.get('buyer_review')
			rating.user = detail.objects.get(user=request.user)
			rating.review_for_user = OrderItem.objects.get(id=order_no).customer
			rating.review_for = "buyer"
			rating.save()
			if user.customer:
				return redirect('/cartnew/my_orders')		
		return render(request,'userdetail/customer_rating.html')

def delivery_rating_form(request, order_no):
	if request.user.is_authenticated:
		email=request.user.email
		print(email)
		user = detail.objects.get(email=request.user.email)
		if request.POST.get('delivery_person_stars'):
			rating = rating_users()
			rating.stars = request.POST.get('delivery_person_stars')
			rating.review = request.POST.get('delivery_review')
			rating.user = detail.objects.get(email=request.user.email)
			rating.review_for_user = request.POST.get('delivery_review_for_user') # TODO: delivery detail
			rating.review_for = "delivery_person"
			rating.save()
			if user.customer:
				return redirect('/cartnew/my_orders')
		return render(request,'userdetail/delivery_rating.html')

def seller_rating_form(request, order_no):
	if request.user.is_authenticated:
		email=request.user.email
		print(email)
		user = detail.objects.get(email=request.user.email)
		if request.POST.get('vendor_stars'):
			rating = rating_users()
			rating.stars = request.POST.get('vendor_stars')
			rating.review = request.POST.get('vendor_review')
			rating.user = user
			rating.review_for_user = OrderItem.objects.get(id=order_no).product.seller
			rating.review_for = "vendor"
			rating.save()
			if user.customer:
				return redirect('/cartnew/my_orders')
		return render(request,'userdetail/seller_rating.html')

def product_rating_form(request, order_no):
	if request.user.is_authenticated:
		email=request.user.email
		print(email)
		user = detail.objects.get(email=request.user.email)
		if request.POST.get('product_stars'):
			rating = rating_users()
			rating.stars = request.POST.get('product_stars')
			rating.review = request.POST.get('product_review')
			rating.user = user
			rating.review_for_user = OrderItem.objects.get(id=order_no).product
			rating.review_for = "product"
			rating.save()
			if user.customer:
				return redirect('/cartnew/my_orders')
		return render(request,'userdetail/product_rating.html')


def logistic_runner_register(request):
	obj=staff_Categories.objects.all()
	vendor_data = detail.objects.filter(vendor=True)
	data={
	"exist":False,
	"obj":obj, 
	'vendor_data': vendor_data, #
	}
	if request.POST:
		name=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		contact=request.POST.get('contact')
		gender=request.POST.get('gender')
		category=request.POST.get('category')
		category=staff_Categories.objects.filter(name=category).first()
		position=request.POST.get('position')
		vendor = request.POST.get('vendor')
		user=User.objects.filter(email=email)
		if user.count()>0:
			data={
			"exist":True
			}
		else:
			user=User.objects.create_user(
				email=email,
				username=email,
				password=password)
			user1=detail(
				name=name,
				email=email,
				password=password,
				contact=contact,
				gender=gender,
				customer=False,
				vendor=False,
				buisness_Customer=False,
				staff=True,
				staff_category=category,
				position=position,
				vendor_name=vendor,
				runner=True
			)
			user1.save()
			# runner_profile = logistic_runner()
			# runner_profile.user = user1
			# runnser_profile.save()
			objs=detail.objects.filter(
				staff=True,
				position='H',
				staff_category=category
				)
			objs1=detail.objects.filter(
				staff=True,
				position='M',
				staff_category=category
				)
			for i in objs:
				oj=notifications(title="New Staff Registered Activate it !",
					description="A New Staff is Registered please verify it and Activate its Account",
					link="/userdetail/staff_profile/"+str(email),
					user=i)
				oj.save()
				oj.link=oj.link+"?noti="+str(oj.id)
				oj.save()
			for i in objs1:
				oj=notifications(title="New Staff Registered Activate it !",
					description="A New Staff is Registered please verify it and Activate its Account",
					link="/userdetail/staff_profile/"+str(email),
					user=i)
				oj.save()
				oj.link=oj.link+"?noti="+str(oj.id)
				oj.save()
			return redirect('/userdetail/login')
	return render(request,"userdetail/logistic_runner_register.html",data)

def add_distribution_center(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			# lati = request.POST.dict()
			# print(lati)
			center = distribution_center()
			center.name = request.POST.get("name")
			center.pickup_frequency = request.POST.get("frequency")
			center.state=request.POST.get("state")
			center.city=request.POST.get("city")
			center.address=request.POST.get("address")
			center.coordinates=request.POST.get("coordinates")
			center.city_tire=request.POST.get("city_tire")
			if center.pickup_frequency == 1:
					delay_time = 24
			elif center.pickup_frequency == 2:
				delay_time = 12
			elif center.pickup_frequency == 3:
				delay_time = 8
			elif center.pickup_frequency == 4:
				delay_time = 6
			center.delay_time = delay_time
			center.save()
			print(center.state, center.city, center.address, center.coordinates, center.city_tire)
			return render(request,"userdetail/add_distribution_center.html")
	return render(request,"userdetail/add_distribution_center.html")
