from django.shortcuts import render
from .models import Requisition, Vouchers, Wage, Minute, Mon_Minute, Factory_Overhead,Administrative_Expenses, Financial_Expenses, Commercial_Expenses, Direct_Wage
# Create your views here.
def cpm(request):
    return render(request, 'home.html')

def domestic_travel_requisition(request):
    if request.method == 'POST':
        traveltype = request.POST['travtype']
        purpose = request.POST['purp']
        purposedescrip = request.POST['purdesc']
        journeytype = request.POST['jourtype']
        mode1 = request.POST['mode']
        placefrom1 = request.POST['placefrom']
        placeto1 = request.POST['placeto']
        traveldate1 = request.POST['travdate']
        etd1 = request.POST['etd']
        class1 = request.POST['class']
        airtrain1 = request.POST['preference']
        bookingtype1 = request.POST['booktype']
        mode2 = request.POST['mode0']
        placefrom2 = request.POST['placefrom0']
        placeto2 = request.POST['placeto0']
        traveldate2 = request.POST['travdate0']
        etd2 = request.POST['etd0']
        class2 = request.POST['class0']
        airtrain2 = request.POST['preference0']
        bookingtype2 = request.POST['booktype0']
        nationality = request.POST['nationality']
        passportno = request.POST['passp']
        placeofissue = request.POST['poi']
        dateofissue = request.POST['doi']
        dateofexpiry = request.POST['doe']
        dateofbirth = request.POST['dob']
        passportpcopy = request.POST['passcopy']
        advancedreq = request.POST['advance']
        travelinsurance =request.POST['travinsu']
        visa = request.POST['visa']
        simcard = request.POST['sim']
        r= Requisition(traveltype=traveltype,purpose = purpose, purposedescrip = purposedescrip,journeytype = journeytype,mode1 = mode1,placefrom1 = placefrom1,placeto1 =placeto1, traveldate1 = traveldate1,etd1 = etd1,class1 =class1, airtrain1 =airtrain1, bookingtype1 = bookingtype1,mode2 =mode2, placefrom2 = placefrom2,placeto2 = placeto2,traveldate2 = traveldate2,etd2 = etd2,class2 =class2, airtrain2 =airtrain2, bookingtype2 =bookingtype2, nationality = nationality,passportno =passportno, placeofissue = placeofissue,dateofissue =dateofissue, dateofexpiry =dateofexpiry, dateofbirth =dateofbirth,advancedreq = advancedreq,travelinsurance =travelinsurance, visa = visa,simcard =simcard)
        r.save()
        return render(request, 'domestic_travel_requisition.html')
    return render(request, 'domestic_travel_requisition.html')

def domestic_travel_voucher(request):
    if request.method == 'POST':
        fromdate = request.POST['from']
        todate = request.POST['to']
        days = request.POST['diff']
        nights = request.POST['ndiff']
        accomodation = request.POST['accomo']
        hotelname = request.POST['hotel']
        city = request.POST['city']
        roomrent = request.POST['rent']
        taxes = request.POST['tax']
        allcost = request.POST['total']
        excesscost = request.POST['amt']
        justification = request.POST['justi']
        companygst = request.POST['cgst']
        hotelgst = request.POST['hgst']
        hotelstate = request.POST['hstate']
        grandtotal = request.POST['totalities']
        v = Vouchers(fromdate=fromdate,todate=todate,days=days,nights=nights,accomodation=accomodation,hotelname=hotelname,city=city,roomrent=roomrent,taxes=taxes,allcost=allcost,excesscost=excesscost,justification=justification,companygst=companygst,hotelgst=hotelgst,hotelstate=hotelstate,grandtotal=grandtotal)
        v.save()
        return render(request, 'domestic_travel_voucher.html')
    return render(request, 'domestic_travel_voucher.html')

def wages_and_emp_summary(request):
    if request.method == 'POST':
        depart = request.POST['department']
        line = request.POST['line_no']
        month = request.POST['mon']
        employee = request.POST['emp']
        amount = request.POST['amt']
        w = Wage(department = depart, line_number = line, month = month, employee = employee, amount = amount)
        w.save()
        return render(request, 'wages.html')
    return render(request, 'wages.html')

def daily_linewise_available_minutes(request):
    if request.method == 'POST':
        date = request.POST['date']
        line = request.POST['value']
        minute = request.POST['min']
        m = Minute(date = date, line = line, minutes = minute)
        m.save()
        return render(request, 'minutes.html')
    return render(request, 'minutes.html')
