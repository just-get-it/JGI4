




from django.shortcuts import render,redirect
from .models import category,sub_category,super_category,product
from .models import attribute, product_common_attribute_values, product_cate_b2b,size_color_quantity,labels_Object,labels_Attributes,label_Attributes_Values,safety_stock
# Create your views here.

from filter.models import filter_Categories,filter_Objects
from django.core.paginator import Paginator

from copy import deepcopy
# from cart.models import *
# from cartnew.models import OrderItem


from django.db.models import Q, Max, Avg


from django.core import serializers
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model
# Create your views here.
from userdetail.models import detail,seller_Categories,staff_Categories
import random
import json
from b2b.models import notifications,company_Order,activities,quantity_b2b,activities_Category,production_order
from b2b.models import color_model,address_model
from userdetail.models import brand
from POM.models import measurement

from .models import product,washcare_model,option_tags

from seller_info.models import labels,fits,seasons
from django.http import HttpResponse
import datetime
from django.utils import timezone
from django.utils.dateparse import parse_date
from userdetail.models import response_time

from POM.models import POM
from b2b.models import assortment
from b2b.models import messages_head,chats_head

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from controladmin.forms import *
from .forms import UploadProductForm

@csrf_exempt
def sub_fetch(request):
    categ = request.POST.getlist("category[]")
    subcateg = request.POST.getlist("subcategories[]")
    str1_send = ""

    subcat_list =[]
    supcat_list =[]

    if categ != []:

        for cat in categ:
            for catna in sub_category.objects.filter(product_Category__name__contains=cat):
                subcat_list.append(catna.name)


    # if subcateg != []:
    # 	for sub in subcateg:
    # 		supcat_list.append(sup_category.objects.filter(product_Subcategory__name__contains=subcateg))
    
    for su in subcat_list:
        if su in subcateg:
            
            str1_send = (str1_send
                    +'<div class="row"><input type="checkbox" checked   name="'+str(su)+'" value="'+str(su)+'" class="ml-2 common_selector subcategories"><label class="ml-2 fontcabin">'+str(su)+'</label></div>')
        else:
            str1_send = (str1_send
                    +'<div class="row"><input type="checkbox"    name="'+str(su)+'" value="'+str(su)+'" class="ml-2 common_selector subcategories"><label class="ml-2 fontcabin">'+str(su)+'</label></div>')			


    return HttpResponse(str1_send)


@csrf_exempt
def sup_fetch(request):
    categ = request.POST.getlist("category[]")
    subcateg = request.POST.getlist("subcategories[]")
    supcateg = request.POST.getlist("supcategories[]")
    str2_send = ""

    subcat_list =[]
    supcat_list =[]

    if subcateg != []:

        for sub in subcateg:
            for subcat in super_category.objects.filter(product_Subcategory__name__contains=sub):
                supcat_list.append(subcat.name)
    
        for su in supcat_list:
            if su in supcateg:
                hey ='test'
                str2_send = (str2_send
                            +'<div class="row"><input type="checkbox" checked name="'+str(su)+'" value="'+str(su)+'" class="ml-2 common_selector supcategories"><label class="ml-2 fontcabin">'+str(su)+'</label></div>')
            else:
                str2_send = (str2_send
                            +'<div class="row"><input type="checkbox" name="'+str(su)+'" value="'+str(su)+'" class="ml-2 common_selector supcategories"><label class="ml-2 fontcabin">'+str(su)+'</label></div>')			
    else:
        for cat in categ:
            for catna in super_category.objects.filter(product_Category__name__contains=cat):
                supcat_list.append(catna.name)

        for su in supcat_list:
            if su in supcateg:
                str2_send = (str2_send
                            +'<div class="row"><input type="checkbox" checked name="'+str(su)+'" value="'+str(su)+'" class="ml-2 common_selector supcategories"><label class="ml-2 fontcabin">'+str(su)+'</label></div>')
            else:
                str2_send = (str2_send
                            +'<div class="row"><input type="checkbox" name="'+str(su)+'" value="'+str(su)+'" class="ml-2 common_selector supcategories"><label class="ml-2 fontcabin">'+str(su)+'</label></div>')

        


    return HttpResponse(str2_send)

@csrf_exempt
def brand_fetch(request):
    categ = request.POST.getlist("category[]")
    subcateg = request.POST.getlist("subcategories[]")
    supcateg = request.POST.getlist("supcategories[]")
    brands = request.POST.getlist("brands[]")	
    query = product.objects.all()	
    str3_send = ""
    brand_list = []
    if supcateg != []:	
        query = query.filter(product_Supercategory__name__in=supcateg)
        brand_to_send = query.values_list("brand", flat=True).distinct()

        for brand in brand_to_send:
            brand_list.append(brand)

        for br in brand_list:
                if br in brands:
                    str3_send = (str3_send
                            +'<div class="row"> <input type="checkbox" checked name="'+str(br)+'" value="'+str(br)+'" class="ml-2 common_selector brand"> <label class="ml-2 fontcabin">'+str(br)+'</label></div>')
                else:
                    str3_send = (str3_send
                            +'<div class="row"> <input type="checkbox"  name="'+str(br)+'" value="'+str(br)+'" class="ml-2 common_selector brand"> <label class="ml-2 fontcabin">'+str(br)+'</label></div>')
    elif subcateg != []:	

        query = query.filter(product_Subcategory__name__in=subcateg)
        brand_to_send = query.values_list("brand", flat=True).distinct()

        for brand in brand_to_send:
            brand_list.append(brand)

        for br in brand_list:
            if br in brands:
                str3_send = (str3_send
                            +'<div class="row"> <input type="checkbox" checked name="'+str(br)+'" value="'+str(br)+'" class="ml-2 common_selector brand"> <label class="ml-2 fontcabin">'+str(br)+'</label></div>')
            else:
                str3_send = (str3_send
                            +'<div class="row"> <input type="checkbox"  name="'+str(br)+'" value="'+str(br)+'" class="ml-2 common_selector brand"> <label class="ml-2 fontcabin">'+str(br)+'</label></div>')	
    else:	
        query = query.filter(product_Category__name__in=categ)
        brand_to_send = query.values_list("brand", flat=True).distinct()

        for brand in brand_to_send:
            brand_list.append(brand)
        for br in brand_list:
            if br in brands:
                str3_send = (str3_send
                            +'<div class="row"> <input type="checkbox" checked name="'+str(br)+'" value="'+str(br)+'" class="ml-2 common_selector brand"> <label class="ml-2 fontcabin">'+str(br)+'</label></div>')
            else:
                str3_send = (str3_send
                            +'<div class="row"> <input type="checkbox"  name="'+str(br)+'" value="'+str(br)+'" class="ml-2 common_selector brand"> <label class="ml-2 fontcabin">'+str(br)+'</label></div>')	

    return HttpResponse(str3_send)

@csrf_exempt
def specifications_fetch(request):
    categ = request.POST.getlist("category[]")
    subcateg = request.POST.getlist("subcategories[]")
    supcateg = request.POST.getlist("supcategories[]")
    brands = request.POST.getlist("brands[]")	
    specifications = request.POST.getlist("specifications[]")
    # query = product.objects.all()	
    str4_send = ""

    
    label = labels_Attributes.objects.filter(sub_category__name__in=subcateg)
    for lab in label:
        val= lab.values
        lab_val = val.split(",")
        if lab_val != ['']:		
            str4_send = (str4_send
                +'<div class="row pt-2 filters_name" style="border-top: 1px solid rgba(0,0,0,0.3)"><h6><b>'+str(lab.name)+' </b></h6></div><div class="row filters_brand"><div class="container">')

            for value in lab_val:
                if value in specifications:
                    str4_send = (str4_send
                                    +'<div class="row"><input type="checkbox" checked name="'+str(value)+'" value = "'+str(value)+'" class="ml-2 common_selector specifications"><label class="ml-2 fontcabin">'+str(value)+'</label></div>')
                else:
                    str4_send = (str4_send
                                    +'<div class="row"><input type="checkbox" name="'+str(value)+'" value = "'+str(value)+'" class="ml-2 common_selector specifications"><label class="ml-2 fontcabin">'+str(value)+'</label></div>')					
            str4_send= (str4_send
                        +'</div></div>')

    return HttpResponse(str4_send)	

@csrf_exempt
def fetch_page(request):
    categ = request.POST.getlist("category[]")
    subcateg = request.POST.getlist("subcategories[]")
    supcateg = request.POST.getlist("supcategories[]")
    specifications = request.POST.getlist("specifications[]")
    page = request.POST.get("page")
    brands = request.POST.getlist("brands[]")
    rate = request.POST.get("rate[]")
    min_price = request.POST.get("min_price")
    max_price = request.POST.get("max_price")
    query = product.objects.all()
    str5_send =''
    
    if request.user.is_authenticated:
        onclick_cart = "cart_auth"
    else:
        onclick_cart = "cart_un_auth"
    if categ != []:
        query = query.filter(product_Category__name__in=categ)
    if subcateg != []:
        query = query.filter(
            product_Subcategory__name__in=subcateg
        )
    if supcateg != []:
        query = query.filter(
            product_Supercategory__name__in=supcateg
        )
    if brands != []:
        query = query.filter(brand__in=brands)

    if specifications:
        # specifications = [' 8 GB ', ' 12 GB ']
        prod_list = []
        label_specific = label_Attributes_Values.objects.filter(value__in= specifications)

        # for pro in label_specific:
        prod_list.append(label_specific.values('prod'))

        #for prod in prod_list: 	
        query= query.filter(product_code__in = prod_list)		
    if rate:
        query = query.filter(price__range=(min_price, max_price))		
    # query = query.filter(Q(price__gte=rate))
    # page = 1
    if query.count() == 0:

        return HttpResponse(str5_send)

    else:
        if page is None:
            page =1
        paginator = Paginator(query, 40)
        query = paginator.get_page(page)
        
        if query.has_other_pages:
            str5_send = ( str5_send 
                        + '<ul class="pagination">')
            # if query.has_previous:
            cast = int(page)
            if cast>1:
                previous= cast-1
                check=query.previous_page_number
                print(check)
                str5_send = ( str5_send 
                            + '<li class="page-item"><span class="page-link" text="'+str(previous)+'">&laquo;</span></li>')		
            else:
                str5_send = ( str5_send 
                            + '<li class="page-item"><span class="page-link" text="'+str(page)+'">&laquo;</span></li>')				

            for i in query.paginator.page_range:
                if query.number == i:
            
                    str5_send = ( str5_send 
                                + '<li class="page-item active"><span  class ="page-link active" text="'+str(i)+'">'+str(i)+'</span></li>')
                else:
                    str5_send = ( str5_send 
                                + '<li class="page-item"><span class="page-link" text="'+str(i)+'">'+str(i)+'</span></li>')
            # if query.has_next:
            
            if cast>=1:
                next_page=cast+1
                
                str5_send = ( str5_send 
                            + '<li class="page-item"><span class="page-link" text="'+str(next_page)+'">&raquo;</span></li>')								
            
            str5_send = ( str5_send 
                        + '</ul>')

            return HttpResponse(str5_send)	

@csrf_exempt
def fetch_pricerange(request):
    categ = request.POST.getlist("category[]")

    slider= category.objects.filter(name__in=categ)
    slider_price= slider.aggregate(maxprice=Max('higher_price'))['maxprice']
        
    slider_range = slider.filter(higher_price=slider_price)	

    for i in slider_range:
        higher_price=i.higher_price
        price_range =i.price_range

    return JsonResponse({'higher_price': higher_price,'price_range': price_range})	
        
 
