from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template



from django.core.mail import send_mail,EmailMultiAlternatives
from movintrendz.settings import EMAIL_HOST_USER


from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



ones = ["", "One ","Two ","Three ","Four ", "Five ", "Six ","Seven ","Eight ","Nine ","Ten ","Eleven ","Twelve ", "Thirteen ", "Fourteen ", "Fifteen ","Sixteen ","Seventeen ", "Eighteen ","Nineteen "]

twenties = ["","","Twenty ","Thirty ","Forty ", "Fifty ","Sixty ","Seventy ","Eighty ","Ninety "]

thousands = ["","Thousand ","Million ", "Billion ", "Trillion ", "Quadrillion ", "Quintillion ", "Sextillion ", "Septillion ","Octillion ", "Nonillion ", "Decillion ", "Undecillion ", "Duodecillion ", "Tredecillion ", "Quattuordecillion ", "Quindecillion", "Sexdecillion ", "Septendecillion ", "Octodecillion ", "Novemdecillion ", "Vigintillion "]


def num999(n):
    c = n % 10 # singles digit
    b = int(((n % 100) - c) / 10) # tens digit
    a = int(((n % 1000) - (b * 10) - c) / 100) # hundreds digit
    t = ""
    h = ""
    if a != 0 and b == 0 and c == 0:
        t = ones[int(a)] + "Hundred "
    elif a != 0:
        t = ones[int(a)] + "Hundred and "
    if b <= 1:
        h = ones[int(n%100)]
    elif b > 1:
        h = twenties[int(b)] + ones[int(c)]
    st = t + h
    return st

def num2word(num):
    if num == 0:
        return 'Zero'
    i = 3
    n = str(num)
    word = ""
    k = 0
    while(i == 3):
        nw = n[-i:]
        n = n[:-i]
        if int(nw) == 0:
            word = num999(int(nw)) + thousands[int(nw)] + word
        else:
            word = num999(int(nw)) + thousands[int(k)] + word
        if n == '':
            i = i+1
        k += 1
    return word[:-1]




def send_email(subject,message,from_email,to_list):
    send_mail(subject,message,from_email,to_list,fail_silently=True)
    return True



import math, random

import string

# function to generate OTP
def generateOTP4digit() :

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

   # length of password can be chaged
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


# function to generate OTP
def generateOTP6digit() :

    # Declare a string variable
    # which stores all string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]

    return OTP





def randomStringDigits(stringLength=30):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))



import re

# Make a regular expression
# for validating an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for
# for validating an Email
def check_email_correctness(email):

    # pass the regualar expression
    # and the string in search() method
    if(re.search(regex,email)):
        return True

    else:
        return False

'''Calendar utility'''
from cal.models import Event
from .models import Subscription_Stop
from datetime import date, datetime, timedelta

def createEvents(a):
    '''
        Create event for each deliver.
    '''

    start_date = a.start_date
    s_year, s_month, s_day = [int(x) for x in str(start_date).split('-')]
    end_date = a.end_date
    e_year, e_month, e_day = [int(x) for x in str(end_date).split('-')]
    interval = int(a.interval)
    start_date = datetime(s_year, s_month, s_day)
    start_date_copy = datetime(s_year, s_month, s_day)
    end_date = datetime(e_year, e_month, e_day)
    user = a.customer_email
    transaction_id = a.transaction_id
    title = a.product_name + " subscription " + a.shifts

    while start_date <= end_date:
        print('created')
        e = Event(
            title = title,
            user = user,
            sub_transaction_id = transaction_id,
            start_time = start_date
        )
        e.save()
        start_date = start_date + timedelta(days=interval)
    # Set the first Event(start_date) isPaidForEvent = True
    Event.objects.filter(sub_transaction_id=transaction_id, start_time=start_date_copy).update(isPaidForEvent=True)   

