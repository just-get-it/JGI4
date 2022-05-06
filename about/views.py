from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from .models import FileUpload
from homepage.models import *
from enquiry.models import *
from enquiry.forms import *

# Create your views here.
def about(request):
    # file = FileUploads.objects.all()
    # context = {
    #     'files': file
    # }
    # fashion=""
    # design=""
    # retail=""
    # software=""
    Quick=""
    Connect=""
    Consult=""
    Digitize=""
    Automation=""   
    Create=""
    Source=""
    Manufacturing=""
    Catalogue=""
    Market=""
    Brands=""
    Supplychain=""
    Credit=""
    banner_images =""
    card_images =""
    bodyimage1=""
    HomePageBanners=HomePage_Banners.objects.count()
    ad  = Add_Page.objects.get
    # Homepage_Card=Homepage_cardimg.objects.count()
    if HomePageBanners:
        # f = HomePage_Banners.objects.get(title="fashion")
        # f1 = f.id
        # d = HomePage_Banners.objects.get(title="design")
        # d1 = d.id
        # r = HomePage_Banners.objects.get(title="retail")
        # r1 = r.id
        # s = HomePage_Banners.objects.get(title="software")
        # s1 = s.id
        b = HomePage_Banners.objects.get(title="banner_images")
        b1 = b.id
        banner_images = Homepage_Banners_Image.objects.filter(banner=b1)
    # try:
    # if Homepage_Card:
        
        ca = Homepage_Card.objects.get(title="Quick")
        ca1 = ca.id
        co = Homepage_Card.objects.get(title="Connect")
        co1 = co.id
        cn = Homepage_Card.objects.get(title="Consult")
        cn1 = cn.id
        d = Homepage_Card.objects.get(title="Digitize")
        d1 = d.id
        a = Homepage_Card.objects.get(title="Automation")
        a1 = a.id
        cr = Homepage_Card.objects.get(title="Create")
        cr1 = cr.id
        so = Homepage_Card.objects.get(title="Source")
        so1 = so.id
        m = Homepage_Card.objects.get(title="Manufacturing")
        m1 = m.id
        ct = Homepage_Card.objects.get(title="Catalogue")
        ct1 = ct.id
        mr = Homepage_Card.objects.get(title="Market")
        mr1 = mr.id
        br = Homepage_Card.objects.get(title="Brands")
        br1 = br.id
        br = Homepage_Card.objects.get(title="Supplychain")
        sc1 = br.id
        br = Homepage_Card.objects.get(title="Credit")
        cre1 = br.id
        # bi= Body_image.objects.get(Add_body_title="bodyimage1")
        # bi1=bi.id
        Quick = Homepage_cardimg.objects.filter(card=ca1)
        Connect = Homepage_cardimg.objects.filter(card=co1)
        Consult = Homepage_cardimg.objects.filter(card=cn1)
        Digitize = Homepage_cardimg.objects.filter(card=d1)
        Automation = Homepage_cardimg.objects.filter(card=a1)
        Create = Homepage_cardimg.objects.filter(card=cr1)
        Source = Homepage_cardimg.objects.filter(card=so1)
        Manufacturing = Homepage_cardimg.objects.filter(card=m1)
        Catalogue = Homepage_cardimg.objects.filter(card=ct1)
        Market = Homepage_cardimg.objects.filter(card=mr1)
        Brands = Homepage_cardimg.objects.filter(card=br1)
        Supplychain = Homepage_cardimg.objects.filter(card=sc1)
        Credit = Homepage_cardimg.objects.filter(card=cre1)
        # bodyimage1=Body_image.objects.filter(Add_body_title=bi1)

    # else:Homepage_Card.queryset().all
    #     Homepage_Card.objects.first()
    # except Homepage_Card.DoesNotExist:
    #     Homepage_Card.objects.get.all()
    #     cards = Homepage_Card.objects.all()[0]
        
        # b = HomePage_Banners.objects.filter()
       
        # image=get_object_or_404(Homepage_Banners_Images,id=imageid)
       
        

        # fashion = Homepage_Banners_Images.objects.filter(banner=f1)
        # design = Homepage_Banners_Images.objects.filter(banner=d1)
        # retail = Homepage_Banners_Images.objects.filter(banner=r1)
        # software = Homepage_Banners_Images.objects.filter(banner=s1)

        ca2 = Body_image_category.objects.get(title="Quick1")
        ca3 = ca2.id
        co2 = Body_image_category.objects.get(title="Connect1")
        co3 = co2.id
        cn2 = Body_image_category.objects.get(title="Consult1")
        cn3 = cn2.id
        d2 = Body_image_category.objects.get(title="Digitize1")
        d3 = d2.id
        a2 = Body_image_category.objects.get(title="Automation1")
        a3 = a2.id
        cr2 = Body_image_category.objects.get(title="Create1")
        cr3 = cr2.id
        so2 = Body_image_category.objects.get(title="Source1")
        so3 = so2.id
        m2 = Body_image_category.objects.get(title="Manufacturing1")
        m3 = m2.id
        ct2 = Body_image_category.objects.get(title="Catalogue1")
        ct3 = ct2.id
        mr2 = Body_image_category.objects.get(title="Market1")
        mr3 = mr2.id
        br2 = Body_image_category.objects.get(title="Brands1")
        br3 = br2.id
        br2 = Body_image_category.objects.get(title="Supplychain1")
        sc3 = br2.id
        br2 = Body_image_category.objects.get(title="Credit1")
        cre3 = br2.id
        
        Quick1 = Body_image.objects.filter(card=ca3)
        Connect1 = Body_image.objects.filter(card=co3)
        Consult1 = Body_image.objects.filter(card=cn3)
        Digitize1 = Body_image.objects.filter(card=d3)
        Automation1 = Body_image.objects.filter(card=a3)
        Create1 = Body_image.objects.filter(card=cr3)
        Source1 = Body_image.objects.filter(card=so3)
        Manufacturing1 = Body_image.objects.filter(card=m3)
        Catalogue1 = Body_image.objects.filter(card=ct3)
        Market1 = Body_image.objects.filter(card=mr3)
        Brands1 = Body_image.objects.filter(card=br3)
        Supplychain1 = Body_image.objects.filter(card=sc3)
        Credit1 = Body_image.objects.filter(card=cre3)


    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        number = request.POST.get('number')
        country = request.POST.get('country')
        subject = request.POST.get('subject')
        disp = request.POST.get('disp')
        en_title = request.POST.get('en_title')
        enquiry = enquiry_port(fullname=fullname,email=email,number=number,country=country,subject=subject,disp=disp,en_title=en_title)
        enquiry.save()

    # enquiry = enquiry_form(request.POST)
    # if request.POST.get == "homepage_enquiry":
    #     enq = enquiry_form(request.POST)
    #     if enq.is_valid():
    #         enq.save()
    #     else:
    #         print("Homepage enquiry error: ", enq.errors) 
    # 
    #  , {'fashion': fashion, 'design': design, 'retail': retail, 'software': software,  'banner_images': banner_images }
    #  , context)
    # 'enquiry_form': enquiry

    return render(request, 'about/index.html', {'banner_images': banner_images ,'card_images': card_images ,'Quick':Quick,'Connect': Connect
    ,'Consult': Consult,'Digitize':Digitize,'Automation':Automation,'Create':Create,'Source':Source,'Manufacturing':Manufacturing,'Catalogue':Catalogue,'Market':Market,'Brands':Brands,'Supplychain':Supplychain,'Credit':Credit,'Quick1':Quick1,'Connect1': Connect1
    ,'Consult1': Consult1,'Digitize1':Digitize1,'Automation1':Automation1,'Create1':Create1,'Source1':Source1,'Manufacturing1':Manufacturing1,'Catalogue1':Catalogue1,'Market1':Market1,'Brands1':Brands1,'Supplychain1':Supplychain1,'Credit1':Credit1,'bodyimage1':bodyimage1,})

    # return render(request, 'about/index.html' )  