@csrf_exempt
def fetch(request):
    categ = request.POST.getlist("category[]")
    subcateg = request.POST.getlist("subcategories[]")
    supcateg = request.POST.getlist("supcategories[]")
    specifications = request.POST.getlist("specifications[]")
    brands = request.POST.getlist("brands[]")
    rate = request.POST.get("rate[]")
    page = request.POST.get("page")	
    sort = request.POST.get("sort")
    min_price = request.POST.get("min_price")
    max_price = request.POST.get("max_price")
    is_user_vendor = False
    if request.user.is_authenticated and detail.objects.get(email=request.user.email).vendor == True:
        is_user_vendor = True
    # if is_user_vendor:
    #     # query = product.objects.filter(b2b_product = True) # B2BCHECKBOX
    #     b2bTag = labels_Object.objects.get(name='B2B')
    #     query = product.objects.filter(product_tags = b2bTag)
    # else:
    #     # query = product.objects.filter(b2c_product = True) # B2BCHECKBOX
    #     b2cTag = labels_Object.objects.get(name='B2C')
    #     query = product.objects.filter(product_tags = b2cTag)
    query=product.objects.all()
    if request.user.is_authenticated:
        onclick_cart = "cart_auth"
    else:
        onclick_cart = "cart_un_auth"
    if categ != []:
        categ_ids=[]
        for i in categ:
            cate = category.objects.get(name=i)
            categ_ids.append(cate.id)
        query = query.filter(product_Category__in=categ_ids)

    if subcateg != []:
        subcateg_ids=[]
        for i in subcateg:
            subcate = sub_category.objects.get(name=i)
            subcateg_ids.append(subcate.id)
        query = query.filter(
            product_Subcategory__in=subcateg_ids
        )
    if supcateg != []:
        supcateg_ids=[]
        for i in supcateg:
            supcate = super_category.objects.get(name=i)
            supcateg_ids.append(supcate.id)
        query = query.filter(
            product_Supercategory__in=supcateg_ids
        )
    if brands != []:
        query = query.filter(brand__in=brands)

    if specifications:
        # specifications = [' 8 GB ', ' 12 GB ']
        prod_list = []
        label_specific = label_Attributes_Values.objects.filter(value__in= specifications)

        # for pro in label_specific:
        prod_list.append(label_specific.values('prod'))

        #for prod in prod_list: 	
        query= query.filter(product_code__in = prod_list)		
    if rate:
        query = query.filter(price__range=(min_price, max_price))		
    # query = query.filter(Q(price__gte=rate))
    query = query.order_by("price")
    if sort == "1":
        query = query.order_by("price")
    elif sort == "2":
        query = query.order_by("-price")	
    if page is None:
        page =1	
    paginator = Paginator(query, 40)
    query = paginator.get_page(page)	
    str_to_send = ""
    print("query= ",query)
    for que in query:
        print(que.product_code,que.image1)
        if que.image1=="":
            str_to_send = (
                str_to_send
                +'''
    <div class="col-6 col-xs-6 col-sm-4 col-md-3 col-lg-3 mb-4 product_card">
    <div>
    <div class="container-fluid">
        <div class="row">
            <div class="product_image">
                <a href="/products/'''+str(que.slug)+'''">
                    <img class="prod-image" src="'''+ str(que.product_code)+ '''" id="'''+ str(que.slug)+'''" onclick="detailpage();" onerror="this.src='/static/img/noimage.jpg'" alt="">
                </a>
            </div>
        </div>
    </div>
    <div class="row">
        <a href="/products/'''+ str(que.slug)+'''">
            <b>
                <h6  onclick="detailpage() class="ml-4 mt-2 fontcabin" id="name'''+ str(que.product_code)+'''">
                    '''+ str(que.title)+ '''
                </h6>product
            </b>
        </a>
        <br>
        <br>
    </div>
    <div class="row">
        <b>
            <h6 class="ml-4 fontcabin" style="color: grey" id="price'''+ str(que.product_code)+'''">
                Rs'''+ str(que.price)+'''
            </h6>
        </b>
    </div>
    <button id="'''+ str(que.product_code)+'''" data-action="add" class="btn-sm btn-dark" onclick="'''+onclick_cart+'''('''+str(que.product_code)+''');">
        <b>Add to Cart</b>
    </button>
</div>
</div>'''
                )

        else: 
            mrp_update = que.price
            if is_user_vendor:
                offer_update = que.B2Boffer
            else:
                offer_update = que.offer
            price_update = mrp_update-(mrp_update * offer_update // 100)
            str_to_send = (
                str_to_send
                + '''<div class="col-6 col-xs-6 col-sm-4 col-md-3 col-lg-3 product_card"><div><div class="container-fluid"><div class="row"><div class="product_image"><a href="/products/'''
                + str(que.slug)
                + '''"><img class="prod-image" src="'''
                + str(que.image1.url)
                + '''" id="'''
                + str(que.slug)
                + '''" onclick="detailpage();" onerror="this.src='/static/img/noimage.jpg'" alt=""></a></div></div></div><div class="row"><a href="/products/'''
                + str(que.slug)
                +'''"><b><h6 class="ml-3 mt-2 fontcabin p-1" onclick="detailpage()" id="name'''
                + str(que.product_code)
                + '''">'''
                + str(que.title)
                + '''</h6></b></a></div><div class="row"><b><h5 class="ml-3 fontcabin" style="color: #27ae60; font-weight: 550 " id="price'''
                + str(que.product_code)
                + '''">Rs. '''+str(price_update)+ '<i class="product-mrp"> MRP : '''
                + str(que.price)
                + '''</i> <span class="product-offer" style=color:#30c5ff>('''+str(que.offer)+
                '% off )*</span></h5></b></div><button id="'''
                + str(que.product_code)
                + '''" data-action="add" class="btn-sm btn-block btn-dark" onclick="'''+onclick_cart+'''('''
                +str(que.product_code)
                +''');"><b>Add to Cart</b></button></div></div>'''
                )
    return HttpResponse(str_to_send)



def products(request):
    selected = []
    cate_bool = True
    sub_bool = False
    sup_bool = False
    cate_to_send = []
    sub_to_send = []
    sup_to_send = []
    if request.user.is_authenticated:
        customer = request.user.email
        if not detail.objects.filter(email=customer).exists():
            userprofile = detail(name=customer, email=customer)
            userprofile.save()
        # if not Customer.objects.filter(email=customer).exists():
        #     a = Customer(name=customer, email=customer)
        #     a.save()
        # cus_id = Customer.objects.filter(email=customer).values("id")[0]["id"]
        # order, created = Order.objects.get_or_create(customer_id=cus_id, complete=False)
        # """if not Order.objects.filter(customer_id=cus_id).exists():
        # 	b=Order(customer_id=cus_id,complete=False)
        # 	b.save()"""
        # items = order.orderitem_set.all()
        # cartItems = order.get_cart_items

    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]
    if request.GET.get("cate"):
       
        cate = request.GET.get("cate").replace("aanndd", "&")
        print("cate ", cate)
        sub = request.GET.get("sub")
        brand = request.GET.get("brand")	
        
        if sub:
            sub.replace("aanndd", "&")

        sup = request.GET.get("sup")
        if sup:
            sup.replace("aanndd", "&")
        
        try:
            
            cate = category.objects.get(name=cate)
            print("cate2=",cate)
           
        except:
            # return redirect('/')
            pass
    
        if sub:
            try:
                
                sub = sub_category.objects.get(name__contains=sub)
                
            except:
                # return redirect('/')
                pass
        if sup:
            try:
                sup = super_category.objects.get(
                    name__icontains=sup
                )
                # sup = super_category.objects.get(
                #     name__icontains=sup, product_Category=cate, product_Subcategory=sub
                # )
            except:
                pass
        
        if sub and sup:
            sub_bool = True
            sup_bool = True
            sub_to_send = sub_category.objects.filter(
                product_Category__name__contains=cate.name
            )
            sup_to_send = super_category.objects.filter(
                product_Subcategory__name__contains=sub.name
            )
            selected.append(cate.name)
            selected.append(sub.name)
            selected.append(sup.name)
            query = product.objects.filter(
                product_Category=cate,
                product_Subcategory=sub,
                product_Supercategory=sup,
            )
        
        elif sub:
            
            selected.append(cate.name)
            sub_bool = True
            sup_bool = True			
            sub_to_send = sub_category.objects.filter(
                name__contains=sub
            )
            print("sub=",sub_to_send)
            # sup_to_send = super_category.objects.filter(product_Subcategory__name__contains=sub)
            selected.append(sub_to_send[0].name)
            for su in sub_to_send:
                temp = sub_category.objects.get(id=su.id)
                if product.objects.filter(product_Subcategory=su).exists():
                    query = product.objects.filter(product_Category__in=su.product_Category.all())
                
            
            print("selected", query)
        elif sup:
            # selected.append(cate.name)
            sup_bool = True
            # sup_to_send = super_category.objects.filter(
            #     product_Category__name__contains=cate.name
            # )
            sup_to_send = super_category.objects.filter(
                name__contains=sup
            )
            selected.append(sup_to_send[0].name)
            for supe in sup_to_send:
                 if product.objects.filter(product_Supercategory=supe).exists():
                    query = product.objects.filter(product_Category=supe.product_Category.name)
                

          
        else:

            print(cate)
            selected.append(cate.name)
            sub_to_send = sub_category.objects.filter(product_Category__name__contains=cate.name)
            sup_to_send = super_category.objects.filter(product_Category__name__contains=cate.name)			
            sub_bool = True
            sup_bool = True			
            cate_bool = True
            cate_to_send = category.objects.all()
            query = product.objects.filter(product_Category=cate)
        
        if brand:
            selected.append(brand)			
        cate_to_send = category.objects.all()
        filter_cate = filter_Categories.objects.get(name="Price")
        filter_price = filter_Objects.objects.filter(filter_category=filter_cate)
        filter_cate = filter_Categories.objects.get(name="Color")
        filter_color = filter_Objects.objects.filter(filter_category=filter_cate)
        rate = query.all().order_by("-price")
        if not rate:
            high_rate = 0
        else:
            high_rate = rate[0].price
        brand_to_send = query.values_list("brand", flat=True).distinct()
        marketid = []
        new_pro = []
        product_market_id = []
        product_market_name = []
        for item in query:
            x = item.product_Category.all()
            for i in x:
                if i not in product_market_id:
                    product_market_id.append(i.id)
        for i in product_market_id:
            pro_name = category.objects.filter(id=i).values('name')[0]['name']
            new_pro.append(pro_name)
        slider= category.objects.filter(name__in=new_pro)
        slider_price= slider.aggregate(maxprice=Max('higher_price'))['maxprice']
        
        slider_range = slider.filter(higher_price=slider_price)
        is_user_vendor=False
        if request.user.is_authenticated and detail.objects.get(email=request.user.email).vendor == True:
            is_user_vendor = True		
        data = {
            "obj": query,
            "empty": False,
            "price": filter_price,
            "color": filter_color,
            "cate": cate,
            "rate": high_rate,
            "sub": sub,
            "sup": sup,
            "brands": brand_to_send,
            "cate_print": cate_bool,
            "slider_range": slider_range,
            "sub_print": sub_bool,
            "sup_print": sup_bool,
            "categories": cate_to_send,
            "subcategories": sub_to_send,
            "supcategories": sup_to_send,
            "checked": selected,
        }
        cartItems = {}

        if query.count() < 1:
            data["empty"] = True
        return render(
            request,
            "products/productlistview.html",
            {"data": data, "cartItems": cartItems, "is_user_vendor": is_user_vendor},
        )
    else:
        return redirect("/")

