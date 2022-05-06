from django.shortcuts import render
from .forms import UserForm,windowForm
from .models import UserProfileInfo,OperatorWindow,leaveCalender,operator_skill_matrix
from .models import line1attendence,line2attendence,line3attendence,line4attendence,line5attendence
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from datetime import date
from itertools import chain

def index(request):
    return render(request,'op_index.html')
@login_required
def special(request):
    return HttpResponse("You are logged in !")

def logout(request):
    return render(request,'op_index.html')

def register(request):
    if request.method == 'POST':
        operator_name=request.POST['operator_name']
        operator_id=request.POST['operator_id']
        line_no=request.POST['line_no']
        address=request.POST['address']
        product_category=request.POST['product_category']
        product_sub_category=request.POST['product_sub_category']
        operation=request.POST.getlist('operation')
        operation_complexity=request.POST['operation_complexity']
        no_of_operation=request.POST['no_of_operation']
        skill_percentage=request.POST.getlist('skill_percentage')
        grade=request.POST['grade']
        password=request.POST['password']
        operators=UserProfileInfo.objects.all()
        print(operator_id,operation,skill_percentage)
        operationconvert=listToString(operation)
        skillconvert=listToString(skill_percentage)
        c=0
        for i in operators:
            if(i.operator_id==operator_id):
                c=1
        if(c==1):
            mess="UserId is Already used"
            return render(request,'op_registration.html',{'mess':mess})
        else:
            user_info=UserProfileInfo(operator_name=operator_name,operator_id=operator_id,line_no=line_no,address=address,product_category=product_category
            ,product_sub_category=product_sub_category,operation=operationconvert,operation_complexity=operation_complexity
            ,no_of_operation=no_of_operation,skill_percentage=skillconvert,grade=grade,password=password)
            user_info.save()
            
            for i, val in enumerate(skill_percentage):
                skillmatrix=operator_skill_matrix(operator_id=operator_id,operator_name=operator_name,line_no=line_no,product_category=product_category
                ,grade=grade,skill_percentage=val,operation=operation[i])
                skillmatrix.save()

            return render(request,'op_login.html')
    else:
        return render(request,'op_registration.html')

def user_login(request):
    if request.method == 'POST':
        operator_id = request.POST.get('operator_id')
        password = request.POST.get('password')
        result=UserProfileInfo.objects.filter(operator_id=operator_id,password=password)
        if result:
            for i in result:
                name=i.operator_name
                id=i.operator_id
                product=i.product_category
                lineno=i.line_no
            hr = str(datetime.datetime.now().hour)
            min = str(datetime.datetime.now().minute)
            time=hr+':'+min
            corrdate=str(datetime.date.today())
            date=dateFormat(corrdate)
            print(name,id,product,time,date)
            total_pieces=0
            rework_pieces=0
            daily_repair=0
            daily_finish_return=0
            daily_cut_defect=0
            dailycuttingmiss=0
            displace=0
            setting=0
            breakdown=0
            powerfailure=0
            machineissue=0
            qualityissue=0
            trimsissue=0
            others=0
            delaystart=0
            demo=0
            machinelosstime=0
            colosstime=0
            waitinglosstime=0
            qualitylosstime=0
            learing=0
            fullswing=0
            return render(request, 'operator_window.html', {'name':name,'id':id,'product':product,'time':time,'date':date,'lineno':lineno
                ,'total_pieces':total_pieces,'rework_pieces':rework_pieces,'daily_repair':daily_repair
                ,'daily_finish_return':daily_finish_return,'daily_cut_defect':daily_cut_defect,'dailycuttingmiss':dailycuttingmiss
                ,'displace':displace,'setting':setting,'breakdown':breakdown,'powerfailure':powerfailure
                ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
                ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'machinelosstime':machinelosstime,'colosstime':colosstime,
                'waitinglosstime':waitinglosstime,'qualitylosstime':qualitylosstime})
        else:
            register='You have to register than you can login'
            return render(request, 'op_login.html', {'registerfirst':register})
    else:
        return render(request, 'op_login.html', {})

