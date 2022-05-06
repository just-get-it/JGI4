



from django.shortcuts import render,redirect
from userdetail.models import detail,staff_Categories,seller_Categories
# Create your views here.
from django.http import HttpResponse,JsonResponse
import json
from product.models import category,sub_category,super_category
from permission.models import section,orders_permission
from .utils.orders_utils import *

from Notification.models import Offset


def products(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details:
            #if details.staff:
                if request.POST.get('prod_cate'):
                    prod_cate=int(request.POST.get('prod_cate'))
                    obj=category.objects.filter(id=prod_cate).first()
                    obj=sub_category.objects.filter(product_Category=obj)
                    bol=False
                    if obj.count()>0:
                        bol=True
                    obj1=list(obj.values())
                    return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
                if request.POST.get('prod_subcate'):
                    prod_cate=int(request.POST.get('prod_subcate'))
                    obj=sub_category.objects.filter(id=prod_cate).first()
                    obj=super_category.objects.filter(product_Subcategory=obj)
                    bol=False
                    if obj.count()>0:
                        bol=True
                    obj1=list(obj.values())
                    return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")




def orders_section(request,order_no,name):
    section_obj=section.objects.filter(name=name).first()
    details=detail.objects.filter(email=request.user.email).first()
    if details and section_obj:
        brand=seller_Categories.objects.filter(name="Products Vendor").first()
        perm=False
        if details.staff:
            perm=orders_permission.objects.filter(allowed_section=section_obj,staff_category=details.staff_category).first()
        elif details.vendor and details.seller_category==brand:
            perm=orders_permission.objects.filter(allowed_section=section_obj,seller_category=details.seller_category).first()
        elif details.vendor:
            perm=orders_permission.objects.filter(allowed_section=section_obj,seller_category=details.seller_category).first()

        elif details.buisness_Customer:
            perm=orders_permission.objects.filter(allowed_section=section_obj,customer=True).first()
        if perm:
            data={}
            if name=="Orders_Description":
                data=getOrderDesc(request,details,order_no)
            elif name=="Staff_Allocation":
                data=getOrderStaffAllocation(request,details,order_no)
            elif name=="Production_Orders":
                data=getProductionOrder(request,details,order_no)
            elif name=="Size_Assortment":
                data=getSizeAssortment(request,details,order_no)
            elif name=="Measurement_Chart":
                data=getMeasurementChart(request,details,order_no)
            elif name=="Activities":
                data=getActivities(request,details,order_no)
            elif name=="Order_Forms":
                data=getOrderForms(request,details,order_no)
            elif name=="Order_Documents":
                data=getOrderDocuments(request,details,order_no)
            elif name=="Staff_Contacts":
                data=getStaffContacts(request,details,order_no)
            elif name=="Assortment_Permissions":
                data=getAssortmentPermissions(request,details,order_no)
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"access":False})
    else:
        return JsonResponse({"access":False})



def getOffset(request):
    offset=Offset.objects.all().first()
    if offset:
        return JsonResponse({"ok":True,"offset":offset.offset})
    else:
        return JsonResponse({"ok":False})


def setOffset(request):
    if request.GET.get('apikey')=="1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A":
        offset=Offset.objects.all().first()
        if offset and request.GET.get('offset'):
            offset.offset=request.GET.get('offset')
            offset.offset=int(offset.offset)+1
            offset.save()
            print(offset.offset)
            return True
        else:
            return False
    else:
        return False


def checkLoggedIn(request):
    if request.GET.get('apikey')=="1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A":
        if request.GET.get('chat_id'):
            details=detail.objects.filter(telegram_id=request.GET.get('chat_id')).first()
            if details:
                return JsonResponse({"ok":True})
            else:
                return JsonResponse({"ok":False})
        else:
            return JsonResponse({"ok":False})
    else:
        return JsonResponse({"ok":False})



def checkUser(request):
    if request.GET.get('apikey')=="1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A":
        if request.GET.get('chat_id') and request.GET.get('email') and request.GET.get('password'):
            details=detail.objects.filter(telegram_id=request.GET.get('chat_id')).first()
            if details:
                return JsonResponse({"ok":False})
            else:
                details=detail.objects.filter(email=request.GET.get('email'),password=request.GET.get('password')).first()
                if details:
                    details.telegram_id=request.GET.get('chat_id')
                    details.save()
                    return JsonResponse({"ok":True})
                else:
                    return JsonResponse({"ok":False})
        else:
            return JsonResponse({"ok":False})
    else:
        return JsonResponse({"ok":False})