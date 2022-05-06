from inputform.resubmit import second_table


def floor_data_seperation(presentdate,date,time,factory_name,floor_no,Sew_Handle,shears,Bundle,Machine_Delay,MB,Personal_fatigue,WT,Others):
    ##---------sending data to variables then to database REPORTS TABLE-----------------------
    report_date= presentdate.date()
    A3_Sew_Handle=0
    A3_shears=0
    A3_Bundle=0
    A3_Machine_Delay=0
    A3_H1_MB=0
    A3_PF=0
    A3_H1_WT=0
    A3_Others=0
    A4_Sew_Handle=0
    A4_shears=0
    A4_Bundle=0
    A4_Machine_Delay=0
    A4_H1_MB=0
    A4_PF=0
    A4_H1_WT=0
    A4_Others=0
            
    if floor_no=="A3 - Line 1" or floor_no=="A3 - Line 2" or floor_no=="A3 - Line 3" or floor_no=="A3 - Line 4":
    
        A3_Sew_Handle   =  Sew_Handle   
        A3_shears   =   shears
        A3_Bundle   =   Bundle
        A3_Machine_Delay   =   Machine_Delay
        A3_H1_MB   =    MB
        A3_PF   =    Personal_fatigue
        A3_H1_WT   =   WT
        A3_Others   =    Others

    elif floor_no=="A4 - Line 1" or floor_no=="A4 - Line 2" or floor_no=="A4 - Line 3" or floor_no=="A4 - Line 4":
    
        A4_Sew_Handle   =    Sew_Handle 
        A4_shears   =    shears
        A4_Bundle   =   Bundle
        A4_Machine_Delay   =   Machine_Delay
        A4_H1_MB   =    MB
        A4_PF   =    Personal_fatigue
        A4_H1_WT   =   WT
        A4_Others   = Others
    
    #calling the function for cummulative table which is located in resubmit.py module
    second_table(date,report_date,A3_Sew_Handle,A3_shears,A3_Bundle,A3_Machine_Delay,A3_H1_MB,A3_PF,A3_H1_WT,A3_Others,A4_Sew_Handle,A4_shears,A4_Bundle,A4_Machine_Delay,A4_H1_MB,A4_PF,A4_H1_WT,A4_Others,)

       