def updateEvent(subscription_instance, isStartDateChanged, isEndDateChanged, isIntervalChanged):
    '''
        User Subscription_Stop model to get the Events that are valid.
        To be flexible with start_date and end_date
    '''
    transaction_id = subscription_instance[0].transaction_id
    title = subscription_instance[0].product_name + " subscription " + subscription_instance[0].shifts
    interval = subscription_instance[0].interval
    subscription_start = subscription_instance[0].start_date
    subscription_end = subscription_instance[0].end_date
    user = subscription_instance[0].customer_email
    
    events = Event.objects.filter(sub_transaction_id = transaction_id, user=user)
    
    today_date = date.today()

    if isStartDateChanged:
        
        # deleting previous events:
        Event.objects.filter(sub_transaction_id = transaction_id, user=user).delete()

        # recreating all events:
        current_date = subscription_start
        while current_date <= subscription_end:
            e = Event(
                title = title,
                sub_transaction_id = transaction_id,
                start_time = current_date,
                user = user
            )
            e.save()
            current_date = current_date + timedelta(days=interval)

        Event.objects.filter(sub_transaction_id=transaction_id, start_time=subscription_start).update(isPaidForEvent=True)
    else:
        if isIntervalChanged:
            # delete all the records from today onwards:
            
            Event.objects.filter(sub_transaction_id = transaction_id, user = user, start_time__gte=today_date).delete()
            if today_date <= subscription_start:
                current_date = subscription_start
            else:
                last_end_date = Event.objects.filter(sub_transaction_id = transaction_id, user=user).order_by('-start_time')[0].start_time
                print(last_end_date)
                current_date = last_end_date + timedelta(days=interval)
            while current_date <= subscription_end:
                e = Event(
                    title = title,
                    sub_transaction_id = transaction_id,
                    start_time = current_date,
                    user = user
                )
                e.save()
                current_date = current_date + timedelta(days=interval)

            if today_date <= subscription_start:
                Event.objects.filter(sub_transaction_id=transaction_id, start_time=subscription_start).update(isPaidForEvent=True)
        else:
            # check if end date is changed:
            if isEndDateChanged != 0:
                if isEndDateChanged == 1:
                    # adding dates:
                    last_end_date = Event.objects.filter(sub_transaction_id = transaction_id, user=user).order_by('-start_time')[0].start_time
                    current_date = last_end_date + timedelta(days=interval)
                    while current_date <= subscription_end:
                        e = Event(
                            title = title,
                            sub_transaction_id = transaction_id,
                            start_time = current_date,
                            user = user
                        )
                        e.save()
                        current_date = current_date + timedelta(days=interval)
                else:
                    # deleting extra:
                    Event.objects.filter(sub_transaction_id = transaction_id, user=user, start_time__gt=subscription_end).delete()    
            
        # Handling changes in interval:
        

    # Handling changes in start_date:
    # e = Event.objects.filter(sub_transaction_id = transaction_id, start_time__lte=subscription_start).delete()

    # Handling changes in end_date:
    # prev_last_date = Event.objects.filter(sub_transaction_id=transaction_id).order_by('-start_time')[0].start_time
    # if prev_last_date > subscription_end:
    #     Event.objects.filter(sub_transaction_id=transaction_id, start_time__gt=subscription_end).delete()
    # else:
    #     current_last_date = prev_last_date + timedelta(days=interval)
    #     while current_last_date <= subscription_end:
    #         e = Event(
    #         title = title,
    #         sub_transaction_id = transaction_id,
    #         start_time = current_last_date
    #         )
    #         e.save()
    #         current_last_date = current_last_date + timedelta(days=interval)

    # Handling stops
    stop_dates = Subscription_Stop.objects.filter(transaction_id = transaction_id, user = user)
    for event in events:
        for stop_date in stop_dates:
            if stop_date.start_date <= event.start_time <= stop_date.end_date:
                event.isStopped = True
                event.save(update_fields=['isStopped'])
            else:
                event.isStopped = False
                event.save(update_fields=['isStopped'])
        
def deleteEvent(transaction_id, user):
    '''
        To delete all the events once Subscription is deleted.
        To delete all the subscription stops once subscription is deleted
    '''
    Event.objects.filter(sub_transaction_id = transaction_id, user = user).delete()
    Subscription_Stop.objects.filter(transaction_id = transaction_id, user = user).delete()