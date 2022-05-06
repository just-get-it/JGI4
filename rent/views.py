import datetime
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import dates

from product.models import product
from .forms import StartDateAndEndDateForm,QuantitySizeColourForm
from .models import (RentOrder,
                     RentPlan,
                     RentingCost,
                     QuantitySizeColour,
                     QuantityAndDuration,
                     ProductInRentCart)


def rentProductListView(request):
    rent_product_list=product.objects.filter(is_rent=True)

    context={
        'objects':rent_product_list,
    }

    return render(request,'rent/rent_product_listView.html',context)

def rentProductDetailView(request,slug):
    rentProduct=product.objects.get(is_rent=True,slug=slug)
    date_form=StartDateAndEndDateForm()
    quantity_size_colour_form = QuantitySizeColourForm()
    if request.method == "POST":
        quantity_size_colour_form = QuantitySizeColourForm(request.POST or None)
        date_form = StartDateAndEndDateForm(request.POST or None)
        if quantity_size_colour_form.is_valid() and date_form.is_valid():
            form = quantity_size_colour_form.save(commit=False)
            start_date=date_form.cleaned_data['start_date']
            end_date=date_form.cleaned_data['end_date']

            try:
                quantity=date_form.cleaned_data['quantity']
            except:
                quantity=1

            form.save()
            current_product_in_rent_cart = ProductInRentCart.objects.create(rent_product=rentProduct,
                                                                            start_date=start_date,
                                                                            end_date=end_date)
            current_product_in_rent_cart.quantity_size_colour.add(form)
            number_of_days=current_product_in_rent_cart.get_days()
            if start_date < date.today():
                messages.warning(request, "Starting date must be from today onwards ..!")
                return redirect('rent_product_detail', slug)

            if end_date < date.today()+datetime.timedelta(days=3):
                messages.warning(request, "At least 3 days gap should be their")
                return redirect('rent_product_detail', slug)

            if end_date > date.today()+datetime.timedelta(days=12):
                messages.warning(request, "At Most 15 days gap should be their")
                return redirect('rent_product_detail', slug)

            #TODO Number days should be greater that 3

            # if number_of_days < datetime.timedelta(days=3):
            #     messages.warning(request,"Number Of Days Must be Greater than or equal to 3")
            #     return redirect('rent_product_detail',slug)

            orders=RentOrder.objects.filter(is_ordered=False)

            if orders.exists():
                for order in orders:
                    if(start_date==order.get_start_date() and end_date==order.get_end_date()):
                            suitable_order_id=order.id
                            suitable_order=RentOrder.objects.get(id=suitable_order_id)
                            suitable_order.rent_products.add(current_product_in_rent_cart)
                            suitable_order.add_start_and_end_date()

                            quantity_and_date = QuantityAndDuration.objects.filter(quantity=quantity)
                            # duration_acc_to_quantity =
                            if quantity_and_date.exists():
                                quantity_and_date_ = quantity_and_date[0]
                                duration_acc_to_quantity = quantity_and_date_.quantity


                            if suitable_order.get_selected_quantity()>=6:
                                suitable_order.end_date=suitable_order.start_date+datetime.timedelta(days=15)
                                messages.warning(request,"We increase number days according our terms and quantity ")
                            suitable_order.save()

                            return redirect('rent_order_DetailView', suitable_order_id)
                else:
                    # create new order
                    #TODO You have to think quantity field also
                    new_rent_order = RentOrder.objects.create()
                    new_rent_order.rent_products.add(current_product_in_rent_cart)
                    suitable_order_id = new_rent_order.id
                    new_rent_order.add_start_and_end_date()

                    if new_rent_order.get_selected_quantity() >= 6:
                        new_rent_order.end_date = new_rent_order.start_date + datetime.timedelta(days=15)
                        messages.warning(request,"We increase number days according our terms and quantity ")
                    new_rent_order.save()

                    return redirect('rent_order_DetailView', suitable_order_id)
            # create new order
            else:
                new_rent_order = RentOrder.objects.create()
                new_rent_order.rent_products.add(current_product_in_rent_cart)
                suitable_order_id=new_rent_order.id
                new_rent_order.add_start_and_end_date()

                if new_rent_order.get_selected_quantity() >= 6:
                    new_rent_order.end_date = new_rent_order.start_date + datetime.timedelta(days=15)
                    messages.warning(request,"We increase number days according our terms and quantity ")
                new_rent_order.save()

                return redirect('rent_order_DetailView',suitable_order_id)

    context={
        # 'size_colour_quantity':size_colour_quantity_of_main_product,
        'object':rentProduct,
        'form':QuantitySizeColourForm,
        'date_form':date_form,
        'todays_date':date.today(),
    }
    return render(request,'rent/rent_product_detail_view.html',context)


def rentOrders(request):
    rent_orders = RentOrder.objects.filter(is_ordered=False)
    context={
        'objects':rent_orders,
    }
    return render(request,'rent/rent_orderlistView.html',context)

def rentOrderDetailView(request,order_id):

    current_rent_order = RentOrder.objects.get(is_ordered=False,pk=order_id)
    selected_total_rent_products,selected_total_quantity=current_rent_order.get_selected_total_number_of_rent_products()

    plan_id = current_rent_order.get_plan_id()

    #Todo for is_Heavy product

    current_renting_cost = RentingCost.objects.get(plan__id=plan_id,is_heavy=False)
    total_rent_cost = current_renting_cost.total_rent_cost_per_quantity(current_rent_order.get_selected_quantity())
    base_rent_cost = current_renting_cost.total_rent_cost_per_quantity(1)
    context = {

        'object': current_rent_order,
        'total_rent_cost': total_rent_cost,
        'base_rent_cost': base_rent_cost,
        'selected_total_rent_products':selected_total_rent_products,
        'selected_total_quantity':selected_total_quantity,
    }

    return render(request,'rent/home.html',context)

def add_to_rent_cart(request,slug,order_id):
    current_product=product.objects.get(slug=slug)

    product_in_cart=ProductInRentCart.objects.filter(rent_product=current_product)
    product_in_carts = product_in_cart[0]
    rent_orders=RentOrder.objects.filter(is_ordered=False)
    if rent_orders.exists():
        rent_order=rent_orders[0]
        if rent_order.rent_products.filter(rent_product=current_product).exists():
            product_in_carts.quantity+=1
            product_in_carts.save()
            return redirect('rent_order_DetailView',order_id)
        else:
            rent_order.rent_products.add(product_in_carts)
            return redirect('rent_order_DetailView',order_id)
    else:
        rent_new_order=RentOrder.objects.create()
        rent_new_order.rent_products.add(product_in_carts)
        return redirect('rent_orders')