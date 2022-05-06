
import datetime
from .models import InputTable,Total_values_Table

#This file is used to get  cummulative values in database and storing these cummulative values in new table named "Total_values_Table"
def second_table(date,report_date,A3_Sew_Handle,A3_shears,A3_Bundle,A3_Machine_Delay,A3_H1_MB,A3_PF,A3_H1_WT,A3_Others,A4_Sew_Handle,A4_shears,A4_Bundle,A4_Machine_Delay,A4_H1_MB,A4_PF,A4_H1_WT,A4_Others):

    
    all_old_data = Total_values_Table.objects.all()
    
    for NEW in all_old_data:
        if  NEW.report_date == report_date:
            #Taking a dummy variables for updating the old rows in DB
            updating_A3_Sew_Handle      = NEW.A3_Sew_Handle + int(A3_Sew_Handle)  #i[] means db previous value 
            updating_A3_shears          = NEW.A3_shears + int(A3_shears)
            updating_A3_Bundle          = NEW.A3_Bundle + int(A3_Bundle)
            updating_A3_Machine_Delay   = NEW.A3_Machine_Delay + int(A3_Machine_Delay)
            updating_A3_H1_MB           = NEW.A3_H1_MB + int(A3_H1_MB)
            updating_A3_PF              = NEW.A3_PF + int(A3_PF)
            updating_A3_H1_WT           = NEW.A3_H1_WT + int(A3_H1_WT)
            updating_A3_Others          = NEW.A3_Others + int(A3_Others)  

            updating_A4_Sew_Handle      = NEW.A4_Sew_Handle + int(A4_Sew_Handle)
            updating_A4_shears          = NEW.A4_shears + int(A4_shears)
            updating_A4_Bundle          = NEW.A4_Bundle + int(A4_Bundle)
            updating_A4_Machine_Delay   = NEW.A4_Machine_Delay + int(A4_Machine_Delay)
            updating_A4_H1_MB           = NEW.A4_H1_MB + int(A4_H1_MB)
            updating_A4_PF              = NEW.A4_PF + int(A4_PF)
            updating_A4_H1_WT           = NEW.A4_H1_WT + int(A4_H1_WT)
            updating_A4_Others          = NEW.A4_Others + int(A4_Others)

            TotalValuesTable = Total_values_Table.objects.get(report_date=date)
            TotalValuesTable.A3_Sew_Handle = updating_A3_Sew_Handle 
            TotalValuesTable.A3_shears  =   updating_A3_shears
            TotalValuesTable.A3_Bundle   =  updating_A3_Bundle
            TotalValuesTable.A3_Machine_Delay  =   updating_A3_Machine_Delay
            TotalValuesTable.A3_H1_MB   =  updating_A3_H1_MB
            TotalValuesTable.A3_PF   =  updating_A3_PF
            TotalValuesTable.A3_H1_WT   =  updating_A3_H1_WT
            TotalValuesTable.A3_Others    = updating_A3_Others  

            TotalValuesTable.A4_Sew_Handle   =  updating_A4_Sew_Handle
            TotalValuesTable.A4_shears   =  updating_A4_shears
            TotalValuesTable.A4_Bundle   =  updating_A4_Bundle
            TotalValuesTable.A4_Machine_Delay   =  updating_A4_Machine_Delay
            TotalValuesTable.A4_H1_MB   =  updating_A4_H1_MB
            TotalValuesTable.A4_PF   =  updating_A4_PF
            TotalValuesTable.A4_H1_WT   =  updating_A4_H1_WT
            TotalValuesTable.A4_Others   =  updating_A4_Others

            TotalValuesTable.save()
            break

    else:
        updating_A3_Sew_Handle      = int(A3_Sew_Handle)  #i[] means db previous value 
        updating_A3_shears          = int(A3_shears)
        updating_A3_Bundle          = int(A3_Bundle)
        updating_A3_Machine_Delay   = int(A3_Machine_Delay)
        updating_A3_H1_MB           = int(A3_H1_MB)
        updating_A3_PF              = int(A3_PF)
        updating_A3_H1_WT           = int(A3_H1_WT)
        updating_A3_Others          = int(A3_Others)  

        updating_A4_Sew_Handle      = int(A4_Sew_Handle)
        updating_A4_shears          = int(A4_shears)
        updating_A4_Bundle          = int(A4_Bundle)
        updating_A4_Machine_Delay   = int(A4_Machine_Delay)
        updating_A4_H1_MB           = int(A4_H1_MB)
        updating_A4_PF              = int(A4_PF)
        updating_A4_H1_WT           = int(A4_H1_WT)
        updating_A4_Others          = int(A4_Others)


    
        ## we need to check once
        TotalvaluesTable=Total_values_Table(report_date=report_date,
                            A3_Sew_Handle=updating_A3_Sew_Handle,
                            A3_shears=updating_A3_shears,
                            A3_Bundle=updating_A3_Bundle,
                            A3_Machine_Delay=updating_A3_Machine_Delay,
                            A3_H1_MB=updating_A3_H1_MB,
                            A3_PF=updating_A3_PF,
                            A3_H1_WT=updating_A3_H1_WT,
                            A3_Others=updating_A3_Others,
                            A4_Sew_Handle=updating_A4_Sew_Handle,
                            A4_shears=updating_A4_shears,
                            A4_Bundle=updating_A4_Bundle,
                            A4_Machine_Delay=updating_A4_Machine_Delay,
                            A4_H1_MB=updating_A4_H1_MB,
                            A4_PF=updating_A4_PF,
                            A4_H1_WT=updating_A4_H1_WT,
                            A4_Others=updating_A4_Others)
        
        TotalvaluesTable.save()
