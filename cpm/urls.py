from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('hello', views.cpm, name = 'cpm'),
    path('domestic_travel_requisition', views.domestic_travel_requisition, name='domestic_travel_requisition'),
    path('domestic_travel_voucher', views.domestic_travel_voucher, name = 'domestic_travel_voucher'),
    path('domestic_voucher_view', views.domestic_voucher_view, name = 'domestic_voucher_view'),
    path('wages_and_emp_summary', views.wages_and_emp_summary, name = 'wages_and_emp_summary'),
    path('daily_linewise_available_minutes', views.daily_linewise_available_minutes, name = 'daily_linewise_available_minutes'),
    path('monthly_linewise_available_minutes', views.monthly_linewise_available_minutes, name = 'monthly_linewise_available_minutes'),
    path('data', views.data, name = 'data'),
    path('wage_table', views.wage_table, name = 'wage_table'),
    path('min_table', views.min_table, name = 'min_table'),
    path('mon_minute', views.mon_minute, name = 'mon_minute'),
    path('expenses_data', views.expenses_data, name = 'expenses_data'),
    path('direct_wages', views.direct_wages, name = 'direct wages'),
    path('factory_overhead', views.factory_overhead, name = 'factory_overhead'),
    path('administrative_expenses', views.administrative_expenses, name = 'administrative_expenses'),
    path('commercial_expenses', views.commercial_expenses, name='commercial_expenses'),
    path('financial_expenses', views.financial_expenses, name='financial_expenses'),
    path('expenses_record', views.expenses_record, name = 'expenses_record'),

]