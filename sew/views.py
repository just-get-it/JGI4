from django.shortcuts import render
from django.http import JsonResponse
from .forms import pfm, operations#,orders
import json
from .models import GeneratePFM,AddOperations, GenerateOB, GOperationBul
from django.forms import formset_factory,modelformset_factory
from product.models import category, sub_category, super_category, PFM_Components, PFM_Attributes, labels_Attributes
from product.models import FabricDetails, StyleDetails, MachineType, Department, Section, subsection, StyleType, WashType, Fabric
from b2b.models import company_Order

from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

cate=0

def sew(request):
    return render(request,'sewindex.html')

def generatepfm(request):


    if request.POST.get('pfmm'):
        pf = request.POST.get('pfmm')
        te= GeneratePFM.objects.filter(pfmno=pf).values_list('pfmno',flat=True)
        idd=[]
        for j in te:
            idd.append(j)

        return JsonResponse({'ids': idd})
    if request.POST.get('cat'):
        d = request.POST.get('cat')
        e = request.POST.get('subc')
        f = request.POST.get('superc')
        Gpm=GeneratePFM.objects.all()
        print("--")
        print(e)
        for x in Gpm:
            y=GeneratePFM.objects.filter(category=x.category,sub_category=x.sub_category,super_category=x.super_category).all()
        for i in y:
            te=GeneratePFM.objects.filter(category=d,sub_category=e,super_category=f).values_list('pfmno',flat=True)
        g=[]
        idd=[]
        c=0
        for j in te:
            idd.append(j)
        print("__0")
        print(idd)

        return JsonResponse({'ids': idd})


    if request.POST.get('scate'):
        d = request.POST.get('scate')
        e = request.POST.get('catee')
        Gpm=GeneratePFM.objects.all()
        print("--")
        print(e)
        for x in Gpm:
            y=GeneratePFM.objects.filter(category=x.category,sub_category=x.sub_category).all()
        for i in y:
            te=GeneratePFM.objects.filter(category=d,sub_category=e).values_list('pfmno',flat=True)
        g=[]
        idd=[];
        c=0
        for j in te:
            idd.append(j)

        return JsonResponse({'ids': idd})

    if request.POST.get('cate'):
        d = request.POST.get('cate')

        Gpm=GeneratePFM.objects.all()
        for x in Gpm:
            y=GeneratePFM.objects.filter(category=x.category).all()
        for i in y:
            te=GeneratePFM.objects.filter(category=d).values_list('pfmno',flat=True)
        g=[]
        idd=[];
        c=0
        for j in te:
            idd.append(j)

        return JsonResponse({'ids': idd})

    if request.POST.get('fab'):
        d = request.POST.get('fab')

        Gpm=GeneratePFM.objects.all()
        for x in Gpm:
            y=GeneratePFM.objects.filter(fabric=x.fabric).all()
        for i in y:
            te=GeneratePFM.objects.filter(fabric=d).values_list('pfmno',flat=True)
        g=[]
        idd=[];
        c=0
        for j in te:
            idd.append(j)

        return JsonResponse({'ids': idd})

    if request.POST.get('wash'):
        d = request.POST.get('wash')

        Gpm=GeneratePFM.objects.all()
        for x in Gpm:
            y=GeneratePFM.objects.filter(wash=x.wash).all()
        for i in y:
            te=GeneratePFM.objects.filter(wash=d).values_list('pfmno',flat=True)
        g=[]
        idd=[];
        c=0
        for j in te:
            idd.append(j)

        return JsonResponse({'ids': idd})

    if request.POST.get('style'):
        d = request.POST.get('style')

        Gpm=GeneratePFM.objects.all()
        for x in Gpm:
            y=GeneratePFM.objects.filter(style_type=x.style_type).all()
        for i in y:
            te=GeneratePFM.objects.filter(style_type=d).values_list('pfmno',flat=True)
        g=[]
        idd=[];
        c=0
        for j in te:
            idd.append(j)

        return JsonResponse({'ids': idd})


    if request.POST.get('prodcategory'):
        global cate

        prodcategory = request.POST.get('prodcategory')
        cate=prodcategory
        print(cate)

        sub = sub_category.objects.filter(product_Category=cate).order_by("name")
        print(sub)
        print(len(sub))
        sub = [s.name for s in sub]

        return JsonResponse({"sub": sub})


    elif request.POST.get('prodsubcategory'):

        prodsubcategory = request.POST.get('prodsubcategory')
        print(cate)
        print(prodsubcategory)
        x = sub_category.objects.filter(product_Category=cate, name=prodsubcategory).values_list('id', flat=True)
        print(x[0])

        superc = super_category.objects.filter(product_Subcategory=x[0], product_Category=cate)
        print(len(superc))
        superc = [s.name for s in superc]
        print(superc)
        return JsonResponse({"superc": superc})



    form = pfm(request.POST or None)
    if form.is_valid():
        print('abc')

    if request.POST.get('pfmno'):
        pfmn=request.POST.get('pfmno')
        ob=GeneratePFM.objects.filter(pfmno=pfmn).values_list('super_category',flat=True)
        oa=ob[0]
        print(ob[0])
        q=0
        sup_id=super_category.objects.filter(name=ob[0]).values_list('id',flat=True)
        sub_id=super_category.objects.filter(name=ob[0]).values_list('product_Category_id',flat=True)
        cat_id=super_category.objects.filter(name=ob[0]).values_list('product_Subcategory_id',flat=True)
        print(sub_id)
        count=[]
        ar=[]
        zx=[]
        least=[]
        n=[]
        lab=labels_Attributes.objects.filter(product_Supercategory_id=sup_id[0],product_Category_id=sub_id[0],
            product_Subcategory_id=cat_id[0]).values_list('name',flat=True)
        for i in lab:
            #print(i)
            pf_com=PFM_Components.objects.filter(name=i).values_list('id',flat=True)
            ar.append(pf_com)

        print(ar)
        for i in ar:
            if i.exists():
                print(i[0])
                n.append(PFM_Components.objects.filter(id=i[0]).values_list('name',flat=True))
                zx.append(PFM_Attributes.objects.filter(pfm_component_id=i[0]).order_by('name'))
            else:
                print("Emoty")

        print(zx)
        for i in n:
            count.append(str(i[0]))


        for i in zx:
            #print(i)
            for z in i:
                print(z)
                least.append(str(z))
            least.append("o")

        print(least)
        print(count)
        print("got")
        print(ar)


        return JsonResponse({'component':count, 'type':least  })

    if request.GET:
        pfmno = request.GET.get('pf')
        fab = request.GET.get('fabric')
        was = request.GET.get('wash')
        cate = request.GET.get('category')
        scate = request.GET.get('sub_category')
        pcate = request.GET.get('super_category')
        st = request.GET.get('style_type')
        print("why")
        fd = GeneratePFM(pfmno=pfmno, fabric=fab, wash=was, category=cate, sub_category=scate, super_category=pcate, style_type=st)
        fd.save()

    fabricdetailsobjects = GeneratePFM.objects.all()
    prodcategoryobjects = category.objects.all()


    generate=GeneratePFM.objects.all()
    print(generate)
    pfmnod=""
    if not generate:
        pfmnochar='CT-'+str(00)
        print(pfmnochar)
    else:
        for i in generate:
            pfmnod=i.pfmno
            print(pfmnod)
        pfmno=int(pfmnod[3:])
        pfmno=pfmno+1
        pfmnochar='CT-'+str(pfmno)
        print(pfmnochar)

    washtype=WashType.objects.all()
    fabric=Fabric.objects.all()
    styletype=StyleType.objects.all()


    context = {
        "responseform" : form,
        "fabricdetailsobjects" : fabricdetailsobjects,
        "prodcategoryobjects" : prodcategoryobjects,
        "pfmno":pfmnochar,
        "washtype":washtype,
        "fabric":fabric,
        "styletype":styletype,

    }

    return render(request, 'generatepfm.html', context)


