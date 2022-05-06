from b2b.models import company_Order
from product.models import product,Orders,super_category,label_Attributes_Values, labels_Attributes, size_color_quantity
from userdetail.models import detail
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from cartnew.models import *
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
from django.db.models import Q
from django.forms import formset_factory
from product.models import upload_image_path
from newrentapp.models import *
# Create your views here.

class company_OrderListView(ListView):
    model =company_Order
    template_name = 'controladmin/companyorder.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['label']
    paginate_by = 20

class productListView(ListView):
    model=product
    template_name='controladmin/product.html'
    context_object_name = 'posts'
    paginate_by = 20

class OrdersListView(ListView):
    model=Orders
    template_name='controladmin/orders.html'
    context_object_name = 'posts'
    paginate_by = 20

class detailListView(ListView):
    model = detail  
    template_name = 'controladmin/userdetail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['name']
    paginate_by = 20
    def get_queryset(self):
        return detail.objects.filter(customer=True)

def productUpdateView(request, slug):
    editProduct = product.objects.get(slug=slug)
    productForm = update_product_form(instance=editProduct)
    template_name = 'controladmin/new_update.html'
    user = request.user.email
    userDetail = detail.objects.get(email=user)
    # Label Attributes Form
    all_labels = labels_Attributes.objects.filter(category=editProduct.product_Category)
    label_data = []
    label_prefilled_name = {}
    label_values = label_Attributes_Values.objects.filter(prod=editProduct)
    for label_value in label_values:
        label_prefilled_name[label_value.label_attribute.name] = label_value
    print('PREFILLED VALUES: {}'.format(label_prefilled_name))
    for label in all_labels:
        if label.name in label_prefilled_name.keys():
            label_data.append([label, label_prefilled_name[label.name]])
        else:
            label_data.append([label, None])
    # Size form
    old_size_data = []
    old_sizes = size_color_quantity.objects.filter(linked_product = editProduct)
    print("THESE ARE OLD SIZE: {}".format(old_sizes))
    if old_sizes:
        i = 1
        for old_size in old_sizes:
            old_size_form = size_color_quantity_form(instance=old_size, prefix=str(i)+'-size')
            temp_size_images = Add_images.objects.filter(size=old_size)
            temp_image_data = []
            for size_image in temp_size_images:
                temp_image_data.append(size_image)
            old_size_data.append([old_size_form, temp_image_data, len(temp_image_data), old_size])
            i+=1
        total_size = i
    else:
        total_size = 1
    # OLD IMAGES FORM
    image_forms = []
    old_images = Add_images.objects.filter(prod=editProduct, size__isnull = True)
    print('OLD IMAGES: {}'.format(old_images))

    i = 1
    for old_image in old_images:
        old_image_form = add_images_form(instance=old_image, prefix=i)
        image_forms.append(old_image_form)
        i+=1
    total_image = i
    contextDict = {'form': productForm, 'label_data': label_data, 'size_data': old_size_data, 'total_size': total_size, 'image_forms': image_forms, 'total_image': total_image}
    # print('THIS IS CONTEXT : {}'.format(contextDict))
    # POST Request handling
    if request.method == 'POST':
        print("THIS IS POST DATA: {}".format(request.POST))
        editedProductForm = update_product_form(request.POST, request.FILES, instance=editProduct)
        if editedProductForm.is_valid():
            editedProductForm.save()

        # LABEL POST HANDLING
        for label in all_labels:
            name_val = label.name + "-value"
            if request.POST.get(name_val):
                if label.name in label_prefilled_name.keys():
                    attr = label_prefilled_name[label.name]
                    attr.value = request.POST.get(name_val)
                    attr.save()
                else:
                    new_label_attr = label_Attributes_Values(prod=editProduct, label_attribute=label, value=request.POST.get(name_val))
                    new_label_attr.save()

        # OLD SIZE POST HANDLINGG
        i = 1
        if old_sizes:
            for old_size in old_sizes:
                if request.POST.get(str(i) + "-size-delete"):
                    old_size.delete()
                else:
                    edited_size_form = size_color_quantity_form(request.POST, instance=old_size, prefix=str(i)+'-size')
                    edited_size_form.save()
                i+=1
        for k in range(i,10):
            j = str(k)
            if request.POST.get(j+'-size'):
                print(f"CREATING NEW SIZE OBJECT {j+'-size'}")
                new_size = size_color_quantity(linked_product=editProduct, 
                                                size=request.POST.get(j+'-size'),
                                                unit=request.POST.get(j+'-unit'),
                                                color=request.POST.get(j+'-color'),
                                                price=request.POST.get(j+ '-price'),
                                                c_price=request.POST.get(j+ '-c_price'),
                                                quantity=request.POST.get(j+'-quantity'),
                                                safety_stock_limit=request.POST.get(j+'-safety_stock_limit'),
                                                owned_by=userDetail)
                new_size.save()
                # if j+'-image1' in request.FILES.keys():
                for l in range(1,10):
                    m = str(l)
                    is_actual = False
                    if request.POST.get( j +'isactual'+ m):
                        postActual = request.POST.get( j +'isactual'+ m)
                        if postActual == 'true':
                            is_actual = True
                    if j+'-image'+m in request.FILES.keys():
                        size_image = Add_images(prod=editProduct, image=request.FILES[j+'-image'+m], size=new_size, is_actual=is_actual)
                        size_image.save()
            # OLD SIZE IMAGE HANDLING
        i = 1
        for size_data in old_size_data:
            temp_size_images = size_data[1]
            old_size = size_data[3]
            g = 1
            exists = size_color_quantity.objects.filter(pk = old_size.pk).count()
            print(f" EXISTS : {exists}")
            if exists:
                for old_img in temp_size_images:
                    if request.POST.get(str(i) +'-delete-'+ str(g)):
                        old_img.delete()
                    else:
                        is_actual = False
                        if request.POST.get(str(i) +'isactual'+ str(g)):
                            postActual = request.POST.get(str(i) +'isactual'+ str(g))
                            if postActual == 'true':
                                is_actual = True
                        old_img.is_actual = is_actual
                        old_img.save()
                        if str(i) +'-image'+ str(g) in request.FILES.keys():
                            updated_image = request.FILES[str(i) +'-image'+ str(g)]
                            old_img.image.save("local/product/"+ str(random.randint(1, 13516546431654)) +".jpg", updated_image)
                            old_img.save()
                    g+=1
            for j in range(g,10):
                is_actual = False
                if request.POST.get(str(i) +'isactual'+ str(j)):
                    postActual = request.POST.get(str(i) +'isactual'+ str(j))
                    if postActual == 'true':
                        is_actual = True
                if str(i) +'-image'+ str(j) in request.FILES.keys():
                    size_image = Add_images(prod=editProduct, image=request.FILES[str(i)+'-image'+str(j)], size=old_size, is_actual=is_actual)
                    size_image.save()
            i += 1


        # Image post handling
        if old_images:
            i = 1
            for old_image in old_images:
                if request.POST.get(str(i)+'-delete'):
                    old_image.delete()
                else:
                    edited_image_form = add_images_form(request.POST, request.FILES, instance=old_image, prefix=i)
                    edited_image_form.save()
                i += 1
            for k in range(i,10):
                j = str(k)
                if request.FILES.get(j+'-image'):
                    is_actual = False
                    if request.POST.get(j +'-is_actual'):
                        postActual = request.POST.get(j +'-is_actual')
                        if postActual == 'true':
                            is_actual = True
                    new_image = Add_images(prod=editProduct, image=request.FILES[j+'-image'], is_actual=is_actual)
                    new_image.save()
        else:
            for l in range(1,10):
                l = str(l)
                if request.FILES.get(l+'-image'):
                    is_actual = False
                    if request.POST.get(l +'-isactual'):
                        postActual = request.POST.get(l +'-isactual')
                        if postActual == 'true':
                            is_actual = True
                    new_image = Add_images(prod=editProduct, image=request.FILES[l+'-image'], is_actual=is_actual)
                    new_image.save()
        return HttpResponseRedirect(reverse('product'))
    return render(request, template_name, contextDict)


