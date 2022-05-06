from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render,redirect,render
from django.contrib.auth import authenticate,login,logout,get_user_model

import random
import json
# import datetime
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar

from datetime import datetime
from datetime import timedelta

from calendar import calendar
from calendar import monthrange
# def calendar(request):


#     return render(request,"calendar/calendar.html",{})

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, user = self.request.user)
        p_year, p_month = prev_month(d)
        n_year, n_month = next_month(d)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # get previous and next year
        context['p_year'] = p_year
        context['p_month'] = p_month

        context['n_year'] = n_year
        context['n_month'] = n_month        
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()

def prev_month(d):
    print(d)
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    return prev_month.year, prev_month.month

def next_month(d):
    number_of_days = monthrange(d.year, d.month)[1]
    first = d.replace(day=number_of_days)
    next_month = first + timedelta(days=1)
    return next_month.year, next_month.month