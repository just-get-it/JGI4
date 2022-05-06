from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from .forms import *
from datetime import *
from xhtml2pdf import pisa
from django.conf import settings as djangoSettings
from django.core.files import File
from django.conf import settings
import razorpay
from .generate_invoice import invoice
import json
from product.models import category
from wallet.models import *
from django.urls import reverse
from django.contrib import messages
from .generate_subscription_bill import sub_bill
from newrentapp.models import *
import geocoder
import requests
from django.http import HttpResponseRedirect
from userdetail.views import *
import math
# Razorpay ID and Secret
razorpay_id = "rzp_test_9joF0fVvCUMOZC"
razorpay_secret = "2Alnr3lLV7jsMJ4OJya2eUeO"

# bing map key
bing_key = 'AgB7hiqOcS-Xw-jNEegI1kq-LPI1BJPDRi5mlCfaLrs_0tBrOvsTTBpbJ4eSrEqo'

state_full_forms = { "an":"Andaman and Nicobar Islands","ap":"Andhra Pradesh","ar": "Arunachal Pradesh", "as": "Assam","br":"Bihar","ch":"Chandigarh"
,"ct":"Chhattisgarh","dn":"Dadra and Nagar Haveli","dd":"Daman and Diu","dl":"Delhi","ga":"Goa","gj":"Gujarat","hr":"Haryana","hp":"Himachal Pradesh","jk":"Jammu and Kashmir","jh":"Jharkhand","ka": "Karnataka","kl":"Kerala","ld":"Lakshadweep","mp":"Madhya Pradesh","mh":"Maharashtra","mn":"Manipur","ml":"Meghalaya","mz":"Mizoram","nl":"Nagaland","or":"Odisha","py":"Puducherry"
,"pb":"Punjab","rj":"Rajasthan","sk":"Sikkim","tn":"Tamil Nadu","tg":"Telangana","tr":"Tripura","up":"Uttar Pradesh","ut":"Uttarakhand","wb":"West Bengal"}
# Create your views here.

def get_distance_and_time(start, end):		# my changes
	start.reverse()
	end.reverse()
	print(start, end)
	start_string = ','.join([str(elem) for elem in start])
	end_string = ','.join([str(elem) for elem in end])
	print(start_string, end_string)
	url = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins='+ end_string + '&destinations=' + start_string + '&travelMode=driving&key='+ bing_key
	r = requests.get(url)
	resp = (r.json())["resourceSets"][0]["resources"][0]
	print(resp)
	results = resp.get('results')
	if results :
		res = resp["results"][0]
		distance =  res["travelDistance"]
		time = res["travelDuration"]
		return abs(distance), abs(time)
	else:
		return False
# print(get_distance_and_time([77.5491,12.9847],[77.5772,13.0352]))

def get_location_address(cordinates):		# my changes
	print(cordinates)
	# cordinates.reverse()
	coordinates = ','.join([str(elem) for elem in cordinates])
	addr = geocoder.bing(coordinates, method = 'reverse', key = bing_key)
	addr_json = addr.json
	print(coordinates)
	print(addr_json)
	if addr_json:
		print(addr_json['address'])
		return addr_json['address']
	else: 
		return False
# get_location_address([77.5772,13.0352])

def get_order_coords(request, order_item_id):     # my changes
	order_item_now = OrderItem.objects.get(pk = order_item_id)
	print(order_item_now)
	delivery_location = order_item_now.customer.current_loc_coord
	order_pickup_location = order_item_now.product.seller.current_loc_coord
	data = {
		'delivery_coords' : delivery_location,
		'order_pickup_coords' : order_pickup_location
	}
	return JsonResponse(data)

def get_live_location_coords(request, order_item_id):     # my changes
	order_item_now = OrderItem.objects.get(pk = order_item_id)
	print(order_item_now)
	delivery_location = order_item_now.customer.current_loc_coord
	order_coords = Logistics.objects.get(order_item = order_item_now).order_curr_location
	data = {
		'delivery_coords' : delivery_location,
		'order_coords' : order_coords,
	}
	return JsonResponse(data)

def updatecart(request):
	# Getting User
	currUser = detail.objects.filter(email=request.user.email).first()
	if not currUser.customer and request.POST.get('action') == 'add':
		
		if request.POST.get('action') == 'add':
			print('THIS IS action: ', request.POST)
			slug = request.POST['product']
			prod = product.objects.get(slug = slug)
			if request.POST.get('sizes'):
				print("in size")
				size_color_quantity_arr = request.POST.get('sizes')
				size_color_quantity_arr = json.loads(size_color_quantity_arr)
				cartItems = 0
				print(size_color_quantity_arr)
				for i in size_color_quantity_arr:
					size=i['size']
					color=i['color']
					quantity=i['quantity']
					print(size,color,quantity,prod)
					size_object = size_color_quantity.objects.filter(linked_product=prod, size=int(size), color=color).first()
					# Getting Cart Object
					old_cart = OrderItem.objects.filter(customer=currUser, product=prod, size_color=size_object, is_placed=False, is_Cancelled = False)
					empty_old_cart = OrderItem.objects.filter(customer=currUser, is_placed=False, product__isnull=True, is_Cancelled = False)
					if old_cart:
						old_cart = old_cart[0]
						old_cart.quantity += int(quantity)
						old_cart.set_total
						old_cart.save()
					elif empty_old_cart:
						cart = empty_old_cart[0]
						cart.customer = currUser
						cart.product = prod
						cart.size_color = size_object
						cart.quantity = int(quantity)
						cart.save()
					else:
						newCart = OrderItem(
							customer=currUser,
							product=prod,
							size_color=size_object,
							quantity=quantity
						)
						newCart.save()
						newCart.set_total
						price = newCart.get_price
					# Calculating Number of items in cart
					
					cart = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
				for item in cart:
					cartItems += item.quantity
					print("cartItems",cartItems)
				return JsonResponse({"cartItems": cartItems})
				#here
				
	else:
		if request.POST.get('action') == 'add':
			print('THIS IS POST: ', request.POST)
			# Getting product
			slug = request.POST['product']
			prod = product.objects.get(slug = slug)
			# Getting addtocart quantity
			quant = request.POST.get('quantity')
			quant = int(quant)
			print("QUANT: ", quant)
			# Getting size_color_quantity
			if request.POST.get('size'):
				size_value = request.POST.get('size')
				size_int = size_value.split()
				size_int = int(size_int[0])
				color_value = request.POST.get('color')
				size_object = size_color_quantity.objects.filter(linked_product=prod, size=size_int, color=color_value).first()
			else:
				size_object = size_color_quantity.objects.filter(linked_product=prod).first()
			print(f'This is SIZE: {size_object}')
			# Getting Cart Object
			old_cart = OrderItem.objects.filter(customer=currUser, product=prod, size_color=size_object, is_placed=False, is_Cancelled = False)
			empty_old_cart = OrderItem.objects.filter(customer=currUser, is_placed=False, product__isnull=True, is_Cancelled = False)
			if old_cart:
				old_cart = old_cart[0]
				old_cart.quantity += quant
				old_cart.set_total
				old_cart.save()
			elif empty_old_cart:
				cart = empty_old_cart[0]
				cart.customer = currUser
				cart.product = prod
				cart.size_color = size_object
				cart.quantity = quant
				cart.save()
			else:
				newCart = OrderItem(
					customer=currUser,
					product=prod,
					size_color=size_object,
					quantity=quant
				)
				newCart.save()
				newCart.set_total
				price = newCart.get_price
			# Calculating Number of items in cart
			cartItems = 0
			cart = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
			for item in cart:
				cartItems += item.quantity
			return JsonResponse({"cartItems": cartItems})
		elif request.POST.get("action") == 'update':
			# Getting Old Item and Update quantity
			Oid = request.POST.get("Oid") 
			print("OID ",Oid)
			quantity = request.POST.get("quantity")
			Oitem = OrderItem.objects.get(pk=Oid)
			# Setting quantity and calculating total
			Oitem.quantity = quantity
			Oitem.save()
			if currUser.customer:
				Oitem.set_total
			else:
				Oitem.set_b2b_total
			Oitem.save()
			print("total=   ",Oitem.total)
			itemTotal = Oitem.total
			cartItems = 0
			cartTotal = 0
			if(Oitem.is_placed==False):
				cart = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
			else:
				order = Order.objects.get(id=Oitem.order.id)
				cart = OrderItem.objects.filter(customer=currUser, is_placed=True, order=order, is_Cancelled = False) 
		
			for item in cart:
					cartItems += item.quantity
					if currUser.customer:
						item.set_total
					else:
						item.set_b2b_total
					cartTotal += item.total
			
			if(Oitem.is_placed==True):
				order = Order.objects.get(id=Oitem.order.id)
				# here mov is 10k
				if cartTotal < 10000:
						cartTotal += 101 # 101 is delivery charge

				order.total = cartTotal
				invoice(order,cart)
				order.save()
			
			return JsonResponse({"itemTotal":itemTotal, "cartItems": cartItems, "cartTotal": cartTotal})
		elif request.POST.get('action') == "delete":
			Oid = request.POST.get('Oid')
			Oitem = OrderItem.objects.get(pk=Oid)
			Oitem.product = None
			Oitem.size_color = None
			Oitem.quantity = None
			Oitem.total = None
			Oitem.save()
			return JsonResponse({"deleted" : True})
		elif request.POST.get('action') == "get":
			cartItems = 0
			cart = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
			for item in cart:
				cartItems += item.quantity
			print(f'Returning json cartitems: ', cartItems)
			return JsonResponse({"cartItems": cartItems})
		else:
			cols = False
			return JsonResponse({"data":cols})

