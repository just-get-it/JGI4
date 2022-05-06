from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order,CostingRate,Fabric,Measurments
from .forms import ProductForm,MeasurmentForm
# Create your views here.


def home(request):
    order=Order.objects.all()
    context={
        'objects':order
    }
    return render(request,'quick_costing/home.html',context)

def createOrder(request):
    productForm=ProductForm()
    if request.method=='POST':
        productForm=ProductForm(request.POST or None)
        if productForm.is_valid():
            prod = productForm.save(commit=False)
            # prod.cost=
            prod.save()
            slug = prod.slug
            print(slug)
            return redirect('quick_costing_measurments', slug)
    context = {
        'productform':productForm
    }
    return render(request,'quick_costing/create_order.html',context)

def measurments(request,slug):
    current_order = get_object_or_404(Order, slug=slug)
    current_order_quantity=current_order.quantity
    sizeandquantity=MeasurmentForm()
    if request.method=="POST":
        sizeandquantity=MeasurmentForm(request.POST or None)
        if sizeandquantity.is_valid():
            measurment=sizeandquantity.save(commit=False)
            measurment.order=current_order
            total_quantity=measurment.get_total_quantity()

            if total_quantity==current_order_quantity:
                measurment.save()
                return redirect('quick_costing_order_detail', slug)
            else:
                messages.warning(request,"Quantity is not equal ")
                return redirect('measurments',slug)

    context={
        'sizeAndQuantityForm':sizeandquantity,
        'object':current_order,
    }
    return render(request,'quick_costing/create_measurments.html',context)

def loadFabric(request):
    garment_id=request.GET.get('garment')
    fabrics=Fabric.objects.filter(garment_id=garment_id)
    return render(request, 'quick_costing/fabric_dropdown_list_options.html', {'fabrics': fabrics})


def orderDetail(request,slug):
    current_order=get_object_or_404(Order, slug=slug)
    sizeAndQuantity = Measurments.objects.get(order=current_order)
    plan_id=current_order.get_plan_id()
    quantity=current_order.quantity
    fabric_=current_order.fabric
    print(fabric_)
    print(quantity)
    print(plan_id)
    current_Costing_Rate=CostingRate.objects.get(fabric=fabric_,plan__pk=plan_id)
    # current_Costing_Rate=get_object_or_404(CostingRate,fabric=fabric_)

    context={
        'sizeAndQuantity': sizeAndQuantity,
        'object': current_order,
        'basic_cost':current_Costing_Rate.get_basic_cost_unit,
        'final_costing':current_Costing_Rate.get_final_costing,
        'business_value':current_Costing_Rate.get_business_value,

    }
    return render(request, 'quick_costing/order_detail.html', context)