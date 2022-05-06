from django.shortcuts import render,HttpResponse, redirect
from enquiry.models import enquiry_port

# Create your views here.
def index(request):
    return render(request, 'academy/index.html')

def about(request):
	return render(request, 'academy/about.html')

def blog(request):
	return render(request, 'academy/blog.html')

def blog_details(request):
	return render(request, 'academy/blog_details.html')

def contact(request):
	return render(request, 'academy/contact.html')

def courses(request):
	return render(request, 'academy/courses.html')

def elements(request):
	return render(request, 'academy/elements.html')

def login(request):
	return render(request, 'academy/login.html')

def register(request):
	return render(request, 'academy/register.html')

def academy_enquiry(request):    
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

    return redirect('../../academy/contact')