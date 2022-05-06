

from __future__ import print_function
from io import BytesIO
from django.shortcuts import get_object_or_404
from filter.models import filter_Categories,filter_Objects
from product.models import category, sub_category, super_category
import pyzbar.pyzbar as pyzbar
import numpy as np
from PIL import Image
import re
import io
import base64
import json
from django.shortcuts import render, redirect
from math import ceil
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from django.template.loader import get_template
from django.db.models import Q, Max
from product.models import *
from homepage.models import *
from xhtml2pdf import pisa
from userdetail.models import *
from cartnew.models import *

from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
import json
import razorpay
from django.utils import timezone
from itertools import groupby
from itertools import chain
import random
import datetime

client = razorpay.Client(
    auth=("rzp_live_ditQLxTKtYPFdI", "StJvU3tFjtD6Eg7Uhz2QxhW4"))


def index(request):
    user = ''
    objs = product_cate_b2b.objects.filter(show_on_homepage=True)
    items = []


    # new_prod = product.objects.filter(product_Category)
    # print(new_prod)
    product_quan = product.objects.all()
    # all_product =product.objects.all()

    test_new = product.objects.all()
    print("etst ", test_new)

    n = len(test_new)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))



    testt = []
    for cate in test_new:
        products = product.objects.all()
        random_product = random.choice(products)
        print("rp = ",random_product)
        testt.append(random_product.slug)
    print("testt ",testt)
    final_t = product.objects.none()
    for t in testt:
        final_t |= product.objects.filter(slug=t)

    # test_new = final_t
    print("ft= ",final_t)
    

    #product_name=[x.product_Supercategory for x in product_quan]
    product_id = []
    product_sub = []

    for i in product_quan:
        print("i= ",i)
        x = i.product_Supercategory.all()
        for j in x:
            if j.id not in product_id:
                product_id.append(j.id)
    for i in product_quan:
        x = i.product_Subcategory.all()
        for j in x:
            if j.id not in product_sub:
                product_sub.append(j.id)

    product_name = []
    product_sub_name = []
    for i in product_id:
        pro_name = super_category.objects.filter(
            id=i).values('name')[0]['name']
        product_name.append(pro_name)
    for i in product_sub:
        pro_name = sub_category.objects.filter(id=i).values('name')[0]['name']
        product_sub_name.append(pro_name)

    products_stack = []
    cate = [x.name for x in objs]
    # print(cate)
    # print(objs)
    for i in objs:
        sin_objs = product.objects.filter(product_cate=i)[:6]

        if len(sin_objs) > 0:
            products_stack.append(sin_objs)

    home_crousel = homepage_crousel.objects.filter(active=True)
    n1 = len(home_crousel)

    dis_crou1 = discount_corousel1.objects.filter(active=True)
    dis_crou2 = discount_corousel2.objects.filter(active=True)

    # if request.user.is_authenticated:
    #     customer = request.user.email
    #     user = customer
    #     if not Customer.objects.filter(email=customer).exists():
    #         a = Customer(name=customer, email=customer)
    #         a.save()
    #     cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
    #     order, created = Order.objects.get_or_create(
    #         customer_id=cus_id, complete=False)
    #     '''if not Order.objects.filter(customer_id=cus_id).exists():
    #         b=Order(customer_id=cus_id,complete=False)
    #         b.save()'''
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    #     email = request.user.email
    #     carts, created = CartItems.objects.get_or_create(
    #         email=request.user.email)
    #     if created:
    #         CartItems.objects.filter(email=email).update(items=cartItems)
    #     else:
    #         CartItems.objects.filter(email=email).update(items=cartItems)

    # else:
    #     user = ''

    #     order = {'get_cart_total': 0, 'get_cart_items': 0}
    #     cartItems = order['get_cart_items']
    # print("homeprodlist:")
    cartItems = None
    print(products_stack)
    context = {"prod": zip(products_stack, cate), "home_crou": home_crousel, 'dis_crou1': dis_crou1, 'dis_crou2': dis_crou2, 'cartItems': cartItems, 'user': user,
               'product_name': product_name, 'product_sub_name': product_sub_name, 'test_new': test_new ,'no_of_slides':nSlides, 'range': range(1,nSlides),'product': test_new,'range1': range(1,n1),}
    return render(request, "index.html", context ,)


