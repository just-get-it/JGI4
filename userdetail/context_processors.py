



from product.models import category,sub_category,super_category
from .models import detail,seller_Categories
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from homepage.models import logo,address,licence,homepage_link
import datetime
from django.utils import timezone
from product.models import labels_Object

def add_variable_to_context(request):
	cated={}
	for cate in category.objects.all():
		subcated={}
		for subcate in sub_category.objects.filter(product_Category=cate):
			#superl=[]
			superl= super_category.objects.filter(product_Subcategory=subcate,product_Category=cate)
			subcated[subcate.name]=superl
		cated[cate.name]=subcated

	sub=sub_category.objects.all()
	li=[]
	for a in sub:
		li.append(a)
	# print(li[0].super_category_set.all())
	oim1=None
	if request.user.is_authenticated:
		if request.user.email is None:
			oim1=None
		else:
			oim1=detail.objects.filter(email=request.user.email).first()
	vend_pro=False
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details is not None:
			sel_cate=seller_Categories.objects.filter(name="Products Vendor")
			if details.vendor and not(details.seller_category==sel_cate):
				vend_pro=True
	ad=False
	if request.user.is_authenticated:
		if request.user.is_superuser:
			ad=True
	logo_main=logo.objects.filter(default=True).first()
	address_main=address.objects.filter(default=True).first()
	oer=licence.objects.all()
	for oe in oer:
		date=oe.valid_upto
		d1=datetime.datetime(date.year,date.month,date.day)
		date2=datetime.datetime.now()
		d2=datetime.datetime(date2.year,date2.month,date2.day)
		if d2>=d1:
			oe.user.is_staff=False
			oe.user.save()
		oe.delete()
	home_links=homepage_link.objects.filter(active=True).first()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details:
			details.last_activity=timezone.now()
			details.save()
	return {
		"category": cated,
        'testme': "helle",
        # 'a1':li[0].super_category_set.all(),
		# 'a2':li[1].super_category_set.all(),
		# 'a3':li[2].super_category_set.all(),
		# 'a4':li[3].super_category_set.all(),
		# 'a5':li[4].super_category_set.all(),
		# 'a6':li[5].super_category_set.all(),
		# 'a7':li[6].super_category_set.all(),
		# 'a8':li[7].super_category_set.all(),
		# 'a9':li[8].super_category_set.all(),
		# 'a10':li[9].super_category_set.all(),
		# 'a11':li[10].super_category_set.all(),
		# 'a12':li[11].super_category_set.all(),
		# 'a13':li[12].super_category_set.all(),
		# 'a14':li[13].super_category_set.all(),
		# 'a15':li[14].super_category_set.all(),
		# 'a16':li[15].super_category_set.all(),
		# 'a17':li[16].super_category_set.all(),
		# 'a18':li[17].super_category_set.all(),
		# 'a19':li[18].super_category_set.all(),
		# 'a20':li[19].super_category_set.all(),
		# 'a21':li[20].super_category_set.all(),
		# 'a22':li[21].super_category_set.all(),
		# 'a23':li[22].super_category_set.all(),
		# 'a24':li[23].super_category_set.all(),
		# 'a25':li[24].super_category_set.all(),
		# 'a26':li[25].super_category_set.all(),
		# 'a27':li[26].super_category_set.all(),
		# 'a28':li[27].super_category_set.all(),
		# 'a29':li[28].super_category_set.all(),
		# 'a30':li[29].super_category_set.all(),
		# 'a31':li[30].super_category_set.all(),
		# 'a32':li[31].super_category_set.all(),
		# 'a33':li[32].super_category_set.all(),
		# 'a34':li[33].super_category_set.all(),
		# 'a35':li[34].super_category_set.all(),
		# 'a36':li[35].super_category_set.all(),
		# 'a37':li[36].super_category_set.all(),
		# 'a38':li[37].super_category_set.all(),
		# 'a39':li[38].super_category_set.all(),
		# 'a40':li[39].super_category_set.all(),
		# 'a41':li[40].super_category_set.all(),
		# 'a42':li[41].super_category_set.all(),
		# 'a43':li[42].super_category_set.all(),
		# 'a44':li[43].super_category_set.all(),
		"oim1":oim1,
		"vend_pro456":vend_pro,
		"ad789":ad,
		"logo":logo_main,
		"address789":address_main,
		"home_links":home_links,
		"tags_wise":labels_Object.objects.all()
    }