class productQuickeditView(LoginRequiredMixin, UpdateView):
    model = product
    #fields = '__all__'
    fields = ['price', 'offer', 'B2Boffer','sold_quantity']
    template_name = 'controladmin/product_quick_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('product')
    # print(post.id)


     
class productDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = product
    template_name='controladmin/delete.html'
    def test_func(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('product')



class orderUpdateView(LoginRequiredMixin, UpdateView):
    model = Orders
    fields='__all__'
    template_name = 'controladmin/update.html'
    def form_valid(self, form):
        return super().form_valid(form)
    '''
    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False'''
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('order')
    #print(post.id)

     
class orderDeleteView(LoginRequiredMixin, DeleteView):
    model = Orders
    template_name='controladmin/delete.html'

    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('order')



class userdetailUpdateView(LoginRequiredMixin, UpdateView):
    model = detail
    fields='__all__'
    template_name = 'controladmin/update.html'
    def form_valid(self, form):
        return super().form_valid(form)

   
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('userdetail')
    #print(post.id)

     
class userdetailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = detail
    template_name='controladmin/delete.html'
    def test_func(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('userdetail')

class companyorderUpdateView(LoginRequiredMixin, UpdateView):
    model = company_Order
    fields='__all__'
    template_name = 'controladmin/update.html'
    def form_valid(self, form):
        return super().form_valid(form)

   
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('userdetail')
    #print(post.id)

     
class companyorderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = company_Order
    template_name='controladmin/delete.html'
    def test_func(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('userdetail')

class vendorListView(ListView):
    model = detail
    template_name = 'controladmin/vendorlist.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    #ordering = ['label']
    paginate_by = 20
    def get_queryset(self):
        return detail.objects.filter(vendor=True)
@login_required
def vendorDetailView(request,pk):
    
    posts= detail.objects.filter(pk=pk)
    delivery=pick_and_deliver_order.objects.filter(product_name__seller__pk=pk)
    profit=0
    for i in delivery:
        profit+=i.product_name.price
    print(profit)
    return render(request,'controladmin/vendordashboard.html',{'posts':posts,'profit':profit})

def type_of_account(user):
    try:
        a = detail.objects.get(Q(vendor=True) | Q(staff=True), email=user.email)
        return True
    except detail.DoesNotExist:
        print("except:")
        return False

@login_required()
# @user_passes_test(type_of_account)
def dashboard(request):
    noofvendor=detail.objects.filter(vendor=True).count()
    noofcustomer=detail.objects.filter(customer=True).count()
    noofproduct=product.objects.filter().count()
    logi=staff_Categories.objects.filter(name="Logistic").first()
    nooflogistics= detail.objects.filter(staff_category=logi).count()
    # nooforders=Orders.objects.all().count()
    # noofrejectedorder=OrderItem.objects.filter(rejectedbywhom__isnull=False,acceptedbywhom__isnull=True).count()
    noofrejecteddelivery=pick_and_deliver_order.objects.filter(deliveryrejectedbywhom__isnull=False,deliveryacceptedbywhom__isnull=True).count()
    
    
    user = request.user.email
    try:
        a = detail.objects.get(email=user)
    except detail.DoesNotExist:
        a = User.objects.get(email=user)
        if a.is_superuser:
            return redirect('/admin')

    if a.vendor:
        if a.is_logistics_vendor:
            user_type = "Logistics Vendor"
        else:
            user_type = "Vendor"
    elif a.staff:
        if a.is_logistics:
            user_type = "Driver"
        elif a.is_sales:
            user_type = "Sales"
        else:
            user_type = "Other"


    if user_type == "Vendor":
        all_products = product.objects.filter(seller=a)
        all_products_length = all_products.count()

        ordder = OrderItem.objects.all().filter(is_placed=True)

        # ordered_products = ordder.get_ordered_products
        ordered_prod_list=[]
        ordered_products=[]
        for i in ordder:
            ordered_products.append(product.objects.get(slug=i.product.slug))

        ordered_product_count = 0
        for prod in ordered_products:
            for i in all_products:
                if(i==prod):
                    ordered_prod_list.append(prod)
                    ordered_product_count += 1
        
        pending_for_delivery = ordered_product_count
        rent_order_items = rental_OrderItem.objects.filter(is_placed=True)
        rent_order_left = 0
        for i in rent_order_items:
            if(i.product.seller.email == request.user.email and not i.rent_status == "Completed" ):
                rent_order_left+=1
        context = {
            "user_type": user_type,
            "all_products_length": all_products_length,
            "ordered_product_count": ordered_product_count,
             "pending_for_delivery": pending_for_delivery,
             'pending_rentals': rent_order_left,
        }

        return render(request,'controladmin/adminhome.html',context)

    elif user_type == "Driver":
        this_user = detail.objects.get(email=request.user)
        # orderitem = OrderItem.objects.filter(acceptedbywhom=this_user)

        context = {
            "user_type": user_type,
            # "orderitem": orderitem,
        }

        return render(request,'controladmin/adminhome.html',context)

    else:
        user_type = "Other"

        noofvendor=detail.objects.filter(vendor=True).count()
        noofcustomer=detail.objects.filter(customer=True).count()
        noofproduct=product.objects.filter().count()
        logi=staff_Categories.objects.filter(name="Logistic").first()
        nooflogistics= detail.objects.filter(staff_category=logi).count()
        # nooforders=Orders.objects.all().count()
        # noofrejectedorder=OrderItem.objects.filter(rejectedbywhom__isnull=False,acceptedbywhom__isnull=True).count()
        noofrejecteddelivery=pick_and_deliver_order.objects.filter(deliveryrejectedbywhom__isnull=False,deliveryacceptedbywhom__isnull=True).count()
     
        context = {
            "user_type": user_type,
            'noofrejecteddelivery':noofrejecteddelivery,
            # 'noofrejectedorder':noofrejectedorder,
            'noofvendor':noofvendor,
            'noofcustomer':noofcustomer,
            'noofproduct':noofproduct,
            'nooflogistics':nooflogistics,
            # 'nooforders':nooforders
        }

        return render(request,'controladmin/adminhome.html',context)

    context = {
        "user_type": user_type,
        "all_products_length": all_products_length,
        'noofrejecteddelivery':noofrejecteddelivery,
        # 'noofrejectedorder':noofrejectedorder,
        'noofvendor':noofvendor,
        'noofcustomer':noofcustomer,
        'noofproduct':noofproduct,
        'nooflogistics':nooflogistics,
        # 'nooforders':nooforders
    }

    return render(request,'controladmin/adminhome.html',context)

def check_vendor(user):
    try:
        a = detail.objects.get(vendor=True, email=user.email)
        return not a.is_logistics_vendor
    except detail.DoesNotExist:
        return False

@login_required()
@user_passes_test(check_vendor)
def vendor_product_list(request):
    user = request.user.email
    a = detail.objects.get(email=user)
    # all_products = size_color_quantity.objects.filter(owned_by=a)
    all_products = product.objects.filter(seller=a)
    context = {
        'all_products': all_products,
    }

    return render(request,'controladmin/vendor_product_list.html',context)

@login_required()
@user_passes_test(check_vendor)
def vendor_order_list(request):
    ordder = OrderItem.objects.all().filter(is_placed=True)
    ordered_products = []
    my_products = []
    for i in ordder:   
        if i.product.seller.email == request.user.email:
             my_products.append([i,i.product])

    add = ShippingAddress.objects.filter()
    print(my_products)
    context = {
        'my_products': my_products,
    }
    return render(request,'controladmin/vendor_order.html',context)

@login_required()
@user_passes_test(check_vendor)
def vendor_rent_order_list(request):
    rent_order_items = rental_OrderItem.objects.all().filter(is_placed=True)
    ordered_products = []
    my_products = []
    all_order_ids = []
    all_orders = []
    ORDER_STATUS_LIST = ['Placed','Accpted','Dispatched','In Use','Get Return','Completed' ]
    for i in rent_order_items:   
        if i.product.seller.email == request.user.email:
            pickup_time =  i.date_placed + timedelta(days=2)
            new_hour = 4  
            new_minutes = 30 
            pickup_time = pickup_time.replace(hour=new_hour, minute=new_minutes, second=0, microsecond=0)
            # req time is 10AM but due to async between backend and template here time taken is 4:30AM = (10AM - 5:30hrs)
            if i.rent_order.id not in all_order_ids:
                all_order_ids.append(i.rent_order.id)
                all_orders.append({
                    "id":i.rent_order.id,
                    "pickup_person":  "pickup man info comes here", 
                    "pickup_person_contact": "contact info comes here",
                    "pickup_time": pickup_time, 
                    "placed_at":i.rent_order.date_rental_placed,
                    "payment_method": i.rent_order.payment_method,
                    "chargable_amount":i.rent_order.chargable_amount,
                    "security_amount":i.rent_order.security_amount,
                })
            
            
            
            my_products.append(
                {
                    "product_name": i.product.title, 
                    "order_id": i.rent_order.id, 
                    "order_quantity": i.quantity, 
                    "size_color":i.size_color_quantity,
                    "price":i.price,
                    "amount":i.amount,
                    "start_date":i.start_date,
                    "end_date":i.end_date,
                    "rent_status":i.rent_status,
                }
            )
    my_products = sorted(my_products, key = lambda i: (i['product_name'], i['price']))
    all_orders = sorted(all_orders, key = lambda i: i['id'], reverse=True)
    context = {
        "my_products":my_products,
        "all_orders": all_orders,
        "status_list":ORDER_STATUS_LIST,
    }

    return render(request,'controladmin/rental_vendor_pickup.html',context)

@login_required()
@user_passes_test(check_vendor)
def vendor_pickup_list(request):
    ordder = OrderItem.objects.all().filter(is_placed=True)
    ordered_products = []
    my_products = []
    all_order_ids = []
    all_orders = []
    ORDER_STATUS_LIST = ['Accpted','Packed','Dispatched','Reached Nearby','Out for Delivery','Delivered','Returned' ]
    for i in ordder:   
        if i.product.seller.email == request.user.email:
            pickup_time =  i.date_placed + timedelta(days=2)
            new_hour = 4  
            new_minutes = 30 
            pickup_time = pickup_time.replace(hour=new_hour, minute=new_minutes, second=0, microsecond=0)
            # req time is 10AM but due to async between backend and template here time taken is 4:30AM = (10AM - 5:30hrs)
            if i.order.id not in all_order_ids:
                all_order_ids.append(i.order.id)
                print("gracious",i.order.id)
                all_orders.append({
                    "id":i.order.id,
                    "pickup_person":  "pickup man info comes here", 
                    "pickup_person_contact": "contact info comes here",
                    "pickup_time": pickup_time, 
                    "placed_at":i.date_placed,
                    "status": i.order.status,
                    "total":i.order.total,
                })
            
            
            peice = 0
            if(i.quantity >= float(i.product.Moq_range1.lower)):
                total = i.total
                price = total/i.quantity
            else:
                price = i.get_price
            my_products.append(
                {
                    "product_name": i.product.title, 
                    "order_id": i.order.id, 
                    "order_quantity": i.quantity, 
                    "size_color":i.size_color,
                    "price":price,
                }
            )
    my_products = sorted(my_products, key = lambda i: (i['product_name'], i['price']))
    all_orders = sorted(all_orders, key = lambda i: i['id'], reverse=True)
    context = {
        "my_products":my_products,
        "all_orders": all_orders,
        "status_list":ORDER_STATUS_LIST,
    }

    return render(request,'controladmin/vendor_pickup.html',context)


@login_required()
def admins_panel(request):
    noofvendor=detail.objects.filter(vendor=True).count()
    noofcustomer=detail.objects.filter(customer=True).count()
    noofproduct=product.objects.filter().count()
    logi=staff_Categories.objects.filter(name="Logistic").first()
    nooflogistics= detail.objects.filter(staff_category=logi).count()
    nooforders=Orders.objects.all().count()
    noofrejectedorder=OrderItem.objects.filter(rejectedbywhom__isnull=False,acceptedbywhom__isnull=True).count()
    noofrejecteddelivery=pick_and_deliver_order.objects.filter(deliveryrejectedbywhom__isnull=False,deliveryacceptedbywhom__isnull=True).count()

    context = {
        # "user_type": user_type,
        # "all_products_length": all_products_length,
        'noofrejecteddelivery':noofrejecteddelivery,
        'noofrejectedorder':noofrejectedorder,
        'noofvendor':noofvendor,
        'noofcustomer':noofcustomer,
        'noofproduct':noofproduct,
        'nooflogistics':nooflogistics,
        'nooforders':nooforders
    }

    return render(request,'controladmin/admin_panel.html',context)

@login_required()
def admins_allorder(request):
    ordder = Order()
    ordered_products = ordder.get_ordered_products

    if request.method == "POST":
        deliveryboy_id = request.POST.get('deliveryboy')
        orderitem_id = request.POST.get('orderitem_id')
        orderitem = OrderItem.objects.get(id=orderitem_id)
        orderitem.acceptedbywhom = detail.objects.get(id=deliveryboy_id)
        orderitem.save()

    context = {
        'ordered_products': ordered_products,
    }
    return render(request,'controladmin/admins_allorders.html',context)

@login_required()
def assign_deliveryboy(request, some_id):
    logi=staff_Categories.objects.filter(name="Logistic").first()
    deliveryboy=detail.objects.filter(staff_category=logi)
    orderitem = OrderItem.objects.get(id=some_id)
    cus_address=ShippingAddress.objects.get(order=orderitem.order)
    
    logi=staff_Categories.objects.filter(name="Logistic").first()
    all_deliveryboy=detail.objects.filter(staff_category=logi)

    context = {
        'orderitem': orderitem,
        'cus_address': cus_address,
        'all_deliveryboy': all_deliveryboy,
    }
    return render(request,'controladmin/assign_deliveryboy.html',context)

# in control admin make request accept and decline interface and send singal to other view
def check_driver(user):
    try:
        a = detail.objects.get(email=user.email)
        if a.is_logistics or a.is_driver:
            return True
        return False
    except detail.DoesNotExist:
        return False

@login_required
@user_passes_test(check_driver)
def delivery_panel(request):
    this_user = detail.objects.get(email=request.user)
    orderitem = OrderItem.objects.filter(acceptedbywhom=this_user)
    my_list = []
    for item in orderitem:
        delivery_address = ShippingAddress.objects.get(order=item.order).address
        product = item.product
        product_name = product.title
        product_quantity = item.quantity
        seller_object = product.seller
        seller = seller_object.name
        seller_contact = seller_object.contact
        pickup_address = seller_object.address
        receiver = item.order.customer.name
        receiver_email = item.order.customer.email
        receiver_contact = detail.objects.get(email=receiver).contact

        my_list.append(
            {
            "seller": seller, 
            "seller_contact": seller_contact, 
            "pickup_address": pickup_address, 
            "product_name": product_name, 
            "product_quantity": product_quantity, 
            "receiver":receiver, 
            "receiver_contact": receiver_contact, 
            "delivery_address": delivery_address, 
            }
        )

    context = {

        "this_user":this_user,
        "orderitem":orderitem,
        "my_list":my_list,
    }
    return render(request,'controladmin/logistic_panel.html',context)
    

# class vendorOrderView(ListView):
#     model = OrderItem
#     template_name = 'controladmin/orderitem.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     #ordering = ['label']
#     paginate_by = 20
#     def get_queryset(self):
#         query= OrderItem.objects.filter(product__seller__pk=self.kwargs.get('pk'),delivered=False,accepted=False).exclude(rejectedbywhom__pk=self.kwargs.get('pk'))|OrderItem.objects.filter(acceptedbywhom__pk=self.kwargs.get('pk'))|OrderItem.objects.filter(assigntoafterrejection__pk=self.kwargs.get('pk'))
#         return query.order_by('accepted')    


@login_required
def deliverycreate(request,pk,pk1,slug):
        if request.user.is_authenticated:
            if request.method=='POST':
                product1=request.POST['product']
                other=request.POST['other']
                instruction=request.POST['instruction']
                pick_contact=request.POST['pick_contact_number']
                pick_person=request.POST['pick_person']
                pick_date=request.POST['date']
                pick_time=request.POST['time']
                pick_address=request.POST['pick_address']
                pick_landmark=request.POST['pick_landmark']
                delivery_contact=request.POST['delivery_contact_number']
                delivery_person=request.POST['delivery_contact_person']
                delivery_date=request.POST['delivery_date']
                delivery_time=request.POST['delivery_time']
                delivery_address=request.POST['delivery_address']
                delivery_landmark=request.POST['delivery_landmark']
                distance=request.POST['distance']
                moq=request.POST['moq']
                charge_paid=request.POST['charge_paid']
                other_charge=request.POST['other_charge']
                customer_id=request.POST['customer_id']
                if product1=='Other':
                    product1=other
                if charge_paid=='Other':
                    charge_paid=other_charge
                pro_id=product.objects.get(title=product1)
                
                date=d=datetime.datetime.now().strftime('%H:%M:%S')
                transaction_id=str(request.user.id)+str(pro_id.slug)[:1]+str(''.join(list(date.split(':'))))
                print(transaction_id)
                a=pick_and_deliver_order(transaction_id=transaction_id,product_name=pro_id,packing_instruction=instruction # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                    ,pickup_contact=pick_contact,pickup_person=detail.objects.get(email=pick_person),pickup_date=pick_date,
                    pickup_address=pick_address,pickup_landmark=pick_landmark,
                    delivery_contact=delivery_contact,delivery_person=detail.objects.get(email=delivery_person),delivery_date=delivery_date,
                    delivery_address=delivery_address,delivery_landmark=delivery_landmark,
                    service_charge_paid_at=charge_paid,customer_id=customer_id,placedbystaff=detail.objects.get(pk=pk))
                a.save()
                return redirect('logisticsvendorListView',pk=pk)
        
            else:
                    super_cat=product.objects.all()
                    prod=product.objects.get(slug=slug)
                    logi=staff_Categories.objects.filter(name="Logistic").first()
                    deliveryboy=detail.objects.filter(staff_category=logi)
                    ins=OrderItem.objects.get(pk=pk1)
                    ins.delivered=True
                    ins.save()

                    cus_address=ShippingAddress.objects.filter(order=ins.order)
                    for i in cus_address:
                        print(i)
                        print(i.city)
                    return render(request,'controladmin/deliverycreate.html',{'super_cat':super_cat,'cus_address':cus_address,'prod':prod,'deliveryboy':deliveryboy})
        else:
            return redirect('login_page')
    
def editorder(request,pk,pk1):
    orderitem=OrderItem.objects.get(pk=pk1)
    order=orderitem.order
    address=ShippingAddress.objects.filter(order=order).first()
    if request.method == 'POST':
        u_form = editorderitem(request.POST, instance=orderitem)
        p_form = editorderr(request.POST,instance=orderitem.order)
        s_form = editshippingaddress(request.POST,instance=address)
        if u_form.is_valid() and p_form.is_valid() and s_form.is_valid():
            u_form.save()
            p_form.save()
            s_form.save()

            return redirect('vendororder',pk=pk)

    else:
        u_form = editorderitem(instance=orderitem)
        p_form = editorderr(instance=order)
        s_form = editshippingaddress(instance=address)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        's_form':s_form
    }
    return render(request, 'controladmin/orderupdate.html',context)


     
# class orderitemDeleteView(LoginRequiredMixin, DeleteView):
#     model = OrderItem
#     template_name='controladmin/delete.html'
#     def test_func(self):
#         if self.request.user.is_superuser or self.request.user.is_staff:
#             return True
#         return False
#     def get_success_url(self, **kwargs):         
#         if  kwargs != None:
#             return redirect('vendor',pk=self.kwargs.get('pk'))

class logisticsvendorListView(ListView):
    model = pick_and_deliver_order
    template_name = 'controladmin/pick_and_deliver_order.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    #ordering = ['label']
    paginate_by = 20
    def get_queryset(self):
        return pick_and_deliver_order.objects.filter(product_name__seller__pk=self.kwargs.get('pk'))| pick_and_deliver_order.objects.filter(placedbystaff__pk=self.kwargs.get('pk'))

@login_required
def deliveryboylist(request):    
    logi=staff_Categories.objects.filter(name="Logistic").first()
    deliveryboy=detail.objects.filter(staff_category=logi)

    return render(request,'controladmin/deliveryboylist.html',{'posts':deliveryboy})
@login_required
def deliveryadmin(request,pk):
    person=detail.objects.get(pk=pk)
    pickup=pick_and_deliver_order.objects.filter(deliveryacceptedbywhom__pk=pk).order_by('picked_up')
    deliver=pick_and_deliver_order.objects.filter(deliveryacceptedbywhom__pk=pk).order_by('delivered_up')
    p=pick_and_deliver_order.objects.filter(deliveryassigntoafterrejection__pk=pk,deliveryacceptedbywhom__isnull=True)|pick_and_deliver_order.objects.filter(pickup_person=person,deliveryacceptedbywhom__isnull=True)|pick_and_deliver_order.objects.filter(delivery_person=person,deliveryacceptedbywhom__isnull=True)
    p=p.count()
    return render(request,'controladmin/deliveryboydashboard.html',{'pickup':pickup,'deliver':deliver,'pk':pk,'deliverytobeaccepted':p})

def pickstatus(request,pk,pk1):
    ins=pick_and_deliver_order.objects.get(pk=pk1)
    ins.picked_up=True
    ins.save()
    return redirect('deliveryadmin',pk=pk)
def deliverstatus(request,pk,pk1):
    ins=pick_and_deliver_order.objects.get(pk=pk1)
    ins.delivered_up=True
    ins.save()
    return redirect('deliveryadmin',pk=pk)
@login_required
def accept(request):
    if request.method == 'GET':
               post_id = request.GET['post_id']
               pk=request.GET['pk']
               item = OrderItem.objects.get(pk=post_id) #getting the liked posts
               item.accepted=True
               item.acceptedbywhom=detail.objects.get(pk=pk) # Creating Like Object
               item.save()  # saving it to store in database
               return HttpResponse("Success!") # Sending an success response
    else:
               return HttpResponse("Request method is not a GET")
@login_required
def reject(request):
    if request.method == 'GET':
               post_id = request.GET['post_id']
               pk=request.GET['pk']
               item = OrderItem.objects.get(pk=post_id) #getting the liked posts
               
               item.rejectedbywhom=detail.objects.get(pk=pk) # Creating Like Object
               item.save()  # saving it to store in database
               return HttpResponse("Success!") # Sending an success response
    else:
               return HttpResponse("Request method is not a GET")

@login_required
def rejectedorder(request):
    posts=OrderItem.objects.filter(rejectedbywhom__isnull=False,acceptedbywhom__isnull=True)
    return render(request,'controladmin/rejectedorders.html',{'posts':posts})

@login_required
def assign(request,pk):
    ins=OrderItem.objects.filter(pk=pk).first()
    if request.method== 'POST' :
        
        b=orderform(request.POST,instance=ins)
        if b.is_valid():
            b.save()
            return redirect('rejectedorder')
    else:
        b=orderform(instance=ins)
        return render(request,'controladmin/update.html',{'form':b})

@login_required
def deliveryaccept(request):
    if request.method == 'GET':
               post_id = request.GET['post_id']
               pk=request.GET['pk']
               item = pick_and_deliver_order.objects.get(pk=post_id) #getting the liked posts
               item.accepted=True
               item.deliveryacceptedbywhom=detail.objects.get(pk=pk) # Creating Like Object
               item.save()  # saving it to store in database
               return HttpResponse("Success!") # Sending an success response
    else:
               return HttpResponse("Request method is not a GET")
@login_required
def deliveryreject(request):
    if request.method == 'GET':
               post_id = request.GET['post_id']
               pk=request.GET['pk']
               item = pick_and_deliver_order.objects.get(pk=post_id) #getting the liked posts
               
               item.deliveryrejectedbywhom=detail.objects.get(pk=pk) # Creating Like Object
               item.save()  # saving it to store in database
               return HttpResponse("Success!") # Sending an success response
    else:
               return HttpResponse("Request method is not a GET")

@login_required
def rejecteddelivery(request):
    posts=pick_and_deliver_order.objects.filter(deliveryrejectedbywhom__isnull=False,deliveryacceptedbywhom__isnull=True)
    return render(request,'controladmin/rejecteddeliveries.html',{'posts':posts})

@login_required
def deliveryassign(request,pk):
    ins=pick_and_deliver_order.objects.filter(pk=pk).first()
    if request.method== 'POST' :
        
        b=deliveryform(request.POST,instance=ins)
        if b.is_valid():
            b.save()
            return redirect('rejecteddelivery')
    else:
        b=deliveryform(instance=ins)
        return render(request,'controladmin/update.html',{'form':b})

@login_required
def deliveryacceptbyboy(request,pk):
    #p=pick_and_deliver_order.objects.filter(pickup_person__pk=pk,deliveryacceptedbywhom__isnull=True).order_by('picked_up')|pick_and_deliver_order.objects.filter(delivery_person__pk=pk,deliveryacceptedbywhom__isnull=True).order_by('delivered_up')
    pickup=pick_and_deliver_order.objects.filter(deliveryassigntoafterrejection__pk=pk,deliveryacceptedbywhom__isnull=True).order_by('picked_up')|pick_and_deliver_order.objects.filter(pickup_person__pk=pk,deliveryacceptedbywhom__isnull=True)
    deliver=pick_and_deliver_order.objects.filter(deliveryassigntoafterrejection__pk=pk,deliveryacceptedbywhom__isnull=True).order_by('delivered_up')|pick_and_deliver_order.objects.filter(delivery_person__pk=pk,deliveryacceptedbywhom__isnull=True)
    return render(request,'controladmin/deliveryaccepting.html',{'pickup':pickup,'deliver':deliver,'pk':pk})

    