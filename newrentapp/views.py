from django.shortcuts import render, redirect
from product.models import product, size_color_quantity
from userdetail.models import detail
from .models import *
from cartnew.forms import shipping_address_form
from wallet.models import *
from django.contrib import messages
from .generate_rent_bill import invoice
from cartnew.models import coupons, coupons_applied
# Create your views here.
def rentProductListView(request):
	rent_product_list=product.objects.filter(is_rent=True)

	context={
		'objects':rent_product_list,
	}

	return render(request,'rentapp/rent_product_listView.html',context)

def rentProductDetailView(request,slug):
	rentProduct=product.objects.get(is_rent=True,slug=slug)
	currUser = detail.objects.get(email=request.user.email)
	if request.method == "POST" and request.user.is_authenticated:
		size_color_id = request.POST.get('size-color')
		size_color_obj = size_color_quantity.objects.get(id=size_color_id)
		rent_product = size_color_obj.linked_product
		quantity = request.POST.get("quantity")
		start_date = request.POST.get("start_date")
		end_date = request.POST.get("end_date")
		price = size_color_obj.price
		customer = currUser
		rent_plans = rental_Plan.objects.filter(lower_limit_price__lt=price+1, upper_limit_price__gte=price).first()
		rentOdItem = rental_OrderItem()
		rentOdItem.product = rent_product
		rentOdItem.quantity = quantity
		rentOdItem.start_date = start_date
		rentOdItem.end_date = end_date
		rentOdItem.price = price
		rentOdItem.rent_plan = rent_plans
		rentOdItem.size_color_quantity = size_color_obj
		rentOdItem.customer = customer
		rentOdItem.amount = rentOdItem.base_rate()
		rentOdItem.save()
		message = str(rent_product)+" has been added to Cart"
		messages.add_message(request, messages.INFO, message)
		return redirect("products_on_rent")
		

	context={
		'object':rentProduct,
	}
	return render(request,'rentapp/rent_product_detail_view.html',context)

def rentCart(request):
	currUser = detail.objects.filter(email=request.user.email).first()
	if request.user.is_authenticated and request.method=="GET":
		rentItems = rental_OrderItem.objects.filter(is_placed=False, customer=currUser,is_Cancelled=False) 
		rentCartItems=0
		rentCartTotal=0
		for item in rentItems:
			price = item.amount
			rentCartItems += item.quantity 
			rentCartTotal += item.get_total_amount()
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
				if curr_coupon and curr_coupon.min_amount <= rentCartTotal:
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
						discount = rentCartTotal * curr_coupon.discount/100
				single_prod_sum = 0
				for item in rentCartItems:
					single_prod_sum += item.total/item.quantity
				for item in rentCartItems:
					print(item.total, "item total before discount")
					if curr_coupon.is_category_coupon:
						if item.product.product_Supercategory == curr_coupon.category:
							discounted_price = (item.total/rentCartTotal)*discount	# TODO: calculating discounted price
							item.total -= discounted_price
							item.save()	
					else:
						discounted_price = (item.total/rentCartTotal)*discount
						item.total -= discounted_price
						item.save()	
				rentCartTotal -= curr_coupon.discount_amount
		context = {
			"cartdata":rentItems,
			"cartTotal":rentCartTotal,
			"cartItems":rentCartItems,
			'coupons': available_coupons,
			'coupon_applied': coupon_applied,
			'code': code,
			'discount': discount,
		}
		return render(request,"cart/rentCart.html", context=context)

