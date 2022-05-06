






from django.db import models


# Create your models here.



class filter_Categories(models.Model):
	name=models.CharField(max_length=255)


	def __str__(self):
		return self.name



class filter_Objects(models.Model):
	filter_category=models.ForeignKey(filter_Categories,on_delete=models.CASCADE)
	title=models.CharField(max_length=255)
	background=models.CharField(max_length=255,null=True,blank=True)
	max_price_value=models.IntegerField(null=True,blank=True)
	min_price_value=models.IntegerField(null=True,blank=True)


	def __str__(self):
		return self.title