def data(request):
    if request.method == 'POST':
        month = request.POST['month']
        line = request.POST['line_no']
        list = [int(x) for x in month.split("-")]
        obj = Minute.objects.all()
        total = 0
        for x in obj:
            b = str(x.date)
            list1 = [int(y) for y in b.split("-")]
            if list[0] == list1[0]:
                if list[1] == list1[1]:
                    if x.line == line:
                        total = total + x.minutes

        return render(request, 'monthly_minutes.html', {'minutes' : total, 'mon' : month, 'line' : line})
    else:
        return render(request, 'data.html')

def monthly_linewise_available_minutes(request):
    month = request.POST['month']
    line = request.POST['line_no']
    minutes = request.POST['min']
    m = Mon_Minute(month=month, line=line,minutes=minutes)
    m.save()
    return render(request, 'monthly_minutes.html')

def expenses_data(request):
    return render(request, 'expences_data.html')

def direct_wages(request):
    if request.method == 'POST':
        month = request.POST['month']
        wages = request.POST['wages']
        if request.POST.get('total'):
            total = request.POST['total']

            w = Direct_Wage(
                Month = month,
                Wages = wages,
                Total = total
            )
            w.save()
            return render(request, 'direct_wages.html')
        else:
            Total = wages
            depend = {'month':month, 'wages':wages, 'total':Total}
            return render(request, 'direct.html', depend)
    else:
        return render(request, 'direct_wages.html')


def factory_overhead(request):
    if request.method == 'POST':
        month     = request.POST.get('month')
        bonus     = int(request.POST['bonus'])
        carry     = int(request.POST['carry'])
        leave     = int(request.POST['leave'])
        bill      = int(request.POST['bill'])
        epf       = int(request.POST['epf'])
        rent      = int(request.POST['rent'])
        supply    = int(request.POST['supply'])
        food      = int(request.POST['food'])
        fuel      = int(request.POST['fuel'])
        cf        = int(request.POST['cf'])
        freight   = int(request.POST['freight'])
        insurance = int(request.POST['insurance'])
        labour    = int(request.POST['labour'])
        land      = int(request.POST['land'])
        medical   = int(request.POST['medical'])
        misc      = int(request.POST['misc'])
        repair    = int(request.POST['repair'])
        spare     = int(request.POST['spare'])
        transport = int(request.POST['transport'])
        travel    = int(request.POST['travel'])
        water     = int(request.POST['water'])
        welfare   = int(request.POST['welfare'])

        if request.POST.get('total'):
            total = request.POST['total']
            f = Factory_Overhead(
                month = month,
                bonus_incentives_others=bonus,
                carrying = carry,
                earn_leave_allowances=carry,
                electricity_bill = leave,
                epf_expenses = epf,
                factory_rent = rent,
                factory_supply = supply,
                food_expenses = food,
                generator_fuel = fuel,
                import_charges = cf,
                import_freight_charges = freight,
                insurance_premium = insurance,
                labour_charge = labour,
                land_rent = land,
                medical_expenses = medical,
                misc_expenses = misc,
                repair_nd_main = repair,
                small_tools_spares = spare,
                transport = transport,
                travel_conveyance = travel,
                water_bill = water,
                welfare_fund = welfare,
                total = total
            )
            f.save()
            return render(request, 'factory_overhead.html')
        else:
            Total = bonus+carry+leave+bill+epf+rent+supply+food+fuel+cf+freight+insurance+labour+land+medical\
                    +misc+repair+spare+transport+travel+water+welfare
            depend = { 'month':month,'bonus':bonus,'carry':carry,'leave':leave,'bill':bill,'epf':epf,'rent':rent,
                      'food':food,'fuel':fuel,'cf':cf,'freight':freight,'insurance':insurance,'labour':labour,
                      'land':land,'medical':medical,'misc':misc,'repair':repair,'spare':spare,'supply':supply,
                      'transport':transport,'travel':travel,'water':water,'welfare':welfare,'total':Total}
            return render(request, 'factory.html', depend)
    else:
        return render(request, 'factory_overhead.html')