def window(request):
    if request.method=='POST' and 'machinestop' in request.POST:
        operator_id =request.POST['opid']
        operator_name =request.POST['opname']
        operation=request.POST['operation']
        start_time=request.POST['optime']
        hr = str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute)
        
        stop_time=hr+":"+min

        date=request.POST['opdate']
        total_pieces=request.POST['hourlyachieved']
        rework_pieces=request.POST['reworkpieces']
        maintenance=request.POST['maintenance']
        daily_repair=request.POST['dailyrepair']
        daily_finish_return=request.POST['dailyfinishreturn']
        daily_cut_defect=request.POST['dailycutdefect']
        dailycutting_miss=request.POST['dailycutmiss']
        displace=request.POST['displace']
        setting=request.POST['setting']
        breakdown=request.POST['breakdown']
        powerfailure=request.POST['powerfailure']
        machineissue=request.POST['machineissue']
        qualityissue=request.POST['qualityissue']
        trimsissue=request.POST['trimsissue']
        others=request.POST['others']
        delaystart=request.POST['delaystart']
        demo=request.POST['demo']
        learing=request.POST['learing']
        fullswing=request.POST['fullswing']
        qualitylosstime=request.POST['qualitylosstime']
        waitinglosstime=12.8
        machinelosstime=request.POST['machinelosstime']
        colosstime=request.POST['colosstime']


        maintenancename=""
        maintenanceval=0
        if maintenance == "dw0.5":
            maintenancename="Displace/Waiting"
            maintenanceval=0
            displace=float(displace)+float(maintenanceval)
        elif maintenance == "se1":
            maintenancename="Setting"
            maintenanceval=0
            setting=float(setting)+float(maintenanceval)
        elif maintenance == "br2":
            maintenancename="Breakdown"
            maintenanceval=0
            breakdown=float(breakdown)+float(maintenanceval)
        elif maintenance == "pf1":
            maintenancename="Power failure"
            maintenanceval=0
            powerfailure=float(powerfailure)+float(maintenanceval)

        machinelosstime=float(displace)+float(setting)+float(breakdown)+float(powerfailure)
        totallosstime=float(qualitylosstime)+float(waitinglosstime)+float(machinelosstime)+float(colosstime)
        print(maintenance,maintenanceval,maintenancename)
        window_info=OperatorWindow(operator_id=operator_id,operator_name=operator_name,operation=operation
            ,date=date,maintenance_name=maintenancename,maintenance_value=maintenanceval
            ,maintenance_stop_time=stop_time)
        window_info.save()                

        result=UserProfileInfo.objects.filter(operator_id=operator_id)
        if result:
            for i in result:
                name=i.operator_name
                id=i.operator_id
                product=i.product_category
                lineno=i.line_no
            hr = str(datetime.datetime.now().hour)
            min = str(datetime.datetime.now().minute)
            time=hr+':'+min
            corrdate=str(datetime.date.today())
            date=dateFormat(corrdate)
            print(name,id,product,time,date)
            return render(request, 'operator_window.html', {'name':name,'id':id,'product':product,'time':time
                ,'date':date,'lineno':lineno,'total_pieces':total_pieces,'rework_pieces':rework_pieces
                ,'dailycuttingmiss':dailycutting_miss,'daily_cut_defect':daily_cut_defect
                ,'daily_finish_return':daily_finish_return,'daily_repair':daily_repair
                ,'displace':displace,'setting':setting,'breakdown':breakdown,'powerfailure':powerfailure,'machinelosstime':machinelosstime
                ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
                ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'totallosstime':totallosstime,'colosstime':colosstime,
                'waitinglosstime':waitinglosstime,'qualitylosstime':qualitylosstime})
    if request.method=='POST' and 'machinestart' in request.POST:
        operator_id =request.POST['opid']
        operator_name =request.POST['opname']
        operation=request.POST['operation']
        start_time=request.POST['optime']
        date=request.POST['opdate']
        
        total_pieces=request.POST['hourlyachieved']
        rework_pieces=request.POST['reworkpieces']
        daily_repair=request.POST['dailyrepair']
        daily_finish_return=request.POST['dailyfinishreturn']
        daily_cut_defect=request.POST['dailycutdefect']
        dailycutting_miss=request.POST['dailycutmiss']

        displace=request.POST['displace']
        setting=request.POST['setting']
        breakdown=request.POST['breakdown']
        powerfailure=request.POST['powerfailure']

        machineissue=request.POST['machineissue']
        qualityissue=request.POST['qualityissue']
        trimsissue=request.POST['trimsissue']
        others=request.POST['others']
        delaystart=request.POST['delaystart']
        demo=request.POST['demo']
        learing=request.POST['learing']
        fullswing=request.POST['fullswing']

        qualitylosstime=request.POST['qualitylosstime']
        waitinglosstime=12.8
        machinelosstime=request.POST['machinelosstime']
        colosstime=request.POST['colosstime']


        
        hr = str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute)
        h=int(hr) #converted hour in h
        m=int(min)
        start_time=hr+":"+min
        maintenancename=""
        x=OperatorWindow.objects.filter(operator_id=operator_id,date=date)
        for i in x:
            st=i.maintenance_stop_time 
            idd=i.id
            maintenancename=i.maintenance_name

        
        t=strtolistfortime(st)
        hr1=t[0] #hour
        min1=t[1] #min
        hh=h-int(hr1)
        mm=m-int(min1)
        #value=str(hh)+":"+str(mm)
        value=(hh*60)+mm
        if maintenancename=='Displace/Waiting':
            displace=value
        elif maintenancename=='Setting':
            setting=value
        elif maintenancename=='Breakdown':
            breakdown=value
        elif maintenancename=='Power failure':
            powerfailure=value


        machinelosstime=float(displace)+float(setting)+float(breakdown)+float(powerfailure)
        totallosstime=float(qualitylosstime)+float(waitinglosstime)+float(machinelosstime)+float(colosstime)

       # window_info=OperatorWindow(operator_id=operator_id,operator_name=operator_name,operation=operation
       #     ,date=date,maintenance_start_time=start_time,maintenance_time=value,maintenance_name=maintenancename)
        window_info=OperatorWindow(operator_id=operator_id,id=idd,operator_name=operator_name,operation=operation,date=date,maintenance_stop_time=st, maintenance_start_time=start_time,maintenance_time=value,maintenance_name=maintenancename)
        window_info.save()                
        
        result=UserProfileInfo.objects.filter(operator_id=operator_id)
        if result:
            for i in result:
                name=i.operator_name
                id=i.operator_id
                product=i.product_category
                lineno=i.line_no
            hr = str(datetime.datetime.now().hour)
            min = str(datetime.datetime.now().minute)
            time=hr+':'+min
            corrdate=str(datetime.date.today())
            date=dateFormat(corrdate)
            print(name,id,product,time,date)
            return render(request, 'operator_window.html', {'name':name,'id':id,'product':product,'time':time
                ,'date':date,'lineno':lineno,'total_pieces':total_pieces,'rework_pieces':rework_pieces
                ,'dailycuttingmiss':dailycutting_miss,'daily_cut_defect':daily_cut_defect
                ,'daily_finish_return':daily_finish_return,'daily_repair':daily_repair
                ,'displace':displace,'setting':setting,'breakdown':breakdown,'powerfailure':powerfailure,'machinelosstime':machinelosstime
                ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
                ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'totallosstime':totallosstime,'colosstime':colosstime,
                'waitinglosstime':waitinglosstime,'qualitylosstime':qualitylosstime})
    if request.method=='POST' and 'saverework' in request.POST:
        operator_id =request.POST['opid']
        operator_name =request.POST['opname']
        operation=request.POST['operation']
        date=request.POST['opdate']
        rwp=int(request.POST['reworkpieces'])
        stitp=request.POST['hourlyachieved']
        selfreworktktno=request.POST['selfreworktktno']
        selfreworktktno_list=strtolist(selfreworktktno)
        repairtktno=request.POST['repairtktno']
        daily_repair=request.POST['dailyrepair']
        daily_finish_return=request.POST['dailyfinishreturn']
        daily_cut_defect=request.POST['dailycutdefect']
        dailycutting_miss=request.POST['dailycutmiss']
        finishreturntktno=request.POST['finishreturntktno']
        cutdefectno=request.POST['cutdefectno']
        cutmissdefectno=request.POST['cutmissdefectno']

        displace=request.POST['displace']
        setting=request.POST['setting']
        breakdown=request.POST['breakdown']
        powerfailure=request.POST['powerfailure']

        machineissue=request.POST['machineissue']
        qualityissue=request.POST['qualityissue']
        trimsissue=request.POST['trimsissue']
        others=request.POST['others']
        delaystart=request.POST['delaystart']
        demo=request.POST['demo']
        learing=request.POST['learing']
        fullswing=request.POST['fullswing']

        qualitylosstime=request.POST['qualitylosstime']
        waitinglosstime=12.8
        machinelosstime=request.POST['machinelosstime']
        colosstime=request.POST['colosstime']



        cutmissdefectno_list=strtolist(cutmissdefectno)
        dailycuttingmiss=(int(cutmissdefectno_list[1])-int(cutmissdefectno_list[0]))+1
        rework_ticket_no=selfreworktktno_list
        rework_ticket_no=list(filter(None,rework_ticket_no))
        listsize=len(rework_ticket_no)
        rework_pieces=(int(selfreworktktno_list[1])-int(selfreworktktno_list[0]))+1
        rwp=rwp+rework_pieces
        daily_repair=int(daily_repair)+1
        daily_finish_return=int(daily_finish_return)+1
        daily_cut_defect=int(daily_cut_defect)+1
        dailycutting_miss=int(dailycutting_miss)+int(dailycuttingmiss)
        totalpcs=int(rwp)+int(daily_repair)+int(daily_finish_return)+int(daily_cut_defect)+int(dailycutting_miss)
        qualitylosstime=int(rwp)*1+int(daily_repair)*1+int(daily_finish_return)*2+int(daily_cut_defect)*1+int(dailycutting_miss)*1.5
        coq=qualitylosstime*3
        window_info=OperatorWindow(operator_id=operator_id,operator_name=operator_name
            ,operation=operation,date=date,rework_ticket_no=selfreworktktno,repair_tkt_no=repairtktno
            ,finishreturn_tkt_no=finishreturntktno,cutdefect_no=cutdefectno,cutmiss_tkt_no=cutmissdefectno
            ,rework_pieces=rwp,daily_cutting_miss=dailycuttingmiss)
        window_info.save() 

        totallosstime=float(qualitylosstime)+float(waitinglosstime)+float(machinelosstime)+float(colosstime)
        result=UserProfileInfo.objects.filter(operator_id=operator_id)
        if result:
            for i in result:
                name=i.operator_name
                id=i.operator_id
                product=i.product_category
                lineno=i.line_no
            hr = str(datetime.datetime.now().hour)
            min = str(datetime.datetime.now().minute)
            time=hr+':'+min
            corrdate=str(datetime.date.today())
            date=dateFormat(corrdate)
            print(name,id,product,time,date)
            return render(request, 'operator_window.html', {'name':name,'id':id,'product':product,'time':time,'date':date,'lineno':lineno
                ,'rework_pieces':rwp,'total_pieces':stitp,'dailycuttingmiss':dailycutting_miss
                ,'daily_cut_defect':daily_cut_defect,'daily_finish_return':daily_finish_return
                ,'daily_repair':daily_repair,'qualitylosstime':qualitylosstime
                ,'totalpcs':totalpcs,'coq':coq,'displace':displace,'setting':setting,'breakdown':breakdown,'powerfailure':powerfailure
                ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
                ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'totallosstime':totallosstime,'machinelosstime':machinelosstime,'colosstime':colosstime,
                'waitinglosstime':waitinglosstime})
    if request.method=='POST' and 'saveticket' in request.POST:
        operator_id =request.POST['opid']
        date=request.POST['opdate']
        operator_name =request.POST['opname']
        operation=request.POST['operation']
        ticket_no_start=request.POST['ticketnostart']
        ticket_no_end=request.POST['ticketnoend']
        nextoperation=request.POST['nextoperation']
        stitp=request.POST['hourlyachieved']
        rwp=int(request.POST['reworkpieces'])
        daily_repair=request.POST['dailyrepair']
        daily_finish_return=request.POST['dailyfinishreturn']
        daily_cut_defect=request.POST['dailycutdefect']
        dailycuttingmiss=request.POST['dailycutmiss']

        displace=request.POST['displace']
        setting=request.POST['setting']
        breakdown=request.POST['breakdown']
        powerfailure=request.POST['powerfailure']

        machineissue=request.POST['machineissue']
        qualityissue=request.POST['qualityissue']
        trimsissue=request.POST['trimsissue']
        others=request.POST['others']
        delaystart=request.POST['delaystart']
        demo=request.POST['demo']
        learing=request.POST['learing']
        fullswing=request.POST['fullswing']
        qualitylosstime=request.POST['qualitylosstime']
        waitinglosstime=12.8
        machinelosstime=request.POST['machinelosstime']
        colosstime=request.POST['colosstime']



        stitp=int(stitp)
        total_pieces=(int(ticket_no_end)-int(ticket_no_start))+1
        stitp=stitp+total_pieces
        wip=int(nextoperation)-int(ticket_no_end)
        efficiency=(stitp*0.8)/450
        performance=(stitp*0.8)/(450-96.90)
        window_info=OperatorWindow(operator_id=operator_id,operator_name=operator_name,operation=operation
            ,ticket_no_start=ticket_no_start,date=date
            ,ticket_no_end=ticket_no_end,total_pieces=stitp,next_operation=nextoperation,wip=wip)
        window_info.save()
        totallosstime=float(qualitylosstime)+float(waitinglosstime)+float(machinelosstime)+float(colosstime)

        result=UserProfileInfo.objects.filter(operator_id=operator_id)
        if result:
            for i in result:
                name=i.operator_name
                id=i.operator_id
                product=i.product_category
                lineno=i.line_no
            hr = str(datetime.datetime.now().hour)
            min = str(datetime.datetime.now().minute)
            time=hr+':'+min
            corrdate=str(datetime.date.today())
            date=dateFormat(corrdate)
            print(name,id,product,time,date)
            return render(request, 'operator_window.html', {'name':name,'id':id,'product':product,'time':time,'date':date,'lineno':lineno
                ,'total_pieces':stitp,'wip':wip,'efficiency':efficiency,'performance':performance,'rework_pieces':rwp,'daily_repair':daily_repair
                ,'daily_finish_return':daily_finish_return,'daily_cut_defect':daily_cut_defect,'dailycuttingmiss':dailycuttingmiss
                ,'displace':displace,'setting':setting,'breakdown':breakdown,'powerfailure':powerfailure
                ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
                ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'totallosstime':totallosstime,'machinelosstime':machinelosstime,'colosstime':colosstime,
                'waitinglosstime':waitinglosstime,'qualitylosstime':qualitylosstime}) 

    if request.method=='POST' and 'costop' in request.POST:
        operator_id =request.POST['opid']
        operator_name =request.POST['opname']
        operation=request.POST['operation']
        start_time=request.POST['optime']
        hr = str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute)
        stop_time=hr+':'+min
        date=request.POST['opdate']
        total_pieces=request.POST['hourlyachieved']
        rework_pieces=request.POST['reworkpieces']
        daily_repair=request.POST['dailyrepair']
        daily_finish_return=request.POST['dailyfinishreturn']
        daily_cut_defect=request.POST['dailycutdefect']
        dailycutting_miss=request.POST['dailycutmiss']
        displace=request.POST['displace']
        setting=request.POST['setting']
        breakdown=request.POST['breakdown']
        powerfailure=request.POST['powerfailure']
        machineissue=request.POST['machineissue']
        qualityissue=request.POST['qualityissue']
        trimsissue=request.POST['trimsissue']
        others=request.POST['others']
        delaystart=request.POST['delaystart']
        demo=request.POST['demo']
        learing=request.POST['learing']
        fullswing=request.POST['fullswing']
        smed=request.POST['smed']
        qualitylosstime=request.POST['qualitylosstime']
        waitinglosstime=12.8
        machinelosstime=request.POST['machinelosstime']
        colosstime=request.POST['colosstime']




        smedname=""
        smedval=0
        if smed == "mi0.1":
            smedname="Machine Issue"
            smedval=0
            machineissue=float(machineissue)+float(smedval)
        elif smed == "qi0.1":
            smedname="Quality Issue"
            smedval=0
            qualityissue=float(qualityissue)+float(smedval)
        elif smed == "ti0.05":
            smedname="Trims Issue"
            smedval=0
            trimsissue=float(trimsissue)+float(smedval)
        elif smed == "ot0.05":
            smedname="Others"
            smedval=0
            others=float(others)+float(smedval)
        elif smed == "ds5.00":
            smedname="Delay Start"
            smedval=0
            delaystart=float(delaystart)+float(smedval)
        elif smed == "de5.00":
            smedname="Demo"
            smedval=0
            demo=float(demo)+float(smedval)
        elif smed == "le10.00":
            smedname="Learing"
            smedval=0
            learing=float(learing)+float(smedval)
        elif smed == "fs0.00":
            smedname="Full Swing"
            smedval=0
            fullswing=float(fullswing)+float(smedval)

        colosstime=float(machineissue)+float(qualityissue)+float(trimsissue)+float(others)+float(delaystart)+float(demo)+float(learing)+float(fullswing)
        totallosstime=float(qualitylosstime)+float(waitinglosstime)+float(machinelosstime)+float(colosstime)

        print(smed,smedval,smedname)
        window_info=OperatorWindow(operator_id=operator_id,operator_name=operator_name,operation=operation
            ,date=date,smed_stop_time=stop_time,smed_name=smedname,smed_value=smedval)
        window_info.save()                

        result=UserProfileInfo.objects.filter(operator_id=operator_id)
        if result:
            for i in result:
                name=i.operator_name
                id=i.operator_id
                product=i.product_category
                lineno=i.line_no
            hr = str(datetime.datetime.now().hour)
            min = str(datetime.datetime.now().minute)
            time=hr+':'+min
            corrdate=str(datetime.date.today())
            date=dateFormat(corrdate)
            print(name,id,product,time,date)
            return render(request, 'operator_window.html', {'name':name,'id':id,'product':product,'time':time
                ,'date':date,'lineno':lineno,'total_pieces':total_pieces,'rework_pieces':rework_pieces
                ,'dailycuttingmiss':dailycutting_miss,'daily_cut_defect':daily_cut_defect
                ,'daily_finish_return':daily_finish_return,'daily_repair':daily_repair
                ,'displace':displace,'setting':setting,'breakdown':breakdown,'powerfailure':powerfailure
                ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
                ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'colosstime':colosstime,'totallosstime':totallosstime,
                'machinelosstime':machinelosstime,
                'waitinglosstime':waitinglosstime,'qualitylosstime':qualitylosstime})
    if request.method=='POST' and 'costart' in request.POST:
        operator_id =request.POST['opid']
        operator_name =request.POST['opname']
        operation=request.POST['operation']
        start_time=request.POST['optime']
        date=request.POST['opdate']
        hr = str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute)
        h=int(hr) #converted hour in h
        m=int(min)
        start_time=hr+":"+min
        x=OperatorWindow.objects.filter(operator_id=operator_id,date=date)
        for i in x:
            st=i.smed_stop_time 
            idd=i.id
            smedname=i.smed_name
        
        t=strtolistfortime(st)
        hr1=t[0] #hour
        min1=t[1] #min
        hh=h-int(hr1)
        mm=m-int(min1)
        #value=str(hh)+":"+str(mm)
        value=(hh*60)+mm
        total_pieces=request.POST['hourlyachieved']
        rework_pieces=request.POST['reworkpieces']
        daily_repair=request.POST['dailyrepair']
        daily_finish_return=request.POST['dailyfinishreturn']
        daily_cut_defect=request.POST['dailycutdefect']
        dailycutting_miss=request.POST['dailycutmiss']
        displace=request.POST['displace']
        setting=request.POST['setting']
        breakdown=request.POST['breakdown']
        powerfailure=request.POST['powerfailure']
        machineissue=request.POST['machineissue']
        qualityissue=request.POST['qualityissue']
        trimsissue=request.POST['trimsissue']
        others=request.POST['others']
        delaystart=request.POST['delaystart']
        demo=request.POST['demo']
        learing=request.POST['learing']
        fullswing=request.POST['fullswing']
        qualitylosstime=request.POST['qualitylosstime']
        waitinglosstime=12.8
        machinelosstime=request.POST['machinelosstime']
        colosstime=request.POST['colosstime']


        if smedname=="Machine Issue":
            machineissue=value
        elif smedname=="Quality Issue":
            qualityissue=value
        elif smedname=="Trims Issue":
            trimsissue=value
        elif smedname=="Others":
            others=value
        elif smedname=="Delay Start":
            delaystart=value
        elif smedname=="Demo":
            demo=value
        elif smedname=="Learing":
            learing=value
        elif smedname=="Full Swing":
            fullswing=value


        colosstime=float(machineissue)+float(qualityissue)+float(trimsissue)+float(others)+float(delaystart)+float(demo)+float(learing)+float(fullswing)
        totallosstime=float(qualitylosstime)+float(waitinglosstime)+float(machinelosstime)+float(colosstime)

        #print(smed,smedval,smedname)
        window_info=OperatorWindow(operator_id=operator_id,id=idd,operator_name=operator_name,operation=operation
            ,date=date,smed_start_time=start_time,smed_value=value,smed_name=smedname,smed_stop_time=st)
        window_info.save()                

        result=UserProfileInfo.objects.filter(operator_id=operator_id)
        if result:
            for i in result:
                name=i.operator_name
                id=i.operator_id
                product=i.product_category
                lineno=i.line_no
            hr = str(datetime.datetime.now().hour)
            min = str(datetime.datetime.now().minute)
            time=hr+':'+min
            corrdate=str(datetime.date.today())
            date=dateFormat(corrdate)
            print(name,id,product,time,date)
            return render(request, 'operator_window.html', {'name':name,'id':id,'product':product,'time':time
                ,'date':date,'lineno':lineno,'total_pieces':total_pieces,'rework_pieces':rework_pieces
                ,'dailycuttingmiss':dailycutting_miss,'daily_cut_defect':daily_cut_defect
                ,'daily_finish_return':daily_finish_return,'daily_repair':daily_repair
                ,'displace':displace,'setting':setting,'breakdown':breakdown,'powerfailure':powerfailure
                ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
                ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'colosstime':colosstime,'totallosstime':totallosstime,
                'machinelosstime':machinelosstime,
                'waitinglosstime':waitinglosstime,'qualitylosstime':qualitylosstime})

    total_pieces=0
    rework_pieces=0
    return render(request,'operator_window.html',{'total_pieces':total_pieces,'rework_pieces':rework_pieces})

