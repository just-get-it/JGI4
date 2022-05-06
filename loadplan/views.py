from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http.request import QueryDict
from loadplan.models import Ord,Avc,Cpr,Mat,Lio
from .forms import CprForm
# Create your views here.

def loadplan(request):
    return render(request,'hello.html')

def orderdetails(request):
    if request.method == 'POST':
        orderno=request.POST['orderno']
        styleno=request.POST['styleno']
        orderqty=request.POST['orderqty']
        ordercd=request.POST['ordercd']
        plancd = request.POST['plancd']
        ocd=request.POST['ocd']
        ltf=request.POST['ltf']
        ltb=request.POST['ltb']
        s=Ord(orderno=orderno, styleno=styleno, orderqty=orderqty, ordercd=ordercd, plancd=plancd, ocd=ocd, ltf=ltf, ltb=ltb)
        s.save()
        return render(request,'orderdetails.html')
    return render(request, 'orderdetails.html')

def availablecapacity(request):
    if request.method == 'POST':
        lineno=request.POST['lineno']
        noo=request.POST['noo']
        workdays=request.POST['workdays']
        dwh=request.POST['dwh']
        absent = request.POST['absent']
        efficiency=request.POST['efficiency']
        mac=request.POST['mac']
        s1=Avc(lineno=lineno, noo=noo, workdays=workdays, dwh=dwh, absent=absent, efficiency=efficiency, mac=mac)
        s1.save()
        return render(request,'availablecapacity.html')
    return render(request, 'availablecapacity.html')

def capreqd(request):
    if request.method == 'POST':
        orderno=request.POST['orderno']
        ltlc=request.POST['ltlc']
        orderqty=request.POST['orderqty']
        smv=request.POST['smv']
        crm = request.POST['crm']
        capd=request.POST['capd']
        crd=request.POST['crd']
        s2=Cpr(orderno=orderno, ltlc=ltlc, orderqty=orderqty, smv=smv, crm=crm, capd=capd, crd=crd)
        s2.save()
        return render(request,'capreqd.html')
    macfill = Avc.objects.all()
    allorder = Ord.objects.all()
    return render(request,'capreqd.html',{'macfill': macfill, 'allorder': allorder})

def ordtable(request):
    allorder = Ord.objects.all()
    return render(request,'ordtable.html', {'allorder': allorder})

def avctable(request):
    allavc = Avc.objects.all()
    return render(request,'avctable.html', {'allavc': allavc})

def cprtable(request):
    allcpr = Cpr.objects.all()
    return render(request,'cprtable.html', {'allcpr': allcpr})

def material(request):
    if request.method == 'POST':
        orderno=request.POST['orderno']
        fin=request.POST['fin']
        threads=request.POST['threads']
        sewtrim=request.POST['sewtrim']
        fintrim = request.POST['fintrim']
        packtrim=request.POST['packtrim']
        s4=Mat(orderno=orderno, fin=fin, threads=threads, sewtrim=sewtrim, fintrim=fintrim, packtrim=packtrim)
        s4.save()
        return render(request,'material.html')

    allorder = Ord.objects.all()
    return render(request,'material.html', {'allorder': allorder})

def mattable(request):
    allmat = Mat.objects.all()
    return render(request,'mattable.html', {'allmat': allmat})

def loadsugg(request):
    allorder = Ord.objects.all()
    allcpr = Cpr.objects.all()
    allmat = Mat.objects.all()
    allavc = Avc.objects.all()
    rc = Ord.objects.all().count()
    print(rc)
    return render(request,'loadsugg.html',{'allorder': allorder, 'allcpr': allcpr,'allmat':allmat,'allavc':allavc,'rc':rc})

def exp(request):
    if request.method == 'GET':
        #print(request.GET)
        #print("hello")
        on=request.GET.get('orderno')
        
        if(on):
            allorder=Ord.objects.filter(orderno=on)
            allcpr = Cpr.objects.filter(orderno=on)
            allmat = Mat.objects.filter(orderno=on)
            allavc = Avc.objects.all()
            allcap = Cpr.objects.all().order_by('crm')
            allmac = Avc.objects.all().order_by('mac')
            #print(allorder['styleno'])
            #for a in allorder:
             #   print(a['styleno'])
           #queryset = UnitTestCollection.objects.filter(unit__type=unit_type).values_list('<insert field>', flat=True)
            #print(allorder)
            #print(my_values)
            return render(request,'exptable.html',{'allorder':allorder,'allcpr': allcpr,'allmat':allmat,'allavc':allavc, 'allcap':allcap, 'allmac':allmac})
            #return redirect(exptable, orderno=on, button=bu)
        else:
            allorder = Ord.objects.all().order_by('ocd')
            return render(request,'exp.html',{'allorder': allorder})
    
    
        #print(on)
        #QueryDict.__init__(query_string=None, mutable=False, encoding=None)
        #print(QueryDict.__getitem__('orderno'))
        #data = QueryDict(request.GET)
        #print(data)
    #allorder = Ord.objects.all()
    #return render(request,'exp.html',{'allorder': allorder})


def lg(request):
    if request.method == 'POST':
        orderno=request.POST['orderno']
        ltlc=request.POST['ltlc']
        s5=Lio(orderno=orderno, ltlc=ltlc)
        s5.save()
        return render(request,'lg.html')

    macfill = Cpr.objects.all()
    allorder = Ord.objects.all()
    return render(request,'lg.html',{'macfill': macfill, 'allorder':allorder})

def exptable(request):
    if request.method == 'POST':
        return render(request,'exp.html')

def linetable(request):
    allcpr=Lio.objects.all()
    return render(request, 'linetable.html', {'allcpr':allcpr})