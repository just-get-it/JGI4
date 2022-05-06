from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'phinix/index.html')

def project(request):
    return render(request, 'phinix/project.html')

def services(request):
    return render(request, 'phinix/services.html')

def about(request):
    return render(request, 'phinix/about.html')

def blog(request):
    return render(request, 'phinix/blog.html')

def single(request):
    return render(request, 'phinix/single.html')

def contact(request):
    return render(request, 'phinix/contact.html')
