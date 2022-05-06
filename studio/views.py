from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect 
from django.http import HttpResponseRedirect



def archbase(request):
    return render(request, 'studio/home.html')

def about(request):
    return render(request, 'studio/about.html')

def services(request):
    return render(request, 'studio/services.html')

def projects(request):
    return render(request, 'studio/projects.html')

def gallery(request):
    return render(request, 'studio/gallery.html')

def contact(request):
    return render(request, 'studio/contact.html')
