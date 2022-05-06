from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from enquiry.models import enquiry_port
# Create your views here.

def index(request):
    return render(request, "kudugudu/index.html")

def about(request):
    return render(request, 'kudugudu/about.html')

def blog_details(request):
    return render(request, 'kudugudu/blog_details.html')

def blog(request):
    return render(request, 'kudugudu/blog.html')

def contact(request):
    return render(request, 'kudugudu/contact.html')

def elements(request):
    return render(request, 'kudugudu/elements.html')

def portfolio(request):
    return render(request, 'kudugudu/portfolio.html')

def pricing(request):
    return render(request, 'kudugudu/pricing.html')

def kudugudu_contact(request):    
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

    return redirect('../../kudugudu/contact')