def coupon_delete(request):
	response = HttpResponseRedirect('/cartnew/cart')
	all_cookies = ['coupon_applied', 'code', 'min_amount', 'dicount_percentage', 'dicount_amount', 'disc_type_is_percents', 'description']
	for cookie in all_cookies:
		if request.COOKIES.get(cookie, None):
			response.delete_cookie(cookie)
	return response

def coupon_apply(request, coupon_code):
	response = HttpResponseRedirect('/cartnew/cart')
	item = coupons.objects.filter(code = coupon_code).first()
	if item == None:
		response.set_signed_cookie('coupon_applied', 'Wrong')
	else:
		response.set_signed_cookie('coupon_applied', 'True')
		response.set_signed_cookie('code', item.code)
		response.set_signed_cookie('min_amount', item.min_amount)
		response.set_signed_cookie('discount_percentage', item.discount_percentage)
		response.set_signed_cookie('discount_amount', item.discount_amount)
		response.set_signed_cookie('disc_type_is_percents', item.disc_type_is_percents)
		response.set_signed_cookie('description', item.description)
	print(response, "accept coupon")
	return response

def cart(request):
	currUser = detail.objects.filter(email=request.user.email).first()
	print(request.POST)
	if currUser.customer and request.user.is_authenticated:
		cartdt = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
		cartItems = 0
		cartTotal = 0
		order_id=None
		for item in cartdt:
			if item.order:
				order_id = item.order.id
			cartItems += item.quantity
			print("item=",item.size_color)
			if currUser.customer:
				item.set_total
			else:
				item.set_b2b_total
			cartTotal += item.total
		coupon_applied = False
		discount = 0
		code = ''
		one_time_coupons = coupons.objects.filter(one_time_only = True)
		not_applied_one_time_coupons = coupons_applied.objects.filter(number_of_usages = 0, user = currUser, coupons__in = one_time_coupons)
		business_model_coupons = coupons.objects.filter(one_time_only = False, business_model = 'product')
		default_coupons = coupons.objects.filter(one_time_only = False, is_category_coupon=False, is_business_model_coupon=False)
		category_coupons = coupons.objects.filter(one_time_only = False, is_category_coupon=True)
		available_coupons_duplicates = list(not_applied_one_time_coupons) + list(business_model_coupons) + list(category_coupons) + list(default_coupons)
		available_coupons = []
		[available_coupons.append(x) for x in available_coupons_duplicates if x not in available_coupons]
		if request.COOKIES.get('coupon_applied', None) and request.get_signed_cookie('coupon_applied') == 'True':
			if request.COOKIES.get('code', None): 
				curr_coupon = coupons.objects.filter(code = request.get_signed_cookie('code')).first()
				if curr_coupon and curr_coupon.min_amount <= cartTotal:
					coupon_applied = True
					code = curr_coupon.code
					if len(list(not_applied_one_time_coupons)) > 0:
						curr_applied_coupon = coupons_applied.filter(coupons = coupons.objects.get(code = code))
						curr_applied_coupon.number_of_usages += 1 
						curr_applied_coupon.save()
					else:
						curr_applied_coupon = coupons_applied()
						curr_applied_coupon.user = currUser
						curr_applied_coupon.coupons = coupons.objects.get(code = code)
						curr_applied_coupon.number_of_usages = 1
						curr_applied_coupon.save()
					if curr_coupon.disc_type_is_percents == False:
						discount = curr_coupon.discount_amount
					else:
						discount = cartTotal * curr_coupon.discount/100
				single_prod_sum = 0
				for item in cartdt:
					single_prod_sum += item.total/item.quantity
				for item in cartdt:
					print(item.total, "item total before discount")
					if curr_coupon.is_category_coupon:
						if item.product.product_Supercategory == curr_coupon.category:
							discounted_price = (item.total/cartTotal)*discount	# TODO: calculating discounted price
							item.total -= discounted_price
							item.save()	
					else:
						discounted_price = (item.total/cartTotal)*discount
						item.total -= discounted_price
						item.save()	
				cartTotal -= curr_coupon.discount_amount
					
		order = ""
		if not(order_id == None):
			order = Order.objects.get(id=order_id)
		context = {
			'cartdata': reversed(cartdt),
			'cartItems': cartItems,
			'cartTotal': cartTotal,
			'order':order,
			'coupons': available_coupons,
			'coupon_applied': coupon_applied,
			'code': code,
			'discount': discount,
			  }
		print(context['coupon_applied'])
		return render(request, "cart/cart.html", context=context)
	
	elif not currUser.customer and request.user.is_authenticated:
		cartdt = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
		cartItems = 0
		cartTotal = 0
		for item in cartdt:
			cartItems += item.quantity
			print("item=",item.size_color)
			if currUser.customer:
				item.set_total
			else:
				item.set_b2b_total
			cartTotal += item.total
		return render(request, "cart/cart.html", {'cartdata': reversed(cartdt), 'cartItems': cartItems, 'cartTotal': cartTotal})
	else:
		return redirect('login_page')