def windowreportindex(request):
    return render(request,'windowreport.html')   


def windowreport(request):
    if request.method=='POST':
        operatorid=request.POST['opid']
        operation=request.POST['operation']
        date=request.POST['date']
        print(operatorid,operation,str(datetime.date.today()))
        reports=OperatorWindow.objects.filter(operator_id=operatorid,operation=operation,date=date)
        print(reports)
        a=0
        for i in reports:
            a=a+i.total_pieces
        userp=UserProfileInfo.objects.filter(operator_id=operatorid)
        efficiency=(a*0.8)/450
        performance=(a*0.8)/(450-96.90)
        return render(request,'operatorwindowreport.html',{'reports':reports,'total':a
            ,'userp':userp,'efficiency':efficiency,'performance':performance})
    
    return render(request,'operatorwindowreport.html')

def reworkreport(request):
    if request.method=='POST':
        operatorid=request.POST['opid']
        operation=request.POST['operation']
        date=request.POST['date']
        print(operatorid,operation,date,str(datetime.date.today()))
        reports=OperatorWindow.objects.filter(operator_id=operatorid,operation=operation,date=date)
        print(reports)
        a=0
        drep=0
        ftktno=0
        cutdefno=0
        daicutmiss=0
        for i in reports:
            if i.rework_ticket_no!="": 
                reworkticketlist=strtolist(i.rework_ticket_no)
                a=a+((int(reworkticketlist[1])-int(reworkticketlist[0]))+1)
            if i.repair_tkt_no!=0:
                drep=drep+1
            if i.finishreturn_tkt_no!=0:
                ftktno=ftktno+1
            if i.cutdefect_no!=0:
                cutdefno=cutdefno+1
            if i.daily_cutting_miss!=0:
                daicutmiss=daicutmiss+i.daily_cutting_miss

        totalpcs=int(a)+int(drep)+int(ftktno)+int(cutdefno)+int(daicutmiss)
        qualitytimeloss=int(a)*1+int(drep)*1+int(ftktno)*2+int(cutdefno)*1+int(daicutmiss)*1.5
        coq=qualitytimeloss*3

        userp=UserProfileInfo.objects.filter(operator_id=operatorid)
        return render(request,'reworkreport.html',{'reports':reports,'total':a,'userp':userp,'totalpcs':totalpcs
            ,'qualitytimeloss':qualitytimeloss,'coq':coq,'dailyrepair':drep,'dailyfinishreturn':ftktno
            ,'dailycutdefect':cutdefno,'dailycuttingmiss':daicutmiss})
    return render(request,'reworkreport.html') 

