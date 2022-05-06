import uuid
from django.db import models
from django.conf import settings
from datetime import datetime
from django.urls import reverse
#from .views  import index

User=settings.AUTH_USER_MODEL


class Items(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    Item=models.CharField(max_length=50)
    Quantity=models.CharField(max_length=50)
    slug=models.SlugField()
    status=models.CharField(max_length=500)
    date = models.DateField()

    def get_absolute_url(self):
        return reverse('home')
    
    def __str__(self):
        return self.Item

#business_code,cust_number,name_customer,clear_date,buisness_year,doc_id,posting_date,document_create_date,
#document_create_date,due_in_date,invoice_currency,document_type,posting_id,area_business,total_open_amount,
#baseline_create_date,cust_payment_terms,invoice_id,isOpen
class t1(models.Model):
    #user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    id=models.AutoField(primary_key=True)
    business_code=models.CharField(max_length=50)
    cust_number=models.CharField(max_length=50)
    name_customer=models.CharField(max_length=50)
    clear_date=models.CharField(max_length=50)
    buisness_year=models.CharField(max_length=50)
    doc_id=models.CharField(max_length=50)
    posting_date=models.CharField(max_length=50)
    document_create_date=models.CharField(max_length=50)
    document_create_date1=models.CharField(max_length=50)
    due_in_date=models.CharField(max_length=50)
    invoice_currency=models.CharField(max_length=50)
    document_type=models.CharField(max_length=50)
    posting_id=models.CharField(max_length=50)
    area_business=models.CharField(max_length=50)
    total_open_amount=models.CharField(max_length=50)
    baseline_create_date=models.CharField(max_length=50)
    cust_payment_terms=models.CharField(max_length=50)
    invoice_id=models.CharField(max_length=50)
    isOpen=models.CharField(max_length=50)

    def __str__(self):
        return self.name_customer

    def get_absolute_url(self):
        return reverse('home1')


class about(models.Model):
    id=models.AutoField(primary_key=True)
    des =models.CharField(max_length=500)
    web=models.CharField(max_length=500)
    comm=models.CharField(max_length=500)
    inst=models.CharField(max_length=500)
    twit=models.CharField(max_length=500)
    offer=models.CharField(max_length=500)
    tran=models.CharField(max_length=500)
    
class page(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    catg=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    desc=models.CharField(max_length=500)
    webs=models.CharField(max_length=500,default='google.com')
    loct=models.CharField(max_length=500,default='varanasi')
    hour=models.CharField(max_length=500,default='Unknown')
    slug=models.SlugField()
    page_art=models.ImageField(upload_to="channel/", default='/media/dp.png')
    page_icon=models.ImageField(upload_to='profile/', default='/media/g.png')

    def __str__(self):
        return self.name



class review(models.Model):
    id=models.AutoField(primary_key=True)
    desc=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    pid=models.ForeignKey('about',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name_customer
    def get_absolute_url(self):
        return reverse('home1')


class foll(models.Model):
    id=models.AutoField(primary_key=True)
    #desc=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    pid=models.ForeignKey('about',on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.name_customer
    def get_absolute_url(self):
        return reverse('home1')


class mesg(models.Model):
    id=models.AutoField(primary_key=True)
    #type=models.CharField(max_length=500)
    dete=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    #user1=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    #pid=models.ForeignKey('about',on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.name_customer
    def get_absolute_url(self):
        return reverse('home1')

class post(models.Model):
    id=models.AutoField(primary_key=True)
    #type=models.CharField(max_length=500)
    desc=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    img=models.ImageField(upload_to='media/img/')
    slug=models.SlugField()
    #user1=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    paid=models.CharField(max_length=50)
    cs=models.IntegerField()
    ls=models.IntegerField()

    
    def __str__(self):
        return self.desc
    def get_absolute_url(self):
        return reverse('home1')

class cont(models.Model):
    cid=models.AutoField(primary_key=True)
    type=models.CharField(max_length=500,default='0')
    slug=models.SlugField()
    dete=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    pid=models.IntegerField()
    paid=models.CharField(max_length=50)
    
    def __str__(self):
        return self.dete
    def get_absolute_url(self):
        return reverse('home1')

class like(models.Model):
    id=models.AutoField(primary_key=True)
    #desc=models.CharField(max_length=500)
    slug=models.SlugField()
   # user1=models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    pid=models.IntegerField()
    paid=models.IntegerField()

    def __str__(self):
        return self.lid
    def get_absolute_url(self):
        return reverse('home1')