def rent_select_address(request):
	if request.user.is_authenticated:
		print('THIS IS POST: ', request.POST)
		# Basic Page View
		currUser = detail.objects.filter(email=request.user.email).first()
		rentItems = rental_OrderItem.objects.filter(customer=currUser, is_placed=False, is_Cancelled = False)
		userAddresses = ShippingAddress.objects.filter(user = currUser, is_saved=True)
		addressdt = []
		if userAddresses:
			for address in userAddresses:
				addressform = shipping_address_form(instance=address, prefix=address.id)
				addressdt.append([address,addressform])
		if not rentItems:
			return redirect('rentCart')
		addressform = shipping_address_form()
		# Addnewform Post handling
		if request.POST.get('new_address'):
			print(f"This is post data: {request.POST}")
			editedAddressForm = shipping_address_form(request.POST)
			if editedAddressForm.is_valid():
				savedAddress = editedAddressForm.save()
				savedAddress.user = currUser
				savedAddress.save()
			return redirect('rent_selectaddress')
		# EDIT ADDRESS FORM POST HANDLING
		if request.POST.get('update_address'):
			pref = request.POST.get('update_address')
			editAddInstance = ShippingAddress.objects.get(pk=pref)
			print("THSI IS INSTANCE: ", editAddInstance)
			editedForm = shipping_address_form(request.POST, instance=editAddInstance, prefix=pref)
			if editedForm.is_valid():
				editedForm.save()
			return redirect('rent_selectaddress')
		
		# Go To Order Summary Page
		if request.POST.get('AddrId'):
			AddrId = request.POST.get('AddrId')
			rentItems = rental_OrderItem.objects.filter(customer=currUser, is_placed=False, is_Cancelled = False)
			toAddress = ShippingAddress.objects.get(pk=AddrId)
			rentCartTotal = 0
			rentCartSecurity = 0
			for item in rentItems:
				price = item.amount
				rentCartSecurity += item.get_total_price()
				rentCartTotal += item.get_total_amount()
			return render(request, "cart/rent_confirm.html", {'cartdata':reversed(rentItems), 'toAddress':toAddress, 'cartTotal':rentCartTotal, 'security':rentCartSecurity})

		# Place a new rental
		if request.POST.get('confirm_rental'):
			payment_method = request.POST.get('payment_method')
			if not payment_method == "onspot":
				billing_frequency = request.POST.get('bill_freq')
			AddrId = request.POST.get('confirm_rental')
			orderdt = rental_OrderItem.objects.filter(customer=currUser, is_placed=False, is_Cancelled = False)
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
			newOrder = rental_Order()
			newOrder.date_rental_placed = datetime.datetime.now()
			newOrder.customer = currUser
			newOrder.save()
			security = 0
			chargeable = 0
			for seller, odItems in orderDict.items():
				print('THIS IS SELLER {} THIS IS ITEMS {}'.format(seller, odItems))
				for item in odItems:
					security += item.get_total_price()
					chargeable += item.get_total_amount()
					item.shipping_address = confirmAddr
					item.date_placed = datetime.datetime.now()
					item.is_placed = True
					item.rent_order = newOrder
					item.save()
				#temporarily mov for delivery is 10000
				if chargeable < 10000:
					chargeable += 101 #101 is delivery charge
				else:
					newOrder.free_delivery=True
				newOrder.security_amount = security
				newOrder.chargable_amount = chargeable
				newOrder.payment_method = payment_method
				if not payment_method == "onspot":
					newOrder.billing_freq = billing_frequency
					counter = 1
					if billing_frequency == "weekly":
						counter=7
					elif billing_frequency == "monthly":
						counter=30
					newOrder.next_billing_date = datetime.date.today()+datetime.timedelta(days=counter)
				else:
					newOrder.next_billing_date = datetime.date.today()
				newOrder.save()
			if payment_method == 'prepaid':
				currUser = detail.objects.filter(email=request.user.email).first()
				currWallet = user_wallet.objects.filter(user=currUser).first()
				
				# sellerObj = detail.objects.filter(email="raymond@raymond.in").first()
				obj = wallet_transaction(wallet=currWallet,transaction_amount=float(newOrder.security_amount), transactionType="Block", receiving_user=currUser)
				if currWallet.amount >= counter*(newOrder.security_amount):
					currWallet.amount = currWallet.amount - newOrder.security_amount
					obj.transaction_status = "SUCCESSFUL"
					obj.payment_method = "Wallet"
					currWallet.blockedAmount += newOrder.security_amount
					obj.is_successful = True
					obj.save()
					currWallet.save()
					for item in orderdt:
						item.isPaid = True
						item.save()
				else:
					diff = counter*(newOrder.security_amount) - currWallet.amount
					order_amount = newOrder.security_amount
					for item in orderdt:
						item.is_placed = False
						item.save()
					newOrder.delete()
					message = "Add atleast Rs."+str(diff)+" to proceed with weekly prepaid plan."
					messages.add_message(request, messages.INFO, message)
					return redirect('add_money')
			invoice(newOrder,orderdt)  
			return redirect('myrentals')
		return render(request, "cart/select_address.html", {'addressform':addressform, 'addressdata':addressdt})
	else:
		return redirect('login_page')

def my_rentals(request):
	if request.user.is_authenticated:
		currUser = detail.objects.filter(email=request.user.email).first()
		all_rental_orders = rental_Order.objects.filter(customer=currUser).order_by('-id')
		rentalorderdt = []
		category = []
		for rentalorder in all_rental_orders:
			odItems = rental_OrderItem.objects.filter(rent_order=rentalorder).order_by('-product')
			tempItems = []
			for item in odItems:
				if item.product.product_Category.first() not in category:
					category.append(item.product.product_Category.first())
					
				tempItems.append(item)
			rentalorderdt.append([rentalorder,tempItems])
		
		category.sort(key = lambda i:i.name)
		return render(request, "cart/my_rentals.html", {"orderdata": rentalorderdt, "categories":category})
	else:
		return redirect('login_page')