def retail_service(request):
    return render(request, 'about/retail-service.html')

def retail_product(request):
    return render(request, 'about/retail-product.html')

def fashion_product(request):
    
    ConsultingBanners=Consulting_Banners.objects.count()
    # Consulting_Card=Consulting_Cardimg.objects.count()
    if ConsultingBanners:
        # f = Consulting_Banners.objects.get(title="fashion")
        # f1 = f.id
        # d = Consulting_Banners.objects.get(title="design")
        # d1 = d.id
        # r = Consulting_Banners.objects.get(title="retail")
        # r1 = r.id
        # s = Consulting_Banners.objects.get(title="software")
        # s1 = s.id
        b = Consulting_Banners.objects.get(title="consulting_banner_images")
        b1 = b.id
        consulting_banner_images = Consulting_Banners_Image.objects.filter(banner=b1)
    # try:
    # if Consulting_Card:
        
        ca = Consulting_Card.objects.get(title="Product_Devlopment")
        ca1 = ca.id
        co = Consulting_Card.objects.get(title="Manufacturing")
        co1 = co.id
        
        # bi= Body_image.objects.get(Add_body_title="bodyimage1")
        # bi1=bi.id
        Product_Devlopment = Consulting_Cardimg.objects.filter(card=ca1)
        Manufacturing = Consulting_Cardimg.objects.filter(card=co1)
        
   
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        number = request.POST.get('number')
        country = request.POST.get('country')
        subject = request.POST.get('subject')
        disp = request.POST.get('disp')
        en_title = request.POST.get('en_title')
        enquiry = enquiry_port(fullname=fullname,email=email,number=number,country=country,subject=subject,disp=disp,en_title=en_title)
        enquiry.save()

    return render(request, 'about/fashion-product.html', {'consulting_banner_images': consulting_banner_images ,'Product_Devlopment':Product_Devlopment,'Manufacturing': Manufacturing,})


