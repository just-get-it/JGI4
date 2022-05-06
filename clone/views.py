from django.shortcuts import render,redirect
from django.contrib import messages
from clone.models import account,new_events,old_events,enquiry_port
import smtplib
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.conf import settings

# Create your views here.
name='NULL'

def home(request):
    user=request.user
    print(user)
    return render(request,'clone/homepage.html',{})


def signup(request):
    return render(request,'clone/signup.html')




def create(request):
    if request.method == 'POST':
        
        name = request.POST["name"]
        email= request.POST["email"]

        phone_number= request.POST["phone_number"]
        Studying= request.POST["Studying"]
        
        education_intrest= request.POST["education_intrest"]
        city= request.POST["city"]
        password= request.POST["pass"]
        

        a=account(name=name,email=email,phone_number=phone_number,studying=Studying,education_intrest=education_intrest,city=city)
        a.save()
        user =User.objects.create_user(username=name,first_name=name,last_name='NULL',email=email,password=password)
        user.save()
        return redirect('/')
            
    else:
        messages.info(request,'Method should be post....!!!!')
        return redirect('/')    



def new_event(request):
  
    data = new_events.objects.all()
    data2 = old_events.objects.all()


    for x in data:
        print(x.upcoming_form)


    return render(request,'clone/newevents.html',{"data":data,"data2":data2})     

def contact(request):
    return render(request,'clone/contact.html')


def about_contact(request):    
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        number = str(request.POST.get('number'))
        country = request.POST.get('country')
        subject = request.POST.get('subject')
        disp = request.POST.get('disp')
        en_title = request.POST.get('en_title')
        enquiry = enquiry_port(fullname=fullname,email=email,number=number,country=country,subject=subject,disp=disp,en_title=en_title)
        enquiry.save()
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(email, receivers, subject)         
            print("Successfully sent email")
        except SMTPException:
            print("Error: unable to send email")
            return redirect('')    


    return redirect('/') 

def news(request):
    data = new_events.objects.all()

    data3 = old_events.objects.all()

    return render(request,'clone/news.html',{"data":data,"data3":data3}  ) 


def QnA(request):
    return render(request,'clone/QnA.html')

    
def login(request):
    

    return render(request,'clone/login.html')



def loggin(request):
    email= request.POST['email']
    pasword= request.POST['password']

    u=User.objects.get(email=email)
    name=u.username
    user =authenticate(request,Username=name,password=pasword)
    print(user)
    if user is not None:
        auth.login(request,user)
        return redirect('/')
    else:
        messages.info(request,'username or password is incorrect')
        return redirect("/login")
 


def logout(request):
    auth.logout(request)
    return redirect("/")

def career(request):
    return render(request,'clone/career.html')        
    
def Blog(request):
    return render(request,'clone/Blog.html')