def maintenancereport(request):
    if request.method=='POST':
        operatorid=request.POST['opid']
        operation=request.POST['operation']
        date=request.POST['date']
        print(operatorid,operation,date,str(datetime.date.today()))
        reports=OperatorWindow.objects.filter(operator_id=operatorid,operation=operation,date=date)
        print(reports)
        displace=0
        breakdown=0
        setting=0
        powerfailure=0
        for i in reports:
            if i.maintenance_name=='Displace/Waiting':
                displace=displace+convert(i.maintenance_time)
            elif i.maintenance_name=='Breakdown':
                breakdown=breakdown+convert(i.maintenance_time)
            elif i.maintenance_name=='Setting':
                setting=setting+convert(i.maintenance_time)
            elif i.maintenance_name=='Power failure':
                powerfailure=powerfailure+convert(i.maintenance_time)

        machinelosstime=displace+breakdown+setting+powerfailure

        userp=UserProfileInfo.objects.filter(operator_id=operatorid)
        return render(request,'operatorwindowmaintenancereport.html',{'reports':reports,'userp':userp
            ,'displace':displace,'breakdown':breakdown,'setting':setting,'powerfailure':powerfailure,'machinelosstime':machinelosstime})
    return render(request,'operatorwindowmaintenancereport.html')

