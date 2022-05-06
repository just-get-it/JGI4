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
    # return render(request,'enquiry/create.html')
    return render(request,'enquiry/branding.html')

def portfolio(request):
    return render(request, 'enquiry/branding_portfolio.html')

def contact(request):
    return render(request, 'enquiry/branding_contact.html')

def about(request):
    return render(request, 'enquiry/branding_about.html')

def services(request):
    return render(request, 'enquiry/branding_services.html')

def user_experience(request):
    return render(request, 'enquiry/branding_userexperience.html')

def user_interface(request):
    return render(request, 'enquiry/branding_userinterface.html')

def explainer_video(request):
    return render(request, 'enquiry/branding_explainer_video.html')

def design_and_concept(request):
    return render(request, 'enquiry/branding_design_and_concept.html')

def social_media_marketing(request):
    return render(request, 'enquiry/branding_social_media_marketing.html')

def seo(request):
    return render(request, 'enquiry/branding_seo.html')

def animation(request):
    return render(request, 'enquiry/branding_animation.html')
    
def branding(request):
    return render(request, 'enquiry/branding_branding.html')

def presentation(request):
    return render(request, 'enquiry/branding_presentation.html')

def email_marketing(request):
    return render(request, 'enquiry/branding_email_marketing.html')
    
def content_strategy(request):
    return render(request, 'enquiry/branding_content_strategy.html')

def privacy_policy(request):
    return render(request, 'enquiry/branding_privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'enquiry/branding_terms_and_conditions.html')

def industries(request):
    return render(request, 'enquiry/branding_industries.html')

def innovation(request):
    return render(request, 'enquiry/branding_innovation.html')

def blogp(request, num):
    if num == 2:
        return render(request, 'enquiry/branding_blogp2.html') 
    return render(request, 'enquiry/branding_blogp1.html')

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

    return redirect('../../enquiry/digital-marketing')
    



