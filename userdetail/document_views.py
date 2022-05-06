




from django.core import serializers
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model


from .models import detail
from b2b.models import company_Order,company_detail,bom
from .utils import render_to_pdf,num2word
import datetime

from product.models import trims_Category
from seller_info.models import trimcard_sections

from b2b.models import packing_list,cartons_list

from b2b.models import cartons_list,packing_list

from userdetail.utils import randomStringDigits
from b2b.models import production_order

def qr_generate(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no).first()
            if order:
                pack=packing_list.objects.filter(order=order).first()
                cartons_links=[]
                count=0
                for i in pack.cartons.all():
                    if not(i.carton_password):
                        i.carton_password=randomStringDigits(10)
                        i.save()
                    count+=1
                    link=""+str(order.order_no)+"_"+str(i.carton_password)
                    cartons_links.append(link)
                data={
                    "order":order,
                    "pack":pack,
                    "cartons_links":cartons_links
                }
                return render(request,"order_documents/qr_generate.html",data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')





def qr_view(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no).first()
            if order:
                if request.GET.get('size') and request.GET.get('carton'):
                    cnt=request.GET.get('carton')
                    siz=request.GET.get('size')
                    link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(cnt)+"&size="+str(siz)
                    data={
                        "link":link,
                        "order":order
                    }
                    return render(request,"order_documents/qr_view.html",data)
                elif request.GET.get('carton'):
                    count=request.GET.get('carton')
                    link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)
                    pack=packing_list.objects.filter(order=order).first()
                    carton_obj=None
                    coun=0
                    for i in pack.cartons.all():
                        coun+=1
                        if coun==int(count):
                            carton_obj=i
                            break
                    data={
                        "link":link,
                        "carton":carton_obj,
                        "order":order
                    }
                    return render(request,"order_documents/qr_view.html",data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')



def carton_update_status(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no).first()
            if order:
                if request.GET.get('size') and request.GET.get('carton'):
                    status="u"
                    count=request.GET.get('carton')
                    siz=request.GET.get('size')
                    pack=packing_list.objects.filter(order=order).first()
                    carton_obj=None
                    coun=0
                    for i in pack.cartons.all():
                        coun+=1
                        if coun==int(count):
                            carton_obj=i
                            break
                    if siz=="24":
                        act_quan=carton_obj.quantity_24_count
                        quan=carton_obj.quantity_24
                    elif siz=="26":
                        act_quan=carton_obj.quantity_26_count
                        quan=carton_obj.quantity_26
                    elif siz=="28":
                        act_quan=carton_obj.quantity_28_count
                        quan=carton_obj.quantity_28
                    elif siz=="30":
                        act_quan=carton_obj.quantity_30_count
                        quan=carton_obj.quantity_30
                    elif siz=="32":
                        act_quan=carton_obj.quantity_32_count
                        quan=carton_obj.quantity_32
                    elif siz=="34":
                        act_quan=carton_obj.quantity_34_count
                        quan=carton_obj.quantity_34
                    elif siz=="36":
                        act_quan=carton_obj.quantity_36_count
                        quan=carton_obj.quantity_36
                    elif siz=="38":
                        act_quan=carton_obj.quantity_38_count
                        quan=carton_obj.quantity_38
                    elif siz=="40":
                        act_quan=carton_obj.quantity_40_count
                        quan=carton_obj.quantity_40
                    elif siz=="42":
                        act_quan=carton_obj.quantity_42_count
                        quan=carton_obj.quantity_42
                    elif siz=="44":
                        act_quan=carton_obj.quantity_44_count
                        quan=carton_obj.quantity_44
                    elif siz=="46":
                        act_quan=carton_obj.quantity_46_count
                        quan=carton_obj.quantity_46
                    elif siz=="48":
                        act_quan=carton_obj.quantity_48_count
                        quan=carton_obj.quantity_48
                    elif siz=="50":
                        act_quan=carton_obj.quantity_50_count
                        quan=carton_obj.quantity_50
                    elif siz=="50":
                        act_quan=carton_obj.quantity_50_count
                        quan=carton_obj.quantity_50
                    if not(quan):
                        quan=0
                    if not(act_quan):
                        act_quan=0
                    if act_quan>=quan:
                        status="p"
                    data={
                        "status":status,
                        "order":order,
                        "carton":carton_obj
                    }
                    if request.POST.get('status')=="p":
                        carton_obj.packing_count+=1
                        if siz=="24":
                            carton_obj.quantity_24_count+=1
                        elif siz=="26":
                            carton_obj.quantity_26_count+=1
                        elif siz=="28":
                            carton_obj.quantity_28_count+=1
                        elif siz=="30":
                            carton_obj.quantity_30_count+=1
                        elif siz=="32":
                            carton_obj.quantity_32_count+=1
                        elif siz=="34":
                            carton_obj.quantity_34_count+=1
                        elif siz=="36":
                            carton_obj.quantity_36_count+=1
                        elif siz=="38":
                            carton_obj.quantity_38_count+=1
                        elif siz=="40":
                            carton_obj.quantity_40_count+=1
                        elif siz=="42":
                            carton_obj.quantity_42_count+=1
                        elif siz=="44":
                            carton_obj.quantity_44_count+=1
                        elif siz=="46":
                            carton_obj.quantity_46_count+=1
                        elif siz=="48":
                            carton_obj.quantity_48_count+=1
                        elif siz=="50":
                            carton_obj.quantity_50_count+=1
                        elif siz=="52":
                            carton_obj.quantity_52_count+=1
                        carton_obj.save()
                        return redirect('/userdetail/staff_profile')
                    return render(request,"order_documents/update_status.html",data)
                elif request.GET.get('carton'):
                    count=request.GET.get('carton')
                    pack=packing_list.objects.filter(order=order).first()
                    carton_obj=None
                    coun=0
                    for i in pack.cartons.all():
                        coun+=1
                        if coun==int(count):
                            carton_obj=i
                            break
                    status=carton_obj.status
                    data={
                        "status":status,
                        "order":order,
                        "carton":carton_obj
                    }
                    if request.POST.get('status'):
                        carton_obj.status=request.POST.get('status')
                        carton_obj.save()
                        return redirect('/userdetail/staff_profile')
                    return render(request,"order_documents/update_status.html",data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        next_url="userdetail/staff_profile/orders/"+str(order_no)+"/update_status?carton="+str(request.GET.get('carton'))
        if request.GET.get('size'):
            next_url=next_url+"&size="+request.GET.get("size")
        return redirect("/userdetail/login?next="+next_url)




def carton_details(request,order_no,carton_count):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no).first()
            if order:
                count=carton_count
                pack=packing_list.objects.filter(order=order).first()
                carton_obj=None
                coun=0
                for i in pack.cartons.all():
                    coun+=1
                    if coun==int(count):
                        carton_obj=i
                        break
                links=[]
                if carton_obj:
                    if not(carton_obj.carton_password):
                        carton_obj.carton_password=randomStringDigits(10)
                        carton_obj.save()
                if carton_obj.quantity_24:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_24"
                    links.append([link,24])
                if carton_obj.quantity_26:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_26"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=26"
                    links.append([link,26])
                if carton_obj.quantity_28:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_28"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=28"
                    links.append([link,28])
                if carton_obj.quantity_30:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_30"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=30"
                    links.append([link,30])
                if carton_obj.quantity_32:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_32"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=32"
                    links.append([link,32])
                if carton_obj.quantity_34:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_34"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=34"
                    links.append([link,34])
                if carton_obj.quantity_36:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_36"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=36"
                    links.append([link,36])
                if carton_obj.quantity_38:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_38"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=38"
                    links.append([link,38])
                if carton_obj.quantity_40:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_40"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=40"
                    links.append([link,40])
                if carton_obj.quantity_42:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_42"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=42"
                    links.append([link,42])
                if carton_obj.quantity_44:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_44"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=44"
                    links.append([link,44])
                if carton_obj.quantity_46:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_46"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=46"
                    links.append([link,46])
                if carton_obj.quantity_48:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_48"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=48"
                    links.append([link,48])
                if carton_obj.quantity_50:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_50"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=50"
                    links.append([link,50])
                if carton_obj.quantity_52:
                    link=""+str(order.order_no)+"_"+str(carton_obj.carton_password)+"_52"
                    # link="http://raymondinstitutional.justgetit.in/userdetail/staff_profile/orders/"+str(order.order_no)+"/update_status?carton="+str(count)+"&size=52"
                    links.append([link,52])

                print(links)
                data={
                    "link":links,
                    "carton":carton_obj,
                    "order":order,
                    "count":count
                }
                return render(request,"order_documents/carton_details.html",data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')

from b2b.models import order_status,list_types,size_status,Carton_new,new_pl,distribution_list_1,warehouse_list,dispatch_list,logistic_list
from django.http import JsonResponse
from movintrendz.views import decode
from b2b.models import address_model,color_model,size_color_quantity
import datetime

def order_qr_scanner(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no).first()
            if order:
                pack=packing_list.objects.filter(order=order).first()
                status=order_status.objects.all().order_by('sequence')
                s=[]
                total_cartons=pack.cartons.all().count()
                print(total_cartons)
                quan_24=0
                quan_26=0
                quan_28=0
                quan_30=0
                quan_32=0
                quan_34=0
                quan_36=0
                quan_38=0
                quan_40=0
                quan_42=0
                quan_44=0
                quan_46=0
                quan_48=0
                quan_50=0
                quan_52=0
                for i in pack.cartons.all():
                    if i.quantity_24:
                        quan_24+=i.quantity_24
                    if i.quantity_26:
                        quan_26+=i.quantity_26
                    if i.quantity_28:
                        quan_28+=i.quantity_28
                    if i.quantity_30:
                        quan_30+=i.quantity_30
                    if i.quantity_32:
                        quan_32+=i.quantity_32
                    if i.quantity_34:
                        quan_34+=i.quantity_34
                    if i.quantity_36:
                        quan_36+=i.quantity_36
                    if i.quantity_38:
                        quan_38+=i.quantity_38
                    if i.quantity_40:
                        quan_40+=i.quantity_40
                    if i.quantity_42:
                        quan_42+=i.quantity_42
                    if i.quantity_44:
                        quan_44+=i.quantity_44
                    if i.quantity_46:
                        quan_46+=i.quantity_46
                    if i.quantity_48:
                        quan_48+=i.quantity_48
                    if i.quantity_50:
                        quan_50+=i.quantity_50
                    if i.quantity_52:
                        quan_52+=i.quantity_52
                for j in status:
                    cartons=cartons_list.objects.filter(carton_status=j).count()
                    co=[["Cartons",total_cartons,cartons,j]]
                    # print(co)
                    sizes_stat=size_status.objects.filter(status=j)
                    for i in sizes_stat:
                        if i.size==24:
                            co.append(["Size_24",quan_24,i.quantity,i])
                        elif i.size==26:
                            co.append(["Size_26",quan_26,i.quantity,i])
                        elif i.size==28:
                            co.append(["Size_28",quan_28,i.quantity,i])
                        elif i.size==30:
                            co.append(["Size_30",quan_30,i.quantity,i])
                        elif i.size==32:
                            co.append(["Size_32",quan_32,i.quantity,i])
                        elif i.size==34:
                            co.append(["Size_34",quan_34,i.quantity,i])
                        elif i.size==36:
                            co.append(["Size_36",quan_36,i.quantity,i])
                        elif i.size==38:
                            co.append(["Size_38",quan_38,i.quantity,i])
                        elif i.size==40:
                            co.append(["Size_40",quan_40,i.quantity,i])
                        elif i.size==42:
                            co.append(["Size_42",quan_42,i.quantity,i])
                        elif i.size==44:
                            co.append(["Size_44",quan_44,i.quantity,i])
                        elif i.size==46:
                            co.append(["Size_46",quan_46,i.quantity,i])
                        elif i.size==48:
                            co.append(["Size_48",quan_48,i.quantity,i])
                        elif i.size==50:
                            co.append(["Size_50",quan_50,i.quantity,i])
                        elif i.size==52:
                            co.append(["Size_52",quan_52,i.quantity,i])
                    s.append([j.title,co])
                print(s)

                packing_lst=new_pl.objects.all()

                distribution_lst=distribution_list_1.objects.all()
                dispatch_lst=dispatch_list.objects.all()
                warehouse_lst=warehouse_list.objects.all()
                logistic_lst=logistic_list.objects.all()
                data={
                    "status":status,
                    "order":order,
                    "graph":s,
                    "lists":list_types.objects.all(),
                    "packing_list":packing_lst,
                    "distribution_list":distribution_lst,
                    "dispatch_list":dispatch_lst,
                    "warehouse_list":warehouse_lst,
                    "logistic_list":logistic_lst

                }
                if request.POST.get('ajax_qr'):
                    print(request.POST.get('which'))
                    print(request.POST.get('table_options'))
                    my_QR = decode(request.POST.get('ajax_qr'))
                    if my_QR:
            			# json_data=json.dumps(my_QR)
                        my_QR=list(str(my_QR[0]['code']).strip().split("_"))
                        l=len(my_QR)
                        if request.POST.get('which')=="New" and my_QR[0]=="Piece":
                            if(request.POST.get('table_options')=="Packing list"):
                                address=address_model.objects.filter(address=my_QR[4]).first()
                                color=color_model.objects.filter(name=my_QR[5]).first()
                                quantity=1
                                size=int(my_QR[6])
                                scl=size_color_quantity(size=size,color=color.name,quantity=1,order=order)
                                scl.save()
                                s=new_pl(order=order,scan=True,color=color,address=address,description="",date_time=datetime.datetime.now(),is_packed=True)
                                s.save()
                                s.sizes.add(scl)
                                s.save()
                            elif (request.POST.get('table_options') == "Distribution list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])
                                scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                scl.save()
                                s = distribution_list_1(order=order, scan=True, color=color, address=address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True)
                                s.save()
                                s.sizes.add(scl)
                                s.save()
                            elif (request.POST.get('table_options') == "Dispatch list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])
                                scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                scl.save()
                                s = dispatch_list(order=order, scan=True, color=color, address=address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True)
                                s.save()
                                s.sizes.add(scl)
                                s.save()

                            elif (request.POST.get('table_options') == "Warehouse list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])
                                scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                scl.save()
                                s = warehouse_list(order=order, scan=True, color=color, address=address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True)
                                s.save()
                                s.sizes.add(scl)
                                s.save()
                            elif (request.POST.get('table_options') == "Logistic list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])
                                scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                scl.save()
                                s = new_pl(order=order, scan=True, color=color, address=address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True)
                                s.save()
                                s.sizes.add(scl)
                                s.save()
                        elif request.POST.get('which')=="old" and my_QR[0]=="Piece":
                            if(request.POST.get('table_options')=="Packing list"):
                                address=address_model.objects.filter(address=my_QR[4]).first()
                                color=color_model.objects.filter(name=my_QR[5]).first()
                                quantity=1
                                size=int(my_QR[6])

                                s=new_pl.objects.filter(order=order,list_no=request.POST.get("List_no")).first()
                                a=s.sizes.objects.filter(order=order,size=size,color=color).first()
                                if(a):
                                    a.quantity+=1
                                    a.save()
                                else:
                                    scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                    scl.save()
                                    s.sizes.add(scl)
                                    s.save()
                                s.save()

                            elif (request.POST.get('table_options') == "Distribution list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])

                                s = distribution_list_1.objects.filter(order=order, list_no=request.POST.get("List_no")).first()
                                a = s.sizes.objects.filter(order=order, size=size, color=color).first()
                                if (a):
                                    a.quantity += 1
                                    a.save()
                                else:
                                    scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                    scl.save()
                                    s.sizes.add(scl)
                                    s.save()
                                s.save()
                            elif (request.POST.get('table_options') == "Dispatch list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])

                                s = dispatch_list.objects.filter(order=order, list_no=request.POST.get("List_no")).first()
                                a = s.sizes.objects.filter(order=order, size=size, color=color).first()
                                if (a):
                                    a.quantity += 1
                                    a.save()
                                else:
                                    scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                    scl.save()
                                    s.sizes.add(scl)
                                    s.save()
                                s.save()
                            elif (request.POST.get('table_options') == "Warehouse list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])

                                s = warehouse_list.objects.filter(order=order, list_no=request.POST.get("List_no")).first()
                                a = s.sizes.objects.filter(order=order, size=size, color=color).first()
                                if (a):
                                    a.quantity += 1
                                    a.save()
                                else:
                                    scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                    scl.save()
                                    s.sizes.add(scl)
                                    s.save()
                                s.save()
                            elif (request.POST.get('table_options') == "Logistic list"):
                                address = address_model.objects.filter(address=my_QR[4]).first()
                                color = color_model.objects.filter(name=my_QR[5]).first()
                                quantity = 1
                                size = int(my_QR[6])

                                s = logistic_list.objects.filter(order=order, list_no=request.POST.get("List_no")).first()
                                a = s.sizes.objects.filter(order=order, size=size, color=color).first()
                                if (a):
                                    a.quantity += 1
                                    a.save()
                                else:
                                    scl = size_color_quantity(size=size, color=color.name, quantity=1, order=order)
                                    scl.save()
                                    s.sizes.add(scl)
                                    s.save()
                                s.save()
                        elif request.POST.get('which')=="New" and my_QR[0]=="Carton":
                            if(request.POST.get('table_options')=="Packing list"):

                                carton=Carton_new.objects.filter(order=order,id=my_QR[2]).first()
                                number=1
                                z=new_pl.objects.order_by('-list_no')
                                if(z.first()):
                                    number=z.first().list_no
                                s = new_pl(order=order, scan=True, address=carton.address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True,list_no=number)
                                s.save()
                                for i in carton.sizes.objects.all():
                                    s.sizes.add(i)
                                    s.save()



                            elif (request.POST.get('table_options') == "Distribution list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                number = 1
                                z = new_pl.objects.order_by('-list_no')
                                if (z.first()):
                                    number = z.first().list_no
                                s = distribution_list_1(order=order, scan=True, address=carton.address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True, list_no=number)
                                s.save()
                                for i in carton.sizes.objects.all():
                                    s.sizes.add(i)
                                    s.save()
                            elif (request.POST.get('table_options') == "Dispatch list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                number = 1
                                z = new_pl.objects.order_by('-list_no')
                                if (z.first()):
                                    number = z.first().list_no
                                s = dispatch_list(order=order, scan=True, address=carton.address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True, list_no=number)
                                s.save()
                                for i in carton.sizes.objects.all():
                                    s.sizes.add(i)
                                    s.save()
                            elif (request.POST.get('table_options') == "Warehouse list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                number = 1
                                z = new_pl.objects.order_by('-list_no')
                                if (z.first()):
                                    number = z.first().list_no
                                s = warehouse_list(order=order, scan=True, address=carton.address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True, list_no=number)
                                s.save()
                                for i in carton.sizes.objects.all():
                                    s.sizes.add(i)
                                    s.save()
                            elif (request.POST.get('table_options') == "Logistic list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                number = 1
                                z = new_pl.objects.order_by('-list_no')
                                if (z.first()):
                                    number = z.first().list_no
                                s = logistic_list(order=order, scan=True, address=carton.address, description="",
                                           date_time=datetime.datetime.now(), is_packed=True, list_no=number)
                                s.save()
                                for i in carton.sizes.objects.all():
                                    s.sizes.add(i)
                                    s.save()
                        elif request.POST.get('which')=="old" and my_QR[0]=="Carton":
                            if(request.POST.get('table_options')=="Packing list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                pl=new_pl.objects.filter(order=order,list_no=request.POST.get('List_no')).first()
                                for i in carton.sizes.objects.all():
                                    size=i.size
                                    color=i.color
                                    a=pl.sizes.objects.filter(size=size,color=color).first()
                                    if(a):
                                        a.quantity+=i.quantity
                                        a.save()
                                    else:
                                        a=size_color_quantity(size=size,color=color,quantity=i.quantity)
                                        a.save()
                                        i.sizes.add(a)
                                        i.save()




                            elif (request.POST.get('table_options') == "Distribution list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                pl = distribution_list_1.objects.filter(order=order, list_no=request.POST.get('List_no')).first()
                                for i in carton.sizes.objects.all():
                                    size = i.size
                                    color = i.color
                                    a = pl.sizes.objects.filter(size=size, color=color).first()
                                    if (a):
                                        a.quantity += i.quantity
                                        a.save()
                                    else:
                                        a = size_color_quantity(size=size, color=color, quantity=i.quantity)
                                        a.save()
                                        i.sizes.add(a)
                                        i.save()
                            elif (request.POST.get('table_options') == "Dispatch list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                pl = dispatch_list.objects.filter(order=order, list_no=request.POST.get('List_no')).first()
                                for i in carton.sizes.objects.all():
                                    size = i.size
                                    color = i.color
                                    a = pl.sizes.objects.filter(size=size, color=color).first()
                                    if (a):
                                        a.quantity += i.quantity
                                        a.save()
                                    else:
                                        a = size_color_quantity(size=size, color=color, quantity=i.quantity)
                                        a.save()
                                        i.sizes.add(a)
                                        i.save()
                            elif (request.POST.get('table_options') == "Warehouse list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                pl = warehouse_list.objects.filter(order=order, list_no=request.POST.get('List_no')).first()
                                for i in carton.sizes.objects.all():
                                    size = i.size
                                    color = i.color
                                    a = pl.sizes.objects.filter(size=size, color=color).first()
                                    if (a):
                                        a.quantity += i.quantity
                                        a.save()
                                    else:
                                        a = size_color_quantity(size=size, color=color, quantity=i.quantity)
                                        a.save()
                                        i.sizes.add(a)
                                        i.save()
                            elif (request.POST.get('table_options') == "Logistic list"):
                                carton = Carton_new.objects.filter(order=order, id=my_QR[2]).first()
                                pl = logistic_list.objects.filter(order=order, list_no=request.POST.get('List_no')).first()
                                for i in carton.sizes.objects.all():
                                    size = i.size
                                    color = i.color
                                    a = pl.sizes.objects.filter(size=size, color=color).first()
                                    if (a):
                                        a.quantity += i.quantity
                                        a.save()
                                    else:
                                        a = size_color_quantity(size=size, color=color, quantity=i.quantity)
                                        a.save()
                                        i.sizes.add(a)
                                        i.save()
                        return JsonResponse({"data": True})




                        stat=order_status.objects.filter(sequence=int(request.POST.get('status'))).first()
                        if l==2 and int(my_QR[0])==order_no:
                            obj=pack.cartons.all().filter(carton_password=my_QR[1]).first()
                            if obj and stat:
                                obj.carton_status=stat
                                obj.save()
                                return JsonResponse({"data":True})
                            return JsonResponse({"data":False})
                        elif l==3 and int(my_QR[0])==order_no:
                            obj=pack.cartons.all().filter(carton_password=my_QR[1]).first()
                            if obj and stat:
                                size=int(my_QR[2])
                                size_status_obj=size_status.objects.filter(status=stat,carton=obj,size=size).first()
                                if size_status_obj:
                                    size_status_obj.quantity+=1
                                else:
                                    size_status_obj=size_status(status=stat,carton=obj,size=size,quantity=1)
                                size_status_obj.save()
                                return JsonResponse({"data":True})

                            return JsonResponse({"data":False})
                        return JsonResponse({"data":False,"Scanned":True})
                    return JsonResponse({"data":False,"Scanned":False})

                return render(request,"order_documents/order_qr_scanner.html",data)
            else:
                return redirect('/userdetail/staff_profile')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')

from POM.models import measurement,POM,measurement_chart
from b2b.models import quantity_b2b,bom



def trim_card(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        order=company_Order.objects.filter(order_no=order_no).first()
        if details and order and details in order.staffs_Allocated.all():
            order=company_Order.objects.filter(order_no=order_no)
            # print(f'COMPANY ORDER: {order}')
            if order.count()>0:
                order=order.first()
                print(f'NORMAL ORDER: {order}')
                meas_chart=measurement.objects.filter(label=order.label,fit=order.fit,season=order.season,
                    product_Category=order.product_Category,product_Subcategory=order.product_Subcategory,
                    product_Supercategory=order.product_Supercategory).last()
                print(f'MEAS CHART: {meas_chart}')
                if meas_chart:
                    quants=quantity_b2b.objects.filter(order=order,production=True)
                    print(f'QUANTS: {quants}')
                    sizes_avail=[]
                    for i in quants:
                        if i.size_label not in sizes_avail:
                            sizes_avail.append([i.size_label,i.quantity])
                    poms=POM.objects.filter(product_Supercategory=order.product_Supercategory)
                    poms=order.poms_keys.all()
                    print(f'POMS: {poms}')
                    meas=[]
                    for i in poms:
                        meas.append([i,[]])
                        for j in sizes_avail:
                            val=measurement_chart.objects.filter(chart=meas_chart,pom=i,size=int(j[0])).first()
                            if val:
                                meas[-1][-1].append(val.value)
                            else:
                                meas[-1][-1].append(0)
                    print(f'MEAS: {meas}')
                else:
                    meas=[0]
                    sizes_avail=[]
                bom_obj=bom.objects.filter(order=order).last()
                print(f'BOM_OBJ: {bom_obj}\n\n\n bom.trims_used.all(): {bom_obj.trims_used.all()}')
                print(f'product_Category = {order.product_Category}, product_Supercategory = {order.product_Supercategory}, product_Subcategory = {order.product_Subcategory}')
                trims_details = trimcard_sections.objects.filter(seller=order.fashion_Brand, product_Category = order.product_Category, product_Supercategory = order.product_Supercategory, product_Subcategory = order.product_Subcategory).first()
                all_trim_details = trimcard_sections.objects.filter(seller=details)
                print(f'ALL TRIMS: {all_trim_details}')
                data={
                    "order":order,
                    "meas":meas,
                    "sizes_avail":sizes_avail,
                    "bom":bom_obj,
                    "trim_section":trims_details,
                }
                print(f'\n\n\nTHIS IS DATA: {data}\n\n\n')
                return render(request,'order_documents/trim_card.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')




def order_po(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
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
                    prod=production_order.objects.filter(order=order).order_by('production_no')
                    f=[]
                    for i in prod:
                        sizes=[]
                        col_map=[]
                        for j in i.sizes.all():
                            if not(j.size_label in sizes):
                                sizes.append(j.size_label)
                            if not([j.color,j.address] in col_map):
                                col_map.append([j.color,j.address])
                        sizes.sort()
                        prod_quan=[]
                        for k in col_map:
                            li=[]
                            for l in sizes:
                                qu=i.sizes.all().filter(color=k[0],address=k[1],size_label=l)
                                t=0
                                for m in qu:
                                    t+=m.quantity
                                li.append({"size":l,"quantity":t})
                            prod_quan.append([k,li])
                        f.append({"sizes":sizes,"prods":prod_quan})
                    data={
                        'order':order,
                        'details':details,
                        'compan':compan,
                        'delivery':order.order_date_time + datetime.timedelta(days=tlt),
                        'total_cost':order.total_Price*order.quantity,
                        'total_cost_words':num2word(int(order.total_Price*order.quantity)),
                        'check':check,
                        "production":f,
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







def order_invoice(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
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
                    prod=production_order.objects.filter(order=order).order_by('production_no')
                    f=[]
                    for i in prod:
                        sizes=[]
                        col_map=[]
                        for j in i.sizes.all():
                            if not(j.size_label in sizes):
                                sizes.append(j.size_label)
                            if not([j.color,j.address] in col_map):
                                col_map.append([j.color,j.address])
                        sizes.sort()
                        prod_quan=[]
                        for k in col_map:
                            li=[]
                            for l in sizes:
                                qu=i.sizes.all().filter(color=k[0],address=k[1],size_label=l)
                                t=0
                                for m in qu:
                                    t+=m.quantity
                                li.append({"size":l,"quantity":t})
                            prod_quan.append([k,li])
                        f.append({"sizes":sizes,"prods":prod_quan})
                    data={
                        'order':order,
                        'details':details,
                        'compan':compan,
                        'delivery':order.order_date_time + datetime.timedelta(days=tlt),
                        'total_cost':order.total_Price*quan,
                        'quan':quan,
                        'total_cost_words':num2word(int(order.total_Price*quan)),
                        'check':check,
                        'compan_det':compan_det,
                        "production":f
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








def garment_po(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
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
                        'check':check,
                        'compan_det':compan_det
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/garment_po.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')







def garment_invoice(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
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
                return render_to_pdf('order_documents/garment_invoice.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')












def finishing_po(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(name="Finishing").first()
                # finishing_objs=bom_obj.products.filter(category=finishing_obj)
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_finishing1,bom_obj.specification_finishing1,bom_obj.consumption_finishing1,
                        bom_obj.wastage_finishing1,bom_obj.rate_finishing1,bom_obj.cost_finishing1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_finishing2,bom_obj.specification_finishing2,bom_obj.consumption_finishing2,
                        bom_obj.wastage_finishing2,bom_obj.rate_finishing2,bom_obj.cost_finishing2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_finishing3,bom_obj.specification_finishing3,bom_obj.consumption_finishing3,
                        bom_obj.wastage_finishing3,bom_obj.rate_finishing3,bom_obj.cost_finishing3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_finishing4,bom_obj.specification_finishing4,bom_obj.consumption_finishing4,
                        bom_obj.wastage_finishing4,bom_obj.rate_finishing4,bom_obj.cost_finishing4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_finishing5,bom_obj.specification_finishing5,bom_obj.consumption_finishing5,
                        bom_obj.wastage_finishing5,bom_obj.rate_finishing5,bom_obj.cost_finishing5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_finishing6,bom_obj.specification_finishing6,bom_obj.consumption_finishing6,
                        bom_obj.wastage_finishing6,bom_obj.rate_finishing6,bom_obj.cost_finishing6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_finishing7,bom_obj.specification_finishing7,bom_obj.consumption_finishing7,
                        bom_obj.wastage_finishing7,bom_obj.rate_finishing7,bom_obj.cost_finishing7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_finishing8,bom_obj.specification_finishing8,bom_obj.consumption_finishing8,
                        bom_obj.wastage_finishing8,bom_obj.rate_finishing8,bom_obj.cost_finishing8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_finishing9,bom_obj.specification_finishing9,bom_obj.consumption_finishing9,
                        bom_obj.wastage_finishing9,bom_obj.rate_finishing9,bom_obj.cost_finishing9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_finishing10,bom_obj.specification_finishing10,bom_obj.consumption_finishing10,
                        bom_obj.wastage_finishing10,bom_obj.rate_finishing10,bom_obj.cost_finishing10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_po.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')








def finishing_invoice(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(finishing=True).first()
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_finishing1,bom_obj.specification_finishing1,bom_obj.consumption_finishing1,
                        bom_obj.wastage_finishing1,bom_obj.rate_finishing1,bom_obj.cost_finishing1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_finishing2,bom_obj.specification_finishing2,bom_obj.consumption_finishing2,
                        bom_obj.wastage_finishing2,bom_obj.rate_finishing2,bom_obj.cost_finishing2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_finishing3,bom_obj.specification_finishing3,bom_obj.consumption_finishing3,
                        bom_obj.wastage_finishing3,bom_obj.rate_finishing3,bom_obj.cost_finishing3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_finishing4,bom_obj.specification_finishing4,bom_obj.consumption_finishing4,
                        bom_obj.wastage_finishing4,bom_obj.rate_finishing4,bom_obj.cost_finishing4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_finishing5,bom_obj.specification_finishing5,bom_obj.consumption_finishing5,
                        bom_obj.wastage_finishing5,bom_obj.rate_finishing5,bom_obj.cost_finishing5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_finishing6,bom_obj.specification_finishing6,bom_obj.consumption_finishing6,
                        bom_obj.wastage_finishing6,bom_obj.rate_finishing6,bom_obj.cost_finishing6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_finishing7,bom_obj.specification_finishing7,bom_obj.consumption_finishing7,
                        bom_obj.wastage_finishing7,bom_obj.rate_finishing7,bom_obj.cost_finishing7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_finishing8,bom_obj.specification_finishing8,bom_obj.consumption_finishing8,
                        bom_obj.wastage_finishing8,bom_obj.rate_finishing8,bom_obj.cost_finishing8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_finishing9,bom_obj.specification_finishing9,bom_obj.consumption_finishing9,
                        bom_obj.wastage_finishing9,bom_obj.rate_finishing9,bom_obj.cost_finishing9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_finishing10,bom_obj.specification_finishing10,bom_obj.consumption_finishing10,
                        bom_obj.wastage_finishing10,bom_obj.rate_finishing10,bom_obj.cost_finishing10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
                if not(tlt) or not(order.total_Price) or fini==[]:
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_invoice.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')







def fabric_po(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(name="Fabric").first()
                # finishing_objs=bom_obj.products.filter(category=finishing_obj)
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_fabric1,bom_obj.specification_fabric1,bom_obj.consumption_fabric1,
                        bom_obj.wastage_fabric1,bom_obj.rate_fabric1,bom_obj.cost_fabric1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_fabric2,bom_obj.specification_fabric2,bom_obj.consumption_fabric2,
                        bom_obj.wastage_fabric2,bom_obj.rate_fabric2,bom_obj.cost_fabric2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_fabric3,bom_obj.specification_fabric3,bom_obj.consumption_fabric3,
                        bom_obj.wastage_fabric3,bom_obj.rate_fabric3,bom_obj.cost_fabric3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_fabric4,bom_obj.specification_fabric4,bom_obj.consumption_fabric4,
                        bom_obj.wastage_fabric4,bom_obj.rate_fabric4,bom_obj.cost_fabric4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_fabric5,bom_obj.specification_fabric5,bom_obj.consumption_fabric5,
                        bom_obj.wastage_fabric5,bom_obj.rate_fabric5,bom_obj.cost_fabric5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_fabric6,bom_obj.specification_fabric6,bom_obj.consumption_fabric6,
                        bom_obj.wastage_fabric6,bom_obj.rate_fabric6,bom_obj.cost_fabric6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_fabric7,bom_obj.specification_fabric7,bom_obj.consumption_fabric7,
                        bom_obj.wastage_fabric7,bom_obj.rate_fabric7,bom_obj.cost_fabric7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_fabric8,bom_obj.specification_fabric8,bom_obj.consumption_fabric8,
                        bom_obj.wastage_fabric8,bom_obj.rate_fabric8,bom_obj.cost_fabric8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_fabric9,bom_obj.specification_fabric9,bom_obj.consumption_fabric9,
                        bom_obj.wastage_fabric9,bom_obj.rate_fabric9,bom_obj.cost_fabric9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_fabric10,bom_obj.specification_fabric10,bom_obj.consumption_fabric10,
                        bom_obj.wastage_fabric10,bom_obj.rate_fabric10,bom_obj.cost_fabric10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
                if not(tlt) or not(order.total_Price) or fini==[]:
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_po.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')








def fabric_invoice(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(name="Fabric").first()
                # finishing_objs=bom_obj.products.filter(category=finishing_obj)
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_fabric1,bom_obj.specification_fabric1,bom_obj.consumption_fabric1,
                        bom_obj.wastage_fabric1,bom_obj.rate_fabric1,bom_obj.cost_fabric1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_fabric2,bom_obj.specification_fabric2,bom_obj.consumption_fabric2,
                        bom_obj.wastage_fabric2,bom_obj.rate_fabric2,bom_obj.cost_fabric2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_fabric3,bom_obj.specification_fabric3,bom_obj.consumption_fabric3,
                        bom_obj.wastage_fabric3,bom_obj.rate_fabric3,bom_obj.cost_fabric3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_fabric4,bom_obj.specification_fabric4,bom_obj.consumption_fabric4,
                        bom_obj.wastage_fabric4,bom_obj.rate_fabric4,bom_obj.cost_fabric4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_fabric5,bom_obj.specification_fabric5,bom_obj.consumption_fabric5,
                        bom_obj.wastage_fabric5,bom_obj.rate_fabric5,bom_obj.cost_fabric5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_fabric6,bom_obj.specification_fabric6,bom_obj.consumption_fabric6,
                        bom_obj.wastage_fabric6,bom_obj.rate_fabric6,bom_obj.cost_fabric6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_fabric7,bom_obj.specification_fabric7,bom_obj.consumption_fabric7,
                        bom_obj.wastage_fabric7,bom_obj.rate_fabric7,bom_obj.cost_fabric7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_fabric8,bom_obj.specification_fabric8,bom_obj.consumption_fabric8,
                        bom_obj.wastage_fabric8,bom_obj.rate_fabric8,bom_obj.cost_fabric8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_fabric9,bom_obj.specification_fabric9,bom_obj.consumption_fabric9,
                        bom_obj.wastage_fabric9,bom_obj.rate_fabric9,bom_obj.cost_fabric9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_fabric10,bom_obj.specification_fabric10,bom_obj.consumption_fabric10,
                        bom_obj.wastage_fabric10,bom_obj.rate_fabric10,bom_obj.cost_fabric10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
                if not(tlt) or not(order.total_Price) or fini==[]:
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_invoice.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')










def packing_po(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(name="Packing").first()
                # finishing_objs=bom_obj.products.filter(category=finishing_obj)
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_packing1,bom_obj.specification_packing1,bom_obj.consumption_packing1,
                        bom_obj.wastage_packing1,bom_obj.rate_packing1,bom_obj.cost_packing1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_packing2,bom_obj.specification_packing2,bom_obj.consumption_packing2,
                        bom_obj.wastage_packing2,bom_obj.rate_packing2,bom_obj.cost_packing2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_packing3,bom_obj.specification_packing3,bom_obj.consumption_packing3,
                        bom_obj.wastage_packing3,bom_obj.rate_packing3,bom_obj.cost_packing3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_packing4,bom_obj.specification_packing4,bom_obj.consumption_packing4,
                        bom_obj.wastage_packing4,bom_obj.rate_packing4,bom_obj.cost_packing4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_packing5,bom_obj.specification_packing5,bom_obj.consumption_packing5,
                        bom_obj.wastage_packing5,bom_obj.rate_packing5,bom_obj.cost_packing5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_packing6,bom_obj.specification_packing6,bom_obj.consumption_packing6,
                        bom_obj.wastage_packing6,bom_obj.rate_packing6,bom_obj.cost_packing6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_packing7,bom_obj.specification_packing7,bom_obj.consumption_packing7,
                        bom_obj.wastage_packing7,bom_obj.rate_packing7,bom_obj.cost_packing7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_packing8,bom_obj.specification_packing8,bom_obj.consumption_packing8,
                        bom_obj.wastage_packing8,bom_obj.rate_packing8,bom_obj.cost_packing8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_packing9,bom_obj.specification_packing9,bom_obj.consumption_packing9,
                        bom_obj.wastage_packing9,bom_obj.rate_packing9,bom_obj.cost_packing9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_packing10,bom_obj.specification_packing10,bom_obj.consumption_packing10,
                        bom_obj.wastage_packing10,bom_obj.rate_packing10,bom_obj.cost_packing10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
                if not(tlt) or not(order.total_Price) or fini==[]:
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_po.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')








def packing_invoice(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(name="Packing").first()
                # finishing_objs=bom_obj.products.filter(category=finishing_obj)
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_packing1,bom_obj.specification_packing1,bom_obj.consumption_packing1,
                        bom_obj.wastage_packing1,bom_obj.rate_packing1,bom_obj.cost_packing1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_packing2,bom_obj.specification_packing2,bom_obj.consumption_packing2,
                        bom_obj.wastage_packing2,bom_obj.rate_packing2,bom_obj.cost_packing2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_packing3,bom_obj.specification_packing3,bom_obj.consumption_packing3,
                        bom_obj.wastage_packing3,bom_obj.rate_packing3,bom_obj.cost_packing3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_packing4,bom_obj.specification_packing4,bom_obj.consumption_packing4,
                        bom_obj.wastage_packing4,bom_obj.rate_packing4,bom_obj.cost_packing4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_packing5,bom_obj.specification_packing5,bom_obj.consumption_packing5,
                        bom_obj.wastage_packing5,bom_obj.rate_packing5,bom_obj.cost_packing5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_packing6,bom_obj.specification_packing6,bom_obj.consumption_packing6,
                        bom_obj.wastage_packing6,bom_obj.rate_packing6,bom_obj.cost_packing6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_packing7,bom_obj.specification_packing7,bom_obj.consumption_packing7,
                        bom_obj.wastage_packing7,bom_obj.rate_packing7,bom_obj.cost_packing7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_packing8,bom_obj.specification_packing8,bom_obj.consumption_packing8,
                        bom_obj.wastage_packing8,bom_obj.rate_packing8,bom_obj.cost_packing8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_packing9,bom_obj.specification_packing9,bom_obj.consumption_packing9,
                        bom_obj.wastage_packing9,bom_obj.rate_packing9,bom_obj.cost_packing9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_packing10,bom_obj.specification_packing10,bom_obj.consumption_packing10,
                        bom_obj.wastage_packing10,bom_obj.rate_packing10,bom_obj.cost_packing10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_invoice.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')












def sewing_po(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(name="Sewing").first()
                # finishing_objs=bom_obj.products.filter(category=finishing_obj)
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_sewing1,bom_obj.specification_sewing1,bom_obj.consumption_sewing1,
                        bom_obj.wastage_sewing1,bom_obj.rate_sewing1,bom_obj.cost_sewing1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_sewing2,bom_obj.specification_sewing2,bom_obj.consumption_sewing2,
                        bom_obj.wastage_sewing2,bom_obj.rate_sewing2,bom_obj.cost_sewing2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_sewing3,bom_obj.specification_sewing3,bom_obj.consumption_sewing3,
                        bom_obj.wastage_sewing3,bom_obj.rate_sewing3,bom_obj.cost_sewing3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_sewing4,bom_obj.specification_sewing4,bom_obj.consumption_sewing4,
                        bom_obj.wastage_sewing4,bom_obj.rate_sewing4,bom_obj.cost_sewing4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_sewing5,bom_obj.specification_sewing5,bom_obj.consumption_sewing5,
                        bom_obj.wastage_sewing5,bom_obj.rate_sewing5,bom_obj.cost_sewing5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_sewing6,bom_obj.specification_sewing6,bom_obj.consumption_sewing6,
                        bom_obj.wastage_sewing6,bom_obj.rate_sewing6,bom_obj.cost_sewing6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_sewing7,bom_obj.specification_sewing7,bom_obj.consumption_sewing7,
                        bom_obj.wastage_sewing7,bom_obj.rate_sewing7,bom_obj.cost_sewing7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_sewing8,bom_obj.specification_sewing8,bom_obj.consumption_sewing8,
                        bom_obj.wastage_sewing8,bom_obj.rate_sewing8,bom_obj.cost_sewing8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_sewing9,bom_obj.specification_sewing9,bom_obj.consumption_sewing9,
                        bom_obj.wastage_sewing9,bom_obj.rate_sewing9,bom_obj.cost_sewing9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_sewing10,bom_obj.specification_sewing10,bom_obj.consumption_sewing10,
                        bom_obj.wastage_sewing10,bom_obj.rate_sewing10,bom_obj.cost_sewing10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
                if not(tlt) or not(order.total_Price) or fini==[]:
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_po.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')








def sewing_invoice(request,order_no):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.staff:
            order=company_Order.objects.filter(order_no=order_no)
            if order.count()>0:
                order=order.first()
                compan=company_detail.objects.filter(email=order.user_email).first()
                compan_det=detail.objects.filter(email=order.user_email).first()
                tlt=order.target_lead_time
                a=order.total_Price
                check=True
                bom_obj=bom.objects.filter(order=order).first()
                finishing_obj=trims_Category.objects.filter(name="Sewing").first()
                # finishing_objs=bom_obj.products.filter(category=finishing_obj)
                if not(bom_obj):
                    check=False
                    finishing_objs=[]
                else:
                    finishing_objs=bom_obj.products.filter(category=finishing_obj)
                count=0
                fini=[]
                final_price=0
                final_quan=0
                for i in finishing_objs:
                    count+=1
                    kum=[]
                    if count==1:
                        kum=[i.title,bom_obj.uom_sewing1,bom_obj.specification_sewing1,bom_obj.consumption_sewing1,
                        bom_obj.wastage_sewing1,bom_obj.rate_sewing1,bom_obj.cost_sewing1]
                    elif count==2:
                        kum=[i.title,bom_obj.uom_sewing2,bom_obj.specification_sewing2,bom_obj.consumption_sewing2,
                        bom_obj.wastage_sewing2,bom_obj.rate_sewing2,bom_obj.cost_sewing2]
                    elif count==3:
                        kum=[i.title,bom_obj.uom_sewing3,bom_obj.specification_sewing3,bom_obj.consumption_sewing3,
                        bom_obj.wastage_sewing3,bom_obj.rate_sewing3,bom_obj.cost_sewing3]
                    elif count==4:
                        kum=[i.title,bom_obj.uom_sewing4,bom_obj.specification_sewing4,bom_obj.consumption_sewing4,
                        bom_obj.wastage_sewing4,bom_obj.rate_sewing4,bom_obj.cost_sewing4]
                    elif count==5:
                        kum=[i.title,bom_obj.uom_sewing5,bom_obj.specification_sewing5,bom_obj.consumption_sewing5,
                        bom_obj.wastage_sewing5,bom_obj.rate_sewing5,bom_obj.cost_sewing5]
                    elif count==6:
                        kum=[i.title,bom_obj.uom_sewing6,bom_obj.specification_sewing6,bom_obj.consumption_sewing6,
                        bom_obj.wastage_sewing6,bom_obj.rate_sewing6,bom_obj.cost_sewing6]
                    elif count==7:
                        kum=[i.title,bom_obj.uom_sewing7,bom_obj.specification_sewing7,bom_obj.consumption_sewing7,
                        bom_obj.wastage_sewing7,bom_obj.rate_sewing7,bom_obj.cost_sewing7]
                    elif count==8:
                        kum=[i.title,bom_obj.uom_sewing8,bom_obj.specification_sewing8,bom_obj.consumption_sewing8,
                        bom_obj.wastage_sewing8,bom_obj.rate_sewing8,bom_obj.cost_sewing8]
                    elif count==9:
                        kum=[i.title,bom_obj.uom_sewing9,bom_obj.specification_sewing9,bom_obj.consumption_sewing9,
                        bom_obj.wastage_sewing9,bom_obj.rate_sewing9,bom_obj.cost_sewing9]
                    elif count==10:
                        kum=[i.title,bom_obj.uom_sewing10,bom_obj.specification_sewing10,bom_obj.consumption_sewing10,
                        bom_obj.wastage_sewing10,bom_obj.rate_sewing10,bom_obj.cost_sewing10]
                    fini.append(kum)
                    final_price+=int(kum[6])
                    final_quan+=int(kum[3])
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
                        'total_cost_words':num2word(int(final_price)),
                        'check':check,
                        'compan_det':compan_det,
                        'fini':fini,
                        'bom_obj':bom_obj,
                        'final_price':final_price,
                        'final_quan':final_quan
                    }
                else:
                    data={
                        "not_possible":True
                    }
                return render_to_pdf('order_documents/finishing_invoice.html',data)
            else:
                return redirect('/userdetail/logout')
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')
