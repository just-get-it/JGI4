from django.shortcuts import render
from inputform.models import Total_values_Table
from output_reports.calculations import calculation
from output_reports.collect_db_data import output_values_seperation


#This is the main function
def outputreports(request):

     if request.method=='POST':
          #taking input from user
          selected_floor_no=request.POST.get('selected_floor_no')
          selected_date=request.POST.get('selected_date')

          
          #this condition is to check blank date
          if selected_date=='':
               output_info='**Please provide a proper date'
               return render(request,'inputform/reports.html',{"output_info":output_info})

          #accessing data from database based on date 
          NEW=Total_values_Table.objects.raw('select * from inputform_total_values_table where report_date between "'+selected_date+'" and "'+selected_date+'"  ') 

          for result in NEW:

               #this is from collect_db_data.py  it collecting the data from database based on floor and date
               object_seperation = output_values_seperation()
               object_seperation.result_after_search(result,selected_floor_no,selected_date)

               #these are from calculations.py module where all the calculations are done
               object_calculations = calculation()
               object_calculations.calculating_all(object_seperation)
               object_calculations.finding_percent()
               object_calculations.finding_percent_sewingtime()
               object_calculations.standard_values()
               object_calculations.scope_of_improve()

               output_info='**Reports on "'+selected_date+'" for the floor "'+selected_floor_no+'"'

               return render(request,'reports.html',{"selected_floor_no":selected_floor_no,
                                                       "object_seperation":object_seperation,
                                                       "object_calculations":object_calculations,
                                                       "output_info":output_info,
                                                  })
                    
          #This ELSE is for "FOR-LOOP"
          else:
               
               output_info='**Provided date "'+selected_date+'" is not in our  database'
               return render(request,'inputform/reports.html',{"output_info":output_info})

     #This ELSE is for "NON POST METHOD"
     else:
          output_info=''
          return render(request,'inputform/reports.html',{"output_info":output_info})