def smedreport(request):
    if request.method=='POST':
        operatorid=request.POST['opid']
        operation=request.POST['operation']
        date=request.POST['date']
        print(operatorid,operation,date,str(datetime.date.today()))
        reports=OperatorWindow.objects.filter(operator_id=operatorid,operation=operation,date=date)
        print(reports)
        machineissue=0
        qualityissue=0
        trimsissue=0
        others=0
        delaystart=0
        demo=0
        learing=0
        fullswing=0
        for i in reports:
            if i.smed_name=='Machine Issue':
                machineissue=machineissue+convert(i.smed_value)
            elif i.smed_name=='Quality Issue':
                qualityissue=qualityissue+convert(i.smed_value)
            elif i.smed_name=='Trims Issue':
                trimsissue=trimsissue+convert(i.smed_value)
            elif i.smed_name=='Others':
                others=others+convert(i.smed_value)
            elif i.smed_name=='Delay Start':
                delaystart=delaystart+convert(i.smed_value)
            elif i.smed_name=='Demo':
                demo=demo+convert(i.smed_value)
            elif i.smed_name=='Learing':
                learing=learing+convert(i.smed_value)
            elif i.smed_name=='Full Swing':
                fullswing=fullswing+convert(i.smed_value)

        colosstime=machineissue+qualityissue+trimsissue+others+delaystart+demo+learing+fullswing

        userp=UserProfileInfo.objects.filter(operator_id=operatorid)
        return render(request,'operatorwindowsmedreport.html',{'reports':reports,'userp':userp
            ,'machineissue':machineissue,'qualityissue':qualityissue,'trimsissue':trimsissue,'others':others
            ,'delaystart':delaystart,'demo':demo,'learing':learing,'fullswing':fullswing,'colosstime':colosstime})
    return render(request,'operatorwindowsmedreport.html')

def operatorskillmatrix(request):
    dart=0
    panel=0
    dartpanelpressing=0
    centrebackstitch=0
    diamondstitch=0
    chestweltiron=0
    chestweltattach=0
    sideseam=0
    
    if request.method=='POST' and 'linesubmit' in request.POST:
        lineno=request.POST['lineno']
        product=request.POST['product']
        inpdate=request.POST['date']
        print(str(inpdate))
        cdate=str(date.today())
        if(int(lineno)==1):
            operator_list=operator_skill_matrix.objects.filter(line_no=1,product_category=product)
            
            for operator in operator_list:
                if 'dart_stitch' in operator.operation:
                    dart=dart+1
                elif 'panel_attach' in operator.operation:
                    panel=panel+1
                elif 'dart_and_panel_pressing' in operator.operation:
                    dartpanelpressing=dartpanelpressing+1
                elif 'centre_back_stitch' in operator.operation:
                    centrebackstitch=centrebackstitch+1
                elif 'diamond_stitch' in operator.operation:
                    diamondstitch=diamondstitch+1
                elif 'chest_welt_iron' in operator.operation:
                    chestweltiron=chestweltiron+1
                elif 'chest_welt_attach' in operator.operation:
                    chestweltattach=chestweltattach+1
                elif 'side_seam' in operator.operation:
                    sideseam=sideseam+1
            
            operatorpop = {'dart_stitch':dart, 'panel_attach':panel,'dart_and_panel_pressing':dartpanelpressing
            ,'centre_back_stitch':centrebackstitch,'diamond_stitch':diamondstitch
            ,'chest_welt_iron':chestweltiron,'chest_welt_attach':chestweltattach,'side_seam':sideseam}

            operator_list=UserProfileInfo.objects.filter(line_no=1,product_category=product)
            sumachieve=0
            for operator in operator_list:
                ope=strtolistforoperation(operator.operation)
                sk=strtolistforoperation(operator.skill_percentage)
                sumachieve=sumachieve+get_achieved(zip(ope,sk))
            operator_attendences=line1attendence.objects.filter(product=product,date=inpdate)
            return render(request,'operator_skill_matrix_linewise.html',{'operator_list':operator_list
            ,'operator_attendences':operator_attendences,'cdate':cdate,'inpdate':inpdate
            ,'lineno':lineno,'product':product,'operatorpop':operatorpop,'achievedskilllevel':sumachieve})
        elif(int(lineno)==2):
            operator_list=operator_skill_matrix.objects.filter(line_no=2,product_category=product)
            
            for operator in operator_list:
                if 'dart_stitch' in operator.operation:
                    dart=dart+1
                elif 'panel_attach' in operator.operation:
                    panel=panel+1
                elif 'dart_and_panel_pressing' in operator.operation:
                    dartpanelpressing=dartpanelpressing+1
                elif 'centre_back_stitch' in operator.operation:
                    centrebackstitch=centrebackstitch+1
                elif 'diamond_stitch' in operator.operation:
                    diamondstitch=diamondstitch+1
                elif 'chest_welt_iron' in operator.operation:
                    chestweltiron=chestweltiron+1
                elif 'chest_welt_attach' in operator.operation:
                    chestweltattach=chestweltattach+1
                elif 'side_seam' in operator.operation:
                    sideseam=sideseam+1
            
            operatorpop = {'dart_stitch':dart, 'panel_attach':panel,'dart_and_panel_pressing':dartpanelpressing
            ,'centre_back_stitch':centrebackstitch,'diamond_stitch':diamondstitch
            ,'chest_welt_iron':chestweltiron,'chest_welt_attach':chestweltattach,'side_seam':sideseam}

            operator_list=UserProfileInfo.objects.filter(line_no=2,product_category=product)
            sumachieve=0
            for operator in operator_list:
                ope=strtolistforoperation(operator.operation)
                sk=strtolistforoperation(operator.skill_percentage)
                sumachieve=sumachieve+get_achieved(zip(ope,sk))
            operator_attendences=line2attendence.objects.filter(product=product,date=inpdate)
            return render(request,'operator_skill_matrix_linewise',{'operator_list':operator_list
            ,'operator_attendences':operator_attendences,'cdate':cdate,'inpdate':inpdate
            ,'lineno':lineno,'product':product,'operatorpop':operatorpop,'achievedskilllevel':sumachieve})
        elif(int(lineno)==3):
            operator_list=operator_skill_matrix.objects.filter(line_no=3,product_category=product)
            
            for operator in operator_list:
                if 'dart_stitch' in operator.operation:
                    dart=dart+1
                elif 'panel_attach' in operator.operation:
                    panel=panel+1
                elif 'dart_and_panel_pressing' in operator.operation:
                    dartpanelpressing=dartpanelpressing+1
                elif 'centre_back_stitch' in operator.operation:
                    centrebackstitch=centrebackstitch+1
                elif 'diamond_stitch' in operator.operation:
                    diamondstitch=diamondstitch+1
                elif 'chest_welt_iron' in operator.operation:
                    chestweltiron=chestweltiron+1
                elif 'chest_welt_attach' in operator.operation:
                    chestweltattach=chestweltattach+1
                elif 'side_seam' in operator.operation:
                    sideseam=sideseam+1
            
            operatorpop = {'dart_stitch':dart, 'panel_attach':panel,'dart_and_panel_pressing':dartpanelpressing
            ,'centre_back_stitch':centrebackstitch,'diamond_stitch':diamondstitch
            ,'chest_welt_iron':chestweltiron,'chest_welt_attach':chestweltattach,'side_seam':sideseam}

            operator_list=UserProfileInfo.objects.filter(line_no=3,product_category=product)
            sumachieve=0
            for operator in operator_list:
                ope=strtolistforoperation(operator.operation)
                sk=strtolistforoperation(operator.skill_percentage)
                sumachieve=sumachieve+get_achieved(zip(ope,sk))
            operator_attendences=line3attendence.objects.filter(product=product,date=inpdate)
            return render(request,'operator_skill_matrix_linewise.html',{'operator_list':operator_list
            ,'operator_attendences':operator_attendences,'cdate':cdate,'inpdate':inpdate
            ,'lineno':lineno,'product':product,'operatorpop':operatorpop,'achievedskilllevel':sumachieve})
        elif(int(lineno)==4):
            operator_list=operator_skill_matrix.objects.filter(line_no=4,product_category=product)
            
            for operator in operator_list:
                if 'dart_stitch' in operator.operation:
                    dart=dart+1
                elif 'panel_attach' in operator.operation:
                    panel=panel+1
                elif 'dart_and_panel_pressing' in operator.operation:
                    dartpanelpressing=dartpanelpressing+1
                elif 'centre_back_stitch' in operator.operation:
                    centrebackstitch=centrebackstitch+1
                elif 'diamond_stitch' in operator.operation:
                    diamondstitch=diamondstitch+1
                elif 'chest_welt_iron' in operator.operation:
                    chestweltiron=chestweltiron+1
                elif 'chest_welt_attach' in operator.operation:
                    chestweltattach=chestweltattach+1
                elif 'side_seam' in operator.operation:
                    sideseam=sideseam+1
            
            operatorpop = {'dart_stitch':dart, 'panel_attach':panel,'dart_and_panel_pressing':dartpanelpressing
            ,'centre_back_stitch':centrebackstitch,'diamond_stitch':diamondstitch
            ,'chest_welt_iron':chestweltiron,'chest_welt_attach':chestweltattach,'side_seam':sideseam}

            operator_list=UserProfileInfo.objects.filter(line_no=4,product_category=product)
            sumachieve=0
            for operator in operator_list:
                ope=strtolistforoperation(operator.operation)
                sk=strtolistforoperation(operator.skill_percentage)
                sumachieve=sumachieve+get_achieved(zip(ope,sk))
            operator_attendences=line4attendence.objects.filter(product=product,date=inpdate)
            return render(request,'operator_skill_matrix_linewise.html',{'operator_list':operator_list
            ,'operator_attendences':operator_attendences,'cdate':cdate,'inpdate':inpdate
            ,'lineno':lineno,'product':product,'operatorpop':operatorpop,'achievedskilllevel':sumachieve})
        elif(int(lineno)==5):
            operator_list=operator_skill_matrix.objects.filter(line_no=5,product_category=product)
            
            for operator in operator_list:
                if 'dart_stitch' in operator.operation:
                    dart=dart+1
                elif 'panel_attach' in operator.operation:
                    panel=panel+1
                elif 'dart_and_panel_pressing' in operator.operation:
                    dartpanelpressing=dartpanelpressing+1
                elif 'centre_back_stitch' in operator.operation:
                    centrebackstitch=centrebackstitch+1
                elif 'diamond_stitch' in operator.operation:
                    diamondstitch=diamondstitch+1
                elif 'chest_welt_iron' in operator.operation:
                    chestweltiron=chestweltiron+1
                elif 'chest_welt_attach' in operator.operation:
                    chestweltattach=chestweltattach+1
                elif 'side_seam' in operator.operation:
                    sideseam=sideseam+1
            
            operatorpop = {'dart_stitch':dart, 'panel_attach':panel,'dart_and_panel_pressing':dartpanelpressing
            ,'centre_back_stitch':centrebackstitch,'diamond_stitch':diamondstitch
            ,'chest_welt_iron':chestweltiron,'chest_welt_attach':chestweltattach,'side_seam':sideseam}

            operator_list=UserProfileInfo.objects.filter(line_no=5,product_category=product)
            sumachieve=0
            for operator in operator_list:
                ope=strtolistforoperation(operator.operation)
                sk=strtolistforoperation(operator.skill_percentage)
                sumachieve=sumachieve+get_achieved(zip(ope,sk))

            operator_attendences=line5attendence.objects.filter(product=product,date=inpdate)
            return render(request,'operator_skill_matrix_linewise.html',{'operator_list':operator_list
            ,'operator_attendences':operator_attendences,'cdate':cdate,'inpdate':inpdate
            ,'lineno':lineno,'product':product,'operatorpop':operatorpop,'achievedskilllevel':sumachieve})
    if request.method=='POST' and 'skillsubmit' in request.POST:
        operators=UserProfileInfo.objects.all()
        for i,val in enumerate(operators):
            skill=request.POST.getlist(val.operator_id)
            print(skill,i)
    
    cdate=str(date.today())
    operator_list=operator_skill_matrix.objects.all()
    for operator in operator_list:
        if 'dart_stitch' in operator.operation:
            dart=dart+1
        elif 'panel_attach' in operator.operation:
            panel=panel+1
        elif 'dart_and_panel_pressing' in operator.operation:
            dartpanelpressing=dartpanelpressing+1
        elif 'centre_back_stitch' in operator.operation:
            centrebackstitch=centrebackstitch+1
        elif 'diamond_stitch' in operator.operation:
            diamondstitch=diamondstitch+1
        elif 'chest_welt_iron' in operator.operation:
            chestweltiron=chestweltiron+1
        elif 'chest_welt_attach' in operator.operation:
            chestweltattach=chestweltattach+1
        elif 'side_seam' in operator.operation:
            sideseam=sideseam+1
    
    operatorpop = {'dart_stitch':dart, 'panel_attach':panel,'dart_and_panel_pressing':dartpanelpressing
    ,'centre_back_stitch':centrebackstitch,'diamond_stitch':diamondstitch
    ,'chest_welt_iron':chestweltiron,'chest_welt_attach':chestweltattach,'side_seam':sideseam}

    operator_list=UserProfileInfo.objects.all()
     
    sumachieve=0
    for operator in operator_list:
        ope=strtolistforoperation(operator.operation)
        sk=strtolistforoperation(operator.skill_percentage)
        sumachieve=sumachieve+get_achieved(zip(ope,sk))

    return render(request,'operator_skill_matrix.html',{'operator_list':operator_list
    ,'cdate':cdate,'operatorpop':operatorpop,'achievedskilllevel':sumachieve})

