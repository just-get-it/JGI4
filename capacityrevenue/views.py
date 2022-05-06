from django.shortcuts import render
from capacityrevenue.models import capacity_revenue_table
from capacityrevenue.calculations import calculations
from django.db import connection
import psycopg2

# Create your views here.
def capacity_n_revenue(request):

    if request.method == 'POST':
          
        selected_date=request.POST.get('selected_date')
        
        results=capacity_revenue_table.objects.filter(output_date=selected_date)
        for data in results:
            if str(selected_date)==str(data.output_date):
                object_alldata=calculations()             
                object_alldata.results_after_search(data)
                dynamic_rows=list(range(1,no+1))
                
                return render(request,'internship/capacitynrevenue.html',{"dynamic_rows":dynamic_rows,"object_alldata":object_alldata})
            
        return render(request,'internship/capacitynrevenue.html')
    
    else:
        return render(request,'internship/capacitynrevenue.html')

