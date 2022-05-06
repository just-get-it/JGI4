







from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from userdetail.models import detail
from userdetail.models import seller_Categories
from b2b.models import acti, size_assortment_1
from .models import company_detail,company_Order,quantity_b2b,assortment,address_model,color_model
# from .models import brand as bran
# Create your views here.
import csv
import datetime
from django.contrib.auth import get_user_model
from movintrendz.settings import BASE_DIR
import os
from userdetail.models import detail,staff_Categories
import json
from django.http import HttpResponse, JsonResponse

from seller_info.models import labels,fits,seasons

from product.models import trims_product,trims_Category,product_cate_b2b, labels_Attributes, trims_label_attributes, StyleType, WashType, Fabric, garment_matching_parameters, garment_matching_requirements
from POM.models import POM,measurement

from product.models import sub_category,super_category
from product.models import category as cat

from b2b.models import notifications,activities,activities_Category

from .models import activities
from b2b.models import consumer_Order_Quantity

from .models import coloums,excel
from userdetail.utils import check_email_correctness,send_email
# import library
import math, random
from movintrendz.settings import EMAIL_HOST_USER

from b2b.models import packing_list,cartons_list,distribution_list
from b2b.models import carton as ca

from b2b.models import company_Order,company_detail,bom
from userdetail.utils import render_to_pdf,num2word
import datetime

import random
import string

from POM.models import measurement_chart, size_assortment_pattern, size_labels
from permission.models import section,orders_permission


def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
# function to generate OTP
def generateOTP() :

    # Declare a string variable
    # which stores all string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]

    return OTP








User=get_user_model()
def buisness_index(request):
    if request.user.is_authenticated:
        user=detail.objects.filter(email=request.user.email)
        if user.count()>0:
            if user.first().activate_Buisness:
                return redirect('/buisness/buisness_timeline')
            elif user.first().buisness_Customer:
                return redirect('/buisness/activate')
            else:
                return redirect('/userdetail/buisness_registration')
    return render(request,'b2b/buisness_index.html',{})



def buisness_timeline(request):
    if request.user.is_authenticated:
        user=detail.objects.filter(email=request.user.email)
        if user.count()>0:
            if user.first().buisness_Customer:
                user=user.first()
                oyu=company_detail.objects.filter(email=request.user.email).first()
                if request.POST:
                    name=request.POST.get('name')
                    desc=request.POST.get('desc')
                    mission=request.POST.get('mission')
                    gstin=request.POST.get('gstin')
                    file=None
                    if request.FILES:
                        file=request.FILES.get('logo')
                    if oyu:
                        obj=oyu
                    else:
                        obj=company_detail()
                    # obj=company_detail(
                    # 		name=name,
                    # 		email=request.user.email,
                    # 		company_Description=desc,
                    # 		company_Mission=mission,
                    # 		gstin=gstin,
                    # 		logo=file
                    # 	)
                    obj.name=name
                    obj.email=request.user.email
                    obj.company_Description=desc
                    obj.company_Mission=mission
                    obj.gstin=gstin
                    if file:
                        obj.logo=file
                    obj.save()
                    # user=user.first()
                    user.address=request.POST.get('address')
                    user.info_update=True
                    user.save()
                    return redirect('/buisness/buisness_profile')
                # if user.first().info_update:
                # 	return redirect('/buisness/buisness_profile')
                return render(request,'b2b/buisness_timeline.html',{'buis':oyu,'user':user})
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/buisness_registration')




def activate(request):
    if request.user.is_authenticated:
        user=detail.objects.filter(email=request.user.email)
        if user.count()>0:
            user=user.first()
            if not(user.activate_Buisness):
                return render(request,'b2b/activate.html',{})
            else:
                return redirect('/buisness/buisness_profile')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/buisness_registration')




def buisness_profile(request):
    data={}
    if request.user.is_authenticated:
        us=detail.objects.filter(email=request.user.email).first()
        user=company_detail.objects.filter(email=request.user.email)
        orders=company_Order.objects.filter(user_email=request.user.email,order_type='O')
        sample=company_Order.objects.filter(user_email=request.user.email,order_type='S')
        design=company_Order.objects.filter(user_email=request.user.email,order_type='D')
        enquiry=company_Order.objects.filter(user_email=request.user.email,order_type='E')
        act=activities.objects.filter(user=us)
        # print(orders)
        if user.count()>0:
            user=user.first()
            data={
                "name":user.name,
                "desc":user.company_Description,
                "mission":user.company_Mission,
                "gstin":user.gstin,
                "logo2":user.logo,
                "email":user.email,
                "order_bool":False,
                "orders":orders[:5],
                "sample":sample,
                "enquiry":enquiry,
                "design":design,
                "sample_bool":False,
                "enquiry_bool":False,
                "design_bool":False,
                "act":act,
                "us":us
            }
            if orders.count()>0:
                data["order_bool"]=True
            if sample.count()>0:
                data["sample_bool"]=True
            if enquiry.count()>0:
                data["enquiry_bool"]=True
            if design.count()>0:
                data["design_bool"]=True

            if request.POST.get('industry_ajax'):
                industry=request.POST.get('industry_ajax')
                us.industry=industry
                us.save()

        else:
            return redirect('/userdetail/login')
    else:
        return redirect('/userdetail/login')
    return render(request,'b2b/buisness_profile.html',data)