def updateItems(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    customer = request.user.email
    productitem = product.objects.get(product_code=productId)

    # print('prod:',productitem)
    cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
    order, created = Order.objects.get_or_create(customer_id=cus_id, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=productitem)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item added',safe=False)

import random

from product.models import recently_viewed, product_common_attribute_values




def productdetails(request,slug):
    query=product.objects.get(slug=slug)
    query1=query.product_Supercategory.get().attributes.all()
    isAvailableForSubscription = query.available_for_subscription
    size_color_quantity_obj = size_color_quantity.objects.filter(linked_product=query)
    for i in size_color_quantity_obj:
        print("holaa",i.size)
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
    tempSize = set(sizes)
    print('TEMP SIZE {}'.format(tempSize))
    sizes = list(tempSize)
    print('THIS IS SIEZES {}'.format(sizes))
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
    # if request.user.is_authenticated:
        #OLDCART
    # 	items=CartItems.objects.filter(email=request.user.email).values('items')[0]['items']
    # #print(prod_id)
    # 	obj=wishlist.objects.filter(email=request.user.email,product_code=prod_id)
    # 	if obj:
    # 		wish="true"
    # 	else:
    # 		wish="false"

    objimg=Add_images.objects.filter(prod=query,size__isnull = True)
    images=[]
    print(objimg.values())
    for i in objimg:
        images.append(i)

    min_start_date = datetime.date.today() + datetime.timedelta(days = 1)
    is_user_vendor = False
    if request.user.is_authenticated and detail.objects.get(email=request.user.email).vendor == True: is_user_vendor = True
    data={
        "obj":query,
        "data":li,
        "similiar":query5,
        "sizes":size_color_quantity_obj,
        "recent":re,
        "tred":tred,
        "attributes":attributes,
        "product_code":prod_id,
        "wishlist":wish,
        "images":images,
        'isAvailableForSubscription': isAvailableForSubscription,
        'min_start_date': min_start_date,
        "is_user_vendor": is_user_vendor,				
    }
    # product_price(base_price for quantity = 1)
    product_instance = product.objects.filter(slug=slug).first()
    data['amount'] = data['base_price'] = product_instance.price
    data['unit_of_measurement'] = product_instance.unit_of_measurement
    if isAvailableForSubscription:
        data['discount'] = product_instance.subscription_discount
        data['amount'] = data['base_price'] = product_instance.price*((100 - data['discount'])/100)
        print('********************************************************')
        print(data['discount'])

    # Other seller
    other_sellers = product.objects.exclude(pk=product_instance.pk).filter(title = product_instance.title)
    data['other_sellers'] = other_sellers


    import re
    if request.POST.get('sizes_ajax'):
        val=request.POST.get('sizes_ajax')
        print('This are sizes to color: {}'.format(val))
        temp = val.split()
        size_int = temp.pop(0)
        size_int = int(size_int)
        size_unit = ' '.join(temp)
        size_objects = size_color_quantity.objects.filter(linked_product=product_instance, size=size_int)
        cols=[]
        print("THESE ARE SIZE OBJ: {}".format(size_objects))
        for size_object in size_objects:
            if size_object.quantity!=None:
                cols.append(size_object.color)
        print("cols ",cols)
        return JsonResponse({"data":cols})
    if request.POST.get('size_value'):
        size_value = request.POST.get('size_value')
        size_int = size_value.split()
        size_int = int(size_int[0])
        color_value = request.POST.get('color_value')
        print("THIS IS REQUESTED SIZE {} & COLOR {}".format(size_value,color_value))
        size_object = size_color_quantity.objects.filter(linked_product=product_instance, size=size_int, color=color_value).first()
        color_images = Add_images.objects.filter(prod=product_instance, size=size_object)
        image_urls = []
        if len(color_images) > 0:
            for image in color_images:
                image_urls.append(image.image.url)
        print('THIS IS PRICE: {}'.format(size_object.price))
        return JsonResponse({"data":size_object.price , "images": image_urls})

    currProduct = product.objects.get(slug=slug)
    AllReviews = ProductReview.objects.filter(product=currProduct)
    data['all_reviews'] = AllReviews
    print("INITITAL ALL REVIEWS: {}".format(AllReviews))
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        OldReview = ProductReview.objects.filter(product=currProduct,user=details).first()
        if OldReview:
            data['old_review'] = OldReview
            AllReviews = ProductReview.objects.exclude(product=currProduct,user=details)
            data['all_reviews'] = AllReviews.filter(product=currProduct)
        else:
            AllReviews = ProductReview.objects.filter(product=currProduct)
            data['all_reviews'] = AllReviews
        print("931 ALL REVIEWS: {}".format(AllReviews))
        # if request.method == "POST":
        if request.POST.get("star"):
            OldReview = ProductReview.objects.filter(product=currProduct,user=details).first()
            if OldReview:
                OldReview.stars = int(request.POST.get("star"))
                OldReview.description = request.POST.get("review_description")
                if 'review_image' in request.FILES:
                    OldReview.review_image = request.FILES['review_image']
                OldReview.save()
            else:
                review_description = request.POST.get("review_description")
                stars = int(request.POST.get("star"))
                if 'review_image' in request.FILES:
                    image = request.FILES['review_image']
                    review = ProductReview(user=details, description=review_description, product=currProduct, stars=stars, review_image=image)
                else:
                    review = ProductReview(user=details, description=review_description, product=currProduct, stars=stars)
                review.save()
                currProduct.product_total_reviews += 1
            averageStars = ProductReview.objects.filter(product=currProduct).aggregate(Avg('stars'))
            temp_stars = round(averageStars.get('stars__avg'),1)
            currProduct.product_stars = temp_stars
            currProduct.save() 
            return redirect(f'/products/{currProduct.slug}/')
    print("FINAL ALL REVIEWS: {}".format(AllReviews))
    print("\n\n\nFINAL DATA: {}\n\n\n".format(data))
    return render(request,'products/productdetailview.html',context=data)



#some codee


# pom_objs=POM.objects.filter(product_Supercategory=None)
# for i in pom_objs:
# 	to_be=super_category.objects.filter(product_Subcategory=i.product_Subcategory)
# 	for j in to_be:
# 		new_obj=POM(
# 			label=i.label,
# 			product_Category=i.product_Category,
# 			product_Subcategory=i.product_Subcategory,
# 			product_Supercategory=j,
# 			admin_Tolerance=i.admin_Tolerance,
# 			half_length=i.half_length,
# 			show_to_Customer=i.show_to_Customer,
# 			max_Value=i.max_Value,
# 			min_Value=i.min_Value
# 		)
# 		new_obj.save()
# for j in pom_objs:
    # j.delete()

#
# def society():
# 	pom_objs=POM.objects.filter(product_Supercategory=None)
# 	count=0
# 	for i in pom_objs:
# 		to_be=super_category.objects.filter(product_Subcategory=i.product_Subcategory)
# 		for j in to_be:
# 			new_obj=POM(
# 				label=i.label,
# 				product_Category=i.product_Category,
# 				product_Subcategory=i.product_Subcategory,
# 				product_Supercategory=j,
# 				admin_Tolerance=i.admin_Tolerance,
# 				half_Length=i.half_Length,
# 				show_to_Customer=i.show_to_Customer,
# 				max_Value=i.max_Value,
# 				min_Value=i.min_Value
# 			)
# 			new_obj.save()
# 			count+=1
# 	print(count)
# 	count=0
# 	for j in pom_objs:
# 		j.delete()
# 		count+=1
# 	print(count)






from .models import attribute, product_common_attribute_values, product_cate_b2b,size_color_quantity,labels_Object,labels_Attributes,label_Attributes_Values,safety_stock,units
from product.models import label_dropdowns
from seller_info.models import washcares,barcodes

def upload_product(request):
    if request.user.is_authenticated:
        details=detail.objects.get(email=request.user.email)
        if details.vendor or details.staff or details.buisness_Customer or details.customer:
            seller_id=detail.objects.filter(email=request.user.email).values('seller_category__id')[0]['seller_category__id']
            cate=category.objects.filter(seller_cat__id=seller_id).all()
            b2b_cate = product_cate_b2b.objects.all()
            prod_cate=product_cate_b2b.objects.all()
            label=labels_Object.objects.filter(seller_Categories__id=seller_id)
            dependent_commons = attribute.objects.filter(seller_Categories__id=seller_id).all().order_by("id")
            #attribute_values=label_dropdowns.objects.all()
            otcolors=['AliceBlue','AntiqueWhite','Aqua','Aquamarine','Azure','Bisque','BlanchedAlmond','BlueViolet','BurlyWood','CadetBlue','Chartreuse','Chocolate','Coral','CornflowerBlue','Cornsilk','Crimson','DarkBlue','DarkCyan','DarkGoldenRod','DarkGray','DarkGrey','DarkGreen','DarkKhaki','DarkMagenta','DarkOliveGreen','DarkOrange','DarkOrchid','DarkRed','DarkSalmon','DarkSeaGreen','DarkSlateBlue','DarkSlateGray','DarkSlateGrey','DarkTurquoise','DarkViolet','DeepPink','DeepSkyBlue','DimGray','DimGrey','DodgerBlue','FireBrick','FloralWhite','ForestGreen','Fuchsia','Gainsboro','GhostWhite','Gold','GoldenRod','Grey','GreenYellow','HoneyDew','HotPink','IndianRed','Indigo','Ivory','Khaki','Lavender','LavenderBlush','LawnGreen','LemonChiffon','LightBlue','LightCoral','LightCyan','LightGoldenRodYellow','LightGray','LightGrey','LightGreen','LightPink','LightSalmon','LightSeaGreen','LightSkyBlue','LightSlateGray','LightSlateGrey','LightSteelBlue','LightYellow','Lime','LimeGreen','Linen','MediumAquaMarine','MediumBlue','MediumOrchid','MediumPurple','MediumSeaGreen','MediumSlateBlue','MediumSpringGreen','MediumTurquoise','MediumVioletRed','MidnightBlue','MintCream','MistyRose','Moccasin','NavajoWhite','Navy','OldLace','Olive','OliveDrab','OrangeRed','Orchid','PaleGoldenRod','PaleGreen','PaleTurquoise','PaleVioletRed','PapayaWhip','PeachPuff','Peru','Plum','PowderBlue','RebeccaPurple','RosyBrown','RoyalBlue','SaddleBrown','Salmon','SandyBrown','SeaGreen','SeaShell','Sienna','Silver','SkyBlue','SlateBlue','SlateGray','SlateGrey','Snow','SpringGreen','SteelBlue','Tan','Teal','Thistle','Tomato','Turquoise','Wheat','WhiteSmoke','YellowGreen']
            majcolors=['Black','Blue','Beige','Brown','Green','Orange','Pink','Purple','Red','Violet','Yellow','White','Magenta','Maroon','Cyan','Gray']
            cont=[]
            objatt=[]
            #diction={}
            #diction={}
            if label !=None:
                for i in label:
                    objs=labels_Attributes.objects.filter(label=i,seller_Categories=seller_id)
                    objs=list(objs.values())
                    diction=[i,objs]
                    cont.append(diction)
                #print(diction['id'],diction['obj'])
            #id_sub_cate=0
            #super_cat_obj=[]
            sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
            brands=detail.objects.filter(activate_Seller=True,seller_category=seller_id)
            if details.vendor and details.seller_category.name=="Products Vendor":
                brands=[details]
            service=detail.objects.filter(email=request.user.email).values('service')[0]['service']
            if service==False:
                vendor_servive=False
            else:
                vendor_servive=True
            seller_d=detail.objects.filter(email=request.user.email).values('seller_category_id')[0]['seller_category_id']
            super_cat=super_category.objects.filter(seller_cat__id=seller_d).all()
            product_group_obj=product_group_type.objects.all()
            units= all_units.objects.filter(seller_Categories__id=seller_id,detail=details).order_by('unit')
            units_list=[]
            for i in units:
                units_list.append(i.unit)

            pieces_per_unit=False
            color_exits=False
            prices_exist=False
            stock_info_exists=False
            otherbrands= OtherBrands.objects.filter(seller_Categories=seller_id).order_by('brand')
            data={
            "cate":cate,
            "prod_cate":prod_cate,
            "label":label,
            "cont":cont,
            "brands":brands,
            "details":details,
            #"attribute_values":attribute_values,
            "dependent_commons":dependent_commons,
            "majcolors":majcolors,
            "otcolors":otcolors,
            "b2b_cate": b2b_cate,
            "vendor_servive":vendor_servive,
            'super_cat':super_cat,
            'product_group_obj':product_group_obj,
            "units":units_list,
            "cont":cont,
            "otherbrand":otherbrands,
            "options":option_tags.objects.all(),
            }

            #AutoFill Title
            if request.POST.get('title_search'):
                results = []
                queryset = product.objects.all()
                strings = request.POST['title_search']
                for string in strings:
                    queryset = queryset.filter(title__icontains=string)
                for r in queryset:
                    results.append(r.title)
                return JsonResponse({"data":results,})
            
            # Autofill Form
            if request.POST.get('title_value'):
                title = request.POST.get('title_value')
                upload_product = product.objects.filter(title=title).first()
                label_attrs = label_Attributes_Values.objects.filter(prod=upload_product)
                label_data = []
                for label_attr in label_attrs:
                    label_data.append([label_attr.label_attribute.id, label_attr.value])
                print("This is label Data: {}".format(label_data))
                data = {}
                if upload_product:
                    data["notes"] = upload_product.notes
                    data["description"] = upload_product.description
                    data["terms"] = upload_product.terms
                return JsonResponse({"data":data,"label_data": label_data})


            if request.POST.get('product_group_type'):
                type_id=product_group_type.objects.filter(type=request.POST.get('product_group_type')).values('id')[0]['id']
                categories_group=developer_attributes.objects.filter(product_group_type=type_id,detail=details)
                print(categories_group)
                bol=False
                if categories_group.count()>0:
                    bol=True
                
                list_obj=[]
                for i in categories_group:
                    lr=[i.attributes,i.input_type]
                    if i.values!= None:
                        lr.append(i.values)
                    list_obj.append(lr)


                return HttpResponse(json.dumps({'data': list_obj,'bol':bol}), content_type="application/json")

            if request.POST.get('brand_ajax_cate'):
                vendor_obj=detail.objects.filter(email=request.POST.get('brand_ajax_cate')).first()
                label_obj=labels.objects.filter(vendor=vendor_obj)
                bol=False
                if label_obj.count()>0:
                    bol=True
                # print("wor",label_obj)
                label_obj=list(label_obj.values())
                return HttpResponse(json.dumps({'data': label_obj,'bol':bol}), content_type="application/json")

            if request.POST.get('brand_ajax_cate_other'):
                otherbrands=OtherBrands.objects.filter(brand=request.POST.get('brand_ajax_cate_other')).first()
                #vendor_obj=detail.objects.filter(email=).first()
                label_obj=OtherLabel.objects.filter(OtherBrands=otherbrands)
                bol=False
                if label_obj.count()>0:
                    bol=True
                label_obj=list(label_obj.values())
                print("wor",label_obj)
                return HttpResponse(json.dumps({'data': label_obj,'bol':bol}), content_type="application/json")

            if request.POST.get('label_fits_ajax'):
                label_obj=labels.objects.filter(id=int(request.POST.get('label_fits_ajax'))).first()
                fits_obj=fits.objects.filter(label=label_obj)
                bol=False
                if fits_obj.count()>0:
                    bol=True
                fits_obj=list(fits_obj.values())
                return HttpResponse(json.dumps({"data":fits_obj,"bol":bol}), content_type="application/json")
            if request.POST.get('fits_season_ajax'):
                label_obj=fits.objects.filter(id=int(request.POST.get('fits_season_ajax'))).first()
                # print(label_obj)
                fits_obj=seasons.objects.filter(fit=label_obj)
                bol=False
                if fits_obj.count()>0:
                    bol=True
                fits_obj=list(fits_obj.values())
                return HttpResponse(json.dumps({"data":fits_obj,"bol":bol}), content_type="application/json")
            if request.POST.get('season_washcare_ajax'):
                label_obj=seasons.objects.filter(id=int(request.POST.get('season_washcare_ajax'))).first()
                # print(label_obj)
                superc=super_category.objects.filter(id=int(request.POST.get('season_supercategory_ajax'))).first()
                meas=measurement.objects.filter(product_Supercategory=superc,season=label_obj,user=label_obj.vendor).first()
                if meas:
                    meas=meas.measurement_chart_set.all()
                else:
                    meas=[]
                sizes=[]
                for i in meas:
                    if not(i.size in sizes):
                        sizes.append(i.size)
                washcare_obj=washcare_model.objects.filter(product_Supercategory=superc)
                barcode_obj=barcodes.objects.filter(season=label_obj)
                print(washcare_obj)
                bol=False
                if washcare_obj.count()>0:
                    bol=True
                washcare_obj=[str(washcare) for washcare in washcare_obj]
                print(washcare_obj)
                barcode_obj=list(barcode_obj.values())
                # print(barcode_obj)
                return HttpResponse(json.dumps({"data":washcare_obj,"barcode":barcode_obj,"bol":bol,"sizes":sizes}), content_type="application/json")
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
                newid=request.POST.get('id_ajax_subcate_cate')
                cate_obj=category.objects.get(id=newid)
                obj1=sub_category.objects.filter(id=id1).first()
                id_sub_cate=id1
                obj1=super_category.objects.filter(product_Subcategory=obj1,product_Category=cate_obj)
                if obj1.count():
                    bol=True
                else:
                    bol=False
                obj1=list(obj1.values())
                return HttpResponse(json.dumps({'data': obj1,'bol':bol}), content_type="application/json")
            if request.POST.get('id_ajax_supcate'):
                id1=request.POST.get('id_ajax_supcate')
                cate_id1=request.POST.get('id_ajax_cate')
                sub_cate_id1=request.POST.get('id_ajax_subcate_cate')

                #cate=category.objects.filter(id=request.POST.get('id_ajax_cate')).first()
                
                sup_categ=super_category.objects.get(id=id1)
                
                sub_cats=sup_categ.product_Subcategory.all()
                
                for i in sub_cats:
                    sub_cat_id=i.id
                    print(sub_cat_id)
                    categs = i.product_Category.all()
                    for j in categs:
                        cate_id=j.id
                    #print(i)
                    #print(sub_cat_id)
                    
                #subcate=sub_category.objects.filter(id=int(sub_cat_id)).first()
                obj1=super_category.objects.filter(id=id1).first()
                #print(id1,sub_cat_id,cate_id)
                saf=safety_stock.objects.filter(vendor=details,product_Supercategory=obj1).first()
                if saf:
                    saf=saf.limit
                else:
                    saf=1

                obj1=obj1.attributes.all()
                
                if obj1.count():
                    bol=True
                else:
                    bol=False
                objatt=list(obj1.values())
                cont=[]
                objlist=[]
                label=labels_Object.objects.all()
                for i in label:
                    #print(i)
                    objs=labels_Attributes.objects.filter(label=i,seller_Categories=seller_id)
                    #print(objs)
                    objs_value=list(objs.values())
                    flag=0
                    for item in objs:

                        #print(item.values())
                        if item!=None:
                            categories=(item.category.all())
                            sub_categories=item.sub_category.all()
                            sup_categories=item.super_category.all()

                        for i in categories.values():
                            if i['id']==cate_id:
                                flag=1
                        if flag==0:
                            continue
                        if flag==1:
                            for i in sub_categories.values():
                                if i['id']==sub_cat_id:
                                    flag=2
                        if flag==1:
                            continue
                        if flag==2:
                            for i in sup_categories.values():
                                #print(i['id'],id1)
                                if int(i['id'])== int(id1):
                                    flag=3
                        print(flag)
                        if flag==3:
                            objlist.append(str(item))

                #print(objlist)
                
                requiredparams=FormAttributes.objects.filter(seller_Categories=seller_id,detail=details)
                #print(requiredparams)
                for i in requiredparams.values():
                    pieces_per_unit=i['pieces_per_unit']
                    size_exists=i['sizes_exist']
                    color_exits=i['color_exits']
                    prices_exist=i['prices_exist']
                    stock_info_exists=i['stock_info_exists']
                    brand_exists=i['brand']
                    label=i['label']
                    images=i['images']
                    variations=i['variations']
                    otherbrand=i['otherbrand']
                    commoninfo=i['commoninfo']
                    compliance=i['compliance']
                    Description=i['Description']
                    vitalinfo=i['vitalinfo']
                    washcare=i['washcare']
                    fit=i['fit']
                    season=i['season']
                    services=i['services']

                if not requiredparams:
                    pieces_per_unit=True
                    size_exists=True
                    color_exits=True
                    prices_exist=True
                    stock_info_exists=True
                    brand_exists=True
                    label=True
                    images=True
                    variations=True
                    otherbrand=True
                    commoninfo=True
                    compliance=True
                    Description=True
                    vitalinfo=True
                    washcare=True
                    fit=True
                    season=True
                    if vendor_servive:
                        services=True
                    else:
                        services=False


                list_reqs=[pieces_per_unit,color_exits,prices_exist,stock_info_exists,brand_exists,label,images,variations,size_exists,otherbrand,commoninfo,compliance,Description,vitalinfo,fit,season]

                print(pieces_per_unit,color_exits,prices_exist,stock_info_exists,brand_exists,label,images,variations)
                return HttpResponse(json.dumps({'data': objatt,'bol':bol,'limit':saf,'reqs':list_reqs,'labels':objlist}), content_type="application/json")

            if request.POST.get('slug_ajax_prod'):
                slug=request.POST.get('slug_ajax_prod')
                obj1=product.objects.filter(slug=slug)

                if obj1.count()>0:
                    bol=False
                else:
                    bol=True
                return HttpResponse(json.dumps({'bol':bol}), content_type="application/json")

            if request.POST.get('title'):
                #print('submitted')
                print(request.POST)
                print(request.FILES)
                cate=category.objects.filter(id=int(request.POST.get('cate'))).first()
                subcate=sub_category.objects.filter(id=int(request.POST.get('sub_cate'))).first()
                supcate=super_category.objects.filter(id=int(request.POST.get('sup_cate'))).first()
                # b2b_cate=None
                # if request.POST.get('b2b_cate'):
                # 	b2b_cate=product_cate_b2b.objects.filter(id=int(request.POST.get('b2b_cate'))).first()
                
                #label_obj=labels.objects.filter(id=int(request.POST.get('label'))).first()
                #fit_obj=fits.objects.filter(id=int(request.POST.get('fit'))).first()
                #season_obj=seasons.objects.filter(id=int(request.POST.get('season'))).first()
                #if request.POST.get('washcare'):
                #	washcare_obj=washcares.objects.filter(id=int(request.POST.get('washcare'))).first()
                #else:
                #	washcare_obj=None
                #barcode_obj=barcodes.objects.filter(id=int(request.POST.get('barcode'))).first()
                product_code = (str(cate)[:2]+str(subcate)[:2]+str(supcate)[:2] +
                                    datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                print(request.POST.get('desc_up'))
                packed=request.POST.get('packed')
                service=request.POST.get('service')
                subscription=request.POST.get('subscription')
                made_in=request.POST.get('made_in')

                is_rent=request.POST.get('is_rent')
                if(is_rent ==None):
                    is_rent=False

                is_heavy=request.POST.get('is_heavy')
                if(is_heavy ==None):
                    is_heavy=False
                is_garment=request.POST.get('is_garment')
                if(is_garment==None):
                    is_garment=False
                old_product=request.POST.get('new_product')
                product_group=request.POST.get('product_group')
                quantityperunit=request.POST.get('indi_quantity')
                if product_group==None:
                    product_group="Others"
                product_group_id=product_group_type.objects.filter(type=product_group).values('id')[0]['id']
                print(product_group_id)
                label=None
                fit_obj=None
                season_obj=None
                wash_obj=None
                brandother=request.POST.get('brandother')
                if request.POST.get('fit'):
                    fit_obj=fits.objects.filter(id=int(request.POST.get('fit'))).first()
                if request.POST.get('season'):
                    season_obj=seasons.objects.filter(id=int(request.POST.get('season'))).first()

                if request.POST.get('washcare'):
                    wash_obj=washcares.objects.filter(id=int(request.POST.get('washcare'))).first()


                
                #print('brandlabel',request.POST.get('label'))
                label=None
                fit_obj=None
                season_obj=None
                wash_obj=None
                brandother=request.POST.get('brandother')
                brand=request.POST.get('brand')
                if request.POST.get('fit'):
                    fit_obj=fits.objects.filter(id=int(request.POST.get('fit'))).first()
                if request.POST.get('season'):
                    season_obj=seasons.objects.filter(id=int(request.POST.get('season'))).first()

                if request.POST.get('washcare'):
                    wash_obj=washcares.objects.filter(id=int(request.POST.get('washcare'))).first()

                options = request.POST.getlist('options')

                moq1_lb = request.POST.get('moq1_lower')
                moq1_ub = request.POST.get('moq1_upper')
                moq1_discount = request.POST.get('moq1_discount')
                Moq_range1 = (int(moq1_lb),int(moq1_ub))
                Moq_discount1 = float(moq1_discount)

                moq2_lb = request.POST.get('moq2_lower')
                moq2_ub = request.POST.get('moq2_upper')
                moq2_discount = request.POST.get('moq2_discount')
                Moq_range2 = (int(moq2_lb),int(moq2_ub))
                Moq_discount2 = float(moq2_discount)

                moq3_lb = request.POST.get('moq3_lower')
                moq3_ub = request.POST.get('moq3_upper')
                moq3_discount = request.POST.get('moq3_discount')
                Moq_range3 = (int(moq3_lb),int(moq3_ub))
                Moq_discount3 = float(moq3_discount)
                
                #print('brandlabel',request.POST.get('label'))
                print(brand,brandother)
                labelother=None
                brand=None
                if brandother!="":
                    brand=brandother
                    if request.POST.get('label') !="":
                        labelother=OtherLabel.objects.filter(id=int(request.POST.get('label')))
                        print(labelother.values())
                        for m in labelother.values():
                            labelothername=m['label']
                        #print(labelothername)
                elif brand!="":
                    brand_obj=detail.objects.filter(email=request.POST.get('brand')).first()
                    print(brand_obj)
                    if brand_obj!=None:
                        brand=brand_obj.name


                label_obj=None
                if request.POST.get('label')!="":
                        if labelother!=None:
                            label_obj,created=labels.objects.get_or_create(name=labelothername,vendor=details)
                        else: 
                            label_obj=labels.objects.filter(id=int(request.POST.get('label'))).first()
                
                print(label_obj)


                # attvals=[None]*101
                # for i in objatt:
                # 	if(i.input_type=='Text'):
                # 		attvals[k]=request.POST.get('attribute'+str(k))
                #print(request.FILES.get('file-upload-input1'))
                obj=product(
                        product_code = product_code,
                        title=request.POST.get('title'),
                        slug=request.POST.get('slug'),
                        notes=request.POST.get('notes'),
                        seller=details,
                        brand=brand,
                        label=label_obj,
                        fit=fit_obj,
                        season=season_obj,
                        washcare=wash_obj,
                        #barcode=barcode_obj,
                        terms=request.POST.get('terms'),
                        description=request.POST.get('desc_up'),
                        privacy=request.POST.get('fixed_privacy'),
                        packed=packed,
                        Service=service,
                        available_for_subscription=subscription,
                        made_in=made_in,
                        old_product=old_product,
                        selling_unit=quantityperunit,
                        image1=request.FILES.get('file-upload-input1'),
                        Moq_range1 = Moq_range1,
                        Moq_discount1 = Moq_discount1,
                        Moq_range2 = Moq_range2,
                        Moq_discount2 = Moq_discount2,
                        Moq_range3 = Moq_range3,
                        Moq_discount3 = Moq_discount3,
                )
                

                obj.is_rent=is_rent
                obj.is_heavy=is_heavy
                obj.is_garment=is_garment
                obj.manufacturername=request.POST.get('ManufacturerNameC')
                obj.manufacturerno=request.POST.get('ManufacturerNoC')
                obj.volume=request.POST.get('VolumeCapacityC')
                obj.weight=request.POST.get('WeightC')
                obj.batteriesincluded=request.POST.get('BatteriesInC')
                obj.batteriesno=request.POST.get('NoofBatterisC')
                obj.wattage=request.POST.get('WattageC')
                obj.dangerousgood=request.POST.get('ApptoDangerC')
                obj.shape=request.POST.get('ShapeC')
                obj.length=request.POST.get('LenC')
                obj.width=request.POST.get('WidthC')
                obj.height=request.POST.get('heightC')
                obj.countryorigin=request.POST.get('CountryC')
                obj.pattern=request.POST.get('allpartsC')
                obj.shafttype=request.POST.get('PatternC')
                obj.features=request.POST.get('ShaftC')
                obj.style=request.POST.get('FeatureC')
                obj.graphics=request.POST.get('StyleC')
                obj.powersource=request.POST.get('GraphicsC')
                obj.occasion=request.POST.get('SpecificationsC')
                obj.noofitems=request.POST.get('PowerSourceC')
                obj.sale=request.POST.get('OccasionC')
                obj.salestartdate=request.POST.get('NoofItemsC')
                obj.saleenddate=request.POST.get('SaleC')
                obj.salediscount=request.POST.get('SaleStartC')
                obj.allparts=request.POST.get('SaleEndC')
                obj.specifications=request.POST.get('SaleDiscC')
                obj.keywords=request.POST.get('searchterms')
                '''
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
                )'''
                obj.price=int(request.POST.get('price1'))
                obj.offer=int(request.POST.get('offer'))
                obj.B2Boffer=int(request.POST.get('B2Boffer'))
                obj.save()
                obj.product_group.add(product_group_type.objects.get(id=product_group_id))
                obj.product_Category.add(category.objects.get(id=cate.id))
                obj.product_Subcategory.add(sub_category.objects.get(id=subcate.id))
                obj.product_Supercategory.add(super_category.objects.get(id=supcate.id))
                for i in options:
                    if i == "Perishable":
                        grade=request.POST.get('grade')
                        print(grade)
                        obj.grade_quality=grade
                        obj.save()
                    if i == "Subscribe":
                        obj.available_for_subscription=True
                        obj.save()
                    if i == "Rent":
                        obj.is_rent=True
                        obj.save()
                    obj.options.add(option_tags.objects.get(name=i))
                # if b2b_cate:
                # 	obj.product_cate.add(b2b_cate)
                # if request.POST.get('b2b_product'):
                # 	obj.b2b_product=True
                # if request.POST.get('b2c_product'):
                # 	obj.b2c_product=True
                # if request.POST.get('sample_product'):
                # 	obj.sample_product=True
                # obj.save()

                ####### section for gettiing the extra details #####################
                prodDesc=request.POST.get('product')
                subscription='yes'
                email=request.user.email
                add_subscription(prodDesc,subscription,email)

                prodSer=request.POST.get('productservice')
                print("prodser",prodSer)
                price=request.POST.get('serviceprice')
                # service_unit(email,price,prodSer)

                attris=developer_attributes.objects.filter(product_group_type=product_group_id,detail=details)
                print(attris)
                #extras=extradetails(prod=obj)
                new_attris={}

                index=0
                for i in attris:
                    index=index+1
                    x=request.POST.get(i.attributes)
                    print(x)
                    lt=[i.attributes,x]
                    new_attris[str(index)]=lt
                    #extras[atrriname]=i.attributes
                    #extras[valuename]=x
                    #ob=product_common_attribute_values

                for i in range(index+1,21):
                    new_attris[str(i)]=["",""]

                print(new_attris.values())
                for i in range(2,51):
                    img="file-upload-input"+str(i)
                    if request.FILES.get(img):
                        if request.POST.get("isactual" + str(i)) == 'true':
                            actual = True
                        else:
                            actual = False
                        images=Add_images(prod=obj,image=request.FILES.get(img), is_actual=actual)
                        images.save()

                extras=extradetails(prod=obj,
                    attribute1=new_attris["1"][0],
                    value1=new_attris["1"][1],
                    attribute2=new_attris["2"][0],
                    value2=new_attris["2"][1],
                    attribute3=new_attris["3"][0],
                    value3=new_attris["3"][1],
                    attribute4=new_attris["4"][0],
                    value4=new_attris["4"][1],
                    attribute5=new_attris["5"][0],
                    value5=new_attris["5"][1],
                    attribute6=new_attris["6"][0],
                    value6=new_attris["6"][1],
                    attribute7=new_attris["7"][0],
                    value7=new_attris["7"][1],
                    attribute8=new_attris["8"][0],
                    value8=new_attris["8"][1],
                    attribute9=new_attris["9"][0],
                    value9=new_attris["9"][1],
                    attribute10=new_attris["10"][0],
                    value10=new_attris["10"][1],
                    attribute11=new_attris["11"][0],
                    value11=new_attris["11"][1],
                    attribute12=new_attris["12"][0],
                    value12=new_attris["12"][1],
                    attribute13=new_attris["13"][0],
                    value13=new_attris["13"][1],
                    attribute14=new_attris["14"][0],
                    value14=new_attris["14"][1],
                    attribute15=new_attris["15"][0],
                    value15=new_attris["15"][1],
                    attribute16=new_attris["16"][0],
                    value16=new_attris["16"][1],
                    attribute17=new_attris["17"][0],
                    value17=new_attris["17"][1],
                    attribute18=new_attris["18"][0],
                    value18=new_attris["18"][1],
                    attribute19=new_attris["19"][0],
                    value19=new_attris["19"][1],
                    attribute20=new_attris["20"][0],
                    value20=new_attris["20"][1]

                    )

                extras.save()

                ###########end##########################

                for i in range(1,101):
                    if not request.POST.get('attribute'+str(i)):
                        continue
                    attr = attribute.objects.get(pk=request.POST.get('deplabel'+str(i)))
                    prod = obj
                    value = request.POST.get('attribute'+str(i))
                    prod_attr = product_common_attribute_values(
                        prod=prod, 
                        attribute=attr,
                        value=value
                    )
                    prod_attr.save()
                label=labels_Object.objects.all()
                
                for i in label:
                    if request.POST.get(str(i.id)):
                        obj.product_tags.add(i)
                        if i.name == "B2B" and request.POST.get('b2b_cate'):
                            for b2b_cate_ob in request.POST.getlist('b2b_cate'):
                                obj.product_cate.add(product_cate_b2b.objects.get(pk=b2b_cate_ob))
                for i in cont:
                    for j in i[1]:
                        print(j)
                        if request.POST.get('label_content_'+str(j['id'])):
                            print(j['id'])
                            obj59=labels_Attributes.objects.filter(id=j['id'])[0]
                            obj45=label_Attributes_Values(prod=obj,label_attribute=obj59,value=request.POST.get('label_content_'+str(j['id'])))
                            obj45.save()

                obj1=size_color_quantity(linked_product=obj,
                                        size=request.POST.get('size1'),
                                        unit=request.POST.get('unit1'),
                                        color=request.POST.get('color1'),
                                        quantity=request.POST.get('quantity1'),
                                        price=request.POST.get('price1'),
                                        c_price=request.POST.get('c_price1'),
                                        safety_stock_limit=request.POST.get('safety_stock1'),
                                        owned_by=details)
                obj1.save()
                if '1-sizeimage-1' in request.FILES.keys():
                    for l in range(1,10):
                        m = str(l)
                        if '1-sizeimage-'+m in request.FILES.keys():
                            if request.POST.get('1-isactual-'+m) == 'true':
                                actual = True
                            else:
                                actual = False
                            size_image = Add_images(prod=obj, image=request.FILES.get('1-sizeimage-'+m), size=obj1, is_actual=actual)
                            size_image.save() 
                if request.POST.get('size2'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size2')),
                    unit=request.POST.get('unit2'),
                    color=request.POST.get('color2'),
                    quantity=int(request.POST.get('quantity2')),
                    price=int(request.POST.get('price2')),
                    c_price=request.POST.get('c_price2'),
                    safety_stock_limit=request.POST.get('safety_stock2'),
                    owned_by=details)
                    obj1.save()
                    if '2-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '2-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('2-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('2-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                    
                if request.POST.get('size3'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size3')),
                    unit=request.POST.get('unit3'),
                    color=request.POST.get('color3'),
                    quantity=int(request.POST.get('quantity3')),
                    price=int(request.POST.get('price3')),
                    c_price=request.POST.get('c_price3'),
                    safety_stock_limit=request.POST.get('safety_stock3'),
                    owned_by=details)
                    obj1.save()
                    if '3-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '3-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('3-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('3-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                if request.POST.get('size4'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size4')),
                    unit=request.POST.get('unit4'),
                    color=request.POST.get('color4'),
                    quantity=int(request.POST.get('quantity4')),
                    price=int(request.POST.get('price4')),
                    c_price=request.POST.get('c_price4'),
                    safety_stock_limit=request.POST.get('safety_stock4'),
                    owned_by=details)
                    obj1.save()
                    if '4-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '4-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('4-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('4-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                if request.POST.get('size5'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size5')),
                    unit=request.POST.get('unit5'),
                    color=request.POST.get('color5'),
                    quantity=int(request.POST.get('quantity5')),
                    price=int(request.POST.get('price5')),
                    c_price=request.POST.get('c_price5'),
                    safety_stock_limit=request.POST.get('safety_stock5'),
                    owned_by=details)
                    obj1.save()
                    if '5-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '5-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('5-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('5-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                if request.POST.get('size6'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size6')),
                    unit=request.POST.get('unit6'),
                    color=request.POST.get('color6'),
                    quantity=int(request.POST.get('quantity6')),
                    price=int(request.POST.get('price6')),
                    c_price=request.POST.get('c_price6'),
                    safety_stock_limit=request.POST.get('safety_stock6'),
                    owned_by=details)
                    obj1.save()
                    if '6-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '6-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('6-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('6-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                if request.POST.get('size7'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size7')),
                    unit=request.POST.get('unit7'),
                    color=request.POST.get('color7'),
                    quantity=int(request.POST.get('quantity7')),
                    price=int(request.POST.get('price7')),
                    c_price=request.POST.get('c_price7'),
                    safety_stock_limit=request.POST.get('safety_stock7'),
                    owned_by=details)
                    obj1.save()
                    if '7-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '7-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('7-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('7-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                if request.POST.get('size8'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size8')),
                    unit=request.POST.get('unit8'),
                    color=request.POST.get('color8'),
                    quantity=int(request.POST.get('quantity8')),
                    price=int(request.POST.get('price8')),
                    c_price=request.POST.get('c_price8'),
                    safety_stock_limit=request.POST.get('safety_stock8'),
                    owned_by=details)
                    obj1.save()
                    if '8-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '8-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('8-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('8-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                if request.POST.get('size9'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size9')),
                    unit=request.POST.get('unit9'),
                    color=request.POST.get('color9'),
                    quantity=int(request.POST.get('quantity9')),
                    price=int(request.POST.get('price9')),
                    c_price=request.POST.get('c_price9'),
                    safety_stock_limit=request.POST.get('safety_stock9'),
                    owned_by=details)
                    obj1.save()
                    if '9-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '9-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('9-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('9-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()
                if request.POST.get('size10'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size10')),
                    unit=request.POST.get('unit10'),
                    color=request.POST.get('color10'),
                    quantity=int(request.POST.get('quantity10')),
                    price=int(request.POST.get('price10')),
                    c_price=request.POST.get('c_price10'),
                    safety_stock_limit=request.POST.get('safety_stock10'),
                    owned_by=details)
                    obj1.save()
                    if '10-sizeimage-1' in request.FILES.keys():
                        for l in range(1,10):
                            m = str(l)
                            if '10-sizeimage-'+m in request.FILES.keys():
                                if request.POST.get('10-isactual-'+m) == 'true':
                                    actual = True
                                else:
                                    actual = False
                                size_image = Add_images(prod=obj, image=request.FILES.get('10-sizeimage-'+m), size=obj1, is_actual=actual)
                                size_image.save()

                if details.staff:
                    return redirect('/userdetail/staff_profile')
                elif details.vendor and details.seller_category.name=="Products Vendor":
                    return redirect('/userdetail/seller_profile')
                elif details.vendor:
                    return redirect('/userdetail/vendor_profile')
                elif details.buisness_Customer:
                    return redirect('/buisness/buisness_profile')

            return render(request,'products/upload_product.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')

# def upload_product(request):
#     if request.method == 'POST':
#         form = UploadProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_product = product()
#             new_product = form.save(commit=False)
#             new_product.slug = slugify(new_product.title + 'tyjppp')
#             new_product.save()
#             messages.success(request, f'Your product was uploaded!!')
#             return redirect('/')
#     else:
#         form = UploadProductForm()
#         return render(request, 'products/upload_product2.html', {'form': form})


from .models import trims_Attribute,trims_Category,trims_product


def vendor_product_upload(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.vendor:
            fabric=seller_Categories.objects.filter(name="Fabric Vendor").first()
            packing=seller_Categories.objects.filter(name="Packing Trims Vendor").first()
            sewing=seller_Categories.objects.filter(name="Sewing Trims Vendor").first()
            finishing=seller_Categories.objects.filter(name="Finishing Trims Vendor").first()
            fab=False
            pack=False
            sew=False
            fini=False
            fabric_dir = []
            fabric_wid=[]
            fabric_design=[]
            fabric_type=[]
            attri=[]
            trims_label_attributes=[]
            if details.seller_category==fabric:
                fab=True
                attri=trims_Category.objects.filter(fabric=True).first().attributes.all()
                trims_label_attributes=trims_Category.objects.filter(fabric=True).first().trims_label_attributes.all()
                fabric_dir = fabric_direction.objects.all()
                fabric_wid = fabric_width.objects.all()
                fabric_design = fabric_print_design.objects.all()
                fabric_type = fabric_print_type.objects.all()
                # print(attri)
            elif details.seller_category==packing:
                pack=True
                attri=trims_Category.objects.filter(packing=True).first().attributes.all()
                trims_label_attributes=trims_Category.objects.filter(packing=True).first().trims_label_attributes.all()
            elif details.seller_category==sewing:
                sew=True
                attri=trims_Category.objects.filter(sewing=True).first().attributes.all()
                trims_label_attributes=trims_Category.objects.filter(sewing=True).first().trims_label_attributes.all()
            elif details.seller_category==finishing:
                fini=True
                attri=trims_Category.objects.filter(finishing=True).first().attributes.all()
                trims_label_attributes=trims_Category.objects.filter(finishing=True).first().trims_label_attributes.all()
            data={
                "fab":fab,
                "pack":pack,
                "sew":sew,
                "fini":fini,
                "attri":attri,
                "trims_attri":trims_label_attributes,
                "fabric_direction": fabric_dir,
                "fabric_width": fabric_wid,
                "fabric_print_design": fabric_design,
                "fabric_print_type": fabric_type

            }
            if request.POST.get('title'):
                obj=trims_product(
                        title=request.POST.get('title'),
                        notes=request.POST.get('notes'),
                        seller=details,
                        comments=request.POST.get('description'),
                        image1=request.FILES.get('image1'),
                        image2=request.FILES.get('image2'),
                        image3=request.FILES.get('image3'),
                        image4=request.FILES.get('image4'),
                        image5=request.FILES.get('image5'),
                        price=int(request.POST.get('price')),
                        offer=int(request.POST.get('offer')), 
                        B2Boffer=int(request.POST.get('B2Boffer')), 
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
                        fabric_direction=fabric_direction.objects.filter(name=request.POST.get('fabric_direction')).first(),
                        fabric_width=fabric_width.objects.filter(name=request.POST.get('fabric_width')).first(),
                        fabric_print_design=fabric_print_design.objects.filter(name=request.POST.get('fabric_print_design')).first(),
                        fabric_print_type=fabric_print_type.objects.filter(name=request.POST.get('fabric_print_type')).first(),
                        trims_labels=request.POST.getlist('trims_labels')
                    )
                if fab:
                    qwe=trims_Category.objects.filter(fabric=True).first()
                    obj.category=qwe
                elif pack:
                    qwe=trims_Category.objects.filter(packing=True).first()
                elif sew:
                    qwe=trims_Category.objects.filter(sewing=True).first()
                elif fini:
                    qwe=trims_Category.objects.filter(finishing=True).first()
                obj.category=qwe
                obj.save()
                return redirect('/userdetail/vendor_profile')
            return render(request,"products/vendor_product_upload.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')


# for i in range(2,101):
# 	print("""			elif count=="""+str(i)+""":
# 				atr=prod.atrribute"""+str(i))



def product_edit(request,slug):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        prod=product.objects.filter(slug=slug).first()
        if details and prod and prod.seller and details.email==prod.seller.email:
            cate=category.objects.all()
            prod_cate=product_cate_b2b.objects.all()
            label=labels_Object.objects.all()
            cont=[]
            for i in label:
                objs=labels_Attributes.objects.filter(label=i)
                cont.append([i,objs])
            sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
            brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
            if details.vendor and details.seller_category.name=="Products Vendor":
                brands=[details]
            attri=[]
            count=1
            for i in prod.product_Supercategory.attributes.all():
                atr=None
                if count==1:
                    atr=prod.atrribute1
                elif count==2:
                    atr=prod.atrribute2
                elif count==3:
                    atr=prod.atrribute3
                elif count==4:
                    atr=prod.atrribute4
                elif count==5:
                    atr=prod.atrribute5
                elif count==6:
                    atr=prod.atrribute6
                elif count==7:
                    atr=prod.atrribute7
                elif count==8:
                    atr=prod.atrribute8
                elif count==9:
                    atr=prod.atrribute9
                elif count==10:
                    atr=prod.atrribute10
                elif count==11:
                    atr=prod.atrribute11
                elif count==12:
                    atr=prod.atrribute12
                elif count==13:
                    atr=prod.atrribute13
                elif count==14:
                    atr=prod.atrribute14
                elif count==15:
                    atr=prod.atrribute15
                elif count==16:
                    atr=prod.atrribute16
                elif count==17:
                    atr=prod.atrribute17
                elif count==18:
                    atr=prod.atrribute18
                elif count==19:
                    atr=prod.atrribute19
                elif count==20:
                    atr=prod.atrribute20
                elif count==21:
                    atr=prod.atrribute21
                elif count==22:
                    atr=prod.atrribute22
                elif count==23:
                    atr=prod.atrribute23
                elif count==24:
                    atr=prod.atrribute24
                elif count==25:
                    atr=prod.atrribute25
                elif count==26:
                    atr=prod.atrribute26
                elif count==27:
                    atr=prod.atrribute27
                elif count==28:
                    atr=prod.atrribute28
                elif count==29:
                    atr=prod.atrribute29
                elif count==30:
                    atr=prod.atrribute30
                elif count==31:
                    atr=prod.atrribute31
                elif count==32:
                    atr=prod.atrribute32
                elif count==33:
                    atr=prod.atrribute33
                elif count==34:
                    atr=prod.atrribute34
                elif count==35:
                    atr=prod.atrribute35
                elif count==36:
                    atr=prod.atrribute36
                elif count==37:
                    atr=prod.atrribute37
                elif count==38:
                    atr=prod.atrribute38
                elif count==39:
                    atr=prod.atrribute39
                elif count==40:
                    atr=prod.atrribute40
                elif count==41:
                    atr=prod.atrribute41
                elif count==42:
                    atr=prod.atrribute42
                elif count==43:
                    atr=prod.atrribute43
                elif count==44:
                    atr=prod.atrribute44
                elif count==45:
                    atr=prod.atrribute45
                elif count==46:
                    atr=prod.atrribute46
                elif count==47:
                    atr=prod.atrribute47
                elif count==48:
                    atr=prod.atrribute48
                elif count==49:
                    atr=prod.atrribute49
                elif count==50:
                    atr=prod.atrribute50
                elif count==51:
                    atr=prod.atrribute51
                elif count==52:
                    atr=prod.atrribute52
                elif count==53:
                    atr=prod.atrribute53
                elif count==54:
                    atr=prod.atrribute54
                elif count==55:
                    atr=prod.atrribute55
                elif count==56:
                    atr=prod.atrribute56
                elif count==57:
                    atr=prod.atrribute57
                elif count==58:
                    atr=prod.atrribute58
                elif count==59:
                    atr=prod.atrribute59
                elif count==60:
                    atr=prod.atrribute60
                elif count==61:
                    atr=prod.atrribute61
                elif count==62:
                    atr=prod.atrribute62
                elif count==63:
                    atr=prod.atrribute63
                elif count==64:
                    atr=prod.atrribute64
                elif count==65:
                    atr=prod.atrribute65
                elif count==66:
                    atr=prod.atrribute66
                elif count==67:
                    atr=prod.atrribute67
                elif count==68:
                    atr=prod.atrribute68
                elif count==69:
                    atr=prod.atrribute69
                elif count==70:
                    atr=prod.atrribute70
                elif count==71:
                    atr=prod.atrribute71
                elif count==72:
                    atr=prod.atrribute72
                elif count==73:
                    atr=prod.atrribute73
                elif count==74:
                    atr=prod.atrribute74
                elif count==75:
                    atr=prod.atrribute75
                elif count==76:
                    atr=prod.atrribute76
                elif count==77:
                    atr=prod.atrribute77
                elif count==78:
                    atr=prod.atrribute78
                elif count==79:
                    atr=prod.atrribute79
                elif count==80:
                    atr=prod.atrribute80
                elif count==81:
                    atr=prod.atrribute81
                elif count==82:
                    atr=prod.atrribute82
                elif count==83:
                    atr=prod.atrribute83
                elif count==84:
                    atr=prod.atrribute84
                elif count==85:
                    atr=prod.atrribute85
                elif count==86:
                    atr=prod.atrribute86
                elif count==87:
                    atr=prod.atrribute87
                elif count==88:
                    atr=prod.atrribute88
                elif count==89:
                    atr=prod.atrribute89
                elif count==90:
                    atr=prod.atrribute90
                elif count==91:
                    atr=prod.atrribute91
                elif count==92:
                    atr=prod.atrribute92
                elif count==93:
                    atr=prod.atrribute93
                elif count==94:
                    atr=prod.atrribute94
                elif count==95:
                    atr=prod.atrribute95
                elif count==96:
                    atr=prod.atrribute96
                elif count==97:
                    atr=prod.atrribute97
                elif count==98:
                    atr=prod.atrribute98
                elif count==99:
                    atr=prod.atrribute99
                elif count==100:
                    atr=prod.atrribute100
                attri.append([i,atr])
                count+=1


            meas=measurement.objects.filter(user=prod.brand,season=prod.season,product_Supercategory=prod.product_Supercategory).first()
            sizes=[]
            '''
            for i in meas.measurement_chart_set.all():
                if not(i.size in sizes):
                    sizes.append(i.size)
            '''
            image_count=1
            if prod.image5:
                image_count=5
            elif prod.image4:
                image_count=4
            elif prod.image3:
                image_count=3
            elif prod.image2:
                image_count=2

            data={
            "cate":cate,
            "prod_cate":prod_cate,
            "label":label,
            "cont":cont,
            "brands":brands,
            "details":details,
            "prod":prod,
            "attri":attri,
            "meas":sizes,
            "image_count":image_count,
            "default_safety":safety_stock.objects.filter(vendor=prod.seller,product_Supercategory=prod.product_Supercategory).first().limit,
            }
            if request.POST.get('brand_ajax_cate'):
                vendor_obj=detail.objects.filter(email=request.POST.get('brand_ajax_cate')).first()
                label_obj=labels.objects.filter(vendor=vendor_obj)
                bol=False
                if label_obj.count()>0:
                    bol=True
                # print("wor",label_obj)
                label_obj=list(label_obj.values())
                return HttpResponse(json.dumps({'data': label_obj,'bol':bol}), content_type="application/json")
            if request.POST.get('label_fits_ajax'):
                label_obj=labels.objects.filter(id=int(request.POST.get('label_fits_ajax'))).first()
                fits_obj=fits.objects.filter(label=label_obj)
                bol=False
                if fits_obj.count()>0:
                    bol=True
                fits_obj=list(fits_obj.values())
                return HttpResponse(json.dumps({"data":fits_obj,"bol":bol}), content_type="application/json")
            if request.POST.get('fits_season_ajax'):
                label_obj=fits.objects.filter(id=int(request.POST.get('fits_season_ajax'))).first()
                # print(label_obj)
                fits_obj=seasons.objects.filter(fit=label_obj)
                bol=False
                if fits_obj.count()>0:
                    bol=True
                fits_obj=list(fits_obj.values())
                return HttpResponse(json.dumps({"data":fits_obj,"bol":bol}), content_type="application/json")
            if request.POST.get('season_washcare_ajax'):
                label_obj=seasons.objects.filter(id=int(request.POST.get('season_washcare_ajax'))).first()
                # print(label_obj)
                superc=super_category.objects.filter(id=int(request.POST.get('season_supercategory_ajax'))).first()
                meas=measurement.objects.filter(product_Supercategory=superc,season=label_obj,user=label_obj.vendor).first()
                if meas:
                    meas=meas.measurement_chart_set.all()
                else:
                    meas=[]
                sizes=[]
                for i in meas:
                    if not(i.size in sizes):
                        sizes.append(i.size)
                fits_obj=washcares.objects.filter(season=label_obj)
                barcode_obj=barcodes.objects.filter(season=label_obj)
                bol=False
                if fits_obj.count()>0:
                    bol=True
                fits_obj=list(fits_obj.values())
                barcode_obj=list(barcode_obj.values())
                # print(barcode_obj)
                return HttpResponse(json.dumps({"data":fits_obj,"barcode":barcode_obj,"bol":bol,"sizes":sizes}), content_type="application/json")
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
                # newid=request.POST.get('id_ajax_subcate_cate')
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
                # if request.POST.get('b2b_cate'):
                # 	b2b_cate=product_cate_b2b.objects.filter(id=int(request.POST.get('b2b_cate'))).first()
                brand_obj=detail.objects.filter(email=request.POST.get('brand')).first()
                label_obj=labels.objects.filter(id=int(request.POST.get('label'))).first()
                fit_obj=fits.objects.filter(id=int(request.POST.get('fit'))).first()
                season_obj=seasons.objects.filter(id=int(request.POST.get('season'))).first()
                washcare_obj=washcares.objects.filter(id=int(request.POST.get('washcare'))).first()
                barcode_obj=barcodes.objects.filter(id=int(request.POST.get('barcode'))).first()
                # print(request.POST.get('desc_up'))
                prod.title=request.POST.get('title')
                prod.slug=request.POST.get('slug')
                prod.notes=request.POST.get('notes')
                prod.seller=details
                prod.brand=brand_obj
                prod.label=label_obj
                prod.fit=fit_obj
                prod.season=season_obj
                prod.washcare=washcare_obj
                prod.barcode=barcode_obj
                prod.terms=request.POST.get('terms')
                prod.description=request.POST.get('desc_up')
                prod.image1=request.FILES.get('image1') if request.FILES.get('image1') else prod.image1
                prod.image2=request.FILES.get('image2') if request.FILES.get('image2') else prod.image2
                prod.image3=request.FILES.get('image3') if request.FILES.get('image3') else prod.image3
                prod.image4=request.FILES.get('image4') if request.FILES.get('image4') else prod.image4
                prod.image5=request.FILES.get('image5') if request.FILES.get('image5') else prod.image5
                prod.privacy=request.POST.get('fixed_privacy')
                '''prod.atrribute1=request.POST.get('attribute1')
                prod.atrribute2=request.POST.get('attribute2')
                prod.atrribute3=request.POST.get('attribute3')
                prod.atrribute4=request.POST.get('attribute4')
                prod.atrribute5=request.POST.get('attribute5')
                prod.atrribute6=request.POST.get('attribute6')
                prod.atrribute7=request.POST.get('attribute7')
                prod.atrribute8=request.POST.get('attribute8')
                prod.atrribute9=request.POST.get('attribute9')
                prod.atrribute10=request.POST.get('attribute10')
                prod.atrribute11=request.POST.get('attribute11')
                prod.atrribute12=request.POST.get('attribute12')
                prod.atrribute13=request.POST.get('attribute13')
                prod.atrribute14=request.POST.get('attribute14')
                prod.atrribute15=request.POST.get('attribute15')
                prod.atrribute16=request.POST.get('attribute16')
                prod.atrribute17=request.POST.get('attribute17')
                prod.atrribute18=request.POST.get('attribute18')
                prod.atrribute19=request.POST.get('attribute19')
                prod.atrribute20=request.POST.get('attribute20')
                prod.atrribute21=request.POST.get('attribute21')
                prod.atrribute22=request.POST.get('attribute22')
                prod.atrribute23=request.POST.get('attribute23')
                prod.atrribute24=request.POST.get('attribute24')
                prod.atrribute25=request.POST.get('attribute25')
                prod.atrribute26=request.POST.get('attribute26')
                prod.atrribute27=request.POST.get('attribute27')
                prod.atrribute28=request.POST.get('attribute28')'''
                prod.atrribute29=request.POST.get('attribute29')
                prod.atrribute30=request.POST.get('attribute30')
                prod.atrribute31=request.POST.get('attribute31')
                prod.atrribute32=request.POST.get('attribute32')
                prod.atrribute33=request.POST.get('attribute33')
                prod.atrribute34=request.POST.get('attribute34')
                prod.atrribute35=request.POST.get('attribute35')
                prod.atrribute36=request.POST.get('attribute36')
                prod.atrribute37=request.POST.get('attribute37')
                prod.atrribute38=request.POST.get('attribute38')
                prod.atrribute39=request.POST.get('attribute39')
                prod.atrribute40=request.POST.get('attribute40')
                prod.atrribute41=request.POST.get('attribute41')
                prod.atrribute42=request.POST.get('attribute42')
                prod.atrribute43=request.POST.get('attribute43')
                prod.atrribute44=request.POST.get('attribute44')
                prod.atrribute45=request.POST.get('attribute45')
                prod.atrribute46=request.POST.get('attribute46')
                prod.atrribute47=request.POST.get('attribute47')
                prod.atrribute48=request.POST.get('attribute48')
                prod.atrribute49=request.POST.get('attribute49')
                prod.atrribute50=request.POST.get('attribute50')
                prod.atrribute51=request.POST.get('attribute51')
                prod.atrribute52=request.POST.get('attribute52')
                prod.atrribute53=request.POST.get('attribute53')
                prod.atrribute54=request.POST.get('attribute54')
                prod.atrribute55=request.POST.get('attribute55')
                prod.atrribute56=request.POST.get('attribute56')
                prod.atrribute57=request.POST.get('attribute57')
                prod.atrribute58=request.POST.get('attribute58')
                prod.atrribute59=request.POST.get('attribute59')
                prod.atrribute60=request.POST.get('attribute60')
                prod.atrribute61=request.POST.get('attribute61')
                prod.atrribute62=request.POST.get('attribute62')
                prod.atrribute63=request.POST.get('attribute63')
                prod.atrribute64=request.POST.get('attribute64')
                prod.atrribute65=request.POST.get('attribute65')
                prod.atrribute66=request.POST.get('attribute66')
                prod.atrribute67=request.POST.get('attribute67')
                prod.atrribute68=request.POST.get('attribute68')
                prod.atrribute69=request.POST.get('attribute69')
                prod.atrribute70=request.POST.get('attribute70')
                prod.atrribute71=request.POST.get('attribute71')
                prod.atrribute72=request.POST.get('attribute72')
                prod.atrribute73=request.POST.get('attribute73')
                prod.atrribute74=request.POST.get('attribute74')
                prod.atrribute75=request.POST.get('attribute75')
                prod.atrribute76=request.POST.get('attribute76')
                prod.atrribute77=request.POST.get('attribute77')
                prod.atrribute78=request.POST.get('attribute78')
                prod.atrribute79=request.POST.get('attribute79')
                prod.atrribute80=request.POST.get('attribute80')
                prod.atrribute81=request.POST.get('attribute81')
                prod.atrribute82=request.POST.get('attribute82')
                prod.atrribute83=request.POST.get('attribute83')
                prod.atrribute84=request.POST.get('attribute84')
                prod.atrribute85=request.POST.get('attribute85')
                prod.atrribute86=request.POST.get('attribute86')
                prod.atrribute87=request.POST.get('attribute87')
                prod.atrribute88=request.POST.get('attribute88')
                prod.atrribute89=request.POST.get('attribute89')
                prod.atrribute90=request.POST.get('attribute90')
                prod.atrribute91=request.POST.get('attribute91')
                prod.atrribute92=request.POST.get('attribute92')
                prod.atrribute93=request.POST.get('attribute93')
                prod.atrribute94=request.POST.get('attribute94')
                prod.atrribute95=request.POST.get('attribute95')
                prod.atrribute96=request.POST.get('attribute96')
                prod.atrribute97=request.POST.get('attribute97')
                prod.atrribute98=request.POST.get('attribute98')
                prod.atrribute99=request.POST.get('attribute99')
                prod.atrribute100=request.POST.get('attribute100')
                prod.price=int(request.POST.get('price1'))
                obj=prod
                prod.deal_of_day = int(request.POST.get('deal_of_day'))
                obj.save()
                # if b2b_cate:
                # 	obj.product_cate.add(b2b_cate)
                # if request.POST.get('b2b_product'):
                # 	obj.b2b_product=True
                # if request.POST.get('b2c_product'):
                # 	obj.b2c_product=True
                # if request.POST.get('sample_product'):
                # 	obj.sample_product=True
                # obj.save()
                # for i in label:
                # 	if request.POST.get(str(i.id)):
                # 		obj.product_tags.add(i)
                # for i in cont:
                # 	for j in i[1]:
                # 		if request.POST.get('label_content_'+str(j.id)):
                # 			obj45=label_Attributes_Values(prod=obj,label_attribute=j,value=request.POST.get('label_content_'+str(j.id)))
                # 			obj45.save()
                c=1
                for i in prod.size_color_quantity_set.all():
                    i.size=request.POST.get('size'+str(c)) if request.POST.get('size'+str(c)) else i.size
                    i.color=request.POST.get('color'+str(c)) if request.POST.get('color'+str(c)) else i.color
                    i.quantity=request.POST.get('quantity'+str(c)) if request.POST.get('quantity'+str(c)) else i.quantity
                    i.price=request.POST.get('price'+str(c)) if request.POST.get('price'+str(c)) else i.price
                    i.c_price=request.POST.get('c_price'+str(c)) if request.POST.get('c_price'+str(c)) else i.c_price
                    i.safety_stock_limit=request.POST.get('safety_stock'+str(c)) if request.POST.get('safety_stock'+str(c)) else i.safety_stock_limit
                    i.save()
                    c+=1
                cnt=prod.size_color_quantity_set.all().count()
                if cnt<2 and request.POST.get('size2'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size2')),
                    color=request.POST.get('color2'),
                    quantity=int(request.POST.get('quantity2')),
                    price=int(request.POST.get('price2')),
                    c_price=request.POST.get('c_price2'),
                    safety_stock_limit=request.POST.get('safety_stock2'),
                    owned_by=details)
                    obj1.save()
                if cnt<3 and  request.POST.get('size3'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size3')),
                    color=request.POST.get('color3'),
                    quantity=int(request.POST.get('quantity3')),
                    price=int(request.POST.get('price3')),
                    c_price=request.POST.get('c_price3'),
                    safety_stock_limit=request.POST.get('safety_stock3'),
                    owned_by=details)
                    obj1.save()
                if cnt<4 and  request.POST.get('size4'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size4')),
                    color=request.POST.get('color4'),
                    quantity=int(request.POST.get('quantity4')),
                    price=int(request.POST.get('price4')),
                    c_price=request.POST.get('c_price4'),
                    safety_stock_limit=request.POST.get('safety_stock4'),
                    owned_by=details)
                    obj1.save()
                if cnt<5 and  request.POST.get('size5'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size5')),
                    color=request.POST.get('color5'),
                    quantity=int(request.POST.get('quantity5')),
                    price=int(request.POST.get('price5')),
                    c_price=request.POST.get('c_price5'),
                    safety_stock_limit=request.POST.get('safety_stock5'),
                    owned_by=details)
                    obj1.save()
                if cnt<6 and  request.POST.get('size6'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size6')),
                    color=request.POST.get('color6'),
                    quantity=int(request.POST.get('quantity6')),
                    price=int(request.POST.get('price6')),
                    c_price=request.POST.get('c_price6'),
                    safety_stock_limit=request.POST.get('safety_stock6'),
                    owned_by=details)
                    obj1.save()
                if cnt<7 and  request.POST.get('size7'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size7')),
                    color=request.POST.get('color7'),
                    quantity=int(request.POST.get('quantity7')),
                    price=int(request.POST.get('price7')),
                    c_price=request.POST.get('c_price7'),
                    safety_stock_limit=request.POST.get('safety_stock7'),
                    owned_by=details)
                    obj1.save()
                if cnt<8 and  request.POST.get('size8'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size8')),
                    color=request.POST.get('color8'),
                    quantity=int(request.POST.get('quantity8')),
                    price=int(request.POST.get('price8')),
                    c_price=request.POST.get('c_price8'),
                    safety_stock_limit=request.POST.get('safety_stock8'),
                    owned_by=details)
                    obj1.save()
                if cnt<9 and  request.POST.get('size9'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size9')),
                    color=request.POST.get('color9'),
                    quantity=int(request.POST.get('quantity9')),
                    price=int(request.POST.get('price9')),
                    c_price=request.POST.get('c_price9'),
                    safety_stock_limit=request.POST.get('safety_stock9'),
                    owned_by=details)
                    obj1.save()
                if cnt<10 and  request.POST.get('size10'):
                    obj1=size_color_quantity(linked_product=obj,
                    size=int(request.POST.get('size10')),
                    color=request.POST.get('color10'),
                    quantity=int(request.POST.get('quantity10')),
                    price=int(request.POST.get('price10')),
                    c_price=request.POST.get('c_price10'),
                    safety_stock_limit=request.POST.get('safety_stock10'),
                    owned_by=details)
                    obj1.save()
                if details.staff: 
                    return redirect('/userdetail/staff_profile')
                elif details.vendor and details.seller_category.name=="Products Vendor":
                    return redirect('/userdetail/seller_profile')
                elif details.vendor:
                    return redirect('/userdetail/vendor_profile')
                elif details.buisness_Customer:
                    return redirect('/buisness/buisness_profile')

            return render(request,'products/product_edit.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')

def product_unit(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        seller_id=detail.objects.filter(email=request.user.email).values('id')[0]['id']
        pro_unit=request.POST['unit']
        supcate=request.POST['product']
        super_id=super_category.objects.filter(name=supcate).values('id')[0]['id']
        if units.objects.filter(seller_id=seller_id,supercategory_id=super_id,unit=pro_unit).exists():
            return HttpResponse("This unit is already exists for this product")
        else:
            a=units(seller_id=seller_id,supercategory_id=super_id,unit=pro_unit)
            a.save()
        if details.staff:
            return redirect('/userdetail/staff_profile')
        elif details.vendor and details.seller_category.name=="Products Vendor":
            return redirect('/userdetail/seller_profile')
        elif details.vendor:
            return redirect('/userdetail/vendor_profile')
        elif details.buisness_Customer:
            return redirect('/buisness/buisness_profile')

from .models import *
def service_unit(email,pro_unit,supcate):
    print("supcate",supcate)
    details=detail.objects.filter(email=email).first()
    seller_id=detail.objects.filter(email=email).values('id')[0]['id']
    super_id=super_category.objects.get(name=supcate.id)
    print("highhhh",super_id.id)
    a=service_add(seller_id=seller_id,supercategory_id=super_id,price_range=pro_unit)
    a.save()
        
def add_subscription(product,subscription,email):
    details=detail.objects.filter(email= email).first()
    #product=request.POST['product']
    #subscription=request.POST['subscription']
    seller=detail.objects.filter(email=email).values('id')[0]['id']
    super_cat=super_category.objects.filter(name=product)
    
    if subscription=='yes':
        for t in super_cat:
            t.available_for_subscription=True
            t.save()
    else:
        for t in super_cat:
            t.available_for_subscription=False
            t.save()



    