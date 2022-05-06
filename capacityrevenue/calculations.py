

class calculations():

    def results_after_search(self,date_based_data):

        #taking all the data from database and storing in some variables
        self.date =  date_based_data.output_date
        self.no_of_years =  int(date_based_data.no_of_years)
        self.no_of_wrkng_days_month =  date_based_data.no_of_wrkng_days_month 
        self.no_of_production_days_year =  date_based_data.no_of_production_days_year 
        self.exchange_rate =  date_based_data.exchange_rate 

        #these are from OB page
        self.output_100per = date_based_data.output_100per
        self.total_sams = date_based_data.total_sams
        self.total_sewing_sams = date_based_data.total_sewing_sams

        #hifashion
        #this below llines are for temporary
        self.hi_fashion_y1 =  int(date_based_data.hi_fashion_y1) 
        self.hi_fashion_y2 =  int(date_based_data.hi_fashion_y2) 
        self.hi_fashion_y3 =  int(date_based_data.hi_fashion_y3) 
        '''
        #This is the actual menthod of fetching data from that particular element from DB
        self.hi_fash_list=[]
        for j in hi_fashion:
            self.hi_fash_list.append(j)
        '''
        self.hi_fash_list = [self.hi_fashion_y1,self.hi_fashion_y2,self.hi_fashion_y3]
        #final_productive_factor #temporary
        self.final_productive_factor_y1 =  float(date_based_data.final_productive_factor_y1) 
        self.final_productive_factor_y2 =  float(date_based_data.final_productive_factor_y2) 
        self.final_productive_factor_y3 =  float(date_based_data.final_productive_factor_y3) 
        '''
        self.fpf_list=[]
        for j in final_productive_factor_y:
            self.fpf_list.append(j)
        '''
        self.fpf_list = [self.final_productive_factor_y1,self.final_productive_factor_y2,self.final_productive_factor_y3]
        #hi_fashion
        self.hi_fashion_subtotal =  float(date_based_data.hi_fashion_subtotal) 
        self.hi_fashion_checkingtable = float(date_based_data.hi_fashion_checkingtable) 
        self.hi_fashion_helpertable =  float(date_based_data.hi_fashion_helpertable) 
        self.hi_fashion_irontable =  float(date_based_data.hi_fashion_irontable) 
        self.hi_fashion_manual =  float(date_based_data.hi_fashion_manual)
        
        #total_direct_expenses #temporary
        self.total_direct_expenses_y1 =  float(date_based_data.total_direct_expenses_y1) 
        self.total_direct_expenses_y2 =  float(date_based_data.total_direct_expenses_y2) 
        self.total_direct_expenses_y3 =  float(date_based_data.total_direct_expenses_y3) 
        
        self.TDE_list = [self.total_direct_expenses_y1,self.total_direct_expenses_y2,self.total_direct_expenses_y3]
        #total_indirect_expenses #temporary
        self.total_indirect_expenses_y1 =  float(date_based_data.total_indirect_expenses_y1) 
        self.total_indirect_expenses_y2 =  float(date_based_data.total_indirect_expenses_y2) 
        self.total_indirect_expenses_y3 =  float(date_based_data.total_indirect_expenses_y3) 

        self.TIE_list = [self.total_indirect_expenses_y1,self.total_indirect_expenses_y2,self.total_indirect_expenses_y3]
        #gross_operating_profit #temporary
        self.gross_operating_profit_y1 =  float(date_based_data.gross_operating_profit_y1) 
        self.gross_operating_profit_y2 =  float(date_based_data.gross_operating_profit_y2) 
        self.gross_operating_profit_y3 =  float(date_based_data.gross_operating_profit_y3)

        self.GOP_list=[self.gross_operating_profit_y1,self.gross_operating_profit_y2,self.gross_operating_profit_y3] 
        #PBT_y1 #temporary
        self.PBT_y1 =  float(date_based_data.PBT_y1) 
        self.PBT_y2 =  float(date_based_data.PBT_y2) 
        self.PBT_y3 =  float(date_based_data.PBT_y3) 

        self.PBT_list=[self.PBT_y1,self.PBT_y2,self.PBT_y3]
        #income_tax #temp
        self.income_tax_y1  = float(date_based_data.income_tax_y1)
        self.income_tax_y2  = float(date_based_data.income_tax_y2) 
        self.income_tax_y3 =  float(date_based_data.income_tax_y3) 
        
        self.income_tax_list = [self.income_tax_y1,self.income_tax_y2,self.income_tax_y3]
        #PAT #temp
        self.PAT_y1 =  float(date_based_data.PAT_y1) 
        self.PAT_y2 =  float(date_based_data.PAT_y2) 
        self.PAT_y3 =  float(date_based_data.PAT_y3) 

        self.PAT_list = [self.PAT_y1,self.PAT_y2,self.PAT_y3]
        #FOB 
        self.FOB_y1 =  float(date_based_data.FOB_y1) 
        self.FOB_y2 = float(date_based_data.FOB_y2) 
        self.FOB_y3 = float(date_based_data.FOB_y3) 

        self.FOB_list=[self.FOB_y1,self.FOB_y2,self.FOB_y3]

        #--------------------------------------------------------------------------------------------------------------------------------------------
        #actual calculations stared here

        self.hi_fash_noofcheckers = self.hi_fashion_subtotal+self.hi_fashion_irontable+self.hi_fashion_manual
        self.no_of_mach_running=[self.hi_fashion_subtotal*digit for digit in self.hi_fash_list]
        self.fpflist_perc_2_no = [digit/100 for digit in self.fpf_list]
        self.pro_op100per_machrunning=[self.output_100per*digit for digit in self.fpflist_perc_2_no]
        self.daily_production=[]
        for i,j in zip(self.no_of_mach_running,self.pro_op100per_machrunning):
            self.daily_production.append(j*i)
        
        self.total_annual_production_list = [(8*self.no_of_production_days_year*digit)/12 for digit in self.daily_production]

        #total_sewing_sams
        self.total_sewing_sams_earned = [ self.total_sewing_sams*digit for digit in self.total_annual_production_list]
        self.total_sams_earned = [ self.total_sams*digit for digit in self.total_annual_production_list]

        #revenue row
        self.dollar_2_inr=[ self.exchange_rate*digit for digit in self.FOB_list]
        self.revenue = []
        for i,j in zip(self.dollar_2_inr,self.total_annual_production_list):
            self.revenue.append(i*j)
        
        self.total_revenue_million = [digit/10**6 for digit in self.revenue]

        #last table

        self.variable_costs=[]

        for i,j in zip(self.TIE_list,self.total_annual_production_list):
            self.variable_costs.append((i*10**6)/j)

        
        self.FOB_list_X_exchangerate = [digit*self.exchange_rate for digit in self.FOB_list]
        self.unit_economics=[] 
        for i,j in zip(self.variable_costs,self.FOB_list_X_exchangerate):
            self.unit_economics.append(j-i)


        #sales revenue at unit level

        self.sales_revenue_unit_level = []
        for i,j in zip(self.total_revenue_million,self.total_annual_production_list):
            self.sales_revenue_unit_level.append((i/j)*(10**6))
        
        #fixed unit cost
        self.fixed_unit_costs = []
        for i,j in zip(self.TDE_list,self.total_annual_production_list):
            self.fixed_unit_costs.append((i*(10**6))/j)
        
        #Unit contribution 
        self.unit_contribution = []
        for i,j in zip(self.sales_revenue_unit_level,self.variable_costs):
            self.unit_contribution.append(i-j)
        
        #Fixed corporate cost
        self.fixed_corp_costs = []
        for i,j in zip(self.income_tax_list,self.total_annual_production_list):
            self.fixed_corp_costs.append((i*(10**6))/j)
        
        #Gross profit PBDIT
        self.gross_profit_PBDIT = []
        for i,j in zip(self.GOP_list,self.total_annual_production_list):
            self.gross_profit_PBDIT.append((i*(10**6))/j)
        #Gross profit PBT
        self.gross_profit_PBT = []
        for i,j in zip(self.PBT_list,self.total_annual_production_list):
            self.gross_profit_PBT.append((i*(10**6))/j)

        #Gross profit PAT
        self.gross_profit_PAT = []
        for i,j in zip(self.PAT_list,self.total_annual_production_list):
            self.gross_profit_PAT.append((i*(10**6))/j)


        
