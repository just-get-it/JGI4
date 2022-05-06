from django.db import models
from product.models import product, size_color_quantity, super_category
from userdetail.models import *
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField

# Create your models here.


def upload_image_path(instance, filename):
	new_filename = random.randint(1, 13516546431654)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(
		new_filename=new_filename, ext=ext)
	return "local/orders/orderitems/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename
	)


def invoice_path(instance, filename):
	new_filename = random.randint(1, 13516546431654)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=name, ext=ext)
	return "local/orders/invoices/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename
	)


ORDER_STATUS = (
	('Accepted', 'ACCEPTED'),
	('Packed', 'PACKED'),
	('Dispatched', 'DISPATCHED'),
	('Reached Nearby', 'REACHED NEARBY'),
	('Out for Delivery', 'OUT FOR DELIVERY'),
	('Delivered', 'DELIVERED'),
	('Returned', 'RETURNED'),
)

class subscriptionOrder(models.Model):
	date_sub_placed = models.DateTimeField(null=True)
	customer = models.ForeignKey(detail, null=True, on_delete=models.SET_NULL)
	total = models.FloatField(default=0, null=True)
	payment_method = models.CharField(max_length=200, null=True)
	# bill_frequency = models.CharField(max_length=200, null=True)
	status = models.TextField(default='Accepted')
	free_delivery = models.BooleanField(default=False)
	is_Cancelled = models.BooleanField(default=False)
	billing_freq =models.CharField(max_length=256, blank=True)
	next_billing_date = models.DateField(null=True, blank=True)
	last_updated = models.DateTimeField(blank=True,null=True)
	def get_all_orders(self):
		res=[]
		orders = self.order_set.all()
		for order in orders:
			res.append(order)
		return res

class Order(models.Model):
	date_order_placed = models.DateTimeField(null=True)
	customer = models.ForeignKey(detail, null=True, on_delete=models.SET_NULL)
	total = models.FloatField(default=0, null=True)
	payment_method = models.CharField(max_length=200, null=True)
	payment_status = models.CharField(max_length=200, null=True, blank=True)
	transactionID = models.CharField(max_length=200, null=True, blank=True)
	invoice = models.FileField(upload_to=invoice_path, null=True)
	razorpay_payment_id = models.CharField(max_length=256, null=True, blank=True)
	razorpay_order_id = models.CharField(max_length=256, null=True, blank=True)
	razorpay_signature = models.CharField(max_length=256, null=True, blank=True)
	complete = models.BooleanField(default=False, blank=False)
	status = models.TextField(choices=ORDER_STATUS, default='Accepted')
	free_delivery = models.BooleanField(default=False)
	is_Cancelled = models.BooleanField(default=False)
	is_sub_order = models.BooleanField(default=False)
	sub_order = models.ForeignKey(subscriptionOrder, on_delete=models.CASCADE, null=True, blank=True)

	# def __str__(self):
	#     return str(self.customer)+" "+str(self.total)+" "+self.payment_method+" id-"+str(self.id)

	def get_all_items(self):
		res = []
		orderItems = self.orderitem_set.all()
		for orderItem in orderItems:
			res.append(orderItem)
		return res

	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


@receiver(models.signals.post_delete, sender=Order)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	if instance.invoice:
		if os.path.isfile(instance.invoice.path):
			os.remove(instance.invoice.path)


