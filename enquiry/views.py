from django.shortcuts import render,HttpResponse, redirect
from more_itertools import first
from enquiry.models import enquiry_port
from homepage.models import *
# Create your views here.

    
  

def enquiry(request):    
    AutomationBanners=Automation_Banners.objects.count()
    # Automation_Card=Automation_Cardimg.objects.count()
    if AutomationBanners:
        # f = Automation_Banners.objects.get(title="fashion")
        # f1 = f.id
        # d = Automation_Banners.objects.get(title="design")
        # d1 = d.id
        # r = Automation_Banners.objects.get(title="retail")
        # r1 = r.id
        # s = Automation_Banners.objects.get(title="software")
        # s1 = s.id
        b = Automation_Banners.objects.get(title="Automation_banner_images")
        b1 = b.id
        Automation_banner_images = Automation_Banners_Image.objects.filter(banner=b1)
    # try:
    # if Automation_Card:
        
        ca = Automation_Card.objects.get(title="First")
        ca1 = ca.id
        co = Automation_Card.objects.get(title="Second")
        co1 = co.id
        
        # bi= Body_image.objects.get(Add_body_title="bodyimage1")
        # bi1=bi.id
        First = Automation_Cardimg.objects.filter(card=ca1)
        Second = Automation_Cardimg.objects.filter(card=co1)
    
    
    
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
    return render(request, 'enquiry/portfolio.html', {'Automation_banner_images': Automation_banner_images ,'First': First,'Second': Second,})                     


def enquiry_sourcing(request):    

    SourcingBanners=Sourcing_Banners.objects.count()
    # Sourcing_Card=Sourcing_Cardimg.objects.count()
    if SourcingBanners:
        # f = Sourcing_Banners.objects.get(title="fashion")
        # f1 = f.id
        # d = Sourcing_Banners.objects.get(title="design")
        # d1 = d.id
        # r = Sourcing_Banners.objects.get(title="retail")
        # r1 = r.id
        # s = Sourcing_Banners.objects.get(title="software")
        # s1 = s.id
        b = Sourcing_Banners.objects.get(title="Sourcing_banner_images")
        b1 = b.id
        Sourcing_banner_images = Sourcing_Banners_Image.objects.filter(banner=b1)
    # try:
    # if Sourcing_Card:
        
        ca = Sourcing_Card.objects.get(title="First")
        ca1 = ca.id
        co = Sourcing_Card.objects.get(title="Second")
        co1 = co.id
        
        # bi= Body_image.objects.get(Add_body_title="bodyimage1")
        # bi1=bi.id
        First = Sourcing_Cardimg.objects.filter(card=ca1)
        Second = Sourcing_Cardimg.objects.filter(card=co1)


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

    return render(request,'enquiry/sourcing.html', {'Sourcing_banner_images': Sourcing_banner_images ,'First': First,'Second': Second,})


def enquiry_contact(request):    
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

    return render(request,'gown/contact.html')



def port_app(request): 
    stud = enquiry_port.objects.all()
     
    return render(request,'enquiry/show_appointmnt.html',{'stu': stud})


def show_app(request):
    en_tit = request.POST.get('en_tit')
    stud = enquiry_port.objects.filter(en_title=en_tit)

    return render(request,'enquiry/show_appointmnt.html',{'stu': stud})


def videos(request):
    return render(request, 'enquiry/videos.html')

def blog(request):
    return render(request, 'enquiry/blog.html')

def content_writing(request):
    return render(request, 'enquiry/content-writing.html')

def digital_marketing(request):
    return render(request, 'enquiry/digital-marketing.html')

def digital_marketing_enquiry(request):    
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

    return redirect('../../enquiry/digital-marketing')
    



