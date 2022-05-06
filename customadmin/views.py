



from django.shortcuts import render,redirect
from product.models import category,sub_category,super_category,product
from .forms import category_form,subcategory_form,product_form, supercategory_form
# Create your views here.





def customadmin(request):
	return render(request,'customadmin/customadmin.html',{})


def productcategories(request):
	data={
		'objects':category.objects.all(),
		'head':'Category'
	}
	return render(request,'customadmin/productcategories.html',data)




def categorydetail(request,num):
	try:
		obj=category.objects.get(id=num)
	except:
		return redirect('/')
	form_class=category_form(request.POST)
	data={
		'obj':obj,
		'form':form_class,
		'head':'Category'
	}
	if request.POST:
		if form_class.is_valid():
			name=form_class.cleaned_data.get('name')
			obj.name=name
			obj.save()
		return redirect('/customadmin/productcategories')
	return render(request,'customadmin/categorydetail.html',data)

def categorydelete(request,num):
	try:
		obj=category.objects.get(id=num)
	except:
		return redirect('/')
	obj.delete()
	return redirect('/customadmin/productcategories')


def categoryadd(request):
	form_class=category_form(request.POST)
	data={
	"form":form_class,
	'head':'Category'
	}
	if request.POST:
		if form_class.is_valid():
			form_class.save()
			return redirect('/customadmin/productcategories')
	return render(request,'customadmin/categoryadd.html',data)








def subcategories(request):
	data={
		'objects':sub_category.objects.all(),
		'head':'Sub-category'
	}
	return render(request,'customadmin/productcategories.html',data)




def subcategorydetail(request,num):
	try:
		obj=sub_category.objects.get(id=num)
	except:
		return redirect('/')
	form_class=subcategory_form(request.POST)
	data={
		'obj':obj,
		'form':form_class,
		'head':'Sub-category'
	}
	if request.POST:
		if form_class.is_valid():
			name=form_class.cleaned_data.get('name')
			obj.name=name
			obj.save()
		return redirect('/customadmin/subcategories')
	return render(request,'customadmin/categorydetail.html',data)

def subcategorydelete(request,num):
	try:
		obj=sub_category.objects.get(id=num)
	except:
		return redirect('/')
	obj.delete()
	return redirect('/customadmin/subcategories')


def subcategoryadd(request):
	form_class=subcategory_form(request.POST)
	data={
	"form":form_class,
	'head':'Sub-category'
	}
	if request.POST:
		if form_class.is_valid():
			form_class.save()
			return redirect('/customadmin/subcategories')
	return render(request,'customadmin/categoryadd.html',data)


def productlist(request):
	context={
		'objects':product.objects.all(),
		'head':'Products'
	}
	return render(request,'customadmin/productcategories.html',context)


def productdetail(request, id):
	try:
		obj = product.objects.get(product_code=id)
	except:
		print("PD", id)
		return redirect('../')
	
	# form = product_form(request.POST)
	form = product_form(instance=obj)
	context = {
		'obj':obj,
		'form':form,
		'head':'Products'
	}

	if request.POST:
		if form.is_valid():
			form.save()
		return redirect('/customadmin/product')

	return render(request,'customadmin/productdetail.html',context)


def productdelete(request, id):
	try:
		obj=product.objects.get(product_code=id)
	except:
		return redirect('../')
	obj.delete()
	return redirect('/customadmin/product')

def productadd(request):
	form = product_form(request.POST)
	context = {
		"form":form,
		'head':'Products'
	}
	if request.POST:
		if form.is_valid():
			form.save()
			return redirect('/customadmin/products')
	
	# return redirect("/userdetail/seller_profile/upload_product")
	return render(request, 'customadmin/productadd.html',context)
	
	
def supercategories(request):
	context={
		'objects':super_category.objects.all(),
		'head':'Super-category'
	}
	return render(request,'customadmin/productcategories.html',context)



def supercategoriesdetail(request, id):
	try:
		obj = super_category.objects.get(id=id)
	except:
		return redirect('/')

	form = supercategory_form(request.POST)
	data={
		'obj':obj,
		'form':form,
		'head':'Super-category'
	}

	if request.POST:
		if form_class.is_valid():
			name=form_class.cleaned_data.get('name')
			obj.name=name
			obj.save()
		return redirect('/customadmin/supercategory')
	return render(request,'customadmin/supercategorydetail.html',data)

def supercategoriesdelete(request, id):
	try:
		obj=super_category.objects.get(id=id)
	except:
		return redirect('/')
	obj.delete()
	return redirect('/customadmin/supercategory')


def supercategoriesadd(request):
	form_class=supercategory_form(request.POST)
	data={
	"form":form_class,
	'head':'Super-category'
	}
	if request.POST:
		if form_class.is_valid():
			form_class.save()
			return redirect('/customadmin/supercategories')
	return render(request,'customadmin/supercategoryadd.html',data)