def takeattendence(request):
    today = str(date.today())
    if request.method=='POST' and 'linesubmit' in request.POST:
        lineno=request.POST['lineno']
        product=request.POST['product']
        print(lineno)
        operator_list=UserProfileInfo.objects.filter(line_no=lineno,product_category=product)
        print(operator_list)
        leaves=leaveCalender.objects.all()
        return render(request,'takeattendence.html',{'operator_list':operator_list,'line_no':lineno,'today':today,'product':product,'leaves':leaves})
    elif request.method=='POST' and 'attendencesubmit' in request.POST:
        a=submitattendence(request)
        print(a)
        if a==2:
            mess="Attendence submitted"
            return render(request,'takeattendence.html',{'mess':mess,'today':today})
        elif a==1:
            mess="Already submitted"
            return render(request,'takeattendence.html',{'mess':mess,'today':today})
        else:
            mess="Error Occured"
            return render(request,'takeattendence.html',{'mess':mess,'today':today})
    return render(request,'takeattendence.html',{'today':today})

def submitattendence(request):
    a=2
    lineno=request.POST['linenot']
    product=request.POST['productt']
    print(product,lineno)
    operators=UserProfileInfo.objects.filter(line_no=lineno,product_category=product)
    print('hello',lineno)
    if(int(lineno) == 1):
        attenddatescheck=line1attendence.objects.all()
        today = str(date.today())
        c=0
        for check in attenddatescheck:
            if((str(check.date)==today) & (check.product == product)):
                c=1
        if(c==0):
            print('inside')
            for i in operators:
                attend=request.POST[i.operator_id]
                print(i.operator_id,attend)
                pro=UserProfileInfo.objects.filter(operator_id=i.operator_id)
                for j in pro:
                    product=j.product_category

                leaves=leaveCalender.objects.filter(operator_id=i.operator_id)
                print(leaves)
                for k in leaves:
                    if(k.leave_end>=date.today()):
                        attend='absent'

                operatorAttend=line1attendence(operator_id=i.operator_id,operator_name=i.operator_name
                ,product=product,attendence=attend)
                operatorAttend.save()
                print(attend)
            return a
        else:
            a=1
            return a

    elif(int(lineno) == 2):
        print('true')
        attenddatescheck=line2attendence.objects.all()
        today = str(date.today())
        c=0
        for check in attenddatescheck:
            if((str(check.date)==today) & (check.product == product)):
                c=1
        if(c==0):
            print('inside')
            for i in operators:
                attend=request.POST[i.operator_id]
                print(i.operator_id,attend)
                pro=UserProfileInfo.objects.filter(operator_id=i.operator_id)
                for j in pro:
                    product=j.product_category

                leaves=leaveCalender.objects.filter(operator_id=i.operator_id)
                print(leaves)
                for k in leaves:
                    if(k.leave_end>=date.today()):
                        attend='absent'
                             
                operatorAttend=line2attendence(operator_id=i.operator_id,operator_name=i.operator_name
                ,product=product,attendence=attend)
                operatorAttend.save()
            return a
        else:
            a=1
            return a
    elif(int(lineno) == 3):
        print('true')
        attenddatescheck=line3attendence.objects.all()
        today = str(date.today())
        c=0
        for check in attenddatescheck:
            if((str(check.date)==today) & (check.product == product)):
                c=1
        if(c==0):
            print('inside')
            for i in operators:
                attend=request.POST[i.operator_id]
                print(i.operator_id,attend)
                pro=UserProfileInfo.objects.filter(operator_id=i.operator_id)
                for j in pro:
                    product=j.product_category

                leaves=leaveCalender.objects.filter(operator_id=i.operator_id)
                print(leaves)
                for k in leaves:
                    if(k.leave_end>=date.today()):
                        attend='absent'
                             
                operatorAttend=line3attendence(operator_id=i.operator_id,operator_name=i.operator_name
                ,product=product,attendence=attend)
                operatorAttend.save()
                print(attend)
            return a
        else:
            a=1
            return a
    elif(int(lineno) == 4):
        print('true')
        attenddatescheck=line4attendence.objects.all()
        today = str(date.today())
        c=0
        for check in attenddatescheck:
            if((str(check.date)==today) & (check.product == product)):
                c=1
        if(c==0):
            print('inside')
            for i in operators:
                attend=request.POST[i.operator_id]
                print(i.operator_id,attend)
                pro=UserProfileInfo.objects.filter(operator_id=i.operator_id)
                for j in pro:
                    product=j.product_category

                leaves=leaveCalender.objects.filter(operator_id=i.operator_id)
                print(leaves)
                for k in leaves:
                    if(k.leave_end>=date.today()):
                        attend='absent'
                             
                operatorAttend=line4attendence(operator_id=i.operator_id,operator_name=i.operator_name
                ,product=product,attendence=attend)
                operatorAttend.save()
                print(attend)
            return a
        else:
            a=1
            return a
    elif(int(lineno) == 5):
        print('true')
        attenddatescheck=line5attendence.objects.all()
        today = str(date.today())
        c=0
        for check in attenddatescheck:
            if((str(check.date)==today) & (check.product == product)):
                c=1
        if(c==0):
            print('inside')
            for i in operators:
                attend=request.POST[i.operator_id]
                print(i.operator_id,attend)
                pro=UserProfileInfo.objects.filter(operator_id=i.operator_id)
                for j in pro:
                    product=j.product_category

                leaves=leaveCalender.objects.filter(operator_id=i.operator_id)
                print(leaves)
                for k in leaves:
                    if(k.leave_end>=date.today()):
                        attend='absent'
                             
                operatorAttend=line5attendence(operator_id=i.operator_id,operator_name=i.operator_name
                ,product=product,attendence=attend)
                operatorAttend.save()
                print(attend)
            return a
        else:
            a=1
            return a