def select_address(request):
	if request.user.is_authenticated:
		print('THIS IS POST: ', request.POST)
		# Basic Page View
		currUser = detail.objects.filter(email=request.user.email).first()
		cartdt = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
		userAddresses = ShippingAddress.objects.filter(user = currUser, is_saved=True)
		addressdt = []
		if userAddresses:
			for address in userAddresses:
				addressform = shipping_address_form(instance=address, prefix=address.id)
				addressdt.append([address,addressform])
		if not cartdt:
			return redirect('newcart')
		addressform = shipping_address_form()
		# Addnewform Post handling
		if request.POST.get('new_address'):
			print(f"This is post data: {request.POST}")
			editedAddressForm = shipping_address_form(request.POST)
			if editedAddressForm.is_valid():
				savedAddress = editedAddressForm.save()
				savedAddress.user = currUser
				savedAddress.save()
			return redirect('selectaddress')
		# EDIT ADDRESS FORM POST HANDLING
		if request.POST.get('update_address'):
			pref = request.POST.get('update_address')
			editAddInstance = ShippingAddress.objects.get(pk=pref)
			print("THSI IS INSTANCE: ", editAddInstance)
			editedForm = shipping_address_form(request.POST, instance=editAddInstance, prefix=pref)
			if editedForm.is_valid():
				editedForm.save()
			return redirect('selectaddress')
		
		# Go To Order Summary Page
		if request.POST.get('AddrId'):
			AddrId = request.POST.get('AddrId')
			cartdt = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
			toAddress = ShippingAddress.objects.get(pk=AddrId)
			cartTotal = 0
			for item in cartdt:
				if currUser.customer:
					item.set_total
				else:
					item.set_b2b_total
				cartTotal += item.total
			return render(request, "cart/confirm_order.html", {'cartdata':reversed(cartdt), 'toAddress':toAddress, 'cartTotal':cartTotal})

		# Place a new order
		if request.POST.get('confirm_order'):
			payment_method = request.POST.get('payment_method')
			AddrId = request.POST.get('confirm_order')
			orderdt = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
			confirmAddr = ShippingAddress.objects.get(pk=AddrId)
			confirmAddr.pk = None
			confirmAddr.is_saved = False
			confirmAddr.save()
			orderDict = {}
			for odItem in orderdt:
				sellerId = odItem.product.seller.email
				if sellerId in orderDict.keys():
					orderDict[sellerId].append(odItem)
				else:
					orderDict[sellerId] = [odItem,]
			print('THIS IS ORDERDT : {} This is OderDICT {}'.format(orderdt, orderDict))
			newOrder = Order()
			newOrder.date_order_placed = datetime.datetime.now()
			newOrder.customer = currUser
			newOrder.save()
			orderTotal = 0
			for seller, odItems in orderDict.items():
				print('THIS IS SELLER {} THIS IS ITEMS {}'.format(seller, odItems))
				for item in odItems:
					if currUser.customer:
						item.set_total
					else:
						item.set_b2b_total
					orderTotal += item.total
					item.shipping_address = confirmAddr
					item.product_name = item.product.title
					item.cust_name = currUser.name
					item.date_placed = datetime.datetime.now()
					item.seller_name = item.product.seller.email
					item.seller_address = item.product.seller.address
					item.size_name = str(item.size_color.size) + str(item.size_color.unit)
					item.size_cost = item.size_color.price
					item.is_placed = True
					item.order = newOrder
					item.save()
				#temporarily mov for delivery is 10000
				if orderTotal < 10000:
					orderTotal += 101 #101 is delivery charge
				newOrder.total = orderTotal
				newOrder.payment_method = payment_method
				newOrder.save()
			if payment_method != 'razorpay':
				odItems = OrderItem.objects.filter(order=newOrder)
				invoice(newOrder,odItems)
			if payment_method == 'razorpay':
				newOrder.payment_status = 'Failed'
				newOrder.save()
				cartdt = OrderItem.objects.filter(order=newOrder)
				toAddress = cartdt[0].shipping_address
				address_string = toAddress.shipping_address + ", " + toAddress.city + " - " + toAddress.pin_code + ". " + toAddress.state 
				cartTotal = newOrder.total
				order_amount = cartTotal*100
				order_currency = 'INR'
				order_receipt = 'order_rcptid_' + str(newOrder.id)
				notes = {'Shipping address': address_string}
				client = razorpay.Client(auth=(razorpay_id, razorpay_secret))
				orderDict = {'amount': order_amount, "currency" : order_currency, "receipt" : order_receipt, "notes": notes, "payment_capture": "1"}
				orderResp = client.order.create(orderDict)
				print("orderResphere******",orderResp)
				newOrder.razorpay_order_id = orderResp.get('id')
				newOrder.save()
				return render(request, "cart/razorpay_checkout.html", {'order': newOrder,'cartdata':reversed(cartdt), 'toAddress':toAddress, 'cartTotal':cartTotal, 'razorpay_od_id': newOrder.razorpay_order_id})
			return redirect('order', order_id=newOrder.id)
		return render(request, "cart/select_address.html", {'addressform':addressform, 'addressdata':addressdt})
	else:
		return redirect('login_page')

def payment_status(request):
	currUser = detail.objects.filter(email=request.user.email).first()
	currOrder = Order.objects.filter(payment_status='pending', customer=currUser, payment_method="razorpay").first()
	if request.method == "POST":
		print(f'THIS IS POST {request.POST}')
		razorpay_payment_id = request.POST.get('razorpay_payment_id')
		razorpay_order_id = request.POST.get('razorpay_order_id')
		razorpay_signature = request.POST.get('razorpay_signature')
		razorData = {'razorpay_payment_id':razorpay_payment_id, 'razorpay_order_id':razorpay_order_id, 'razorpay_signature':razorpay_signature}
		client = razorpay.Client(auth=(razorpay_id, razorpay_secret))
		client.utility.verify_payment_signature(razorData)
		currOrder = Order.objects.get(razorpay_order_id=razorpay_order_id)
		currOrder.razorpay_payment_id = razorpay_payment_id
		currOrder.razorpay_signature = razorpay_signature
		currOrder.payment_status = "Paid Successfully"
		currOrder.save()
		odItems = OrderItem.objects.filter(order=currOrder)
		invoice(currOrder,odItems)
		return redirect('order', order_id=currOrder.id)
	return redirect('newcart')

def checkout(request):
	return render(request, "cart/checkout.html")

