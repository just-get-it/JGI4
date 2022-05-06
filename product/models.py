from django.db import models
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import IntegerRangeField

# Create your models here.

import random, os
from django.utils import timezone
import datetime
# from b2b.models import color_model


from userdetail.models import detail, seller_Categories
from django.contrib.postgres.fields import ArrayField


class PFM_Components(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PFM_Attributes(models.Model):
    pfm_component = models.ForeignKey(PFM_Components, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('pfm_component', 'name',)

    def __str__(self):
        return self.name


Fabric_choices = (
    ('woven', 'Woven'),
    ('knit', 'Knit'),
    ('others', 'Others')
)

Wash = (
    ('non-wash', 'Non-Wash'),
    ('wash', 'Wash'),
)

Style = (
    ('formal', 'Formal'),
    ('casual', 'Casual'),
)


class FabricDetails(models.Model):
    pfmno = models.CharField(max_length=100, primary_key=True)
    Fabric = models.CharField(max_length=100, default="0")
    WashType = models.CharField(max_length=100, default="0")
    category = models.CharField(max_length=200, null=True)
    subcategory = models.CharField(max_length=200, null=True)
    supercategory = models.CharField(max_length=200, null=True)
    StyleType = models.CharField(max_length=100, default="0")


class StyleDetails(models.Model):
    pfmno = models.CharField(max_length=100, primary_key=True)
    comp = models.CharField(max_length=200)
    attribute = models.CharField(max_length=200)
    operations = models.CharField(max_length=1000)
    complexity = models.IntegerField(default="1")
    spi = models.IntegerField(default="12")
    stitch_length = models.IntegerField(default="3")
    thread_consumption = models.DecimalField(max_digits=6, decimal_places=5)
    machine_auto = models.CharField(max_length=100, default="SNLS")
    work_aid = models.CharField(max_length=100, default="BINDER")
    smv = models.DecimalField(max_digits=6, default="0.33", decimal_places=5)
    allowance = models.DecimalField(max_digits=6, decimal_places=5)
    sam = models.DecimalField(max_digits=6, default="0.53", decimal_places=5)
    ct = models.DecimalField(max_digits=6, default="0.88", decimal_places=5)
    grade = models.CharField(max_length=100)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "local/product/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class category(models.Model):
    seller_cat = models.ManyToManyField(seller_Categories, blank=True)
    # seller_cat = models.ForeignKey(seller_Categories, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)

    show_on_homepage = models.BooleanField(default=True)
    image = models.FileField(upload_to=upload_image_path, default='local/product/2208226540442.jpeg')
    price_range = models.IntegerField(default=500)
    higher_price = models.IntegerField(default=500000)

    def __str__(self):
        return self.name


class sub_category(models.Model):
    seller_cat = models.ManyToManyField(seller_Categories, blank=True)
    # seller_cat = models.ForeignKey(seller_Categories, on_delete=models.CASCADE, blank=True, null=True)
    product_Category = models.ManyToManyField(category)
    name = models.CharField(max_length=255, unique=True)

    image = models.FileField(upload_to=upload_image_path, default='local/product/2208226540442.jpeg')

    # class Meta:
    #     unique_together = ('product_Category', 'name',)

    def __str__(self):
        return self.name

    def get_product_Category(self):
        categories = []
        for i in self.product_Category.all():
            categories.append(i)
        return categories

INPUT_CHOICES = [
    ("Text", "Text"),
    ("Drop Down", "Drop Down"),
    ("Date", "Date"),
]


class attribute(models.Model):
    seller_Categories = models.ManyToManyField(seller_Categories)
    name = models.CharField(max_length=255)
    #	seller_info=models.ForeignKey(seller_Categories,on_delete=models.CASCADE,blank=True,null=True)
    description = models.TextField(
        default="This would help users to know Product Easily - <br> -  This can only contain all types Charcater<br> -  This can also contain Special Characters")
    input_type = models.CharField(max_length=50, choices=INPUT_CHOICES, default="Text")
    values = models.TextField(blank=True)

    def __str__(self):
        return self.name


class bestoffer(models.Model):
    title = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class product_group_type(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class super_category(models.Model):
    seller_cat = models.ManyToManyField(seller_Categories, blank=True)
    # seller_cat = models.ForeignKey(seller_Categories, on_delete=models.CASCADE, blank=True, null=True)
    product_Category = models.ManyToManyField(category)
    product_Subcategory = models.ManyToManyField(sub_category)
    # product_Subcategory = ChainedManyToManyField(
    #     sub_category,
    #     chained_field="product_Category",
    #     chained_model_field="product_Category"
    # )
    # product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, default=1)
    product_Category = models.ManyToManyField(category)
    product_Subcategory = ChainedManyToManyField(
        sub_category,
        chained_field="product_Category",
        chained_model_field="product_Category"
    )
    name = models.CharField(max_length=255, unique=True)
    attributes = models.ManyToManyField(attribute)
    image = models.FileField(upload_to=upload_image_path, default='local/product/2208226540442.jpeg')
    Type = models.CharField(max_length=10)
    product_group = models.ForeignKey(product_group_type, on_delete=models.CASCADE, null=True, blank=True)
    service = models.NullBooleanField(null=True, blank=False, default=False)
    available_for_subscription = models.NullBooleanField(default=False)

    # class Meta:
    #     unique_together = ('product_Subcategory', 'name',)

    def __str__(self):
        return self.name


class product_cate_b2b(models.Model):
    name = models.CharField(max_length=255)
    show_on_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class labels_Object(models.Model):
    seller_Categories = models.ManyToManyField(seller_Categories)
    name = models.CharField(max_length=255)
    homepage_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class RandomManager(models.Manager):
    def get_query_set(self):
        return super(RandomManager, self).get_query_set().order_by('?')


from seller_info.models import labels, fits, seasons, washcares, barcodes

# from .models import labels_Object


Privacy_Choices = (
    ('private', 'Private'),
    ('consumers', 'Consumers'),
    ('staffs', 'Staffs'),
    ('merchant', 'Merchandiser'),
    ('public', 'Public')
)


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=10, default="")
    additional_items = models.CharField(max_length=300, default="")
    instructions = models.CharField(max_length=500, default="")
    payment_method = models.CharField(max_length=100, default="", null=True, blank=True)

    def __str__(self):
        return self.name


ORDER_STATUS = (
    ('packed', 'Packed'),
    ('shipped', 'Shipped'),
    ('deliverd', 'Deliverd')
)


class history(models.Model):
    ordertype = models.CharField(max_length=100)
    order_id = models.CharField(max_length=200)
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS, default="Packed")
    email = models.CharField(max_length=100, default="")
    date = models.DateField(auto_now=True)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.email

class TermAndCondition(models.Model):
	version = models.FloatField()
	subscriptionTerms = models.CharField(max_length=10000, default='')
    
class add_wallet(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, default="")
    amount = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class remove_wallet(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, default="")
    amount = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now=True)
    reciever = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.email