def takeleave(request):
    if request.method=='POST':
        oid=request.POST['operatorid']
        leavestart=request.POST['leavestart']
        leaveend=request.POST['leaveend']
        check=UserProfileInfo.objects.filter(operator_id=oid)
        leaveobjects=leaveCalender.objects.filter(operator_id=oid)
        key=0
        for i in check:
            key=1
        if(key==1):
            print("Hello")
            for leaves in leaveobjects:
                print(date.today(),leaves.leave_end)
                if(date.today()<=leaves.leave_end):
                    mess="Already on Leave"
                    return render(request,'takeleave.html',{'mess':mess})
            
            leavestart = datetime.datetime.strptime(leavestart, '%Y-%m-%d')
            leaveend = datetime.datetime.strptime(leaveend, '%Y-%m-%d')
            delta = (leaveend - leavestart)
            noofdays=(delta.days+1)
            leaveob=leaveCalender(operator_id=oid,leave_start=leavestart,leave_end=leaveend,days=noofdays)
            leaveob.save()
            mess="Submited"
            return render(request,'takeleave.html',{'mess':mess})
        else:
            mess="Enter valid Operator ID"
            return render(request,'takeleave.html',{'mess':mess})
    return render(request,'takeleave.html')

def leavereport(request):
    op1=leaveCalender.objects.all()
    return render(request,'leavereport.html',{'op1':op1})

def attendreporthome(request):
    return render(request,'attendreporthome.html')