def operat(request):
    # if request.POST.get('component'):

    #   comp = request.POST.get('component')
    #   print(comp)
    #   sub = PFM_Attributes.objects.filter(pfm_component=comp).order_by("name")
    #   sub = [s.name for s in sub]
    #   return JsonResponse({"sub": sub})

    if request.POST.get('dep'):
        d = request.POST.get('dep')
        print("___")
        aoo = AddOperations.objects.all()
        for x in aoo:
            y = AddOperations.objects.filter(department=x.department).all()
        for i in y:
            te = AddOperations.objects.filter(department=d).values_list('id', flat=True)
        g = []
        idd = [];
        c = 0
        for j in te:
            idd.append(j)
        print(idd)
        return JsonResponse({'ids': idd})

    if request.POST.get('sec'):
        d = request.POST.get('depa')
        s = request.POST.get('sec')
        print("1--1")
        aoo = AddOperations.objects.all()
        for x in aoo:
            y = AddOperations.objects.filter(department=x.department, section=x.section).all()
        for i in y:
            te = AddOperations.objects.filter(department=d, section=s).values_list('id', flat=True)
        g = []
        idd = [];
        c = 0
        for j in te:
            idd.append(j)
        print(idd)
        return JsonResponse({'ids': idd})

    if request.POST.get('de'):
        d = request.POST.get('de')
        s = request.POST.get('seca')
        ss = request.POST.get('subse')
        print("1--2")
        aoo = AddOperations.objects.all()
        for x in aoo:
            y = AddOperations.objects.filter(department=x.department, section=x.section,
                                             sub_section=x.sub_section).all()
        for i in y:
            te = AddOperations.objects.filter(department=d, section=s, sub_section=ss).values_list('id', flat=True)
        g = []
        idd = [];
        c = 0
        for j in te:
            idd.append(j)
        print(idd)
        return JsonResponse({'ids': idd})

    if request.POST.get('o'):
        o = request.POST.get('o')
        c = request.POST.get('c')
        g = request.POST.get('g')
        p = request.POST.get('p')
        # ,complexity=c,grade=g,pfmno=p
        print("1--3")
        print(p)
        print(g)
        aoo = AddOperations.objects.all()

        if o and c and g and p:
            print("ocg")
            te = AddOperations.objects.filter(operations=o, complexity=c, grade=g, pfmno=p).values_list('id', flat=True)

        elif o:
            te = AddOperations.objects.filter(operations=o).values_list('id', flat=True)
        elif g:
            te = AddOperations.objects.filter(grade=g).values_list('id', flat=True)
        elif p:
            te = AddOperations.objects.filter(pfmno=p).values_list('id', flat=True)

        g = []
        idd = [];
        c = 0
        for j in te:
            idd.append(j)
        print(idd)
        return JsonResponse({'ids': idd})

    elif request.POST.get('g'):
        print("GG")
        c = request.POST.get('g')
        te = AddOperations.objects.filter(grade=c).values_list('id', flat=True)
        idd = [];
        c = 0
        for j in te:
            idd.append(j)
        print(idd)
        return JsonResponse({'ids': idd})

    elif request.POST.get('p'):
        print("P")
        c = request.POST.get('p')
        te = AddOperations.objects.filter(pfmno=p).values_list('id', flat=True)
        idd = [];
        c = 0
        for j in te:
            idd.append(j)
        print(idd)
        return JsonResponse({'ids': idd})

    elif request.POST.get('c'):
        print("CCC")
        c = request.POST.get('c')
        te = AddOperations.objects.filter(complexity=c).values_list('id', flat=True)
        idd = [];
        c = 0
        for j in te:
            idd.append(j)
        print(idd)
        return JsonResponse({'ids': idd})

    if request.POST.get('department'):
        global dept
        dept = request.POST.get('department')

        section_res = Section.objects.filter(department=dept).order_by("name")
        section_res = [s.name for s in section_res]
        return JsonResponse({'section_res': section_res})

    elif request.POST.get('section'):

        comp = request.POST.get('section')
        print(dept)
        print(comp)
        x = Section.objects.filter(department=dept, name=comp).values_list('id', flat=True)
        print(x[0])

        sub_section_res = subsection.objects.filter(section=x[0], department=dept)
        sub_section_res = [s.name for s in sub_section_res]
        print(sub_section_res)
        return JsonResponse({"sub_section_res": sub_section_res})

    form = operations(request.POST or None)
    if form.is_valid():
        print('abc')

    if request.GET:
        pn = request.GET.get("pfmno")
        c = request.GET.get("comp")
        a = request.GET.get("attribute")
        dep = request.GET.get("department")
        sec = request.GET.get("section")
        subsec = request.GET.get("subsection")
        o = request.GET.get("operations")
        # com = request.GET.get("complexity")
        spi = request.GET.get("spi")
        sl = request.GET.get("stitch_length")
        ma = request.GET.get("machine_auto")
        tc = request.GET.get("thread_consumption")
        wa = request.GET.get("work_aid")
        spif = request.GET.get("spifactor")
        shade = request.GET.get("shade")
        tspec = request.GET.get("tspec")
        tt = request.GET.get("turntime")
        mt = request.GET.get("maintime")
        pt = request.GET.get("picktime")
        dt = request.GET.get("distime")
        psmv = request.GET.get("psmv")
        oc = request.GET.get("oc")
        spic = request.GET.get("spic")
        stitchc = request.GET.get("stitchc")
        send = request.GET.getlist("send[]")
        fp = send[2]
        dp = send[3]
        pp = send[1]
        psam = send[4]
        g = send[5]
        ty = send[6]
        pct = send[7]
        act = send[8]
        mpall = send[9]
        name = send[10]
        asmv = send[0]
        oph = send[11]
        # asmv = request.GET.get("asmv")
        # pp = request.GET.get("personal")
        # fp = request.GET.get("fatigue")
        # dp = request.GET.get("delay")
        # psam = request.GET.get("psam")
        # ty = request.GET.get("t")
        # pct = request.GET.get("pct")
        # act = request.GET.get("act")
        # mpall = request.GET.get("mpall")
        # name = request.GET.get("name")
        # oph = request.GET.get("oph")
        # g = request.GET.get("grade")

        print("__")
        print(send)

        # smv = request.GET.get("smv")
        # al = request.GET.get("allowance")
        # sam = request.GET.get("sam")
        # ct = request.GET.get("ct")
        print("SAveee")
        sd = AddOperations(pfmno=pn, component=c, component_type=a, department=dep, section=sec
                           , sub_section=subsec, operations=o, spi=spi, stitch_length=sl, thread_consumption=tc
                           , machine_auto=ma, work_aid=wa, spi_factor=spif, shade=shade, grade=g,
                           asmv=asmv, psmv=psmv, thread_spec=tspec, pick_time=pt, main_time=mt, turn_time=tt,
                           dispose_time=dt,
                           operation_complexity=oc, spi_complexity=spic, stitch_complexity=stitchc, personal=pp,
                           fatique=fp, delay=dp, psam=psam, typee=ty, pct=pct, mpall=mpall, name=name, oph=oph, act=act)
        sd.save()

    pfmnos = GeneratePFM.objects.all()
    styledetailsobjects = AddOperations.objects.all()
    pfmcomponents = PFM_Components.objects.all()
    machine_type = MachineType.objects.all()
    department = Department.objects.all()
    section = Section.objects.all()
    sub_section = subsection.objects.all()
    context = {
        "operations": form,
        "pfmnos": pfmnos,
        "styledetailsobjects": styledetailsobjects,
        "pfmcomponents": pfmcomponents,
        "machine_type": machine_type,
        "department": department,
        "section": section,
        "sub_section": sub_section,
    }

    return render(request, 'operations.html', context)


