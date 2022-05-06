from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import Resume





def resume(request):
    qs = Resume.objects.all()
  

    content = {
        'qs' : qs,
        
}
    return  render(request, 'resume/resume.html',content)