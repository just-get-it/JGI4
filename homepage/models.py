from django.db import models
# Create your models here.
import random,os
from django.contrib.auth import get_user_model
from product.models import labels_Object



def get_filename_ext(filepath):
	base_name=os.path.basename(filepath)
	name ,ext=os.path.splitext(base_name)
	return name ,ext

def upload_image_path(instance,filename):
	new_filename=random.randint(1,13516546431654)
	name ,ext=get_filename_ext(filename)
	final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "local/product/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename
		)


class logo(models.Model):
	name=models.CharField(max_length=255)
	image=models.FileField(upload_to=upload_image_path)
	default=models.BooleanField(default=False)

	def __str__(self):
		return self.name


class address(models.Model):
	name=models.CharField(max_length=255)
	address_of_website=models.TextField()
	default=models.BooleanField(default=False)
	email = models.EmailField(blank=True,null=True)
	mob = models.CharField(max_length=10,blank=True,null=True)
	gstin=models.CharField(max_length=15,blank=True,null=True)
	pincode=models.CharField(max_length=6,blank=True,null=True)


	def __str__(self):
		return self.name


class message(models.Model):
	location=models.CharField(max_length=100, default='')
	hint=models.CharField(max_length=500, default='')

	def __str__(self):
		return str(self.hint)


class homepage_crousel(models.Model):
	active=models.BooleanField(default=False)
	product_type = models.CharField(max_length=100) 
	product_name = models.CharField(max_length=100,default='justgetit')
	# product_tag=models.ForeignKey(labels_Object,on_delete=models.CASCADE,null=True,blank=True)
	image = models.FileField(upload_to=upload_image_path)
	link = models.CharField(max_length=100,default='http://retail.justgetit.in/')


	def __str__(self):
		return str(self.active)

class discount_corousel1(models.Model):
	active=models.BooleanField(default=False)
	image = models.ImageField(upload_to='uploads/products/', default="")


	def __str__(self):
		return str(self.active)

class discount_corousel2(models.Model):
	active=models.BooleanField(default=False)
	image = models.ImageField(upload_to='uploads/products/', default="")


	def __str__(self):
		return str(self.active)

User=get_user_model()
class licence(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	valid_upto=models.DateField()

	def __str__(self):
		return str(self.user)


class homepage_link(models.Model):
	active=models.BooleanField(default=False)
	ready_to_wear=models.BooleanField(default=False)
	bespoke=models.BooleanField(default=False)
	mtm=models.BooleanField(default=False)
	institutional=models.BooleanField(default=False)
	printful=models.BooleanField(default=False)
	task=models.BooleanField(default=False)
	my_Design=models.BooleanField(default=False)
	footer_men=models.BooleanField(default=False)
	footer_women=models.BooleanField(default=False)
	footer_kids=models.BooleanField(default=False)
	footer_home=models.BooleanField(default=False)
	footer_bespoke=models.BooleanField(default=False)
	footer_track=models.BooleanField(default=False)
	footer_shipping=models.BooleanField(default=False)
	footer_return=models.BooleanField(default=False)
	footer_faq=models.BooleanField(default=False)


	def __str__(self):
		return str(self.active)



class B2B_homepage_crousel(models.Model):
	active=models.BooleanField(default=False)
	product_type = models.CharField(max_length=100)
	product_name = models.CharField(max_length=100,default='justgetit')
	# product_tag=models.ForeignKey(labels_Object,on_delete=models.CASCADE,null=True,blank=True)
	image = models.ImageField(upload_to='uploads/products/', default="")
	link = models.CharField(max_length=100,default='http://retail.justgetit.in/')
	tag = models.CharField(max_length= 100,default = 'home')


	def __str__(self):
		return str(self.active)

class B2B_discount_corousel1(models.Model):
	active=models.BooleanField(default=False)
	image = models.ImageField(upload_to='uploads/products/', default="")

	def __str__(self):
		return str(self.active)

class B2B_discount_corousel2(models.Model):
	active=models.BooleanField(default=False)
	image = models.ImageField(upload_to='uploads/products/', default="")

	def __str__(self):
		return str(self.active)

class HomePage_Banners(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return str(self.title)

class Homepage_Banners_Image(models.Model):
	banner = models.ForeignKey(HomePage_Banners, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=200)
	button = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)

class Add_Page(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return str(self.name)		

class Homepage_Card(models.Model):
	title = models.CharField(max_length=200)
	page = models.ForeignKey(Add_Page, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.title)
# class Body_image(models.Model):
# 	page = models.ForeignKey(Add_Page, on_delete=models.CASCADE)
# 	card = models.ForeignKey(Homepage_Card, on_delete=models.CASCADE)
# 	Add_body_image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
# 	Add_body_title=models.CharField(max_length=200)
# 	Add_body_text=models.CharField(max_length=200)
# 	button = models.CharField(max_length=200, null=True, blank=True)
# 	button_link = models.CharField(max_length=200, null=True, blank=True)
# 	def __str__(self):
# 		return str(self.Add_body_title)	

class Body_image_category(models.Model):
	title = models.CharField(max_length=200)
	page = models.ForeignKey(Add_Page, on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return str(self.title)

class Body_image(models.Model):
	name = models.CharField(max_length=200)
	card = models.ForeignKey(Body_image_category, on_delete=models.CASCADE)
	Add_body_image=models.FileField(upload_to=upload_image_path,null=True,blank=True)

	def __str__(self):
		return str(self.name)

class Homepage_cardimg(models.Model):
	card = models.ForeignKey(Homepage_Card, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	# body_image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)	


# Consulting banner and cards

class Consulting_Banners(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return str(self.title)

class Consulting_Banners_Image(models.Model):
	banner = models.ForeignKey(Consulting_Banners, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=200)
	button = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)


class Consulting_Card(models.Model):
	title = models.CharField(max_length=200)
	page = models.ForeignKey(Add_Page, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.title)	

class Consulting_Cardimg(models.Model):
	card = models.ForeignKey(Consulting_Card, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)	



# Sourcing banner and cards

class Sourcing_Banners(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return str(self.title)

class Sourcing_Banners_Image(models.Model):
	banner = models.ForeignKey(Sourcing_Banners, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=200)
	button = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)


class Sourcing_Card(models.Model):
	title = models.CharField(max_length=200)
	page = models.ForeignKey(Add_Page, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.title)	

class Sourcing_Cardimg(models.Model):
	card = models.ForeignKey(Sourcing_Card, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)	




# Manufacturing banner and cards

class Manufacturing_Banners(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return str(self.title)

class Manufacturing_Banners_Image(models.Model):
	banner = models.ForeignKey(Manufacturing_Banners, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=200)
	button = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)


class Manufacturing_Card(models.Model):
	title = models.CharField(max_length=200)
	page = models.ForeignKey(Add_Page, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.title)	

class Manufacturing_Cardimg(models.Model):
	card = models.ForeignKey(Manufacturing_Card, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)	

# Automation banner and cards

class Automation_Banners(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return str(self.title)

class Automation_Banners_Image(models.Model):
	banner = models.ForeignKey(Automation_Banners, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=200)
	button = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)


class Automation_Card(models.Model):
	title = models.CharField(max_length=200)
	page = models.ForeignKey(Add_Page, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.title)	

class Automation_Cardimg(models.Model):
	card = models.ForeignKey(Automation_Card, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	desc = models.CharField(max_length=200)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.name)	