def attendencereport(request):
    if request.method == 'POST':
        lineno=request.POST['lineno']
        product=request.POST['product_category']
        if int(lineno)==1:
            reports=line1attendence.objects.filter(product=product)
            return render(request,'attendencereport.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==2:
            reports=line2attendence.objects.filter(product=product)
            return render(request,'attendencereport.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==3:
            reports=line3attendence.objects.filter(product=product)
            return render(request,'attendencereport.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==4:
            reports=line4attendence.objects.filter(product=product)
            return render(request,'attendencereport.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==5:
            reports=line5attendence.objects.filter(product=product)
            return render(request,'attendencereport.html',{'reports':reports,'lineno':lineno,'product':product})
    return render(request,'attendencereport.html')

def attendreportdatewise(request):
    if request.method=='POST':
        lineno=request.POST['lineno']   
        product=request.POST['product_category']
        date=request.POST['date']   
        if int(lineno)==1:
            reports=line1attendence.objects.filter(product=product,date=date)
            return render(request,'attendreportdatewise.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==2:
            reports=line2attendence.objects.filter(product=product,date=date)
            return render(request,'attendreportdatewise.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==3:
            reports=line3attendence.objects.filter(product=product,date=date)
            return render(request,'attendreportdatewise.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==4:
            reports=line4attendence.objects.filter(product=product,date=date)
            return render(request,'attendreportdatewise.html',{'reports':reports,'lineno':lineno,'product':product})
        if int(lineno)==5:
            reports=line5attendence.objects.filter(product=product,date=date)
            return render(request,'attendreportdatewise.html',{'reports':reports,'lineno':lineno,'product':product})
    return render(request,'attendreportdatewise.html')

def dprreporthome(request):
    
    return render(request,'dprreporthome.html')

def dprreport(request):
    return render(request,'dprreport.html')

def listToString(s): 
    str1 = ","
    return (str1.join(s))

def strtolist(s):
    return list(s.split("-"))

def convert(stt):
    x=int(stt)
    print(x)
    return x

def strtolistfortime(s):
    return list(s.split(":"))

def strtolistforoperation(s):
    return list(s.split(","))

def dateFormat(s):
    li = list(s.split("-")) 
    li.reverse()
    str2="/"
    return (str2.join(li)) 

def get_achieved(oplist):
    achieve=0
    for a,b in oplist:
        if a == 'dart_stitch':
            achieve=achieve+((int(b)*4)/100)
        elif a=='panel_attach':
            achieve=achieve+((int(b)*3)/100)
        elif a=='dart_and_panel_pressing':
            achieve=achieve+((int(b)*5)/100)
        elif a=='centre_back_stitch':
            achieve=achieve+((int(b)*2)/100)
        elif a=='diamond_stitch':
            achieve=achieve+((int(b)*3)/100)
        elif a=='chest_welt_iron':
            achieve=achieve+((int(b)*1)/100)
        elif a=='chest_welt_attach':
            achieve=achieve+((int(b)*4)/100)
        elif a=='side_seam':
            achieve=achieve+((int(b)*3)/100)
    return achieve
    
def operationbulletin(request):
    if request.method=='POST' :
        lineno=request.POST['lineno']   
        product=request.POST['product']
        inpdate=request.POST['date']
        mode=request.POST['mode']
        if mode=='auto':    
            if(int(lineno)==1):
                operator_attendences=line1attendence.objects.filter(product=product,attendence='present',date=inpdate)
                
                operator_list_dart=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='dart_stitch')
                first=0
                second=0
                for operators in operator_list_dart:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_dart1=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='dart_stitch',skill_percentage=first)
                operator_list_dart2=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='dart_stitch',skill_percentage=second)
                dart_list = list(chain(operator_list_dart1, operator_list_dart2))
                print(dart_list)

                operator_list_panel=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='panel_attach')
                first=0
                second=0
                for operators in operator_list_panel:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_panel1=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='panel_attach',skill_percentage=first)
                operator_list_panel2=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='panel_attach',skill_percentage=second)
                panel_list = list(chain(operator_list_panel1, operator_list_panel2))
                print(panel_list)

                operator_list_sideseam=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='side_seam')
                first=0
                second=0
                for operators in operator_list_sideseam:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_sideseam1=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='side_seam',skill_percentage=first)
                operator_list_sideseam2=operator_skill_matrix.objects.filter(line_no=1,product_category=product
                    ,operation='side_seam',skill_percentage=second)
                sideseam_list = list(chain(operator_list_sideseam1, operator_list_sideseam2))
                print(sideseam_list)

                return render(request,'operationbulletin.html',{'operator_attendences':operator_attendences,'lineno':lineno,'inpdate':inpdate
                ,'product':product,'dart_list':dart_list,'panel_list':panel_list,'sideseam_list':sideseam_list,'mode':mode})
            elif(int(lineno)==2):
                operator_attendences=line2attendence.objects.filter(product=product,attendence='present',date=inpdate)
                
                operator_list_dart=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='dart_stitch')
                first=0
                second=0
                for operators in operator_list_dart:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_dart1=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='dart_stitch',skill_percentage=first)
                operator_list_dart2=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='dart_stitch',skill_percentage=second)
                dart_list = list(chain(operator_list_dart1, operator_list_dart2))
                print(dart_list)

                operator_list_panel=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='panel_attach')
                first=0
                second=0
                for operators in operator_list_panel:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_panel1=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='panel_attach',skill_percentage=first)
                operator_list_panel2=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='panel_attach',skill_percentage=second)
                panel_list = list(chain(operator_list_panel1, operator_list_panel2))
                print(panel_list)

                operator_list_sideseam=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='side_seam')
                first=0
                second=0
                for operators in operator_list_sideseam:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_sideseam1=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='side_seam',skill_percentage=first)
                operator_list_sideseam2=operator_skill_matrix.objects.filter(line_no=2,product_category=product
                    ,operation='side_seam',skill_percentage=second)
                sideseam_list = list(chain(operator_list_sideseam1, operator_list_sideseam2))
                print(sideseam_list)

                return render(request,'operationbulletin.html',{'operator_attendences':operator_attendences,'lineno':lineno,'inpdate':inpdate
                ,'product':product,'dart_list':dart_list,'panel_list':panel_list,'sideseam_list':sideseam_list,'mode':mode})
            elif(int(lineno)==3):
                operator_attendences=line3attendence.objects.filter(product=product,attendence='present',date=inpdate)
                
                operator_list_dart=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='dart_stitch')
                first=0
                second=0
                for operators in operator_list_dart:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_dart1=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='dart_stitch',skill_percentage=first)
                operator_list_dart2=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='dart_stitch',skill_percentage=second)
                dart_list = list(chain(operator_list_dart1, operator_list_dart2))
                print(dart_list)

                operator_list_panel=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='panel_attach')
                first=0
                second=0
                for operators in operator_list_panel:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_panel1=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='panel_attach',skill_percentage=first)
                operator_list_panel2=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='panel_attach',skill_percentage=second)
                panel_list = list(chain(operator_list_panel1, operator_list_panel2))
                print(panel_list)

                operator_list_sideseam=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='side_seam')
                first=0
                second=0
                for operators in operator_list_sideseam:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_sideseam1=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='side_seam',skill_percentage=first)
                operator_list_sideseam2=operator_skill_matrix.objects.filter(line_no=3,product_category=product
                    ,operation='side_seam',skill_percentage=second)
                sideseam_list = list(chain(operator_list_sideseam1, operator_list_sideseam2))
                print(sideseam_list)

                return render(request,'operationbulletin.html',{'operator_attendences':operator_attendences,'lineno':lineno,'inpdate':inpdate
                ,'product':product,'dart_list':dart_list,'panel_list':panel_list,'sideseam_list':sideseam_list,'mode':mode})
            elif(int(lineno)==4):
                operator_attendences=line4attendence.objects.filter(product=product,attendence='present',date=inpdate)
                
                operator_list_dart=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='dart_stitch')
                first=0
                second=0
                for operators in operator_list_dart:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_dart1=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='dart_stitch',skill_percentage=first)
                operator_list_dart2=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='dart_stitch',skill_percentage=second)
                dart_list = list(chain(operator_list_dart1, operator_list_dart2))
                print(dart_list)

                operator_list_panel=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='panel_attach')
                first=0
                second=0
                for operators in operator_list_panel:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_panel1=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='panel_attach',skill_percentage=first)
                operator_list_panel2=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='panel_attach',skill_percentage=second)
                panel_list = list(chain(operator_list_panel1, operator_list_panel2))
                print(panel_list)

                operator_list_sideseam=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='side_seam')
                first=0
                second=0
                for operators in operator_list_sideseam:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_sideseam1=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='side_seam',skill_percentage=first)
                operator_list_sideseam2=operator_skill_matrix.objects.filter(line_no=4,product_category=product
                    ,operation='side_seam',skill_percentage=second)
                sideseam_list = list(chain(operator_list_sideseam1, operator_list_sideseam2))
                print(sideseam_list)

                return render(request,'operationbulletin.html',{'operator_attendences':operator_attendences,'lineno':lineno,'inpdate':inpdate
                ,'product':product,'dart_list':dart_list,'panel_list':panel_list,'sideseam_list':sideseam_list,'mode':mode})
            elif(int(lineno)==5):
                operator_attendences=line5attendence.objects.filter(product=product,attendence='present',date=inpdate)
                
                operator_list_dart=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='dart_stitch')
                first=0
                second=0
                for operators in operator_list_dart:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_dart1=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='dart_stitch',skill_percentage=first)
                operator_list_dart2=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='dart_stitch',skill_percentage=second)
                dart_list = list(chain(operator_list_dart1, operator_list_dart2))
                print(dart_list)

                operator_list_panel=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='panel_attach')
                first=0
                second=0
                for operators in operator_list_panel:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_panel1=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='panel_attach',skill_percentage=first)
                operator_list_panel2=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='panel_attach',skill_percentage=second)
                panel_list = list(chain(operator_list_panel1, operator_list_panel2))
                print(panel_list)

                operator_list_sideseam=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='side_seam')
                first=0
                second=0
                for operators in operator_list_sideseam:
                    for opattend in operator_attendences:
                        if operators.operator_id==opattend.operator_id:
                            if second<=int(operators.skill_percentage):
                                second=int(operators.skill_percentage)
                                if first<second:
                                    first,second=second,first
                                    print(first,second)
                operator_list_sideseam1=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='side_seam',skill_percentage=first)
                operator_list_sideseam2=operator_skill_matrix.objects.filter(line_no=5,product_category=product
                    ,operation='side_seam',skill_percentage=second)
                sideseam_list = list(chain(operator_list_sideseam1, operator_list_sideseam2))
                print(sideseam_list)

                return render(request,'operationbulletin.html',{'operator_attendences':operator_attendences,'lineno':lineno,'inpdate':inpdate
                ,'product':product,'dart_list':dart_list,'panel_list':panel_list,'sideseam_list':sideseam_list,'mode':mode})
    return render(request,'operationbulletin.html')    
