from django.db import models
from django.contrib.auth.models import User

from product.models import product
from userdetail.models import *



# class Customer(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.email

# class Product(models.Model):
#     name = models.ForeignKey(product, on_delete=models.CASCADE,null=True)
#     digital = models.BooleanField(default=False,blank=False)

#     def __str__(self):
#         return self.name



# class Order(models.Model):
#     customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, blank=False)
#     transaction_id = models.CharField(max_length=200,null=True)
    

#     def __str__(self):
#         return str(self.customer_id) + '  ' + str(self.customer) 

#     @property
#     def get_ordered_products(self):
#         # orderitems = OrderItem.objects.all() # for all the items
#         orderitems = OrderItem.objects.filter(delivered=False)  # undelivered only
        
#         my_products = []
#         for item in orderitems:
#             if item.product:
#                 for scq in item.product.size_color_quantity_set.all():
#                     my_products.append([scq, item.date_added, item])

#         return my_products


#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total for item in orderitems])
#         return total

#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total

# class OrderItem(models.Model):
#     delivered=models.NullBooleanField(default=False,blank=True)
#     product = models.ForeignKey(product, on_delete= models.SET_NULL,null=True,blank=True)
#     order = models.ForeignKey(Order, on_delete= models.SET_NULL,null=True,blank=True)
#     quantity = models.IntegerField(default=0, null=True,blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#     accepted=models.NullBooleanField(default=False,blank=True)
#     rejectedbywhom=models.ForeignKey(detail,related_name='rejection',on_delete=models.SET_NULL,null=True,blank=True)
#     acceptedbywhom=models.ForeignKey(detail,related_name='acception',on_delete=models.SET_NULL,null=True,blank=True)
#     assigntoafterrejection=models.ManyToManyField(detail,blank=True,related_name='assigntoanothervendorafterrejection')
    

#     def __str__(self):
#         return str(self.product) + '  ' + str(self.order) + '  ' + str(self.id) 

#     @property
#     def get_price(self):
#         price = self.product.price
#         if self.product.offer:
#             mrp = price
#             offer = self.product.offer
#             price = mrp - (mrp * offer // 100)
#         return price

#     @property
#     def get_total(self):
#         total = self.get_price * self.quantity
#         return total


# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
#     address = models.CharField(max_length=200, null=True)
#     city = models.CharField(max_length=200, null=True)
#     state = models.CharField(max_length=200, null=True)
#     zipcode = models.CharField(max_length=200, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.address


# class wishlist(models.Model):
#     email=models.CharField(max_length=100)
#     product_code=models.CharField(max_length=100)

# class CartItems(models.Model):
#     email=models.CharField(max_length=100)
#     items=models.IntegerField(default=0)


