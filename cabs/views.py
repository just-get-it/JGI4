from django.shortcuts import render,HttpResponse, redirect
from enquiry.models import enquiry_port

# Create your views here.
def index(request):
    return render(request, 'cabs/index.html')