#diet type to e implemeted while update
from datetime import time
from django.db.models.query import EmptyQuerySet
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from .models import NutritionModel,Nutrition_item,diet,diet_detail,ml,memo,memo1,memo2,memo3
from  nutrition.models import Diet_sheet,Nutrition_table
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm 
from django.contrib.auth.decorators import login_required
from csv import writer
import csv
from .forms import dietform,dietform1
from django.db.models import Func, F
from django.views.generic import UpdateView,DeleteView
from django.core.exceptions import FieldError
from django.contrib.postgres.operations import UnaccentExtension
from django.contrib.postgres.search import TrigramDistance
#from django.shortcuts import ()

def index(request):
    return render(request,"diet_plan/index.html")

def healthy_diet(request):
    return render(request,"diet_plan/healthy_diet.html")



def admin_login(request):
    return render(request,"diet_plan/healthy_diet.html")


def diet_plan(request):
    id=request.POST.getlist('id')
    print(id)

    return render(request,"diet_plan/diet_plan.html",{'data':id})


def user_health_profile(request):
    return render(request, "diet_plan/user_health_profile.html")


reqs={}
ret={}

@login_required
def check_nutri(request):
    list2 = dietform() 
    if request.method =="POST":
        form = dietform(request.POST) 
        if form.is_valid():
            print('hi')
            b=form.cleaned_data.get('Product')
            c=form.cleaned_data.get('type')

    gen=request.POST.get('gender')
    age=int(request.POST.get('age'))
    height=int(request.POST.get('height'))
    weight=int(request.POST.get('weight'))
    #bodyfat=int(request.POST.get('bodyfat'))
    bodyphy=request.POST.get('bodyphy')
    exercise=request.POST.get('exercise')
    activity=request.POST.get('activity')
    blood_pressure=request.POST.get('blood_pressure')
    sugar=request.POST.get('sugar')
    # vitamin=request.POST.get('vitamin')
    # mineral=request.POST.get('mineral')
    blood_group=request.POST.get('blood_group')
    meal=int(request.POST.get('meal'))

    food_habbit=request.POST.get('food_habbit')
    food_preference=request.POST.get('food_preference')
    disability=request.POST.get('disability')
    medical_issues=request.POST.get('medical_issues')
    diseases=request.POST.get('diseases')

    data={'gen':gen,'age':age,'height':height,'weight':weight,'bodyfat':0,'bodyphy':bodyphy,
          'exercise':exercise,'activity':activity,'blood_pressure':blood_pressure,'sugar':sugar,
          'blood_group':blood_group,'food_habbit':food_habbit,'food_preference':food_preference,'disability':disability,
          'medical_issues':medical_issues,'diseases':diseases}

    memo1.objects.all().delete()
    memo1.objects.create(d=1,gen=gen,age=age,height=height,weight=weight,bodyfat=0,bodyphy=bodyphy,
          exercise=exercise,activity=activity,blood_pressure=blood_pressure,sugar=sugar,
          blood_group=blood_group,food_habbit=food_habbit,food_preference=food_preference,disability=disability,
          medical_issues=medical_issues,diseases=diseases)


    bmi=(10000*weight)/(height*height)

    # lean_body_mass=((100-bodyfat)*weight)/100  #according to excel calculation

    #  Katch-McArdle formula for calculating lean_body_mass
    array = ['Sedentary',"Lightly Active","Moderately Active","Intence Weight training/sports","Very Active","Extra Active"]
    act =0
    ahj=0
    for x in array:
        if x==activity:
            act =ahj
        ahj+=1

#uncomment to add a new line in csv for training & ml
    # List=[weight,bmi,act,1]

    # with open('diet.csv', 'a') as f_object:
  
    # # Pass this file object to csv.writer()
    # # and get a writer object
    #     writer_object = writer(f_object)
  
    # # Pass the list as an argument into
    # # the writerow()
    #     writer_object.writerow(List)
  
    # #Close the file object
    #     f_object.close()


#uncomment to involve csv input
    # datasets = pd.read_csv('diet.csv')
    # print(datasets)