class option_tags(models.Model):
    name = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.name

class product(models.Model):
    product_code = models.CharField(max_length=50, blank=True, editable=False, primary_key=True)
    product_Category = models.ManyToManyField(category)
    product_total_reviews = models.IntegerField(blank=True, default=0)
    product_stars = models.FloatField(blank=True, default=5.0)
    product_Subcategory = ChainedManyToManyField(
        sub_category,
        chained_field="product_Category",
        chained_model_field="product_Category"
    )
    product_Supercategory = ChainedManyToManyField(
        super_category,
        chained_field="product_Subcategory",
        chained_model_field="product_Subcategory"
    )
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=1000, unique=True)
    notes = models.TextField()
    seller = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True, related_name='sellers')
    description = models.TextField()
    price = models.FloatField(default=0, blank=True, null=True)
    offer = models.FloatField(default=0, blank=True, null=True)
    B2Boffer = models.FloatField(default=0, blank=True, null=True)
    Moq_range1 = IntegerRangeField(blank=True, null=True)
    Moq_discount1 = models.FloatField(default=0, blank=True, null=True)
    Moq_range2 = IntegerRangeField(blank=True, null=True)
    Moq_discount2 = models.FloatField(default=0, blank=True, null=True)
    Moq_range3 = IntegerRangeField(blank=True, null=True)
    Moq_discount3 = models.FloatField(default=0, blank=True, null=True)
    privacy = models.CharField(max_length=255, choices=Privacy_Choices, null=True, blank=True)
    bestoffers = models.ManyToManyField(bestoffer, blank=True)
    product_cate = models.ManyToManyField(product_cate_b2b, blank=True)
    deal_of_day = models.IntegerField(default=0, blank=True, null=True)
    # b2b_product = models.BooleanField(default=False)
    # b2c_product = models.BooleanField(default=True)
    # sample_product = models.BooleanField(default=False)
    brand = models.CharField(max_length=255, null=True, blank=True)
    label = models.ForeignKey(labels, on_delete=models.CASCADE, null=True, blank=True)  # optional
    fit = models.ForeignKey(fits, on_delete=models.CASCADE, null=True, blank=True)  # fashion
    season = models.ForeignKey(seasons, on_delete=models.CASCADE, null=True, blank=True)  # Fashion
    washcare = models.ForeignKey(washcares, on_delete=models.CASCADE, null=True, blank=True)  # Fashion
    barcode = models.ForeignKey(barcodes, on_delete=models.CASCADE, null=True, blank=True)
    terms = models.TextField(null=True, blank=True)
    product_tags = models.ManyToManyField(labels_Object, blank=True)
    sold_quantity = models.IntegerField(default=0, blank=True, null=True)
    safe_stock = models.IntegerField(default=10, blank=True, null=True)
    trending_view = models.IntegerField(default=0, blank=True, null=True)
    last_trending = models.DateField(auto_now=True, blank=True, null=True)
    selling_unit = models.CharField(max_length=255, null=True, blank=True)
    image1 = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    ###############new atrris#############
    manufacturername = models.CharField(max_length=255, null=True, blank=True)
    manufacturerno = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    batteriesincluded = models.CharField(max_length=255, null=True, blank=True)
    batteriesno = models.CharField(max_length=255, null=True, blank=True)
    wattage = models.CharField(max_length=255, null=True, blank=True)
    dangerousgood = models.CharField(max_length=255, null=True, blank=True)
    shape = models.CharField(max_length=255, null=True, blank=True)
    length = models.CharField(max_length=255, null=True, blank=True)
    width = models.CharField(max_length=255, null=True, blank=True)
    height = models.CharField(max_length=255, null=True, blank=True)
    countryorigin = models.CharField(max_length=255, null=True, blank=True)
    pattern = models.CharField(max_length=255, null=True, blank=True)
    shafttype = models.CharField(max_length=255, null=True, blank=True)
    features = models.CharField(max_length=255, null=True, blank=True)
    style = models.CharField(max_length=255, null=True, blank=True)
    graphics = models.CharField(max_length=255, null=True, blank=True)
    powersource = models.CharField(max_length=255, null=True, blank=True)
    occasion = models.CharField(max_length=255, null=True, blank=True)
    noofitems = models.CharField(max_length=255, null=True, blank=True)
    sale = models.CharField(max_length=255, null=True, blank=True)
    salestartdate = models.CharField(max_length=255, null=True, blank=True)
    saleenddate = models.CharField(max_length=255, null=True, blank=True)
    salediscount = models.CharField(max_length=255, null=True, blank=True)
    allparts = models.CharField(max_length=255, null=True, blank=True)
    specifications = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    ##########################################ma
    atrribute29 = models.CharField(max_length=255, null=True, blank=True)
    atrribute30 = models.CharField(max_length=255, null=True, blank=True)
    atrribute31 = models.CharField(max_length=255, null=True, blank=True)
    atrribute32 = models.CharField(max_length=255, null=True, blank=True)
    atrribute33 = models.CharField(max_length=255, null=True, blank=True)
    atrribute34 = models.CharField(max_length=255, null=True, blank=True)
    atrribute35 = models.CharField(max_length=255, null=True, blank=True)
    atrribute36 = models.CharField(max_length=255, null=True, blank=True)
    atrribute37 = models.CharField(max_length=255, null=True, blank=True)
    atrribute38 = models.CharField(max_length=255, null=True, blank=True)
    atrribute39 = models.CharField(max_length=255, null=True, blank=True)
    atrribute40 = models.CharField(max_length=255, null=True, blank=True)
    atrribute41 = models.CharField(max_length=255, null=True, blank=True)
    atrribute42 = models.CharField(max_length=255, null=True, blank=True)
    atrribute43 = models.CharField(max_length=255, null=True, blank=True)
    atrribute44 = models.CharField(max_length=255, null=True, blank=True)
    atrribute45 = models.CharField(max_length=255, null=True, blank=True)
    atrribute46 = models.CharField(max_length=255, null=True, blank=True)
    atrribute47 = models.CharField(max_length=255, null=True, blank=True)
    atrribute48 = models.CharField(max_length=255, null=True, blank=True)
    atrribute49 = models.CharField(max_length=255, null=True, blank=True)
    atrribute50 = models.CharField(max_length=255, null=True, blank=True)
    atrribute51 = models.CharField(max_length=255, null=True, blank=True)
    atrribute52 = models.CharField(max_length=255, null=True, blank=True)
    atrribute53 = models.CharField(max_length=255, null=True, blank=True)
    atrribute54 = models.CharField(max_length=255, null=True, blank=True)
    atrribute55 = models.CharField(max_length=255, null=True, blank=True)
    atrribute56 = models.CharField(max_length=255, null=True, blank=True)
    atrribute57 = models.CharField(max_length=255, null=True, blank=True)
    atrribute58 = models.CharField(max_length=255, null=True, blank=True)
    atrribute59 = models.CharField(max_length=255, null=True, blank=True)
    atrribute60 = models.CharField(max_length=255, null=True, blank=True)
    atrribute61 = models.CharField(max_length=255, null=True, blank=True)
    atrribute62 = models.CharField(max_length=255, null=True, blank=True)
    atrribute63 = models.CharField(max_length=255, null=True, blank=True)
    atrribute64 = models.CharField(max_length=255, null=True, blank=True)
    atrribute65 = models.CharField(max_length=255, null=True, blank=True)
    atrribute66 = models.CharField(max_length=255, null=True, blank=True)
    atrribute67 = models.CharField(max_length=255, null=True, blank=True)
    atrribute68 = models.CharField(max_length=255, null=True, blank=True)
    atrribute69 = models.CharField(max_length=255, null=True, blank=True)
    atrribute70 = models.CharField(max_length=255, null=True, blank=True)
    atrribute71 = models.CharField(max_length=255, null=True, blank=True)
    atrribute72 = models.CharField(max_length=255, null=True, blank=True)
    atrribute73 = models.CharField(max_length=255, null=True, blank=True)
    atrribute74 = models.CharField(max_length=255, null=True, blank=True)
    atrribute75 = models.CharField(max_length=255, null=True, blank=True)
    atrribute76 = models.CharField(max_length=255, null=True, blank=True)
    atrribute77 = models.CharField(max_length=255, null=True, blank=True)
    atrribute78 = models.CharField(max_length=255, null=True, blank=True)
    atrribute79 = models.CharField(max_length=255, null=True, blank=True)
    atrribute80 = models.CharField(max_length=255, null=True, blank=True)
    atrribute81 = models.CharField(max_length=255, null=True, blank=True)
    atrribute82 = models.CharField(max_length=255, null=True, blank=True)
    atrribute83 = models.CharField(max_length=255, null=True, blank=True)
    atrribute84 = models.CharField(max_length=255, null=True, blank=True)
    atrribute85 = models.CharField(max_length=255, null=True, blank=True)
    atrribute86 = models.CharField(max_length=255, null=True, blank=True)
    atrribute87 = models.CharField(max_length=255, null=True, blank=True)
    atrribute88 = models.CharField(max_length=255, null=True, blank=True)
    atrribute89 = models.CharField(max_length=255, null=True, blank=True)
    atrribute90 = models.CharField(max_length=255, null=True, blank=True)
    atrribute91 = models.CharField(max_length=255, null=True, blank=True)
    atrribute92 = models.CharField(max_length=255, null=True, blank=True)
    atrribute93 = models.CharField(max_length=255, null=True, blank=True)
    atrribute94 = models.CharField(max_length=255, null=True, blank=True)
    atrribute95 = models.CharField(max_length=255, null=True, blank=True)
    atrribute96 = models.CharField(max_length=255, null=True, blank=True)
    atrribute97 = models.CharField(max_length=255, null=True, blank=True)
    atrribute98 = models.CharField(max_length=255, null=True, blank=True)
    atrribute99 = models.CharField(max_length=255, null=True, blank=True)
    atrribute100 = models.CharField(max_length=255, null=True, blank=True)

    made_in = models.CharField(max_length=255, null=True, blank=True)
    old_product = models.NullBooleanField(default=False)
    product_group = models.ManyToManyField(product_group_type)
    
    # MY_CHOICES = (('1', 'Item title 1.1'),
    #           ('2', 'Item title 1.2'),
    #           ('3', 'Item title 1.3'),
    # )
    options = models.ManyToManyField(option_tags, blank=True)
    grade_quality = models.TextField(blank=True, max_length=25)
    packed = models.NullBooleanField(default=False)
    Service = models.NullBooleanField(default=False)
    UNITS_OF_MEASUREMENT = (
					('K', 'kg'),
					('L', 'litre'),
					('P', 'pieces')
	)
    unit_of_measurement = models.CharField(max_length=1, choices=UNITS_OF_MEASUREMENT, default='P')
    period_to_change = models.IntegerField(default=2)
    available_for_subscription=models.NullBooleanField(default=False)
    subscription_discount = models.FloatField(default=5)
    is_rent = models.BooleanField(default=False)
    gst = models.DecimalField(default=5, max_digits=4, decimal_places=2)

    objects = models.Manager()

    # randoms=RandomManager()

    @property
    def final_price(self):
        f_price = self.price - (self.price * self.offer // 100)
        return f_price
        
    def final_b2b_price(self):
        f_price = self.price - (self.price * self.B2Boffer // 100)
        return f_price

    def get_moq1_price(self):
        f_price = self.price - (self.price * self.Moq_discount1 // 100)
        return f_price

    def get_moq2_price(self):
        f_price = self.price - (self.price * self.Moq_discount2 // 100)
        return f_price

    def get_moq3_price(self):
        f_price = self.price - (self.price * self.Moq_discount3 // 100)
        return f_price

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.product_code:
            self.product_code = str(self.product_Category)[:2] + str(self.product_Subcategory)[:2] + str(
                self.product_Supercategory)[:2] + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        super(product, self).save(*args, **kwargs)
    
    def get_categories(self):
        categories = []
        for i in self.product_Category.all():
            categories.append(str(i))
        return categories

    def get_options(self):
        options = []
        for i in self.options.all():
            options.append(i)
        return options

class units(models.Model):
    seller = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True)
    supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE)
    unit = models.CharField(max_length=200)


class service_add(models.Model):
    seller = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True)
    supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE)
    price_range = models.CharField(max_length=200)


class recently_viewed(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.user)


class labels_Attributes(models.Model):
    seller_Categories = models.ManyToManyField(seller_Categories)
    label = ChainedManyToManyField(
        labels_Object,
        chained_field='seller_Categories',
        chained_model_field='seller_Categories',
    )
    # product_Category=models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True)
    # product_Subcategory=models.ForeignKey(sub_category,on_delete=models.CASCADE,null=True,blank=True)
    # product_Supercategory=models.ForeignKey(super_category,on_delete=models.CASCADE,null=True,blank=True)
    # labels_Object=models.ManyToManyField(labels_Object,blank=True)
    category = models.ManyToManyField(category, blank=True)
    sub_category = models.ManyToManyField(sub_category, blank=True)
    super_category = models.ManyToManyField(super_category, blank=True)
    name = models.CharField(max_length=255)
    input_type = models.CharField(max_length=50, choices=INPUT_CHOICES, default="Text")
    values = models.TextField(blank=True)
    component_fabric_consumption = models.TextField(blank=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class label_dropdowns(models.Model):
    attribute = models.ForeignKey(labels_Attributes, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return self.attribute_value


class label_Attributes_Values(models.Model):
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    label_attribute = models.ForeignKey(labels_Attributes, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class product_common_attribute_values(models.Model):
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)


class size_color_quantity(models.Model):
    linked_product = models.ForeignKey(product, on_delete=models.CASCADE)
    size = models.IntegerField(default=1, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    c_price = models.IntegerField(default=100, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    safety_stock_limit = models.IntegerField(default=0, null=True, blank=True)
    owned_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.linked_product.title+" "+str(self.size)+" "+str(self.color)
    def final_price(self):
        return self.price -  (self.price * self.linked_product.offer // 100)
    

class trims_Attribute(models.Model):
    name = models.CharField(max_length=255)
    seller_info = models.ForeignKey(seller_Categories, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class trims_label_attributes(models.Model):
    name = models.CharField(max_length=255)
    seller_info = models.ForeignKey(seller_Categories, on_delete=models.CASCADE, blank=True, null=True)
    input_type = models.CharField(max_length=50, choices=INPUT_CHOICES, default="Drop Down")
    values = models.TextField(blank=True)
    impact_fabric_consumption = models.TextField(blank=True)
    shrinkage_percent = models.IntegerField(blank=True, null=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class fabric_direction(models.Model):
    name = models.CharField(max_length=255)
    impact_fabric_consumption = models.IntegerField(blank=True)
    shrinkage_percent = models.IntegerField(blank=True, null=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class fabric_width(models.Model):
    name = models.CharField(max_length=255)
    impact_fabric_consumption = models.IntegerField(blank=True)
    shrinkage_percent = models.IntegerField(blank=True, null=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class fabric_print_design(models.Model):
    name = models.CharField(max_length=255)
    impact_fabric_consumption = models.IntegerField(blank=True)
    shrinkage_percent = models.IntegerField(blank=True, null=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class fabric_print_type(models.Model):
    name = models.CharField(max_length=255)
    impact_fabric_consumption = models.IntegerField(blank=True)
    shrinkage_percent = models.IntegerField(blank=True, null=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class trims_Category(models.Model):
    name = models.CharField(max_length=255)
    attributes = models.ManyToManyField(trims_Attribute)
    trims_label_attributes = models.ManyToManyField(trims_label_attributes)
    fabric = models.BooleanField(default=False)
    packing = models.BooleanField(default=False)
    sewing = models.BooleanField(default=False)
    finishing = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class trims_product(models.Model):
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
    standard = models.BooleanField(default=False)
    category = models.ForeignKey(trims_Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    notes = models.TextField()
    seller = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True)
    comments = models.TextField()
    image1 = models.FileField(upload_to=upload_image_path)
    image2 = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    image3 = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    image4 = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    image5 = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    price = models.IntegerField()
    offer = models.IntegerField(default=0)
    B2Boffer = models.IntegerField(default=0)
    bestoffers = models.ManyToManyField(bestoffer)
    atrribute1 = models.CharField(max_length=255, null=True, blank=True)
    atrribute2 = models.CharField(max_length=255, null=True, blank=True)
    atrribute3 = models.CharField(max_length=255, null=True, blank=True)
    atrribute4 = models.CharField(max_length=255, null=True, blank=True)
    atrribute5 = models.CharField(max_length=255, null=True, blank=True)
    atrribute6 = models.CharField(max_length=255, null=True, blank=True)
    atrribute7 = models.CharField(max_length=255, null=True, blank=True)
    atrribute8 = models.CharField(max_length=255, null=True, blank=True)
    atrribute9 = models.CharField(max_length=255, null=True, blank=True)
    atrribute10 = models.CharField(max_length=255, null=True, blank=True)
    atrribute11 = models.CharField(max_length=255, null=True, blank=True)
    atrribute12 = models.CharField(max_length=255, null=True, blank=True)
    atrribute13 = models.CharField(max_length=255, null=True, blank=True)
    atrribute14 = models.CharField(max_length=255, null=True, blank=True)
    atrribute15 = models.CharField(max_length=255, null=True, blank=True)
    atrribute16 = models.CharField(max_length=255, null=True, blank=True)
    atrribute17 = models.CharField(max_length=255, null=True, blank=True)
    atrribute18 = models.CharField(max_length=255, null=True, blank=True)
    atrribute19 = models.CharField(max_length=255, null=True, blank=True)
    atrribute20 = models.CharField(max_length=255, null=True, blank=True)
    atrribute21 = models.CharField(max_length=255, null=True, blank=True)
    atrribute22 = models.CharField(max_length=255, null=True, blank=True)
    atrribute23 = models.CharField(max_length=255, null=True, blank=True)
    atrribute24 = models.CharField(max_length=255, null=True, blank=True)
    atrribute25 = models.CharField(max_length=255, null=True, blank=True)
    atrribute26 = models.CharField(max_length=255, null=True, blank=True)
    atrribute27 = models.CharField(max_length=255, null=True, blank=True)
    atrribute28 = models.CharField(max_length=255, null=True, blank=True)
    atrribute29 = models.CharField(max_length=255, null=True, blank=True)
    atrribute30 = models.CharField(max_length=255, null=True, blank=True)
    fabric_direction = models.ForeignKey(fabric_direction, on_delete=models.CASCADE, null=True, blank=True)
    fabric_width = models.ForeignKey(fabric_width, on_delete=models.CASCADE, null=True, blank=True)
    fabric_print_type = models.ForeignKey(fabric_print_type, on_delete=models.CASCADE, null=True, blank=True)
    fabric_print_design = models.ForeignKey(fabric_print_design, on_delete=models.CASCADE, null=True, blank=True)
    trims_labels = ArrayField(models.CharField(max_length=255, blank=True, null=True), size=100, blank=True, null=True)

    def __str__(self):
        return "fab_" + str(datetime.datetime.now().date().year) + "0000" + str(self.id)


class trims_product_quantity(models.Model):
    to_product = models.ForeignKey(trims_product, on_delete=models.CASCADE)
    seller = models.ForeignKey(detail, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.seller)


class product_requests(models.Model):
    to_product = models.ForeignKey(product, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    delivery = models.TextField(null=True, blank=True)
    to_user = models.ForeignKey(detail, on_delete=models.CASCADE)
    size = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)
    from_user = models.ForeignKey(detail, on_delete=models.CASCADE, related_name="from_user", null=True, blank=True)


class htm(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_Subcategory = ChainedForeignKey(
        sub_category,
        chained_field="product_Category",
        chained_model_field="product_Category",
        show_all=False,
        auto_choose=True,
        sort=False)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_image_path)


class safety_stock(models.Model):
    vendor = models.ForeignKey(detail, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE)
    limit = models.IntegerField()


class standard_fabric_blend(models.Model):
    name = models.CharField(max_length=255)
    standard = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Standard Fabric Blend"
        verbose_name_plural = "Standard Fabric Blends"


class care_symbols(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to=upload_image_path)
    standard = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Care Symbol"


class washcare_model(models.Model):
    blend = models.ForeignKey(standard_fabric_blend, on_delete=models.CASCADE)
    care_icons = models.ManyToManyField(care_symbols, blank=True)
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE)
    width = models.IntegerField(default=250)
    height = models.IntegerField(default=450)
    margin_top = models.IntegerField(default=10)
    margin_bottom = models.IntegerField(default=10)
    heading = models.BooleanField(default=True)
    top_heads = models.TextField(blank=True, null=True)
    bottom_heads = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.blend)

    class Meta:
        verbose_name = "Washcare"


class MachineType(models.Model):
    machine_name = models.CharField(max_length=255)
    thread_consumption_factor = models.CharField(max_length=255)

    def __str__(self):
        return str(self.machine_name)


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('department', 'name',)

    def __str__(self):
        return self.name


class subsection(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = ChainedForeignKey(
        Section,
        chained_field="department",
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=False)

    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('section', 'name',)

    def __str__(self):
        return self.name


class StyleType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Fabric(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class WashType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class garment_consumption_formula(models.Model):
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
    components = models.ForeignKey(labels_Attributes, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    pom1 = models.CharField(max_length=255, null=True, blank=True)
    pom2 = models.CharField(max_length=255, null=True, blank=True)
    pom3 = models.CharField(max_length=255, null=True, blank=True)
    pom4 = models.CharField(max_length=255, null=True, blank=True)
    allowance1 = models.CharField(max_length=255, null=True, blank=True)
    allowance2 = models.CharField(max_length=255, null=True, blank=True)
    allowance3 = models.CharField(max_length=255, null=True, blank=True)
    allowance4 = models.CharField(max_length=255, null=True, blank=True)
    formula = models.CharField(max_length=255, null=True, blank=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class garment_matching_parameters(models.Model):
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    input_type = models.CharField(max_length=50, choices=INPUT_CHOICES, default="Text")
    values = models.TextField(blank=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class garment_matching_requirements(models.Model):
    product_Category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    product_Subcategory = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    product_Supercategory = models.ForeignKey(super_category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    garment_matching_parameters = models.ForeignKey(garment_matching_parameters, on_delete=models.CASCADE, null=True,
                                                    blank=True)
    no_matching = models.TextField(blank=True)
    level1 = models.TextField(blank=True)
    level2 = models.TextField(blank=True)
    level3 = models.TextField(blank=True)
    fabric_consumption_level1 = models.IntegerField(blank=True)
    fabric_consumption_level2 = models.IntegerField(blank=True)
    fabric_consumption_level3 = models.IntegerField(blank=True)
    is_component = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class repeat_size(models.Model):
    fabric_direction = models.ForeignKey(fabric_direction, on_delete=models.CASCADE, blank=True, null=True)
    fabric_print_design = models.ForeignKey(fabric_print_design, on_delete=models.CASCADE, blank=True, null=True)
    fabric_width = models.ForeignKey(fabric_width, on_delete=models.CASCADE, blank=True, null=True)
    fabric_print_type = models.ForeignKey(fabric_print_type, on_delete=models.CASCADE, blank=True, null=True)
    garment_matching_parameters = models.ForeignKey(garment_matching_parameters, on_delete=models.CASCADE)
    LEVELS = (('no_matching', 'no matching'),
              ('level1', 'level1'),
              ('level2', 'level2'),
              ('level3', 'level3'))
    garment_matching_level = models.CharField(max_length=50, choices=LEVELS, default="", blank=True, null=True)
    horizontal_repeat_range = models.TextField(blank=True, null=True)
    vertical_repeat_range = models.TextField(blank=True, null=True)
    increase_in_marker_cons = models.TextField(blank=True, null=True)


class developer_attributes(models.Model):
    product_group_type = models.ManyToManyField(product_group_type, blank=True)
    detail = models.ManyToManyField(detail, blank=True)
    attributes = models.CharField(max_length=100)
    input_type = models.CharField(max_length=50, choices=INPUT_CHOICES, default="Text")
    values = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.attributes


class all_units(models.Model):
    unit = models.CharField(max_length=100)
    seller_Categories = models.ManyToManyField(seller_Categories, blank=True)
    detail = models.ManyToManyField(detail, blank=True)

    def __str__(self):
        return self.unit


class extradetails(models.Model):
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    attribute1 = models.CharField(max_length=100, blank=True, null=True)
    value1 = models.CharField(max_length=100, blank=True, null=True)
    attribute2 = models.CharField(max_length=100, blank=True, null=True)
    value2 = models.CharField(max_length=100, blank=True, null=True)
    attribute3 = models.CharField(max_length=100, blank=True, null=True)
    value3 = models.CharField(max_length=100, blank=True, null=True)
    attribute4 = models.CharField(max_length=100, blank=True, null=True)
    value4 = models.CharField(max_length=100, blank=True, null=True)
    attribute5 = models.CharField(max_length=100, blank=True, null=True)
    value5 = models.CharField(max_length=100, blank=True, null=True)
    attribute6 = models.CharField(max_length=100, blank=True, null=True)
    value6 = models.CharField(max_length=100, blank=True, null=True)
    attribute7 = models.CharField(max_length=100, blank=True, null=True)
    value7 = models.CharField(max_length=100, blank=True, null=True)
    attribute8 = models.CharField(max_length=100, blank=True, null=True)
    value8 = models.CharField(max_length=100, blank=True, null=True)
    attribute9 = models.CharField(max_length=100, blank=True, null=True)
    value9 = models.CharField(max_length=100, blank=True, null=True)
    attribute10 = models.CharField(max_length=100, blank=True, null=True)
    value10 = models.CharField(max_length=100, blank=True, null=True)
    attribute11 = models.CharField(max_length=100, blank=True, null=True)
    value11 = models.CharField(max_length=100, blank=True, null=True)
    attribute12 = models.CharField(max_length=100, blank=True, null=True)
    value12 = models.CharField(max_length=100, blank=True, null=True)
    attribute13 = models.CharField(max_length=100, blank=True, null=True)
    value13 = models.CharField(max_length=100, blank=True, null=True)
    attribute14 = models.CharField(max_length=100, blank=True, null=True)
    value14 = models.CharField(max_length=100, blank=True, null=True)
    attribute15 = models.CharField(max_length=100, blank=True, null=True)
    value15 = models.CharField(max_length=100, blank=True, null=True)
    attribute16 = models.CharField(max_length=100, blank=True, null=True)
    value16 = models.CharField(max_length=100, blank=True, null=True)
    attribute17 = models.CharField(max_length=100, blank=True, null=True)
    value17 = models.CharField(max_length=100, blank=True, null=True)
    attribute18 = models.CharField(max_length=100, blank=True, null=True)
    value18 = models.CharField(max_length=100, blank=True, null=True)
    attribute19 = models.CharField(max_length=100, blank=True, null=True)
    value19 = models.CharField(max_length=100, blank=True, null=True)
    attribute20 = models.CharField(max_length=100, blank=True, null=True)
    value20 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.attribute1


class Add_images(models.Model):
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    image = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    size = models.ForeignKey(size_color_quantity, null=True, blank=True, on_delete=models.CASCADE)
    is_actual = models.BooleanField(default=False)
    def __str__(self):
        return self.prod.title


class FormAttributes(models.Model):
    seller_Categories = models.ManyToManyField(seller_Categories, blank=True)
    detail = models.ManyToManyField(detail, blank=True)
    category = models.ManyToManyField(category, blank=True)
    sub_category = models.ManyToManyField(sub_category, blank=True)
    super_category = models.ManyToManyField(super_category, blank=True)
    pieces_per_unit = models.BooleanField(default=True)
    color_exits = models.BooleanField(default=True)
    sizes_exist = models.BooleanField(default=True)
    prices_exist = models.BooleanField(default=True)
    offer = models.BooleanField(default=True)
    B2Boffer = models.BooleanField(default=True)
    stock_info_exists = models.BooleanField(default=True)
    brand = models.BooleanField(default=True)
    otherbrand = models.BooleanField(default=True)
    label = models.BooleanField(default=True)
    images = models.BooleanField(default=True)
    variations = models.BooleanField(default=True)
    commoninfo = models.BooleanField(default=True)
    compliance = models.BooleanField(default=True)
    Description = models.BooleanField(default=True)
    vitalinfo = models.BooleanField(default=True)
    washcare = models.BooleanField(default=True)
    fit = models.BooleanField(default=True)
    season = models.BooleanField(default=True)
    services = models.BooleanField(default=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class OtherBrands(models.Model):
    brand = models.CharField(max_length=255, blank=True, null=True)
    seller_Categories = models.ManyToManyField(seller_Categories, blank=True)
    category = models.ManyToManyField(category, blank=True)
    sub_category = models.ManyToManyField(sub_category, blank=True)
    super_category = models.ManyToManyField(super_category, blank=True)

    def __str__(self):
        return self.brand


class OtherLabel(models.Model):
    OtherBrands = models.ManyToManyField(OtherBrands, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)

def upload_review_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "local/review/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class ProductReview(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    review_image = models.FileField(upload_to=upload_review_image_path, blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
