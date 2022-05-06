from django.db import models
import random,os
from django.utils import timezone
# Create your models here.
import datetime
from location_field.models.plain import PlainLocationField

def get_filename_ext(filepath):
	base_name=os.path.basename(filepath)
	name ,ext=os.path.splitext(base_name)
	return name ,ext

def upload_image_path(instance,filename):
	new_filename=random.randint(1,13516546431654)
	name ,ext=get_filename_ext(filename)
	final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "local/b2b/logo/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename
		)


class brand(models.Model):
	name=models.CharField(max_length=255,unique=True)
	activate=models.BooleanField(default=False)


	def __str__(self):
		return self.name





class weekdays(models.Model):
	num=models.IntegerField()
	name=models.CharField(max_length=255)

	def __str__(self):
		return self.name



class Resumes(models.Model):
	email = models.CharField(max_length=255)
	files = models.FileField(upload_to='resumes')
	def __str__(self):
		return self.email

class seller_additional_features(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class staff_additional_features(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class seller_Categories(models.Model):
	name=models.CharField(max_length=255,unique=True)
	holidays=models.ManyToManyField(weekdays,blank=True)
	customer=models.BooleanField(default=False)
	vendor=models.BooleanField(default= False)
	staff=models.BooleanField(default= False)
	buisness_Customer=models.BooleanField(default= False)
	activate_Seller=models.BooleanField(default=False)
	activate_Buisness=models.BooleanField(default=False)
	activate_Staff=models.BooleanField(default=False)
	buisness_Timeline=models.BooleanField(default=False)
	vendor_Timeline=models.BooleanField(default=False)
	b2b_order=models.BooleanField(default=False)
	seller_additional_features = models.ManyToManyField(seller_additional_features, blank=True, null=True)

	def __str__(self):
		return self.name





class staff_Categories(models.Model):
	name=models.CharField(max_length=255,unique=True)
	holidays=models.ManyToManyField(weekdays,blank=True)
	staff_additional_features = models.ManyToManyField(staff_additional_features, blank=True, null=True)

	def __str__(self):
		return self.name



Choices=(
	('H','Head'),
	('M','Manager'),
	('C','Staff')
	)



class detail(models.Model):
	name=models.CharField(max_length=255)
	email=models.EmailField()
	password=models.CharField(max_length=255)
	contact=models.BigIntegerField(null=True,blank=True)
	gender=models.CharField(max_length=255,null=True,blank=True)
	unique_id_for_report = models.CharField(max_length=10,default=1)
	customer=models.BooleanField(default=False)
	fashion_brand=models.BooleanField(default= False)
	brand=models.BooleanField(default= False)
	vendor=models.BooleanField(default= False)
	staff=models.BooleanField(default= False)
	runner=models.BooleanField(default= False)
	buisness_Customer=models.BooleanField(default= False)
	activate_Seller=models.BooleanField(default=False)
	activate_Buisness=models.BooleanField(default=False)
	activate_Staff=models.BooleanField(default=False)
	activate_runner=models.BooleanField(default=False)
	buisness_Timeline=models.BooleanField(default=False)
	vendor_Timeline=models.BooleanField(default=False)
	b2b_order=models.BooleanField(default=False)
	b2b_order_no=models.IntegerField(null=True,blank=True)
	seller_category=models.ForeignKey(seller_Categories,on_delete=models.CASCADE,null=True,blank=True)
	staff_category=models.ForeignKey(staff_Categories,on_delete=models.CASCADE,null=True,blank=True)
	description=models.TextField(null=True,blank=True)
	mission=models.CharField(max_length=255,null=True,blank=True)
	coverimage=models.ImageField(default='default2.jpg', upload_to=upload_image_path,null=True,blank=True)
	image=models.ImageField(default='default.jpg', upload_to=upload_image_path,null=True,blank=True)
	info_update=models.BooleanField(default=False)
	position=models.CharField(max_length=255,choices=Choices,null=True,blank=True)
	# seller_brand=models.ForeignKey(brand,on_delete=models.CASCADE,null=True,blank=True)
	max_quantity=models.IntegerField(default=1)
	average_response_time=models.FloatField(default=0)
	average_time_divi=models.IntegerField(default=0)
	target_response_time=models.IntegerField(default=0)
	last_target=models.DateField(null=True,blank=True)
	last_target1=models.DateField(null=True,blank=True)
	last_target2=models.DateField(null=True,blank=True)
	lead_time=models.IntegerField(default=0)
	lap_lead_time=models.IntegerField(default=0)
	industry=models.CharField(max_length=255,null=True,blank=True)
	address=models.TextField(null=True,blank=True)
	no_of_working=models.IntegerField(default=0)
	last_activity=models.DateTimeField(null=True,blank=True)
	dept=models.CharField(max_length=255,null=True,blank=True)
	sub_dept=models.CharField(max_length=255,null=True,blank=True)
	reg_no=models.IntegerField(default=0)
	excel_attribute1=models.CharField(max_length=255,null=True,blank=True)
	excel_attribute2=models.CharField(max_length=255,null=True,blank=True)
	excel_attribute3=models.CharField(max_length=255,null=True,blank=True)
	user_otp=models.CharField(max_length=255,null=True,blank=True)
	user_otp_time=models.DateTimeField(null=True,blank=True)
	user_otp_key=models.TextField(null=True,blank=True)
	user_otp_verify=models.DateTimeField(null=True,blank=True)
	t_and_c=models.TextField(null=True,blank=True)
	budget_hit_rate=models.BigIntegerField(default=100000)
	run_rate=models.IntegerField(null=True,blank=True)
	telegram_id=models.IntegerField(default=0)
	
	Landmark=models.CharField(max_length=300,null=True,blank=True)
	service=models.NullBooleanField(null=True,blank=False,default=False)
	
	vendor_name = models.CharField(max_length=255,null=True, blank=True)
	#### Planner App Fields
	student = models.NullBooleanField(null=True, default=False, blank=True)
	# project_id =models.IntegerField(null=True, blank=True)
	# completion=models.IntegerField(default=0, null=True)
	# timeline_filled=models.BooleanField(default=False)
	# inter=models.BooleanField(default=True)
	# college=models.CharField(max_length=255, null=True, blank=True)
	# skill=models.CharField(max_length=500, null=True, blank=True)
	# location=models.CharField(max_length=255, null=True, blank=True)
	current_loc_coord = PlainLocationField(default='13.0352,77.5772', zoom=7)

	def __str__(self):
		return self.email
	@property
	def is_logistics(self):
		if self.staff:
			logi=staff_Categories.objects.filter(name="Logistic").first()
			if self.staff_category==logi:
				return True
			else:
				return False
		else:
			return False

	@property
	def is_logistics_vendor(self):
		if self.vendor:
			logi=seller_Categories.objects.filter(name="Logistic Vendor").first()
			if self.seller_category==logi:
				return True
			return False
		else:
			return False

	
	@property
	def is_driver(self):
		drive=seller_Categories.objects.filter(name="Logistics Driver").first()
		# print(drive,"khjg")
		if self.seller_category==drive:
			return True
		return False

	@property
	def is_sales(self):
		sal=staff_Categories.objects.filter(name="Sales").first()
		if self.staff and self.staff_category==sal:
			return True
		return False
	

class response_time(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	date=models.DateField(auto_now_add=True)
	response_tm=models.IntegerField(default=0)
	response_var=models.IntegerField(default=0)
	response_tm_total=models.IntegerField(default=0)


	def __str__(self):
		return str(self.user)




class list_of_holidays(models.Model):
	date_of_holiday=models.DateField()
	users=models.ManyToManyField(detail,blank=True)


	def __str__(self):
		return str(self.date_of_holiday)


class profile_status(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	status=models.CharField(max_length=255)
	date_update=models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return str(self.status)


class access_perm(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	staff_category=models.ManyToManyField(staff_Categories,blank=True)
	seller_category=models.ManyToManyField(seller_Categories,blank=True)


	def __str__(self):
		return str(self.user.name)


	class Meta:
		verbose_name="Access Permission"
		verbose_name_plural="Access Permissions"



class profile_status_update(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	updated_on=models.DateTimeField(auto_now=True)
	date = models.DateField(auto_now=False)
	time = models.TimeField(auto_now=False)
	color=models.CharField(max_length=255)
	status_text=models.TextField()
	daily_achi=models.CharField(max_length=255)
	daily_hurd=models.CharField(max_length=255)
	order_no=models.CharField(max_length=255)


	def __str__(self):
		return str(self.user.email)

	class Meta:
		verbose_name="Profile Status"




#sanskar's code



class Color(models.Model):
	name=models.CharField(max_length=20)

	def __str__(self):
		return self.name

class items(models.Model):
	Brand_name=models.CharField(max_length=200)
	color= models.ForeignKey(Color,on_delete=models.CASCADE)
	total=models.IntegerField(default=0,null=True)
	ts24=models.IntegerField(default=0,null=True)
	ts26 = models.IntegerField(default=0,null=True)
	ts28 = models.IntegerField(default=0,null=True)
	ts30 = models.IntegerField(default=0,null=True)
	ts32 = models.IntegerField(default=0,null=True)
	ts34 = models.IntegerField(default=0,null=True)
	ts36 = models.IntegerField(default=0,null=True)
	ts38 = models.IntegerField(default=0,null=True)
	ts40 = models.IntegerField(default=0,null=True)
	ts42 = models.IntegerField(default=0,null=True)
	ts44 = models.IntegerField(default=0,null=True)
	ts46 = models.IntegerField(default=0,null=True)
	ts48 = models.IntegerField(default=0,null=True)
	ts50 = models.IntegerField(default=0,null=True)
	fs24 = models.IntegerField(default=0)
	fs26 = models.IntegerField(default=0)
	fs28 = models.IntegerField(default=0)
	fs30 = models.IntegerField(default=0)
	fs32 = models.IntegerField(default=0)
	fs34 = models.IntegerField(default=0)
	fs36 = models.IntegerField(default=0)
	fs38 = models.IntegerField(default=0)
	fs40 = models.IntegerField(default=0)
	fs42 = models.IntegerField(default=0)
	fs44 = models.IntegerField(default=0)
	fs46 = models.IntegerField(default=0)
	fs48 = models.IntegerField(default=0)
	fs50 = models.IntegerField(default=0)
	barcode=models.CharField(max_length=2000,default=None)
	packed_on = models.CharField(max_length=200,default=" ")
	Categories = models.CharField(max_length=2000,default=" ")
	Super_categories = models.CharField(max_length=2000,default=" ")
	Fit = models.CharField(max_length=2000,default=" ")
	Description = models.CharField(max_length=2000,default=" ")
	Style = models.CharField(max_length=2000,default=" ")
	Vendor_code = models.CharField(max_length=2000,default=" ")
	address = models.CharField(max_length=2000,default=" ")

	def __str__(self):
		return self.Brand_name


class Carton(models.Model):
	carton_no=models.AutoField(primary_key=True)
	capacity=models.IntegerField()
	colors=models.ManyToManyField(Color)
	address=models.CharField(max_length=200,default=" ")
	leftcapacity=models.IntegerField(default=capacity)
	ts24 = models.IntegerField(default=0)
	ts26 = models.IntegerField(default=0)
	ts28 = models.IntegerField(default=0)
	ts30 = models.IntegerField(default=0)
	ts32 = models.IntegerField(default=0)
	ts34 = models.IntegerField(default=0)
	ts36 = models.IntegerField(default=0)
	ts38 = models.IntegerField(default=0)
	ts40 = models.IntegerField(default=0)
	ts42 = models.IntegerField(default=0)
	ts44 = models.IntegerField(default=0)
	ts46 = models.IntegerField(default=0)
	ts48 = models.IntegerField(default=0)
	ts50 = models.IntegerField(default=0)
	qrcode=models.CharField(max_length=390)
	is_filled=models.BooleanField(default=False)

	def __str__(self):
		return "Carton "+str(self.carton_no)


class order(models.Model):
	product=models.ForeignKey(items,on_delete=models.CASCADE)
	carton=models.ForeignKey(Carton,on_delete=models.CASCADE)
	address=models.CharField(max_length=200)
	color=models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
	quantity=models.IntegerField(default=0)

	def __str__(self):
		return "Order "+str(self.id)


COLOR_CHOICES = (
		('B.TECH','B.TECH'),
		('B.SC', 'B.SC'),
		('M.TECH','M.TECH'),
		('B.COM','B.COM'),
		
	)


#academic
class add_degree(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name
class add_field_of_study(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name
class academic(models.Model):
	name=models.CharField(max_length=200)
	email=models.CharField(max_length=200,null=True,blank=True)
	school_or_college=models.CharField(max_length=200)
	#degree=models.ForeignKey(add_degree,on_delete=models.CASCADE,null=True,blank=True)
	#field_of_study=models.ForeignKey(add_field_of_study,on_delete=models.CASCADE,null=True,blank=True)
	degree=models.CharField(max_length=200)
	field_of_study=models.CharField(max_length=200)

	start_date=models.DateField()
	end_date=models.DateField(null=True,blank=True)
	grade=models.CharField(max_length=200,null=True,blank=True)

SALARY_CHOICES = (
		('1,50,000','2,00,000'),
		('2,00,000','2,50,000'),
		('2,50,000','3,00,000'),
		('above 3,00,000','>3,00,000'),
		
	)


#professional
EMP_TYPE_CHOICES = (
		('Internship','Internship'),
		('Full-time','Full-time'),
		('Part-time','Part-time'),
		('Self-employed','Self-employed'),
		('Freelance','Freelance'),
		('Contract','Contract')
		)


class professional_pro(models.Model):
	name=models.CharField(max_length=200)
	email=models.CharField(max_length=200,null=True,blank=True)
	title=models.CharField(max_length=400)
	employment_type=models.CharField(max_length=200, choices=EMP_TYPE_CHOICES,default='Full-time')
	company=models.CharField(max_length=1000)
	current_company=models.BooleanField()
	location=models.CharField(max_length=200)
	start_date=models.DateField()
	end_date=models.DateField(null=True,blank=True)
	description=models.CharField(max_length=500)
	def __str__(self):
		return self.name
class add_project(models.Model):
	email=models.CharField(max_length=200,null=True,blank=True)
	project_name=models.CharField(max_length=200)
	start_date=models.DateField()
	end_date=models.DateField()
	description=models.CharField(max_length=500)
	project_url=models.CharField(max_length=200)
	def __str__(self):
		return self.email
class add_skill(models.Model):
	email=models.CharField(max_length=200,null=True,blank=True)
	name=models.CharField(max_length=200)
class add_certifications(models.Model):
	email=models.CharField(max_length=200,null=True,blank=True)
	title=models.CharField(max_length=200)
	organization=models.CharField(max_length=200)
	issued_date=models.DateField()
	issued_id=models.CharField(max_length=200)



GENDER_CHOICES = (
		('MALE','MALE'),
		('FEMALE','FEMALE'),
		
	)
MARITAL_CHOICES = (
		('MARRIED','MARRIED'),
		('UNMARRIED','UNMARRIED'),
		
	)

CATEGORY_CHOICES = (
		('GENERAL','GENERAL'),
		('SC/ST','SC/ST'),
		('OBC','OBC')
		
	)


#social
class social(models.Model):
	#name=models.CharField(max_length=200,null=True,blank=True)
	email=models.CharField(max_length=200,null=True,blank=True)
	dob=models.CharField(max_length=400)
	gender=models.CharField(max_length=1000,choices=GENDER_CHOICES,default='MALE')
	marital=models.CharField(max_length=200, choices=MARITAL_CHOICES,default='MARRIED')
	hometown=models.CharField(max_length=500)
	hobbies=models.CharField(max_length=500)
	mobile_number=models.CharField(max_length=13,null=True,blank=True)
	#category=models.CharField(max_length=500,choices=CATEGORY_CHOICES,default='GENERAL')
	#languages=models.CharField(max_length=500)
	linkedin_profile=models.CharField(max_length=500)
	facebook_profile=models.CharField(max_length=500)

class Social_Profile(models.Model):
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="profile_social")
	age=models.CharField(max_length=400)
	gender=models.CharField(max_length=1000,choices=GENDER_CHOICES,default='MALE')
	marital=models.CharField(max_length=200, choices=MARITAL_CHOICES,default='MARRIED')
	hometown=models.CharField(max_length=500)
	hobbies=models.CharField(max_length=500)
	mobile_number=models.CharField(max_length=13,null=True,blank=True)
	linkedin_profile=models.CharField(max_length=500)
	facebook_profile=models.CharField(max_length=500)



class diseases(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name

YES_CHOICES = (
		('YES','YES'),
		('NO','NO'),
		
	)

#medical
class medical(models.Model):
	email=models.CharField(max_length=200,null=True,blank=True)
	age=models.CharField(max_length=400)
	height=models.IntegerField()
	weight=models.IntegerField()
	blood_group=models.CharField(max_length=200)
	disability=models.CharField(max_length=100,choices=YES_CHOICES,default='NO')
	medical_issues=models.CharField(max_length=100, choices=YES_CHOICES,default='NO')
	diseases=models.ForeignKey(diseases,on_delete=models.CASCADE,null=True,blank=True)

class Medical_Profile(models.Model):
	created_by = models.ForeignKey(detail, null=True, blank=True, on_delete=models.CASCADE, related_name="profile_medical")
	height=models.IntegerField()
	weight=models.IntegerField()
	blood_group=models.CharField(max_length=200)
	disability=models.CharField(max_length=100,choices=YES_CHOICES,default='NO')
	medical_issues=models.CharField(max_length=100, choices=YES_CHOICES,default='NO')
	diseases=models.CharField(max_length=200, null=True ,blank=True)



class age(models.Model):
	age_range=models.CharField(max_length=200)
	def __str__(self):
		return self.age_range
class height(models.Model):
	height_range=models.CharField(max_length=200)
	def __str__(self):
		return self.height_range
class weight(models.Model):
	weight_range=models.CharField(max_length=200)
	def __str__(self):
		return self.weight_range
class quantity(models.Model):
	quantity_range=models.CharField(max_length=200)
	def __str__(self):
		return self.quantity_range
class frequency(models.Model):
	frequency_add=models.CharField(max_length=200)
	def __str__(self):
		return self.frequency_add
class shift(models.Model):
	shift_add=models.CharField(max_length=200)
	def __str__(self):
		return self.shift_add
class diet_product(models.Model):
	product_add=models.CharField(max_length=200)
	def __str__(self):
		return self.product_add
DAY_CHOICES=(
	('Monday','Monday'),
	('Tuesday','Tuesday'),
	('Wednesay','Wednesday'),
	('Thurday','Thurday'),
	('Friday','Friday'),
	('Saturday','Saturday'),
	('Sunday','Sunday')


	)
class diet_plan(models.Model):
	diseases=models.ForeignKey(diseases,on_delete=models.CASCADE,null=True,blank=True)
	age=models.ForeignKey(age,on_delete=models.CASCADE,null=True,blank=True)
	height=models.ForeignKey(height,on_delete=models.CASCADE,null=True,blank=True)
	weight=models.ForeignKey(weight,on_delete=models.CASCADE,null=True,blank=True)
	product=models.ForeignKey(diet_product,on_delete=models.CASCADE,null=True,blank=True)
	quantity=models.ForeignKey(quantity,on_delete=models.CASCADE,null=True,blank=True)
	frequency=models.ForeignKey(frequency,on_delete=models.CASCADE,null=True,blank=True)
	date=models.DateTimeField()
	day=models.CharField(max_length=200,choices=DAY_CHOICES,default='Sunday')
	shift=models.ForeignKey(shift,on_delete=models.CASCADE,null=True,blank=True)

class productorder(models.Model):
	transaction_id=models.BigIntegerField(null=True,blank=True)
	product_id=models.IntegerField()
	product_name=models.CharField(max_length=200)
	specifications=models.CharField(max_length=200)
	quantity=models.CharField(max_length=200)
	no_of_quantity=models.IntegerField(null=True,blank=True)
	vendor=models.CharField(max_length=200)
	vendor_address=models.CharField(max_length=200)
	vendor_landmark=models.CharField(max_length=200)
	customer_drop_address=models.CharField(max_length=200)
	customer_landmark=models.CharField(max_length=200)
	customer_id=models.CharField(max_length=200,null=True,blank=True)
	refundable_packing_charge=models.BooleanField(default=False)
	price=models.IntegerField(null=True,blank=True)
	def __str__(self):
		return self.product_name
	@property
	def get_total(self):
		total = self.price * self.no_of_quantity
		return total

class service_certifications(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name



class serviceorder(models.Model):
	transaction_id=models.BigIntegerField(null=True,blank=True)
	service_id=models.IntegerField()
	service_name=models.CharField(max_length=200)
	price_range=models.CharField(max_length=200)
	vendor=models.CharField(max_length=200)
	service_date=models.DateField(max_length=200)
	service_time=models.TimeField(max_length=200)
	service_rating=models.CharField(max_length=200)
	certifications=models.ForeignKey(service_certifications,on_delete=models.CASCADE)
	terms_and_conditions=models.CharField(max_length=200)
	customer_id=models.CharField(max_length=200,null=True,blank=True)
	def __str__(self):
		return self.service_name
class customizeorder(models.Model):
	requirement=models.CharField(max_length=300)
	service_date=models.DateField(max_length=200)
	service_time=models.TimeField(max_length=200)
	customer_id=models.CharField(max_length=200,null=True,blank=True)
	def __str__(self):
		return self.service_name
class order_frequency(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name
class subscriptionorder(models.Model):
	""" useless """
	transaction_id=models.IntegerField(null=True,blank=True)
	name=models.CharField(max_length=200)
	product_id=models.IntegerField(null=True,blank=True)
	unit_of_quantity=models.CharField(max_length=200)
	vendor=models.CharField(max_length=200)
	quantity=models.IntegerField()
	order_frequency=models.ForeignKey(order_frequency,on_delete=models.CASCADE)
	delivery_schedule=models.TimeField()
	start_date=models.DateField()
	remark=models.CharField(max_length=200)
	refundable_packing_charge=models.BooleanField(default=False)
	customer_id=models.CharField(max_length=200,null=True,blank=True)
	def __str__(self):
		return self.name

''' New model for subscription '''
class Subscription_Order(models.Model):

	SHIFTS = (
		('M', 'Morning'),
		('A', 'Afternoon'),
		('E', 'Evening')
	)

	transaction_id = models.CharField(max_length=200)
	product_slug = models.CharField(max_length=200)
	product_name = models.CharField(max_length=200, default='default')
	quantity = models.FloatField()
	# frequency = models.ForeignKey(order_frequency, on_delete=models.CASCADE)
	interval = models.IntegerField(default=7)
	start_date = models.DateField()
	end_date = models.DateField()
	shifts = models.CharField(max_length=1, choices=SHIFTS, default='M')
	remark = models.CharField(max_length=300, default='-')
	customer_email = models.CharField(max_length=100)
	vendor_email = models.CharField(max_length=100)
	refundable_packing_charge = models.BooleanField(default=False)
	stop_next = models.BooleanField(default=False) # Allows to stop the subscription for next time.
	isPaid = models.BooleanField(default=True)
	amount = models.FloatField(default = 100)
	
	def __str__(self):
		return self.product_name

class SubscriptionPayment(models.Model):
	payment_id = models.AutoField(primary_key=True)
	items_json = models.CharField(max_length=10000)
	amount = models.FloatField()
	name = models.CharField(max_length=20)
	email = models.CharField(max_length=100)
	address = models.CharField(max_length=1000)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=20)
	phone = models.CharField(max_length=12)

from product.models import product
from django.utils.timezone import now

''' To add subscription stops '''
class Subscription_Stop(models.Model):
	user = models.CharField(max_length = 100, default='consumer1@gmail.com')
	transaction_id = models.CharField(max_length=200)
	start_date = models.DateField(default=now)
	end_date = models.DateField(default='9999-12-31')

	def __str__(self):
		return str(self.start_date) + ' - ' + str(self.end_date)

class pick_and_deliver_order(models.Model):
	transaction_id=models.BigIntegerField(null=True,blank=True)
	product_name=models.ForeignKey(product,on_delete=models.CASCADE,null=True,blank=True)
	packing_instruction=models.CharField(max_length=200)
	pickup_contact=models.CharField(max_length=10)
	pickup_person=models.ForeignKey(detail,related_name='pickup_person',on_delete=models.CASCADE,null=True,blank=True)
	pickup_date=models.DateField()
	pickup_time=models.TimeField(null=True,blank=True)
	picked_up=models.NullBooleanField(default= False)
	delivered_up=models.NullBooleanField(default= False)
	pickup_address=models.CharField(max_length=200)
	pickup_landmark=models.CharField(max_length=200)
	pickup_coords = PlainLocationField(default='13.0352,77.5772', zoom=7)
	delivery_contact=models.CharField(max_length=10)
	delivery_person=models.ForeignKey(detail,related_name='delivery_person',on_delete=models.CASCADE,null=True,blank=True)
	delivery_date=models.DateField()
	delivery_time=models.TimeField(null=True,blank=True)
	delivery_address=models.CharField(max_length=200)
	delivery_landmark=models.CharField(max_length=200)
	distance=models.IntegerField(null=True,blank=True)
	minimum_order_quantity=models.IntegerField(null=True,blank=True)
	charge=models.IntegerField(null=True,blank=True)
	service_charge_paid_at=models.CharField(max_length=200)
	refundable_packing_charge=models.BooleanField(default=False)
	customer_id=models.CharField(max_length=200,null=True,blank=True)
	deliveryaccepted=models.NullBooleanField(default=False,blank=True)
	deliveryrejectedbywhom=models.ForeignKey(detail,related_name='deliveryrejection',on_delete=models.SET_NULL,null=True,blank=True)
	deliveryacceptedbywhom=models.ForeignKey(detail,related_name='deliveryacception',on_delete=models.SET_NULL,null=True,blank=True)
	deliveryassigntoafterrejection=models.ManyToManyField(detail,blank=True,related_name='assigntoanotherlogisticsafterrejection')
	drop_coords = PlainLocationField(default='13.0352,77.5772', zoom=7)
	placedbystaff=models.ForeignKey(detail,related_name='placedbystaff',on_delete=models.SET_NULL,null=True,blank=True)
	runner = models.ForeignKey(detail, null=True, blank=True, on_delete=models.SET_NULL, related_name="runner_detail")
	def __str__(self):
		return self.product_name.title

class customer_address(models.Model):
	email=models.CharField(max_length=200)
	address=models.CharField(max_length=200)
	permanent=models.BooleanField(default=False)
	pick_lat=models.FloatField(default=0,null=True)
	pick_lon=models.FloatField(default=0,null=True)
	def __str__(self):
		return self.address

class rating_users(models.Model):
	review_for = (
		('vendor' , 'vendor'),
		('delivery_person','delivery_person'),
		('buyer', 'buyer'),
		('product', 'product'),
	)
	stars = models.IntegerField(default=5, null=True, blank=True)
	review = models.CharField(max_length=100, null=True, blank=True)
	user = models.ForeignKey(detail,on_delete=models.CASCADE, null=True, blank=True)
	review_for_user = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True, related_name='review_for_user')
	review_for = models.CharField(choices=review_for, max_length=100, null=True, blank=True)

class distribution_center(models.Model):
	city_tiers = (
		('tier1' , 'tier1'),
		('tier2','tier2'),
		('tier3', 'tier3'),
		('tier4', 'tier4'),
	)
	name = models.CharField(max_length=200,null=True,blank=True)
	user = models.ForeignKey(detail,on_delete=models.CASCADE,null=True, blank=True)
	state = models.CharField(max_length=200,null=True,blank=True)
	city = models.CharField(max_length=200, null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	coordinates = PlainLocationField(default='13.0352,77.5772', zoom=7)
	city_tire = models.CharField(choices=city_tiers, max_length=100, null=True, blank=True)
	pickup_frequency = models.IntegerField(null=True, blank=True)
	delay_time = models.IntegerField(null=True, blank=True)