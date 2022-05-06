

#Here you can find whole calculation part

class calculation():
    #collecting input data for calculations
    def calculating_all(self,object_seperation):
        self.total_sew_handle_value = object_seperation.total_sew_handle_value
        self.total_shears_value = object_seperation.total_shears_value
        self.total_Bundle_value = object_seperation.total_Bundle_value
        self.total_machine_delay_value = object_seperation.total_machine_delay_value
        self.total_machine_breakdown_value = object_seperation.total_machine_breakdown_value
        self.total_pf_value = object_seperation.total_pf_value
        self.total_wt_value = object_seperation.total_wt_value
        self.total_others_value = object_seperation.total_others_value

        #adding all the values 
        self.percent_symbol='%'
        self.total_sewhandle_shears_value=object_seperation.total_sew_handle_value + object_seperation.total_shears_value
        self.total_occurance=object_seperation.total_sew_handle_value + object_seperation.total_shears_value + object_seperation.total_Bundle_value + object_seperation.total_machine_delay_value + object_seperation.total_machine_breakdown_value + object_seperation.total_pf_value + object_seperation.total_wt_value + object_seperation.total_others_value
        
        #Below are percent calculation for percent row in output reports page

        
    def finding_percent(self):    
        self.percent_sew_handle = round((self.total_sewhandle_shears_value/self.total_occurance)*100,2)         if self.total_occurance !=0 else 0
        self.percent_Bundle_value = round((self.total_Bundle_value/self.total_occurance)*100,2)                 if self.total_occurance !=0 else 0
        self.percent_machine_delay_value = round((self.total_machine_delay_value/self.total_occurance)*100,2)   if self.total_occurance !=0 else 0
        self.percent_machine_breakdown_value = round((self.total_machine_breakdown_value/self.total_occurance)*100,2) if self.total_occurance !=0 else 0
        self.percent_pf_value = round((self.total_pf_value/self.total_occurance)*100,2)                         if self.total_occurance !=0 else 0
        self.percent_wt_value = round((self.total_wt_value/self.total_occurance)*100,2)                         if self.total_occurance !=0 else 0
        self.percent_others_value = round((self.total_others_value/self.total_occurance)*100,2)                 if self.total_occurance !=0 else 0
        
        self.total_percents = round(self.percent_Bundle_value+self.percent_machine_delay_value + self.percent_machine_breakdown_value + self.percent_pf_value + self.percent_wt_value + self.percent_others_value,2)

        #Below are for percent sewing time 
    def finding_percent_sewingtime(self):

        self.sew_sewing_time = round((self.percent_sew_handle/self.percent_sew_handle)*100,2)                   if self.percent_sew_handle !=0 else 0
        self.Bundle_value_sewing_time = round((self.percent_Bundle_value/self.percent_sew_handle)*100,2)        if self.percent_sew_handle !=0 else 0
        self.machine_delay_value_sewing_time = round((self.percent_machine_delay_value/self.percent_sew_handle)*100,2) if self.percent_sew_handle !=0 else 0
        self.machine_breakdown_value_sewing_time = round((self.percent_machine_breakdown_value/self.percent_sew_handle)*100,2) if self.percent_sew_handle !=0 else 0
        self.pf_value_sewing_time = round((self.percent_pf_value/self.percent_sew_handle)*100,2)                if self.percent_sew_handle !=0 else 0
        self.wt_value_sewing_time = round((self.percent_wt_value/self.percent_sew_handle)*100,2)                if self.percent_sew_handle !=0 else 0
        self.others_value_sewing_time = round((self.percent_others_value/self.percent_sew_handle)*100,2)        if self.percent_sew_handle !=0 else 0

        self.total_sewing_time_percent = round(self.sew_sewing_time + self.Bundle_value_sewing_time + self.machine_breakdown_value_sewing_time + self.machine_delay_value_sewing_time + self.pf_value_sewing_time + self.wt_value_sewing_time,2)

        #these are the standard values
    def standard_values(self):
        
        self.total_sewhandle_shears_standard = 100
        self.Bundle_value_standard = 15
        self.machine_delay_value_standard = 2
        self.machine_breakdown_value_standard = 1
        self.pf_value_standard = 3
        self.wt_value_standard = 1
        self.others_value_standard = 3

        self.total_standard_values = round(self.Bundle_value_standard + self.machine_delay_value_standard  + self.machine_breakdown_value_standard + self.pf_value_standard + self.wt_value_standard + self.others_value_standard,2)

        self.estimated_efficiency = 60

        #Below values for scope of improve row in output reports page
    def scope_of_improve(self):
        self.Bundle_value_soi = self.Bundle_value_sewing_time-self.Bundle_value_standard
        self.machine_delay_value_soi =  self.machine_delay_value_sewing_time - self.machine_delay_value_standard
        self.machine_breakdown_value_soi = self.machine_breakdown_value_sewing_time - self.machine_breakdown_value_standard
        self.pf_value_soi = self.pf_value_sewing_time - self.pf_value_standard
        self.wt_value_soi = self.wt_value_sewing_time -  self.wt_value_standard
        self.others_value_soi = self.others_value_sewing_time - self.others_value_standard

        self.total_soi = round(self.Bundle_value_soi + self.machine_delay_value_soi + self.machine_breakdown_value_soi + self.pf_value_soi + self.wt_value_soi + self.others_value_soi,2)
    
        self.acheivable_imporvement  = round(self.total_soi * self.estimated_efficiency,2)
        

        
