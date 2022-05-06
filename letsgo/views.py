from django.shortcuts import render,redirect
from django.http import HttpResponse
import facebook
import requests
from . import combined,ll_accesstoken,twitter
from .models import User_details

ro_key=''
ro_secret=''
page_id=''
def initial(request):
   return render(request,"initial.html")

def login(request):
   return render(request,"login.html")

def signup(request):
   return render(request,"signup.html")

def index(request):
     thank=False
     if request.method=="POST" :
        
        page_name=request.POST.get('name','')
        msg=request.POST.get('msg','')
       
        
        prod=User_details.objects.filter(user_name=page_name)
        q=prod.values('user_name','page_id','access_token','tweet_access_token','access_token_secret')
        page_id= q[0]['page_id']
        atoken=q[0]['access_token']
        key=q[0]['tweet_access_token']
        secret=q[0]['access_token_secret']
        print(page_id,atoken)
        combined.post_status(page_id,msg,atoken)
        combined.twitter_status(key,secret,msg)
     return render(request,"index.html",{'thank':thank})
    
def status(request):
   if request.method=="POST" :
        user_token=request.POST.get('fblogin','')
        print(user_token)
        ll_accesstoken.get_atoken(user_token)
   return render(request,"status.html")

def statustw(request):
   
   if request.method=="GET" :
        
        ro=twitter.get_resource_token()
        global ro_key,ro_secret
        ro_key=ro[0]
        ro_secret=ro[1]
        
   
   return render(request,"twstatus.html")

def accesstoken(request):
   if request.method=="POST":
         verifier=request.POST.get('pin','')
         print(ro_key,ro_secret,verifier)
         access_token_list=twitter.twitter_get_access_token(verifier,ro_key,ro_secret)
         key=access_token_list[0]
         secret=access_token_list[1]
         ll_accesstoken.update_twitter(key,secret)
         # combined.set_var(key,secret)
         url='home/'
         return redirect(index)

      
def postimg(request):
   if request.method=="POST" :
       fb_id=request.POST.get('name','')
      #  insta_id=request.POST.get('instaid','')
       img_url=request.POST.get('img','')
       msg=request.POST.get('msg','')
       prod=User_details.objects.filter(page_id=fb_id)
       q=prod.values('user_name','page_id','access_token','insta_id','iaccess_token','tweet_access_token','access_token_secret')
       page_id= q[0]['page_id']
       atoken=q[0]['access_token']
       insta_id=q[0]['insta_id']
       iaccess=q[0]['iaccess_token']
       key=q[0]['tweet_access_token']
       secret=q[0]['access_token_secret']

       combined.post_img(page_id,img_url,msg,atoken)
       combined.insta_post(insta_id,iaccess,img_url,msg)
       combined.twitter_img(key,secret,img_url,msg)
   return render(request,"imagepost.html")