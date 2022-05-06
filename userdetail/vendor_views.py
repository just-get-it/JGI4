

from django.core import serializers
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model


from .models import detail
from b2b.models import company_Order,company_detail,bom
from .utils import render_to_pdf,num2word
import datetime

from product.models import trims_Category

from b2b.models import packing_list,cartons_list

from b2b.models import cartons_list,packing_list,address_model
from .models import seller_Categories
from b2b.models import labels,fits,seasons
from .models import staff_Categories,seller_Categories
from product.models import category as cat
from product.models import sub_category,super_category

from django.http import HttpResponse
import json
from b2b.models import color_model



def vendor_new_order(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        obj=seller_Categories.objects.filter(name="Garmenting Vendor").first()
        sel_cate=seller_Categories.objects.filter(name="Products Vendor").first()
        brands=detail.objects.filter(activate_Seller=True,seller_category=sel_cate)
        cate=cat.objects.all()
        if details.vendor and details.seller_category==obj:
            if request.POST and request.FILES:
                brand=request.POST.get('brand')
                brand=detail.objects.get(id=brand)
                # label=request.POST.get('label')
                # label=labels.objects.get(slug=label)
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
                		label=None,
                		fit=None,
                		season=None,
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
                        personal_order=True
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
                order.staffs_Allocated.add(details)
                print(request.POST.get("from_date"))
                order.vendor_from_date=datetime.datetime.strptime(request.POST.get("from_date"),"%Y-%m-%d")
                order.vendor_to_date=datetime.datetime.strptime(request.POST.get("to_date"),"%Y-%m-%d")
                order.save()
                return redirect('/userdetail/vendor_profile')
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
            return render(request,'vendor/new_order.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')


from product.models import trims_Category,trims_product,trims_product_quantity




def update_availiable_products(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details.vendor:
            packing=seller_Categories.objects.filter(name="Packing Trims Vendor").first()
            finishing=seller_Categories.objects.filter(name="Finishing Trims Vendor").first()
            sewing=seller_Categories.objects.filter(name="Sewing Trims Vendor").first()
            fabrics=seller_Categories.objects.filter(name="Fabric Vendor").first()
            if details.seller_category==packing:
                prod_cate=trims_Category.objects.filter(name="Packing").first()
            elif details.seller_category==finishing:
                prod_cate=trims_Category.objects.filter(name="Finishing").first()
            elif details.seller_category==sewing:
                prod_cate=trims_Category.objects.filter(name="Sewing").first()
            elif details.seller_category==fabrics:
                prod_cate=trims_Category.objects.filter(name="Fabric").first()
            obj=trims_product.objects.filter(category=prod_cate)
            data={
                "obj":obj
            }
            if request.POST.get('prod_ajax_id') and request.POST.get('prod_ajax_quantity'):
                prod=trims_product.objects.filter(id=int(request.POST.get('prod_ajax_id'))).first()
                check=True
                try:
                    quan=int(request.POST.get('prod_ajax_quantity'))
                except:
                    check=False
                if not(prod):
                    check=False
                if check:
                    ofg=trims_product_quantity.objects.filter(to_product=prod,seller=details).first()
                    if ofg:
                        ofg.quantity+=int(request.POST.get('prod_ajax_quantity'))
                        ofg.save()
                    else:
                        ofg=trims_product_quantity(
                            to_product=prod,
                            seller=details,
                            quantity=int(request.POST.get('prod_ajax_quantity'))
                        )
                        ofg.save()
                return HttpResponse(json.dumps({'bol':check}), content_type="application/json")
            return render(request,'vendor/update_availiable_products.html',data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')