def manage_addresses(request):
	if request.POST.get('action') == "delete":
		AddrId = request.POST.get('AddrId')
		address = ShippingAddress.objects.get(pk = AddrId)
		address.delete()
		return JsonResponse({"deleted":True})

def my_orders(request):
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		all_orders = Order.objects.filter(customer=currUser).order_by('-id')
		orderdt = []
		category = []
		for order in all_orders:
			odItems = OrderItem.objects.filter(order=order).order_by('-product')
			tempItems = []
			for item in odItems:
				if item.product.product_Category.first() not in category:
					category.append(item.product.product_Category.first())
					
				tempItems.append(item)
			orderdt.append([order,tempItems])
		
		category.sort(key = lambda i:i.name)
		return render(request, "cart/my_orders.html", {"orderdata": orderdt, "categories":category})
	else:
		return redirect('login_page')

def track_order(request, order_id):
	curr_order_item = OrderItem.objects.get(id=order_id)
	customer_loc = curr_order_item.customer.current_loc_coord
	logistics_loc = Logistics.objects.get(order_item = curr_order_item).order_curr_location
	print(curr_order_item, customer_loc, logistics_loc)
	customer_loc_ls = customer_loc.split(',')
	customer_loc_ls.reverse()
	logistics_loc_ls = logistics_loc.split(',')
	logistics_loc_ls.reverse() 
	distance, time = get_distance_and_time(customer_loc_ls, logistics_loc_ls) 	# Time is in mins
	days = int(time / 1440)     
	# leftover_minutes = time % 1440
	# hours = leftover_minutes / 60
	# mins = time - (days*1440) - (hours*60)
	# print(str(days) + " days, " + str(hours) + " hours, " + str(mins) +  " mins. ")
	curr_order_item.days_for_delivery = days
	curr_order_item.save()
	print(distance, time)
	data = {
		'order_item_id': curr_order_item,
	}
	return render(request, "cart/track_order.html", data)

def order(request, order_id):
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		all_orders = Order.objects.filter(customer=currUser)
		order = Order.objects.filter(pk=order_id).first()
		if order:
			if order in all_orders:
				orderdt = []
				odItems = OrderItem.objects.filter(order=order).order_by('product_name')
				category = []
				tempItems = []
				for item in odItems:
					if item.product.product_Category.first() not in category:
						category.append(item.product.product_Category.first())
					tempItems.append(item)
				orderdt.append([order,tempItems])
				print(f'orderdt: {orderdt}')
				category.sort(key = lambda i:i.name)
				return render(request, "cart/order.html", {"orderdata": orderdt, "categories":category})
			else:
				return redirect('myorders')
		else:
			return redirect('myorders')
	else:
		return redirect('login_page')

def edit_order(request,order_id):
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		all_orders = Order.objects.filter(customer=currUser)
		order = Order.objects.filter(pk=order_id).first()
		if order.is_Cancelled: 
			return redirect('myorders')
		if order and order.status == "Accepted":
			if order in all_orders:
				orderdt = []
				odItems = OrderItem.objects.filter(order=order, is_Cancelled = False).order_by('product_name')
				category = []
				tempItems = []
				for item in odItems:
					tempItems.append(item)
					if item.product.product_Category.first() not in category:
						category.append(item.product.product_Category.first())
				orderdt.append([order,tempItems])
				print(f'orderdt: {orderdt}')
				category.sort(key = lambda i:i.name)
				return render(request, "cart/edit_order.html", {"orderdata": orderdt, "categories":category})
			else:
				return redirect('myorders')
		else:
			return redirect('myorders')
	else:
		return redirect('login_page')

def edit_addresses(request):
	currUser = detail.objects.filter(email=request.user.email).first()
	# Addnewform Post handling
	if request.POST.get('new_address'):
		editedAddressForm = shipping_address_form(request.POST)
		if editedAddressForm.is_valid():
			savedAddress = editedAddressForm.save()
			savedAddress.user = currUser
			savedAddress.save()
		return redirect('editaddresses')
	# EDIT ADDRESS FORM POST HANDLING
	if request.POST.get('update_address'):
		pref = request.POST.get('update_address')
		editAddInstance = ShippingAddress.objects.get(pk=pref)
		editedForm = shipping_address_form(request.POST, instance=editAddInstance, prefix=pref)
		if editedForm.is_valid():
			editedForm.save()
		return redirect('editaddresses')
	currUser = detail.objects.filter(email=request.user.email).first()
	cartdt = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0)
	userAddresses = ShippingAddress.objects.filter(user = currUser, is_saved=True)
	if not cartdt:
		return redirect('newcart')
	addressdt = []
	if userAddresses:
		for address in userAddresses:
			addressform = shipping_address_form(instance=address, prefix=address.id)
			addressdt.append([address,addressform])
	addressform = shipping_address_form()

	return render(request, 'cart/edit_addresses.html', {'addressdata': addressdt, 'addressform': addressform})


def add_item(request,order_id):
	currUser = detail.objects.filter(email=request.user.email).first()
	order = Order.objects.filter(pk=order_id).first()
	cartdt = OrderItem.objects.filter(customer=currUser, order=order, is_Cancelled = False)
	for item in cartdt:
		item.is_placed = False
		item.save()
	return redirect('/b2c')

def update_existing_order(request,order_id):
	
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		order = Order.objects.filter(pk=order_id).first()
		
		if request.POST.get('action') == "delete":
			orderTotal = 0
			Oid = request.POST.get('Oid')
			Oitem = OrderItem.objects.get(pk=Oid)
			Oitem.is_Cancelled = True
			Oitem.save()
			odItems = OrderItem.objects.filter(customer=currUser, order=order, is_Cancelled = False)
			print("length = ",len(odItems))
			if len(odItems)==0:
				order.is_Cancelled = True
				order.total = 0
				order.save()
			else:
				for item in odItems:
					orderTotal += item.total
				if orderTotal < 10000:
					orderTotal += 101 #101 is delivery charge
				order.total = orderTotal
				order.date_order_placed = datetime.datetime.now()
				order.save()
			odItems = OrderItem.objects.filter(order=order)
			invoice(order,odItems)
			return JsonResponse({"deleted" : True})

		else:
			odItems = OrderItem.objects.filter(customer=currUser, is_placed=False, quantity__gt = 0, is_Cancelled = False)
			confirmAddr=""
			orderTotal = 0
			for item in odItems:
				if currUser.customer:
					item.set_total
				else:
					item.set_b2b_total
				if item.order:
					item.is_placed = True
					confirmAddr = item.shipping_address
					orderTotal += item.total
					item.save()
				else:
					orderTotal += item.total
					item.shipping_address = confirmAddr
					item.product_name = item.product.title
					item.cust_name = currUser.name
					item.date_placed = datetime.datetime.now()
					item.seller_name = item.product.seller.email
					item.seller_address = item.product.seller.address
					item.size_name = str(item.size_color.size) + str(item.size_color.unit)
					item.size_cost = item.size_color.price
					item.is_placed = True
					item.order = order
					item.save()
			if orderTotal < 10000:
					orderTotal += 101 #101 is delivery charge
			order.total = orderTotal
			order.date_order_placed = datetime.datetime.now()
			order.save()
			odItems = OrderItem.objects.filter(order=order)
			invoice(order,odItems)
		return redirect('myorders')

