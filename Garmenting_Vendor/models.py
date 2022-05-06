



from django.db import models

from smart_selects.db_fields import ChainedForeignKey
from product.models import category,sub_category,super_category
# Create your models here.


from userdetail.models import detail
from b2b.models import company_Order


class kpi(models.Model):
	name=models.CharField(max_length=255)


	def __str__(self):
		return self.name

class kpi_data(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	kpi_val=models.ForeignKey(kpi,on_delete=models.CASCADE)
	rating=models.FloatField()



	def __str__(self):
		return str(self.user)


	class Meta:
		verbose_name="K.P.I. Data"
		verbose_name_plural="K.P.I. Data"



class kpi_data_order(models.Model):
	by_user=models.ForeignKey(detail,on_delete=models.CASCADE,related_name="by_user",null=True,blank=True)
	to_user=models.ForeignKey(detail,on_delete=models.CASCADE,related_name="to_user",null=True,blank=True)
	order=models.ForeignKey(company_Order,on_delete=models.CASCADE)
	kpi_val=models.ForeignKey(kpi,on_delete=models.CASCADE)
	rating=models.FloatField()



	def __str__(self):
		return str(self.user)


	class Meta:
		verbose_name="K.P.I. Data"
		verbose_name_plural="K.P.I. Data"






class production_Product(models.Model):
	product_Category=models.ForeignKey(category,on_delete=models.CASCADE)
	product_Subcategory = ChainedForeignKey(
        sub_category,
        chained_field="product_Category",
        chained_model_field="product_Category",
        show_all=False,
        auto_choose=True,
        sort=False)
	product_Supercategory= ChainedForeignKey(
		super_category,
		chained_field="product_Subcategory",
		chained_model_field="product_Subcategory",
		show_all=False,
		auto_choose=True,
		sort=False)
	quantity=models.IntegerField(default=0)
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	cost=models.IntegerField(default=0)


	def __str__(self):
		return str(self.user)


class production_Line(models.Model):
	production_product=models.ForeignKey(production_Product,on_delete=models.CASCADE)
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	name=models.CharField(max_length=255)
	quantity=models.IntegerField(default=0)


	def __str__(self):
		return self.name


from b2b.models import company_Order


class floated_orders(models.Model):
	to_user=models.ForeignKey(detail,on_delete=models.CASCADE)
	from_user=models.CharField(max_length=255,null=True,blank=True)
	order=models.ForeignKey(company_Order,on_delete=models.CASCADE)
	comments_from_user=models.TextField(null=True,blank=True)
	comments_to_user=models.TextField(null=True,blank=True)
	updated_price=models.IntegerField(null=True,blank=True)


	def __str__(self):
		return str(self.to_user)


class production_Daily_Update(models.Model):
	date_update=models.DateField()
	production_obj=models.ForeignKey(production_Product,on_delete=models.CASCADE)
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	quantity=models.IntegerField()

	def __str__(self):
		return str(user.name)

	