def is_valid_queryparam(param):
    return param != '' and param is not None


def orderform(request):
    context = {}
    global obgenformset
    global count
    count = 0
    allopp= []
    global fd
    global qs
    qs=FabricDetails.objects.all()
    if request.method == 'POST' and count == 0:
        form1 = orders(request.POST)
        if form1.is_valid:
            form1.save(commit=True)
            odno = form1.cleaned_data['orderno']
            stno = form1.cleaned_data['styleno']
            lno = form1.cleaned_data['lineno']
            odqno = form1.cleaned_data['order_quantity']
            cpc=form1.cleaned_data['capacity']
            tgt = form1.cleaned_data['target']
            minps = form1.cleaned_data['mins_shift']
            expskill = form1.cleaned_data['expected_skill_level']
            fb=form1.cleaned_data['fabric']
            wsh=form1.cleaned_data['wash']
            ctg=form1.cleaned_data['category']
            subctg=form1.cleaned_data['subcategory']
            stype=form1.cleaned_data['styletype']
            cp=form1.cleaned_data['comp']
            atr=form1.cleaned_data['attribute']

            if is_valid_queryparam(fb):
                qs= qs.filter(fabric=fb)

            if is_valid_queryparam(wsh):
                qs = qs.filter(wash=wsh)

            if is_valid_queryparam(ctg):
                qs= qs.filter(category=ctg)

            if is_valid_queryparam(subctg):
                qs = qs.filter(subcategory=subctg)

            if is_valid_queryparam(stype):
                qs = qs.filter(styletype=stype)
            print(qs)

            for q in qs:
                print(q.pfmno)
                fd = StyleDetails.objects.filter(pfmno=q)
                if is_valid_queryparam(cp):
                    fd = fd.filter(comp=cp)

                if is_valid_queryparam(atr):
                    fd = fd.filter(attribute=atr)

                allopp.append(fd)
            print(allopp)
            sz=0
            for opp in allopp:
                sz=sz+1
            print(sz)
            obgenformset = modelformset_factory(Obgenerate, fields='__all__', extra=sz)
            context['allopp'] =allopp
            context['orderno']=odno
            context['styleno'] =stno
            context['target']=tgt
            context['expskill']=expskill
            context['minps']=minps
            formset = obgenformset()
            context['formset'] = formset
            count=count+1
            return render(request,'orderformgen.html',context)

    if request.method == "POST":
        formset = obgenformset(request.post or None)
        for form in formset.form:
            form.save()


    form1 = orders()
    context['form1'] = form1
    return render(request, "orderformgen.html", context)