MERCHANT_KEY = 'ewNvWo7IsK3#qZSA'
tmp = 1
@csrf_exempt
def checkout(request):
    hint = message.objects.filter(location='Checkout')[0]
    if request.method == "POST" and 'razorbutton' in request.POST:
        items_json = request.POST.get('itemsJson', '')
        # '' is default value
        name = request.POST.get('name', '')
        # '' is default value
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        instructions = request.POST.get('instructions', '')
        additional_items = request.POST.get('additional_items', '')

        doneorder = True

        context = {}
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'Bommanahalli, Bangalore'}

        amount = max(tmp, int(amount))
        response = client.order.create(
            dict(amount=int(amount)*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']

        if order_status == 'created':

            # Server data for user convinience
            context['product_id'] = product
            context['price'] = int(amount)
            context['name'] = name
            context['phone'] = phone
            context['email'] = email
            context['address'] = address
            context['city'] = city
            context['instructions'] = instructions
            context['additional_items'] = additional_items
            context['hint_message'] = hint
            request.session['name'] = name
            request.session['phone'] = phone
            request.session['email'] = email
            request.session['address'] = address
            request.session['city'] = city

            # data that'll be send to the razorpay for
            context['order_id'] = order_id
            order = Orders(items_json=items_json, name=name, email=email, phone=phone,
                           address=address, city=city, state=state, zip_code=zip_code,
                           instructions=instructions, additional_items=additional_items, amount=amount, payment_method="razorpay")  # name(database)=name(variable here)
            order.save()
            hist = history(ordertype="Order",
                           order_id=order.order_id, email=email)
            hist.save()
            if request.user.is_authenticated:
                return render(request, 'checkout/confirm_order.html', context)
            else:
                context = {'cart': True}
                return render(request, 'userdetail/login.html', context)
        else:
            context = {'cart': True}
            return render(request, 'userdetail/login.html', context)

    elif request.method == "POST" and 'paytmbutton' in request.POST:
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')  # '' is default value
        amount = request.POST.get('amount', '')  # '' is default value
        print("amot:", amount)
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')

        order = Orders(items_json=items_json, name=name, email=email, phone=phone,
                       address=address, city=city, state=state, zip_code=zip_code,
                       instructions=instructions, additional_items=additional_items, amount=amount, payment_method="paytm")  # name(database)=name(variable here)
        order.save()
        hist = history(ordertype="Order", order_id=order.order_id, email=email)
        hist.save()
        doneorder = True
        id = order.order_id
        host = "http://"+request.META['HTTP_HOST']+"/handlerequest/"

        param_dict = {
            'MID': 'LaxLMj03444256041341',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': host,  # payment successfull msg by paytm
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        if request.user.is_authenticated:
            return render(request, 'checkout/paytm.html', {'param_dict': param_dict})
        else:
            context = {'cart': True}
            return render(request, 'userdetail/login.html', context)

    elif request.method == "POST" and 'cod' in request.POST:
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')  # '' is default value
        amount = request.POST.get('amount', '')  # '' is default value
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        instructions = request.POST.get('instructions', '')
        additional_items = request.POST.get('additional_items', '')
        context = {}

        context['price'] = int(amount)

        context['name'] = name
        context['phone'] = phone
        context['email'] = email
        context['address'] = address
        context['city'] = city
        context['state'] = state
        context['zip_code'] = zip_code
        context['instructions'] = instructions
        context['additional_items'] = additional_items
        context['hint_message'] = hint
        order = Orders(items_json=items_json, name=name, email=email, phone=phone,
                       address=address, city=city, state=state, zip_code=zip_code,
                       instructions=instructions, additional_items=additional_items, amount=amount, payment_method="cod")
        order.save()
        hist = history(ordertype="Order", order_id=order.order_id, email=email)
        hist.save()
        if request.user.is_authenticated:
            return render(request, 'checkout/cod_confirm.html', context)
        else:
            context = {'cart': True}
            return render(request, 'userdetail/login.html', context)

        # return render(request, 'paytm.html', {'param_dict': param_dict})
    if request.user.is_authenticated:
        customer = request.user.email

        user = detail.objects.filter(email=customer)

        cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
        order, created = Order.objects.get_or_create(
            customer_id=cus_id, complete=False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_items
    else:
        context = {'cart': True}
        return render(request, 'userdetail/login.html', context)
    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'user': user, 'hint_message' : hint}
    return render(request, 'checkout/checkout.html', context)


MERCHANT_KEY = 'ewNvWo7IsK3#qZSA'


def checkoutquick(request):
    hint = message.objects.filter(location='Checkout')[0]
    if request.method == "POST" and 'razorbutton' in request.POST:
        items_json = request.POST.get('itemsJson', '')
        # '' is default value
        name = request.POST.get('name', '')
        # '' is default value
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        instructions = request.POST.get('instructions', '')
        additional_items = request.POST.get('additional_items', '')
        doneorder = True
        context = {}
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'Bommanahalli, Bangalore'}
        response = client.order.create(
            dict(amount=int(amount)*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']

        if order_status == 'created':

            # Server data for user convinience
            # context['product_id'] = product
            context['price'] = int(amount)
            print("amount:::", amount)
            context['name'] = name
            context['phone'] = phone
            context['email'] = email
            context['address'] = address
            context['instructions'] = instructions
            context['additional_items'] = additional_items
            context['hint_message'] = hint

            # data that'll be send to the razorpay for
            context['order_id'] = order_id
            order = Orders(items_json=items_json, name=name, email=email, phone=phone,
                           address=address, city=city, state=state, zip_code=zip_code,
                           instructions=instructions, additional_items=additional_items, amount=amount, payment_method="razorpay")  # name(database)=name(variable here)
            order.save()
            hist = history(ordertype="Order",
                           order_id=order.order_id, email=email)
            hist.save()
            if request.user.is_authenticated:
                return render(request, 'confirm_order.html', context)
            else:
                return redirect('login_page')

    elif request.method == "POST" and 'paytmbutton' in request.POST:
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')  # '' is default value
        amount = request.POST.get('amount', '')  # '' is default value
        print("amot:", amount)
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        instructions = request.POST.get('instruction', '')
        additional_items = request.POST.get('additional_items', '')        
        order = Orders(items_json=items_json, name=name, email=email, phone=phone,
                       address=address, city=city, state=state, zip_code=zip_code,
                       instructions=instructions, additional_items=additional_items, amount=amount, payment_method="paytm")  # name(database)=name(variable here)
        order.save()
        hist = history(ordertype="Order", order_id=order.order_id, email=email)
        hist.save()
        doneorder = True
        id = order.order_id
        host = "http://"+request.META['HTTP_HOST']+"/handlerequest/"

        param_dict = {
            'MID': 'LaxLMj03444256041341',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': host,  # payment successfull msg by paytm
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        if request.user.is_authenticated:
            return render(request, 'paytm.html', {'param_dict': param_dict})
        else:
            return redirect('login_page')

        # return render(request, 'paytm.html', {'param_dict': param_dict})
    if request.user.is_authenticated:
        customer = request.user.email

        user = detail.objects.filter(email=customer)
        '''print("customer:", len(user))
        cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
        order, created = Order.objects.get_or_create(customer_id=cus_id, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        print("items:",items)'''
        product = productorder.objects.filter(
            customer_id=request.user.email).all()
        product_count = productorder.objects.filter(
            customer_id=request.user.email).count()
        service = serviceorder.objects.filter(
            customer_id=request.user.email).all()
        service_count = serviceorder.objects.filter(
            customer_id=request.user.email).count()
        pick = pick_and_deliver_order.objects.filter(
            customer_id=request.user.email).all()
        pick_count = pick_and_deliver_order.objects.filter(
            customer_id=request.user.email).count()
        price_lt, quantity_lt = [], []
        for i in product:
            price_lt.append(i.price)
            quantity_lt.append(i.no_of_quantity)
        sums = 0
        for (a, b) in zip(price_lt, quantity_lt):
            total = a*b
            sums = total+sums
        context = {'user': user, 'product': product, 'service': service, 'product_count': product_count,
                   'service_count': service_count, 'pick': pick, 'pick_count': pick_count, 'sums': sums}
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        user = ''
        context = {'items': items, 'order': order,
                   'cartItems': cartItems, 'user': user}
    return render(request, 'checkout_quick.html', context)


def payment_status(request):
    response = request.POST
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')
    params_dict = {
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_signature': razorpay_signature,
    }
    subs = request.POST.get('subs')
    if subs is not None:
        import json
        # subscription checkout:
        items_json = request.POST.get('items_json')
        print('////////////////////////////////////////////')
        print(items_json)
        if type(items_json) is str:
            import ast
            items_json = ast.literal_eval(items_json) 

        totalAmount = 0
        if type(items_json) is dict:
            for key, values in items_json.items():
                totalAmount += values['amount']
        print('**************************************')
        print(totalAmount)
        context = {}
        context['maps'] = items_json
        context['totalPrice'] = totalAmount
        context['todayDate'] = datetime.date.today()
        context['name'] = request.session['name']
        context['phone'] = request.session['phone']
        context['email'] = request.session['email']
        context['address'] = request.session['address']
        context['city'] = request.session['city']

        comp_details = address.objects.get(default=True)
        context['comp_name'] = comp_details.name
        context['comp_email'] = comp_details.email
        context['comp_mob'] = comp_details.mob
        context['comp_add'] = comp_details.address_of_website
        
        try:
            status = client.utility.verify_payment_signature(params_dict)
            params_dict['status'] = 'Payment Successful'
            return render(request, 'checkout/subscriptionConfirm.html', {'maps': items_json, 'context': context})
        except:
            params_dict['status'] = 'Payment Failure'
            return render(request, 'checkout/razorpaymentstatus.html', {'response': params_dict})
    customer = request.user.email
    cus_id = detail.objects.filter(email=customer).values('id')[0]['id']
    order = Order.objects.filter(customer_id=cus_id, complete=False).last()
    # print("order:",order)
    items = order.orderitem_set.all()
    sell_price_lt = []
    product_total_lt = []
    for i in items:
        gst = i.get_price * float(i.product.gst/100)
        sell_price = i.get_price - gst
        sell_price_lt.append((sell_price))
        product_total_lt.append(i.get_price * i.quantity)
    final_amt = sum(product_total_lt)

    item_n_sell_n_prodtot = zip(items, sell_price_lt, product_total_lt)

    context = {}
    context['name'] = request.session['name']
    context['phone'] = request.session['phone']
    context['email'] = request.session['email']
    context['address'] = request.session['address']
    context['city'] = request.session['city']
    

    del request.session['name']
    del request.session['phone']
    del request.session['email']
    del request.session['address']
    del request.session['city']

    comp_details = address.objects.get(default=True)
    context['comp_name'] = comp_details.name
    context['comp_email'] = comp_details.email
    context['comp_mob'] = comp_details.mob
    context['comp_add'] = comp_details.address_of_website
    context['comp_gstin'] = comp_details.gstin

    try:
        status = client.utility.verify_payment_signature(params_dict)
        params_dict['status'] = 'Payment Successful'
        return render(request, 'checkout/razorpaymentstatus.html', {'response': params_dict, 'item_n_sell_n_prodtot': item_n_sell_n_prodtot, 'final_amt': final_amt, 'context': context})
    except:
        params_dict['status'] = 'Payment Failure'
        return render(request, 'checkout/razorpaymentstatus.html', {'response': params_dict})


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    checksum = ""
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    # print("form; ",form)

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            # print(response_dict['RESPCODE'])
        else:
            print('order was not successful because ' +
                  response_dict['RESPMSG'])
            # print(response_dict['RESPCODE'])
    return render(request, 'checkout/paymentstatus.html', {'response': response_dict})


def cart(request):
    if request.user.is_authenticated:
        print("runninggggggg")
        ''' Activate below code for 1 time only '''
        # reset quantity and price:
        # allSubscriptions = Subscription_Order.objects.filter(customer_email=request.user)
        # for subscription in allSubscriptions:
        #     product_slug = subscription.product_slug
        #     product_instance = product.objects.filter(slug=product_slug).first()
        #     product_price = product_instance.price
            
        #     subscription.amount = product_price
        #     subscription.quantity = 1

        #     subscription.save(update_fields=['quantity', 'amount'])

        currUser = detail.objects.filter(email=request.user.email).first()
        cus_id = currUser.id
        order, created = Order.objects.get_or_create(
            customer_id=cus_id, complete=False, is_Cancelled=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        products = productorder.objects.filter(
            customer_id=request.user.email).all()
        product_count = productorder.objects.filter(
            customer_id=request.user.email).count()
        service = serviceorder.objects.filter(
            customer_id=request.user.email).all()
        service_count = serviceorder.objects.filter(
            customer_id=request.user.email).count()
        pick = pick_and_deliver_order.objects.filter(
            customer_id=request.user.email).all()
        pick_count = pick_and_deliver_order.objects.filter(
            customer_id=request.user.email).count()
        price_lt, quantity_lt, gst_lt = [], [], []
        product_exist, service_exist, pick_exist = False, False, False
        if productorder.objects.filter(customer_id=request.user.email).exists():
            product_exist = True
        if serviceorder.objects.filter(customer_id=request.user.email).exists():
            service_exist = True
        if pick_and_deliver_order.objects.filter(customer_id=request.user.email).exists():
            pick_exist = True

        for i in zip(products, items):
            price_lt.append(i.get_price)
            quantity_lt.append(i.no_of_quantity)
        sums = 0
        # gst=0
        for (a, b,) in zip(price_lt, quantity_lt):
            total = a*b
            sums = total+sums
        servicetotal = 0
        import re

        if service_exist == True:
            for i in service:
                price = int(re.findall(r'\d+', i.price_range)[0])
                servicetotal = servicetotal + price

        items = items.order_by('id')
        ############## Subscribe cart ===> Unpaid Subscription ##############
        unpaidSubscriptions = Subscription_Order.objects.filter(customer_email = request.user, isPaid = False)
        unpaidSubscriptionMapping = {}
        subscriptionCartAmount = 0
        numItemsInSubscriptionCart = len(unpaidSubscriptions)
        print('///////////////////////////////////////')
        print(numItemsInSubscriptionCart)
        if len(unpaidSubscriptions) != 0:
            for subscription in unpaidSubscriptions:
                transaction_id = subscription.transaction_id
                product_name = subscription.product_name
                quantity = subscription.quantity
                amount = subscription.amount
                start_date = subscription.start_date
                end_date = subscription.end_date
                shift = subscription.shifts
                remark = subscription.remark
                transaction_id = subscription.transaction_id
                interval = subscription.interval
                slug = subscription.product_slug
                # extracting image of a product
                slug = subscription.product_slug
                product_instance = product.objects.filter(slug=slug).first()
                product_price = product_instance.price
                unpaidSubscriptionMapping[transaction_id] = {
                    'product_name': product_name,
                    'product_image': product_instance.image1,
                    'price': product_price,
                    'amount': amount,
                    'quantity': quantity,
                    'start_date': start_date,
                    'end_date': end_date,
                    'shift': shift,
                    'remark': remark,
                    'transaction_id': transaction_id,
                    'interval': interval,
                    'slug': slug
                }
                subscriptionCartAmount += amount
            areThereUnpaidSubscriptions = True
        else:
            areThereUnpaidSubscriptions = False

        ### subscriptions
        allSubscriptions = Subscription_Order.objects.filter(customer_email = request.user, isPaid=True)
        subscriptionAmount = 0
        subscriptionMapping = {}
        areThereSubscriptions = True
        if len(allSubscriptions) != 0:
            for subscription in allSubscriptions:
                transaction_id = subscription.transaction_id
                product_name = subscription.product_name
                quantity = subscription.quantity
                amount = subscription.amount
                start_date = subscription.start_date
                end_date = subscription.end_date
                # extracting image of a product
                slug = subscription.product_slug
                product_instance = product.objects.filter(slug=slug).first()
                product_price = product_instance.price
                subscriptionMapping[transaction_id] = {
                    'product_name': product_name,
                    'product_image': product_instance.image1,
                    'price': product_price,
                    'amount': amount,
                    'quantity': quantity,
                    'start_date': start_date,
                    'end_date': end_date,
                }
                subscriptionAmount += amount
            areThereSubscriptions = True
        else:
            areThereSubscriptions = False

        # wallet amount
        obj = history.objects.filter(email=request.user.email)
        totalamount = 0
        for it in obj:
            if it.ordertype == "Add" or it.ordertype == "Recieved":
                totalamount += it.total_amount
            elif it.ordertype == "Send":
                totalamount -= it.total_amount

        # get the total amount for each subscription to be paid get all the subcriptions
        from cal.models import Event
        totalSubscriptionAmount = 0
        todays_date = datetime.date.today()
        for subscription in allSubscriptions:
            transaction_id = subscription.transaction_id
            print(transaction_id)
            # extract all last unpaid events of this transaction_id
            unpaidEvents = Event.objects.filter(sub_transaction_id=transaction_id, isPaidForEvent = False, start_time__lte = todays_date, isStopped=False)
            lastPaymentEvent = Event.objects.filter(sub_transaction_id=transaction_id, isPaidForEvent=True).order_by('-start_time').first()
            subscriptionMapping[transaction_id]['lastPaymentDate'] = lastPaymentEvent.start_time
            
            date_difference = (todays_date - lastPaymentEvent.start_time).days
            if date_difference >= 30:
                subscriptionMapping[transaction_id]['show_warning'] = True
                if date_difference < 40:
                    subscriptionMapping[transaction_id]['message'] = f'Pay within {40 - date_difference} to continue your subscription else your subscription will be halted unless the amount is paid'
                else:
                    subscriptionMapping[transaction_id]['message'] = f'Your subscription is stopped, pay to continue'
                    # check if it is already stopped or not.
                    last_stop = Subscription_Stop.objects.filter(user=request.user, transaction_id=transaction_id, end_date='9999-12-31')
                    print(last_stop)
                    if len(last_stop) == 0:
                        # it is not stopped yet so add a stop
                        Subscription_Stop(user=request.user, transaction_id=transaction_id).save()
                        from userdetail.utils import updateEvent
                        subscription_instance = Subscription_Order.objects.filter(transaction_id=transaction_id, customer_email=request.user)
                        updateEvent(subscription_instance, False, False, False)

            numberOfUnpaidEvents = len(unpaidEvents)
            priceOfOneEvent = subscription.amount
            subscriptionMapping[transaction_id]['amountOfUnpaidEvents'] = numberOfUnpaidEvents * priceOfOneEvent
            
            totalSubscriptionAmount += numberOfUnpaidEvents * priceOfOneEvent
           
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'product': products, 'service': service,
                   'product_count': product_count,
                   'service_count': service_count, 'pick': pick, 'pick_count': pick_count, 'sums': sums, 'servicetotal': servicetotal,
                   'product_exist': product_exist, 'service_exist': service_exist, 'pick_exist': pick_exist,
                   'areThereSubscriptions': areThereSubscriptions,
                   'subscriptionMapping': subscriptionMapping,
                   'numItemsInSubscriptionCart':numItemsInSubscriptionCart,
                   'areThereUnpaidSubscriptions': areThereUnpaidSubscriptions,
                   'unpaidSubscriptionMapping': unpaidSubscriptionMapping,
                   'subscriptionCartAmount': subscriptionCartAmount,
                   'totalamount': totalamount,
                   'totalSubscriptionAmount': totalSubscriptionAmount}
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        context = {'items': items, 'order': order, 'cartItems': cartItems
                   }
    return render(request, 'cart.html', context)

def deleteSubscribeCart(request):
    '''
        Delete Subscription from cart.
    '''
    transaction_id = request.POST.get('transaction_id')
    instance = Subscription_Order.objects.filter(transaction_id = transaction_id, isPaid = False)
    instance.delete()
    data = {
        'msg': 'success',
        'transaction_id': transaction_id
    }
    return JsonResponse(data)

def editSubscription(request, slug):
    """
        For Subscription editing
        models used: userdetail.models.Subscription_Order, product.model.product
    """
    # extracting subscription details
    sub = Subscription_Order.objects.filter(transaction_id = slug).first()
    product_slug = sub.product_slug
    product_name = sub.product_name
    sub_interval = sub.interval
    stop_next = sub.stop_next
    shifts = sub.shifts
    start_date = sub.start_date
    end_date = sub.end_date
    quantity = sub.quantity
    remark = sub.remark

    vendor_email = sub.vendor_email
    amount = sub.amount
    username = request.user.username

    # extracting product details
    product_instance = product.objects.filter(slug = product_slug).first()
    product_image = product_instance.image1
    base_price = product_instance.price
    unit_of_measurement = product_instance.unit_of_measurement
    

    # extracting today's date
    # if today's date > start_date ===> Donot allow to edit start_date
    cannot_edit_start_date = False
    today_date = datetime.date.today()
    if today_date >= start_date:
        cannot_edit_start_date = True
    data = {
        'transaction_id': slug,
        'product_name': product_name,
        'frequency': frequency,
        'sub_interval': sub_interval,
        'stop_next': stop_next,
        'start_date': start_date,
        'end_date': end_date,
        'quantity': quantity,
        'image': product_image,
        'remark': remark,
        'product_slug': product_slug,
        'unit_of_measurement': unit_of_measurement,
        'cannot_edit_start_date': cannot_edit_start_date,
        'today_date': today_date,
        'shifts': shifts,
        'vendor_email': vendor_email,
        'username': username,
        'base_price': base_price,
        'amount': amount
    }

    return render(request, 'editSubscription.html', context = data)

def updateItems(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    customer = request.user.email
    productitem = product.objects.get(product_code=productId)

    # print('prod:',productitem)
    cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
    order, created = Order.objects.get_or_create(
        customer_id=cus_id, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=productitem)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    cartItems = order.get_cart_items
    carts, created = CartItems.objects.get_or_create(email=request.user.email)
    if created:

        CartItems.objects.filter(
            email=request.user.email).update(items=cartItems)
    else:
        CartItems.objects.filter(
            email=request.user.email).update(items=cartItems)

    return JsonResponse('Item added', safe=False)


def getinvoice(request):
    hint = message.objects.filter(location='Checkout')[0]
    name = request.GET.get('name', '')  # '' is default value
    email = request.GET.get('email', '')
    phone = request.GET.get('phone', '')
    cust_address = request.GET.get('address', '')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')
    zip_code = request.GET.get('zip_code', '')
    instructions = request.GET.get('instructions', '')
    additional_items = request.GET.get('additional_items', '')
    instructions = '\n'.join(instructions.split(','))
    additional_items = '\n'.join(additional_items.split(','))
    # print("namee:",city)
    thank = True

    context = {}

    context['name'] = name
    context['phone'] = phone
    context['email'] = email
    context['address'] = cust_address
    context['city'] = city
    context['state'] = state
    context['zip_code'] = zip_code
    context['instructions'] = instructions
    context['additional_items'] = additional_items
    context['hint_message'] = hint
    customer = request.user.email

    cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
    order, created = Order.objects.get_or_create(
        customer_id=cus_id, complete=False)
    items = order.orderitem_set.all()
    sell_price_lt = []
    product_total_lt = []
    for i in items:
        gst = i.get_price * (i.product.gst / 100)
        sell_price = i.get_price - gst
        sell_price_lt.append((sell_price))
        product_total_lt.append(i.get_price * i.quantity)
    final_amt = sum(product_total_lt)

    item_n_sell_n_prodtot = zip(items, sell_price_lt, product_total_lt)

    comp_details = address.objects.get(default=True)
    context['comp_name'] = comp_details.name
    context['comp_email'] = comp_details.email
    context['comp_mob'] = comp_details.mob
    context['comp_add'] = comp_details.address_of_website
    context['comp_gstin'] = comp_details.gstin

    cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
    order, created = Order.objects.get_or_create(
        customer_id=cus_id, complete=False)
    return render(request, 'checkout/invoicedownload.html', {'context': context, 'item_n_sell_n_prodtot': item_n_sell_n_prodtot, 'order': order, 'final_amt': final_amt})


def setSession(request):
    request.session['session_data_1'] = "This is Session 1 Data"
    request.session['session_data_2'] = "This is Session 2 Data"
    return HttpResponse("Session Set")


def view_session(request):
    if request.session.has_key("session_data_1"):
        session_data_1 = request.session['session_data_1']
    else:
        session_data_1 = "Data is Blank"
    if request.session.has_key("session_data_2"):
        session_data_2 = request.session['session_data_2']
    else:
        session_data_2 = "Data is Blank"
    return render(request, "invoice/show_session_data.html", {"session_data_1": session_data_1, "session_data_2": session_data_2})


def del_session(request):
    del request.session['session_data_1']
    del request.session['session_data_2']
    return HttpResponse("Session Deleted")


def getPdfPage(request):
    hint = message.objects.filter(location='Checkout')[0]
    if request.user.is_authenticated:
        name = request.GET.get('name', '')  # '' is default value
        email = request.GET.get('email', '')
        phone = request.GET.get('phone', '')
        cust_address = request.GET.get('address', '')
        city = request.GET.get('city', '')
        state = request.GET.get('state', '')
        zip_code = request.GET.get('zip_code', '')
        instructions = request.GET.get('instructions', '')
        additional_items = request.GET.get('additional_items', '')
        a4 = request.GET.get('a4', '')
        thank = True
        context = {}

        context['name'] = name
        context['phone'] = phone
        context['email'] = email
        context['address'] = cust_address
        context['city'] = city
        context['state'] = state
        context['zip_code'] = zip_code
        context['instructions'] = instructions
        context['additional_items'] = additional_items
        context['hint_message'] = hint
        comp_detail = address.objects.get(default=True)

        context['comp_name'] = comp_detail.name
        context['comp_email'] = comp_detail.email
        context['comp_mob'] = comp_detail.mob
        context['comp_add'] = comp_detail.address_of_website
        context['comp_gstin'] = comp_detail.gstin

        customer = request.user.email
        cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
        order, created = Order.objects.get_or_create(
            customer_id=cus_id, complete=False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_items
        order.complete = True
        order.save()
        ship, created = ShippingAddress.objects.get_or_create(
            customer_id=cus_id, order=order)
        ship.address = cust_address
        ship.city = city
        ship.state = state
        ship.zipcode = zip_code
        ship.save()
        sell_price_lt = []
        product_total_lt = []
        for i in items:
            gst = i.get_price * (i.product.gst / 100)
            sell_price = i.get_price - gst
            sell_price_lt.append((sell_price))
            product_total_lt.append(i.get_price * i.quantity)
        final_amt = sum(product_total_lt)

        item_n_sell_n_prodtot = zip(items, sell_price_lt, product_total_lt)

        data = {'context': context, 'order': order, 'cartItems': cartItems,
                'item_n_sell_n_prodtot': item_n_sell_n_prodtot, 'final_amt': final_amt}  # 'items': items,
        if a4 == '1':
            template = get_template("invoice/pdf_page.html")
        else:
            template = get_template("invoice/pdf_page_small.html")
        data_p = template.render(data)
        response = BytesIO()
        pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)

        if not pdfPage.err:
            return HttpResponse(response.getvalue(), content_type="application/pdf")
        else:
            return HttpResponse("Error Generating PDF")


def myorder(request):
    customer = request.user.email
    # all_student = detail.objects.filter(email=customer)
    # all_student2 = Customer.objects.values('name')
    # print(all_student2)
    cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
    ship = ShippingAddress.objects.filter(customer_id=cus_id)
    # print(ship)
    order = Order.objects.filter(customer_id=cus_id, complete=True)
    # print(order)
    items = []
    ships = []
    for i in order:
        items.append(i.orderitem_set.all())
        ships.append(i.shippingaddress_set.all())
    # cartItems = order.get_cart_items
    print(items)
    # context = {'items': items}
    # context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout/myorder.html', {'context': zip(items, ships)})


def decode(url):
    # Find barcodes and QR codes

    imgstr = re.search(r'base64,(.*)', url).group(1)
    image_bytes = io.BytesIO(base64.b64decode(imgstr))
    im = Image.open(image_bytes)

    arr = np.array(im)[:, :, 0]
    decodedObjects = pyzbar.decode(arr)
    # print(decodedObjects)

    # return decodedObjects.Decoded
    # Print results
    data = []

    for obj in decodedObjects:
        # print('Type : ', obj.type)
        # print('Data : ', obj.data, '\n')
        data.append({
            "code": obj.data.decode('utf-8'),
            "type": obj.type
        })
        # return "Code: "+code.decode('utf-8') + "\nType: "+ types
    #data = serializers.serialize('json', data)
    # print(data)
    return data


def scan_qr(request):
    data = {

    }
    if request.POST.get('ajax_qr'):
        # print(request.POST.get('ajax_qr'))
        my_QR = decode(request.POST.get('ajax_qr'))
        # my_QR.decode()
        # print(my_QR)
        if my_QR:
            json_data = json.dumps(my_QR)
            print(json_data)
            return JsonResponse(json_data, safe=False)
        return JsonResponse({"code": 'NO BarCode Found'})

        # print(my_QR.data)
    return render(request, "home/scan_qr.html", data)


def label_home_page(request, label_tag):
    objs = get_object_or_404(labels_Object, name=label_tag)
    if objs.name == "B2B":
        return redirect("index")
    cate = category.objects.all()

    prod_dict = {}
    for c in cate:
        # print("-------"+c.name)
        sub_c_dict = {}
        for sc in sub_category.objects.filter(product_Category=c):
            print("**"+sc.name)
            filtered_prods = product.objects.filter(
                product_Category=c,
                product_Subcategory=sc,
                product_tags=objs).order_by("-trending_view")[:6]
            if filtered_prods:
                sub_c_dict[sc.name] = filtered_prods
        if sub_c_dict:
            prod_dict[c.name] = sub_c_dict
    print("dic-", prod_dict)

    products_stack = []
    home_crousel = None
    if objs:
        products_stack = []
        sin_objs = product.objects.filter(product_tags=objs)
        if len(sin_objs) > 0:
            products_stack.append(sin_objs)
        home_crousel = homepage_crousel.objects.filter(product_tag=objs).last()
        return render(request, "label_home_page.html", {"prod": products_stack, "home_crou": home_crousel, "prod_dict": prod_dict})
    else:
        return redirect('/')





def orderdetails(request, order_id):
    if request.user.is_authenticated:
        orders = Orders.objects.filter(order_id=order_id)
        # print(order.items_json.values())
        customer = request.user.email
        cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
        order, created = Order.objects.get_or_create(
            customer_id=cus_id, complete=False)
        items = order.orderitem_set.all()
        print(items)
        return render(request, "orders.html", {'orders': orders, 'items': items, 'id': order_id})


MERCHANT_KEY = 'ewNvWo7IsK3#qZSA'






def transactions(request, order_id):
    obj = history.objects.filter(
        order_id=order_id, email=request.user.email)[0]
    if obj.ordertype == "Add":
        details = add_wallet.objects.filter(
            order_id=order_id, email=request.user.email)
        return render(request, "wallet/transactions.html", {'add': details})
    if obj.ordertype == "Recieved":
        details = remove_wallet.objects.filter(
            order_id=order_id, reciever=request.user.email)
        return render(request, "wallet/transactions.html", {'recieve': details})
    if obj.ordertype == "Send":
        details = add_wallet.objects.filter(order_id=order_id)
        return render(request, "wallet/transactions.html", {'send': details})


def wishlists(request):
    if request.method == "POST":
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        if action == "add":
            wish = wishlist.objects.filter(
                email=request.user.email, product_code=productId)
            print(wish)
            if wish:
                print('exists')
                msg = {'exists': True}
                return JsonResponse(msg, safe=False)
            wishes = wishlist(email=request.user.email, product_code=productId)
            wishes.save()
        if action == "remove":
            wishes = wishlist.objects.filter(
                email=request.user.email, product_code=productId)
            wishes.delete()

        return JsonResponse('Item added', safe=False)

    elif request.user.is_authenticated:
        wishes = wishlist.objects.filter(email=request.user.email)
        prod = []
        # print(obj.product_code)
        for i in wishes:
            #print('in wishlist')
            prod_id = i.product_code
            obj = product.objects.filter(product_code=prod_id)[0]
            prod.append(obj)
        items = CartItems.objects.filter(
            email=request.user.email).values('items')[0]['items']
        return render(request, "wishlist.html", {'items': prod, 'cartItems': items})


def track_order(request):
    return render(request, "wallet/track_location.html")


def searchMatch_attr(query, item):
          # print('item :' , item)
    item['value'] = item['value'].strip()
    query = query.lower()
    if query in item['value'].lower():
        return True
    else:
        return False


def search(request):
    query = request.GET['query']
    print("query is : ", query)

    attributes_data = label_Attributes_Values.objects.values('value', 'prod')
    valuess = [item['prod'].strip()
               for item in attributes_data if searchMatch_attr(query, item)]
    # idss = {item['prod'].strip() for item in attributes_data}
    print('valuess : ', valuess)
    # print('idss : ', idss)
    allprods = []
    #If b2b user is logged in then only b2b products will be queried
    if request.user.is_authenticated and detail.objects.get(email=request.user.email).vendor == True:
        # productTemp = product.objects.filter(b2b_product=True) # B2BCHECKBOX
        b2bTag = labels_Object.objects.get(name='B2B')
        productTemp = product.objects.filter(product_tags = b2bTag)
    else:
        # productTemp = product.objects.filter(b2c_product=True) # B2CCHECKBOX
        b2cTag = labels_Object.objects.get(name='B2C')
        productTemp = product.objects.filter(product_tags = b2cTag)

    for ids in valuess:
        prodtemp = productTemp.filter(product_code__icontains=ids)
        allprods.append(prodtemp)

    print('Allprods :', allprods)
    # print("trial: " , trial)
    # products_match_attrib = label_Attributes_Values.objects.filter(value__icontains = query)
    # products_match_attributes = product.objects.filter(title__icontains = products_match_attrib)
    # print("attr: ", products_match_attrib)
    if query is not None and query != '':
        attr = attribute.objects.all()
        allProducts = productTemp.filter(Q(title__icontains=query) | Q(product_Category__name__icontains=query) | Q(
            product_Subcategory__name__icontains=query) | Q(product_Supercategory__name__icontains=query))
        print(allProducts)
        allProducts_match = []
        if allProducts.exists() or len(allprods) != 0:
            # title = allProducts[0].title

            if allProducts.exists():

                cate = allProducts[0].product_Category
                sub_cate = allProducts[0].product_Subcategory
                sup_cate = allProducts[0].product_Supercategory

                products_match_title = productTemp.filter(
                    Q(title__icontains=query))
                products_match_cate = productTemp.filter(
                    Q(product_Category__name__icontains=cate))
                products_match_subcate = productTemp.filter(
                    Q(product_Subcategory__name__icontains=sub_cate))
                products_match_supcate = productTemp.filter(
                    Q(product_Supercategory__name__icontains=sup_cate))

                allProducts_match = list((chain(products_match_title, products_match_supcate,
                                                products_match_cate, products_match_subcate)))

                for prods in allprods:
                    allProducts_match += prods

                allProducts_match = list(dict.fromkeys(allProducts_match))

                # allProducts_match = products_match_cate | products_match_subcate | products_match_supcate

                # allProducts_match = (products_match_title | allProducts_match).distinct()

                # allProducts_match = list(allProducts_match).distinct()
                # allProducts_match = products_match_title | products_match_cate | products_match_subcate | products_match_supcate
                print('Title: ', products_match_title)
                print('All', allProducts_match)

                print(cate)
                print(sub_cate)
                print(sup_cate)
                # allProducts = product.objects.all()
                # allProducts = product.objects.annotate(
                # 	search=SearchVector('title', 'product_Category__name')).filter(search=query)
            else:
                print('hello', allprods)
                for prods in allprods:
                    allProducts_match += prods
                    allProducts_match = list(dict.fromkeys(allProducts_match))

            is_user_vendor = False
            if request.user.is_authenticated and detail.objects.get(email=request.user.email).vendor == True:
                is_user_vendor = True
            params = {'allProducts': allProducts_match, 'is_user_vendor': is_user_vendor}
            print(len(allProducts))

            return render(request, 'search/search.html', params)

        else:
            return HttpResponse('No products found')

    else:
        user = ''
        objs = product_cate_b2b.objects.filter(show_on_homepage=True)
        items = []

        # new_prod = product.objects.filter(product_Category)
        # print(new_prod)
        product_quan = product.objects.all()
        # all_product =product.objects.all()

        test_new = product.objects.order_by().distinct('product_Category')
        print(test_new)

        # print(all_product)

        #product_name=[x.product_Supercategory for x in product_quan]
        product_id = []
        product_sub = []

        for i in product_quan:
            x = i.product_Supercategory_id

            if x not in product_id:
                product_id.append(x)
        for i in product_quan:
            x = i.product_Subcategory_id

            if x not in product_sub:
                product_sub.append(x)
        product_name = []
        product_sub_name = []
        for i in product_id:
            pro_name = super_category.objects.filter(
                id=i).values('name')[0]['name']
            product_name.append(pro_name)
        for i in product_sub:
            pro_name = sub_category.objects.filter(
                id=i).values('name')[0]['name']
            product_sub_name.append(pro_name)

        products_stack = []
        cate = [x.name for x in objs]
        # print(cate)
        # print(objs)
        for i in objs:
            sin_objs = product.objects.filter(product_cate=i)[:6]

            if len(sin_objs) > 0:
                products_stack.append(sin_objs)

        home_crousel = homepage_crousel.objects.filter(active=True).last()
        print(home_crousel)
        if request.user.is_authenticated:
            customer = request.user.email
            user = customer
            if not Customer.objects.filter(email=customer).exists():
                a = Customer(name=customer, email=customer)
                a.save()
            cus_id = Customer.objects.filter(
                email=customer).values('id')[0]['id']
            order, created = Order.objects.get_or_create(
                customer_id=cus_id, complete=False)
            '''if not Order.objects.filter(customer_id=cus_id).exists():
                b=Order(customer_id=cus_id,complete=False)
                b.save()'''
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            email = request.user.email
            carts, created = CartItems.objects.get_or_create(
                email=request.user.email)
            if created:
                CartItems.objects.filter(email=email).update(items=cartItems)
            else:
                CartItems.objects.filter(email=email).update(items=cartItems)

        else:
            user = ''

            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        # print("homeprodlist:")
        print(products_stack)
        context = {"prod": zip(products_stack, cate), "home_crou": home_crousel, 'cartItems': cartItems, 'user': user,
                   'product_name': product_name, 'product_sub_name': product_sub_name, 'test_new': test_new}
        return render(request, "index.html", context)


def order_history(request):
    if request.user.is_authenticated:
        obj = history.objects.filter(email=request.user.email)
        totalamount = 0
        for it in obj:
            if it.ordertype == "Add" or it.ordertype == "Recieved":
                totalamount += it.total_amount
            elif it.ordertype == "Send":
                totalamount -= it.total_amount

        items = CartItems.objects.filter(
            email=request.user.email).values('items')[0]['items']
        return render(request, "order_histroy.html", {'history': obj, 'totalamount': totalamount, 'cartItems': items})
    else:
        return redirect('login_page')

def searchbrand(request):
    selected = []
    cate_bool = True
    sub_bool = True
    sup_bool = True
    cate_to_send = []
    sub_to_send = []
    sup_to_send = []
    filter_cate = filter_Categories.objects.get(name="Price")
    filter_price = filter_Objects.objects.filter(filter_category=filter_cate)
    filter_cate = filter_Categories.objects.get(name="Color")
    filter_color = filter_Objects.objects.filter(filter_category=filter_cate)    
    if request.user.is_authenticated:
        customer = request.user.email
        if not Customer.objects.filter(email=customer).exists():
            a = Customer(name=customer, email=customer)
            a.save()
        cus_id = Customer.objects.filter(email=customer).values("id")[0]["id"]
        order, created = Order.objects.get_or_create(customer_id=cus_id, complete=False)
        """if not Order.objects.filter(customer_id=cus_id).exists():
			b=Order(customer_id=cus_id,complete=False)
			b.save()"""
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]            
    if request.GET.get('query'):
        
        query= request.GET.get('query')
        
        sub = request.GET.get("sub")
        sup = request.GET.get("sup")

        if query is not None and query != '':
            lookups= Q(title__icontains=query)
            results= product.objects.filter(lookups)
            if results.count() != 0:
                for i in results:
                    cate= i.product_Category
                    brand=i.brand
                selected.append(cate.name)
                selected.append(brand)
                brand_to_send = results.values_list("brand", flat=True).distinct()
                cate_to_send = category.objects.all()
                sub_to_send = sub_category.objects.filter(product_Category__name__contains=cate)
                sup_to_send = super_category.objects.filter(product_Category__name__contains=cate, product_Subcategory__name__contains=sub_to_send)	            
                # Price slider
                marketid = []
                new_pro = []
                product_market_id = []
                product_market_name = []
                for item in results:
                    x = item.product_Category_id
                    if x not in product_market_id:
                        product_market_id.append(x)
                for i in product_market_id:
                    pro_name = category.objects.filter(id=i).values('name')[0]['name']
                    new_pro.append(pro_name)
                slider= category.objects.filter(name__in=new_pro)
                slider_price= slider.aggregate(maxprice=Max('higher_price'))['maxprice']
		
                slider_range = slider.filter(higher_price=slider_price) 
                rate = results.all().order_by("-price")  
                high_rate = rate[0].price   

                data = {
                "obj": query,
                "empty": False,
                "price": filter_price,
                "color": filter_color,
                "cate": cate,
                "rate": high_rate,
			    "slider_range": slider_range,
                "sub": sub,
                "sup": sup,
                "brands": brand_to_send,
                "cate_print": cate_bool,
                "sub_print": sub_bool,
                "sup_print": sup_bool,
                "categories": cate_to_send,
                "subcategories": sub_to_send,
                "supcategories": sup_to_send,
                "checked": selected,
                }       

                return render(
                    request,
                    "products/productlistview.html",
                    {"data": data, "cartItems": cartItems},
                    )
            else:
                return HttpResponse('Sorry No Products Found')
        else:
            return redirect("/")

    else:
        return redirect("/")        
def term (request):
    return render(request,'terms_condi.html')

def privacy (request):
    return render(request,'privacy_policy.html')

# b2b index page

def b2b_index(request):
    user = ''
    objs = product_cate_b2b.objects.filter(show_on_homepage=True)
    items = []

    # new_prod = product.objects.filter(product_Category)
    # print(new_prod)
    # product_quan = product.objects.all()
    # product_quan = product.objects.filter(b2b_product=True) #B2BCHECKBOX
    b2bTag = labels_Object.objects.get(name='B2B')
    product_quan = product.objects.filter(product_tags = b2bTag)
    # print('PRODUCT QUAN: ', product_quan)
    # all_product =product.objects.all()

    # test_new = product.objects.order_by().distinct('product_Category')
    # test_new = product.objects.filter(b2b_product=True).distinct('product_Category') #B2BCHECKBOX
    b2bTag = labels_Object.objects.get(name='B2B')
    test_new = product.objects.filter(product_tags = b2bTag).distinct('product_Category')
    # print('TEST NEW', test_new)
    # print('NEW TEST NEW', test_new_NEW)

    testt = []
    for cate in test_new:
        products = product.objects.filter(
            product_Category=cate.product_Category)
        random_product = random.choice(products)

        testt.append(random_product.slug)

    final_t = product.objects.none()
    for t in testt:
        final_t |= product.objects.filter(slug=t)

    test_new = final_t

    

    #product_name=[x.product_Supercategory for x in product_quan]
    product_id = []
    product_sub = []

    for i in product_quan:
        x = i.product_Supercategory_id

        if x not in product_id:
            product_id.append(x)
    for i in product_quan:
        x = i.product_Subcategory_id

        if x not in product_sub:
            product_sub.append(x)
    product_name = []
    product_sub_name = []
    for i in product_id:
        pro_name = super_category.objects.filter(
            id=i).values('name')[0]['name']
        product_name.append(pro_name)
    for i in product_sub:
        pro_name = sub_category.objects.filter(id=i).values('name')[0]['name']
        product_sub_name.append(pro_name)

    products_stack = []
    cate = [x.name for x in objs]
    # print(cate)
    # print(objs)
    for i in objs:
        sin_objs = product.objects.filter(product_cate=i)[:6]

        if len(sin_objs) > 0:
            products_stack.append(sin_objs)
    home_crousel = B2B_homepage_crousel.objects.filter(active=True)
    n1 = len(home_crousel)

    dis_crou1 = B2B_discount_corousel1.objects.filter(active=True)
    dis_crou2 = B2B_discount_corousel2.objects.filter(active=True)

    if request.user.is_authenticated:
        customer = request.user.email
        user = customer
        if not Customer.objects.filter(email=customer).exists():
            a = Customer(name=customer, email=customer)
            a.save()
        cus_id = Customer.objects.filter(email=customer).values('id')[0]['id']
        order, created = Order.objects.get_or_create(
            customer_id=cus_id, complete=False)
        '''if not Order.objects.filter(customer_id=cus_id).exists():
            b=Order(customer_id=cus_id,complete=False)
            b.save()'''
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        email = request.user.email
        carts, created = CartItems.objects.get_or_create(
            email=request.user.email)
        if created:
            CartItems.objects.filter(email=email).update(items=cartItems)
        else:
            CartItems.objects.filter(email=email).update(items=cartItems)

    else:
        user = ''

        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    # print("homeprodlist:")
    print(products_stack)
    context = {"prod": zip(products_stack, cate), "home_crou": home_crousel, 'dis_crou1': dis_crou1, 'dis_crou2': dis_crou2, 'cartItems': cartItems, 'user': user,
               'product_name': product_name, 'product_sub_name': product_sub_name, 'test_new': test_new,'range1': range(1,n1), }
    return render(request, "b2b_index.html", context)

# tag index page

def tag_index(request,base_name):
    user = ''
    objs = product_cate_b2b.objects.filter(show_on_homepage=True)
    items = []

    # new_prod = product.objects.filter(product_Category)
    # print(new_prod)
    # product_quan = product.objects.all()
    # product_quan = product.objects.filter(b2b_product=True) #B2BCHECKBOX
    tag = labels_Object.objects.get(name=base_name)
    product_quan = product.objects.filter(product_tags = tag)
    # print('PRODUCT QUAN: ', product_quan)
    # all_product =product.objects.all()

    # test_new = product.objects.order_by().distinct('product_Category')
    # test_new = product.objects.filter(b2b_product=True).distinct('product_Category') #B2BCHECKBOX
    test_new = product.objects.filter(product_tags = tag).distinct('product_Category')
    # print('TEST NEW', test_new)
    # print('NEW TEST NEW', test_new_NEW)

    testt = []
    for cate in test_new:
        products = product.objects.filter(
            product_Category=cate.product_Category.all().first())
        random_product = random.choice(products)

        testt.append(random_product.slug)

    final_t = product.objects.none()
    for t in testt:
        final_t |= product.objects.filter(slug=t)

    test_new = final_t

    
    
    #product_name=[x.product_Supercategory for x in product_quan]
    product_id = []
    product_sub = []
    
    for i in product_quan:
        x = i.product_Supercategory.all()
        for j in x:
            if j.id not in product_id:
                product_id.append(j.id)
    for i in product_quan:
        x = i.product_Subcategory.all()

        for j in x:
            if j.id not in product_sub:
                product_sub.append(j.id)
    product_name = []
    product_sub_name = []
    for i in product_id:
        pro_name = super_category.objects.filter(
            id=i).values('name')[0]['name']
        product_name.append(pro_name)
    for i in product_sub:
        pro_name = sub_category.objects.filter(id=i).values('name')[0]['name']
        product_sub_name.append(pro_name)

    products_stack = []
    cate = [x.name for x in objs]
    # print(cate)
    # print(objs)
    for i in objs:
        sin_objs = product.objects.filter(product_cate=i)[:6]

        if len(sin_objs) > 0:
            products_stack.append(sin_objs)
    if B2B_homepage_crousel.objects.filter(tag = base_name,active=True).exists:
        home_crousel = B2B_homepage_crousel.objects.filter(tag=base_name,active=True)
    else:
        home_crousel =  B2B_homepage_crousel.objects.get(tag = 'home')
    n1 = len(home_crousel)

    dis_crou1 = B2B_discount_corousel1.objects.filter(active=True)
    dis_crou2 = B2B_discount_corousel2.objects.filter(active=True)

    if request.user.is_authenticated:
        customer = request.user.email
        user = customer
        if not detail.objects.filter(email=customer).exists():
            userprofile = detail(name=customer, email=customer)
            userprofile.save()
       # cus_id = detail.objects.filter(email=customer).values('id')[0]['id']
        #order, created = Order.objects.get_or_create(
         #   customer_id=cus_id, complete=False)
        '''if not Order.objects.filter(customer_id=cus_id).exists():
            b=Order(customer_id=cus_id,complete=False)
            b.save()'''
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    #     email = request.user.email
    #     carts, created = CartItems.objects.get_or_create(
    #         email=request.user.email)
    #     if created:
    #         CartItems.objects.filter(email=email).update(items=cartItems)
    #     else:
    #         CartItems.objects.filter(email=email).update(items=cartItems)

    # else:
    #     user = ''

    #     order = {'get_cart_total': 0, 'get_cart_items': 0}
    #     cartItems = order['get_cart_items']
    # print("homeprodlist:")

    print(products_stack)
    all_products = product.objects.all()
    print("!@#$%^&*()_!@#$%^&*()")
    print(all_products)
    dod_prods = product.objects.filter(deal_of_day=1)
    
    context = {"prod": zip(products_stack, cate), "home_crou": home_crousel, 'dis_crou1': dis_crou1, 'dis_crou2': dis_crou2,  'user': user, #'cartItems': cartItems,
               'product_name': product_name, 'product_sub_name': product_sub_name, 'test_new': test_new,'range1': range(1,n1),  'products': all_products, 'dod': dod_prods}
    return render(request,"new_b2b_index.html", context)

# Sourcing page

def sourcing(request):
    return render(request, 'enquiry/sourcing.html')

#gown page

def gown(request):
    return render(request, 'gown/index.html')

def about(request):
    return render(request, 'gown/about.html')

def portfolio(request):
    return render(request, 'gown/portfolio.html')

def blog(request):
    return render(request, 'gown/blog.html')

def contact(request):
    return render(request, 'gown/contact.html')

def single_blog(request):
    return render(request, 'gown/single-blog.html')


# fatory-profile pages

def shirt(request):
    return render(request, 'factory-profile/shirts-formal_casual/index.html')

def made_to_measure(request):
    return render(request, 'factory-profile/made-to-measure/index.html')

def jeans(request):
    return render(request, 'factory-profile/Jeans-jackets_bottoms_shorts/index.html')

def ethnic_wear(request):
    return render(request, 'factory-profile/ethnic-wear/index.html')

def gowns(request):
    return render(request, 'factory-profile/gowns/index.html')

def jackets(request):
    return render(request, 'factory-profile/jackets-formal_casual/index.html')

def trousers(request):
    return render(request, 'factory-profile/trouser-formal_casual/index.html')

def leather(request):
    return render(request, 'factory-profile/leather-jackets_etc/index.html')

def tshirts(request):
    return render(request, 'factory-profile/tshirts/index.html')

def tops(request):
    return render(request, 'factory-profile/tops/index.html')

def jeans_product(request):
    return render(request, 'factory-profile/Jeans-jackets_bottoms_shorts/product.html')

def jeans_category(request):
    return render(request, 'factory-profile/Jeans-jackets_bottoms_shorts/category.html')

def jeans_cart(request):
    return render(request, 'factory-profile/Jeans-jackets_bottoms_shorts/cart.html')

def jeans_checkout(request):
    return render(request, 'factory-profile/Jeans-jackets_bottoms_shorts/checkout.html')

def jeans_contact(request):
    return render(request, 'factory-profile/Jeans-jackets_bottoms_shorts/contact.html')

def made_to_measure_about(request):
    return render(request, 'factory-profile/made-to-measure/about.html')

def made_to_measure_blog(request):
    return render(request, 'factory-profile/made-to-measure/blog.html')

def made_to_measure_contact(request):
    return render(request, 'factory-profile/made-to-measure/contact.html')

def made_to_measure_gallery(request):
    return render(request, 'factory-profile/made-to-measure/gallery.html')

def made_to_measure_elements(request):
    return render(request, 'factory-profile/made-to-measure/elements.html')

def made_to_measure_main(request):
    return render(request, 'factory-profile/made-to-measure/main.html')

def made_to_measure_services(request):
    return render(request, 'factory-profile/made-to-measure/services.html')

def made_to_measure_single_blog(request):
    return render(request, 'factory-profile/made-to-measure/single-blog.html')

def shirts_about(request):
    return render(request, 'factory-profile/shirts-formal_casual/about.html')

def shirts_blog_details(request):
    return render(request, 'factory-profile/shirts-formal_casual/blog-details.html')

def shirts_blog(request):
    return render(request, 'factory-profile/shirts-formal_casual/blog.html')

def shirts_checkout(request):
    return render(request, 'factory-profile/shirts-formal_casual/checkout.html')

def shirts_contact(request):
    return render(request, 'factory-profile/shirts-formal_casual/contact.html')

def shirts_main(request):
    return render(request, 'factory-profile/shirts-formal_casual/main.html')

def shirts_shop_details(request):
    return render(request, 'factory-profile/shirts-formal_casual/shop-details.html')

def shirts_shop(request):
    return render(request, 'factory-profile/shirts-formal_casual/shop.html')

def shirts_shopping_cart(request):
    return render(request, 'factory-profile/shirts-formal_casual/shopping-cart.html')

def ethnic_product(request):
    return render(request, 'factory-profile/ethnic-wear/product.html')

def ethic_category(request):
    return render(request, 'factory-profile/ethnic-wear/category.html')

def ethnic_cart(request):
    return render(request, 'factory-profile/ethnic-wear/cart.html')

def ethnic_checkout(request):
    return render(request, 'factory-profile/ethnic-wear/checkout.html')

def ethnic_contact(request):
    return render(request, 'factory-profile/ethnic-wear/contact.html')

def gowns_about(request):
    return render(request, 'factory-profile/gowns/about.html')

def gowns_blog(request):
    return render(request, 'factory-profile/gowns/blog.html')

def gowns_contact(request):
    return render(request, 'factory-profile/gowns/contact.html')

def gowns_gallery(request):
    return render(request, 'factory-profile/gowns/gallery.html')

def gowns_elements(request):
    return render(request, 'factory-profile/gowns/elements.html')

def gowns_main(request):
    return render(request, 'factory-profile/gowns/main.html')

def gowns_services(request):
    return render(request, 'factory-profile/gowns/services.html')

def gowns_single_blog(request):
    return render(request, 'factory-profile/gowns/single-blog.html')

def jackets_about(request):
    return render(request, 'factory-profile/jackets-formal_casual/about.html')

def jackets_blog_details(request):
    return render(request, 'factory-profile/jackets-formal_casual/blog-details.html')

def jackets_blog(request):
    return render(request, 'factory-profile/jackets-formal_casual/blog.html')

def jackets_checkout(request):
    return render(request, 'factory-profile/jackets-formal_casual/checkout.html')

def jackets_contact(request):
    return render(request, 'factory-profile/jackets-formal_casual/contact.html')

def jackets_main(request):
    return render(request, 'factory-profile/jackets-formal_casual/main.html')

def jackets_shop_details(request):
    return render(request, 'factory-profile/jackets-formal_casual/shop-details.html')

def jackets_shop(request):
    return render(request, 'factory-profile/jackets-formal_casual/shop.html')

def jackets_shopping_cart(request):
    return render(request, 'factory-profile/jackets-formal_casual/shopping-cart.html')

def trousers_about(request):
    return render(request, 'factory-profile/trouser-formal_casual/about.html')

def trousers_blog_details(request):
    return render(request, 'factory-profile/trouser-formal_casual/blog-details.html')

def trousers_blog(request):
    return render(request, 'factory-profile/trouser-formal_casual/blog.html')

def trousers_checkout(request):
    return render(request, 'factory-profile/trouser-formal_casual/checkout.html')

def trousers_contact(request):
    return render(request, 'factory-profile/trouser-formal_casual/contact.html')

def trousers_main(request):
    return render(request, 'factory-profile/trouser-formal_casual/main.html')

def trousers_shop_details(request):
    return render(request, 'factory-profile/trouser-formal_casual/shop-details.html')

def trousers_shop(request):
    return render(request, 'factory-profile/trouser-formal_casual/shop.html')

def trousers_shopping_cart(request):
    return render(request, 'factory-profile/trouser-formal_casual/shopping-cart.html')

def tshirts_product(request):
    return render(request, 'factory-profile/tshirts/product.html')

def tshirts_category(request):
    return render(request, 'factory-profile/tshirts/category.html')

def tshirts_cart(request):
    return render(request, 'factory-profile/tshirts/cart.html')

def tshirts_checkout(request):
    return render(request, 'factory-profile/tshirts/checkout.html')

def tshirts_contact(request):
    return render(request, 'factory-profile/tshirts/contact.html')   

def leather_product(request):
    return render(request, 'factory-profile/leather-jackets_etc/product.html')

def leather_category(request):
    return render(request, 'factory-profile/leather-jackets_etc/category.html')

def leather_cart(request):
    return render(request, 'factory-profile/leather-jackets_etc/cart.html')

def leather_checkout(request):
    return render(request, 'factory-profile/leather-jackets_etc/checkout.html')

def leather_contact(request):
    return render(request, 'factory-profile/leather-jackets_etc/contact.html')

def tops_about(request):
    return render(request, 'factory-profile/tops/about.html')

def tops_blog(request):
    return render(request, 'factory-profile/tops/blog.html')

def tops_contact(request):
    return render(request, 'factory-profile/tops/contact.html')

def tops_gallery(request):
    return render(request, 'factory-profile/tops/gallery.html')

def tops_elements(request):
    return render(request, 'factory-profile/tops/elements.html')

def tops_main(request):
    return render(request, 'factory-profile/tops/main.html')

def tops_services(request):
    return render(request, 'factory-profile/tops/services.html')

def tops_single_blog(request):
    return render(request, 'factory-profile/tops/single-blog.html')

def banner(request):
    print('done')
    if request.method == "POST":
        logo1 = request.POST.get('logo')
        img = logo.objects.get(name=logo1)
        image = img.image.url
        print(image)
        return JsonResponse({'image': image})