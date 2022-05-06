from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
from django.urls import reverse

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from product.models import standard_fabric_blend
import random

class Plan(models.Model):
    name=models.CharField(default='Plan ',unique=True,max_length=15)
    from_quantity=models.IntegerField(default=1,
                                        validators=[
                                            MinValueValidator(1),
                                            MaxValueValidator(10000)
                                            ])
    to_quantity = models.IntegerField(default=1,
                                        validators=[
                                            MinValueValidator(20),
                                            MaxValueValidator(50000)
                                        ])
    slug = models.SlugField(blank=True, null=True)
    # costing_rates=models.
    def __str__(self):
        return f'{self.name} {self.pk}'


GARMENT_CHOICE=(
    ('T-Shirts','T-Shirts'),
    ('Shirts','Shirts'),
    ('Trouser','Trouser'),
    ('Blazer','Blazer'),
    ('Jeans','Jeans'),
)

class Garment(models.Model):
    name=models.CharField(choices=GARMENT_CHOICE,unique=True,max_length=20)
    def __str__(self):
        return self.name

FABRIC_CHOICE=(
    ('Canvas','Canvas'),
    ('Rayon','Rayon'),
    ('Poly-Rayon','Poly-Rayon'),
    ('Poplin','Poplin'),
    ('Matte','Matte'),
    ('Twill','Twill'),
    ('Chenille','Chenille'),
    ('Jersey Fabric','Jersey Fabric'),
    ('Poly-Twill','Poly-Twill'),
    ('Corduroy','Corduroy'),
    ('Velvet','Velvet'),
    ('Satin','Satin'),

    ('100% Cotton','100% Cotton'),
    ('Linen','Linen'),
    ('CP- 65/35','CP- 65/35'),
    ('CP- 70/30','CP- 70/30'),
    ('Filafil','Filafil'),
    ('Funnel Fabric','Funnel Fabric'),
    ('Silk','Silk'),
    ('Satin','Satin'),
    ('Cotton Linen','Cotton Linen'),
    ('Denim','Denim'),
    ('Organza','Organza'),
    ('Twil Fabric','Twil Fabric'),
    ('chambray','chambray'),
    ('Honeycomb','Honeycomb'),
    ('Poplin','Poplin'),
    ('Flannel','Flannel'),
)

# class Fabric(models.Model):
#     type = models.CharField(choices=FABRIC_CHOICE, unique=True,max_length=20,blank=True,null=True)
#     # fabric_details = models.OneToOneField(standard_fabric_blend, unique=True,on_delete=models.CASCADE,blank=True,null=True)
#     garment=models.ForeignKey(Garment,on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.type

class Fabric(models.Model):
    # type = models.CharField(choices=FABRIC_CHOICE, unique=True,max_length=20,blank=True,null=True)
    name = models.OneToOneField(standard_fabric_blend, unique=True,on_delete=models.CASCADE,blank=True,null=True)
    garment=models.ForeignKey(Garment,on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name



SIZE_CHOICE=(
    ('Small','Small'),
    ('Medium','Medium'),
    ('Large','Large'),
    ('XL','XL'),
    ('XXL','XXL'),
)



class Measurments(models.Model):
    # type=models.CharField(choices=SIZE_CHOICE,max_length=20)
    order  =   models.OneToOneField('Order',on_delete=models.CASCADE,blank=True,null=True)

    small  =   models.IntegerField(default=0,validators=[ MinValueValidator(0),MaxValueValidator(50000) ])
    medium =   models.IntegerField(default=0,validators=[ MinValueValidator(0),MaxValueValidator(50000) ])
    large  =   models.IntegerField(default=0,validators=[ MinValueValidator(0),MaxValueValidator(50000) ])
    xl     =   models.IntegerField(default=0,validators=[ MinValueValidator(0),MaxValueValidator(50000) ])
    xxl    =   models.IntegerField(default=0,validators=[ MinValueValidator(0),MaxValueValidator(50000) ])

    def __str__(self):
        return f'{self.small} - {self.medium} - {self.large} - {self.xl} - {self.xxl}'

    def get_total_quantity(self):
        return int(self.small + self.medium + self.large + self.xl + self.xxl)




COLOUR_CHOICE=(
    ('Blue','Blue'),
    ('Sky Blue','Sky Blue'),
    ('Red','Red'),
    ('White','White'),
)

class Order(models.Model):
    garment=models.ForeignKey(Garment,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=20)
    fabric=models.ForeignKey(Fabric,on_delete=models.CASCADE)
    colour=models.CharField(choices=COLOUR_CHOICE,max_length=30)
    # size_and_quantity=models.ManyToManyField(Measurments)
    slug=models.SlugField(blank=True,null=True)
    cost=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f'{self.garment.name}-{self.fabric.name.name}-({self.quantity})'

    def get_product_detail(self):
        return reverse('quick_costing_order_detail',kwargs={'slug':self.slug})

    def get_plan_id(self):
        quantity=int(self.quantity)
        plan_id=1
        if(quantity <= 20):
            plan_id=1
        elif(quantity <= 100 ):
            plan_id=2
        elif(quantity <= 500):
            plan_id=3
        elif(quantity <= 5000):
            plan_id=4
        elif(quantity <= 10000):
            plan_id=5
        else:
            plan_id=6
        return plan_id


# def randomNum()

""" Here we are creating slug if their is on slug """
# TODO slugify is user fro creating slug

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(f'{instance.garment.name}{random.randint(10,99999)}')
pre_save.connect(pre_save_blog_post_receiver, sender=Order)



class CostingRate(models.Model):

    plan= models.ForeignKey(Plan,on_delete=models.CASCADE)
    fabric=models.ForeignKey(Fabric,on_delete=models.CASCADE)
    # garment=models.ForeignKey(Garment,on_delete=models.CASCADE)

    Fabric_Rate = models.IntegerField(default=100)
    Fabric_Consumption = models.FloatField(default=2.5)
    SMV = models.IntegerField(default=25)
    Rate_Min = models.IntegerField(default=12)
    Cut_Make = models.IntegerField(default=300)
    Trims_and_Pack = models.IntegerField(default=50)

    Basic_Cost_Unit = models.IntegerField(default=600,blank=True,null=True)

    Finishing_Washing = models.IntegerField(default=10)
    Inspection = models.IntegerField(default=5)
    Packaging_and_Forwarding = models.FloatField(default=3)
    Transportation = models.FloatField(default=0)
    Management_Cost = models.FloatField(default=10)
    Marketing_Cost = models.FloatField(default=5)
    Overheads = models.FloatField(default=10)

    Final_Costing = models.IntegerField(default=78300,blank=True,null=True)

    Business_Value = models.IntegerField(default=1566000,blank=True,null=True)

    def get_basic_cost_unit(self):
        value=(self.Fabric_Rate) * (self.Fabric_Consumption)+(self.Cut_Make)+(self.Trims_and_Pack)
        return value

    def get_final_costing(self):
        basic_cost=self.get_basic_cost_unit()
        value=(basic_cost)+(self.Finishing_Washing)+(self.Inspection)+((basic_cost)*(self.Packaging_and_Forwarding)+(self.Transportation)+(self.Management_Cost)+(self.Marketing_Cost)+(self.Overheads))
        return value

    def get_business_value(self):
        final_costing=self.get_final_costing()
        value=(final_costing)*(self.plan.to_quantity)
        return value

    def __str__(self):
        return f'{self.plan.name}-{self.fabric.name.name}-{self.fabric.garment.name}'