def b2bsourcing(request):
    return render(request, 'about/b2bsourcing.html')

def sourcing_pricing(request):
    return render(request, 'about/sourcing-pricing.html')

def new_user_sign_up(request):
    return render(request, 'about/new-user-sign-up.html')

def fashion_textile_service(request):
    return render(request, 'about/fashion-textile-service.html')

def fashion_apparel_service(request):
    return render(request, 'about/fashion-apparel-service.html')

def fashion_hardgoods_service(request):
    return render(request, 'about/fashion-hardgoods-service.html')

def fashion_design_service(request):
    return render(request, 'about/fashion-design-service.html')

def contact(request):
    return render(request, 'about/contact.html')
def experts(request):
    return render(request, 'about/experts.html')


# def about_contact(request):    
#     if request.method == "POST":
#         fullname = request.POST.get('fullname')
#         email = request.POST.get('email')
#         number = request.POST.get('number')
#         country = request.POST.get('country')
#         subject = request.POST.get('subject')
#         disp = request.POST.get('disp')
#         en_title = request.POST.get('en_title')
#         enquiry = enquiry_port(fullname=fullname,email=email,number=number,country=country,subject=subject,disp=disp,en_title=en_title)
#         enquiry.save()

#     return redirect('../../about-jgi/about-contact')

def quality_control(request):
    return render(request, 'about/quality-control.html')

def machine_maintenance(request):
    return render(request, 'about/machine-maintenance.html')

def product_planning(request):
    return render(request, 'about/product-planning')

def attendance_module(request):
    return render(request, 'about/attendance-module')

def justgetit_admin(request):
    return render(request, 'about/justgetit-admin.html')

def manufacturing(request):
    
    ManufacturingBanners=Manufacturing_Banners.objects.count()
    # Manufacturing_Card=Manufacturing_Cardimg.objects.count()
    if ManufacturingBanners:
        # f = Manufacturing_Banners.objects.get(title="fashion")
        # f1 = f.id
        # d = Manufacturing_Banners.objects.get(title="design")
        # d1 = d.id
        # r = Manufacturing_Banners.objects.get(title="retail")
        # r1 = r.id
        # s = Manufacturing_Banners.objects.get(title="software")
        # s1 = s.id
        b = Manufacturing_Banners.objects.get(title="Manufacturing_banner_images")
        b1 = b.id
        Manufacturing_banner_images = Manufacturing_Banners_Image.objects.filter(banner=b1)
    # try:
    # if Manufacturing_Card:
        
        ca = Manufacturing_Card.objects.get(title="First")
        ca1 = ca.id
        co = Manufacturing_Card.objects.get(title="Second")
        co1 = co.id
        
        # bi= Body_image.objects.get(Add_body_title="bodyimage1")
        # bi1=bi.id
        First = Manufacturing_Cardimg.objects.filter(card=ca1)
        Second = Manufacturing_Cardimg.objects.filter(card=co1)
    
    
    
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        number = request.POST.get('number')
        country = request.POST.get('country')
        subject = request.POST.get('subject')
        disp = request.POST.get('disp')
        en_title = request.POST.get('en_title')
        enquiry = enquiry_port(fullname=fullname,email=email,number=number,country=country,subject=subject,disp=disp,en_title=en_title)
        enquiry.save()
    return render(request, 'about/manufacturing.html', {'Manufacturing_banner_images': Manufacturing_banner_images ,'First': First,'Second': Second,})                     



def tags(request):
    files=FileUpload.objects.all()
    context={
        'objects':files
    }
    return render(request,'about/tags.html',context)

def tagDetail(request,slug):
    file=FileUpload.objects.get(slug=slug)
    context = {
        'object': file
    }
    return render(request, 'about/tag_detail.html', context)

