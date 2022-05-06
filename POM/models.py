







from django.db import models
from userdetail.models import detail

from product.models import category,sub_category,super_category, product_cate_b2b

from seller_info.models import labels,fits,seasons


from smart_selects.db_fields import ChainedForeignKey

# Create your models here.







class size_labels(models.Model):
	name=models.IntegerField(unique=True)

	def __str__(self):
		return str(self.name)



class inch_size_label(models.Model):
	name=models.IntegerField(unique=True)

	def __str__(self):
		return str(self.name)


class roman_size_label(models.Model):
	name=models.CharField(max_length=255,unique=True)

	def __str__(self):
		return str(self.name)


class uk_size_label(models.Model):
	name=models.IntegerField(unique=True)

	def __str__(self):
		return str(self.name)


class conversion_chart_map(models.Model):
	cm=models.ForeignKey(size_labels,on_delete=models.CASCADE,null=True,blank=True)
	inch=models.ForeignKey(inch_size_label,on_delete=models.CASCADE,null=True,blank=True)
	roman=models.ForeignKey(roman_size_label,on_delete=models.CASCADE,null=True,blank=True)
	uk=models.ForeignKey(uk_size_label,on_delete=models.CASCADE,null=True,blank=True)


	def __str__(self):
		return str(self.cm)+"="+str(self.inch)+"="+str(self.roman)+"="+str(self.uk)



class conversion_chart(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE,blank=True,null=True)
	mapping=models.ManyToManyField(conversion_chart_map,blank=True)
	main=models.BooleanField(default=False)


	def __str__(self):
		return str(self.main)




class POM(models.Model):
	label=models.CharField(max_length=255)
	product_Category=models.ManyToManyField(category, blank=True)
	# product_Subcategory=ChainedForeignKey(
	# 	sub_category,
	# 	chained_field="product_Category",
	# 	chained_model_field="product_Category",
	# 	show_all=False,
	# 	auto_choose=True,
	# 	sort=False,null=True,blank=True
	# 	)
	# product_Supercategory=ChainedForeignKey(
	# 	super_category,
	# 	chained_field="product_Subcategory",
	# 	chained_model_field="product_Subcategory",
	# 	show_all=False,
	# 	auto_choose=True,
	# 	sort=False,null=True,blank=True
	# 	)
	product_Subcategory = models.ManyToManyField(sub_category)
	product_Supercategory = models.ManyToManyField(super_category)
	admin_Tolerance=models.FloatField()
	ranges = models.TextField(blank=True)
	half_Length=models.BooleanField()
	show_to_Customer=models.BooleanField()
	max_Value=models.FloatField(default=50)
	min_Value=models.FloatField(default=24)
	impactfull_for_sample_or_custom_fabric_consumption = models.BooleanField(default=False)

	def __str__(self):
		return self.label





