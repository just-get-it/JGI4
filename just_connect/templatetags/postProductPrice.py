from django import template
from just_connect.models import ProductBooking
register = template.Library()


@register.simple_tag
def product_price(product, index):
    prod = product[index]
    booked_instance = ProductBooking.objects.filter(product=prod)
    new_price = prod.mrp + ((prod.mrp*prod.cost_increment)/100)*(len(booked_instance))
    print("newPrice_function", new_price)
    return new_price  

@register.simple_tag
def total_booking(product, index):
    prod = product[index]
    return prod.total_booking

@register.simple_tag
def min_booking (product, index):
    prod = product[index]
    return prod.min_bookings

@register.simple_tag
def max_booking(product, index):
    prod = product[index]
    return prod.max_bookings


@register.simple_tag
def cal_cart_product_price(prod, cost):
    mrp = prod.product.mrp;
    total_mrp = mrp + cost
    return total_mrp

@register.simple_tag
def cart_sub_total(products):
    sub_total = 0
    for prod in products:
        mrp = prod.product.mrp;
        total_mrp = mrp + prod.cost
        sub_total = sub_total + total_mrp
    return sub_total
