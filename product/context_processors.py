from django.shortcuts import get_object_or_404
from product.models import category, sub_category, super_category
import re
import io
import base64
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from product.models import *
from homepage.models import homepage_crousel, discount_corousel1, discount_corousel2, address
from userdetail.models import *
from cart.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
import random





def add_variable_to_context(request):
    #   For the supermarket :- subcategory display in the navbar
    market = ""
    electronic=""
    brand=""
    store=""
    product_quan = product.objects.all()
    marketid = []
    product_market_id = []
    product_market_name = []
    for item in product_quan:
        x = item.product_Category.all()
       
        for i in x:
            print("hello  ",i.id)
            if i not in product_market_id:
                product_market_id.append(i.id)
    for i in product_market_id:
        pro_name = category.objects.filter(id=i).values('name')[0]['name']
        if pro_name == 'Supermarket':
            marketid.append(i)
            market = (product.objects.filter(
                product_Category=i).distinct('product_Subcategory'))

        elif(pro_name == 'Electronics'):
            electronic = (product.objects.filter(
                product_Category=i).distinct('product_Subcategory'))

    store = product.objects.order_by().distinct('product_Category')
    brand = product.objects.order_by().distinct('brand')

    # context = {'market': market, 'electronic': electronic, 'brand':brand, 'store': store}        
    return {'market': market, 'electronic': electronic, 'brand':brand, 'store': store}