from b2b.models import company_Order
from product.models import category, sub_category, super_category, Fabric, StyleType, WashType
from .models import GeneratePFM


def obgenerateform3(request):
    if request.POST.get('department'):
        global dept
        dept = request.POST.get('department')

        section_res = Section.objects.filter(department=dept).order_by("name")
        section_res = [s.name for s in section_res]
        return JsonResponse({'section_res': section_res})

    if request.POST.get('orderno'):
        a = request.POST.get('orderno')
        print(a)



        y = company_Order.objects.filter(order_no=a).values_list('product_Category', flat=True)
        y1 = company_Order.objects.filter(order_no=a).values_list('product_Subcategory', flat=True)
        y2 = company_Order.objects.filter(order_no=a).values_list('product_Supercategory', flat=True)
        y3 = company_Order.objects.filter(order_no=a).values_list('fabric_type', flat=True)
        y4 = company_Order.objects.filter(order_no=a).values_list('wash_type', flat=True)
        y5 = company_Order.objects.filter(order_no=a).values_list('style_type', flat=True)
        idd_y = [];
        idd_y1 = [];
        idd_y2 = [];
        for j in y:
            idd_y.append(j)
        for j in y1:
            idd_y1.append(j)
        for j in y2:
            idd_y2.append(j)
        idd_y3 = [];
        idd_y4 = [];
        idd_y5 = [];
        for j in y3:
            idd_y3.append(j)
        for j in y4:
            idd_y4.append(j)
        for j in y5:
            idd_y5.append(j)

        k1 = category.objects.all()[idd_y[0] - 1]
        k2 = sub_category.objects.all()[idd_y1[0] - 1]
        k3 = super_category.objects.all()[idd_y2[0] - 1]
        k4 = Fabric.objects.all()[idd_y3[0] - 1]
        k5 = WashType.objects.all()[idd_y4[0] - 1]
        k6 = StyleType.objects.all()[idd_y5[0] - 1]
        print(k1, k2, k3, k4,k5,k6)
        k2 = " "+str(k2)+" "
        p = GeneratePFM.objects.filter(category=str(k1), sub_category=k2,fabric=str(k4),wash=str(k5),style_type=str(k6),super_category=str(k3)).values_list('pfmno', flat=True)
        print(p)
        section_res = [s for s in p]
        print(section_res)
        return JsonResponse({'section_res': section_res})

    if request.GET:
        pfmno = request.GET.get('pfmno')
        orderno = request.GET.get('orderno')
        styleno = request.GET.get('styleno')
        lineno = request.GET.get('lineno')
        shift = request.GET.get('shift')
        order_quantity = request.GET.get('order_quantity')
        capacity = request.GET.get('capacity')
        target = request.GET.get('target')
        skill_level = request.GET.get('skill_level')
        department = request.GET.get('department')
        section = request.GET.get('section')
        subSection = request.GET.get('sub_section')
        collar = request.GET.get('collar')
        pocket = request.GET.get('pocket')
        vent = request.GET.get('vent')
        lapel= request.GET.get('lapel')
        cuff = request.GET.get('cuff')
        sleeve = request.GET.get('sleeve')
        print("ggg")
        print(collar)
        gob=GenerateOB(pfmno=pfmno,orderno=orderno,styleno=styleno,lineno=lineno,shift=shift,order_quantity=order_quantity
            ,capacity=capacity,target=target,skill_level=skill_level,department=department,section=section,subSection=subSection,
            collar=collar,pocket=pocket,vent=vent,lapel=lapel,sleeve=sleeve,cuff=cuff)
        gob.save()

    if request.POST.get('pfmno'):
        pfm=request.POST.get('pfmno')
        ob=GeneratePFM.objects.filter(pfmno=pfm).values_list('super_category',flat=True)
        oa=ob[0]
        print(ob[0])
        q=0
        sup_id=super_category.objects.filter(name=ob[0]).values_list('id',flat=True)
        sub_id=super_category.objects.filter(name=ob[0]).values_list('product_Category_id',flat=True)
        cat_id=super_category.objects.filter(name=ob[0]).values_list('product_Subcategory_id',flat=True)
        print(sub_id)
        count=[]
        ar=[]
        zx=[]
        least=[]
        n=[]
        if (sub_id):
            print("pakda")
            lab=labels_Attributes.objects.filter(product_Supercategory_id=sup_id[0],product_Category_id=sub_id[0],
                product_Subcategory_id=cat_id[0]).values_list('name',flat=True)
            for i in lab:
                #print(i)
                pf_com=PFM_Components.objects.filter(name=i).values_list('id',flat=True)
                ar.append(pf_com)

            print(ar)
            for i in ar:
                if i.exists():
                    print(i[0])
                    n.append(PFM_Components.objects.filter(id=i[0]).values_list('name',flat=True))
                    zx.append(PFM_Attributes.objects.filter(pfm_component_id=i[0]).order_by('name'))
                else:
                    print("Emoty")

            print(zx)
            for i in n:
                count.append(str(i[0]))


            for i in zx:
                #print(i)
                for z in i:
                    print(z)
                    least.append(str(z))
                least.append("o")

            print(least)
            print(count)


            return JsonResponse({'component':count, 'type':least  })

        else:
            return JsonResponse({'component':"", 'type':""  })



    elif request.POST.get('section'):

        comp = request.POST.get('section')
        print(dept)
        print(comp)
        x = Section.objects.filter(department=dept,name=comp).values_list('id',flat=True)
        print(x[0])

        sub_section_res=subsection.objects.filter(section=x[0], department=dept)
        sub_section_res = [s.name for s in sub_section_res]
        print(sub_section_res)
        return JsonResponse({"sub_section_res": sub_section_res})

    if request.POST.get('submit'):
        print("got")
    gob= GenerateOB.objects.all()
    pfmnos = GeneratePFM.objects.all()
    department=Department.objects.all()
    section=Section.objects.all()
    sub_section=subsection.objects.all()
    orderno=company_Order.objects.all()
    context = {
        "ob":gob,
        "pfmnos" : pfmnos,
        "department":department,
        "section":section,
        "sub_section":sub_section,
        "orderno": orderno,
        }
    return render(request,'generateob1.html',context)



