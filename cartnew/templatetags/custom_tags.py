from django import template
from datetime import *
register = template.Library()


def startDate(value):
    return str(value.next_delivery_date + timedelta(days=value.interval))+"T"+value.shifts

register.filter('startDate', startDate)