def subscriptionCart(request):
	currUser = detail.objects.filter(email=request.user.email).first()
	if request.user.is_authenticated and request.POST.get('action') == 'add':
		'''
			Method used to save subscriptions in cart i.e. isPaid = False
		'''
		print('******* request rec *********')
		quantity = request.POST.get('quantity')
		amount = request.POST.get('amount')
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')
		interval = request.POST.get('interval')
		shift = request.POST.get('shift')
		remark = request.POST.get('remark')
		slug = request.POST.get('slug')
		print('*******************', slug)
		customer_email = request.user
		isPaid = False
		currUser = detail.objects.filter(email=request.user.email).first()
		prod = product.objects.filter(slug=slug).first()
		product_name = prod.title
		vendor = prod.seller

		transaction_id = str(request.user.id) + slug + "".join(str(start_date).split("-")) + "0" # O for identification of unpaid items

		a = subscriptionOrderItem(
				product = prod,
				product_name = product_name,
				quantity = quantity,
				amount = amount,
				interval = interval,
				start_date = start_date,
				end_date = end_date,
				shifts = shift,
				remark = remark,
				customer_email = customer_email,
				customer=currUser,
				vendor_email = vendor,
				isPaid = isPaid
				)
		a.save()
		print('*********** SAVED IN SUB CART ***********')
		data = {
			'message': 'success',
			'product_name': product_name,
			'quantity': quantity,
			'amount': amount,
			'interval': interval,
			'start_date': start_date,
			'end_date': end_date,
			'shifts': shift,
			'transaction_id': transaction_id
		}
		return JsonResponse(data)
	elif request.user.is_authenticated and request.method=="GET":
		subItems = subscriptionOrderItem.objects.filter(is_placed=False, customer=currUser,is_Cancelled=False) 
		subCartItems=0
		subCartTotal=0
		for item in subItems:
			price = item.get_price
			subCartItems += item.quantity 
			subCartTotal += price
		one_time_coupons = coupons.objects.filter(one_time_only = True)
		not_applied_one_time_coupons = coupons_applied.objects.filter(number_of_usages = 0, user = currUser, coupons__in = one_time_coupons)
		business_model_coupons = coupons.objects.filter(one_time_only = False, business_model = 'product')
		default_coupons = coupons.objects.filter(one_time_only = False, is_category_coupon=False, is_business_model_coupon=False)
		category_coupons = coupons.objects.filter(one_time_only = False, is_category_coupon=True)
		available_coupons_duplicates = list(not_applied_one_time_coupons) + list(business_model_coupons) + list(category_coupons) + list(default_coupons)
		available_coupons = []
		[available_coupons.append(x) for x in available_coupons_duplicates if x not in available_coupons]
		if request.COOKIES.get('coupon_applied', None) and request.get_signed_cookie('coupon_applied') == 'True':
			if request.COOKIES.get('code', None): 
				curr_coupon = coupons.objects.filter(code = request.get_signed_cookie('code')).first()
				if curr_coupon and curr_coupon.min_amount <= subCartTotal:
					coupon_applied = True
					code = curr_coupon.code
					if len(list(not_applied_one_time_coupons)) > 0:
						curr_applied_coupon = coupons_applied.filter(coupons = coupons.objects.get(code = code))
						curr_applied_coupon.number_of_usages += 1 
						curr_applied_coupon.save()
					else:
						curr_applied_coupon = coupons_applied()
						curr_applied_coupon.user = currUser
						curr_applied_coupon.coupons = coupons.objects.get(code = code)
						curr_applied_coupon.number_of_usages = 1
						curr_applied_coupon.save()
					if curr_coupon.disc_type_is_percents == False:
						discount = curr_coupon.discount_amount
					else:
						discount = subCartTotal * curr_coupon.discount/100
				single_prod_sum = 0
				for item in subCartItems:
					single_prod_sum += item.total/item.quantity
				for item in subCartItems:
					print(item.total, "item total before discount")
					if curr_coupon.is_category_coupon:
						if item.product.product_Supercategory == curr_coupon.category:
							discounted_price = (item.total/subCartTotal)*discount	# TODO: calculating discounted price
							item.total -= discounted_price
							item.save()	
					else:
						discounted_price = (item.total/subCartTotal)*discount
						item.total -= discounted_price
						item.save()	
				subCartTotal -= curr_coupon.discount_amount
		context = {
			"cartdata":subItems,
			"cartTotal":subCartTotal,
			"cartItems":subCartItems,
			'coupons': available_coupons,
			'coupon_applied': coupon_applied,
			'code': code,
			'discount': discount,
		}
		return render(request,"cart/subscriptionCart.html", context=context)

