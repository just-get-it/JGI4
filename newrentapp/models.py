from django.db import models
from userdetail.models import *
from cartnew.models import ShippingAddress
from product.models import product, size_color_quantity
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class rental_Plan(models.Model):
    lower_limit_price=models.IntegerField(default=0,validators=[MinValueValidator(1),MaxValueValidator(500000)],unique=True)
    upper_limit_price=models.IntegerField(default=0,validators=[MinValueValidator(100),MaxValueValidator(500000)],unique=True)

    def __str__(self):
        return f'{self.lower_limit_price} to {self.upper_limit_price}'


rentStatus = (
    ('Placed','PLACED'),
    ('Accepted','ACCEPTED'),
    ('Dispatched','DISPATCHED'),
    ('In Use','IN USE'),
    ('Get Return','GET REURN'),
    ('Completed','COMPLETED'),
)

class rental_Order(models.Model):
    date_rental_placed = models.DateTimeField(null=True)
    customer = models.ForeignKey(detail, null=True, on_delete=models.SET_NULL)
    security_amount = models.FloatField(default=0, null=True)
    chargable_amount = models.FloatField(default=0, null=True)
    payment_method = models.CharField(max_length=200, null=True)
    free_delivery = models.BooleanField(default=False)
    is_Cancelled = models.BooleanField(default=False)
    billing_freq =models.CharField(max_length=256, blank=True,null=True)
    next_billing_date = models.DateField(null=True, blank=True)
    invoice = models.FileField(upload_to="local/rental/invoices/",null=True, blank=True)
    def get_all_orders(self):
        res=[]
        orders = self.order_set.all()
        for order in orders:
            res.append(order)
        return res
    
    def get_refund_amount(self):
        return self.security_amount - self.chargable_amount

    def checkPaid(self):
        flag = True
        for i in self.rental_OrderItem_set.all():
            if(i.isPaid==False):
                flag = False
        return flag

class rental_OrderItem(models.Model):
    product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_placed = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    rent_status = models.CharField(choices=rentStatus,max_length=25,default='Placed')
    # per unit
    price = models.FloatField() #mrp - b2c offer
    amount = models.FloatField() #renting amount
    # total
    # total_price = models.FloatField()
    # total_amount = models.FloatField()
    size_color_quantity = models.ForeignKey(size_color_quantity, on_delete=models.DO_NOTHING, null=True)
    customer = models.ForeignKey(detail, on_delete=models.DO_NOTHING, null=True)
    rent_order = models.ForeignKey(rental_Order, on_delete=models.SET_NULL, null=True, blank=True)
    is_Cancelled = models.BooleanField(default=False)
    rent_plan = models.ForeignKey(rental_Plan, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True)
    is_heavy = models.BooleanField(default=False)
    date_placed = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return "Rent "+self.product.title+" "+str(self.id)

    def base_rate(self):
        per=5
        if  self.is_heavy==True:
            per=6
        value=per*(self.rent_plan.upper_limit_price)*0.01
        return value
    
    def get_days(self):
        return int((self.end_date - self.start_date).days)+1

    # total
    def get_total_price(self):
        return self.price * self.quantity
    
    def get_total_amount(self):
        return self.amount * self.quantity * self.get_days()