def administrative_expenses(request):
    if request.method == 'POST':
        month        = request.POST.get('month')
        bonus        = int(request.POST['bonus'])
        compliance   = int(request.POST['compliance'])
        leave        = int(request.POST['leave'])
        fuel         = int(request.POST['fuel'])
        house        = int(request.POST['house'])
        rent         = int(request.POST['rent'])
        medical      = int(request.POST['medical'])
        misc         = int(request.POST['misc'])
        office       = int(request.POST['office'])
        postage      = int(request.POST['postage'])
        fees         = int(request.POST['fees'])
        repair       = int(request.POST['repair'])
        salary       = int(request.POST['salary'])
        security     = int(request.POST['security'])
        stationary   = int(request.POST['stationary'])
        subscription = int(request.POST['subscription'])
        internet     = int(request.POST['internet'])
        transport    = int(request.POST['transport'])
        travel       = int(request.POST['travel'])
        visa         = int(request.POST['visa'])

        if request.POST.get('total'):
            total = request.POST['total']
            a = Administrative_Expenses(
                Month = month,
                Bonus_incentives_others = bonus,
                Compliance_expenses = compliance,
                Earn_leave_allowance=leave,
                Fuel_nd_Lubricant= fuel,
                House_expenses = house,
                House_rent = rent,
                Medical_expenses = medical,
                Miscellaneous = misc,
                Office_supplies =office,
                Postage_courier =postage,
                Professional_fees =fees,
                Repair_nd_Maintain =repair,
                Salary_nd_Remuneration =salary,
                Security_charges =security,
                Stationary =stationary,
                Subscription_fee =subscription,
                Telephone_nd_Internet =internet,
                Transport =transport,
                Travel =travel,
                Visa_fee =visa,
                Total =total
            )
            a.save()
            return render(request, 'administrative_expenses.html')
        else:
            Total = bonus+compliance+leave+fuel+house+rent+medical+misc+office+postage+fees+repair+salary+security\
                    +stationary+subscription+internet+transport+travel+visa
            depend = {'month':month,'bonus':bonus,'compliance':compliance,'leave':leave,'fuel':fuel,'house':house,'rent':rent,
                      'medical':medical,'misc':misc,'office':office,'postage':postage,'fees':fees,'repair':repair,
                      'salary':salary,'security':security,'stationary':stationary,'subscription':subscription,
                      'internet':internet,'transport':transport,'travel':travel,'visa':visa,'total':Total}
            return render(request, 'administrative.html', depend)
    else:
        return render(request, 'administrative_expenses.html')


def commercial_expenses(request):
    if request.method == 'POST':
        month      = request.POST['month']
        commercial = int(request.POST['commercial'])
        cf         = int(request.POST['cf'])
        sample     = int(request.POST['sample'])

        if request.POST.get('total'):
            total = request.POST['total']
            c = Commercial_Expenses(
                Month = month,
                Commercial_expenses = commercial,
                Export_charges = cf,
                Sample_expenses = sample,
                Total = total
            )
            c.save()
            return render(request, 'commercial_expenses.html')
        else:
            Total = commercial + cf + sample
            depend = {'month':month, 'commercial':commercial, 'cf':cf, 'sample':sample, 'total':Total}
            return render(request, 'commercial.html', depend)

    else:
        return render(request, 'commercial_expenses.html')


def financial_expenses(request):
    if request.method == 'POST':
        month = request.POST['month']
        bank   = int(request.POST['bank'])
        export = int(request.POST['export'])
        lc     = int(request.POST['lc'])

        if request.POST.get('total'):
            total = request.POST['total']
            f = Financial_Expenses(
                Month=month,
                Bank_charges = bank,
                Export_bank_charges = export,
                LC_related_charges = lc,
                Total = total
            )
            f.save()
            return render(request, 'financial_expenses.html')
        else:
            Total = bank+export+lc
            depend = {'month':month, 'bank':bank, 'export':export, 'lc':lc, 'total':Total}
            return render(request, 'financial.html', depend)
    else:
        return render(request, 'financial_expenses.html')

def wage_table(request):
    wage_all = Wage.objects.all()
    print(wage_all)
    return render(request, 'wage_table.html',{'wages' : wage_all})

def domestic_voucher_view(request):
    voucher_all = Vouchers.objects.all()
    print(voucher_all)
    return render(request, 'domestic_voucher_view.html',{'domestic_travel_voucher' : voucher_all})

def min_table(request):
    minute_all = Minute.objects.all()
    return render(request, 'min_table.html', {'minutes' : minute_all})

def mon_minute(request):
    mon_min_all = Mon_Minute.objects.all()
    return render(request, 'mon_minute.html', {'minutes': mon_min_all})

def expenses_record(request):
    wage = Direct_Wage.objects.all()
    overhead = Factory_Overhead.objects.all()
    administrative = Administrative_Expenses.objects.all()
    commerce = Commercial_Expenses.objects.all()
    finance = Financial_Expenses.objects.all()

    departments = {'wage':wage, 'overhead':overhead, 'administrative':administrative,
                   'commerce':commerce, 'finance':finance}

    return render(request, 'expenses_record.html', departments)