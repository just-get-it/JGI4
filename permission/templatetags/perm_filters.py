



from django import template
from fractions import Fraction
from permission.models import staff_permissions,vendor_permissions
from userdetail.models import detail

register = template.Library()


@register.filter
def staff_perm(email,to_control):
    details=detail.objects.filter(email=email).first()
    obj=staff_permissions.objects.filter(user=details).first()
    if obj:
        if to_control=="holidays":
            return obj.holidays
        elif to_control=="run_rate":
            return obj.run_rate
        elif to_control=="profile_status":
            return obj.profile_status
        elif to_control=="response_time":
            return obj.response_time
        elif to_control=="profile_performance":
            return obj.profile_performance
        elif to_control=="hit_run_rate":
            return obj.hit_run_rate
        elif to_control=="activities_order":
            return obj.activities_order
        return False
    else:
        return False


@register.filter
def vendor_perm(email,to_control):
    details=detail.objects.filter(email=email).first()
    obj=vendor_permissions.objects.filter(user=details).first()
    if obj:
        if to_control=="production_product":
            return obj.production_product
        elif to_control=="upload_product":
            return obj.upload_product
        elif to_control=="hit_rate":
            return obj.hit_rate
        elif to_control=="dpr":
            return obj.dpr
        return False
    else:
        return False
