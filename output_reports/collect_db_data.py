



#these values are used to provide when the website is open for the first time
#it returns the duplicate dictonary to render for initial value display 
##Do not modify duplicate_output() it may effect the webpage

class output_values_seperation():

    def result_after_search(self,result,selected_floor_no,selected_date):
            
 

            self.total_sew_handle_value = result.A4_Sew_Handle
            self.total_shears_value = result.A4_shears
            self.total_Bundle_value = result.A4_Bundle
            self.total_machine_delay_value = result.A4_Machine_Delay
            self.total_machine_breakdown_value = result.A4_H1_MB
            self.total_pf_value = result.A4_PF
            self.total_wt_value = result.A4_H1_WT
            self.total_others_value = result.A4_Others
        