#uncomment to save csv data in database ml table
    # with open('diet.csv', newline='') as csvfile:
    #      data = csv.reader(csvfile, delimiter=',')
    #      fields = next(data)
    #      for row in data:
    #         print(row)
    #         a=int(row[0]) 
    #         c=float(row[1])
    #         d=int(row[2])
    #         e=float(row[3])

            #ml.objects.create(wt=a,mi=c,ac=d,pr=e)
            #print(row)
    #data = csv.reader(csvfile, delimiter=',')
    mld=ml.objects.all()
    mld = mld.values('wt','mi','ac','pr')
    mld = list(mld)
    #print(mld)
    mld = pd.DataFrame(mld)
    datasets =mld
    X = datasets.iloc[:, :-1].values
    #print(X)
    Y = datasets.iloc[:, 3].values
    #print(Y)
    #print(X)
    labelencoder_X = LabelEncoder()
    #print(X)
    X[:, 2] = labelencoder_X.fit_transform(X[:, 2])
    #onehotencoder = OneHotEncoder(categorical_features = [2])
    #X = onehotencoder.fit_transform(X).toarray()
    #X = X[:, 1:]
    #print(X)
    #X = np.append(arr=np.ones((50,1)), values=X, axis=1)
    ct = ColumnTransformer([("Country", OneHotEncoder(), [2])], remainder = 'passthrough')

    X = ct.fit_transform(X)
    #print(X)

    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
    regressor = LinearRegression()
    regressor.fit(X_Train, Y_Train)
    Y_Pred = regressor.predict(X_Test)
    X_Optimal = X[:, [0,1,2,3,4,5]]
    regressor_OLS = sm.OLS(endog = Y, exog = X_Optimal).fit()
    regressor_OLS.summary()

    X_Optimal = X[:, [0,1,2,4,5]]
    regressor_OLS = sm.OLS(endog = Y, exog = X_Optimal).fit()
    regressor_OLS.summary()

    X_Optimal = X[:, [0,1,4,5]]
    regressor_OLS = sm.OLS(endog = Y, exog = X_Optimal).fit()
    regressor_OLS.summary()

    X_Optimal = X[:, [0,1,4]]
    regressor_OLS = sm.OLS(endog = Y, exog = X_Optimal).fit()
    regressor_OLS.summary()

    X_Optimal_Train, X_Optimal_Test = train_test_split(X_Optimal,test_size = 0.2, random_state = 0)
    regressor.fit(X_Optimal_Train, Y_Train)
    Y_Optimal_Pred = regressor.predict(X_Optimal_Test)
    #print(Y_Optimal_Pred)