def subscribe_select_address(request):
	if request.user.is_authenticated:
		print('THIS IS POST: ', request.POST)
		# Basic Page View
		currUser = detail.objects.filter(email=request.user.email).first()
		subItems = subscriptionOrderItem.objects.filter(customer=currUser, is_placed=False, is_Cancelled = False)
		userAddresses = ShippingAddress.objects.filter(user = currUser, is_saved=True)
		addressdt = []
		if userAddresses:
			for address in userAddresses:
				addressform = shipping_address_form(instance=address, prefix=address.id)
				addressdt.append([address,addressform])
		if not subItems:
			return redirect('subscriptionCart')
		addressform = shipping_address_form()
		# Addnewform Post handling
		if request.POST.get('new_address'):
			print(f"This is post data: {request.POST}")
			editedAddressForm = shipping_address_form(request.POST)
			if editedAddressForm.is_valid():
				savedAddress = editedAddressForm.save()
				savedAddress.user = currUser
				savedAddress.save()
			return redirect('subscribe_selectaddress')
		# EDIT ADDRESS FORM POST HANDLING
		if request.POST.get('update_address'):
			pref = request.POST.get('update_address')
			editAddInstance = ShippingAddress.objects.get(pk=pref)
			print("THSI IS INSTANCE: ", editAddInstance)
			editedForm = shipping_address_form(request.POST, instance=editAddInstance, prefix=pref)
			if editedForm.is_valid():
				editedForm.save()
			return redirect('subscribe_selectaddress')
		
		# Go To Order Summary Page
		if request.POST.get('AddrId'):
			AddrId = request.POST.get('AddrId')
			subItems = subscriptionOrderItem.objects.filter(customer=currUser, is_placed=False, is_Cancelled = False)
			toAddress = ShippingAddress.objects.get(pk=AddrId)
			subCartTotal = 0
			for item in subItems:
				price = item.get_price
				subCartTotal += price
			return render(request, "cart/subscription_confirm.html", {'cartdata':reversed(subItems), 'toAddress':toAddress, 'cartTotal':subCartTotal})

		# Place a new subscription
		if request.POST.get('confirm_subscription'):
			payment_method = request.POST.get('payment_method')
			billing_frequency = request.POST.get('bill_freq')
			# bill_frequency = request.POST.get('bill_freq')
			AddrId = request.POST.get('confirm_subscription')
			orderdt = subscriptionOrderItem.objects.filter(customer=currUser, is_placed=False, is_Cancelled = False)
			confirmAddr = ShippingAddress.objects.get(pk=AddrId)
			confirmAddr.pk = None
			confirmAddr.is_saved = False
			confirmAddr.save()
			orderDict = {}
			for odItem in orderdt:
				sellerId = odItem.product.seller.email
				if sellerId in orderDict.keys():
					orderDict[sellerId].append(odItem)
				else:
					orderDict[sellerId] = [odItem,]
			print('THIS IS ORDERDT : {} This is OderDICT {}'.format(orderdt, orderDict))
			newOrder = subscriptionOrder()
			newOrder.date_sub_placed = datetime.datetime.now()
			newOrder.customer = currUser
			newOrder.save()
			orderTotal = 0
			for seller, odItems in orderDict.items():
				print('THIS IS SELLER {} THIS IS ITEMS {}'.format(seller, odItems))
				for item in odItems:
					print("$$$$$$",item.start_date)
					orderTotal += item.get_price
					item.shipping_address = confirmAddr
					item.product_name = item.product.title
					item.cust_name = currUser.name
					item.date_placed = datetime.datetime.now()
					item.next_delivery_date = item.start_date
					item.seller_name = item.product.seller.email
					item.seller_address = item.product.seller.address
					item.is_placed = True
					item.sub_order = newOrder
					item.save()
				#temporarily mov for delivery is 10000
				if orderTotal < 10000:
					orderTotal += 101 #101 is delivery charge
				else:
					newOrder.free_delivery=True
				newOrder.total = orderTotal
				newOrder.payment_method = payment_method
				newOrder.billing_freq = billing_frequency
				
				counter = 1
				if billing_frequency == "weekly":
					counter=7
				elif billing_frequency == "monthly":
					counter=30
				elif billing_frequency == "quarterly":
					counter=90
				newOrder.next_billing_date = datetime.date.today()+datetime.timedelta(days=counter)
				newOrder.save()
			if payment_method == 'prepaid':
				currUser = detail.objects.filter(email=request.user.email).first()
				currWallet = user_wallet.objects.filter(user=currUser).first()
				
				# sellerObj = detail.objects.filter(email="raymond@raymond.in").first()
				# obj = wallet_transaction(wallet=currWallet,transaction_amount=float(newOrder.total), receiving_user=sellerObj, transactionType="Deduct")
				if currWallet.amount >= counter*(newOrder.total):
					# currWallet.amount = currWallet.amount - newOrder.total
					# obj.transaction_status = "SUCCESSFUL"
					# obj.payment_method = "Wallet"
					# obj.is_successful = True
					# obj.save()
					# currWallet.save()
					return redirect('mysubscriptions')
				else:
					diff = counter*(newOrder.total) - currWallet.amount
					order_amount = newOrder.total
					for item in orderdt:
						item.is_placed = False
						item.save()
					newOrder.delete()
					message = "Add atleast Rs."+str(diff)+" to proceed with weekly prepaid plan."
					messages.add_message(request, messages.INFO, message)
					return redirect('add_money')
			if payment_method == "onspot":
				newOrder.billing_freq = "daily"
				newOrder.next_billing_date = datetime.date.today()+datetime.timedelta(days=1)
				newOrder.save()
			return redirect('mysubscriptions')
		return render(request, "cart/select_address.html", {'addressform':addressform, 'addressdata':addressdt})
	else:
		return redirect('login_page')

def my_subscriptions(request):
	if request.user.is_authenticated:
		# checkSubOrders()  #for testing
		currUser = detail.objects.filter(email=request.user.email).first()
		all_sub_orders = subscriptionOrder.objects.filter(customer=currUser).order_by('-id')
		suborderdt = []
		category = []
		for suborder in all_sub_orders:
			odItems = subscriptionOrderItem.objects.filter(sub_order=suborder).order_by('-product')
			tempItems = []
			for item in odItems:
				if item.product.product_Category.first() not in category:
					category.append(item.product.product_Category.first())
					
				tempItems.append(item)
			suborderdt.append([suborder,tempItems])
		
		category.sort(key = lambda i:i.name)
		return render(request, "cart/my_subscriptions.html", {"orderdata": suborderdt, "categories":category})
	else:
		return redirect('login_page')

def editSubOrder(request,sub_orderID):
	currUser = detail.objects.filter(email=request.user.email).first()
	if request.user.is_authenticated:
		subOrder = subscriptionOrder.objects.filter(id=sub_orderID, customer=currUser).first()
		if request.method == "POST":
			if request.POST.get('action') == "stop":
				id = request.POST.get('Oid')
				odItem = subscriptionOrderItem.objects.get(pk=id)
				if odItem.stop_next == True:
					odItem.stop_next = False
					odItem.next_delivery_date = datetime.date.today() + timedelta(days=1)
				else:
					odItem.stop_next = True
					odItem.next_delivery_date = None
				odItem.save()
				subOrder = odItem.sub_order
				orderTotal = 0
				odItems = subscriptionOrderItem.objects.filter(customer=currUser, sub_order=subOrder, is_Cancelled = False, stop_next=False)
				print("length = ",len(odItems))
				if len(odItems)==0:
					subOrder.total = 0
					subOrder.save()
				else:
					subOrder.is_Cancelled = False
					for item in odItems:
						orderTotal += item.amount
					if orderTotal < 10000:
						orderTotal += 101 #101 is delivery charge
					subOrder.total = orderTotal
					subOrder.last_updated = datetime.datetime.now()
					subOrder.save()
				return JsonResponse({"stopped" : True})
			if request.POST.get('action') == "update":
				id = request.POST.get('itemID')
				odItem = subscriptionOrderItem.objects.get(pk=id)
				odItem.quantity = int(request.POST.get('quantity'))
				odItem.end_date = request.POST.get('end_date')
				odItem.interval = int(request.POST.get('interval'))
				odItem.save()
				odItem.amount = odItem.get_price
				odItem.save()
				subOrder = odItem.sub_order
				orderTotal = 0
				odItems = subscriptionOrderItem.objects.filter(customer=currUser, sub_order=subOrder, is_Cancelled = False, stop_next=False)
				print("length = ",len(odItems))
				if len(odItems)==0:
					subOrder.is_Cancelled = True
					subOrder.total = 0
					subOrder.save()
				else:
					for item in odItems:
						orderTotal += item.amount
					if orderTotal < 10000:
						orderTotal += 101 #101 is delivery charge
					subOrder.total = orderTotal
					subOrder.last_updated = datetime.datetime.now()
					subOrder.save()
				print("********",request.POST)
				return redirect('mysubscriptions')
			if request.POST.get('action') == "delete":
				print(subOrder)
				orderTotal = 0
				Oid = request.POST.get('Oid')
				Oitem = subscriptionOrderItem.objects.filter(pk=Oid).first()
				Oitem.is_Cancelled = True
				Oitem.save()
				odItems = subscriptionOrderItem.objects.filter(customer=currUser, sub_order=subOrder, is_Cancelled = False, stop_next=False)
				print("length = ",len(odItems))
				if len(odItems)==0:
					subOrder.is_Cancelled = True
					subOrder.total = 0
					subOrder.save()
				else:
					for item in odItems:
						orderTotal += item.amount
					if orderTotal < 10000:
						orderTotal += 101 #101 is delivery charge
					subOrder.total = orderTotal
					subOrder.last_updated = datetime.datetime.now()
					subOrder.save()
				print("returning")
				return JsonResponse({"deleted" : True})
		
		else:
			# if subOrder.is_Cancelled: 
			#     return redirect('myorders')
			if subOrder and subOrder.status == "Accepted":
				suborderdt = []
				subodItems = subscriptionOrderItem.objects.filter(sub_order=subOrder, is_Cancelled = False).order_by('product_name')
				category = []
				tempItems = []
				for item in subodItems:
					tempItems.append(item)
					if item.product.product_Category.first() not in category:
						category.append(item.product.product_Category.first())
				suborderdt.append([subOrder,tempItems])
				print(f'orderdt: {suborderdt}')
				category.sort(key = lambda i:i.name)
				return render(request, "cart/edit_subscription.html", {"orderdata": suborderdt, "categories":category})
			# return render(request, "cart/edit_subscription.html")
 
