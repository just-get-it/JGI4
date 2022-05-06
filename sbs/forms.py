#-*- coding: utf-8 -*-
from django import forms
from .models import Items,t1,about,review,page,mesg,like,foll,cont,post
from datetime import datetime

class m1(forms.ModelForm):
   class Meta:
     model= Items
     CHOICES = (('PENDING', 'PENDING'),('BOUGHT', 'BOUGHT'),('NOT AVAILABLE', 'NOT AVAILABLE'),) 
     fields=['Item','Quantity','status','date',]
     widgets={
            'Item':forms.TextInput(attrs={'placeholder':'enter your channel name'}),
            'Quantity':forms.TextInput(),
            'status':forms.TextInput(),
            'date':forms.DateInput(attrs={'class':'border rounded w-full py-2 px-4 outline-none focus:shadow-outline'})
        }

class m(forms.Form): 
    CHOICES = (('PENDING', 'PENDING'),('BOUGHT', 'BOUGHT'),('NOT AVAILABLE', 'NOT AVAILABLE'),) 
    Item = forms.CharField(max_length=50)  
    Quantity  = forms.CharField(max_length = 100) 
    status = forms.ChoiceField(choices=CHOICES)
    date = forms.DateField(initial=datetime.today)

class n(forms.Form): 
    business_code=forms.CharField(max_length=50)
    cust_number=forms.CharField(max_length=50)
    name_customer=forms.CharField(max_length=50)
    clear_date=forms.CharField(max_length=50)
    buisness_year=forms.CharField(max_length=50)
    doc_id=forms.CharField(max_length=50)
    posting_date=forms.CharField(max_length=50)
    document_create_date=forms.CharField(max_length=50)
    document_create_date1=forms.CharField(max_length=50)
    due_in_date=forms.CharField(max_length=50)
    invoice_currency=forms.CharField(max_length=50)
    document_type=forms.CharField(max_length=50)
    posting_id=forms.CharField(max_length=50)
    area_business=forms.CharField(max_length=50)
    total_open_amount=forms.CharField(max_length=50)
    baseline_create_date=forms.CharField(max_length=50)
    cust_payment_terms=forms.CharField(max_length=50)
    invoice_id=forms.CharField(max_length=50)
    isOpen=forms.CharField(max_length=50)


class n1(forms.ModelForm):
   class Meta:
     model= t1
     fields=[
       #'business_code',
       #'cust_number',
       'name_customer',
       'clear_date',
       'buisness_year',
       'doc_id',
       'posting_date',
       'document_create_date',
       'document_create_date',
       'due_in_date',
       'invoice_currency',
       'document_type',
       'posting_id',
       'area_business',
       'total_open_amount',
       'baseline_create_date',
       'cust_payment_terms',
       'invoice_id',
       'isOpen'
     ]
     widgets={
            'business_code':forms.TextInput(),
            'cust_number':forms.TextInput(),
            'name_customer':forms.TextInput(),
            'clear_date':forms.TextInput(),
            'buisness_year':forms.TextInput(),
            'doc_id':forms.TextInput(),
            'posting_date':forms.TextInput(),
            'document_create_date':forms.TextInput(),
            'document_create_date1':forms.TextInput(),
            'due_in_date':forms.TextInput(),
            'invoice_currency':forms.TextInput(),
            'document_type':forms.TextInput(),
            'posting_id':forms.TextInput(),
            'area_business':forms.TextInput(),
            'total_open_amount':forms.TextInput(),
            'baseline_create_date':forms.TextInput(),
            'cust_payment_terms':forms.TextInput(),
            #'invoice_id':forms.TextInput(),
            'isOpen':forms.TextInput()
        }

class pfrm(forms.Form): 
    #CHOICES = (('PENDING', 'PENDING'),('BOUGHT', 'BOUGHT'),('NOT AVAILABLE', 'NOT AVAILABLE'),) 
    name = forms.CharField(max_length=50,label='Page name (required)',widget=forms.TextInput(attrs={'placeholder': 'Page name (required)'}))  
    catg  = forms.CharField(max_length = 100,widget=forms.TextInput(attrs={'placeholder': 'Category (required)'})) 
    desc = forms.CharField(max_length = 500,widget=forms.TextInput(attrs={'placeholder': 'Description (required)'}))
    #date = forms.DateField(initial=datetime.today)

class postf(forms.Form): 
    #CHOICES = (('PENDING', 'PENDING'),('BOUGHT', 'BOUGHT'),('NOT AVAILABLE', 'NOT AVAILABLE'),) 
    desc = forms.CharField(max_length=500,label='Description (required)',widget=forms.TextInput(attrs={'placeholder': 'Description (required)'}))  
    img  = forms.ImageField()
    #pid  = forms.CharField() 
    
    #date = forms.DateField(initial=datetime.today)

class commen(forms.Form):
    dete = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'placeholder': '.. Comment here'}))