#uncomment to add a line from prediction in csv file
    # with open('diet.csv', 'r') as f:
    #     reader = csv.DictReader(f, delimiter=',')
    #     rows = list(reader)
    #     rows[-1].update({'prot_req.': Y_Optimal_Pred[-1]})
    #     #print(rows[-1])

    # with open('diet.csv', 'w') as f:
    #     writer1 = csv.DictWriter(f, fieldnames = rows[-1].keys())
    #     writer1.writeheader()
    #     writer1.writerows(rows)
    
    pro=Y_Optimal_Pred[-1]
    #List[3]=pro
    ml.objects.create(wt=weight,mi=bmi,ac=act,pr=pro)
    print(activity)
    #VitA Vit C Vit D Sodium Iro Potassium Calcium Magnesium Zinc Phosphorus
    if activity=='Sedentary':
        reqs={'energy':(2320/60)*weight,'fat':(25/60)*weight,'pro':pro*weight,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Lightly Active':
        reqs={'energy':(2520/60)*weight,'fat':(27.5/60)*weight,'pro':pro*weight,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Moderately Active':
        reqs={'energy':(2730/60)*weight,'fat':(30/60)*weight,'pro':pro*weight,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Intence Weight training/sports'or "Very Active" or "Extra Active":
        reqs={'energy':(3490/60)*weight,'fat':(40/60)*weight,'pro':pro*weight,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}

    print('reqs:',reqs)

    
    if gen =='Male':
        lean_body_mass= 0.407 *weight+ 0.267 *height- 19.2
    else:
        lean_body_mass= 0.252 *weight+ 0.473 * height - 48.3

    lean_bmi=(10000*lean_body_mass)/(height*height)
    basal_metabolic_rate=370+(21.6*lean_body_mass)

    if activity=='Sedentary':
        maintaince=basal_metabolic_rate*1.200
    elif activity=='Lightly Active':
        maintaince = basal_metabolic_rate * 1.375
    elif activity=='Moderately Active':
        maintaince = basal_metabolic_rate * 1.550
    elif activity=='Intence Weight training/sports':
        maintaince = basal_metabolic_rate * 1.650
    elif activity=='Very Active ':
        maintaince = basal_metabolic_rate * 1.725

    else:
        maintaince = basal_metabolic_rate * 1.900
    data1={'bmi':bmi,'lean_body_mass':lean_body_mass,'basal_metabolic_rate':basal_metabolic_rate,'maintaince':maintaince,'lean_bmi':lean_bmi}
    memo2.objects.all().delete()
    memo2.objects.create(d=1,bmi=bmi,lean_body_mass=lean_body_mass,basal_metabolic_rate=basal_metabolic_rate,maintaince=maintaince,lean_bmi=lean_bmi)
    # protein 30%
    # carbs 50%
    # fat 20%
    protein_in_kcal=(maintaince*0.3)
    protein_in_gr=protein_in_kcal/4
    req=(weight*Y_Optimal_Pred)
    #print(req)
    #print(req[-1])
    #res=diet_detail.Protein()
    diseases=diseases.lower()
    food_habbit=food_habbit.lower()
    food_preference=food_preference.lower()
    print(diseases)
    print(food_habbit)
    print(food_preference)
    #food_preference=request.POST.get('food_preference')
    res=diet_detail.objects.values_list('Protein', flat=True).order_by('Protein').filter(type=food_habbit,regio__contains=food_preference)
    print(res.count())
    if diseases!='none' and diseases!='None':
        print('why here')
        res=diet_detail.objects.values_list('Protein', flat=True).order_by('Protein').filter(disease__contains=diseases,type=food_habbit,regio__contains=food_preference)
    #filter(disease__contains=diseases,type__contains=food_habbit,regio__contains=food_preference)
    if not res:
        print('empty1')
        res=diet_detail.objects.values_list('Protein', flat=True).order_by('Protein').filter(disease__contains=diseases,type=food_habbit)

    if not res:
        print('empty')
        res=diet_detail.objects.values_list('Protein', flat=True).order_by('Protein').filter(diet_sr=8)
    
    res=list(res)
    #print(res)
    
    #if for empty rel required
    if res:
        rel=min(res, key=lambda x:abs(float(x)-req[-1]))
        print('ok')
    
    else:
        rel=100

    print(rel)
    ret=diet_detail.objects.none()
    #ret=1

    print(res)
    rw=0
    rs=0

    for rew in res:
        #print(rew)
        rets=diet_detail.objects.filter(Protein=rew,type=food_habbit,regio__contains=food_preference)
        #print(rets,'hehere')
        if rets[0].Protein==rel:
            rs=rets
            print('hi')
        
        #print(rets[0].Protein)
        
        else:
            ret=ret.union(rets)
        print(ret)

        if rw>3:
            break
    
    if not ret:
        print('empty')
        ret=diet_detail.objects.filter(diet_sr=8)
    
    
    print(ret, "diet plas")
    #print(ret[1])
    #print(data, data1,'here ')
    try:
        
        diet1=diet.objects.filter(diet_sr=ret[0].diet_sr)
        memo.objects.all().delete()
        memo.objects.create(d=1,sr=ret[0].diet_sr,mi=str(reqs['energy']),ac=str(reqs['fat']),pr=str(reqs['pro']))
#uncomment to update diet item by csv
        # with open("diet_updt.csv", "w+") as f:
        #     f.write(ret[0].diet_sr)
        #     #print(reqs)
        #     #print(reqs['energy'])
        #     f.write(",")
        #     f.write(str(reqs['energy']))
        #     f.write(",")
        #     f.write(str(reqs['fat']))
        #     f.write(",")
        #     f.write(str(reqs['pro']))
        #     f.close()
    except IndexError:
        diet1=[]
    #print(diet1[0].diet_sr,'yahi h')
    diet2=list(diet1)
    
    #print(diet2[0])

    carbs_in_kcal=(maintaince*0.5)
    carbs_in_gr=carbs_in_kcal/4
    fat_in_kcal=(maintaince*0.2)
    fat_in_gr=fat_in_kcal/9
    data2={'protein_in_gr':protein_in_gr,'carbs_in_gr':carbs_in_gr,'fat_in_gr':fat_in_gr}
    memo3.objects.all().delete()
    memo3.objects.create(d=1,protein_in_gr=protein_in_gr,carbs_in_gr=carbs_in_gr,fat_in_gr=fat_in_gr)


    print(data, data1,data2)
    rw=ret
    ret=rs[0]

    # print(data)
    # print(data1)
    # print(data2)
    # print(c)
    # print(diet1)
    if food_habbit =='VEG':
        a=Diet_sheet.objects.filter(Preferrence='veg',protein__range=[protein_in_gr-5,protein_in_gr+5])
        b = a.filter(carbs__range=[carbs_in_gr - 5, carbs_in_gr + 5])

        c = b.filter(fat__range=[fat_in_gr - 5, fat_in_gr + 5])[:50]
        return render(request,"show.html",{'data':data,'data1':data1,'data2':data2 ,'a':c,'diet1':diet1})
    else:
        a = Diet_sheet.objects.filter( Preferrence='nonveg',protein__range=[protein_in_gr-5, protein_in_gr + 5])

        b=a.filter(carbs__range=[carbs_in_gr-5,carbs_in_gr+5])

        c=b.filter(fat__range=[fat_in_gr-5,fat_in_gr+5])[:50]

    
        
        return render(request, "diet_plan/show.html", {'data': data, 'data1': data1,'data2':data2 , 'a': c, 'diet1':diet1, 'reqs':reqs,'give':ret,'rw':rw})



# class updt_diet(UpdateView):
#     model=diet
#     form_class=dietform
#     template_name='diet_plan/update.html'
    
#     #redirect=updt_diet1
#     def form_valid(self, form):
#         kwargs=self.kwargs['pk']
#         diet1=diet.objects.filter(id=kwargs)
#         print(diet1)
#         print(kwargs)
#         return redirect(updt_diet1)
    #redirect=updt_diet1

@login_required    
def update_view(request, pk):
    # dictionary for initial data with
    # field names as keys
    id=pk
    context ={}
    print('ok')
 
    # fetch the object related to passed id
    obj = get_object_or_404(diet, id = id)
 
    # pass the object as instance in form
    form = dietform(request.POST or None, instance = obj)
    l=memo.objects.filter(d=1)
    print(l)
    a=int(l[0].sr)
    b=float(l[0].mi)
    c=float(l[0].ac)
    d=float(l[0].pr)


    data=memo1.objects.filter(d=1)
    data1=memo2.objects.filter(d=1)
    data2=memo3.objects.filter(d=1)

    gen= data[0].gen
    age= data[0].age
    height= data[0].height
    weight= data[0].weight
    bodyfat= data[0].bodyfat
    bodyphy= data[0].bodyphy
    exercise= data[0].exercise
    activity= data[0].activity
    blood_pressure= data[0].blood_pressure
    sugar= data[0].sugar
    blood_group= data[0].blood_group
    food_habbit= data[0].food_habbit
    food_preference= data[0].food_preference
    disability= data[0].disability
    medical_issues= data[0].medical_issues
    diseases= data[0].diseases

    bmi=data1[0].bmi
    lean_body_mass=data1[0].lean_body_mass
    basal_metabolic_rate=data1[0].basal_metabolic_rate
    maintaince=data1[0].maintaince
    lean_bmi=data1[0].lean_bmi

    protein_in_gr=data2[0].protein_in_gr
    carbs_in_gr=data2[0].carbs_in_gr
    fat_in_gr=data2[0].fat_in_gr

    data={'gen':gen,'age':age,'height':height,'weight':weight,'bodyfat':0,'bodyphy':bodyphy,
          'exercise':exercise,'activity':activity,'blood_pressure':blood_pressure,'sugar':sugar,
          'blood_group':blood_group,'food_habbit':food_habbit,'food_preference':food_preference,'disability':disability,
          'medical_issues':medical_issues,'diseases':diseases}

    data1={'bmi':bmi,'lean_body_mass':lean_body_mass,'basal_metabolic_rate':basal_metabolic_rate,'maintaince':maintaince,'lean_bmi':lean_bmi}

    data2={'protein_in_gr':protein_in_gr,'carbs_in_gr':carbs_in_gr,'fat_in_gr':fat_in_gr}

    if activity=='Sedentary':
        reqs={'energy':(2320/60)*weight,'fat':(25/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Lightly Active':
        reqs={'energy':(2520/60)*weight,'fat':(27.5/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Moderately Active':
        reqs={'energy':(2730/60)*weight,'fat':(30/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Intence Weight training/sports'or "Very Active" or "Extra Active":
        reqs={'energy':(3490/60)*weight,'fat':(40/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}

    #type='nonveg'
    print(food_preference,'p')
    de=diet.objects.filter(id=id)
    d=de[0].Product
    print(d,'ch')
    d=Nutrition_item.objects.filter(Product__icontains=d)
    sr=diet_detail.objects.filter(diet_sr=de[0].diet_sr)
    retr=Nutrition_item.objects.all()
    
    print(sr[0].type,food_preference)
    if sr[0].type=='nonveg':
        rets=Nutrition_item.objects.filter(season__icontains='all',region__icontains='all')
        ret=Nutrition_item.objects.none()
        ret=ret.union(rets)
        rets=Nutrition_item.objects.filter(season__icontains='all',region__icontains=food_preference)  
       # print(rets)     
        ret=ret.union(rets)
        if not ret:
            rets=Nutrition_item.objects.all()  
        #print(rets)     
            ret=ret.union(rets)
    else:
        rets=Nutrition_item.objects.filter(type__contains='veg',season__contains='all',region__contains='all')
        ret=Nutrition_item.objects.none()
        ret=ret.union(rets)
        rets=Nutrition_item.objects.filter(type__contains='veg',season__contains='all',region__contains=food_preference)        
        ret=ret.union(rets)

    print(ret,'ok')
    
    print(de)
    #d=de[0].diet_sr
    
    print(d)
    a=sr[0].Kcal
    print('ok')
    reqs1={'energy':(3490/60)*weight,'fat':(40/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}

 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        print('here')
        pro=request.POST.get('Product')
        copy=request.POST.get('copy')
        #type=request.POST.get('type')
        print(pro)
        if d[0].Product!=pro or de[0].copy!=copy:
            print('change')
            eg=Nutrition_item.objects.filter(Product__icontains=pro)
            print(eg)
            fp=(eg[0].Protein*float(copy)-d[0].Protein*de[0].copy)/7
            ff=(eg[0].Fat*float(copy)-d[0].Fat*de[0].copy)/7
            fc=(eg[0].Carbs*float(copy)-d[0].Carbs*de[0].copy)/7
            fe=(eg[0].Kcal*float(copy)-d[0].Kcal*de[0].copy)/7
            print(fp,fe,fc,ff)
            if fp!=0 or ff!=0 or fc!=0 or fe!=0:
                print('replace')
                diet_detail.objects.filter(diet_sr=de[0].diet_sr).update(Kcal=F('Kcal') + fe,Protein=F('Protein') + fp,Fat=F('Fat') + ff,Carbs=F('Carbs') + fc)
        #res=diet_detail.objects.values_list('protei', flat=True).order_by('protei').filter(disease__contains=diseases,type=food_habbit)
        form.save()
        return redirect('updt_diet1',id)
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "diet_plan/update.html", {'form':form,'reqs':reqs,'retr':ret})

@login_required
def updt_diet1(request,id):
    # with open('diet_updt.csv', newline='') as csvfile:
    #      data = csv.reader(csvfile, delimiter=',')
    #      for row in data:
    #          #print(row)
    #          li=row
    #          a=int(li[0])
    #          b=float(li[1])
    #          c=float(li[2])
    #          d=float(li[3])
    #          print(d)
    l=memo.objects.filter(d=1)
    print(l)
    a=int(l[0].sr)
    b=float(l[0].mi)
    c=float(l[0].ac)
    d=float(l[0].pr)


    data=memo1.objects.filter(d=1)
    data1=memo2.objects.filter(d=1)
    data2=memo3.objects.filter(d=1)

    gen= data[0].gen
    age= data[0].age
    height= data[0].height
    weight= data[0].weight
    bodyfat= data[0].bodyfat
    bodyphy= data[0].bodyphy
    exercise= data[0].exercise
    activity= data[0].activity
    blood_pressure= data[0].blood_pressure
    sugar= data[0].sugar
    blood_group= data[0].blood_group
    food_habbit= data[0].food_habbit
    food_preference= data[0].food_preference
    disability= data[0].disability
    medical_issues= data[0].medical_issues
    diseases= data[0].diseases

    bmi=data1[0].bmi
    lean_body_mass=data1[0].lean_body_mass
    basal_metabolic_rate=data1[0].basal_metabolic_rate
    maintaince=data1[0].maintaince
    lean_bmi=data1[0].lean_bmi

    protein_in_gr=data2[0].protein_in_gr
    carbs_in_gr=data2[0].carbs_in_gr
    fat_in_gr=data2[0].fat_in_gr

    data={'gen':gen,'age':age,'height':height,'weight':weight,'bodyfat':0,'bodyphy':bodyphy,
          'exercise':exercise,'activity':activity,'blood_pressure':blood_pressure,'sugar':sugar,
          'blood_group':blood_group,'food_habbit':food_habbit,'food_preference':food_preference,'disability':disability,
          'medical_issues':medical_issues,'diseases':diseases}

    data1={'bmi':bmi,'lean_body_mass':lean_body_mass,'basal_metabolic_rate':basal_metabolic_rate,'maintaince':maintaince,'lean_bmi':lean_bmi}

    data2={'protein_in_gr':protein_in_gr,'carbs_in_gr':carbs_in_gr,'fat_in_gr':fat_in_gr}

    if activity=='Sedentary':
        reqs={'energy':(2320/60)*weight,'fat':(25/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Lightly Active':
        reqs={'energy':(2520/60)*weight,'fat':(27.5/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Moderately Active':
        reqs={'energy':(2730/60)*weight,'fat':(30/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Intence Weight training/sports'or "Very Active" or "Extra Active":
        reqs={'energy':(3490/60)*weight,'fat':(40/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}

    dt1=diet.objects.filter(id=id)
    print(dt1,'hi')

    try:
        diet1=diet.objects.filter(diet_sr=dt1[0].diet_sr)
        ret=diet_detail.objects.filter(diet_sr=dt1[0].diet_sr)
        #reqs={'energy':b,'fat':c,'pro':d}


    except IndexError:
        diet1=[]
    print(ret,'here')
    print(reqs)
    #print(ret[0].diet_sr)
    #diet2=list(diet1)
    return render(request,"diet_plan/show.html",{'data':data, 'data1':data1, 'data2':data2, 'diet1':diet1,'reqs':reqs,'give':ret[0]})


@login_required
def check_csv(request):
    file = request.FILES['csv_file'] 
    decoded_file = file.read().decode('utf-8').splitlines()
    data = csv.reader(decoded_file)
    list1=[]
    fields = next(data)
    fields = next(data)
    for row in data:
        print(row)
        li=row
        #print(li)
        a=li[0]
        b=li[1]
        #print(b)
        c=li[2]
        d=li[3]
        e=float(li[4])
        f=float(li[5])
        g=float(li[6])
        h=float(li[7])
        i=float(li[8])
        j=float(li[9])
        k=float(li[10])
        l=float(li[11])
        m=float(li[12])
        n=float(li[13])
        o=float(li[14])
        p=float(li[15])
        q=float(li[16])
        r=float(li[17])
        s=float(li[18])
        t=float(li[19])
        u=float(li[20])
        v=float(li[21])
        w=float(li[22])
        x=float(li[23])
        y=float(li[24])
        z=float(li[25])
        aa=float(li[26])
        ab=float(li[27])
        ac=float(li[28])
        ad=float(li[29])
        ae=float(li[30])
        af=float(li[31])
        ag=float(li[32])
        ah=float(li[33])
        ai=float(li[34])
        aj=float(li[35])
        ak=float(li[36])
        al=float(li[37])
        am=float(li[38])
        an=float(li[39])
        ao=float(li[40])
        ap=float(li[41])
        aq=float(li[42])
        ar=float(li[43])
        asa=float(li[44])
        at=float(li[45])
        au=float(li[46])
        av=float(li[47])
        aw=float(li[48])
        ax=float(li[49])
        ay=float(li[50])
        az=float(li[51])
        ca=float(li[52])
        cb=float(li[53])
        cc=float(li[54])
        cd=float(li[55])
        ce=float(li[56])
        #print("ok")
        cf=float(li[57])
        cg=float(li[58])
        ch=float(li[59])
        ci=float(li[60])
        cj=float(li[61])
        ck=float(li[62])
        cl=float(li[63])
        cm=float(li[64])
        cn=float(li[65])
        co=float(li[66])
        cp=float(li[66])
        cq=float(li[66])
        cr=float(li[66])
        duty=Nutrition_item.objects.filter(Product=a)
        #print(duty,'here')
        if duty:
            print(a,', already saved')
        else:
            Nutrition_item.objects.create(Product=a,type=b,region=c,season=d,Kcal=e,Protein=f,Fat=g,Carbs=h,T_sat_fat=i,T_umo_fat=j,T_upo_fat=k,choles=l,sodium=m,T_fi=n,Vit_A_Re=o,Vit_A_IU=p,alpha_toco=q,ascor=r,thiami=s,iaci=t,Vit_B6=u,folaci=v,Vit_B12=w,Potassium=x,Calcium=y,Phosphorus=z,Magnesium=aa,Iron=ab,Zinc=ac,Pantothenic_acid=ad,Copper=ae,Manganese=af,Ash=ag,Water=ah,energy_kJ=ai,Caprylic_Acid=aj,Capric_Acid=ak,Lauric_Acid=al,Myristic_Acid=am,Palmitic_Acid=an,Palmitoleic_Acid=ao,Stearic_Acid=ap,Oleic_Acid=aq,Linoleic_acid=ar ,Linolenic_acid=asa,Gadoleic_acid=at,Docosenoic_acid=au,Phytosterols=av,Histidine=aw,Isoleucine=ax,Leucine=ay,Lysine=az,Methionine=ca,Cystine=cb,Methionine_Cystine=cc,Phenylalanine=cd,Tyrosine=ce,Phenylalanine_Tyrosine=cf,Threonine=cg,Tryptophan=ch,Valine=ci,Arginine=cj,Alanine=ck,Aspartic_acid=cl,Glutamic_acid=cm,Glycine=cn,Proline=co,Serine=cp,Vit_C=cq,Vit_D=cr)
            print(a,'saved')
            
    

    return render(request, "diet_plan/diet_time_csv.html", locals())

@login_required
def diet_csv(request):
    file = request.FILES['csv_file'] 
    decoded_file = file.read().decode('utf-8').splitlines()
    data = csv.reader(decoded_file)
    list1=[]
    print(data)
    fields = next(data)
    #fields = next(data)
    if diet.objects.count()==0:
        #Water 2.15 g Vit A 390.00 µg Vit C 0.00 mg Vit D 0.00 mg Sodium 0.00 mg Iro 18.41 mg PotassiumCalciumMagnesiumZinc Phosphorus
        diet_detail.objects.update(Kcal=F('Kcal') *0,Protein=F('Protein') * 0,Fat=F('Fat') *0,Carbs=F('Carbs') * 0,Water=F('Water')*0,Vit_A_IU=F('Vit_A_IU')*0,Vit_C=F('Vit_C')*0,Vit_D=F('Vit_D')*0,sodium=F('sodium')*0,Iron=F('Iron')*0,Potassium=F('Potassium')*0,Calcium=F('Calcium')*0,Magnesium=F('Magnesium')*0,Zinc=F('Zinc')*0, Phosphorus=F('Phosphorus')*0)
        print('0 diets')
    else:
        diet_detail.objects.update(Kcal=F('Kcal') *7,Protein=F('Protein') * 7,Fat=F('Fat') *7,Carbs=F('Carbs') * 7,Water=F('Water')*7,Vit_A_IU=F('Vit_A_IU')*7,Vit_C=F('Vit_C')*7,Vit_D=F('Vit_D')*7,sodium=F('sodium')*7,Iron=F('Iron')*7,Potassium=F('Potassium')*7,Calcium=F('Calcium')*7,Magnesium=F('Magnesium')*7,Zinc=F('Zinc')*7, Phosphorus=F('Phosphorus')*7)
    for row in data:
        #print(row)
        li=row
        #print(li)
        a=int(li[0])
        b=int(li[1])
        #print(b)
        c=int(li[2])
        d=float(li[3])
        e=li[4]
        f=li[5]
        de=Nutrition_item.objects.filter(Product__icontains=e)
        
        if e in list1:
            print('ok')
        elif de:
            print('add')
            defa=diet_detail.objects.filter(diet_sr=a)
            if not defa:
                diet_detail.objects.create(diet_sr=a)
            defa=diet_detail.objects.filter(diet_sr=a)
            print(defa,de)
            print(defa[0].type)
            print(de[0].type)
            if defa[0].type=='veg' and de[0].type!='veg':
                diet_detail.objects.filter(diet_sr=a).update(type=de[0].type)
            if defa[0].seaso=='all' and de[0].season!='all':
                diet_detail.objects.filter(diet_sr=a).update(seaso=de[0].season)
            if defa[0].regio=='all' and de[0].region!='all':
                diet_detail.objects.filter(diet_sr=a).update(regio=de[0].region)
            if c>int(defa[0].t_periods):
                diet_detail.objects.filter(diet_sr=a).update(t_periods=str(c))
                    #print(de)
            #print(diet_detail.Kcal)
            if diet.objects.filter(diet_sr=a,diet_day=b,diet_time=c,Product=e):
                print('already added')
            else:
                diet_detail.objects.filter(diet_sr=a).update(Kcal=F('Kcal') + de[0].Kcal*d,Protein=F('Protein') + de[0].Protein*d,Fat=F('Fat') + de[0].Fat*d,Carbs=F('Carbs') + de[0].Carbs*d,Water=F('Water')+ de[0].Water*d,Vit_A_IU=F('Vit_A_IU')+ de[0].Vit_A_IU*d,Vit_C=F('Vit_C')+ de[0].Vit_C*d,Vit_D=F('Vit_D')+ de[0].Vit_D*d,sodium=F('sodium')+ de[0].sodium*d,Iron=F('Iron')+ de[0].Iron*d,Potassium=F('Potassium')+ de[0].Potassium*d,Calcium=F('Calcium')+ de[0].Calcium*d,Magnesium=F('Magnesium')+ de[0].Magnesium*d,Zinc=F('Zinc')+ de[0].Zinc*d, Phosphorus=F('Phosphorus')+ de[0].Phosphorus*d)
                #print('done',e)
            
                diet.objects.create(Product=e,copy=d,diet_sr=a,diet_day=b,diet_time=c,type=f)
            
        else:
            list1.append(e)

    diet_detail.objects.update(Kcal=F('Kcal') /7,Protein=F('Protein') / 7,Fat=F('Fat') / 7,Carbs=F('Carbs') / 7,Water=F('Water')/7,Vit_A_IU=F('Vit_A_IU')/7,Vit_C=F('Vit_C')/7,Vit_D=F('Vit_D')/7,sodium=F('sodium')/7,Iron=F('Iron')/7,Potassium=F('Potassium')/7,Calcium=F('Calcium')/7,Magnesium=F('Magnesium')/7,Zinc=F('Zinc')/7, Phosphorus=F('Phosphorus')/7)
    print(list1)
    if list1:
        return render(request, "diet_plan/readd.html", {'list1':list1})
    
    defa=diet_detail.objects.all()
    print(defa)
    return render(request, "diet_plan/detail.html", {'d':defa})

@login_required    
def update_pla(request, pk):
    # dictionary for initial data with
    # field names as keys
    id=pk
    context ={}
    print('ok')
 
    # fetch the object related to passed id
    obj = get_object_or_404(diet_detail, id = id)
 
    # pass the object as instance in form
    form = dietform1(request.POST or None, instance = obj)

    
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        print('here')
        type=request.POST.get('type')
        regio=request.POST.get('regio')
        t_periods=request.POST.get('t_periods')
        disease=request.POST.get('disease')
    
        #res=diet_detail.objects.values_list('protei', flat=True).order_by('protei').filter(disease__contains=diseases,type=food_habbit)
        form.save()
        return redirect('diet_csv1')
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "diet_plan/updatedetail.html", context)

@login_required
def diet_csv1(request):
    defa=diet_detail.objects.all()
    return render(request, "diet_plan/detail.html", {'d':defa})

@login_required
def otherdiet(request,id):
    l=memo.objects.filter(d=1)
    print(l)
    a=int(l[0].sr)
    b=float(l[0].mi)
    c=float(l[0].ac)
    d=float(l[0].pr)


    data=memo1.objects.filter(d=1)
    data1=memo2.objects.filter(d=1)
    data2=memo3.objects.filter(d=1)

    gen= data[0].gen
    age= data[0].age
    height= data[0].height
    weight= data[0].weight
    bodyfat= data[0].bodyfat
    bodyphy= data[0].bodyphy
    exercise= data[0].exercise
    activity= data[0].activity
    blood_pressure= data[0].blood_pressure
    sugar= data[0].sugar
    blood_group= data[0].blood_group
    food_habbit= data[0].food_habbit
    food_preference= data[0].food_preference
    disability= data[0].disability
    medical_issues= data[0].medical_issues
    diseases= data[0].diseases

    bmi=data1[0].bmi
    lean_body_mass=data1[0].lean_body_mass
    basal_metabolic_rate=data1[0].basal_metabolic_rate
    maintaince=data1[0].maintaince
    lean_bmi=data1[0].lean_bmi

    protein_in_gr=data2[0].protein_in_gr
    carbs_in_gr=data2[0].carbs_in_gr
    fat_in_gr=data2[0].fat_in_gr

    data={'gen':gen,'age':age,'height':height,'weight':weight,'bodyfat':0,'bodyphy':bodyphy,
          'exercise':exercise,'activity':activity,'blood_pressure':blood_pressure,'sugar':sugar,
          'blood_group':blood_group,'food_habbit':food_habbit,'food_preference':food_preference,'disability':disability,
          'medical_issues':medical_issues,'diseases':diseases}

    data1={'bmi':bmi,'lean_body_mass':lean_body_mass,'basal_metabolic_rate':basal_metabolic_rate,'maintaince':maintaince,'lean_bmi':lean_bmi}

    data2={'protein_in_gr':protein_in_gr,'carbs_in_gr':carbs_in_gr,'fat_in_gr':fat_in_gr}

    if activity=='Sedentary':
        reqs={'energy':(2320/60)*weight,'fat':(25/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Lightly Active':
        reqs={'energy':(2520/60)*weight,'fat':(27.5/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Moderately Active':
        reqs={'energy':(2730/60)*weight,'fat':(30/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}
    elif activity=='Intence Weight training/sports'or "Very Active" or "Extra Active":
        reqs={'energy':(3490/60)*weight,'fat':(40/60)*weight,'pro':d,'water':weight*0.033,'VitA':6*weight,'VitC':0,'VitD':0,'Sodium':0,'Iro':0.2833*weight,'Potassium':0, 'Calcium':6*weight, 'Magnesium':5.6666*weight, 'Zinc':0.2*weight, 'Phosphorus':0}

    try:
        diet1=diet.objects.filter(diet_sr=id)
        ret=diet_detail.objects.filter(diet_sr=id)
        #reqs={'energy':b,'fat':c,'pro':d}

    except IndexError:
        diet1=[]
    print(reqs,ret[0].Kcal)
    #print(ret[0].diet_sr)
    #diet2=list(diet1)
    return render(request,"diet_plan/show.html",{'data': data, 'data1': data1,'data2':data2 , 'a': c, 'diet1':diet1, 'reqs':reqs,'give':ret[0]})