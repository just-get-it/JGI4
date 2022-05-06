from django.shortcuts import render,redirect
from django.http import HttpResponse
import datetime
from django.contrib.auth.models import User,auth
from .models import InputTable,Total_values_Table
from inputform.timeconversion import *
from inputform.resubmit import second_table
from inputform.divide_floordata import floor_data_seperation


#this duplicate dictonary render the dynamic  date and time on page loading and also provide some duplicate zeros in some cells
#do not modify duplicate_dictonary() it may effect the webpage
def duplicate_dictonary():
    presentdate=datetime.datetime.now()
    return ({"hour_12":timeconvert.this_hour,"minutes":presentdate.minute,
            "seconds":presentdate.second,"am_or_pm":timeconvert.am_or_pm,
            "next_hour":nexthourconvert.next_hour,"next_hour_am_or_pm":nexthourconvert.next_hour_am_or_pm})
    
     


#main function
def home(request):    

    #-----------Sending 24hrs time to timeconversion.py module-----------------------------------
    presentdate=datetime.datetime.now()
    presenthour=presentdate.hour
    #timeconvert and nexthourconvert are located in timeconversion.py --------------------------
    timeconvert(presenthour)
    nexthourconvert(presenthour+1)  

    #for data submission
    if request.method=='POST':
 
        ##---------sending data to variables then to database inputtable-----------------------
        date=presentdate.date()
        time=presentdate.time()
        factory_name=request.POST.get('factory_name')
        floor_no=request.POST.get('floor_no')
        Sew_Handle=request.POST.get('Sew_Handle')
        shears=request.POST.get('shears')
        Bundle=request.POST.get('Bundle')
        Machine_Delay=request.POST.get('Machine_Delay')
        MB=request.POST.get('H1_MB')
        Personal_fatigue=request.POST.get('Personal_fatigue')  
        WT=request.POST.get('H1_WT')
        Others=request.POST.get('Others') 

        iptable=InputTable(factory_name=factory_name,floor_no=floor_no,date=date,time=time,
                            Sew_Handle=Sew_Handle,shears=shears,Bundle=Bundle,Machine_Delay=Machine_Delay,H1_MB=MB,Personal_fatigue=Personal_fatigue,H1_WT=WT,Others=Others)
        
        iptable.save()      
        #-------------------------------------------------------------------------------------------------------------------
        #calling the function ,which seperates the data based on date and floor no and send to the another table 
        # it is located in divide_floordata.py
        floor_data_seperation(presentdate,date,time,factory_name,floor_no,Sew_Handle,shears,Bundle,Machine_Delay,MB,Personal_fatigue,WT,Others)
        #--------------------------------------------------------------------------------------------------------------------
        
        return render(request,'inputform/index.html',duplicate_dictonary())

    else:
        return render(request,'inputform/index.html',duplicate_dictonary())

