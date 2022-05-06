from django.db import models

# Create your models here.

from userdetail.models import seller_Categories,staff_Categories,detail



class section(models.Model):
	name=models.CharField(max_length=255,unique=True)
	order_section=models.BooleanField(default=False)
	standard_form=models.BooleanField(default=False)
	standard_document=models.BooleanField(default=False)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Section"
		verbose_name_plural="Sections"



class orders_permission(models.Model):
	name=models.CharField(max_length=255)
	seller_category=models.ManyToManyField(seller_Categories,blank=True)
	staff_category=models.ManyToManyField(staff_Categories,blank=True)
	customer=models.BooleanField(default=False)
	allowed_section=models.ManyToManyField(section,blank=True)


	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Order Permission"
		verbose_name_plural="Order Permission"


class staff_permissions(models.Model):
	user=models.OneToOneField(detail,on_delete=models.CASCADE,unique=True)
	holidays=models.BooleanField(default=True)
	run_rate=models.BooleanField(default=True)
	profile_status=models.BooleanField(default=True)
	response_time=models.BooleanField(default=True)
	profile_performance=models.BooleanField(default=True)
	hit_run_rate=models.BooleanField(default=True)
	activities_order=models.BooleanField(default=True)

	def __str__(self):
		return str(self.user.email)

	class Meta:
		verbose_name="Staff Permissions"



class vendor_permissions(models.Model):
	user=models.OneToOneField(detail,on_delete=models.CASCADE,unique=True)
	production_product=models.BooleanField(default=True)
	upload_product=models.BooleanField(default=True)
	hit_rate=models.BooleanField(default=True)
	dpr=models.BooleanField(default=True)

	def __str__(self):
		return str(self.user.email)

	class Meta:
		verbose_name="Vendor Permissions"