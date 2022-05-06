#facebook page
from django.shortcuts import render,redirect,get_object_or_404
from .forms import m,m1,n,n1,pfrm,postf,commen
from .models import Items,t1,about,review,page,mesg,like,foll,cont,post
#, ViewCount, VideoComment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import UpdateView,DeleteView
#from django.urls import reverse
import csv, sqlite3
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.db.models import F
from django.utils.datastructures import MultiValueDictKeyError

def i(request):
    return render(request, 'h.html')
    
@login_required
def pages(request):
    user=request.user
    myitems=page.objects.filter(user=user)
    context={
        'It': myitems
        #"Quantity":myitems.Quantity
        #'status': myitems.status
    }
    return render(request,"just-connect/pmain.html",context)
    #return render(request, 'pmain.html')

@login_required
def page1(request,id):
    user=request.user
    It=page.objects.filter(user=user,id=id)
    Pt=post.objects.filter(user=user,paid=id)
    #print(Pt.paid)
    Ct=cont.objects.filter(paid=id)
    #print(Ct)
    #Lt=like.objects.filter()
    # It[0]=str(It[0])
    # Ct["pid"]=str(Ct["pid"])
    if request.method == 'POST':
        form = postf(request.POST, request.FILES)
        print("wm")
        if form.is_valid():
            desc=form.cleaned_data.get('desc')
            img=form.cleaned_data.get('img')
            obj= post.objects.create(user=user,desc=desc,img=img,paid=id,slug=user.username,ls=0,cs=0)
            obj.save()
            return redirect(pages)
    else:
        form = postf()

    if request.method == 'POST':
        form1 = commen(request.POST, request.FILES)
        print(form1.errors)
        if form1.is_valid():
            dete=form1.cleaned_data.get('dete')
            pa=post.objects.get(id=id)
            obj1= cont.objects.create(user=user,dete=dete, pid=id,paid=pa.paid,slug=user.username)
            obj1.save()
            post.objects.filter(id=id).update(cs=F('cs')+1)
            return redirect(pages)
    else:
        form1 = commen()
    return render(request, 'just-connect/page.html',{'form' : form,'It' : It,'Pt' : Pt, 'form1':form1,'Ct':Ct})

@login_required
def liked(request,id,paid):
    user=request.user
    
    #lk=like.objects.filter(pid=id,user=user).count()
    #if lk>0:
       # return redirect(page1,paid)
    pa=post.objects.get(id=id)
    #pa=get_object_or_404(post,id=id)
    #like.objects.create(paid=pa.paid,pid=id,slug=user.username)
    post.objects.filter(paid=paid,id=id).update(ls=F('ls')+1)
    return redirect(page1,paid)

@login_required
def editp(request,id):
    user=request.user
    
@login_required
def create(request):
    user=request.user
    list1 = pfrm() 
    if request.method =="POST":
        form = pfrm(request.POST) 
        if form.is_valid():
            name=form.cleaned_data.get('name')
            catg=form.cleaned_data.get('catg')
            desc=form.cleaned_data.get('desc')
            #date=form.cleaned_data.get('date')
            page.objects.create(user=user,name=name, catg=catg,slug=user.username,desc=desc)
            #obj = views.objects.get('index')
            return redirect(pages)
      
    #return render(request,"add.html",{'form':list1})
    return render(request, 'just-connect/create.html',{'form':list1})

# Create your views here.

def filter2(request):
    return render(request,"h.html")

@login_required
def index(request):
    user=request.user
    myitems=Items.objects.filter(user=user)
    context={
        'It': myitems
        #"Quantity":myitems.Quantity
        #'status': myitems.status
    }
    return render(request,"index.html",context)

def index1(request):
    return render(request,"index.html")

@login_required
def add(request):
    user=request.user
    list1 = m() 
    if request.method =="POST":
        form = m(request.POST) 
        if form.is_valid():
            Item=form.cleaned_data.get('Item')
            Quantity=form.cleaned_data.get('Quantity')
            status=form.cleaned_data.get('status')
            date=form.cleaned_data.get('date')
            Items.objects.create(user=user,Item=Item, Quantity=Quantity,slug=user.username, status=status,date=date)
            #obj = views.objects.get('index')
            return redirect(index)
      
    return render(request,"add.html",{'form':list1})

class update(UpdateView):
    model=Items
    form_class=m1
    template_name='update.html'
    redirect=index
    

@login_required
def delete(request,id):
    obj=Items.objects.filter(id=id).delete()
    return redirect(index)
            #print(form.errors)
    #return reverse("index")

@login_required  
def filter(request):
    query=request.GET.get('q')
    result=Items.objects.filter(date=query)
    user=request.user
    re=result.filter(user=user)
    context={
        'It':re }
    return render(request,"index.html",context)

def posti(request):
    if request.method == 'POST':
        form = postf(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = postf()
    return render(request, 'page.html', {'form' : form})




            