def form4(request):

    global check
    if request.GET:

        if request.GET.get('addoperation')=='false':

            pfmno = request.GET.get('pfmno')
            print(pfmno)
            typec = request.GET.get('type1')
            print(typec)
            na = request.GET.get('name')
            ids = request.GET.get('ids')
            cost = request.GET.get('cost')
            orderno = request.GET.get('orderno')
            print("xoxp")
            print(orderno)

            sam=AddOperations.objects.filter(id=ids).values_list('psam',flat=True)
            ct=AddOperations.objects.filter(id=ids).values_list('ct',flat=True)
            mp=float((float(sam[0])*600)/(480*1))  #expected skill level take from operator
            r_mp=round(mp)
            oph=float((60/float(ct[0]))*mp)
            print("if")
            Ob= GOperationBul(pfmno=pfmno,orderno=orderno,Type=typec,name=na,operation_id=ids,cost=cost,mpnos=mp,mpallocation=r_mp,oph=oph)
            Ob.save()

                # check=AddOperations.objects.last()
                # print("FG")
                # print(check.id)
                # cob=0

        else:
            o = request.GET.get("operations")
            pfmno = request.GET.get('pfmno')
            com = request.GET.get("complexity")
            spi = request.GET.get("spi")
            sl = request.GET.get("stitch_length")
            ma = request.GET.get("machine_auto")
            tc = request.GET.get("thread_consumption")
            wa = request.GET.get("work_aid")
            smv = request.GET.get("smv")
            al = request.GET.get("allowance")
            sam = request.GET.get("sam")
            ct = request.GET.get("ct")
            g = request.GET.get("grade")
            typec = request.GET.get('type1')
            print(typec)
            na = request.GET.get('name')
            ids = request.GET.get('ids')
            cost = request.GET.get('cost')
            ch= request.GET.get('check')
            t2= request.GET.get('t2')
            name2= request.GET.get('name2')
            print("hpola")
            print(name2)
            cost2= request.GET.get('cost2')
            orderno = request.GET.get('orderno')


            if(ch=="0"):
                dep=GenerateOB.objects.filter(orderno=orderno).values_list('department',flat=True)
                section=GenerateOB.objects.filter(orderno=orderno).values_list('section',flat=True)
                sub=GenerateOB.objects.filter(orderno=orderno).values_list('subSection',flat=True)
                print("db")
                print(dep[0])
                print(section[0][1:])
                print(sub[0][1:])
                sd = AddOperations(pfmno=pfmno,component="",component_type="",department=dep[0],section=section[0][1:]
                    ,sub_section=sub[0][1:],operations=o, complexity=com, spi=spi, stitch_length=sl, thread_consumption=tc
                    ,machine_auto=ma, work_aid=wa, smv=smv, allowance=al, sam=sam, ct=ct, grade=g)
                sd.save()
                check=AddOperations.objects.last()
                cob=1
                print("else")
                sam=AddOperations.objects.filter(id=check.id).values_list('psam',flat=True)
                ct=AddOperations.objects.filter(id=check.id).values_list('ct',flat=True)
                mp=float((float(sam[0])*600)/(480*1))  #expected skill level take from operator
                r_mp=round(mp)
                oph=float((60/float(ct[0]))*mp)
                print("if")
                Ob= GOperationBul(pfmno=pfmno,orderno=orderno,Type=t2,name=name2,operation_id=check.id,cost=cost2,mpnos=mp,mpallocation=r_mp,oph=oph)
                Ob.save()


            else:
                sam=AddOperations.objects.filter(id=ids).values_list('psam',flat=True)
                ct=AddOperations.objects.filter(id=ids).values_list('ct',flat=True)
                mp=float((float(sam[0])*600)/(480*1))  #expected skill level take from operator
                r_mp=round(mp)
                oph=float((60/float(ct[0]))*mp)
                print("if")
                Ob= GOperationBul(pfmno=pfmno,Type=typec,name=na,operation_id=ids,cost=cost,mpnos=mp,mpallocation=r_mp,oph=oph)
                Ob.save()



    if request.POST.get('pfmno'):

        pf = request.POST.get('pfmno')
        print(pf)
        #res = AddOperations.objects.filter(pfmno=pf).values_list('id','operations','complexity','spi','stitch_length'
        #	,'thread_consumption','machine_auto','work_aid','smv','allowance','sam','ct','grade')
        operations = AddOperations.objects.filter(pfmno=pf).values_list('operations',flat=True)
        complexity = AddOperations.objects.filter(pfmno=pf).values_list('complexity',flat=True)
        smv = AddOperations.objects.filter(pfmno=pf).values_list('smv',flat=True)
        psam = AddOperations.objects.filter(pfmno=pf).values_list('psam',flat=True)
        thread_consumption = AddOperations.objects.filter(pfmno=pf).values_list('thread_consumption',flat=True)
        spi = AddOperations.objects.filter(pfmno=pf).values_list('spi',flat=True)
        stitch_length = AddOperations.objects.filter(pfmno=pf).values_list('stitch_length',flat=True)
        work_aid = AddOperations.objects.filter(pfmno=pf).values_list('work_aid',flat=True)
        machine_auto = AddOperations.objects.filter(pfmno=pf).values_list('machine_auto',flat=True)
        pct = AddOperations.objects.filter(pfmno=pf).values_list('pct',flat=True)
        grade = AddOperations.objects.filter(pfmno=pf).values_list('grade',flat=True)
        allowance = AddOperations.objects.filter(pfmno=pf).values_list('allowance',flat=True)
        ida = AddOperations.objects.filter(pfmno=pf).values_list('id',flat=True)
        dept = AddOperations.objects.filter(pfmno=pf).values_list('department',flat=True)

        count=0
        for x in operations:
            count=count+1
        #serialized_q = json.dumps(list(res), cls=DjangoJSONEncoder)
        department= [s for s in dept]
        operations = [s for s in operations]
        complexity = [s for s in complexity]
        smv = [s for s in smv]
        psam = [s for s in psam]
        thread_consumption = [s for s in thread_consumption]
        spi = [s for s in spi]
        stitch_length = [s for s in stitch_length]
        work_aid = [s for s in work_aid]
        machine_auto = [s for s in machine_auto]
        pct = [s for s in pct]
        grade = [s for s in grade]
        allowance = [s for s in allowance]
        ida = [s for s in ida]

        print("holo")
        print(count)
        #res = [s for s in res]
        return JsonResponse({'ida':ida,'count': count,'operations':operations,'complexity':complexity,'smv':smv,'thread_consumption'
            :thread_consumption,'spi':spi,'stitch_length':stitch_length,'work_aid':work_aid,'machine_auto':machine_auto
            ,'ct':ct,'grade':grade,'allowance':allowance,'psam':psam,'dep':department})


    styledetailsobjects = AddOperations.objects.all()
    for x in styledetailsobjects:
        mp=(float(x.psam)*600)/(480*1)  #expected skill level take from operator
        r_mp=round(mp)
        oph=(60/float(x.pct))*mp
    machine_type=MachineType.objects.all()
    pfmnos = GeneratePFM.objects.all()
    gob= GenerateOB.objects.all()
    context = {
         "mp":mp,
         "gob":gob,
         "oph":oph,
         "rmp":r_mp,
         "machine_type": machine_type,
         "pfmnos" : pfmnos,
         "styledetailsobjects" : styledetailsobjects,

        }
    return render(request,'form4.html',context)





