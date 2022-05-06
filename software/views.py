from django.shortcuts import render,HttpResponse, redirect
from enquiry.models import enquiry_port
# Create your views here.

    
  

def enquiry(request):    
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

    return render(request,'enquiry/portfolio.html')

def enquiry_sourcing(request):    
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

    return render(request,'enquiry/sourcing.html')


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

    return redirect('../../software/digital-marketing')
    



