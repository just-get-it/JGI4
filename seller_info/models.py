from django.db import models
from userdetail.models import detail
from product.models import category as cate
from product.models import sub_category, super_category, product_cate_b2b
# from b2b.models import company_Order
# Create your models here.
from smart_selects.db_fields import ChainedForeignKey
import random
import os

def get_filename_ext(filepath):
	base_name=os.path.basename(filepath)
	name ,ext=os.path.splitext(base_name)
	return name ,ext

def upload_image_path(instance,filename):
	new_filename=random.randint(1,13516546431654)
	name ,ext=get_filename_ext(filename)
	final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "local/washcare/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename
		)



class labels(models.Model):
	name=models.CharField(max_length=255)
	slug=models.SlugField(max_length=255,unique=True)
	vendor=models.ForeignKey(detail,on_delete=models.CASCADE)



	def __str__(self):
		return self.name



class fits(models.Model):
	name=models.CharField(max_length=255)
	slug=models.SlugField(max_length=255,unique=True)
	vendor=models.ForeignKey(detail,on_delete=models.CASCADE)
	label = ChainedForeignKey(
        labels,
        chained_field="vendor",
        chained_model_field="vendor",
        show_all=False,
        auto_choose=True,
        sort=False)


	def __str__(self):
		return self.name








class seasons(models.Model):
	name=models.CharField(max_length=255)
	slug=models.SlugField(max_length=255,unique=True)
	vendor=models.ForeignKey(detail,on_delete=models.CASCADE)
	label = ChainedForeignKey(
        labels,
        chained_field="vendor",
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
        sort=False)


	def __str__(self):
		return self.name


class washcares(models.Model):
	name=models.CharField(max_length=255)
	vendor=models.ForeignKey(detail,on_delete=models.CASCADE)
	label=models.ForeignKey(labels,on_delete=models.CASCADE)
	fit=models.ForeignKey(fits,on_delete=models.CASCADE)
	season=models.ForeignKey(seasons,on_delete=models.CASCADE)
	file=models.FileField(upload_to=upload_image_path)


	def __str__(self):
		return self.name


class barcodes(models.Model):
	name=models.CharField(max_length=255)
	vendor=models.ForeignKey(detail,on_delete=models.CASCADE)
	label=models.ForeignKey(labels,on_delete=models.CASCADE)
	fit=models.ForeignKey(fits,on_delete=models.CASCADE)
	season=models.ForeignKey(seasons,on_delete=models.CASCADE)
	file=models.FileField(upload_to=upload_image_path)


	def __str__(self):
		return self.name

class trimcard_sections(models.Model):
	seller = models.ForeignKey(detail, on_delete=models.CASCADE, related_name='trims_sections')
	name = models.CharField(max_length=100)
	product_Category = models.ForeignKey(cate, on_delete=models.CASCADE, null=True)
	product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True)
	product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True)
	fabric_and_quantity_no = models.BooleanField(default=True)
	embroidary_sample_and_thread_code = models.BooleanField(default=True)
	thread_brand_and_count = models.BooleanField(default=True)
	polybag = models.BooleanField(default=True)
	pocketing = models.BooleanField(default=True)
	internlining = models.BooleanField(default=True)

# Add folding, packing, packaging manuals, all_in_one(three documents combined) based on categories under store ( Add buttons under seller_profile/store (each file will be connected to product cate,super,sub ) (display download/view in http://127.0.0.1:8000/userdetail/staff_profile/orders/2019000008 )
def upload_doc_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=name, ext=ext)
    return "local/seller_docs/manual_documents/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class manual_documents(models.Model):
	seller = models.ForeignKey(detail, on_delete=models.CASCADE, related_name='manual_documents')
	order = models.ForeignKey('b2b.company_Order', on_delete=models.SET_NULL, null=True, blank=True)
	name = models.CharField(max_length=100)
	product_Category = models.ForeignKey(cate, on_delete=models.CASCADE, null=True)
	product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True)
	product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True)
	folding_doc = models.FileField(upload_to=upload_doc_path, null=True, blank=True)
	packing_doc = models.FileField(upload_to=upload_doc_path, null=True, blank=True)
	packing_manual = models.FileField(upload_to=upload_doc_path, null=True, blank=True)
	all_in_one = models.FileField(upload_to=upload_doc_path, null=True, blank=True)

	def __str__(self):
		return self.name