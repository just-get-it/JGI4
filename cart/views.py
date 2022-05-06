from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.conf import settings
from userdetail.models import *
# def cart(request):
#     return render(request, 'cart/cart.html')
# def delete_product(request):
# 	product_id=request.GET.get('id')
# 	productorder.objects.filter(id=product_id).all().delete()
# 	return redirect('cart')
# def delete_service(request):
# 	service_id=request.GET.get('id')
# 	serviceorder.objects.filter(id=service_id).all().delete()
# 	return redirect('cart')
# def delete_pick(request):
# 	pick_id=request.GET.get('id')
# 	pick_and_deliver_order.objects.filter(id=pick_id).all().delete()
# 	return redirect('cart')