# scheduled function at 10:00 PM every day
def checkSubOrders():
	print("runs!!!!!!!!!!")
	today = date.today()
	all_sub_orderItems =  subscriptionOrderItem.objects.filter(is_placed=True, is_Cancelled=False, end_date__gt=today, stop_next=False)
	for sub_item in all_sub_orderItems:
		if sub_item.next_delivery_date == today + timedelta(days = 1):
			newOrderItem = OrderItem()
			newOrderItem.customer = sub_item.customer
			newOrderItem.cust_name = sub_item.customer.name
			newOrderItem.product = sub_item.product
			newOrderItem.product_name = sub_item.product_name
			newOrderItem.shipping_address = sub_item.shipping_address
			newOrderItem.date_placed = datetime.datetime.now()
			newOrderItem.seller_name = sub_item.product.seller.name
			newOrderItem.seller_address = sub_item.product.seller.address
			newOrderItem.quantity = sub_item.quantity
			newOrderItem.total = sub_item.amount
			newOrderItem.size_color = sub_item.product.size_color_quantity_set.all().first()
			newOrderItem.size_name = str(sub_item.product.size_color_quantity_set.all().first().size) + str(sub_item.product.size_color_quantity_set.all().first().unit)
			newOrderItem.size_cost = sub_item.product.size_color_quantity_set.all().first().price
			newOrderItem.is_placed = True
			newOrderItem.save()
			sub_item.next_delivery_date = sub_item.next_delivery_date + timedelta(days=sub_item.interval)
			sub_item.save()
			newOrder = Order()
			newOrder.date_order_placed = datetime.datetime.now()
			newOrder.customer = newOrderItem.customer
			newOrder.total = newOrderItem.total
			newOrder.payment_method = "Subscription "+sub_item.sub_order.payment_method
			if newOrderItem.total >= 10000:
				newOrder.free_delivery = True
			else:
				newOrder.total = newOrderItem.total+101 #here delivery charge is 101
				newOrder.free_delivery = False
			newOrder.status="Pending for customer"
			newOrder.is_sub_order=True
			newOrder.sub_order = sub_item.sub_order
			newOrder.save()
			if sub_item.sub_order.payment_method == "prepaid":
				currWallet = user_wallet.objects.filter(user=sub_item.customer).first()
				sellerObj=detail.objects.filter(email=sub_item.product.seller.email).first()
				obj = wallet_transaction(wallet=currWallet,transaction_amount=float(newOrder.total), receiving_user=sellerObj, transactionType="Deduct")
				if currWallet.amount >= newOrder.total:
					currWallet.amount = currWallet.amount - newOrder.total
					obj.transaction_status = "SUCCESSFUL"
					obj.payment_method = "Wallet"
					obj.is_successful = True
					newOrder.payment_status = "Paid using wallet"
					print(newOrder)
					newOrder.save()
					obj.save()
					currWallet.save()
			newOrderItem.order = newOrder
			invoice(newOrder,[newOrderItem])
			newOrderItem.save()

	# Generate bills
	all_sub_orders = subscriptionOrder.objects.filter(is_Cancelled=False)
	for sub_order in all_sub_orders:
		order_list = []
		item_list = []
		final_amount = 0
		counter = 1
		if sub_order.billing_freq == "daily":
			counter = 1
		elif sub_order.billing_freq == "weekly":
			counter = 7
		elif sub_order.billing_freq == "monthly":
			counter = 30
		elif sub_order.billing_freq == "quarterly":
			counter = 90
		if sub_order.next_billing_date == today + timedelta(days = 1):
			# Currently not checking order status if it is delivered/completed or not bill is being generated for placed orders as well.
			orders = Order.objects.filter(is_sub_order=True, sub_order=sub_order, date_order_placed__range=(today - timedelta(days = counter-1),today + timedelta(days = 1))).order_by('-date_order_placed')
			print("ORDERS = ",orders)
			for order in orders:
				order_list.append(order)
			print("ORDERS_list = ",order_list)
			for order in order_list:
				final_amount+=order.total
				items = order.get_all_items()
				item_list.append(items)
			print("item_list***** ",item_list)
			newBill = subscriptionBill()
			newBill.sub_order = sub_order
			newBill.billing_date = sub_order.next_billing_date
			newBill.final_amount = final_amount
			newBill.save()
			sub_bill(newBill,sub_order,order_list,item_list)
			sub_order.next_billing_date = today + timedelta(days = counter)
			sub_order.save()

def subscriptionBills(request):
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		sub_order = subscriptionOrder.objects.filter(customer=currUser)
		bills=subscriptionBill.objects.all()
		data=[]
		for i in sub_order:
			for bill in bills:
				if(bill.sub_order == i):
					data.append(bill)
		context = {
			'data':data,
		}
		return render(request, "cart/subBills.html", context=context)

