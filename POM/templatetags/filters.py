from django import template
from fractions import Fraction    

def dec_to_proper_frac(dec):
    sign = "-" if dec < 0 else ""
    frac = Fraction(str(abs(dec)))
    s=(f"{sign}{frac.numerator // frac.denominator} "
            f"{frac.numerator % frac.denominator} {frac.denominator}")
    s=list(map(int,s.strip().split(" ")))
    return s


register = template.Library()


@register.filter
def fullPOM(value,a):
    return value


@register.filter
def halfPOM(value,a):
    value=float(value)
    if a.get('section1')=='half':
        return round(value/2,2)
    return value

# Section 2
@register.filter
def wholeNo(value,a):
    value=float(value)
    if a.get('section2')=='whole':
        return int(value)
    return value

@register.filter
def approxbyquarter(value,a):
    value=float(value)
    if a.get('section2')=='quarter':
        value=round(value*4)/4
    return value

@register.filter
def approxbyhalf(value,a):
    value=float(value)
    if a.get('section2')=='half':
        value=round(value*2)/2
    return value


@register.filter
def onedigit(value,a):
    value=float(value)
    if a.get('section2')=='one':
        return round(value,1)
    return value


@register.filter
def twodigit(value,a):
    value=float(value)
    return round(value,2)

@register.filter
def eighth(value,a):
    value=float(value)
    if a.get('section2')=='eighth':
        value=round(value*8)/8
    return value

@register.filter
def fraction(value,a):
    value=float(value)
    # if a.get('section2')=='fraction':
    return dec_to_proper_frac(value)
    return value


# Section 3

@register.filter
def cm(value,a):
    value=float(value)
    if a.get('section3')=='cm':
        return round(value,2)
    return value


@register.filter
def inch(value,a):
    value=float(value)
    if a.get('section3')=='inch':
        # x=dec_to_proper_frac(round(value/2.54,2))
        return round(value/2.54,2)
    return value


# Another Section

@register.filter
def doubleTolerance(value):
    return round(value*2,2)




@register.filter
def safe_text(value):
    li=list(map(str,value.split("_")))
    li=' '.join(li)
    return li




@register.filter
def split_top(value):
    li=list(value.split(","))
    print(li)
    return li


@register.filter
def get_item_color(dicto,key):
    return dicto[key][0][0]


@register.filter
def get_item_location(dicto,key):
    return dicto[key][0][1].id

@register.filter
def get_item_sizes(dicto,key):
    return dicto[key][1]



@register.filter
def typelist(value):
    l=value.strip().split(",")
    la=[]
    for i in l:
        if i:
            la.append(i)
    return la