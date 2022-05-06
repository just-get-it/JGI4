from django.contrib import admin
from .models import InputTable,Total_values_Table
import datetime

# Register your models here.
admin.site.register(InputTable)
admin.site.register(Total_values_Table)


#fetching data individually from db
'''
presentdate=datetime.datetime.now()
report_date= presentdate.date()
mydb=mysql.connector.connect(host="localhost",user="root",password="9848358166vV-",database='vamsijgidb')
mycursor = mydb.cursor()
mycursor.execute("select * from inputform_total_values_table")
result=mycursor.fetchall()
display = Total_values_Table.objects.get(report_date='')
print('result',display.A4_Sew_Handle)

'''

