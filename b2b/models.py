from django.db import models
import random, os
from django.utils import timezone
# Create your models here.
from userdetail.models import detail, staff_Categories, seller_Categories
from smart_selects.db_fields import ChainedForeignKey
import datetime

from product.models import trims_product, standard_fabric_blend, washcare_model
from seller_info.models import labels, fits, seasons

from product.models import category as cate
from product.models import sub_category, super_category, product_cate_b2b

from colorfield.fields import ColorField

from POM.models import measurement, POM, measurement_chart


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "local/b2b/logo/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class company_detail(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    company_Description = models.TextField()
    company_Mission = models.CharField(max_length=1000)
    gstin = models.CharField(max_length=255)
    logo = models.FileField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company Detail"
        verbose_name_plural = "Company Detail"


Type_of_order = (
    ('O', 'Order'),
    ('S', 'Sampling'),
    ('D', 'Design'),
    ('E', 'Enquiry'))


class color_model(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Color Model"
        verbose_name_plural = "Color Model"


class address_model(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Address Model"
        verbose_name_plural = "Address Model"


class design_theme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Design Theme"
        verbose_name_plural = "Design Theme"


Acti_Choices = (
    ('BT', 'Before Time'),
    ('IA', 'Immediate Action Required'),
    ('IP', 'In Process'),
    ('ND', 'New Delay'),
    ('OH', 'On Hold'),
    ('OT', 'On Time')
)

Order_Choices = (
    ('S', 'Started'),
    ('IP', 'In Progress'),
    ('C', 'Completed')
)

from product.models import category
from product.models import sub_category, super_category, StyleType, WashType, Fabric


class manuals(models.Model):
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_image_path)
    packing = models.BooleanField(default=False)
    folding = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Manual"


import datetime
from userdetail.models import staff_Categories



class Dependent_attr(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Dependent attributes"
        verbose_name_plural = "Dependent attributes"
class inDependent_attr(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "InDependent attributes"
        verbose_name_plural = "InDependent attributes"

class Layout(models.Model):
    type=models.CharField(max_length=50)
    width=models.IntegerField()
    height=models.IntegerField()
    alignment=models.CharField(max_length=50)
    code_type=models.CharField(max_length=50,default="Barcode")
    #dep_attr=models.ManyToManyField(Dependent_attr)
    dep_atr=models.TextField(max_length=500,default='')
    indep_atr=models.TextField(max_length=500,default='')
    #indep_attr=models.ManyToManyField(inDependent_attr)
    is_selected=models.BooleanField(default=True)


    def __str__(self):
        return "Layout"+str(self.id)

    class Meta:
        verbose_name = "Layout"
        verbose_name_plural = "Layout"

from django.contrib.postgres.fields import ArrayField

def all_poms():
    return POM.objects.all()
class company_Order(models.Model):
    user_email = models.EmailField()
    sector=models.ForeignKey(product_cate_b2b, on_delete=models.CASCADE, null=True, blank=True)
    fashion_Brand = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True)
    label = models.ForeignKey(labels, on_delete=models.CASCADE, null=True, blank=True)
    fit = models.ForeignKey(fits, on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(seasons, on_delete=models.CASCADE, null=True, blank=True)
    product_Category = models.ForeignKey(cate, on_delete=models.CASCADE, null=True, blank=True)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
    left_over = models.IntegerField(default=0)
    availiable_for_consumers = models.BooleanField(default=False)
    availiable_for_b2b = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    excel = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    dispatch_Address = models.ManyToManyField(address_model, blank=True)
    billing_Address = models.TextField(null=True, blank=True)
    total_Price = models.IntegerField(null=True, blank=True)
    quoted_Price = models.IntegerField(default=0)
    alteration_Charge = models.IntegerField(null=True, blank=True)
    custom_Charges = models.IntegerField(null=True, blank=True)
    single_unit_Price = models.IntegerField(null=True, blank=True)
    contact_Person = models.CharField(max_length=255, null=True, blank=True)
    contact_Person_No = models.IntegerField(null=True, blank=True)
    order_no = models.BigIntegerField(unique=True, null=True, blank=True, editable=False)
    enquiry_no = models.IntegerField(unique=True, null=True, blank=True)
    design_no = models.IntegerField(unique=True, null=True, blank=True)
    sampling_no = models.IntegerField(unique=True, null=True, blank=True)
    order_date_time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    order_type = models.CharField(max_length=255, choices=Type_of_order, null=True, blank=True)
    staffs_Allocated = models.ManyToManyField(detail, related_name="staffs_Allocated", blank=True)
    colors_avail = models.ManyToManyField(color_model, blank=True)
    mom = models.TextField(null=True, blank=True)
    target_lead_time = models.IntegerField(null=True, blank=True)
    target_price = models.IntegerField(null=True, blank=True)
    tech_pack = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    specs = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    custom_logo = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    logo_placement = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sizes = models.CharField(max_length=255, null=True, blank=True)
    colors = models.CharField(max_length=255, null=True, blank=True)
    design_theme = models.ForeignKey(design_theme, on_delete=models.CASCADE, null=True, blank=True)
    sample_type = models.CharField(max_length=255, null=True, blank=True)
    sample_quantity = models.IntegerField(null=True, blank=True)
    expected_sample_date = models.DateField(null=True, blank=True)
    order_expected_date = models.DateField(null=True, blank=True)
    mail_confirmation = models.BooleanField(default=False)
    sampling_needed = models.BooleanField(default=False)
    plus_Quantity_Percentage = models.IntegerField(default=0, null=True, blank=True)
    minus_Quantity_Percentage = models.IntegerField(default=0, null=True, blank=True)
    priority_no = models.IntegerField(default=0, null=True, blank=True)
    priority_quantity = models.IntegerField(default=0, null=True, blank=True)
    overall_priority = models.FloatField(default=0, null=True, blank=True)
    htm = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    packing_manual = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    washcare = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    fabrics = models.ForeignKey(trims_product, on_delete=models.CASCADE, null=True, blank=True)
    fabric_consump = models.CharField(max_length=255, null=True, blank=True)
    fabric_color = models.CharField(max_length=255, null=True, blank=True)
    accesories = models.CharField(max_length=255, null=True, blank=True)
    packing_details = models.CharField(max_length=255, null=True, blank=True)
    cpo = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    status = models.CharField(max_length=255, choices=Order_Choices, null=True, blank=True)
    mode = models.CharField(max_length=255, null=True, blank=True)
    route = models.CharField(max_length=255, null=True, blank=True)
    packing_generated = models.BooleanField(default=False)
    from_enquiry = models.BooleanField(default=False)
    from_sample = models.BooleanField(default=False)
    from_design = models.BooleanField(default=False)
    from_order_no = models.IntegerField(null=True, blank=True)
    vendor_from_date = models.DateField(null=True, blank=True)
    vendor_to_date = models.DateField(null=True, blank=True)
    max_quantity_per_consumer = models.IntegerField(default=1000)
    assortment_custom = models.BooleanField(default=False)
    assortment_size_set = models.BooleanField(default=True)
    assortment_brand = models.BooleanField(default=False)
    assortment_per_customer = models.BooleanField(default=False)
    order_password = models.CharField(max_length=255, null=True, blank=True)
    personal_order = models.BooleanField(default=False)
    show_pom_in_assortment = models.BooleanField(default=False)
    fabric_blend = models.ForeignKey(standard_fabric_blend, on_delete=models.CASCADE, null=True, blank=True)
    washcare_obj = models.ForeignKey(washcare_model, on_delete=models.CASCADE, null=True, blank=True)
    pickup_lat = models.FloatField(default=0.00)
    pickup_lng = models.FloatField(default=0.00)
    delivery_lat = models.FloatField(default=0.00)
    delivery_lng = models.FloatField(default=0.00)
    custom_assortment = models.BooleanField(default=False)
    allowed_sizes = models.TextField(blank=True)
    other_fields = models.TextField(null=True, blank=True)
    other_fields_values = models.TextField(null=True, blank=True)
    design_code=models.CharField(max_length=255, null=True, blank=True)
    garment_code=models.CharField(max_length=255, null=True, blank=True)
    style_code=models.CharField(max_length=255, null=True, blank=True)
    fabric_code=models.CharField(max_length=255, null=True, blank=True)
    style_description = models.TextField(null=True, blank=True)
    accepted_rate=models.CharField(max_length=255, null=True, blank=True)
    rejection_rate=models.CharField(max_length=255, null=True, blank=True)
    stock=models.CharField(max_length=255, null=True, blank=True)
    wastage=models.CharField(max_length=255, null=True, blank=True)
    lead_time=models.CharField(max_length=255, null=True, blank=True)
    tentative_cost=models.CharField(max_length=255, null=True, blank=True)
    layout = models.ForeignKey(Layout, null=True, default=None, on_delete=models.SET_NULL, blank=True)
    fabric_type = models.ForeignKey(Fabric, null=True, default=None, on_delete=models.CASCADE, blank=True)
    wash_type = models.ForeignKey(WashType, null=True, default=None, on_delete=models.CASCADE, blank=True)
    style_type = models.ForeignKey(StyleType, null=True, default=None, on_delete=models.CASCADE, blank=True)
    garment_matching_parameter_and_level=models.CharField(max_length=255, null=True, blank=True)
    repeat_size = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute = ArrayField(models.CharField(max_length=255, blank=True, null=True), size=50, blank=True, null=True)
    label_atrribute1 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute2 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute3 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute4 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute5 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute6 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute7 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute8 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute9 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute10 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute11 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute12 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute13 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute14 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute15 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute16 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute17 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute18 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute19 = models.CharField(max_length=255, null=True, blank=True)
    label_atrribute20 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute1 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute2 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute3 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute4 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute5 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute6 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute7 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute8 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute9 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute10 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute11 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute12 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute13 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute14 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute15 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute16 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute17 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute18 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute19 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute20 = models.CharField(max_length=255, null=True, blank=True)
    trims_atrribute = ArrayField(models.CharField(max_length=255, blank=True, null=True), size=50, blank=True, null=True)
    poms_fields = ArrayField(models.CharField(max_length=255, blank=True, null=True), size=50, blank=True, null=True)
    poms_keys = models.ManyToManyField(POM)

    

    
    def __str__(self):
        return str(self.order_no)

    class Meta:
        verbose_name = "Company Order"
        verbose_name_plural = "Company Order"

    @property
    def get_measurement_chart(self):
        # cur=self.order_date_time
        meas = measurement.objects.filter(user=self.fashion_Brand, season=self.season,
                                          product_Supercategory=self.product_Supercategory).first()
        return meas

    @property
    def get_sizes(self):
        pom = POM.objects.filter(product_Supercategory=self.product_Supercategory).first()
        obj = measurement_chart.objects.filter(chart=self.get_measurement_chart, pom=pom)
        sizes = []
        for i in obj:
            if not (i.size in sizes):
                sizes.append(i.size)
        return sizes

    @property
    def get_billing_month(self):
        # cur=self.order_date_time
        bill_month = self.order_date_time + datetime.timedelta(days=self.target_lead_time)
        return bill_month.date

    @property
    def get_billing_amount(self):
        if self.total_Price:
            price = self.total_Price
        elif self.target_price:
            price = self.target_price
        else:
            price = 0
        price = price * self.quantity
        return price

    @property
    def get_merchandiser(self):
        staffs = self.staffs_Allocated.all()
        merch = staff_Categories.objects.filter(name="Merchandising").first()
        staffs = staffs.filter(staff=True, staff_category=merch).first()
        return staffs

    @property
    def get_sales(self):
        staffs = self.staffs_Allocated.all()
        sales = staff_Categories.objects.filter(name="Sales").first()
        staffs = staffs.filter(staff=True, staff_category=sales).first()
        return staffs

    @property
    def get_garment_vendor(self):
        staffs = self.staffs_Allocated.all()
        gar = seller_Categories.objects.filter(name="Garmenting Vendor").first()
        staffs = staffs.filter(vendor=True, seller_category=gar).first()
        return staffs


class consumer_Order_Quantity(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    max_quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Consumer Order Quantity "
        verbose_name_plural = "Consumer Order Quantity"


class priority_of_order(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    priority_no = models.IntegerField()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Order Priority"
        verbose_name_plural = "Order Priority"


# class size_Data(models.Model):
# 	brand=models.ForeignKey(brand,on_delete=models.CASCADE)
# 	size=models.IntegerField()
# 	shoulder=models.IntegerField()
# 	back=models.IntegerField()
# 	front=models.IntegerField()
# 	bicep=models.IntegerField()
# 	chest=models.IntegerField()
# 	hip=models.IntegerField()
# 	waist=models.IntegerField()
# 	sleeve=models.IntegerField()
# 	cuff=models.IntegerField()


def incrementpro():
    last_booking = production_Order.objects.all().order_by('id').last()
    if not last_booking:
        return str(datetime.date.today().year) + 'PRO' + '000001'
    booking_id = last_booking.production_No
    booking_int = int(booking_id[7:])
    new_booking_int = booking_int + 1
    new_booking_id = str(str(datetime.date.today().year)) + 'PRO' + str(new_booking_int).zfill(6)
    return new_booking_id


# class production_Order(models.Model):
# 	user_email=models.EmailField()
# 	fashion_Brand=models.CharField(max_length=255)
# 	quantity=models.IntegerField()
# 	size=models.IntegerField()
# 	order_no=models.IntegerField()
# 	production_No=models.CharField(unique=True,default=incrementpro,max_length=255)
# 	sample_No=models.CharField(null=True,blank=True,max_length=255)


# 	def __str__(self):
# 		return str(self.production_No)


class alteration_assortment(models.Model):
    pom = models.ForeignKey(POM, on_delete=models.CASCADE)
    alteration = models.FloatField(default=0.00)

    def __str__(self):
        return str(self.alteration)


class assortment(models.Model):
    user = models.EmailField()
    user_name = models.CharField(max_length=255)
    order_no = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    size_label = models.IntegerField()
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    comment = models.CharField(max_length=255, null=True, blank=True)
    distributed = models.BooleanField(default=False)
    alteration_req = models.BooleanField(default=False)
    alteration_cost = models.IntegerField(default=0)
    attribute1 = models.FloatField(default=0)
    deviation1 = models.FloatField(default=0)
    alteration1 = models.FloatField(default=0)
    alteration_Cost1 = models.IntegerField(default=0)
    attribute2 = models.FloatField(default=0)
    deviation2 = models.FloatField(default=0)
    alteration2 = models.FloatField(default=0)
    alteration_Cost2 = models.IntegerField(default=0)
    attribute3 = models.FloatField(default=0)
    deviation3 = models.FloatField(default=0)
    alteration3 = models.FloatField(default=0)
    alteration_Cost3 = models.IntegerField(default=0)
    attribute4 = models.FloatField(default=0)
    deviation4 = models.FloatField(default=0)
    alteration4 = models.FloatField(default=0)
    alteration_Cost4 = models.IntegerField(default=0)
    attribute5 = models.FloatField(default=0)
    deviation5 = models.FloatField(default=0)
    alteration5 = models.FloatField(default=0)
    alteration_Cost5 = models.IntegerField(default=0)
    attribute6 = models.FloatField(default=0)
    deviation6 = models.FloatField(default=0)
    alteration6 = models.FloatField(default=0)
    alteration_Cost6 = models.IntegerField(default=0)
    attribute7 = models.FloatField(default=0)
    deviation7 = models.FloatField(default=0)
    alteration7 = models.FloatField(default=0)
    alteration_Cost7 = models.IntegerField(default=0)
    attribute8 = models.FloatField(default=0)
    deviation8 = models.FloatField(default=0)
    alteration8 = models.FloatField(default=0)
    alteration_Cost8 = models.IntegerField(default=0)
    attribute9 = models.FloatField(default=0)
    deviation9 = models.FloatField(default=0)
    alteration9 = models.FloatField(default=0)
    alteration_Cost9 = models.IntegerField(default=0)
    attribute10 = models.FloatField(default=0)
    deviation10 = models.FloatField(default=0)
    alteration10 = models.FloatField(default=0)
    alteration_Cost10 = models.IntegerField(default=0)
    attribute11 = models.FloatField(default=0)
    deviation11 = models.FloatField(default=0)
    alteration11 = models.FloatField(default=0)
    alteration_Cost11 = models.IntegerField(default=0)
    attribute12 = models.FloatField(default=0)
    deviation12 = models.FloatField(default=0)
    alteration12 = models.FloatField(default=0)
    alteration_Cost12 = models.IntegerField(default=0)
    attribute13 = models.FloatField(default=0)
    deviation13 = models.FloatField(default=0)
    alteration13 = models.FloatField(default=0)
    alteration_Cost13 = models.IntegerField(default=0)
    attribute14 = models.FloatField(default=0)
    deviation14 = models.FloatField(default=0)
    alteration14 = models.FloatField(default=0)
    alteration_Cost14 = models.IntegerField(default=0)
    attribute15 = models.FloatField(default=0)
    deviation15 = models.FloatField(default=0)
    alteration15 = models.FloatField(default=0)
    alteration_Cost15 = models.IntegerField(default=0)
    attribute16 = models.FloatField(default=0)
    deviation16 = models.FloatField(default=0)
    alteration16 = models.FloatField(default=0)
    alteration_Cost16 = models.IntegerField(default=0)
    attribute17 = models.FloatField(default=0)
    deviation17 = models.FloatField(default=0)
    alteration17 = models.FloatField(default=0)
    alteration_Cost17 = models.IntegerField(default=0)
    attribute18 = models.FloatField(default=0)
    deviation18 = models.FloatField(default=0)
    alteration18 = models.FloatField(default=0)
    alteration_Cost18 = models.IntegerField(default=0)
    attribute19 = models.FloatField(default=0)
    deviation19 = models.FloatField(default=0)
    alteration19 = models.FloatField(default=0)
    alteration_Cost19 = models.IntegerField(default=0)
    attribute20 = models.FloatField(default=0)
    deviation20 = models.FloatField(default=0)
    alteration20 = models.FloatField(default=0)
    alteration_Cost20 = models.IntegerField(default=0)
    attribute21 = models.FloatField(default=0)
    deviation21 = models.FloatField(default=0)
    alteration21 = models.FloatField(default=0)
    alteration_Cost21 = models.IntegerField(default=0)
    attribute22 = models.FloatField(default=0)
    deviation22 = models.FloatField(default=0)
    alteration22 = models.FloatField(default=0)
    alteration_Cost22 = models.IntegerField(default=0)
    attribute23 = models.FloatField(default=0)
    deviation23 = models.FloatField(default=0)
    alteration23 = models.FloatField(default=0)
    alteration_Cost23 = models.IntegerField(default=0)
    attribute24 = models.FloatField(default=0)
    deviation24 = models.FloatField(default=0)
    alteration24 = models.FloatField(default=0)
    alteration_Cost24 = models.IntegerField(default=0)
    attribute25 = models.FloatField(default=0)
    deviation25 = models.FloatField(default=0)
    alteration25 = models.FloatField(default=0)
    alteration_Cost25 = models.IntegerField(default=0)
    attribute26 = models.FloatField(default=0)
    deviation26 = models.FloatField(default=0)
    alteration26 = models.FloatField(default=0)
    alteration_Cost26 = models.IntegerField(default=0)
    attribute27 = models.FloatField(default=0)
    deviation27 = models.FloatField(default=0)
    alteration27 = models.FloatField(default=0)
    alteration_Cost27 = models.IntegerField(default=0)
    attribute28 = models.FloatField(default=0)
    deviation28 = models.FloatField(default=0)
    alteration28 = models.FloatField(default=0)
    alteration_Cost28 = models.IntegerField(default=0)
    attribute29 = models.FloatField(default=0)
    deviation29 = models.FloatField(default=0)
    alteration29 = models.FloatField(default=0)
    alteration_Cost29 = models.IntegerField(default=0)
    attribute30 = models.FloatField(default=0)
    deviation30 = models.FloatField(default=0)
    alteration30 = models.FloatField(default=0)
    alteration_Cost30 = models.IntegerField(default=0)
    alteration_assort = models.ManyToManyField(alteration_assortment, blank=True)
    alteration_bool = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_no)

    class Meta:
        verbose_name = "Assortment"
        verbose_name_plural = "Assortment"


class quantity_b2b(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    size = models.ForeignKey(measurement, on_delete=models.CASCADE, null=True, blank=True)
    size_label = models.IntegerField()
    quantity = models.IntegerField()
    production = models.BooleanField(default=False)
    packing = models.BooleanField(default=False)
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE, null=True, blank=True)
    assortments = models.ManyToManyField(assortment, blank=True)
    is_csv = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order.order_no)

    class Meta:
        verbose_name = "B2B Quantity"
        verbose_name_plural = "B2B Quantity"


class balance_quantity_b2b(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    size = models.ForeignKey(measurement, on_delete=models.CASCADE, null=True, blank=True)
    size_label = models.IntegerField()
    quantity = models.IntegerField()
    production = models.BooleanField(default=False)
    packing = models.BooleanField(default=False)
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE, null=True, blank=True)
    assortments = models.ManyToManyField(assortment, blank=True)
    is_csv = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order.order_no)

    class Meta:
        verbose_name = "Balance B2B Quantity"
        verbose_name_plural = "Balance B2B Quantity"


field_type = (
    ('C', 'Char Field(max Length - 255)'),
    ('I', 'Integer Field'),
    ('F', 'File Field'),
    ('D', 'Drop-Down Field'))

attri_link = (
    ('htm', 'How to Measure'),
    ('pack_manual', 'Packing Manual'),
    ('wash_care', 'Wash-Care'))


class custom_Form_Attribute(models.Model):
    name = models.CharField(max_length=255)
    field_Type = models.CharField(max_length=255, choices=field_type)
    description = models.TextField(null=True, blank=True)
    attribute_Link_To = models.CharField(max_length=255, choices=attri_link, null=True, blank=True)
    dropdown_Data1 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data2 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data3 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data4 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data5 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data6 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data7 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data8 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data9 = models.CharField(max_length=255, null=True, blank=True)
    dropdown_Data10 = models.CharField(max_length=255, null=True, blank=True)
    staff_Category_Edit_Permissions = models.ManyToManyField(staff_Categories, blank=True, related_name="staff_Edit")
    seller_Category_Edit_Permissions = models.ManyToManyField(seller_Categories, blank=True, related_name="seller_Edit")
    individual_User_Edit_Permissions = models.ManyToManyField(detail, blank=True, related_name="user_Edit")
    staff_Category_View_Permissions = models.ManyToManyField(staff_Categories, blank=True, related_name="staff_View")
    seller_Category_View_Permissions = models.ManyToManyField(seller_Categories, blank=True, related_name="seller_View")
    individual_User_View_Permissions = models.ManyToManyField(detail, blank=True, related_name="user_View")

    def __str__(self):
        return str(self.name) + "_Id:" + str(self.id)

    class Meta:
        verbose_name = "Custom Form Attribute"
        verbose_name_plural = "Custom Form Attribute"


class custom_Form(models.Model):
    seller_category = models.ForeignKey(seller_Categories, on_delete=models.CASCADE, null=True, blank=True)
    staff_category = models.ForeignKey(staff_Categories, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    attributes = models.ManyToManyField(custom_Form_Attribute)
    calculation_Field_Name = models.CharField(max_length=255, null=True, blank=True)
    calculation_Field_Equation = models.CharField(max_length=255, null=True, blank=True)
    calculation_Field_Name1 = models.CharField(max_length=255, null=True, blank=True)
    calculation_Field_Equation1 = models.CharField(max_length=255, null=True, blank=True)
    calculation_Field_Name2 = models.CharField(max_length=255, null=True, blank=True)
    calculation_Field_Equation2 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Custom Form"
        verbose_name_plural = "Custom Form"

class custom_Form_Data(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    form = models.ForeignKey(custom_Form, on_delete=models.CASCADE)
    data1 = models.CharField(max_length=255, null=True, blank=True)
    data2 = models.CharField(max_length=255, null=True, blank=True)
    data3 = models.CharField(max_length=255, null=True, blank=True)
    data4 = models.CharField(max_length=255, null=True, blank=True)
    data5 = models.CharField(max_length=255, null=True, blank=True)
    data6 = models.CharField(max_length=255, null=True, blank=True)
    data7 = models.CharField(max_length=255, null=True, blank=True)
    data8 = models.CharField(max_length=255, null=True, blank=True)
    data9 = models.CharField(max_length=255, null=True, blank=True)
    data10 = models.CharField(max_length=255, null=True, blank=True)
    data11 = models.CharField(max_length=255, null=True, blank=True)
    data12 = models.CharField(max_length=255, null=True, blank=True)
    data13 = models.CharField(max_length=255, null=True, blank=True)
    data14 = models.CharField(max_length=255, null=True, blank=True)
    data15 = models.CharField(max_length=255, null=True, blank=True)
    data16 = models.CharField(max_length=255, null=True, blank=True)
    data17 = models.CharField(max_length=255, null=True, blank=True)
    data18 = models.CharField(max_length=255, null=True, blank=True)
    data19 = models.CharField(max_length=255, null=True, blank=True)
    data20 = models.CharField(max_length=255, null=True, blank=True)
    data21 = models.CharField(max_length=255, null=True, blank=True)
    data22 = models.CharField(max_length=255, null=True, blank=True)
    data23 = models.CharField(max_length=255, null=True, blank=True)
    data24 = models.CharField(max_length=255, null=True, blank=True)
    data25 = models.CharField(max_length=255, null=True, blank=True)
    data26 = models.CharField(max_length=255, null=True, blank=True)
    data27 = models.CharField(max_length=255, null=True, blank=True)
    data28 = models.CharField(max_length=255, null=True, blank=True)
    data29 = models.CharField(max_length=255, null=True, blank=True)
    data30 = models.CharField(max_length=255, null=True, blank=True)
    data31 = models.CharField(max_length=255, null=True, blank=True)
    data32 = models.CharField(max_length=255, null=True, blank=True)
    data33 = models.CharField(max_length=255, null=True, blank=True)
    data34 = models.CharField(max_length=255, null=True, blank=True)
    data35 = models.CharField(max_length=255, null=True, blank=True)
    data36 = models.CharField(max_length=255, null=True, blank=True)
    data37 = models.CharField(max_length=255, null=True, blank=True)
    data38 = models.CharField(max_length=255, null=True, blank=True)
    data39 = models.CharField(max_length=255, null=True, blank=True)
    data40 = models.CharField(max_length=255, null=True, blank=True)
    data41 = models.CharField(max_length=255, null=True, blank=True)
    data42 = models.CharField(max_length=255, null=True, blank=True)
    data43 = models.CharField(max_length=255, null=True, blank=True)
    data44 = models.CharField(max_length=255, null=True, blank=True)
    data45 = models.CharField(max_length=255, null=True, blank=True)
    data46 = models.CharField(max_length=255, null=True, blank=True)
    data47 = models.CharField(max_length=255, null=True, blank=True)
    data48 = models.CharField(max_length=255, null=True, blank=True)
    data49 = models.CharField(max_length=255, null=True, blank=True)
    data50 = models.CharField(max_length=255, null=True, blank=True)
    file1 = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    file2 = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    file3 = models.FileField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Custom Form Data"
        verbose_name_plural = "Custom Form Data"


# for i in range(11,51):
# 	print("""	data"""+str(i)+"""=models.CharField(max_length=255,null=True,blank=True)""")
Choices = (
    ('H', 'Head'),
    ('M', 'Manager'),
    ('C', 'Staff')
)

Chaman = (
    ('B', 'Bill of Materials'),
    ('P', 'Packing List'),
    ('D', 'Distribution List'),
    ('C', 'Cummlative List'),
    ('L', 'Logistics Request'),
    ('Q', 'Quality Evaluation')
)

class activities_Category(models.Model):
    sequence = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    # product_Category=models.ForeignKey(cate,on_delete=models.CASCADE)
    # product_Subcategory = ChainedForeignKey(
    #        sub_category,
    #        chained_field="product_Category",
    #        chained_model_field="product_Category",
    #        show_all=False,
    #        auto_choose=True,
    #        sort=False)
    # product_Supercategory= ChainedForeignKey(
    # 	super_category,
    # 	chained_field="product_Subcategory",
    # 	chained_model_field="product_Subcategory",
    # 	show_all=False,
    # 	auto_choose=True,
    # 	sort=False)
    staff_category = models.ForeignKey(staff_Categories, on_delete=models.CASCADE, null=True, blank=True)
    seller_category = models.ForeignKey(seller_Categories, on_delete=models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length=255, choices=Choices, null=True, blank=True)
    request_Forms = models.ManyToManyField(custom_Form, blank=True)
    completed_in = models.IntegerField(default=1)
    very_Early_Color = ColorField(default='#00FF00')
    before_Time_Color = ColorField(default='#FFFF33')
    on_Time_Color = ColorField(default='#FF7F50')
    late_Time_Color = ColorField(default='#6495ED')
    very_Late_Color = ColorField(default='#FF0000')
    type_of_order = models.CharField(max_length=255, blank=True, null=True, choices=Type_of_order)
    linked_activity = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    Increment_or_Decrement = models.IntegerField(default=1)
    lead_Time_for_120_Days = models.IntegerField(default=0)
    lead_Time_for_105_Days = models.IntegerField(default=0)
    lead_Time_for_90_Days = models.IntegerField(default=0)
    lead_Time_for_75_Days = models.IntegerField(default=0)
    lead_Time_for_60_Days = models.IntegerField(default=0)
    lead_Time_for_45_Days = models.IntegerField(default=0)
    lead_Time_for_30_Days = models.IntegerField(default=0)
    lead_Time_for_15_Days = models.IntegerField(default=0)
    lead_Time_for_7_Days = models.IntegerField(default=0)
    lead_Time_for_3_Days = models.IntegerField(default=0)
    escalation_Time_for_Executive = models.IntegerField(default=20)
    escalation_Time_for_Manager = models.IntegerField(default=20)
    escalation_Time_for_Head = models.IntegerField(default=20)
    standard_forms = models.CharField(max_length=255, choices=Chaman, null=True, blank=True)
    factory_Completion_Activity = models.BooleanField(default=False)
    factory_Dispatch_Activity = models.BooleanField(default=False)

    class Meta:
        ordering = ['sequence']
        verbose_name = "Activities Category"
        verbose_name_plural = "Activities Category"

    def __str__(self):
        return "Activity No - " + str(self.title)

    class Meta:
        verbose_name = "Activity Category"
        verbose_name_plural = "Activity Category"


class macro_Activities(models.Model):
    title = models.CharField(max_length=255)
    activities = models.ManyToManyField(activities_Category, blank=True)
    type_of_activity = models.CharField(max_length=255, choices=Type_of_order, default='O')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Macro Activity"
        verbose_name_plural = "Macro Activity"


class activities(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    activity_Cate = models.ForeignKey(activities_Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    prev_lap = models.IntegerField(null=True, blank=True)
    lap = models.IntegerField(null=True, blank=True)
    custom_date = models.DateField(null=True, blank=True)
    actual_date = models.DateField(null=True, blank=True)
    planned_date = models.DateField(null=True, blank=True)
    created_on = models.DateField(default=timezone.now)
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=Acti_Choices, null=True, blank=True)
    esclated_user = models.ManyToManyField(detail, related_name='esclated_user')
    logistics_pickup_address = models.TextField(null=True, blank=True)
    logistics_delivery_address = models.TextField(null=True, blank=True)
    logistics_delivery_date = models.DateField(default=timezone.now)
    logistics_pickup_user = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name='logistics_pickup_user')
    logistics_delivery_user = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True,
                                                related_name='logistics_delivery_user')
    logistics_invoice_date = models.DateField(null=True, blank=True)
    lr_number = models.IntegerField(null=True, blank=True)
    tentative_date = models.DateField(null=True, blank=True)
    upto_head = models.BooleanField(default=False)
    upto_manager = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Activities"
        verbose_name_plural = "Activities"


class activity_sub_status(models.Model):
    acti = models.ForeignKey(activities, on_delete=models.CASCADE)
    sub_status = models.CharField(max_length=255)
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class notifications(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=255)
    type_of_order = models.CharField(max_length=255, blank=True, null=True, choices=Type_of_order)
    by_staff = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notifications"
        verbose_name_plural = "Notifications"


class size_assortment(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    assortment_no = models.IntegerField()
    sizes = models.ManyToManyField(quantity_b2b, blank=True)
    is_csv = models.BooleanField(default=False)
import datetime

class size_assortment_1(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    assortment_no = models.IntegerField()
    sizes = models.ManyToManyField(quantity_b2b, blank=True)
    is_csv = models.BooleanField(default=False)
    time=models.DateTimeField(default=None,null=True)
    description=models.TextField(default="")
    converted=models.BooleanField(default=False)

class production_order(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    production_no = models.IntegerField()
    sizes = models.ManyToManyField(quantity_b2b, blank=True)
    is_csv = models.BooleanField(default=False)
    time=models.DateTimeField(default=None,null=True)
    def __str__(self):
        return str(self.production_no)

    class Meta:
        verbose_name = "Production Order"
        verbose_name_plural = "Production Order"

class balance_list_2(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    list_no = models.IntegerField()
    sizes = models.ManyToManyField(balance_quantity_b2b, blank=True)
    is_csv = models.BooleanField(default=False)


class plqty(models.Model):
    size = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    leftquantity = models.IntegerField(default=1)


class size_color_quantity(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE, null=True, default=None)
    size = models.IntegerField()
    color = models.ForeignKey(color_model, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Carton_new(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE, default=None, null=True)
    is_filled = models.BooleanField(default=False)
    left_capacity = models.IntegerField(default=2)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE, null=True, default=None)
    sizes = models.ManyToManyField(size_color_quantity)
    qr = models.CharField(max_length=255)


class new_pl(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(plqty, blank=True)
    scan = models.BooleanField(default=False)
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, default=None, null=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE)
    list_no=models.IntegerField(default=1)
    quantity = models.IntegerField()
    date_time=models.DateTimeField(default=None,null=True)
    description=models.TextField(max_length=500,default=" ")
    is_packed = models.BooleanField(default=False)
class list_types(models.Model):
    name=models.CharField(max_length=50)

class distribution_list_1(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(size_color_quantity, blank=True)
    scan = models.BooleanField(default=False)
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, default=None, null=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE)
    list_no = models.IntegerField(default=1)
    quantity = models.IntegerField()
    date_time = models.DateTimeField(default=None, null=True)
    description = models.TextField(max_length=500, default=" ")
    is_packed = models.BooleanField(default=False)

class dispatch_list(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(size_color_quantity, blank=True)
    scan = models.BooleanField(default=False)
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, default=None, null=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE)
    list_no = models.IntegerField(default=1)
    quantity = models.IntegerField()
    date_time = models.DateTimeField(default=None, null=True)
    description = models.TextField(max_length=500, default=" ")
    is_packed = models.BooleanField(default=False)

class logistic_list(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(size_color_quantity, blank=True)
    scan = models.BooleanField(default=False)
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, default=None, null=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE)
    list_no = models.IntegerField(default=1)
    quantity = models.IntegerField()
    date_time = models.DateTimeField(default=None, null=True)
    description = models.TextField(max_length=500, default=" ")
    is_packed = models.BooleanField(default=False)

class warehouse_list(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(size_color_quantity, blank=True)
    scan = models.BooleanField(default=False)
    color = models.ForeignKey(color_model, on_delete=models.CASCADE, default=None, null=True)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE)
    list_no = models.IntegerField(default=1)
    quantity = models.IntegerField()
    date_time = models.DateTimeField(default=None, null=True)
    description = models.TextField(max_length=500, default=" ")
    is_packed = models.BooleanField(default=False)


class packing_list_1(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    list_no = models.IntegerField()
    sizes = models.ManyToManyField(quantity_b2b, blank=True)
    is_csv = models.BooleanField(default=False)


class chats_head(models.Model):
    user1 = models.ForeignKey(detail, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(detail, on_delete=models.CASCADE, related_name="user2")
    last_message = models.TextField(null=True, blank=True)
    last_message_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Chat Head"
        verbose_name_plural = "Chat Head"


class messages_head(models.Model):
    chat = models.ForeignKey(chats_head, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    sent_by_user1 = models.BooleanField(default=True)
    sent_by_user2 = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Message Head"
        verbose_name_plural = "Message Head"


class acti(models.Model):
    acti_file = models.FileField(upload_to=upload_image_path)

    def __str__(self):
        return self.acti_file

    class Meta:
        verbose_name = "Acti File"
        verbose_name_plural = "Acti File"


from product.models import trims_product


class trims_bom(models.Model):
    trim = models.ForeignKey(trims_product, on_delete=models.CASCADE)
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    specification = models.CharField(max_length=255, null=True, blank=True)
    consumption = models.IntegerField(null=True, blank=True)
    wastage = models.IntegerField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    fabric = models.BooleanField(default=False)
    packing = models.BooleanField(default=False)
    sewing = models.BooleanField(default=False)
    uom = models.CharField(max_length=255, null=True, blank=True)
    finishing = models.BooleanField(default=False)

    def __str__(self):
        return str(self.trim)

    class Meta:
        verbose_name = "Trims BOM"
        verbose_name_plural = "Trims BOM"

    @property
    def cost(self):
        consum = self.consumption
        waste = self.wastage
        total_consum = consum + (consum * (waste / 100))
        cost_in = total_consum * self.rate
        return round(cost_in, 2)

    @property
    def trim_quantity(self):
        consum = self.consumption
        waste = self.wastage
        total_consum = (consum + (consum * (waste / 100)))
        if self.order:
            total_consum *= self.order.quantity
        return round(total_consum, 1)


class bom(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    products = models.ManyToManyField(trims_product)
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE, null=True, blank=True)
    merchandising_cost = models.IntegerField(default=0)
    warehouse_cost = models.IntegerField(default=0)
    freight_charges = models.IntegerField(default=0)
    primary_pack_cost = models.IntegerField(default=0)
    sampling_cost = models.IntegerField(default=0)
    barcode_cost = models.IntegerField(default=0)
    cutmake_consum = models.FloatField(default=0)
    cutmake_rate = models.FloatField(default=0)
    cutmake_cost = models.FloatField(default=0)
    profit_percentage = models.FloatField(default=0)
    total_cost = models.FloatField(null=True, blank=True)
    trims_used = models.ManyToManyField(trims_bom, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "BOM"
        verbose_name_plural = "BOM"

    @property
    def total_cost_vendor(self):
        trims_act = self.trims_used.all()
        total_cost = 0
        for i in trims_act:
            total_cost += i.cost
        total_cost += (self.cutmake_consum * self.cutmake_rate)
        total_cost += (total_cost * self.profit_percentage / 100)
        return round(total_cost, 2)

    @property
    def total_cost_staff(self):
        trims_act = self.trims_used.all()
        total_cost = 0
        for i in trims_act:
            total_cost += i.cost
        total_cost += (self.cutmake_consum * self.cutmake_rate)
        total_cost += (total_cost * self.profit_percentage / 100)
        total_cost += self.merchandising_cost
        total_cost += self.warehouse_cost
        total_cost += self.freight_charges
        total_cost += self.primary_pack_cost
        total_cost += self.sampling_cost
        total_cost += self.barcode_cost
        return round(total_cost, 2)


import datetime


class trims_orders(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    trim_bom = models.ForeignKey(trims_bom, on_delete=models.CASCADE)
    placed_by = models.ForeignKey(detail, on_delete=models.CASCADE, related_name="placed_by")
    placed_to = models.ForeignKey(detail, on_delete=models.CASCADE, related_name="placed_to")
    rate = models.IntegerField(default=0)
    moq = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    lead_time = models.IntegerField(default=0)
    floated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = "Trims Orders"
        verbose_name_plural = "Trims Orders"

    @property
    def get_expected_delivery(self):
        lead_time = self.lead_time
        expected = datetime.datetime.now() + datetime.timedelta(days=lead_time)
        if lead_time:
            return expected.date
        else:
            return False


class quantity_color_map(models.Model):
    quantity_key = models.ForeignKey(quantity_b2b, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.quantity)


Carton_Status = (
    ('U', 'Under Process'),
    ('P', 'Packed'),
    ('D', 'Dispatched'),
    ('DD', 'Delivered')
)


class order_status(models.Model):
    sequence = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    distributed = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Order Status"
        verbose_name_plural = "Order Status"


class cartons_list(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE)
    carton_password = models.CharField(max_length=255, null=True, blank=True)
    carton_status = models.ForeignKey(order_status, on_delete=models.CASCADE, null=True, blank=True)
    map_for_color = models.ManyToManyField(quantity_color_map, blank=True)
    quantity_24 = models.IntegerField(null=True, blank=True)
    quantity_26 = models.IntegerField(null=True, blank=True)
    quantity_28 = models.IntegerField(null=True, blank=True)
    quantity_30 = models.IntegerField(null=True, blank=True)
    quantity_32 = models.IntegerField(null=True, blank=True)
    quantity_34 = models.IntegerField(null=True, blank=True)
    quantity_36 = models.IntegerField(null=True, blank=True)
    quantity_38 = models.IntegerField(null=True, blank=True)
    quantity_40 = models.IntegerField(null=True, blank=True)
    quantity_42 = models.IntegerField(null=True, blank=True)
    quantity_44 = models.IntegerField(null=True, blank=True)
    quantity_46 = models.IntegerField(null=True, blank=True)
    quantity_48 = models.IntegerField(null=True, blank=True)
    quantity_50 = models.IntegerField(null=True, blank=True)
    quantity_52 = models.IntegerField(null=True, blank=True)
    fully_filled = models.BooleanField(default=True)
    total_quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=Carton_Status, null=True, blank=True)
    packing_count = models.IntegerField(default=0)
    quantity_24_count = models.IntegerField(default=0)
    quantity_26_count = models.IntegerField(default=0)
    quantity_28_count = models.IntegerField(default=0)
    quantity_30_count = models.IntegerField(default=0)
    quantity_32_count = models.IntegerField(default=0)
    quantity_34_count = models.IntegerField(default=0)
    quantity_36_count = models.IntegerField(default=0)
    quantity_38_count = models.IntegerField(default=0)
    quantity_40_count = models.IntegerField(default=0)
    quantity_42_count = models.IntegerField(default=0)
    quantity_44_count = models.IntegerField(default=0)
    quantity_46_count = models.IntegerField(default=0)
    quantity_48_count = models.IntegerField(default=0)
    quantity_50_count = models.IntegerField(default=0)
    quantity_52_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def get_Colors(self):
        color_vs_map = {}
        for i in self.map_for_color.all():
            try:
                a = color_vs_map[i.quantity_key.color.name]
                color_vs_map[i.quantity_key.color.name] = a + i.quantity
            except:
                color_vs_map[i.quantity_key.color.name] = i.quantity
        return color_vs_map

    class Meta:
        verbose_name = "Carton List"
        verbose_name_plural = "Carton List"


class size_status(models.Model):
    status = models.ForeignKey(order_status, on_delete=models.CASCADE)
    carton = models.ForeignKey(cartons_list, on_delete=models.CASCADE)
    size = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.size)

    class Meta:
        verbose_name = "Size Status"
        verbose_name_plural = "Size Status"


class carton(models.Model):
    # product_Category=models.ForeignKey(cate,on_delete=models.CASCADE,null=True)
    # product_Subcategory = ChainedForeignKey(
    #     sub_category,
    #     chained_field="product_Category",
    #     # chained_model_field="product_Category",
    #     show_all=False,
    #     auto_choose=True,
    #     sort=False,
    # 	null=True)
    # product_Supercategory= ChainedForeignKey(
    # 	super_category,
    # 	chained_field="product_Subcategory",
    # 	# chained_model_field="product_Subcategory",
    # 	show_all=False,
    # 	auto_choose=True,
    # 	sort=False,null=True)
    product_Category = models.ForeignKey(cate, on_delete=models.CASCADE, null=True, blank=True)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
    maximum_quantity = models.IntegerField(default=40)
    length = models.IntegerField(default=0)
    breadth = models.IntegerField(default=0)
    heigth = models.IntegerField(default=0)

    def __str__(self):
        return str(self.maximum_quantity)

    class Meta:
        verbose_name = "Carton"
        verbose_name_plural = "Carton"


class packing_list(models.Model):
    name = models.CharField(max_length=255)
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    cartons = models.ManyToManyField(cartons_list)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Packing List"
        verbose_name_plural = "Packing List"


class distribution_list(models.Model):
    name = models.CharField(max_length=255)
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    address = models.ForeignKey(address_model, on_delete=models.CASCADE)
    quantity_24 = models.IntegerField(default=0)
    quantity_26 = models.IntegerField(default=0)
    quantity_28 = models.IntegerField(default=0)
    quantity_30 = models.IntegerField(default=0)
    quantity_32 = models.IntegerField(default=0)
    quantity_34 = models.IntegerField(default=0)
    quantity_36 = models.IntegerField(default=0)
    quantity_38 = models.IntegerField(default=0)
    quantity_40 = models.IntegerField(default=0)
    quantity_42 = models.IntegerField(default=0)
    quantity_44 = models.IntegerField(default=0)
    quantity_46 = models.IntegerField(default=0)
    quantity_48 = models.IntegerField(default=0)
    quantity_50 = models.IntegerField(default=0)
    quantity_52 = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Distribution List"
        verbose_name_plural = "Distribution List"

    @property
    def total_quantity(self):
        total_quan = self.quantity_24
        total_quan += self.quantity_26
        total_quan += self.quantity_28
        total_quan += self.quantity_30
        total_quan += self.quantity_32
        total_quan += self.quantity_34
        total_quan += self.quantity_36
        total_quan += self.quantity_38
        total_quan += self.quantity_40
        total_quan += self.quantity_42
        total_quan += self.quantity_44
        total_quan += self.quantity_46
        total_quan += self.quantity_48
        total_quan += self.quantity_50
        total_quan += self.quantity_52
        return total_quan

    @property
    def left_over_quantity(self):
        return self.order.quantity - self.total_quantity


from POM.models import POM


class quality_deflection(models.Model):
    pom = models.ForeignKey(POM, on_delete=models.CASCADE)
    deflection = models.FloatField(default=0)
    remark = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.deflection)

    class Meta:
        verbose_name = "Quality Deflection"
        verbose_name_plural = "Quality Deflection"


class quality_evaluation(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    remark = models.TextField(blank=True, null=True)
    poms = models.ManyToManyField(quality_deflection, blank=True)
    label = models.IntegerField(null=True, blank=True)
    by_quality = models.BooleanField(default=False)
    by_factory = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = "Quality Evaluation"
        verbose_name_plural = "Quality Evaluation"


class esclation_home(models.Model):
    active = models.BooleanField(default=False)
    last_check = models.DateTimeField()

    class Meta:
        verbose_name = "Esclation Home"
        verbose_name_plural = "Esclation Home"


class coloums(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    coloumn_no = models.IntegerField(null=True, blank=True)
    coloum_name = models.CharField(max_length=255)
    email = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)
    reg_no = models.BooleanField(default=False)
    gender = models.BooleanField(default=False)
    dept = models.BooleanField(default=False)
    sub_dept = models.BooleanField(default=False)
    name = models.BooleanField(default=False)

    def __str__(self):
        return self.coloum_name

    class Meta:
        verbose_name = "Coloums"
        verbose_name_plural = "Coloums"


class excel(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    coloums = models.ManyToManyField(coloums, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Excel"
        verbose_name_plural = "Excel"


class mom_model(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE, null=True, blank=True)
    acti = models.ForeignKey(activities, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class location_wise_cost(models.Model):
    max_location_in_km = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return str(self.max_location_in_km)

    class Meta:
        verbose_name = "Location wise Cost"
        verbose_name_plural = "Location wise Cost"


class costing(models.Model):
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE)
    sampling_cost = models.FloatField()
    overhead_cost = models.FloatField()
    management_cost = models.FloatField()

    def __str__(self):
        return str(self.product_Category)

    class Meta:
        verbose_name = "Costing"
        verbose_name_plural = "Costing"


class budget_years(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = "Budget Year"


class budget_month(models.Model):
    month = models.IntegerField()
    month_label = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.month)

    class Meta:
        verbose_name = "Budget Month"


class budget_sectors(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    sector_weight = models.IntegerField(null=True, blank=True)
    total_weights = models.IntegerField(null=True, blank=True)
    weight_percent = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Budget Sector"
        verbose_name_plural = "Budget Sectors"


class sector_month_weight(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    sector = models.ForeignKey(budget_sectors, on_delete=models.CASCADE)
    year = models.ForeignKey(budget_years, on_delete=models.CASCADE)
    month = models.ForeignKey(budget_month, on_delete=models.CASCADE)
    weight = models.IntegerField()
    total_weight = models.IntegerField()
    weight_percent = models.IntegerField()

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = "Sector Month Weight"


class sector_run_rate(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    sector = models.ForeignKey(budget_sectors, on_delete=models.CASCADE)
    sector_weight = models.IntegerField()
    month1 = models.IntegerField(null=True, blank=True)
    w_month1 = models.IntegerField(null=True, blank=True)
    month2 = models.IntegerField(null=True, blank=True)
    w_month2 = models.IntegerField(null=True, blank=True)
    month3 = models.IntegerField(null=True, blank=True)
    w_month3 = models.IntegerField(null=True, blank=True)
    month4 = models.IntegerField(null=True, blank=True)
    w_month4 = models.IntegerField(null=True, blank=True)
    month5 = models.IntegerField(null=True, blank=True)
    w_month5 = models.IntegerField(null=True, blank=True)
    month6 = models.IntegerField(null=True, blank=True)
    w_month6 = models.IntegerField(null=True, blank=True)
    month7 = models.IntegerField(null=True, blank=True)
    w_month7 = models.IntegerField(null=True, blank=True)
    month8 = models.IntegerField(null=True, blank=True)
    w_month8 = models.IntegerField(null=True, blank=True)
    month9 = models.IntegerField(null=True, blank=True)
    w_month9 = models.IntegerField(null=True, blank=True)
    month10 = models.IntegerField(null=True, blank=True)
    w_month10 = models.IntegerField(null=True, blank=True)
    month11 = models.IntegerField(null=True, blank=True)
    w_month11 = models.IntegerField(null=True, blank=True)
    month12 = models.IntegerField(null=True, blank=True)
    w_month12 = models.IntegerField(null=True, blank=True)


class custom_assortment_model(models.Model):
    order = models.ForeignKey(company_Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Custom Assortment"


class budget_model(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    year = models.ForeignKey(budget_years, on_delete=models.CASCADE)
    yearly_amount = models.BigIntegerField()
    yearly_amount1 = models.BigIntegerField()

    class Meta:
        verbose_name = "Budget Model"


class budget_model_sector(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    year = models.ForeignKey(budget_years, on_delete=models.CASCADE)
    month = models.ForeignKey(budget_month, on_delete=models.CASCADE)
    sector = models.ForeignKey(budget_sectors, on_delete=models.CASCADE)
    target = models.IntegerField(null=True, blank=True)
    achieved = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Budget Model Sector"


class bulk_order_upload(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE, blank=True, null=True)
    order_no = models.CharField(max_length=255, null=True, blank=True)
    product_Category = models.CharField(max_length=255, null=True, blank=True)
    product_Subcategory = models.CharField(max_length=255, null=True, blank=True)
    product_Supercategory = models.CharField(max_length=255, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    fit = models.CharField(max_length=255, null=True, blank=True)
    season = models.CharField(max_length=255, null=True, blank=True)
    dispatch = models.CharField(max_length=255, null=True, blank=True)
    billing = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    target_lead = models.CharField(max_length=255, null=True, blank=True)
    target_price = models.CharField(max_length=255, null=True, blank=True)
    colors = models.CharField(max_length=255, null=True, blank=True)
    logo_placement = models.CharField(max_length=255, null=True, blank=True)
    max_quantity = models.CharField(max_length=255, null=True, blank=True)
    sales = models.CharField(max_length=255, null=True, blank=True)
    merchandiser = models.CharField(max_length=255, null=True, blank=True)
    garment_vendor = models.CharField(max_length=255, null=True, blank=True)
    other_fields = models.TextField(null=True, blank=True)
    excel = models.FileField(upload_to=upload_image_path)


class bulk_bom_upload(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to=upload_image_path, blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)