def calendar_view(request):
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		all_sub_orders = subscriptionOrder.objects.filter(customer=currUser).order_by('-id')
		suborderdt = []
		category = []
		obj = []
		for suborder in all_sub_orders:
			# getting all the suborder items
			odItems = subscriptionOrderItem.objects.filter(sub_order=suborder).order_by('-product') 
			tempItems = []
			for item in odItems:
				start_delivery = None
				end_delivery = None
				tempItems.append(item)
				#initial order frequency will be 0, since item is delivered on start date
				frequency = 0
				start = item.start_date + timedelta(days=1)
				end = item.end_date+ timedelta(days=1)

				while(start<=end):
					# for getting delivery on each day
					 
					delivery = item.start_date + timedelta(days=frequency)
					start_delivery = str(delivery)+" "+item.shifts
					end_delivery = str(datetime.datetime.strptime(str(delivery)+" "+item.shifts,"%Y-%m-%d %H:%M")+datetime.timedelta(minutes=45))
					if (delivery <= end):
						obj.append({
							'description':"subscribe",
							'title':item.product_name+" x "+str(item.quantity),
							'start':start_delivery,
							'end':end_delivery,
							'color':"red",
							'type':"subscribe",
							'classNames':'subscribe'
						})
					frequency=frequency+item.interval
					start = start + timedelta(days=1)
			suborderdt.append(tempItems)

		all_rental_orders = rental_Order.objects.filter(customer=currUser).order_by('-id')
		rentalorderdt = []
		for rentalorder in all_rental_orders:
			odItems = rental_OrderItem.objects.filter(rent_order=rentalorder).order_by('-start_date')
			tempItems = []
			for item in odItems:
				obj.append({
							'id':'re',
							'description':"rent",
							'title':item.product.title+" x "+str(item.quantity),
							'start':item.start_date.strftime("%Y-%m-%d"),
							'end':item.end_date.strftime("%Y-%m-%d"),
							'color':"blue",
							'type':"rent",
							'classNames':'rent'
						})     
				tempItems.append(item)
			rentalorderdt.append(tempItems)
		print(obj)
		context = {
			"rentorderdata":rentalorderdt,
			"orderdata":suborderdt,
			"obj":obj,
		}
		category.sort(key = lambda i:i.name)
		return render(request, "cart/calendar.html",context=context)

def order_to_be_delivered(request):
	if request.user.is_authenticated:
		user = detail.objects.get(email=request.user.email)
		order_to_be_delivered = selected_distribution_centers.objects.filter(selected_distribution_center__isnull=True, user=user)
		orders_to_be_delivered = []
		for i in list(order_to_be_delivered):
			print(i.order_item.id)
			print(user)
			if i.user == user:
				orders_to_be_delivered.append(i)
				print(i)
		print(orders_to_be_delivered)
		return render(request, 'cart/order_to_be_delivered.html', {'orders': order_to_be_delivered})


def select_distribution_centers(request, order_id):
		distribution_centers = distribution_center.objects.filter(user=detail.objects.get(email=request.user.email))
		order = OrderItem.objects.get(id=order_id)
		print(distribution_centers)
		center_list = []
		for i in distribution_centers:
			print(i.address)
		print(request.POST)
		
		if request.method == "POST":
			delivery_center = []
			# delivery_centers=request.POST.get('center')
			node1 = request.POST.get('node1')
			delivery_center.append(node1)
			if 'node2' in request.POST:
				node2 = request.POST.get('node2')
				print(node2)
				delivery_center.append(node2)
			if 'node3' in request.POST:
				node3 = request.POST.get('node3')
				print(node3)
				delivery_center.append(node3)
			if 'node4' in request.POST:
				node4 = request.POST.get('node4')
				print(node4)
				delivery_center.append(node4)
			if 'node5' in request.POST:
				node5 = request.POST.get('node5')
				print(node5)
				delivery_center.append(node5)
			# node3 = request.POST.get('node3')
			   
			delivery = []
			print(delivery_center)
			for i in delivery_center:
				delivery.append(distribution_center.objects.get(id=int(i)))
			print(delivery)
			distance = 0
			time = 0
			days = 0
			for i in range(len(delivery)-1):
				curr_loc = delivery[i].coordinates.split(',')
				curr_loc.reverse()
				next_loc = delivery[i+1].coordinates.split(',')
				next_loc.reverse() 
				print(curr_loc, next_loc)
				dist, t = get_distance_and_time(curr_loc, next_loc) 	# Time is in mins
				distance += dist
				time += t
				# days += int(time / 1440) 
			hours = time / 60 	
			print(hours)
			for i in delivery:	
				hours += i.delay_time 
			days = int(math.ceil(hours/24))
			print(days)
			delivery_date = date.today() + timedelta(days=days)
			print(delivery_date)
			order_to_be_delivered = selected_distribution_centers.objects.get(order_item=OrderItem.objects.get(id=order_id))
			order_to_be_delivered.selected_distribution_center.add(*delivery)
			order_to_be_delivered.expected_delivery_date = delivery_date 
			order_to_be_delivered.save()
			return redirect('/userdetail/vendor_profile')
		print(order.seller_address)
		data = {
			'centers': list(distribution_centers),
			'order_item': order
		}
		return render(request,"cart/selected_distribution_centers.html", data)

def set_delivery_runner(request, runner_id):
	runner = detail.object.get(id=runner_id)
	all_runners_orders = pick_and_deliver_order.objects.filter(runner = runner)
	todays_orders = pick_and_deliver_order.objects.filter(runner = runner, pickup_date = datetime.date.today())
	deliver_time = todays_orders.objects.all().order_by('delivery_time')
	runner_loc = runner.current_loc_coord
	runner_loc.reverse()
	pickup_locs = []
	drop_locs = []
	pickup_drop_dist = []
	runner_pickup_dist = []
	runner_drop_dist = []
	for i in deliver_time:
		pickup_locs.append([i, i.pickup_coords])
		drop_locs.append([i, i.drop_coords])
		pickup = i.pickup_coords.split(',')
		pickup.reverse()
		o_dist, o_time = get_distance_and_time(pickup, drop)
		drop = i.drop_coords.split(',')
		drop.reverse()
		p_dist, p_time = get_distance_and_time(runner_loc, pickup)
		pickup_drop_dist.append([i, o_dist, o_time])
		runner_pickup_dist.append([i, p_dist, p_time])
		d_dist, d_time = get_distance_and_time(runner_loc, drop)
		runner_drop_dist.append([i, d_dist + o_dist, d_time + o_time])
	sorted_pickup_drop_dist = sorted(pickup_drop_dist, key = lambda i: i[1])
	sorted_runner_pickup_dist = sorted(runner_pickup_dist, key = lambda i: i[1])

	min_pick_time_list = []
	for i in pickup_locs:
		min_time = []
		pickup_loc1 = i[1].split(',')
		pickup_loc1.reverse()
		drop = i.drop_coords.split(',')
		drop.reverse()
		for j in pickup_locs:
			pickup_loc2 = j[1].split(',')
			pickup_loc2.reverse()
			dist, time = get_distance_and_time(pickup_loc1, pickup_loc2)
			dist2, time2 = get_distance_and_time(pickup_loc2, drop)
			min_time.append([i, j, time + time2])
		min_time.sort(key=lambda i: i[2])
		min_pick_time_list.append(min_time[0])

	final_list = []
	for i in runner_drop_dist:
		for j in min_pick_time_list:
			if i[0] == j[0]:
				if i[2] < j[2]:
					final_list.append(['p', j[0]])
				else:
					final_list.append(['d', i[0]])
	return render(request, 'runner_display_orders.html', {'orders': final_list})

print((datetime.datetime.combine(datetime.date(1,1,1), datetime.datetime.now().time()) + datetime.timedelta(minutes=10)).time())