class measurement(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	label = ChainedForeignKey(
        labels,
        chained_field="user",
        chained_model_field="vendor",
        show_all=False,
        auto_choose=True,
        sort=False)
	fit = ChainedForeignKey(
		fits,
		chained_field="label",
		chained_model_field="label",
		show_all=False,
		auto_choose=True,
		sort=False
		)

	season = ChainedForeignKey(
		seasons,
		chained_field="fit",
		chained_model_field="fit",
		show_all=False,
		auto_choose=True,
		sort=False
		)
	product_Category=models.ForeignKey(category,on_delete=models.CASCADE)
	product_Subcategory=ChainedForeignKey(
		sub_category,
		chained_field="product_Category",
		chained_model_field="product_Category",
		show_all=False,
		auto_choose=True,
		sort=False
		)
	product_Supercategory=ChainedForeignKey(
		super_category,
		chained_field="product_Subcategory",
		chained_model_field="product_Subcategory",
		show_all=False,
		auto_choose=True,
		sort=False
		)
	name=models.IntegerField()
	slug=models.SlugField(max_length=200,unique=True)
	cm=models.BooleanField(default=True)
	inch=models.BooleanField(default=False)
	roman=models.BooleanField(default=False)
	uk=models.BooleanField(default=False)
	hides=models.TextField(null=True,blank=True)
	attribute1=models.FloatField(default=0,null=True,blank=True)
	grading1=models.FloatField(default=0,null=True,blank=True)
	tolerance1=models.FloatField(default=0,null=True,blank=True)
	attribute2=models.FloatField(default=0,null=True,blank=True)
	grading2=models.FloatField(default=0,null=True,blank=True)
	tolerance2=models.FloatField(default=0,null=True,blank=True)
	attribute3=models.FloatField(default=0,null=True,blank=True)
	grading3=models.FloatField(default=0,null=True,blank=True)
	tolerance3=models.FloatField(default=0,null=True,blank=True)
	attribute4=models.FloatField(default=0,null=True,blank=True)
	grading4=models.FloatField(default=0,null=True,blank=True)
	tolerance4=models.FloatField(default=0,null=True,blank=True)
	attribute5=models.FloatField(default=0,null=True,blank=True)
	grading5=models.FloatField(default=0,null=True,blank=True)
	tolerance5=models.FloatField(default=0,null=True,blank=True)
	attribute6=models.FloatField(default=0,null=True,blank=True)
	grading6=models.FloatField(default=0,null=True,blank=True)
	tolerance6=models.FloatField(default=0,null=True,blank=True)
	attribute7=models.FloatField(default=0,null=True,blank=True)
	grading7=models.FloatField(default=0,null=True,blank=True)
	tolerance7=models.FloatField(default=0,null=True,blank=True)
	attribute8=models.FloatField(default=0,null=True,blank=True)
	grading8=models.FloatField(default=0,null=True,blank=True)
	tolerance8=models.FloatField(default=0,null=True,blank=True)
	attribute9=models.FloatField(default=0,null=True,blank=True)
	grading9=models.FloatField(default=0,null=True,blank=True)
	tolerance9=models.FloatField(default=0,null=True,blank=True)
	attribute10=models.FloatField(default=0,null=True,blank=True)
	grading10=models.FloatField(default=0,null=True,blank=True)
	tolerance10=models.FloatField(default=0,null=True,blank=True)
	attribute11=models.FloatField(default=0,null=True,blank=True)
	grading11=models.FloatField(default=0,null=True,blank=True)
	tolerance11=models.FloatField(default=0,null=True,blank=True)
	attribute12=models.FloatField(default=0,null=True,blank=True)
	grading12=models.FloatField(default=0,null=True,blank=True)
	tolerance12=models.FloatField(default=0,null=True,blank=True)
	attribute13=models.FloatField(default=0,null=True,blank=True)
	grading13=models.FloatField(default=0,null=True,blank=True)
	tolerance13=models.FloatField(default=0,null=True,blank=True)
	attribute14=models.FloatField(default=0,null=True,blank=True)
	grading14=models.FloatField(default=0,null=True,blank=True)
	tolerance14=models.FloatField(default=0,null=True,blank=True)
	attribute15=models.FloatField(default=0,null=True,blank=True)
	grading15=models.FloatField(default=0,null=True,blank=True)
	tolerance15=models.FloatField(default=0,null=True,blank=True)
	attribute16=models.FloatField(default=0,null=True,blank=True)
	grading16=models.FloatField(default=0,null=True,blank=True)
	tolerance16=models.FloatField(default=0,null=True,blank=True)
	attribute17=models.FloatField(default=0,null=True,blank=True)
	grading17=models.FloatField(default=0,null=True,blank=True)
	tolerance17=models.FloatField(default=0,null=True,blank=True)
	attribute18=models.FloatField(default=0,null=True,blank=True)
	grading18=models.FloatField(default=0,null=True,blank=True)
	tolerance18=models.FloatField(default=0,null=True,blank=True)
	attribute19=models.FloatField(default=0,null=True,blank=True)
	grading19=models.FloatField(default=0,null=True,blank=True)
	tolerance19=models.FloatField(default=0,null=True,blank=True)
	attribute20=models.FloatField(default=0,null=True,blank=True)
	grading20=models.FloatField(default=0,null=True,blank=True)
	tolerance20=models.FloatField(default=0,null=True,blank=True)
	attribute21=models.FloatField(default=0,null=True,blank=True)
	grading21=models.FloatField(default=0,null=True,blank=True)
	tolerance21=models.FloatField(default=0,null=True,blank=True)
	attribute22=models.FloatField(default=0,null=True,blank=True)
	grading22=models.FloatField(default=0,null=True,blank=True)
	tolerance22=models.FloatField(default=0,null=True,blank=True)
	attribute23=models.FloatField(default=0,null=True,blank=True)
	grading23=models.FloatField(default=0,null=True,blank=True)
	tolerance23=models.FloatField(default=0,null=True,blank=True)
	attribute24=models.FloatField(default=0,null=True,blank=True)
	grading24=models.FloatField(default=0,null=True,blank=True)
	tolerance24=models.FloatField(default=0,null=True,blank=True)
	attribute25=models.FloatField(default=0,null=True,blank=True)
	grading25=models.FloatField(default=0,null=True,blank=True)
	tolerance25=models.FloatField(default=0,null=True,blank=True)
	attribute26=models.FloatField(default=0,null=True,blank=True)
	grading26=models.FloatField(default=0,null=True,blank=True)
	tolerance26=models.FloatField(default=0,null=True,blank=True)
	attribute27=models.FloatField(default=0,null=True,blank=True)
	grading27=models.FloatField(default=0,null=True,blank=True)
	tolerance27=models.FloatField(default=0,null=True,blank=True)
	attribute28=models.FloatField(default=0,null=True,blank=True)
	grading28=models.FloatField(default=0,null=True,blank=True)
	tolerance28=models.FloatField(default=0,null=True,blank=True)
	attribute29=models.FloatField(default=0,null=True,blank=True)
	grading29=models.FloatField(default=0,null=True,blank=True)
	tolerance29=models.FloatField(default=0,null=True,blank=True)
	attribute30=models.FloatField(default=0,null=True,blank=True)
	grading30=models.FloatField(default=0,null=True,blank=True)
	tolerance30=models.FloatField(default=0,null=True,blank=True)






	def __str__(self):
		return str(self.name)



class measurement_chart(models.Model):
	chart=models.ForeignKey(measurement,on_delete=models.CASCADE)
	pom=models.ForeignKey(POM,on_delete=models.CASCADE)
	size=models.IntegerField()
	value=models.FloatField()
	grading=models.FloatField()
	tolerance=models.FloatField()
	main_val=models.BooleanField(default=False)

	def __str__(self):
		return str(self.size)



class garment_weight(models.Model):
	user=models.ForeignKey(detail,on_delete=models.CASCADE)
	measurement_obj=models.ForeignKey(measurement,on_delete=models.CASCADE)
	size=models.IntegerField()
	weight=models.IntegerField()


	def __str__(self):
		return str(self.size)


class size_assortment_pattern(models.Model):
	sector=models.ForeignKey(product_cate_b2b, on_delete=models.CASCADE, null=True, blank=True)
	product_Category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
	product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
	product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
	product_Labels = models.ForeignKey(labels, on_delete=models.CASCADE, null=True, blank=True)
	product_Fits = models.ForeignKey(fits, on_delete=models.CASCADE, null=True, blank=True)
	size=models.ManyToManyField(size_labels)
	ratio=models.TextField(blank=True)
	fabric_width = models.TextField(blank=True)
	fabric_consumption_width = models.TextField(blank=True)
	fabric_consumption=models.FloatField()
	default=models.BooleanField(default=False)