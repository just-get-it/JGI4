from django.shortcuts import render,redirect
from .models import Notification
from django.core.paginator import Paginator
 
def event(request):
    event_list = Notification.objects.all().order_by('-id')
    limit = Paginator(event_list,2)
    page_no = request.GET.get('page')
    page_obj = limit.get_page(page_no)
    return render(request, 'events.html', {'page_obj' : page_obj})