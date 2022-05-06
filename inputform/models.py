from django.db import models

# Create your models here.
class InputTable(models.Model):
    factory_name=models.CharField(max_length=100)
    floor_no=models.CharField(max_length=100)
    date    =   models.CharField(max_length=100)       #DateField()
    time    =   models.CharField(max_length=100) #TimeField()
    Sew_Handle  =   models.IntegerField()
    shears  =   models.IntegerField()
    Bundle  =   models.IntegerField()
    Machine_Delay   =   models.IntegerField()
    H1_MB   =   models.IntegerField()
    Personal_fatigue    =   models.IntegerField()
    H1_WT   =  models.IntegerField()
    Others  =   models.IntegerField()

class Total_values_Table(models.Model):
    
    report_date=models.DateField(max_length=100)
    
    #A3
    A3_Sew_Handle   =   models.IntegerField(default=0)
    A3_shears   =   models.IntegerField(default=0)
    A3_Bundle   =   models.IntegerField(default=0)
    A3_Machine_Delay   =   models.IntegerField(default=0)
    A3_H1_MB   =   models.IntegerField(default=0)
    A3_PF   =   models.IntegerField(default=0)
    A3_H1_WT   =   models.IntegerField(default=0)
    A3_Others   =   models.IntegerField(default=0)

    #A4
    A4_Sew_Handle   =   models.IntegerField(default=0)
    A4_shears   =   models.IntegerField(default=0)
    A4_Bundle   =   models.IntegerField(default=0)
    A4_Machine_Delay   =   models.IntegerField(default=0)
    A4_H1_MB   =   models.IntegerField(default=0)
    A4_PF   =   models.IntegerField(default=0)
    A4_H1_WT   =   models.IntegerField(default=0)
    A4_Others   =   models.IntegerField(default=0)
