import datetime

from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone,dates
from datetime import date
from product.models import product



class RentPlan(models.Model):
    name=models.CharField(default="Rent Plan",max_length=20)
    from_price=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(500000)])
    upto_price=models.IntegerField(default=0,validators=[MinValueValidator(2000),MaxValueValidator(500000)])

    def __str__(self):
        return f'{self.from_price} to {self.upto_price}'



class RentingCost(models.Model):
    plan=models.ForeignKey(RentPlan,on_delete=models.CASCADE)
    courier_charge=models.IntegerField(default=25,
                                       validators=[MinValueValidator(25),MaxValueValidator(1000)])
    is_garment=models.BooleanField(default=False,help_text="For Dry Clean Charge")
    dry_clean_charge=models.IntegerField(default=50,
                                         validators=[MinValueValidator(50),MaxValueValidator(1000)],
                                         blank=True,null=True)
    is_heavy=models.BooleanField(default=False,help_text="For Courier Charge")

    def __str__(self):
        return f'{self.plan}--{self.courier_charge}'

    def base_rate(self):
        per=5
        if  self.is_heavy==True:
            per=6
        else:
            per=5
        value=per*(self.plan.upto_price)*0.01
        return value

    def total_rent_cost_per_quantity(self,quantity):
        dry_clean=0
        courier_charge=int(self.courier_charge)
        base_rate = self.base_rate()

        if self.is_garment==True:
            dry_clean=self.dry_clean_charge

        value=courier_charge*2+(dry_clean+base_rate)*quantity
        return value



QUANTITY=(
    (1,1),
    (2,2),
    (4,4),
    (7,7),
    (10,10),
    (15,15),
    (20,20),
    (25,25),
    (30,30),
    (35,35),
    (40,40),
    (50,50),
)
DAYS=(
    (3,3),
    (4,4),
    (7,7),
    (15,15),
)

class QuantityAndDuration(models.Model):
    quantity = models.IntegerField(default=4, choices=QUANTITY)
    duration = models.IntegerField(default=3,choices=DAYS)

    def __str__(self):
        return f'{self.quantity} pics for {self.duration} days'


class QuantitySizeColour(models.Model):
    quantity=models.IntegerField(default=1)
    size=models.CharField(default="Medium",max_length=10,blank=True)
    colour=models.CharField(default="#000000",max_length=10,blank=True)

    def __str__(self):
        return f'{self.size} -- {self.colour} -- {self.quantity}'


class ProductInRentCart(models.Model):
    rent_product=models.ForeignKey(product,on_delete=models.CASCADE)
    total_quantity=models.IntegerField(default=1,blank=True,null=True)
    quantity_size_colour=models.ManyToManyField(QuantitySizeColour,blank=True)
    start_date=models.DateField(blank=True,null=True,help_text="yyyy-mm-dd")
    end_date=models.DateField(blank=True,null=True,help_text="yyyy-mm-dd")

    def __str__(self):
        return f'{self.rent_product.title}'


    # def get_rent_cart_product_absolute_url(self):
    #     return reverse('rent_cart_detailView',kwargs={'rent_cart_product_id':self.pk})

    # Quantity Selected
    def get_total_quantity(self):
        value=0
        for i in self.quantity_size_colour.all():
            value+=i.quantity
        return value

    def total_amount(self):
        quantity=self.get_total_quantity()
        return (quantity*self.rent_product.price)

    def get_days(self):
        value=self.end_date.day - self.start_date.day
        return value


class RentOrder(models.Model):
    rent_products=models.ManyToManyField(ProductInRentCart)
    start_date=models.DateField(blank=True,null=True,help_text="yyyy-mm-dd")
    end_date=models.DateField(blank=True,null=True,help_text="yyyy-mm-dd")
    is_ordered=models.BooleanField(default=False)

    # def __str__(self):
    #     return

    def get_selected_total_number_of_rent_products(self):
        number_of_product=0
        total_quantity=0
        for prod in self.rent_products.all():
            number_of_product+=1
            total_quantity+=prod.get_total_quantity()
        return number_of_product,total_quantity

    def get_selected_quantity(self):
        total_quantity=0
        for prod in self.rent_products.all():
            total_quantity+=prod.get_total_quantity()
        return total_quantity

    def get_selected_final_amount(self):
        final_price=0
        for prod in self.rent_products.all():
            final_price+=prod.total_amount()
        return final_price

    def get_start_date(self):
        prod=self.rent_products.all()[0]
        return prod.start_date

    def get_end_date(self):
        prod=self.rent_products.all()[0]
        return prod.end_date
    def add_start_and_end_date(self):
        self.start_date=self.get_start_date()
        self.end_date=self.get_end_date()
        return

    def get_number_of_days(self):
        return self.get_end_date().day-self.get_start_date().day

    # TODO standard deviation and .....



    def get_avg(self):
        x = self.get_selected_quantity()
        if self.get_selected_quantity() == 0:
            x = 1
        value=1
        for prod in self.rent_products.all():
            value+=prod.total_amount()
        return value//(x)

    def get_plan_id(self):
        price=int(self.get_avg())
        plan_id=1
        if(price <= 2000):
            plan_id=1
        elif(price <= 5000):
            plan_id=2
        elif(price <= 10000):
            plan_id=3
        elif(price <= 20000):
            plan_id=4
        elif(price <= 50000):
            plan_id=5
        elif (price <= 100000):
            plan_id = 6
        elif (price <= 500000):
            plan_id = 7
        else:
            plan_id=8
        return plan_id