def show(request):


    if request.POST.get('department'):
        global dept
        dept = request.POST.get('department')
        section_res = Section.objects.filter(department=dept).order_by("name")
        section_res = [s.name for s in section_res]
        return JsonResponse({'section_res': section_res})

    if request.POST.get('secname'):
        s = request.POST.get('secname')
        d = request.POST.get('dname')
        Gob=GOperationBul.objects.all()
        for x in Gob:
            y=AddOperations.objects.filter(id=x.operation_id).all()
        for i in y:
            te=AddOperations.objects.filter(department=d,section=s).values_list('id',flat=True)
        g=[]
        idd=[];
        c=0
        for j in te:
            idd.append(j)

            g.append(AddOperations.objects.all().filter(id=j))


        return JsonResponse({'ids': idd})


    if request.POST.get('dname'):
        d = request.POST.get('dname')

        Gob=GOperationBul.objects.all()
        for x in Gob:
            y=AddOperations.objects.filter(id=x.operation_id).all()
        for i in y:
            te=AddOperations.objects.filter(department=d).values_list('id',flat=True)
        g=[]
        idd=[];
        c=0
        for j in te:
            idd.append(j)

            g.append(AddOperations.objects.all().filter(id=j))

        return JsonResponse({'ids': idd})




    elif request.POST.get('section'):

        comp = request.POST.get('section')
        x = Section.objects.filter(department=dept,name=comp).values_list('id',flat=True)

        sub_section_res=subsection.objects.filter(section=x[0], department=dept)
        sub_section_res = [s.name for s in sub_section_res]
        return JsonResponse({"sub_section_res": sub_section_res})


    gob= GOperationBul.objects.all()
    ff=AddOperations.objects.all()
    y=[]
    z=[]
    for x in gob:
        y.append(AddOperations.objects.all().filter(id=x.operation_id))


    for i in y:
        z.append(AddOperations.objects.all().filter(id=i))


    department=Department.objects.all()
    context = {
        "ff":y,
        "gob":gob,
        "department":department,
        }

    return render(request,'obulletin.html',context)