class ShippingAddress(models.Model):
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(detail, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	shipping_address = models.CharField(max_length=255)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	pin_code = models.CharField(max_length=200)
	is_saved = models.BooleanField(default=True)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	customer = models.ForeignKey(detail, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(product, on_delete=models.CASCADE, null=True)
	product_name = models.CharField(max_length=255, null=True)
	shipping_address = models.ForeignKey(
		ShippingAddress, on_delete=models.SET_NULL, null=True)
	cust_name = models.CharField(max_length=200, null=True)
	date_placed = models.DateTimeField(null=True)
	seller_name = models.CharField(max_length=200, null=True)
	seller_address = models.CharField(max_length=255, null=True)
	size_color = models.ForeignKey(
		size_color_quantity, on_delete=models.SET_NULL, null=True)
	size_name = models.CharField(max_length=255, null=True)
	size_cost = models.FloatField(null=True)
	quantity = models.IntegerField(null=True)
	total = models.FloatField(null=True)
	is_placed = models.BooleanField(default=False)
	is_Cancelled = models.BooleanField(default=False)
	days_for_delivery = models.IntegerField(null=True, blank=True)
	
	def get_product(self):
		if(self.is_placed):
			return self.product

	@property
	def get_price(self):
		price = self.size_color.price
		if self.product.offer:
			mrp = price
			offer = self.product.offer
			price = mrp - (mrp * offer // 100)
		return price

	@property
	def set_total(self):
		total = float(self.size_color.price) * float(self.quantity)

		if self.product.offer:
			offer = float(self.product.offer)
			mrp = total
			total = mrp - (mrp * offer // 100)
		self.total = total
		return total

	@property
	def set_b2b_total(self):
		total = int(self.product.price) * int(self.quantity)
		if int(self.quantity) < self.product.Moq_range1.lower:
			if self.product.B2Boffer:
				offer = float(self.product.B2Boffer)
				mrp = total
				total = mrp - (mrp * offer // 100)
		elif product.Moq_range1 and int(self.quantity) >= self.product.Moq_range1.lower and int(self.quantity) <= self.product.Moq_range1.upper:
			offer = float(self.product.Moq_discount1)
			mrp = total
			total = mrp - (mrp * offer // 100)
		elif product.Moq_range2 and int(self.quantity) >= self.product.Moq_range2.lower and int(self.quantity) <= self.product.Moq_range2.upper:
			offer = float(self.product.Moq_discount2)
			mrp = total
			total = mrp - (mrp * offer // 100)
		elif product.Moq_range3 and int(self.quantity) >= self.product.Moq_range3.lower:
			offer = float(self.product.Moq_discount3)
			mrp = total
			total = mrp - (mrp * offer // 100)

		self.total = total
		return total


class wishlist(models.Model):
	customer = models.ForeignKey(detail, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(product, on_delete=models.CASCADE, null=True)



class subscriptionOrderItem(models.Model):

	SHIFTS = (
		('07:00', 'Morning'),
		('13:00', 'Afternoon'),
		('19:00', 'Evening')
	)

	product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
	product_name = models.CharField(max_length=200, default='default')
	quantity = models.IntegerField()
	# frequency = models.ForeignKey(order_frequency, on_delete=models.CASCADE)
	interval = models.IntegerField(default=7)
	start_date = models.DateField()
	end_date = models.DateField()
	shifts = models.CharField(max_length=10,choices=SHIFTS, default='07:00')
	remark = models.CharField(max_length=300, default='-')
	customer_email = models.CharField(max_length=100)
	vendor_email = models.CharField(max_length=100)
	refundable_packing_charge = models.BooleanField(default=False)
	# Allows to stop the subscription for next time.
	is_placed = models.BooleanField(default=False)
	stop_next = models.BooleanField(default=False)
	isPaid = models.BooleanField(default=False)
	amount = models.FloatField()
	customer = models.ForeignKey(detail, on_delete=models.DO_NOTHING, null=True)
	sub_order = models.ForeignKey(subscriptionOrder, on_delete=models.SET_NULL, null=True, blank=True)
	is_Cancelled = models.BooleanField(default=False)
	shipping_address = models.ForeignKey(
		ShippingAddress, on_delete=models.SET_NULL, null=True)
	next_delivery_date = models.DateField(blank=True, null=True)
	def __str__(self):
		return "Subscription "+self.product_name+" "+str(self.id)

	@property
	def get_price(self):
		mrp = self.product.price
		offer = self.product.subscription_discount
		final_price = (mrp - (mrp * offer // 100))*(self.quantity)
		return final_price

class subscriptionBill(models.Model):
	sub_order = models.ForeignKey(subscriptionOrder, on_delete=models.CASCADE)
	billing_date = models.DateField()
	bill = models.FileField(upload_to="local/subscriptions/invoices/",null=True)
	final_amount = models.FloatField(default=0, null=True)

class Logistics(models.Model):
	CITY_TIERS = (
		('tier_1', 'tier_1'),
		('tier_2', 'tier_2'),
		('tier_3', 'tier_3'),

	)   
	user = models.ForeignKey(detail,on_delete=models.SET_NULL,null=True,blank=True)
	order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL,null=True,blank=True)
	order_curr_location = PlainLocationField(default='13.0352,77.5772', zoom=7)
	city_tier = models.CharField(max_length=10, choices=CITY_TIERS, default='tier_1')
	hubs = models.CharField(max_length=200)
	route_for_delivery = models.CharField(max_length=300)
	days_for_delivery = models.IntegerField()
	Date_of_delivery = models.DateTimeField()

class coupons(models.Model):
	business_model = (
		('product', 'product'),
		('rental', 'rental'),
		('subscription', 'subscription')
	)
	period = (
		('daily', 'daily'),
		('weekly', 'weekly'),
		('monthly', 'monthly'),
		('yearly', 'yearly')
	)
	category = (

	)
	code = models.CharField(max_length=20)
	min_amount = models.IntegerField(default=0)
	discount_percentage = models.IntegerField(default=0, null=True, blank=True)
	discount_amount = models.IntegerField(default=0, null=True, blank=True)
	description = models.CharField(max_length=200)
	disc_type_is_percents = models.BooleanField(default=False)
	one_time_only = models.BooleanField(default=False)
	business_model = models.CharField(choices = business_model, max_length=30, null=True, blank=True, default='product')
	period = models.CharField(choices=period, max_length=30, null=True, blank=True)
	is_category_coupon = models.BooleanField(default=False)
	is_business_model_coupon = models.BooleanField(default=False)
	category = models.ForeignKey(super_category, on_delete=models.SET_NULL, null=True, blank=True)

class coupons_applied(models.Model):
	coupons = models.ForeignKey(coupons, on_delete=models.SET_NULL, null=True, blank=True)
	user = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True, blank=True)
	number_of_usages = models.IntegerField(default=0)

class selected_distribution_centers(models.Model):
	user = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True, blank=True)
	order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True, blank=True)
	selected_distribution_center = models.ManyToManyField(distribution_center, null=True, blank=True)
	expected_delivery_date = models.DateField(null=True, blank=True)