def buisness_order_list(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            enquiry=company_Order.objects.filter(user_email=details.email,order_type='E')
            design=company_Order.objects.filter(user_email=details.email,order_type='D')
            sample=company_Order.objects.filter(user_email=details.email,order_type='S')
            orders=company_Order.objects.filter(user_email=details.email,order_type='O')
            data={
                "orders":orders,
                "enquiry":enquiry,
                "design":design,
                "sample":sample
            }
            return render(request,"b2b/buisness_order_list.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')





def activities_upload(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            staffs=staff_Categories.objects.all()
            sellers=seller_Categories.objects.all()
            data={
            "staffs":staffs,
            "sellers":sellers,
            "stf_error":False,
            "sel_error":False,
            "acti_error":False
            }
            if request.FILES.get('csv_file'):
                file=request.FILES.get('csv_file')
                obj=acti(acti_file=file)
                obj.save()
                data_read=csv.reader(open(BASE_DIR+obj.acti_file.url[6:],"r"), delimiter=',', quotechar='"')
                all=activities_Category.objects.all()
                for i in all:
                    i.delete()
                for row in data_read:
                    # if row[0]=='Sequence':
                    # 	continue
                    # stf=staff_Categories.objects.filter(name=row[3])
                    # if stf.count()==0:
                    # 	data["stf_error"]=True
                    # 	return render(request,'b2b/activities_upload.html',data)
                    # sel=seller_Categories.objects.filter(name=row[4])
                    # if sel.count()==0:
                    # 	data["sel_error"]=True
                    # 	return render(request,'b2b/activities_upload.html',data)
                    # acti_link=activities_Category.objects.filter(sequence=row[11])
                    # if acti_link.count()==0:
                    # 	data["acti_error"]=True
                    # 	return render(request,'b2b/activities_upload.html',data)
                    # print(row[3],stf)
                    # ohg=activities_Category(
                    # 		sequence=row[0],
                    # 		title=row[1],
                    # 		description=row[2],
                    # 		staff_category=stf.first(),
                    # 		seller_category=sel.first(),
                    # 		position=row[5],
                    # 		completed_in=int(row[6]),
                    # 		before_Time_Color=row[7],
                    # 		late_Time_Color=row[8],
                    # 		on_Time_Color=row[9],
                    # 		type_of_order=row[10],
                    # 		linked_activity=acti_link.first(),
                    # 		Increment_or_Decrement=int(row[12])
                    # 	)
                    # ohg.save()
                    # sequence=int(row[0])
                    # title=row[1]
                    # description=row[2]
                    # staf_cate=staff_Categories.objects.filter(name=row[3]).first()
                    # sel_cate=seller_Categories.objects.filter(name=row[4]).first()
                    # completed_in=0
                    # type_of_order=row[5]
                    # if row[6]:
                    # 	linked_activity=activities_Category.objects.filter(sequence=int(row[6])).first()
                    # else:
                    # 	linked_activity=None
                    # Increment_or_Decrement=int(row[7])

                    # lead_Time_for_120_Days=int(row[8])
                    # lead_Time_for_105_Days=int(row[9])
                    # lead_Time_for_90_Days=int(row[10])
                    # lead_Time_for_75_Days=int(row[11])
                    # lead_Time_for_60_Days=int(row[12])
                    # lead_Time_for_45_Days=int(row[13])
                    # lead_Time_for_30_Days=int(row[14])
                    # lead_Time_for_15_Days=int(row[15])
                    # lead_Time_for_7_Days=int(row[16])
                    # lead_Time_for_3_Days=int(row[17])
                    # escalation_Time_for_Executive=int(row[18])
                    # escalation_Time_for_Manager=int(row[19])
                    # escalation_Time_for_Head=int(row[20])
                    # """ohg=activities_Category(
                    # 		sequence=int(row[0]),
                    # 		title=row[1],
                    # 		description=row[2],
                    # 		staff_category=staff_Categories.objects.filter(name=row[3]).first(),
                    # 		seller_category=seller_Categories.objects.filter(name=row[4]).first(),
                    # 		completed_in=0,
                    # 		type_of_order=row[5],
                    # 		linked_activity=linked_activity,
                    # 		Increment_or_Decrement=int(row[7]),
                    # 		lead_Time_for_120_Days=int(row[8]),
                    # 		lead_Time_for_105_Days=int(row[9]),
                    # 		lead_Time_for_90_Days=int(row[10]),
                    # 		lead_Time_for_75_Days=int(row[11]),
                    # 		lead_Time_for_60_Days=int(row[12]),
                    # 		lead_Time_for_45_Days=int(row[13]),
                    # 		lead_Time_for_30_Days=int(row[14]),
                    # 		lead_Time_for_15_Days=int(row[15]),
                    # 		lead_Time_for_7_Days=int(row[16]),
                    # 		lead_Time_for_3_Days=int(row[17]),
                    # 		escalation_Time_for_Executive=int(row[18]),
                    # 		escalation_Time_for_Manager=int(row[19]),
                    # 		escalation_Time_for_Head=int(row[20]),
                    # 		position='H'
                    # #	)
                    # #ohg.save()
                    # ohg=activities_Category(
                    # 		sequence=int(row[0]),
                    # 		title=row[1],
                    # 		description=row[2],
                    # 		staff_category=staff_Categories.objects.filter(name=row[3]).first(),
                    # 		seller_category=seller_Categories.objects.filter(name=row[4]).first(),
                    # 		completed_in=0,
                    # 		type_of_order=row[5],
                    # 		linked_activity=linked_activity,
                    # 		Increment_or_Decrement=int(row[7]),
                    # 		lead_Time_for_120_Days=int(row[8]),
                    # 		lead_Time_for_105_Days=int(row[9]),
                    # 		lead_Time_for_90_Days=int(row[10]),
                    # 		lead_Time_for_75_Days=int(row[11]),
                    # 		lead_Time_for_60_Days=int(row[12]),
                    # 		lead_Time_for_45_Days=int(row[13]),
                    # 		lead_Time_for_30_Days=int(row[14]),
                    # 		lead_Time_for_15_Days=int(row[15]),
                    # 		lead_Time_for_7_Days=int(row[16]),
                    # 		lead_Time_for_3_Days=int(row[17]),
                    # 		escalation_Time_for_Executive=int(row[18]),
                    # 		escalation_Time_for_Manager=int(row[19]),
                    # 		escalation_Time_for_Head=int(row[20]),
                    # 		position='M'
                    # 	)
                    #                     ohg.save()"""
                    sequence=int(row[0])
                    staff_category=staff_Categories.objects.filter(name=row[24]).first()
                    seller_category=seller_Categories.objects.filter(name=row[24]).first()
                    if int(row[3])>sequence:
                        linked_acti=None
                    else:
                        linked_acti=activities_Category.objects.filter(sequence=int(row[3])).first()
                    ohg=activities_Category(
                            sequence=int(row[0]),
                            title=row[1],
                            description=row[23],
                            staff_category=staff_category,
                            seller_category=seller_category,
                            completed_in=0,
                            type_of_order=row[2],
                            linked_activity=linked_acti,
                            Increment_or_Decrement=int(row[4]),
                            lead_Time_for_120_Days=int(row[5]),
                            lead_Time_for_105_Days=int(row[6]),
                            lead_Time_for_90_Days=int(row[7]),
                            lead_Time_for_75_Days=int(row[8]),
                            lead_Time_for_60_Days=int(row[9]),
                            lead_Time_for_45_Days=int(row[10]),
                            lead_Time_for_30_Days=int(row[11]),
                            lead_Time_for_15_Days=int(row[12]),
                            lead_Time_for_7_Days=int(row[13]),
                            lead_Time_for_3_Days=int(row[14]),
                            escalation_Time_for_Executive=int(row[15]),
                            escalation_Time_for_Manager=int(row[16]),
                            escalation_Time_for_Head=int(row[17]),
                            position='C'
                        )
                    ohg.save()


                return redirect('/userdetail/staff_profile')
            return render(request,'b2b/activities_upload.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')




def placeorder(request, order_no=None):
    sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
    brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
    cate=cat.objects.all()
    sector = product_cate_b2b.objects.all()
    style_type = StyleType.objects.all()
    wash_type = WashType.objects.all()
    fabric_type = Fabric.objects.all()
    sizes = size_labels.objects.all()

    orders=company_Order.objects.filter(order_no=order_no)
    user = company_detail.objects.filter(email=request.user.email)
    user = user.first()
    if not user:
        user=detail.objects.get(email=request.user.email)
    if request.user.is_authenticated:
        if not orders:
            fabric_code = trims_product.objects.all()
            order=auto_generate_order_no(user.email,fabric_code)
        else:
            orders=orders.first()
            order = {"order_no": orders.order_no, "user_email": orders.user_email, "fabrics": orders.fabrics,"fabric_flag":True}

    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer or details.vendor or details.staff:
            if request.POST and request.FILES:
                order_no = int(request.POST.get('Order_No'))
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

                fabric_id = request.POST.get('fabric_code')
                fabric_id = int(fabric_id[12::])
                fabrics = trims_product.objects.filter(id=fabric_id).first()
                #print(fabrics)
                sector_id=request.POST.get('sector')
                #print(sector_id)
                sec=product_cate_b2b.objects.filter(id=sector_id).first()
                design_code=request.POST.get('design_code')
                garment_code=request.POST.get('garment_code')
                style_code=request.POST.get('style_code')
                style_description=request.POST.get('style_desc')
                garment_matching=''
                if request.POST.get('garment_matching_parameters'):
                    garment_matching=garment_matching_parameters.objects.filter(id=int(request.POST.get('garment_matching_parameters'))).first().name
                    garment_matching=garment_matching+', '+request.POST.get('garment_matching_level')


                quantity=request.POST.get('quantity')
                dispatch=request.POST.getlist('dispatch')
                billing=request.POST.getlist('billing')
                bill=""
                for b in billing:
                    bill+=b+", "

                sample=request.FILES.get('sample')
                excel=request.FILES.get('excel')


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
                max_quantity=request.POST.get('max_quantity')
                if max_quantity:
                    max_quantity=int(max_quantity)
                else:
                    max_quantity=1000
                if not(target_lead_time):
                    target_lead_time=0
                if not(target_price):
                    target_price=0
                otp=generateOTP()
                order=company_Order(
                        sector=sec,
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
                        billing_Address=bill,
                        order_no=order_no,
                        user_email=request.user.email,
                        order_type='O',
                        target_lead_time=int(target_lead_time),
                        target_price=int(target_price),
                        tech_pack=tech_pack,
                        specs=specs,
                        logo_placement=logo_place,
                        description=description,
                        sizes=sizes,
                        max_quantity_per_consumer=max_quantity,
                        order_password=otp,
                        fabrics=fabrics,
                        fabric_consump=request.POST.get('average_fabric_comsumption'),
                        design_code=design_code,
                        garment_code=garment_code,
                        style_code=style_code,
                        fabric_code=request.POST.get('fabric_code_name'),
                        style_description=style_description,
                        accepted_rate=request.POST.get('accepted_rate'),
                        rejection_rate=request.POST.get('rejection_rate'),
                        stock=request.POST.get('stock'),
                        wastage=request.POST.get('wastage'),
                        lead_time=request.POST.get('lead_time'),
                        tentative_cost=request.POST.get('tentative_cost'),
                        fabric_type=Fabric.objects.filter(name=request.POST.get('fabric_type')).first(),
                        style_type=StyleType.objects.filter(name=request.POST.get('style_type')).first(),
                        wash_type=WashType.objects.filter(name=request.POST.get('wash_type')).first(),
                        garment_matching_parameter_and_level=garment_matching,
                        repeat_size= request.POST.get('repeat_size'),
                        label_atrribute=request.POST.getlist('label_atrribute'),
                        #trims_atrribute=request.POST.getlist('trims_atrribute'),
                        poms_fields=request.POST.getlist('poms')
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

                for d in dispatch:
                    ofd=address_model(
                        address=d,
                        title="Location1"
                    )
                    ofd.save()
                    order.dispatch_Address.add(ofd)
                    order.save()

                # allorder = company_Order.objects.all().order_by('-order_no')[1]
                # if allorder:
                #     order_n = allorder.order_no + 1
                #     order_n=str(order_n)
                #     order_n=order_n[-5:]
                #     x = str(datetime.datetime.now().year)
                #     y = str(datetime.datetime.now().month)
                #     z = str(datetime.datetime.now().day)
                #     order_n=int(x+y+order_n)
                # else:
                #     x = str(datetime.datetime.now().year)
                #     order_n = int(x + "000001")
                # order.order_no=order_n
                # order.save()

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
                        title="New Order Placed Please Add Manager to it("+str(order.order_no)+") !",
                        description="Add manager to it",
                        user=i,
                        link="/userdetail/staff_profile/orders/"+str(order.order_no),
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
                    col_objs=coloums.objects.filter(user=details)
                    for i in col_objs:
                        if i.email:
                            email_col=i.coloumn_no
                        if i.contact:
                            contact_col=i.coloumn_no
                        if i.gender:
                            gender_col=i.coloumn_no
                        if i.dept:
                            dept_col=i.coloumn_no
                        if i.sub_dept:
                            sub_dept_col=i.coloumn_no
                        if i.reg_no:
                            reg_no_col=i.coloumn_no
                        if i.name:
                            name_col=i.coloumn_no
                    for row in data_read:
                        if count==0:
                            count+=1
                            continue
                        # try:
                        reg_no=row[reg_no_col-1]
                        name=row[name_col-1]
                        dept=row[dept_col-1]
                        sub_dept=row[sub_dept_col-1]
                        email=row[email_col-1]
                        contact=row[contact_col-1]
                        gender=row[gender_col-1]
                        password=randomString(10)
                        col_objs=coloums.objects.filter(user=details,email=False,contact=False,gender=False,dept=False,sub_dept=False,reg_no=False,name=False)
                        attributes=[]
                        for jk in col_objs:
                            attributes.append(row[jk.coloumn_no-1])
                        length=len(attributes)
                        if length==0:
                            attributes=[None,None,None]
                        elif length==1:
                            attributes.append(None)
                            attributes.append(None)
                        elif length==2:
                            attributes.append(None)
                        count=count+1
                        user_obj=User.objects.filter(username=email)
                        if user_obj.count()>0:
                            detail_obj=detail.objects.filter(email=email)
                            if detail_obj.count()>0:
                                obj=consumer_Order_Quantity(user=detail_obj.first(),order=order,max_quantity=max_quantity)
                                obj.save()
                            else:
                                obj=detail(
                                    name=name,
                                    email=email,
                                    password=password,
                                    contact=contact,
                                    b2b_order=True,
                                    b2b_order_no=order_n,
                                    customer=True,
                                    vendor=False,
                                    buisness_Customer=False,
                                    activate_Seller=False,
                                    activate_Buisness=False,
                                    buisness_Timeline=False,
                                    vendor_Timeline=False,
                                    max_quantity=max_quantity,
                                    dept=dept,
                                    sub_dept=sub_dept,
                                    reg_no=reg_no,
                                    gender=gender,
                                    excel_attribute1=attributes[0],
                                    excel_attribute2=attributes[1],
                                    excel_attribute3=attributes[2]
                                )
                                obj.save()
                                oiu=consumer_Order_Quantity(user=obj,order=order,max_quantity=max_quantity)
                                oiu.save()
                        else:
                            obj=User.objects.create_user(username=email,email=email,password=password)
                            obj.save()
                            # print("User Saved")
                            # max_quantity=1
                            detail_obj=detail.objects.filter(email=email)
                            if detail_obj.count()>0:
                                obj=consumer_Order_Quantity(user=detail_obj,order=order,max_quantity=max_quantity)
                                obj.save()
                            else:
                                obj=detail(
                                    name=name,
                                    email=email,
                                    password=password,
                                    contact=contact,
                                    b2b_order=True,
                                    b2b_order_no=order_n,
                                    customer=True,
                                    vendor=False,
                                    buisness_Customer=False,
                                    activate_Seller=False,
                                    activate_Buisness=False,
                                    buisness_Timeline=False,
                                    vendor_Timeline=False,
                                    max_quantity=max_quantity,
                                    dept=dept,
                                    sub_dept=sub_dept,
                                    reg_no=reg_no,
                                    gender=gender,
                                    excel_attribute1=attributes[0],
                                    excel_attribute2=attributes[1],
                                    excel_attribute3=attributes[2]
                                )
                                obj.save()
                                oiu=consumer_Order_Quantity(user=obj,order=order,max_quantity=max_quantity)
                                oiu.save()

                if request.POST.getlist('size_assort'):
                    size_assort =request.POST.getlist('size_assort')
                    address =request.POST.getlist('size_address')
                    color =request.POST.getlist('size_color')
                    quantity =request.POST.getlist('size_quantity')
                    j=0
                    size_order=company_Order.objects.filter(order_no=order_n).first()
                    print(size_order)
                    for (i, m, n, q) in zip(size_assort, address, color, quantity):
                        i=int(i)
                        address = address_model.objects.filter(address=m).first()
                        quantity=int(q)
                        color = color_model.objects.filter(name=n).first()
                        print(i, m, n, quantity, address, color, j)
                        objs_size_assort = quantity_b2b.objects.filter(order=size_order,size_label=i,color=color,address=address, production=False, is_csv=False)
                        if(j==0):
                            final = 1
                            size_ass_obj = size_assortment_1.objects.filter(order=size_order).order_by("-assortment_no")
                            objs_size_assort = quantity_b2b(
                                order=size_order,
                                size_label=i,
                                address=address,
                                color=color,
                                quantity=quantity,
                                production=False,
                                is_csv=False)
                            objs_size_assort.save()
                            if (size_ass_obj.first()):
                                final = size_ass_obj.first().assortment_no + 1
                            d = size_assortment_1(order=size_order, assortment_no=final, is_csv=False)
                            d.save()
                            d.sizes.add(objs_size_assort)
                            d.save()
                        else:
                            no = final
                            size_ass_obj = size_assortment_1.objects.filter(order=size_order, assortment_no=no).first()
                            if (size_ass_obj):
                                a = size_ass_obj.sizes.filter(size_label=i, color=color, address=address,
                                                              production=False, is_csv=False)
                                if a.first():
                                    u = a.first()
                                    u.quantity += quantity
                                    u.save()
                                    print(u.quantity)
                                else:
                                    objs_size_assort = quantity_b2b(
                                        order=size_order,
                                        size_label=i,
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
                        j+=1

                return redirect('/buisness/buisness_profile')
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
            # brands=detail.objects.filter(vendor=True,seller_Category="Products Vendor")
            # if details.vendor and details.seller_Category.name=="Products Vendor":
            #     brands=[details]
            data = {
                    "brand": brands, "cate": cate,
                    "sector": sector, "order": order,
                    "style_type": style_type, "wash_type": wash_type,
                    "depend": None, "fabric_type": fabric_type,
                    "sizes":sizes
                }
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

from product.models import  repeat_size as repeat
@csrf_exempt
def calculate_total_fabric_consumption(request):
    poms=request.POST.getlist('poms_radio[]')
    components=request.POST.getlist('components[]')
    trims=request.POST.get('trims_data')
    size_pattern_manual_assortment = request.POST.getlist('size_pattern_manual_assortment[]')
    sizes=request.POST.getlist('manual_sizes[]')
    manual_size_quantity=request.POST.getlist('manual_size_quantity[]')
    colors=set(request.POST.getlist('colors[]'))
    repeat_size=request.POST.get('repeat_size')
    #print(size_pattern_manual_assortment)
    total = 0

    '''
    if size_quantity_manual:
        size_quantity_optimum = [round(s/min(size_quantity_manual), 1) for s in size_quantity_manual]
        print(size_quantity_optimum)
        aval_size_assortments=size_assortment_pattern.objects.all()
        for x in aval_size_assortments:
            ratio_list=[float(y) for y in x.ratio.split(', ')]
            print(ratio_list)
            differ_list = []
            for i, j in zip(size_quantity_optimum, ratio_list):
                differ_list.append(round(i-j))
                #print(differ_list)
            if str(all(d>0 and d<2 for d in differ_list)):
                total+=float(x.fabric_consumption)
                print(differ_list, x.fabric_consumption,total)
                break
    '''

    if size_pattern_manual_assortment:
        aval_size_assortments = size_assortment_pattern.objects.all()
        fabrc_consumption=0
        for c in colors:
            size_quantity_dct={}
            size_quantity=[]
            for s in size_pattern_manual_assortment:
                if c==s.split(', ')[0]:
                    size_quantity.append(float(s.split(', ')[2]))

            for s in size_pattern_manual_assortment:
                if c==s.split(', ')[0]:
                    size_quantity_dct[int(s.split(', ')[1])]=round(float(s.split(', ')[2])/max(size_quantity), 1)
            size_keys=sorted(size_quantity_dct.keys())

            print(size_quantity_dct)
            for_flag=False
            for a in aval_size_assortments:
                aval_size_dct = {}
                if for_flag:
                    break
                else:
                    a_size = a.size.all()
                    a_ratio = a.ratio.split(', ')
                    #print(a_ratio, a_size)
                    for q, r in zip(a_size, a_ratio):
                        aval_size_dct[int(q.name)] = float(r)
                    #print(aval_size_dct)
                    mid = len(size_keys) // 2
                    flag = 1
                    while True:
                        try:
                            if size_quantity_dct[size_keys[mid]] == aval_size_dct[size_keys[mid]]:
                                if flag % 2 == 0:
                                    mid = mid - flag
                                else:
                                    mid = mid + flag

                                if flag == len(size_keys) - 1:
                                    fabrc_consumption = float(a.fabric_consumption)
                                    print(fabrc_consumption)
                                    total += fabrc_consumption
                                    for_flag = True
                                    print('flag has riched the size of sizes')
                                    break

                                if flag == 3:
                                    fabrc_consumption = float(a.fabric_consumption)
                                    print(fabrc_consumption)
                                    total += fabrc_consumption
                                    for_flag = True
                                    break

                                print('in if loop of while')
                            else:
                                if flag - 1 == 2:
                                    fabrc_consumption = float(a.fabric_consumption)
                                    print(fabrc_consumption)
                                    total += fabrc_consumption
                                    for_flag = True
                                    break
                                #print('else from while loop', flag)

                                break
                            flag += 1
                        except:
                            if flag == len(size_keys):
                                print('None sizes are matched ')
                                break

                            if flag % 2 == 0:
                                mid = mid - flag
                            else:
                                mid = mid + flag
                            flag += 1

    #print(total)
    if request.POST.get('garment_matching_id'):
        garment_matching_id = int(request.POST.get('garment_matching_id'))
        garment_matching_level = request.POST.get('garment_matching_level')
        garment_matching = garment_matching_requirements.objects.filter(id=garment_matching_id).first()
        print(garment_matching)
        if garment_matching:
            if garment_matching_level=='level1':
                total+=garment_matching.fabric_consumption_level1
            elif garment_matching_level=='level2':
                total += garment_matching.fabric_consumption_level2
            elif garment_matching_level=='level3':
                total += garment_matching.fabric_consumption_level3
            elif garment_matching_level=='no matching':
                total += 0
    
    if trims:
        fabric_id=int(trims[12::])
        trims_label=trims_product.objects.filter(id=fabric_id).first().trims_labels
        for t in trims_label:
            if t.split(', ')[2]:
                total+=int(t.split(', ')[2])
        
        fabric_direction_cons = trims_product.objects.filter(id=fabric_id).first().fabric_direction.impact_fabric_consumption
        fabric_width_cons = trims_product.objects.filter(id=fabric_id).first().fabric_width.impact_fabric_consumption
        fabric_print_type_cons = trims_product.objects.filter(id=fabric_id).first().fabric_print_type.impact_fabric_consumption
        fabric_print_design_cons = trims_product.objects.filter(id=fabric_id).first().fabric_print_design.impact_fabric_consumption
        total = total+fabric_direction_cons+fabric_print_design_cons+fabric_width_cons+fabric_print_type_cons
        
        if repeat_size:
            rep=repeat_size.split(', ')
            print(rep)
            rep_val= repeat.objects.filter(fabric_direction__name__exact=trims_product.objects.filter(id=fabric_id).first().fabric_direction.name,
                                          fabric_width__name__exact=trims_product.objects.filter(id=fabric_id).first().fabric_width.name,
                                          fabric_print_type__name__exact=trims_product.objects.filter(id=fabric_id).first().fabric_print_type.name,
                                          fabric_print_design__name__exact=trims_product.objects.filter(id=fabric_id).first().fabric_print_design.name,
                                          garment_matching_parameters__id__exact=request.POST.get('garment_matching_id'),
                                          garment_matching_level = request.POST.get('garment_matching_level')).first()
            # print(rep_val)
            if rep_val is not None:
                hor_repeat_range=rep_val.horizontal_repeat_range.split('\n')
                ver_repeat_range=rep_val.vertical_repeat_range.split('\n')
                inc_cons=rep_val.increase_in_marker_cons.split('\n')

                for (i, j, k) in zip(hor_repeat_range, ver_repeat_range, inc_cons):
                    hor=i.split('-')
                    ver=j.split('-')
                    if float(rep[0]) >= float(hor[0]) and float(rep[0]) <= float(hor[1]) and float(rep[1]) >= float(ver[0]) and float(rep[1]) <= float(ver[1]):
                        if request.POST.get('table_fabric_consumption') != '0':
                            total+= float(request.POST.get('table_fabric_consumption'))+((float(k)/100)*float(request.POST.get('table_fabric_consumption')))
                            # print(total, k)
                            # print(request.POST.get('table_fabric_consumption'))
                            break

            else:
                total += float(request.POST.get('table_fabric_consumption'))
                # repeat_range = rep_val.repeat_range.split(', ')
                # repeat_range_cons = rep_val.repeat_range_consumtion.split(', ')
                # # print(repeat_range, repeat_range_cons)
                # for (i, j) in zip(repeat_range, repeat_range_cons):
                #     r=i.split('-')
                #     # print(r)
                #     if float(rep[0])>= float(r[0]) and float(rep[0])<= float(r[1]) and float(rep[1])>= float(r[0]) and float(rep[1])<= float(r[1]):
                #         total+=rep_val.consumption_length_basic_block+((float(j)/100)*rep_val.consumption_length_basic_block)
                #         # print(i, j)
                #         break

    for c in components:
        com=c.split(', ')
        if com[2]:
            total += float(com[2])

    for p in poms:
        pom=p.split(', ')
        if pom[2]:
            total += float(pom[2])

    # total += float(request.POST.get('table_fabric_consumption'))
    # print(total)
    if request.POST.get('wastage'):
        if float(request.POST.get('wastage')) != 0:
            total+=total+((float(request.POST.get('wastage'))/100)*total)
            # print(total, request.POST.get('wastage'))

    total=round(total, 3)
    data={'total':total}

    return JsonResponse(data)

def auto_generate_order_no(email, fabric_code):
    last_order_no = company_Order.objects.all().last()
    
    if not last_order_no:
        return {"order_no": 2019000001, "user_email": email}
    new_order_no = last_order_no.order_no + 1
    print(new_order_no)
    new_order_no = str(new_order_no)
    new_order_no = new_order_no[-5:]
    x = str(datetime.datetime.now().year)
    y = str(datetime.datetime.now().month)
    z = str(datetime.datetime.now().day)
    new_order_no = int(x+y+z+new_order_no)
    return {"order_no": new_order_no, "user_email": email, "fabrics": fabric_code, "fabric_flag": False}

@csrf_exempt
def auto_fill(request):
    fabric_code = request.POST.get('fabric_code')
    if fabric_code:
        fabric_id = int(fabric_code[12::])
        fabric_co = trims_product.objects.filter(id=fabric_id)
        for f in fabric_co:

            data = {
                'fabric_blend': f.atrribute11,
                'epi': f.atrribute7,
                'ppi': f.atrribute8,
                'gsm': f.atrribute10,
                'wrap': f.atrribute4,
                'weft': f.atrribute5,
                'supplier': f.seller.email,
                'description': f.notes,
                'finish': f.atrribute12
                # 'fabric_direction':f.fabric_direction.name,
                # 'fabric_print_type':f.fabric_print_type.name,
                # 'fabric_print_design':f.fabric_print_design.name,
				# 'width': f.fabric_width.name,
            }

            if f.fabric_width is not None:
                data['width']=f.fabric_width.name
            if f.fabric_direction is not None:
                data['fabric_direction']=f.fabric_direction.name
            if f.fabric_print_type is not None:
                data['fabric_print_type']=f.fabric_print_type.name
            if f.fabric_print_design is not None:
                data['fabric_print_design']=f.fabric_print_design.name

            return JsonResponse(data)


@csrf_exempt
def load_style(request):
    product_Supercategory = request.POST.get('super_cate')
    product_Subcategory = request.POST.get('sub_cate')
    product_Category = request.POST.get('category')
    super_cate = labels_Attributes.objects.filter(product_Category__name__exact=product_Category,
                                                  product_Subcategory__name__exact=product_Subcategory,
                                                  product_Supercategory__name__exact=product_Supercategory)
    pom = POM.objects.filter(product_Category__name__exact=product_Category,
                             product_Subcategory__name__exact=product_Subcategory,
                             product_Supercategory__name__exact=product_Supercategory)

    size = request.POST.get('size')
    color = request.POST.get('color')
    sizes = request.POST.get('sizes')
    dispatch = request.POST.getlist('dispatch[]')
    print(dispatch)
    if size:
        color = color.split(', ')
        sizes = sizes.split(', ')
        data = {'size': size, 'color': color, 'sizes': sizes, 'dispatch': dispatch}
        return render(request, 'b2b/loadStyle.html', data)

    fabric_code = request.POST.get('fabric_code')
    if fabric_code:
        fabric_id = int(fabric_code[12::])
        fabric_co = trims_product.objects.filter(id=fabric_id).first().trims_labels
        return render(request, 'b2b/loadStyle.html', {'trims_attr': fabric_co})

    if request.POST.get('garment'):
        garment_matching = garment_matching_parameters.objects.filter(product_Category__name__exact=product_Category,
                                                                      product_Subcategory__name__exact=product_Subcategory,
                                                                      product_Supercategory__name__exact=product_Supercategory)
        data = {'garment_matching': garment_matching, 'garment': request.POST.get('garment')}
        return render(request, 'b2b/loadStyle.html', data)

    if request.POST.get('garment_matching_id'):
        garment_matching = garment_matching_parameters.objects.filter(
            id=request.POST.get('garment_matching_id')).first()
        levels = garment_matching.values.split(', ')
        print(levels)
        data = {'level': levels}
        return JsonResponse(data)

    if request.POST.get('garment_name'):
        matching_requirements = garment_matching_requirements.objects.filter(
            product_Category__name__exact=product_Category, product_Subcategory__name__exact=product_Subcategory,
            product_Supercategory__name__exact=product_Supercategory).first()
        value = request.POST.get('garment_name')
        requirements = []
        data={}
        if matching_requirements:
            if value == 'no matching':
                fabric_consumption = 'None'
                requirements = matching_requirements.no_matching.split('\n')
            elif value == 'level1':
                fabric_consumption = matching_requirements.fabric_consumption_level1
                requirements = matching_requirements.level1.split('\n')
            elif value == 'level2':
                fabric_consumption = matching_requirements.fabric_consumption_level2
                requirements = matching_requirements.level2.split('\n')
            elif value == 'level3':
                fabric_consumption = matching_requirements.fabric_consumption_level3
                requirements = matching_requirements.level3.split('\n')

            data = {'requirements': requirements, 'fabric_consumption': fabric_consumption}
        return JsonResponse(data)

    return render(request, 'b2b/loadStyle.html', {'super_cate': super_cate, 'pom': pom})

@csrf_exempt
def load_sizeTable(request):

    #size=request.GET.get('size')
    if request.POST.get('sector'):
        cate=request.POST.get('category')
        sector=request.POST.get('sector')
        super_cate=request.POST.get('super_cate')
        sub_cate=request.POST.get('sub_cate')
        label=request.POST.get('labels')
        fit=request.POST.get('fits')
        #print(label)
        #print(fit)
        size_assortment=size_assortment_pattern.objects.filter(sector__id__exact=sector,
                                                               product_Category__name__exact=cate,
                                                               product_Subcategory__name__exact=sub_cate,
                                                               product_Supercategory__name__exact=super_cate,
                                                               product_Labels__slug__exact=label,
                                                               product_Fits__slug__exact=fit)
        data={}
        ratios=list(size_assortment.values())
        j=0
        for i in size_assortment:
            ratios[j]["size"]=list(i.size.values())
            j+=1

        print(ratios)
        for s in size_assortment:
            if s.default:
                size=list(s.size.values())
                data = {"size": size,
                        "ratio": s.ratio.split(", "),
                        "default": s.default,
                        "consumption": s.fabric_consumption,
                        "ratios":ratios
                    }
                print(data)
                return JsonResponse(data)
        return JsonResponse(data)

def buisness_order(request,order_no=None,*args,**kwargs):
    if request.user.is_authenticated:
        orders=company_Order.objects.filter(user_email=request.user.email,order_no=order_no)
        ohj=quantity_b2b.objects.filter(order=orders.first())
        if orders.count()>0:
            order=orders.first()
            oij=staff_Categories.objects.filter(name="Sales").first()
            cnt_per=order.staffs_Allocated.filter(staff=True,position='C',staff_category=oij).first()
            order_bool=False
            enquiry_bool=False
            sample_bool=False
            design_bool=False
            if order.order_type=='O':
                order_bool=True
            elif order.order_type=='E':
                enquiry_bool=True
            elif order.order_type=='S':
                sample_bool=True
            else:
                design_bool=True
            color_av=order.colors_avail.all()
            li=[]
            li1=[]
            color_av=quantity_b2b.objects.filter(order=order)
            some_map_loc=[]
            for hgy in color_av:
                li21=[hgy.color,hgy.address]
                if li21 not in some_map_loc:
                    some_map_loc.append(li21)
            # print(some_map_loc)
            for c in some_map_loc:
                # oyu=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1])
                # for k in oyu:
                li2={"color":None,"size":None,"total":None}
                li3=[]
                some_obj=quantity_b2b.objects.filter(order=order,color=c[0],address=c[1])
                li2["color"]=some_obj.first()
                total=0
                for j in some_obj:
                    li3.append(j)
                    total=total+j.quantity
                li2["size"]=li3
                li2["total"]=total
                print(li2)
                li.append(li2)
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
            for i in ohj:
                if i.size_label not in li1:
                    li1.append(i.size_label)
            li1.sort()
            li4=[]
            total_overall=0
            for j in li1:
                objs=quantity_b2b.objects.filter(order=order,size_label=j)
                total=0
                for k in objs:
                    total=total+k.quantity
                total_overall=total_overall+total
                li4.append(total)
            li4.append(total_overall)
            trims_cate=trims_Category.objects.filter(fabric=True).first()
            # for i in
            trims=trims_product.objects.filter(category=trims_cate)

            fabrics = str(order.fabrics)
            print(fabrics)
            if fabrics != 'None':
                fabric_id = int(fabrics[12::])
                fabrics = trims_product.objects.filter(id=fabric_id).first()

            measu=None
            if order.fashion_Brand and order.label and order.fit and order.season:
                measu=measurement.objects.filter(
                        user=order.fashion_Brand,
                        label=order.label,
                        fit=order.fit,
                        season=order.season
                    ).first()
            details = detail.objects.filter(email=request.user.email).first()
            order_section = orders_permission.objects.filter(staff_category=details.staff_category).first()
            if order_section:
                order_section = order_section.allowed_section.all().filter(order_section=True)
            else:
                order_section = ['Order_Description']

            data={
                "order_no":order_no,
                "order":order,
                "quan":ohj,
                "enquiry_bool":enquiry_bool,
                "order_bool":order_bool,
                "sample_bool":sample_bool,
                "design_bool":design_bool,
                "cnt":cnt_per,
                "quan_by_clr":li,
                "size_by_quan":li1,
                "quan_by_sz":li4,
                "trims":trims,
                "measu":measu,
                "fabrics": fabrics,
                "order_section":order_section
            }
            if request.POST.get('perm_assortment'):
                assortment_custom=request.POST.get('assortment_custom')
                assortment_size_set=request.POST.get('assortment_size_set')
                assortment_brand=request.POST.get('assortment_brand')
                pom_for_consumer=request.POST.get('pom_for_consumer')
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
                if pom_for_consumer:
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
                    address=address)
                if objs_size_assort.count()>0:
                    objs_size_assort=objs_size_assort.first()
                    objs_size_assort.quantity=objs_size_assort.quantity+quantity
                    objs_size_assort.save()
                else:
                    objs_size_assort=quantity_b2b(
                            order=order,
                            size_label=size_assort,
                            address=address,
                            color=color,
                            quantity=quantity
                        )
                    objs_size_assort.save()
                return redirect('/buisness/buisness_order/'+str(order.order_no))
            if request.POST.get('addre'):
                addre=request.POST.get('addre')
                ohj=address_model(
                    title="Location2",
                    address=addre
                    )
                ohj.save()
                order.dispatch_Address.add(ohj)
                order.save()
            if request.POST.get('fabric'):
                fab_id=int(request.POST.get('fabric'))
                objs_trims=trims_product.objects.filter(id=fab_id).first()
                order.fabrics=objs_trims
                order.fabric_consump=request.POST.get('fab_consum')
                order.fabric_color=request.POST.get('fab_color')
                order.accesories=request.POST.get('accesories')
                order.packing_details=request.POST.get('packing_details')
                order.cpo=request.FILES.get('cpo')
                order.save()
                return redirect('/buisness/buisness_order/'+str(order.order_no))
            return render(request,"b2b/buisness_order.html",data)
        else:
            return redirect('/buisness/buisness_profile')
    else:
        return redirect('/userdetail/login')



def size_assortment_algo(base,base_pom,grades,tolerance,input_pom):
    updated=[]
    for i in range(len(input_pom)):
        # print(type(input_pom[i]),type(base_pom[i]),type(grades[i]))
        differ=(input_pom[i]-base_pom[i])/grades[i]
        positive=1
        if differ<0:
            positive=0
        differ=int(differ)
        first=base_pom[i]+grades[i]*differ
        if positive:
            second=first+grades[i]
        else:
            second=first-grades[i]
        if abs(first-input_pom[i]) <= abs(second-input_pom[i]):
            differ_base=differ
        else:
            if positive:
                differ_base=differ+1
            else:
                differ_base=differ-1
        if positive:
            updated.append(base+(differ_base*2))
        else:
            updated.append(base-(differ_base*2))
    updated1=set(updated)
    count_li=[]
    # print(updated,updated1)
    maxium=-1
    for j in updated1:
        count_pom=updated.count(updated[i])
        count_li.append(count_pom)
        if count_pom > maxium:
            maxium=count_pom
            maxim=updated[i]
    # maxi=max(count_li)
    # # print(count_li)
    # indi=count_li.index(maxi)
    # count=0
    # for kl in updated1:
    # 	if count==indi:
    # 		final=kl
    # 	count=count+1
    final=maxim
    divi=[]
    differ_devi=(final-base)/2
    deviation=0
    for hj in range(len(input_pom)):
        cum=base_pom[hj]+(differ_devi*grades[hj])
        if round(abs(cum-input_pom[hj]),2) <= round(tolerance[hj],2):
            divi.append(0)
        else:
            deviation=1
            divi.append(round(input_pom[hj]-cum,2))
    return [[final,deviation],divi]



from b2b.models import alteration_assortment

def order_update(request,order_no):
    if request.user.is_authenticated:
        user=detail.objects.filter(email=request.user.email).first()
        kjl=company_Order.objects.filter(order_no=order_no).first()
        cons_order=consumer_Order_Quantity.objects.filter(user=user,order=kjl).first()
        if user.b2b_order and cons_order:
            brands=detail.objects.filter(activate_Seller=True)
            pom=POM.objects.filter(show_to_Customer=True,product_Supercategory=kjl.product_Supercategory)
            assort=assortment.objects.filter(order_no=kjl,user=user.email).first()
            allowed=True
            if assort:
                quant_obj=quantity_b2b.objects.filter(assortments=assort,production=True).first()
                if quant_obj:
                    allowed=False

            if request.POST.get('tailor') and allowed:
                kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
                if not(kjl.single_unit_Price):
                    kjl.single_unit_Price=1804
                single_price=kjl.single_unit_Price
                kjl.save()
                to_get=POM.objects.filter(
                    product_Category=kjl.product_Category,
                    product_Subcategory=kjl.product_Subcategory,
                    product_Supercategory=kjl.product_Supercategory,
                    show_to_Customer=True)
                to_get=list(to_get.values())
                # attri=request.POST.get(to_get[0]["label"])
                input_pom=[]
                for sin_input in to_get:
                    input_pom.append(float(request.POST.get(sin_input["label"])))
                kj=measurement.objects.filter(
                    season=kjl.season,
                    product_Supercategory=kjl.product_Supercategory,
                    user=kjl.fashion_Brand).first()
                # size=float(attri)
                size1=float(kj.attribute1)
                grade1=float(kj.grading1)
                tolerance1=float(kj.tolerance1)
                base_pom=[]
                grade=[]
                tolerance=[]
                count=1
                while size1:
                    base_pom.append(size1)
                    grade.append(grade1)
                    tolerance.append(tolerance1)
                    if count==1:
                        size1=float(kj.attribute2)
                        grade1=float(kj.grading2)
                        tolerance1=float(kj.tolerance2)
                    elif count==2:
                        if kj.attribute3:
                            size1=float(kj.attribute3)
                            grade1=float(kj.grading3)
                            tolerance1=float(kj.tolerance3)
                        else:
                            size1=None
                    elif count==3:
                        if kj.attribute4:
                            size1=float(kj.attribute4)
                            grade1=float(kj.grading4)
                            tolerance1=float(kj.tolerance4)
                        else:
                            size1=None
                    elif count==4:
                        if kj.attribute5:
                            size1=float(kj.attribute5)
                            grade1=float(kj.grading5)
                            tolerance1=float(kj.tolerance5)
                        else:
                            size1=None
                    elif count==5:
                        if kj.attribute6:
                            size1=float(kj.attribute6)
                            grade1=float(kj.grading6)
                            tolerance1=float(kj.tolerance6)
                        else:
                            size1=None
                    elif count==6:
                        if kj.attribute7:
                            size1=float(kj.attribute7)
                            grade1=float(kj.grading7)
                            tolerance1=float(kj.tolerance7)
                        else:
                            size1=None
                    elif count==7:
                        if kj.attribute8:
                            size1=float(kj.attribute8)
                            grade1=float(kj.grading8)
                            tolerance1=float(kj.tolerance8)
                        else:
                            size1=None
                    elif count==8:
                        if kj.attribute9:
                            size1=float(kj.attribute9)
                            grade1=float(kj.grading9)
                            tolerance1=float(kj.tolerance9)
                        else:
                            size1=None
                    elif count==9:
                        if kj.attribute10:
                            size1=float(kj.attribute10)
                            grade1=float(kj.grading10)
                            tolerance1=float(kj.tolerance10)
                        else:
                            size1=None
                    elif count==10:
                        if kj.attribute11:
                            size1=float(kj.attribute11)
                            grade1=float(kj.grading11)
                            tolerance1=float(kj.tolerance11)
                        else:
                            size1=None
                    elif count==11:
                        if kj.attribute12:
                            size1=float(kj.attribute12)
                            grade1=float(kj.grading12)
                            tolerance1=float(kj.tolerance12)
                        else:
                            size1=None
                    elif count==12:
                        if kj.attribute13:
                            size1=float(kj.attribute13)
                            grade1=float(kj.grading13)
                            tolerance1=float(kj.tolerance13)
                        else:
                            size1=None
                    elif count==13:
                        if kj.attribute14:
                            size1=float(kj.attribute14)
                            grade1=float(kj.grading14)
                            tolerance1=float(kj.tolerance14)
                        else:
                            size1=None
                    elif count==14:
                        if kj.attribute15:
                            size1=float(kj.attribute15)
                            grade1=float(kj.grading15)
                            tolerance1=float(kj.tolerance15)
                        else:
                            size1=None
                    elif count==15:
                        if kj.attribute16:
                            size1=float(kj.attribute16)
                            grade1=float(kj.grading16)
                            tolerance1=float(kj.tolerance16)
                        else:
                            size1=None
                    elif count==16:
                        if kj.attribute17:
                            size1=float(kj.attribute17)
                            grade1=float(kj.grading17)
                            tolerance1=float(kj.tolerance17)
                        else:
                            size1=None
                    elif count==17:
                        if kj.attribute18:
                            size1=float(kj.attribute18)
                            grade1=float(kj.grading18)
                            tolerance1=float(kj.tolerance18)
                        else:
                            size1=None
                    elif count==18:
                        if kj.attribute19:
                            size1=float(kj.attribute19)
                            grade1=float(kj.grading19)
                            tolerance1=float(kj.tolerance19)
                        else:
                            size1=None
                    elif count==19:
                        if kj.attribute20:
                            size1=float(kj.attribute20)
                            grade1=float(kj.grading20)
                            tolerance1=float(kj.tolerance20)
                        else:
                            size1=None
                    elif count==20:
                        if kj.attribute21:
                            size1=float(kj.attribute21)
                            grade1=float(kj.grading21)
                            tolerance1=float(kj.tolerance21)
                        else:
                            size1=None
                    elif count==21:
                        if kj.attribute22:
                            size1=float(kj.attribute22)
                            grade1=float(kj.grading22)
                            tolerance1=float(kj.tolerance22)
                        else:
                            size1=None
                    elif count==22:
                        if kj.attribute23:
                            size1=float(kj.attribute23)
                            grade1=float(kj.grading23)
                            tolerance1=float(kj.tolerance23)
                        else:
                            size1=None
                    elif count==23:
                        if kj.attribute24:
                            size1=float(kj.attribute24)
                            grade1=float(kj.grading24)
                            tolerance1=float(kj.tolerance24)
                        else:
                            size1=None
                    elif count==24:
                        if kj.attribute25:
                            size1=float(kj.attribute25)
                            grade1=float(kj.grading25)
                            tolerance1=float(kj.tolerance25)
                        else:
                            size1=None
                    elif count==25:
                        if kj.attribute26:
                            size1=float(kj.attribute26)
                            grade1=float(kj.grading26)
                            tolerance1=float(kj.tolerance26)
                        else:
                            size1=None
                    elif count==26:
                        if kj.attribute27:
                            size1=float(kj.attribute27)
                            grade1=float(kj.grading27)
                            tolerance1=float(kj.tolerance27)
                        else:
                            size1=None
                    elif count==27:
                        if kj.attribute28:
                            size1=float(kj.attribute28)
                            grade1=float(kj.grading28)
                            tolerance1=float(kj.tolerance28)
                        else:
                            size1=None
                    elif count==28:
                        if kj.attribute29:
                            size1=float(kj.attribute29)
                            grade1=float(kj.grading29)
                            tolerance1=float(kj.tolerance29)
                        else:
                            size1=None
                    elif count==29:
                        if kj.attribute30:
                            size1=float(kj.attribute30)
                            grade1=float(kj.grading30)
                            tolerance1=float(kj.tolerance30)
                        else:
                            size1=None
                    count=count+1


                print(kj.name,base_pom,grade,tolerance,input_pom)
                assorted=size_assortment_algo(kj.name,base_pom,grade,tolerance,input_pom)
                print(assorted)
                final_assortment_obj=assortment()

                final_assortment_obj.size_label=assorted[0][0]
                final_assortment_obj.user=user.email
                final_assortment_obj.user_name=user.name
                final_assortment_obj.order_no=kjl
                final_assortment_obj.alteration_cost=0
                length=len(to_get)
                alt=single_price*0.05
                for i in range(length):
                    if i==0:
                        final_assortment_obj.attribute1=input_pom[i]
                        final_assortment_obj.deviation1=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration1=assorted[1][i]
                            final_assortment_obj.alteration_Cost1=alt
                        else:
                            final_assortment_obj.alteration1=0
                            final_assortment_obj.alteration_Cost1=0
                    elif i==1:
                        final_assortment_obj.attribute2=input_pom[i]
                        final_assortment_obj.deviation2=assorted[1][i]
                        final_assortment_obj.alteration2=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost2=alt
                        else:
                            final_assortment_obj.alteration_Cost2=0
                    elif i==2:
                        final_assortment_obj.attribute3=input_pom[i]
                        final_assortment_obj.deviation3=assorted[1][i]
                        final_assortment_obj.alteration3=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost3=alt
                        else:
                            final_assortment_obj.alteration_Cost3=0
                    elif i==3:
                        final_assortment_obj.attribute4=input_pom[i]
                        final_assortment_obj.deviation4=assorted[1][i]
                        final_assortment_obj.alteration4=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost4=alt
                        else:
                            final_assortment_obj.alteration_Cost4=0
                    elif i==4:
                        final_assortment_obj.attribute5=input_pom[i]
                        final_assortment_obj.deviation5=assorted[1][i]
                        final_assortment_obj.alteration5=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost5=alt
                        else:
                            final_assortment_obj.alteration_Cost5=0
                    elif i==5:
                        final_assortment_obj.attribute6=input_pom[i]
                        final_assortment_obj.deviation6=assorted[1][i]
                        final_assortment_obj.alteration6=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost6=alt
                        else:
                            final_assortment_obj.alteration_Cost6=0
                    elif i==6:
                        final_assortment_obj.attribute7=input_pom[i]
                        final_assortment_obj.deviation7=assorted[1][i]
                        final_assortment_obj.alteration7=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost7=alt
                        else:
                            final_assortment_obj.alteration_Cost7=0
                    elif i==7:
                        final_assortment_obj.attribute8=input_pom[i]
                        final_assortment_obj.deviation8=assorted[1][i]
                        final_assortment_obj.alteration8=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost8=alt
                        else:
                            final_assortment_obj.alteration_Cost8=0
                    elif i==8:
                        final_assortment_obj.attribute9=input_pom[i]
                        final_assortment_obj.deviation9=assorted[1][i]
                        final_assortment_obj.alteration9=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost9=alt
                        else:
                            final_assortment_obj.alteration_Cost9=0
                    elif i==9:
                        final_assortment_obj.attribute10=input_pom[i]
                        final_assortment_obj.deviation10=assorted[1][i]
                        final_assortment_obj.alteration10=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost10=alt
                        else:
                            final_assortment_obj.alteration_Cost10=0
                    elif i==10:
                        final_assortment_obj.attribute11=input_pom[i]
                        final_assortment_obj.deviation11=assorted[1][i]
                        final_assortment_obj.alteration11=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost11=alt
                        else:
                            final_assortment_obj.alteration_Cost11=0
                    elif i==11:
                        final_assortment_obj.attribute12=input_pom[i]
                        final_assortment_obj.deviation12=assorted[1][i]
                        final_assortment_obj.alteration12=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost12=alt
                        else:
                            final_assortment_obj.alteration_Cost12=0
                    elif i==12:
                        final_assortment_obj.attribute13=input_pom[i]
                        final_assortment_obj.deviation13=assorted[1][i]
                        final_assortment_obj.alteration13=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost13=alt
                        else:
                            final_assortment_obj.alteration_Cost13=0
                    elif i==13:
                        final_assortment_obj.attribute14=input_pom[i]
                        final_assortment_obj.deviation14=assorted[1][i]
                        final_assortment_obj.alteration14=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost14=alt
                        else:
                            final_assortment_obj.alteration_Cost14=0
                    elif i==14:
                        final_assortment_obj.attribute15=input_pom[i]
                        final_assortment_obj.deviation15=assorted[1][i]
                        final_assortment_obj.alteration15=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost15=alt
                        else:
                            final_assortment_obj.alteration_Cost15=0
                    elif i==15:
                        final_assortment_obj.attribute16=input_pom[i]
                        final_assortment_obj.deviation16=assorted[1][i]
                        final_assortment_obj.alteration16=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost16=alt
                        else:
                            final_assortment_obj.alteration_Cost16=0
                    elif i==16:
                        final_assortment_obj.attribute17=input_pom[i]
                        final_assortment_obj.deviation17=assorted[1][i]
                        final_assortment_obj.alteration17=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost17=alt
                        else:
                            final_assortment_obj.alteration_Cost17=0
                    elif i==17:
                        final_assortment_obj.attribute18=input_pom[i]
                        final_assortment_obj.deviation18=assorted[1][i]
                        final_assortment_obj.alteration18=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost18=alt
                        else:
                            final_assortment_obj.alteration_Cost18=0
                    elif i==18:
                        final_assortment_obj.attribute19=input_pom[i]
                        final_assortment_obj.deviation19=assorted[1][i]
                        final_assortment_obj.alteration19=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost19=alt
                        else:
                            final_assortment_obj.alteration_Cost19=0
                    elif i==19:
                        final_assortment_obj.attribute20=input_pom[i]
                        final_assortment_obj.deviation20=assorted[1][i]
                        final_assortment_obj.alteration20=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost20=alt
                        else:
                            final_assortment_obj.alteration_Cost20=0
                    elif i==20:
                        final_assortment_obj.attribute21=input_pom[i]
                        final_assortment_obj.deviation21=assorted[1][i]
                        final_assortment_obj.alteration21=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost21=alt
                        else:
                            final_assortment_obj.alteration_Cost21=0
                    elif i==21:
                        final_assortment_obj.attribute22=input_pom[i]
                        final_assortment_obj.deviation22=assorted[1][i]
                        final_assortment_obj.alteration22=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost22=alt
                        else:
                            final_assortment_obj.alteration_Cost22=0
                    elif i==22:
                        final_assortment_obj.attribute23=input_pom[i]
                        final_assortment_obj.deviation23=assorted[1][i]
                        final_assortment_obj.alteration23=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost23=alt
                        else:
                            final_assortment_obj.alteration_Cost23=0
                    elif i==23:
                        final_assortment_obj.attribute24=input_pom[i]
                        final_assortment_obj.deviation24=assorted[1][i]
                        final_assortment_obj.alteration24=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost24=alt
                        else:
                            final_assortment_obj.alteration_Cost24=0
                    elif i==24:
                        final_assortment_obj.attribute25=input_pom[i]
                        final_assortment_obj.deviation25=assorted[1][i]
                        final_assortment_obj.alteration25=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost25=alt
                        else:
                            final_assortment_obj.alteration_Cost25=0
                    elif i==25:
                        final_assortment_obj.attribute26=input_pom[i]
                        final_assortment_obj.deviation26=assorted[1][i]
                        final_assortment_obj.alteration26=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost26=alt
                        else:
                            final_assortment_obj.alteration_Cost26=0
                    elif i==26:
                        final_assortment_obj.attribute27=input_pom[i]
                        final_assortment_obj.deviation27=assorted[1][i]
                        final_assortment_obj.alteration27=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost27=alt
                        else:
                            final_assortment_obj.alteration_Cost27=0
                    elif i==27:
                        final_assortment_obj.attribute28=input_pom[i]
                        final_assortment_obj.deviation28=assorted[1][i]
                        final_assortment_obj.alteration28=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost28=alt
                        else:
                            final_assortment_obj.alteration_Cost28=0
                    elif i==28:
                        final_assortment_obj.attribute29=input_pom[i]
                        final_assortment_obj.deviation29=assorted[1][i]
                        final_assortment_obj.alteration29=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost29=alt
                        else:
                            final_assortment_obj.alteration_Cost29=0
                    elif i==29:
                        final_assortment_obj.attribute30=input_pom[i]
                        final_assortment_obj.deviation30=assorted[1][i]
                        final_assortment_obj.alteration30=assorted[1][i]
                        if assorted[1][i]:
                            final_assortment_obj.alteration_Cost30=alt
                        else:
                            final_assortment_obj.alteration_Cost30=0
                    if assorted[1][i]:
                        final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+alt



                color=request.POST.get('color')
                color=color_model.objects.filter(name=color).first()
                addre=request.POST.get('addre')
                addre=address_model.objects.filter(id=int(addre)).first()
                final_assortment_obj.color=color
                final_assortment_obj.address=addre
                # if assorted[0][1]==1:
                # 	final_assortment_obj.alteration_req=True
                final_assortment_obj.save()


                if assorted[0][1]==0:
                    ouj=quantity_b2b.objects.filter(
                        order=kjl,
                        size=kj,
                        size_label=final_assortment_obj.size_label,
                        production=False,
                        color=color,
                        address=addre)
                    if ouj.count()>0:
                        ouj=ouj.first()
                        ouj.quantity=ouj.quantity+1
                        ouj.assortments.add(final_assortment_obj)
                        ouj.save()
                    else:
                        quantity_order_obj=quantity_b2b(
                            order=kjl,
                            size=kj,
                            size_label=final_assortment_obj.size_label,
                            quantity=1,
                            color=color,
                            address=addre)
                        quantity_order_obj.save()
                        quantity_order_obj.assortments.add(final_assortment_obj)
                        quantity_order_obj.save()
                if final_assortment_obj.alteration_cost!=0:
                    return redirect('/buisness/confirm_alteration')

                # to_del=detail.objects.filter(email=request.user.email).first()
                # to_del.delete()
                # to_del=User.objects.filter(email=request.user.email).first()
                # to_del.delete()
                return redirect('/userdetail/logout')
            if request.POST.get('placeorder_ajax_sizeset'):
                size_set=int(request.POST.get('placeorder_ajax_sizeset'))
                meas=kjl.get_measurement_chart
                sizes_val=measurement_chart.objects.filter(chart=meas,size=size_set)
                data={
                    'sizes':sizes_val
                }
                if kjl.show_pom_in_assortment:
                    return render(request,"ajax_response/b2b/order_update_sizes.html",data)
                else:
                    return HttpResponse()
            if (request.POST.get('size_set_but') and allowed):
                size=request.POST.get('size')
                comment=request.POST.get('comment')
                kjl=company_Order.objects.filter(order_no=order_no).first()
                to_get=POM.objects.filter(
                    product_Category=kjl.product_Category,
                    product_Subcategory=kjl.product_Subcategory,
                    product_Supercategory=kjl.product_Supercategory)
                kj=measurement.objects.filter(
                    season=kjl.season,
                    product_Supercategory=kjl.product_Supercategory,
                    user=kjl.fashion_Brand).first()
                color=request.POST.get('color')
                color=color_model.objects.filter(name=color).first()
                addre=request.POST.get('addre')
                quantity=request.POST.get('quantity')
                if quantity:
                    quantity=int(quantity)
                if addre:
                    addre=address_model.objects.filter(id=int(addre)).first()
                ouj=quantity_b2b.objects.filter(
                    order=kjl,
                    size=kj,
                    size_label=int(size),
                    color=color,
                    address=addre)
                ouj1=assortment.objects.filter(user=user.email,order_no=kjl).first()
                if ouj1:
                    quantity_obj=quantity_b2b.objects.filter(order=kjl,size_label=ouj1.size_label,color=color,address=addre).first()
                    if quantity_obj:
                        quantity_obj.quantity-=ouj1.quantity
                        quantity_obj.assortments.remove(ouj1)
                        quantity_obj.save()
                    ouj1.size_label=int(size)
                    ouj1.color=color
                    ouj1.address=addre
                    ouj1.quantity=quantity
                    ouj1.comment=comment
                    ouj1.alteration_cost=0
                    ouj1.save()
                else:
                    ouj1=assortment(
                        user=user.email,
                        user_name=user.name,
                        order_no=kjl,
                        size_label=int(size),
                        color=color,
                        address=addre,
                        quantity=quantity,
                        comment=comment,
                        alteration_cost=0
                    )
                    ouj1.save()
                check=1
                meas=kjl.get_measurement_chart
                chart=measurement_chart.objects.filter(chart=meas,size=size)
                for i in chart:
                    if request.POST.get('pom_alteration_'+str(i.pom.id)):
                        check=0
                        no=int(request.POST.get('pom_alteration_'+str(i.pom.id)))
                        new_cust_assort=alteration_assortment(pom=POM.objects.filter(id=i.pom.id).first(),alteration=no)
                        new_cust_assort.save()
                        ouj1.alteration_assort.add(new_cust_assort)
                        ouj1.save()
                if check:
                    if ouj.count()>0:
                        ouj=ouj.first()
                        ouj.quantity=ouj.quantity+quantity
                        ouj.assortments.add(ouj1)
                        ouj.save()
                    else:
                        quantity_order_obj=quantity_b2b(
                            order=kjl,
                            size=kj,
                            size_label=int(size),
                            quantity=quantity,
                            color=color,
                            address=addre)
                        quantity_order_obj.save()
                        quantity_order_obj.assortments.add(ouj1)
                        quantity_order_obj.save()

                return redirect('/userdetail/logout')


            ouj1=assortment.objects.filter(user=user.email,order_no=kjl).first()
            if request.POST.get('distributed') and ouj1 and not(ouj1.distributed):
                ouj1.distributed=True
                ouj1.save()
                # print("Done")
                distri_obj=distribution_list.objects.filter(address=ouj1.address,order=kjl).first()
                if not(distri_obj):
                    distri_obj=distribution_list(address=ouj1.address,order=kjl,name="Default")
                size=int(ouj1.size_label)
                if size==24:
                    distri_obj.quantity_24+=ouj1.quantity
                elif size==26:
                    distri_obj.quantity_26+=ouj1.quantity
                elif size==28:
                    distri_obj.quantity_28+=ouj1.quantity
                elif size==30:
                    distri_obj.quantity_30+=ouj1.quantity
                elif size==32:
                    distri_obj.quantity_32+=ouj1.quantity
                elif size==34:
                    distri_obj.quantity_34+=ouj1.quantity
                elif size==36:
                    distri_obj.quantity_36+=ouj1.quantity
                elif size==38:
                    distri_obj.quantity_38+=ouj1.quantity
                elif size==40:
                    distri_obj.quantity_40+=ouj1.quantity
                elif size==42:
                    distri_obj.quantity_42+=ouj1.quantity
                elif size==44:
                    distri_obj.quantity_44+=ouj1.quantity
                elif size==46:
                    distri_obj.quantity_46+=ouj1.quantity
                elif size==48:
                    distri_obj.quantity_48+=ouj1.quantity
                elif size==50:
                    distri_obj.quantity_50+=ouj1.quantity
                elif size==52:
                    distri_obj.quantity_52+=ouj1.quantity
                distri_obj.save()
                # to_del=detail.objects.filter(email=request.user.email).first()
                # to_del.delete()
                # to_del=User.objects.filter(email=request.user.email).first()
                # to_del.delete()

                return redirect('/userdetail/logout')





            if request.POST.get('brand') and allowed:
                obj=detail.objects.filter(id=int(request.POST.get('brand'))).first()
                obj1=labels.objects.get(slug=request.POST.get('label'))
                obj2=fits.objects.get(slug=request.POST.get('fit'))
                obj3=seasons.objects.get(slug=request.POST.get('season'))
                size_by_brand=int(request.POST.get('size'))
                kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
                meas_obj_usr1=measurement.objects.filter(
                    season=obj3,
                    product_Supercategory=kjl.product_Supercategory,
                    user=obj).first()
                meas_obj_usr2=measurement.objects.filter(
                    season=kjl.season,
                    product_Supercategory=kjl.product_Supercategory,
                    user=kjl.fashion_Brand).first()
                size_usr1=int(meas_obj_usr1.name)
                if size_by_brand>size_usr1:
                    times=int(size_by_brand - size_usr1)
                    usr1_attri1=meas_obj_usr1.attribute1 + int(meas_obj_usr1.grading1 * times)
                elif size_by_brand<size_usr1:
                    times=int(size_usr1 - size_by_brand)
                    usr1_attri1=meas_obj_usr1.attribute1 - int(meas_obj_usr1.grading1 * times)
                else:
                    usr1_attri1=meas_obj_usr1.attribute1
                size=int(usr1_attri1)
                size1=int(meas_obj_usr2.attribute1)
                kj=meas_obj_usr2


                if size>size1:
                    times=(size-size1)/int(kj.grading1)
                    final=int(kj.name)+times
                elif size1>size:
                    times=(size+size1)/int(kj.grading1)
                    final=int(kj.name)-times
                else:
                    times=1
                    final=int(kj.name)
                color=request.POST.get('color')
                color=color_model.objects.filter(name=color).first()
                addre=request.POST.get('addre')
                addre=address_model.objects.filter(id=int(addre)).first()
                ouj=quantity_b2b.objects.filter(
                    order=kjl,
                    size=kj,
                    size_label=final,
                    color=color,
                    address=addre)
                if ouj.count()>0:
                    ouj=ouj.first()
                    ouj.quantity=ouj.quantity+1
                    ouj.save()
                else:
                    quantity_order_obj=quantity_b2b(
                        order=kjl,
                        size=kj,
                        size_label=abs(final),
                        quantity=1,
                    color=color,
                    address=addre)
                    quantity_order_obj.save()






                to_del=detail.objects.filter(email=request.user.email).first()
                to_del.delete()
                to_del=User.objects.filter(email=request.user.email).first()
                to_del.delete()
                return redirect('/userdetail/logout')
            if request.POST.get('placeorder_ajax_season'):
                ook=seasons.objects.get(slug=request.POST.get('placeorder_ajax_season'))
                ook1=detail.objects.get(id=request.POST.get('placeorder_ajax_season_brand'))
                ook2=company_Order.objects.get(order_no=user.b2b_order_no).product_Supercategory
                objh=measurement.objects.filter(season=ook,user=ook1,product_Supercategory=ook2)
                if objh.count()>0:
                    bol=True
                else:
                    bol=False
                objh=list(objh.values())
                return HttpResponse(json.dumps({'data': objh,'bol':bol}), content_type="application/json")



            assorted_obj=assortment.objects.filter(user=user.email,order_no=kjl).first()
            data_set={
            "brand":brands,
            "pom":pom,
            "user":user,
            "color":kjl.colors_avail.all(),
            "addr":kjl.dispatch_Address.all(),
            "order":kjl,
            "cons_order":cons_order,
            "assorted_obj":assorted_obj,
            "allowed":not(allowed)
            }
            return render(request,'b2b/order_update.html',data_set)
        return redirect('/userdetail/login')
#
# def order_update(request):
# 	if request.user.is_authenticated:
# 		user=detail.objects.filter(email=request.user.email).first()
# 		if user.b2b_order:
# 			brands=detail.objects.filter(activate_Seller=True)
# 			pom=POM.objects.filter(show_to_Customer=True)
# 			kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
# 			if request.POST.get('tailor'):
# 				kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
# 				if not(kjl.single_unit_Price):
# 					kjl.single_unit_Price=1804
# 				kjl.save()
# 				to_get=POM.objects.filter(
# 					product_Category=kjl.product_Category,
# 					product_Subcategory=kjl.product_Subcategory,
# 					product_Supercategory=kjl.product_Supercategory)
# 				to_get=list(to_get.values())
# 				attri=request.POST.get(to_get[0]["label"])
# 				kj=measurement.objects.filter(
# 					season=kjl.season,
# 					product_Supercategory=kjl.product_Supercategory,
# 					user=kjl.fashion_Brand).first()
# 				size=float(attri)
# 				size1=float(kj.attribute1)
# 				final_assortment_obj=assortment()
# 				if size>size1:
# 					times=(size-size1)/kj.grading1
# 					times=int(times/2)*2
# 					final_size1=size1+(times*kj.grading1)
# 					final=int(kj.name)+times
# 					typeof=1
# 				elif size1>size:
# 					times=(size1-size)/int(kj.grading1)
# 					times=int(times/2)*2
# 					final_size1=size1-(times*kj.grading1)
# 					final=int(kj.name)-times
# 					typeof=2
# 				else:
# 					times=0
# 					final=int(kj.name)
# 					typeof=3
# 				final_assortment_obj.size_label=final
# 				final_assortment_obj.user=user.email
# 				final_assortment_obj.user_name=user.name
# 				final_assortment_obj.order_no=kjl
# 				final_assortment_obj.alteration_cost=0
# 				length=len(to_get)
#
# 				for i in range(length):
#
# 					attri=request.POST.get(to_get[i]["label"])
# 					if i==0:
# 						size1=float(kj.attribute1)
# 						grading=kj.grading1
# 						toler=kj.tolerance1
# 					elif i==1:
# 						size1=float(kj.attribute2)
# 						grading=kj.grading2
# 						toler=kj.tolerance2
# 					elif i==2:
# 						size1=float(kj.attribute3)
# 						grading=kj.grading3
# 						toler=kj.tolerance3
# 					elif i==3:
# 						size1=float(kj.attribute4)
# 						grading=kj.grading4
# 						toler=kj.tolerance4
# 					elif i==4:
# 						size1=float(kj.attribute5)
# 						grading=kj.grading5
# 						toler=kj.tolerance5
# 					elif i==5:
# 						size1=float(kj.attribute6)
# 						grading=kj.grading6
# 						toler=kj.tolerance6
# 					elif i==6:
# 						size1=float(kj.attribute7)
# 						grading=kj.grading7
# 						toler=kj.tolerance7
# 					elif i==7:
# 						size1=float(kj.attribute8)
# 						grading=kj.grading8
# 						toler=kj.tolerance8
# 					elif i==8:
# 						size1=float(kj.attribute9)
# 						grading=kj.grading9
# 						toler=kj.tolerance9
# 					elif i==9:
# 						size1=float(kj.attribute10)
# 						grading=kj.grading10
# 						toler=kj.tolerance10
# 					elif i==10:
# 						size1=float(kj.attribute11)
# 						grading=kj.grading11
# 						toler=kj.tolerance11
# 					elif i==11:
# 						size1=float(kj.attribute12)
# 						grading=kj.grading12
# 						toler=kj.tolerance12
# 					elif i==12:
# 						size1=float(kj.attribute13)
# 						grading=kj.grading13
# 						toler=kj.tolerance13
# 					elif i==13:
# 						size1=float(kj.attribute14)
# 						grading=kj.grading14
# 						toler=kj.tolerance14
# 					elif i==14:
# 						size1=float(kj.attribute15)
# 						grading=kj.grading15
# 						toler=kj.tolerance15
# 					elif i==15:
# 						size1=float(kj.attribute16)
# 						grading=kj.grading16
# 						toler=kj.tolerance16
# 					elif i==16:
# 						size1=float(kj.attribute17)
# 						grading=kj.grading17
# 						toler=kj.tolerance17
# 					elif i==17:
# 						size1=float(kj.attribute18)
# 						grading=kj.grading18
# 						toler=kj.tolerance18
# 					elif i==18:
# 						size1=float(kj.attribute19)
# 						grading=kj.grading19
# 						toler=kj.tolerance19
# 					elif i==19:
# 						size1=float(kj.attribute20)
# 						grading=kj.grading20
# 						toler=kj.tolerance20
# 					elif i==20:
# 						size1=float(kj.attribute21)
# 						grading=kj.grading21
# 						toler=kj.tolerance21
# 					elif i==21:
# 						size1=float(kj.attribute22)
# 						grading=kj.grading22
# 						toler=kj.tolerance22
# 					elif i==22:
# 						size1=float(kj.attribute23)
# 						grading=kj.grading23
# 						toler=kj.tolerance23
# 					elif i==23:
# 						size1=float(kj.attribute24)
# 						grading=kj.grading24
# 						toler=kj.tolerance24
# 					elif i==24:
# 						size1=float(kj.attribute25)
# 						grading=kj.grading25
# 						toler=kj.tolerance25
# 					elif i==25:
# 						size1=float(kj.attribute26)
# 						grading=kj.grading26
# 						toler=kj.tolerance26
# 					elif i==26:
# 						size1=float(kj.attribute27)
# 						grading=kj.grading27
# 						toler=kj.tolerance27
# 					elif i==27:
# 						size1=float(kj.attribute28)
# 						grading=kj.grading28
# 						toler=kj.tolerance28
# 					elif i==28:
# 						size1=float(kj.attribute29)
# 						grading=kj.grading29
# 						toler=kj.tolerance29
# 					elif i==29:
# 						grading=kj.grading30
# 						toler=kj.tolerance30
# 						size1=float(kj.attribute30)
#
# 					size=float(attri)
# 					if typeof==1:
# 						# times=(size-size1)/grading
# 						# times=int(times/2)*2
# 						final_size1=size1+(times*grading)
# 						final=int(kj.name)+times
# 					elif typeof==2:
# 						# times=(size1-size)/grading
# 						# times=int(times/2)*2
# 						final_size1=size1-(times*grading)
# 						final=int(kj.name)-times
# 					else:
# 						times=0
# 						final_size1=size1
# 						final=int(kj.name)
#
#
# 					if i==0:
#
# 						final_assortment_obj.attribute1=size
# 						final_assortment_obj.deviation1=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration1=0
# 							final_assortment_obj.alteration_Cost1=0
# 						else:
# 							final_assortment_obj.alteration1=final_size1-size
# 							final_assortment_obj.alteration_Cost1=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost1
# 					elif i==1:
# 						final_assortment_obj.attribute2=size
# 						final_assortment_obj.deviation2=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration2=0
# 							final_assortment_obj.alteration_Cost2=0
# 						else:
# 							final_assortment_obj.alteration2=final_size1-size
# 							final_assortment_obj.alteration_Cost2=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost2
# 					elif i==2:
# 						final_assortment_obj.attribute3=size
# 						final_assortment_obj.deviation3=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration3=0
# 							final_assortment_obj.alteration_Cost3=0
# 						else:
# 							final_assortment_obj.alteration3=final_size1-size
# 							final_assortment_obj.alteration_Cost3=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost3
# 					elif i==3:
# 						final_assortment_obj.attribute4=size
# 						final_assortment_obj.deviation4=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration4=0
# 							final_assortment_obj.alteration_Cost4=0
# 						else:
# 							final_assortment_obj.alteration4=final_size1-size
# 							final_assortment_obj.alteration_Cost4=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost4
# 					elif i==4:
# 						final_assortment_obj.attribute5=size
# 						final_assortment_obj.deviation5=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration5=0
# 							final_assortment_obj.alteration_Cost5=0
# 						else:
# 							final_assortment_obj.alteration5=final_size1-size
# 							final_assortment_obj.alteration_Cost5=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost5
# 					elif i==5:
# 						final_assortment_obj.attribute6=size
# 						final_assortment_obj.deviation6=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration6=0
# 							final_assortment_obj.alteration_Cost6=0
# 						else:
# 							final_assortment_obj.alteration6=final_size1-size
# 							final_assortment_obj.alteration_Cost6=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost6
# 					elif i==6:
# 						final_assortment_obj.attribute7=size
# 						final_assortment_obj.deviation7=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration7=0
# 							final_assortment_obj.alteration_Cost7=0
# 						else:
# 							final_assortment_obj.alteration7=final_size1-size
# 							final_assortment_obj.alteration_Cost7=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost7
# 					elif i==7:
# 						final_assortment_obj.attribute8=size
# 						final_assortment_obj.deviation8=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration8=0
# 							final_assortment_obj.alteration_Cost8=0
# 						else:
# 							final_assortment_obj.alteration8=final_size1-size
# 							final_assortment_obj.alteration_Cost8=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost8
# 					elif i==8:
# 						final_assortment_obj.attribute9=size
# 						final_assortment_obj.deviation9=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration9=0
# 							final_assortment_obj.alteration_Cost9=0
# 						else:
# 							final_assortment_obj.alteration9=final_size1-size
# 							final_assortment_obj.alteration_Cost9=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost9
# 					elif i==9:
# 						final_assortment_obj.attribute10=size
# 						final_assortment_obj.deviation10=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration10=0
# 							final_assortment_obj.alteration_Cost10=0
# 						else:
# 							final_assortment_obj.alteration10=final_size1-size
# 							final_assortment_obj.alteration_Cost10=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost10
# 					elif i==10:
# 						final_assortment_obj.attribute11=size
# 						final_assortment_obj.deviation11=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration11=0
# 							final_assortment_obj.alteration_Cost11=0
# 						else:
# 							final_assortment_obj.alteration11=final_size1-size
# 							final_assortment_obj.alteration_Cost11=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost11
# 					elif i==11:
# 						final_assortment_obj.attribute12=size
# 						final_assortment_obj.deviation12=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration12=0
# 							final_assortment_obj.alteration_Cost12=0
# 						else:
# 							final_assortment_obj.alteration12=final_size1-size
# 							final_assortment_obj.alteration_Cost12=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost12
# 					elif i==12:
# 						final_assortment_obj.attribute13=size
# 						final_assortment_obj.deviation13=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration13=0
# 							final_assortment_obj.alteration_Cost13=0
# 						else:
# 							final_assortment_obj.alteration13=final_size1-size
# 							final_assortment_obj.alteration_Cost13=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost13
# 					elif i==13:
# 						final_assortment_obj.attribute14=size
# 						final_assortment_obj.deviation14=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration14=0
# 							final_assortment_obj.alteration_Cost14=0
# 						else:
# 							final_assortment_obj.alteration14=final_size1-size
# 							final_assortment_obj.alteration_Cost14=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost14
# 					elif i==14:
# 						final_assortment_obj.attribute15=size
# 						final_assortment_obj.deviation15=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration15=0
# 							final_assortment_obj.alteration_Cost15=0
# 						else:
# 							final_assortment_obj.alteration15=final_size1-size
# 							final_assortment_obj.alteration_Cost15=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost15
# 					elif i==15:
# 						final_assortment_obj.attribute16=size
# 						final_assortment_obj.deviation16=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration16=0
# 							final_assortment_obj.alteration_Cost16=0
# 						else:
# 							final_assortment_obj.alteration16=final_size1-size
# 							final_assortment_obj.alteration_Cost16=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost16
# 					elif i==16:
# 						final_assortment_obj.attribute17=size
# 						final_assortment_obj.deviation17=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration17=0
# 							final_assortment_obj.alteration_Cost17=0
# 						else:
# 							final_assortment_obj.alteration17=final_size1-size
# 							final_assortment_obj.alteration_Cost17=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost17
# 					elif i==17:
# 						final_assortment_obj.attribute18=size
# 						final_assortment_obj.deviation18=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration18=0
# 							final_assortment_obj.alteration_Cost18=0
# 						else:
# 							final_assortment_obj.alteration18=final_size1-size
# 							final_assortment_obj.alteration_Cost18=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost18
# 					elif i==18:
# 						final_assortment_obj.attribute19=size
# 						final_assortment_obj.deviation19=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration19=0
# 							final_assortment_obj.alteration_Cost19=0
# 						else:
# 							final_assortment_obj.alteration19=final_size1-size
# 							final_assortment_obj.alteration_Cost19=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost19
# 					elif i==19:
# 						final_assortment_obj.attribute20=size
# 						final_assortment_obj.deviation20=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration20=0
# 							final_assortment_obj.alteration_Cost20=0
# 						else:
# 							final_assortment_obj.alteration20=final_size1-size
# 							final_assortment_obj.alteration_Cost20=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost20
# 					elif i==20:
# 						final_assortment_obj.attribute21=size
# 						final_assortment_obj.deviation21=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration21=0
# 							final_assortment_obj.alteration_Cost21=0
# 						else:
# 							final_assortment_obj.alteration21=final_size1-size
# 							final_assortment_obj.alteration_Cost21=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost21
# 					elif i==21:
# 						final_assortment_obj.attribute22=size
# 						final_assortment_obj.deviation22=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration22=0
# 							final_assortment_obj.alteration_Cost22=0
# 						else:
# 							final_assortment_obj.alteration22=final_size1-size
# 							final_assortment_obj.alteration_Cost22=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost22
# 					elif i==22:
# 						final_assortment_obj.attribute23=size
# 						final_assortment_obj.deviation23=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration23=0
# 							final_assortment_obj.alteration_Cost23=0
# 						else:
# 							final_assortment_obj.alteration23=final_size1-size
# 							final_assortment_obj.alteration_Cost23=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost23
# 					elif i==23:
# 						final_assortment_obj.attribute24=size
# 						final_assortment_obj.deviation24=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration24=0
# 							final_assortment_obj.alteration_Cost24=0
# 						else:
# 							final_assortment_obj.alteration24=final_size1-size
# 							final_assortment_obj.alteration_Cost24=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost24
# 					elif i==24:
# 						final_assortment_obj.attribute25=size
# 						final_assortment_obj.deviation25=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration25=0
# 							final_assortment_obj.alteration_Cost25=0
# 						else:
# 							final_assortment_obj.alteration25=final_size1-size
# 							final_assortment_obj.alteration_Cost25=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost25
# 					elif i==25:
# 						final_assortment_obj.attribute26=size
# 						final_assortment_obj.deviation26=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration26=0
# 							final_assortment_obj.alteration_Cost26=0
# 						else:
# 							final_assortment_obj.alteration26=final_size1-size
# 							final_assortment_obj.alteration_Cost26=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost26
# 					elif i==26:
# 						final_assortment_obj.attribute27=size
# 						final_assortment_obj.deviation27=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration27=0
# 							final_assortment_obj.alteration_Cost27=0
# 						else:
# 							final_assortment_obj.alteration27=final_size1-size
# 							final_assortment_obj.alteration_Cost27=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost27
# 					elif i==27:
# 						final_assortment_obj.attribute28=size
# 						final_assortment_obj.deviation28=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration28=0
# 							final_assortment_obj.alteration_Cost28=0
# 						else:
# 							final_assortment_obj.alteration28=final_size1-size
# 							final_assortment_obj.alteration_Cost28=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost28
# 					elif i==28:
# 						final_assortment_obj.attribute29=size
# 						final_assortment_obj.deviation29=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration29=0
# 							final_assortment_obj.alteration_Cost29=0
# 						else:
# 							final_assortment_obj.alteration29=final_size1-size
# 							final_assortment_obj.alteration_Cost29=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost29
# 					elif i==29:
# 						final_assortment_obj.attribute30=size
# 						final_assortment_obj.deviation30=final_size1-size
#
# 						if to_get[i]["admin_Tolerance"]>abs(final_size1-size):
# 							final_assortment_obj.alteration30=0
# 							final_assortment_obj.alteration_Cost30=0
# 						else:
# 							final_assortment_obj.alteration30=final_size1-size
# 							final_assortment_obj.alteration_Cost30=kjl.single_unit_Price*0.05
# 							final_assortment_obj.alteration_cost=final_assortment_obj.alteration_cost+final_assortment_obj.alteration_Cost30
#
#
# 				color=request.POST.get('color')
# 				color=color_model.objects.filter(name=color).first()
# 				addre=request.POST.get('addre')
# 				addre=address_model.objects.filter(id=int(addre)).first()
# 				final_assortment_obj.color=color
# 				final_assortment_obj.address=addre
# 				final_assortment_obj.save()
#
#
#
# 				ouj=quantity_b2b.objects.filter(
# 					order=kjl,
# 					size=kj,
# 					size_label=final_assortment_obj.size_label,
# 					production=False,
# 					color=color,
# 					address=addre)
# 				if ouj.count()>0:
# 					ouj=ouj.first()
# 					ouj.quantity=ouj.quantity+1
# 					ouj.save()
# 				else:
# 					quantity_order_obj=quantity_b2b(
# 						order=kjl,
# 						size=kj,
# 						size_label=final_assortment_obj.size_label,
# 						quantity=1,
# 						color=color,
# 						address=addre)
# 					quantity_order_obj.save()
# 				if final_assortment_obj.alteration_cost!=0:
# 					return redirect('/buisness/confirm_alteration')
#
# 				to_del=detail.objects.filter(email=request.user.email).first()
# 				to_del.delete()
# 				to_del=User.objects.filter(email=request.user.email).first()
# 				to_del.delete()
# 				return redirect('/userdetail/logout')
#
#
#
#
#
#
#
# 			if request.POST.get('placeorder_ajax_sizeset'):
# 				size_set=int(request.POST.get('placeorder_ajax_sizeset'))
# 				if size_set<28:
# 					bol=False
# 				elif size_set%2!=0:
# 					bol=False
# 				elif size_set>48:
# 					bol=False
# 				else:
# 					bol=True
# 					kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
# 					to_get=POM.objects.filter(
# 						product_Category=kjl.product_Category,
# 						product_Subcategory=kjl.product_Subcategory,
# 						product_Supercategory=kjl.product_Supercategory)
# 					kj=measurement.objects.filter(
# 						season=kjl.season,
# 						product_Supercategory=kjl.product_Supercategory,
# 						user=kjl.fashion_Brand).first()
# 					to_get=list(to_get.values())
# 					li=[]
# 					times=size_set-kj.name
# 					li.append(kj.attribute1+(kj.grading1*times))
# 					li.append(kj.attribute2+(kj.grading2*times))
# 					li.append(kj.attribute3+(kj.grading3*times))
# 					li.append(kj.attribute4+(kj.grading4*times))
# 					li.append(kj.attribute5+(kj.grading5*times))
# 					li.append(kj.attribute6+(kj.grading6*times))
# 					li.append(kj.attribute7+(kj.grading7*times))
# 					li.append(kj.attribute8+(kj.grading8*times))
# 					li.append(kj.attribute9+(kj.grading9*times))
# 					li.append(kj.attribute10+(kj.grading10*times))
# 					li.append(kj.attribute11+(kj.grading11*times))
# 					li.append(kj.attribute12+(kj.grading12*times))
# 					li.append(kj.attribute13+(kj.grading13*times))
# 					li.append(kj.attribute14+(kj.grading14*times))
# 					li.append(kj.attribute15+(kj.grading15*times))
# 					li.append(kj.attribute16+(kj.grading16*times))
# 					li.append(kj.attribute17+(kj.grading17*times))
# 					li.append(kj.attribute18+(kj.grading18*times))
# 					li.append(kj.attribute19+(kj.grading19*times))
# 					li.append(kj.attribute20+(kj.grading20*times))
# 					li.append(kj.attribute21+(kj.grading21*times))
# 					li.append(kj.attribute22+(kj.grading22*times))
# 					li.append(kj.attribute23+(kj.grading23*times))
# 					li.append(kj.attribute24+(kj.grading24*times))
# 					li.append(kj.attribute25+(kj.grading25*times))
# 					li.append(kj.attribute26+(kj.grading26*times))
# 					li.append(kj.attribute27+(kj.grading27*times))
# 					li.append(kj.attribute28+(kj.grading28*times))
# 					li.append(kj.attribute29+(kj.grading29*times))
# 					li.append(kj.attribute30+(kj.grading30*times))
#
# 					data={
# 					'kh':to_get,
# 					'li':li,
# 					'bol':bol,
# 					'size':size_set
# 					}
# 				return HttpResponse(json.dumps(data), content_type="application/json")
# 			if request.POST.get('size_set_but'):
# 				size=request.POST.get('size')
# 				comment=request.POST.get('comment')
# 				kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
# 				to_get=POM.objects.filter(
# 					product_Category=kjl.product_Category,
# 					product_Subcategory=kjl.product_Subcategory,
# 					product_Supercategory=kjl.product_Supercategory)
# 				kj=measurement.objects.filter(
# 					season=kjl.season,
# 					product_Supercategory=kjl.product_Supercategory,
# 					user=kjl.fashion_Brand).first()
# 				color=request.POST.get('color')
# 				color=color_model.objects.filter(name=color).first()
# 				addre=request.POST.get('addre')
# 				addre=address_model.objects.filter(id=int(addre)).first()
# 				ouj=quantity_b2b.objects.filter(
# 					order=kjl,
# 					size=kj,
# 					size_label=int(size),
# 					color=color,
# 					address=addre)
# 				if ouj.count()>0:
# 					ouj=ouj.first()
# 					ouj.quantity=ouj.quantity+1
# 					ouj.save()
# 				else:
# 					quantity_order_obj=quantity_b2b(
# 						order=kjl,
# 						size=kj,
# 						size_label=int(size),
# 						quantity=1,
# 						color=color,
# 						address=addre)
# 					quantity_order_obj.save()
# 				to_del=detail.objects.filter(email=request.user.email).first()
# 				to_del.delete()
# 				to_del=User.objects.filter(email=request.user.email).first()
# 				to_del.delete()
# 				return redirect('/userdetail/logout')
#
#
#
#
#
#
# 			if request.POST.get('brand'):
# 				obj=detail.objects.filter(id=int(request.POST.get('brand'))).first()
# 				obj1=labels.objects.get(slug=request.POST.get('label'))
# 				obj2=fits.objects.get(slug=request.POST.get('fit'))
# 				obj3=seasons.objects.get(slug=request.POST.get('season'))
# 				size_by_brand=int(request.POST.get('size'))
# 				kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
# 				meas_obj_usr1=measurement.objects.filter(
# 					season=obj3,
# 					product_Supercategory=kjl.product_Supercategory,
# 					user=obj).first()
# 				meas_obj_usr2=measurement.objects.filter(
# 					season=kjl.season,
# 					product_Supercategory=kjl.product_Supercategory,
# 					user=kjl.fashion_Brand).first()
# 				size_usr1=int(meas_obj_usr1.name)
# 				if size_by_brand>size_usr1:
# 					times=int(size_by_brand - size_usr1)
# 					usr1_attri1=meas_obj_usr1.attribute1 + int(meas_obj_usr1.grading1 * times)
# 				elif size_by_brand<size_usr1:
# 					times=int(size_usr1 - size_by_brand)
# 					usr1_attri1=meas_obj_usr1.attribute1 - int(meas_obj_usr1.grading1 * times)
# 				else:
# 					usr1_attri1=meas_obj_usr1.attribute1
# 				size=int(usr1_attri1)
# 				size1=int(meas_obj_usr2.attribute1)
# 				kj=meas_obj_usr2
#
#
# 				if size>size1:
# 					times=(size-size1)/int(kj.grading1)
# 					final=int(kj.name)+times
# 				elif size1>size:
# 					times=(size+size1)/int(kj.grading1)
# 					final=int(kj.name)-times
# 				else:
# 					times=1
# 					final=int(kj.name)
# 				color=request.POST.get('color')
# 				color=color_model.objects.filter(name=color).first()
# 				addre=request.POST.get('addre')
# 				addre=address_model.objects.filter(id=int(addre)).first()
# 				ouj=quantity_b2b.objects.filter(
# 					order=kjl,
# 					size=kj,
# 					size_label=final,
# 					color=color,
# 					address=addre)
# 				if ouj.count()>0:
# 					ouj=ouj.first()
# 					ouj.quantity=ouj.quantity+1
# 					ouj.save()
# 				else:
# 					quantity_order_obj=quantity_b2b(
# 						order=kjl,
# 						size=kj,
# 						size_label=abs(final),
# 						quantity=1,
# 					color=color,
# 					address=addre)
# 					quantity_order_obj.save()
#
#
#
#
#
#
# 				to_del=detail.objects.filter(email=request.user.email).first()
# 				to_del.delete()
# 				to_del=User.objects.filter(email=request.user.email).first()
# 				to_del.delete()
# 				return redirect('/userdetail/logout')
# 			if request.POST.get('placeorder_ajax_season'):
# 				ook=seasons.objects.get(slug=request.POST.get('placeorder_ajax_season'))
# 				ook1=detail.objects.get(id=request.POST.get('placeorder_ajax_season_brand'))
# 				ook2=company_Order.objects.get(order_no=user.b2b_order_no).product_Supercategory
# 				objh=measurement.objects.filter(season=ook,user=ook1,product_Supercategory=ook2)
# 				if objh.count()>0:
# 					bol=True
# 				else:
# 					bol=False
# 				objh=list(objh.values())
# 				return HttpResponse(json.dumps({'data': objh,'bol':bol}), content_type="application/json")
#
# 			data_set={
# 			"brand":brands,
# 			"pom":pom,
# 			"user":user,
# 			"color":kjl.colors_avail.all(),
# 			"addr":kjl.dispatch_Address.all()
# 			}
# 			return render(request,'b2b/order_update.html',data_set)
# 	return redirect('/userdetail/login')










def confirm_alteration(request):
    if request.user.is_authenticated:
        user=detail.objects.filter(email=request.user.email).first()
        if user.b2b_order:
            asd=assortment.objects.filter(user=user.email).first()
            kjl=company_Order.objects.filter(order_no=user.b2b_order_no).first()
            to_get=POM.objects.filter(
                product_Category=kjl.product_Category,
                product_Subcategory=kjl.product_Subcategory,
                product_Supercategory=kjl.product_Supercategory)
            kj=measurement.objects.filter(
                season=kjl.season,
                product_Supercategory=kjl.product_Supercategory,
                user=kjl.fashion_Brand).first()
            to_get=list(to_get.values())
            data={
            "asd":asd,
            "kjl":to_get,
            "kj":kj,
            'ab1':asd.attribute1,
            'db1':asd.deviation1,
            'fd1':asd.attribute1+asd.deviation1,
            'ab2':asd.attribute2,
            'db2':asd.deviation2,
            'fd2':asd.attribute1+asd.deviation2,
            'ab3':asd.attribute3,
            'db3':asd.deviation3,
            'fd3':asd.attribute1+asd.deviation3,
            'ab4':asd.attribute4,
            'db4':asd.deviation4,
            'fd4':asd.attribute1+asd.deviation4,
            'ab5':asd.attribute5,
            'db5':asd.deviation5,
            'fd5':asd.attribute1+asd.deviation5,
            'ab6':asd.attribute6,
            'db6':asd.deviation6,
            'fd6':asd.attribute1+asd.deviation6,
            'ab7':asd.attribute7,
            'db7':asd.deviation7,
            'fd7':asd.attribute1+asd.deviation7,
            'ab8':asd.attribute8,
            'db8':asd.deviation8,
            'fd8':asd.attribute1+asd.deviation8,
            'ab9':asd.attribute9,
            'db9':asd.deviation9,
            'fd9':asd.attribute1+asd.deviation9,
            'ab10':asd.attribute10,
            'db10':asd.deviation10,
            'fd10':asd.attribute1+asd.deviation10,
            'ab11':asd.attribute11,
            'db11':asd.deviation11,
            'fd11':asd.attribute1+asd.deviation11,
            'ab12':asd.attribute12,
            'db12':asd.deviation12,
            'fd12':asd.attribute1+asd.deviation12,
            'ab13':asd.attribute13,
            'db13':asd.deviation13,
            'fd13':asd.attribute1+asd.deviation13,
            'ab14':asd.attribute14,
            'db14':asd.deviation14,
            'fd14':asd.attribute1+asd.deviation14,
            'ab15':asd.attribute15,
            'db15':asd.deviation15,
            'fd15':asd.attribute1+asd.deviation15,
            'ab16':asd.attribute16,
            'db16':asd.deviation16,
            'fd16':asd.attribute1+asd.deviation16,
            'ab17':asd.attribute17,
            'db17':asd.deviation17,
            'fd17':asd.attribute1+asd.deviation17,
            'ab18':asd.attribute18,
            'db18':asd.deviation18,
            'fd18':asd.attribute1+asd.deviation18,
            'ab19':asd.attribute19,
            'db19':asd.deviation19,
            'fd19':asd.attribute1+asd.deviation19,
            'ab20':asd.attribute20,
            'db20':asd.deviation20,
            'fd20':asd.attribute1+asd.deviation20,
            'ab21':asd.attribute21,
            'db21':asd.deviation21,
            'fd21':asd.attribute1+asd.deviation21,
            'ab22':asd.attribute22,
            'db22':asd.deviation22,
            'fd22':asd.attribute1+asd.deviation22,
            'ab23':asd.attribute23,
            'db23':asd.deviation23,
            'fd23':asd.attribute1+asd.deviation23,
            'ab24':asd.attribute24,
            'db24':asd.deviation24,
            'fd24':asd.attribute1+asd.deviation24,
            'ab25':asd.attribute25,
            'db25':asd.deviation25,
            'fd25':asd.attribute1+asd.deviation25,
            'ab26':asd.attribute26,
            'db26':asd.deviation26,
            'fd26':asd.attribute1+asd.deviation26,
            'ab27':asd.attribute27,
            'db27':asd.deviation27,
            'fd27':asd.attribute1+asd.deviation27,
            'ab28':asd.attribute28,
            'db28':asd.deviation28,
            'fd28':asd.attribute1+asd.deviation28,
            'ab29':asd.attribute29,
            'db29':asd.deviation29,
            'fd29':asd.attribute1+asd.deviation29,
            'ab30':asd.attribute30,
            'db30':asd.deviation30,
            'fd30':asd.attribute1+asd.deviation30,
            'cost1':asd.alteration_Cost1,
            'cost2':asd.alteration_Cost2,
            'cost3':asd.alteration_Cost3,
            'cost4':asd.alteration_Cost4,
            'cost5':asd.alteration_Cost5,
            'cost6':asd.alteration_Cost6,
            'cost7':asd.alteration_Cost7,
            'cost8':asd.alteration_Cost8,
            'cost9':asd.alteration_Cost9,
            'cost10':asd.alteration_Cost10,
            'cost11':asd.alteration_Cost11,
            'cost12':asd.alteration_Cost12,
            'cost13':asd.alteration_Cost13,
            'cost14':asd.alteration_Cost14,
            'cost15':asd.alteration_Cost15,
            'cost16':asd.alteration_Cost16,
            'cost17':asd.alteration_Cost17,
            'cost18':asd.alteration_Cost18,
            'cost19':asd.alteration_Cost19,
            'cost20':asd.alteration_Cost20,
            'cost21':asd.alteration_Cost21,
            'cost22':asd.alteration_Cost22,
            'cost23':asd.alteration_Cost23,
            'cost24':asd.alteration_Cost24,
            'cost25':asd.alteration_Cost25,
            'cost26':asd.alteration_Cost26,
            'cost27':asd.alteration_Cost27,
            'cost28':asd.alteration_Cost28,
            'cost29':asd.alteration_Cost29,
            'cost30':asd.alteration_Cost30,
            'cos':asd.alteration_cost
            }


            if request.POST:
                if request.POST.get('with'):
                    asd.alteration_req=True
                    asd.save()
                if request.POST.get('without'):
                    asd.alteration_req=False
                    asd.save()
                to_del=detail.objects.filter(email=request.user.email).first()
                to_del.delete()
                to_del=User.objects.filter(email=request.user.email).first()
                to_del.delete()
                return redirect('/userdetail/logout')



            return render(request,'b2b/confirm_alteration.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')



from b2b.models import design_theme






def placedesign(request):
    sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
    brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
    cate=cat.objects.all()
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            if request.POST:
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

                target_lead_time=request.POST.get('target_lead_time')
                target_price=request.POST.get('target_price')
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
                des=int(request.POST.get('design_theme'))
                des=design_theme.objects.filter(id=des).first()
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
                        order_type='D',
                        target_lead_time=int(target_lead_time),
                        target_price=int(target_price),
                        tech_pack=tech_pack,
                        specs=specs,
                        logo_placement=logo_place,
                        description=description,
                        sizes=sizes,
                        colors=colors,
                        design_theme=des
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
                if dispatch:
                    ofd=address_model(
                        address=dispatch,
                        title="Location1"
                        )
                    ofd.save()
                    order.dispatch_Address.add(ofd)
                order.save()
                staff_cate=staff_Categories.objects.filter(name="Sales").first()

                objs1=detail.objects.filter(
                    staff=True,
                    staff_category=staff_cate,
                    position='H')
                order.save()
                for i in objs1:
                    order.staffs_Allocated.add(i)
                    noti_oj=notifications(
                        title="New Order Placed Please Add Manager to it("+str(order_n)+") !",
                        description="Add manager to it",
                        user=i,
                        link="/userdetail/staff_profile/orders/"+str(order_n),
                        type_of_order='D')
                    noti_oj.save()
                    noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
                    noti_oj.save()
                    acti_cate=activities_Category.objects.filter(
                        position='H',type_of_order='D',staff_category=staff_cate)

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
                        acti.planned_date=getPlannedDate(i,previous_date_to,lead_time)
                        # acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
                        acti.save()
                if order.excel:
                    data_read=csv.reader(open(BASE_DIR+order.excel.url[6:],"r"), delimiter=',', quotechar='"')
                    for row in data_read:
                        name=row[0]
                        email=row[1]
                        password="architkumar"
                        try:
                            obj=User.objects.create_user(username=email,email=email,password=password)
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
                                vendor_Timeline=False
                            )
                        obj.save()
                return redirect('/buisness/buisness_profile')
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
            data={"brand":brands,"cate":cate,"design":design_theme.objects.all(),"depend":None}
            if request.GET.get('order'):
                try:
                    su=int(request.GET.get('order'))
                except:
                    su=0
                data["depend"]=company_Order.objects.filter(order_no=su).first()
            return render(request,'b2b/placedesign.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')







def placesample(request):
    sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
    brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
    cate=cat.objects.all()
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            if request.POST:
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
                # quantity=request.POST.get('quantity')
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

                sample_type=request.POST.get('sample_type')
                sample_quantity=int(request.POST.get('sample_quantity'))
                order=company_Order(
                        fashion_Brand=brand,
                        label=label,
                        fit=fit,
                        season=season,
                        product_Category=category,
                        product_Subcategory=sub_cate,
                        product_Supercategory=super_cate,
                        image=sample,
                        excel=excel,
                        billing_Address=billing,
                        order_no=order_n,
                        user_email=request.user.email,
                        order_type='S',
                        target_lead_time=int(target_lead_time),
                        target_price=int(target_price),
                        tech_pack=tech_pack,
                        specs=specs,
                        logo_placement=logo_place,
                        description=description,
                        sizes=sizes,
                        colors=colors,
                        sample_type=sample_type,
                        sample_quantity=sample_quantity
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
                ofd=address_model(
                    address=dispatch,
                    title="Location1"
                    )
                ofd.save()
                order.dispatch_Address.add(ofd)
                order.save()
                staff_cate=staff_Categories.objects.filter(name="Sales").first()
                objs1=detail.objects.filter(
                    staff=True,
                    position='H',
                    staff_category=staff_cate)
                order.save()
                for i in objs1:
                    order.staffs_Allocated.add(i)
                    noti_oj=notifications(
                        title="New Order Placed Please Add Manager to it("+str(order_n)+") !",
                        description="Add manager to it",
                        user=i,
                        link="/userdetail/staff_profile/orders/"+str(order_n),
                        type_of_order='S')
                    noti_oj.save()
                    noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
                    noti_oj.save()
                    acti_cate=activities_Category.objects.filter(
                        position='H',type_of_order='S',staff_category=staff_cate)

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
                        acti.planned_date=getPlannedDate(i,previous_date_to,lead_time)
                        # acti.planned_date=previous_date_to+datetime.timedelta(days=lead_time)
                        acti.save()
                if order.excel:
                    data_read=csv.reader(open(BASE_DIR+order.excel.url[6:],"r"), delimiter=',', quotechar='"')

                    for row in data_read:
                        name=row[1]
                        email=row[2]
                        password=row[3]
                        max_quantity=int(row[4])
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
                                b2b_order_no=order_no,
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
                return redirect('/buisness/buisness_profile')
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
            return render(request,'b2b/placesample.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')





def placeenquiry(request):
    sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
    brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
    cate=cat.objects.all()
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            if request.POST:
                brand=request.POST.get('brand')
                brand=detail.objects.get(id=brand)
                fit=season=None
                label=request.POST.get('label')
                label=labels.objects.get(slug=label)
                # fit=request.POST.get('fit')
                # fit=fits.objects.get(slug=fit)
                # season=request.POST.get('season')
                # season=seasons.objects.get(slug=season)
                category=request.POST.get('category')
                category=cat.objects.get(name=category)
                sub_cate=request.POST.get('sub_category')
                sub_cate=sub_category.objects.get(name=sub_cate,product_Category=category)
                super_cate=request.POST.get('super_category')
                super_cate=super_category.objects.get(name=super_cate,product_Subcategory=sub_cate)
                quantity=request.POST.get('quantity')
                # dispatch=request.POST.get('dispatch')
                # billing=request.POST.get('billing')
                dispatch=billing=None
                sample=request.FILES.get('sample')
                # excel=request.FILES.get('excel')
                excel=None
                allorder=company_Order.objects.all().order_by('-order_no')
                if allorder.count()>0:
                    order_n=allorder.first().order_no+1
                else:
                    x=str(datetime.datetime.now().year)
                    order_n=int(x+"000001")
                if quantity is None:
                    quantity=0
                target_lead_time=request.POST.get('target_lead_time')
                target_price=request.POST.get('target_price')
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
                        quantity=int(quantity),
                        image=sample,
                        excel=excel,
                        billing_Address=billing,
                        order_no=order_n,
                        user_email=request.user.email,
                        order_type='E',
                        target_lead_time=int(target_lead_time),
                        target_price=int(target_price),
                        tech_pack=tech_pack,
                        specs=specs,
                        logo_placement=logo_place,
                        description=description,
                        sizes=sizes,
                        colors=colors
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
                staff_cate=staff_Categories.objects.filter(name="Sales").first()
                objs1=detail.objects.filter(
                    staff=True,
                    position='H',
                    staff_category=staff_cate)
                order.save()
                for i in objs1:
                    order.staffs_Allocated.add(i)
                    noti_oj=notifications(
                        title="New Order Placed Please Add Manager to it("+str(order_n)+") !",
                        description="Add manager to it",
                        user=i,
                        link="/userdetail/staff_profile/orders/"+str(order_n),
                        type_of_order='E')
                    noti_oj.save()
                    noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
                    noti_oj.save()
                    acti_cate=activities_Category.objects.filter(
                        position='H',type_of_order='E',staff_category=staff_cate).order_by('sequence')

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
                if order.excel:
                    data_read=csv.reader(open(BASE_DIR+order.excel.url[6:],"r"), delimiter=',', quotechar='"')
                    for row in data_read:
                        name=row[0]
                        email=row[1]
                        password="architkumar"
                        try:
                            obj=User.objects.create_user(username=email,email=email,password=password)
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
                                vendor_Timeline=False
                            )
                        obj.save()
                return redirect('/buisness/buisness_profile')
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
            return render(request,'b2b/placeenquiry.html',{"brand":brands,"cate":cate})
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')











def sampling(request,order_no):
    brands=detail.objects.filter(activate_Seller=True)
    cate=cat.objects.all()
    if request.POST:
        quantity=request.POST.get('quantity')
        dispatch=request.POST.get('dispatch')
        billing=request.POST.get('billing')
        sample=request.FILES.get('sample')
        excel=request.FILES.get('excel')
        sample_type=request.POST.get('sample_type')
        sample_quantity=int(request.POST.get('sample_quantity'))
        order=company_Order.objects.filter(order_no=order_no).first()
        # order.quantity=quantity
        order.billing=billing
        order.image=sample
        order.excel=excel
        order.order_type='S'
        order.sample_type=sample_type
        order.sample_quantity=sample_quantity
        order.save()

        ofd=address_model(
            address=dispatch,
            title="Location1"
            )
        ofd.save()
        order.dispatch_Address.add(ofd)
        order.save()
        if excel:
            data_read=csv.reader(open(BASE_DIR+order.excel.url[6:],"r"), delimiter=',', quotechar='"')

            for row in data_read:
                name=row[1]
                email=row[2]
                password=row[3]
                max_quantity=int(row[4])
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
                        b2b_order_no=order_no,
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
        return redirect('/buisness/buisness_profile')
    return render(request,'b2b/sampling.html',{"brand":brands,"cate":cate})









def ordering(request,order_no):
    brands=detail.objects.filter(activate_Seller=True)
    cate=cat.objects.all()
    order=company_Order.objects.filter(order_no=order_no).first()
    order.order_type='O'
    order.save()
    return redirect('/buisness/buisness_profile')





def design(request,order_no):
    brands=detail.objects.filter(activate_Seller=True)
    cate=cat.objects.all()
    order=company_Order.objects.filter(order_no=order_no).first()
    order.order_type='D'
    order.save()
    return redirect('/buisness/buisness_profile')








def buisness_profile_staff(request,email):
    data={}
    if request.user.is_authenticated:

        us=detail.objects.filter(email=request.user.email).first()
        us1=staff_Categories.objects.filter(name="Sales").first()
        if (us.staff and us.staff_category==us1) or us.vendor:
            user=company_detail.objects.filter(email=email)
            user1=detail.objects.filter(email=email).first()
            orders=company_Order.objects.filter(user_email=email,order_type='O')
            sample=company_Order.objects.filter(user_email=email,order_type='S')
            design=company_Order.objects.filter(user_email=email,order_type='D')
            enquiry=company_Order.objects.filter(user_email=email,order_type='E')
            # print(orders)
            if user.count()>0:
                user=user.first()
                data={
                    "name":user.name,
                    "desc":user.company_Description,
                    "mission":user.company_Mission,
                    "gstin":user.gstin,
                    "logo_img":user.logo,
                    "email":user.email,
                    "order_bool":False,
                    "orders":orders,
                    "sample":sample,
                    "enquiry":enquiry,
                    "design":design,
                    "sample_bool":False,
                    "enquiry_bool":False,
                    "design_bool":False,
                    "activate":not(user1.activate_Buisness)
                }
                if orders.count()>0:
                    data["order_bool"]=True
                if sample.count()>0:
                    data["sample_bool"]=True
                if enquiry.count()>0:
                    data["enquiry_bool"]=True
                if design.count()>0:
                    data["design_bool"]=True
                if request.POST:
                    if request.POST.get("activate")=="on":
                        user1.activate_Buisness=True
                    user1.save()
                    return redirect('/userdetail/staff_profile')
            else:
                return redirect('/userdetail/login')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')
    return render(request,'b2b/buisness_profile_staff.html',data)








def buisness_profile_notifications(request):
    if request.GET.get('noti'):
        noti=int(request.GET.get('noti'))
        ogh=notifications.objects.filter(id=noti).first()
        if ogh:
            ogh.seen=True
            ogh.save()
    # print(request.user.email)
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        # print(details.buisness_Customer)
        if details.buisness_Customer:
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
            return render(request,"b2b/buisness_notifications.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')




from b2b.models import consumer_Order_Quantity,assortment



def consumer_profile(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.b2b_order:
            order=consumer_Order_Quantity.objects.filter(user=details)
            orders=[]
            for i in order:
                orders.append(i.order)
            print(orders)
            assort_orders=[]
            order_assort=assortment.objects.filter(user=details.email)
            for i in order_assort:
                if i.order_no in orders:
                    orders.remove(i.order_no)
            products=company_Order.objects.filter(~Q(left_over=0),availiable_for_consumers=True)[:4]
            data={
                "orders":orders,
                "order_assort":order_assort,
                "details":details,
                "products":products
            }
            if request.POST.get('name'):
                details.name=request.POST.get('name')
                details.reg_no=request.POST.get('reg_no')
                details.dept=request.POST.get('dept')
                details.sub_dept=request.POST.get('sub_dept')
                details.save()
                return redirect('/buisness/consumer_profile')
            return render(request,"b2b/consumer_profile.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')




from copy import deepcopy

def consumer_list(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=order_no).first()
        if details.buisness_Customer and order:
            consumers=consumer_Order_Quantity.objects.filter(order=order)
            consumers_li=[]
            for i in consumers:
                obj=assortment.objects.filter(user=i.user.email,order_no=order).first()
                consumers_li.append([i,obj])
            gender_avail=[]
            department_avail=[]
            sub_dept_avail=[]
            for i in consumers_li:
                if i[0].user.gender not in gender_avail:
                    gender_avail.append(i[0].user.gender)
                if i[0].user.dept not in department_avail:
                    department_avail.append(i[0].user.dept)
                if i[0].user.sub_dept not in sub_dept_avail:
                    sub_dept_avail.append(i[0].user.sub_dept)
            data={
                "order":order,
                "details":details,
                "consumers_li":consumers_li,
                "gender_avail":gender_avail,
                "department_avail":department_avail,
                "sub_dept_avail":sub_dept_avail
            }
            if request.GET:
                if request.GET.get('email'):
                    email=request.GET.get('email')
                    c=deepcopy(consumers_li)
                    for i in consumers_li:
                        if email not in i[0].user.email:
                            c.remove(i)
                    conusmers_li=deepcopy(c)
                if request.GET.get('send_email'):
                    email=request.GET.get('send_email')
                    user_to_send=detail.objects.filter(email=email).first()
                    if user_to_send:
                        authentic=check_email_correctness(email)
                        if authentic:
                            subject="Login Details !"
                            message="Hello "+str(user_to_send.name)+"\n\n\nHeartlist Congratulations for getting shortlisted for assortment.\n\n\nHere is your Login Details \n\nUsername - "+str(user_to_send.email)+"\nPassword - "+str(user_to_send.password)+"\n\nPlease login and submit your assortment\nhttp://raymondinstitutional.justgetit.in/userdetail/login\n\nThanks & Regards\nRaymond Institutional Team"
                            from_email=EMAIL_HOST_USER
                            to_list=[str(user_to_send.email)]
                            # to_list=['dwevediar@gmail.com']
                            send_email(subject,message,from_email,to_list)
                if request.GET.get('gender'):
                    gender=request.GET.get('gender')
                    c=deepcopy(consumers_li)
                    for i in consumers_li:
                        if gender!=i[0].user.gender:
                            c.remove(i)
                    consumers_li=deepcopy(c)
                if request.GET.get('dept'):
                    dept=request.GET.get('dept')
                    c=deepcopy(consumers_li)
                    for i in consumers_li:
                        if dept!=i[0].user.dept:
                            c.remove(i)
                    consumers_li=deepcopy(c)
                if request.GET.get('sub_dept'):
                    sub_dept=request.GET.get('sub_dept')
                    c=deepcopy(consumers_li)
                    for i in consumers_li:
                        if sub_dept!=i[0].user.sub_dept:
                            c.remove(i)
                    consumers_li=deepcopy(c)
                if request.GET.get('max_quantity'):
                    max_quantity=request.GET.get('max_quantity')
                    c=deepcopy(consumers_li)
                    for i in consumers_li:
                        if max_quantity!=i[0].max_quantity:
                            c.remove(i)
                    consumers_li=deepcopy(c)
                if request.GET.get('size'):
                    size=int(request.GET.get('size'))
                    c=deepcopy(consumers_li)
                    for i in consumers_li:
                        if i[1]:
                            if size!=i[1].size_label:
                                c.remove(i)
                        else:
                            c.remove(i)
                    consumers_li=deepcopy(c)
                if request.GET.get('login_details'):
                    for i in consumers_li:
                        authentic=check_email_correctness(i[0].user.email)
                        if authentic:
                            subject="Login Details !"
                            message="Hello "+str(i[0].user.name)+"\n\n\nHeartlist Congratulations for getting shortlisted for assortment.\n\n\nHere is your Login Details \n\nUsername - "+str(i[0].user.email)+"\nPassword - "+str(i[0].user.password)+"\n\nPlease login and submit your assortment\nhttp://raymondinstitutional.justgetit.in/userdetail/login\n\nThanks & Regards\nRaymond Institutional Team"
                            from_email=EMAIL_HOST_USER
                            to_list=[str(i[0].user.email)]
                            send_email(subject,message,from_email,to_list)
                    return redirect('/buisness/buisness_profile')
                data["consumers_li"]=consumers_li
            return render(request,"b2b/consumer_list.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')



def consumer_detail(request,order_no,consumer_email):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=order_no).first()
        consumer=detail.objects.filter(email=consumer_email).first()
        consumer_quan=consumer_Order_Quantity.objects.filter(order=order,user=consumer).first()
        if details.buisness_Customer and consumer_quan:
            assortment_obj=assortment.objects.filter(user=consumer_email,order_no=order).first()
            data={
                "order":order,
                "details":details,
                "consumer":consumer,
                "consumer_quan":consumer_quan,
                "assortment_obj":assortment_obj
            }

            if request.POST.get('name'):
                name=request.POST.get('name')
                dept=request.POST.get('dept')
                sub_dept=request.POST.get('sub_dept')
                gender=request.POST.get('gender')
                max_quantity=request.POST.get('max_quantity')
                size=request.POST.get('size')
                color=request.POST.get('color')
                if color:
                    color=int(color)
                    color=color_model.objects.filter(id=color).first()
                address=request.POST.get('address')
                if address:
                    address=int(address)
                    address=address_model.objects.filter(id=address).first()
                quantity=request.POST.get('quantity')
                if quantity:
                    quantity=int(quantity)
                consumer.name=name
                consumer.dept=dept
                consumer.sub_dept=sub_dept
                consumer.gender=gender
                if max_quantity:
                    max_quantity=int(max_quantity)
                    consumer_quan.max_quantity=max_quantity
                consumer.save()
                consumer_quan.save()
                if size:
                    if assortment_obj:
                        quantity_obj=quantity_b2b.objects.filter(order=order,size_label=assortment_obj.size_label,production=False,color=color,address=address).first()
                        if quantity_obj:
                            quantity_obj.quantity-=assortment_obj.quantity
                            quantity_obj.save()
                        assortment_obj.size_label=int(size)
                        assortment_obj.quantity=quantity
                        assortment_obj.save()
                        quantity_obj=quantity_b2b.objects.filter(order=order,size_label=assortment_obj.size_label,production=False,color=color,address=address).first()
                        if quantity_obj:
                            quantity_obj.quantity+=quantity
                            quantity_obj.save()
                        else:
                            quantity_obj=quantity_b2b(
                                order=order,
                                size_label=int(size),
                                quantity=quantity,
                                color=color,
                                address=address
                            )
                            quantity_obj.save()
                    else:
                        assortment_obj=assortment(user=consumer.email,
                                        user_name=consumer.name,
                                        order_no=order,
                                        size_label=int(size),
                                        quantity=quantity,
                                        color=color,address=address
                                        )
                        assortment_obj.save()
                        quantity_obj=quantity_b2b.objects.filter(order=order,size_label=int(size),production=False,color=color,address=address).first()
                        if quantity_obj:
                            quantity_obj.quantity+=quantity
                            quantity_obj.save()
                        else:
                            quantity_obj=quantity_b2b(
                                order=order,
                                size_label=int(size),
                                quantity=quantity,
                                color=color,
                                address=address
                            )
                            quantity_obj.save()
                # return redirect('/buisness/buisness_order/'+str(order.order_no)+'/consumer_list')
                ouj1=assortment.objects.filter(user=consumer_email,order_no=order).first()
                print(request.POST.get('distributed'))
                if request.POST.get('distributed') and ouj1 and not(ouj1.distributed):
                    ouj1.distributed=True
                    ouj1.save()
                    print("Done")
                    distri_obj=distribution_list.objects.filter(address=ouj1.address,order=order).first()
                    if not(distri_obj):
                        distri_obj=distribution_list(address=ouj1.address,order=order,name="Default")
                    size=int(ouj1.size_label)
                    if size==24:
                        distri_obj.quantity_24+=ouj1.quantity
                    elif size==26:
                        distri_obj.quantity_26+=ouj1.quantity
                    elif size==28:
                        distri_obj.quantity_28+=ouj1.quantity
                    elif size==30:
                        distri_obj.quantity_30+=ouj1.quantity
                    elif size==32:
                        distri_obj.quantity_32+=ouj1.quantity
                    elif size==34:
                        distri_obj.quantity_34+=ouj1.quantity
                    elif size==36:
                        distri_obj.quantity_36+=ouj1.quantity
                    elif size==38:
                        distri_obj.quantity_38+=ouj1.quantity
                    elif size==40:
                        distri_obj.quantity_40+=ouj1.quantity
                    elif size==42:
                        distri_obj.quantity_42+=ouj1.quantity
                    elif size==44:
                        distri_obj.quantity_44+=ouj1.quantity
                    elif size==46:
                        distri_obj.quantity_46+=ouj1.quantity
                    elif size==48:
                        distri_obj.quantity_48+=ouj1.quantity
                    elif size==50:
                        distri_obj.quantity_50+=ouj1.quantity
                    elif size==52:
                        distri_obj.quantity_52+=ouj1.quantity
                    distri_obj.save()
                # to_del=detail.objects.filter(email=request.user.email).first()
                # to_del.delete()
                # to_del=User.objects.filter(email=request.user.email).first()
                # to_del.delete()
                return redirect('/buisness/buisness_order/'+str(order.order_no)+'/consumer_list')

                # return redirect('/userdetail/logout')
            return render(request,"b2b/consumer_detail.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')




def consumer_request(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.b2b_order:
            data={
                "details":details,
                "invalid":False
            }
            if request.POST.get('order'):
                order_no=int(request.POST.get('order'))
                org_email=request.POST.get('org_email')
                order_password=request.POST.get('order_password')
                obj=company_Order.objects.filter(order_no=order_no,user_email=org_email,order_password=order_password).first()
                if obj:
                    consu_obj=consumer_Order_Quantity(user=details,order=obj,max_quantity=obj.max_quantity_per_consumer)
                    consu_obj.save()
                    obj.order_password=generateOTP()
                    obj.save()
                    return redirect('/buisness/consumer_profile')
                else:
                    data["invalid"]=True
            return render(request,"b2b/consumer_request.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')








def excel_settings(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            objs=coloums.objects.filter(user=details)
            if objs.count()<7 or request.GET.get('r'):
                for i in objs:
                    i.delete()
                kl=coloums(user=details,email=True,coloumn_no=2,coloum_name="Email")
                kl.save()
                kl=coloums(user=details,contact=True,coloumn_no=3,coloum_name="Contact")
                kl.save()
                kl=coloums(user=details,gender=True,coloumn_no=4,coloum_name="Gender")
                kl.save()
                kl=coloums(user=details,reg_no=True,coloumn_no=5,coloum_name="Registration No")
                kl.save()
                kl=coloums(user=details,dept=True,coloumn_no=6,coloum_name="Department")
                kl.save()
                kl=coloums(user=details,sub_dept=True,coloumn_no=7,coloum_name="Sub-Department")
                kl.save()
                kl=coloums(user=details,name=True,coloumn_no=1,coloum_name="Name")
                kl.save()
            objs=coloums.objects.filter(user=details).order_by('coloumn_no')
            data={
                "details":details,
                "invalid":False,
                "objs":objs
            }
            if request.POST.get('settings_save'):
                for i in objs:
                    if request.POST.get('number'+str(i.id)):
                        i.coloumn_no=int(request.POST.get('number'+str(i.id)))
                        i.save()
                if request.POST.get('new_name1'):
                    name=request.POST.get('new_name1')
                    num=request.POST.get('new_num1')
                    objkl=coloums(user=details,coloum_name=name,coloumn_no=num)
                    objkl.save()
                if request.POST.get('new_name2'):
                    name=request.POST.get('new_name2')
                    num=request.POST.get('new_num2')
                    objkl=coloums(user=details,coloum_name=name,coloumn_no=num)
                    objkl.save()
                if request.POST.get('new_name3'):
                    name=request.POST.get('new_name3')
                    num=request.POST.get('new_num3')
                    objkl=coloums(user=details,coloum_name=name,coloumn_no=num)
                    objkl.save()
                return redirect('/buisness/buisness_profile')
            return render(request,"b2b/excel_settings.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')






def buisness_packing_list(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=order_no,user_email=request.user.email).first()
        if details.buisness_Customer and order:
            # order=company_Order.objects.filter(order_no=order_no).first()
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
                             left_over.append([q.address,to_size,q.size_label])
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
                         cur=cur+carton_max
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
            return render(request,"b2b/buisness_packing_list.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')




def buisness_distribution_list(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=order_no,user_email=request.user.email).first()
        if details.buisness_Customer and order:
            # order=company_Order.objects.filter(order_no=order_no).first()
            distri_obj=distribution_list.objects.filter(order=order)
            if distri_obj:
                pass
            addr=order.dispatch_Address.all()
            s=0
            for i in distri_obj:
                s+=i.total_quantity
            left_over=order.quantity - s
            order.left_over=left_over
            order.save()
            data={
                "distri_obj":distri_obj,
                "order":order,
                "address":addr,
                "left_over":left_over,
                "s":s
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

            if request.POST.get('consumers'):
                order.availiable_for_consumers=True
            if request.POST.get('availiable_b2b'):
                order.availiable_for_b2b=True
            order.save()
            return render(request,"b2b/buisness_distribution_list.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')




def buisness_cummlative_list(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=order_no,user_email=request.user.email).first()
        if details.buisness_Customer and order:
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
            return render(request,"b2b/buisness_cummlative_list.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')







def buisness_order_po(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                if not(tlt) or not(order.total_Price):
                    tlt=0
                    a=0
                    check=False
                if order.total_Price and order.quantity:
                    data={
                        'order':order,
                        'details':details,
                        'compan':compan,
                        'delivery':order.order_date_time + datetime.timedelta(days=tlt),
                        'total_cost':order.total_Price*order.quantity,
                        'total_cost_words':num2word(int(order.total_Price*order.quantity)),
                        'check':check
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/order_po.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')







def buisness_order_invoice(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                carton=packing_list.objects.filter(order=order).first().cartons.all()
                quan=0
                for i in carton:
                    quan+=i.total_quantity
                if not(tlt) or not(order.total_Price):
                    tlt=0
                    a=0
                    check=False
                if order.total_Price and order.quantity:
                    data={
                        'order':order,
                        'details':details,
                        'compan':compan,
                        'delivery':order.order_date_time + datetime.timedelta(days=tlt),
                        'total_cost':order.total_Price*quan,
                        'quan':quan,
                        'total_cost_words':num2word(int(order.total_Price*quan)),
                        'check':check,
                        'compan_det':compan_det
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/order_invoice.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')



from django.db.models import Q
from product.models import product


def buisness_products(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.buisness_Customer:
            orders=company_Order.objects.filter(~Q(left_over=0),availiable_for_b2b=True)
            ordio=product.objects.filter(seller=details)
            o=[]
            data={
                "orders":orders,
                "personal_products":ordio
            }
            return render(request,'b2b/buisness_products.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')



def buisness_products_detail(request,prod_id):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=prod_id).first()
        if details.buisness_Customer and order:
            # orders=company_Order.objects.filter(~Q(left_over=0),availiable_for_b2b=True)
            data={
                "order":order
            }
            return render(request,'b2b/buisness_products_detail.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')





def consumer_profile_products(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.b2b_order:
            orders=company_Order.objects.filter(~Q(left_over=0),availiable_for_b2b=True)
            data={
                "orders":orders
            }
            return render(request,'b2b/consumer_profile_products.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')



def consumer_profile_products_detail(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=order_no).first()
        if details.b2b_order and order:
            # orders=company_Order.objects.filter(~Q(left_over=0),availiable_for_b2b=True)
            data={
                "order":order
            }
            return render(request,'b2b/consumer_profile_products_detail.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')

from .models import custom_assortment_model


def custom_assortment(request,order_no):
    order=company_Order.objects.filter(order_no=order_no).first()
    if order:
        data={

        }
        if request.POST.get('name'):
            obj=custom_assortment_model(name=request.POST.get('name'),
                size=request.POST.get('size'),
                color=request.POST.get('color'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                order=order)
            obj.save()
            print(obj.name)
            return redirect('/')
        return render(request,"b2b/custom_assortment.html",data)
    else:
        return redirect('')


from b2b.models import bulk_order_upload as b_order


def bulk_order_upload(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details and details.buisness_Customer:
            last_uploaded=b_order.objects.filter(user=details).last()
            data={
                "details":details,
                "prev":last_uploaded
            }
            # data_read=csv.reader(open(BASE_DIR+order.excel.url[6:],"r"), delimiter=',', quotechar='"')
            if request.POST.get('p_c') and request.FILES.get('bulk_order'):
                obj=b_order(
                    user=details,
                    order_no=request.POST.get('order_no'),
                    product_Category=request.POST.get('p_c'),
                    product_Subcategory=request.POST.get('p_subc'),
                    product_Supercategory=request.POST.get('p_supc'),
                    label=request.POST.get('label'),
                    fit=request.POST.get('fit'),
                    season=request.POST.get('season'),
                    dispatch=request.POST.get('dispatch'),
                    billing=request.POST.get('billing'),
                    quantity=request.POST.get('quantity'),
                    target_lead=request.POST.get('target_lead'),
                    target_price=request.POST.get('target_price'),
                    colors=request.POST.get('colors'),
                    logo_placement=request.POST.get('logo_placement'),
                    max_quantity=request.POST.get('max_quantity'),
                    sales=request.POST.get('sales'),
                    merchandiser=request.POST.get('merchandiser'),
                    garment_vendor=request.POST.get('garment_vendor'),
                    other_fields=request.POST.get('other_fields'),
                    excel=request.FILES.get('bulk_order')
                )
                obj.save()
                data_read=csv.reader(open(BASE_DIR+obj.excel.url[6:],"r"), delimiter=',', quotechar='"')
                # first_row=data_read[0]
                # mapper={}
                # n=0
                # for i in first_row:
                # 	mapper[i]=n
                # 	n+=1
                # data_read=data_read[1:]
                kammal=0
                for row in data_read:
                    if kammal==0:
                        kammal+=1
                        first_row=row
                        mapper={}
                        n=0
                        for i in first_row:
                            mapper[i]=n
                            n+=1
                    else:
                        brand=detail.objects.get(id=192)
                        label=row[mapper[obj.label]]
                        label=labels.objects.get(name=label)
                        fit=row[mapper[obj.fit]]
                        fit=fits.objects.get(name=fit,label=label)
                        season=row[mapper[obj.season]]
                        season=seasons.objects.get(name=season,fit=fit)
                        category=row[mapper[obj.product_Category]]
                        category=cat.objects.get(name=category)
                        sub_cate=row[mapper[obj.product_Subcategory]]
                        sub_cate=sub_category.objects.get(name=sub_cate,product_Category=category)
                        super_cate=row[mapper[obj.product_Supercategory]]
                        super_cate=super_category.objects.get(name=super_cate,product_Subcategory=sub_cate)
                        quantity=row[mapper[obj.quantity]]
                        dispatch=row[mapper[obj.dispatch]]
                        billing=row[mapper[obj.billing]]
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
                        target_lead_time=row[mapper[obj.target_lead]]
                        target_price=row[mapper[obj.target_price]]
                        if not(target_lead_time):
                            target_lead_time=0
                        if not(target_price):
                            target_price=0
                        tech_pack=request.FILES.get('tech_pack')
                        description=''
                        specs=request.FILES.get('specs')
                        colors=row[mapper[obj.colors]]
                        sizes=request.POST.get('sizes')
                        logo_place=row[mapper[obj.logo_placement]]
                        max_quantity=row[mapper[obj.max_quantity]]
                        if max_quantity:
                            max_quantity=int(max_quantity)
                        else:
                            max_quantity=1000
                        if not(target_lead_time):
                            target_lead_time=0
                        if not(target_price):
                            target_price=0
                        otp=generateOTP()
                        other_fields=obj.other_fields
                        list_other_fields=list(other_fields.split(","))
                        f=''
                        for oth_field in list_other_fields:
                            if oth_field:
                                f+=str(row[mapper[oth_field]])+","
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
                                sizes=sizes,
                                max_quantity_per_consumer=max_quantity,
                                order_password=otp,
                                other_fields=other_fields,
                                other_fields_values=f
                            )
                        order.save()
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
                        other_users=[]
                        sales=detail.objects.filter(email=row[mapper[obj.sales]]).first()
                        merchandiser=detail.objects.filter(email=row[mapper[obj.merchandiser]]).first()
                        garment_vendor=detail.objects.filter(email=row[mapper[obj.garment_vendor]]).first()
                        if sales:
                            other_users.append(sales)
                            order.staffs_Allocated.add(sales)
                        if merchandiser:
                            other_users.append(merchandiser)
                            order.staffs_Allocated.add(merchandiser)
                        if garment_vendor:
                            other_users.append(garment_vendor)
                            order.staffs_Allocated.add(garment_vendor)
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
            return render(request,"b2b/bulk_order_upload.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')


from product.models import trims_product
from b2b.models import bulk_bom_upload, bom, trims_bom

def bulk_order_bom_upload(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details and details.buisness_Customer:
            data = {}
            if request.FILES.get('bulk_order_bom'):
                obj = bulk_bom_upload(user = details, csv_file = request.FILES.get('bulk_order_bom'))
                obj.save()
                data_read=csv.reader(open(BASE_DIR+obj.csv_file.url[6:],"r"), delimiter=',', quotechar='"')
                mapper = {}
                for row in data_read:
                    order = company_Order.objects.filter(order_no = row[0]).first()
                    # trim = trims_product.objects.filter(id = row[1]).first()
                    if order:
                        bom_obj = bom(
                                user= details,
                                order = order,
                                cutmake_consum = row[1],
                                cutmake_rate = row[2],
                                profit_percentage = row[3]
                            )
                        bom_obj.save()
                        count = (len(row)-4)//7
                        for col in range(4,(count*7)+5,7):
                            try:
                                trim = trims_product.objects.filter(id = row[col]).first()
                            except:
                                continue
                            if trim:
                                trims_bom_obj = trims_bom(
                                    trim = trim,
                                    order = order,
                                    uom = row[col+1],
                                    description = row[col+2],
                                    specification = row[col+3],
                                    consumption = row[col+4],
                                    wastage = row[col+5],
                                    rate = row[col+6]
                                )
                                trims_bom_obj.save()
                                bom_obj.trims_used.add(trims_bom_obj)
                                bom_obj.products.add(trim)
                                bom_obj.save()

                return redirect('/buisness/buisness_profile')
            return render(request, "b2b/bulk_order_bom_upload.html", data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')


def buisness_fabrics_id(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details and details.buisness_Customer:
            data = {
                "trims": trims_product.objects.all()
            }
            return render(request, "b2b/buisness_fabrics_id.html", data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')