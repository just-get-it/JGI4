from django.db import models

# Create your models here.

class capacity_revenue_table(models.Model):
    #there are all the temporary values and table for testing purpose only
    output_date = models.DateField()
    no_of_years=models.IntegerField(default=0)
    no_of_wrkng_days_month = models.IntegerField(default=0)
    no_of_production_days_year = models.IntegerField(default=0)
    exchange_rate = models.FloatField(default=0)

    #these are from OB page
    output_100per = models.FloatField(default=0)
    total_sams = models.FloatField(default=76.05)
    total_sewing_sams = models.FloatField(default=0)
    
    #these are from Assumptions page
    hi_fashion_y1 = models.FloatField(default=0)
    hi_fashion_y2 = models.FloatField(default=0)
    hi_fashion_y3 = models.FloatField(default=0)
    
    final_productive_factor_y1 = models.FloatField(default=0)
    final_productive_factor_y2 = models.FloatField(default=0)
    final_productive_factor_y3 = models.FloatField(default=0)
     
    #these are for sewing summary
    hi_fashion_subtotal = models.FloatField(default=0)
    hi_fashion_checkingtable = models.FloatField(default=0)
    hi_fashion_helpertable = models.FloatField(default=0)
    hi_fashion_irontable = models.FloatField(default=0)
    hi_fashion_manual = models.FloatField(default=0)
    
    total_direct_expenses_y1 = models.FloatField(default=0)
    total_direct_expenses_y2 = models.FloatField(default=0)
    total_direct_expenses_y3 = models.FloatField(default=0)
    
    total_indirect_expenses_y1 = models.FloatField(default=0)
    total_indirect_expenses_y2 = models.FloatField(default=0)
    total_indirect_expenses_y3 = models.FloatField(default=0)
    
    gross_operating_profit_y1 = models.FloatField(default=0)
    gross_operating_profit_y2 = models.FloatField(default=0)
    gross_operating_profit_y3 = models.FloatField(default=0)
    
    PBT_y1 = models.FloatField(default=0)
    PBT_y2 = models.FloatField(default=0)
    PBT_y3 = models.FloatField(default=0)
    
    income_tax_y1= models.FloatField(default=0)
    income_tax_y2 = models.FloatField(default=0)
    income_tax_y3 = models.FloatField(default=0)
    
    PAT_y1 = models.FloatField(default=0)
    PAT_y2 = models.FloatField(default=0)
    PAT_y3 = models.FloatField(default=0)

    FOB_y1 = models.FloatField(default=0)
    FOB_y2 = models.FloatField(default=0)
    FOB_y3 = models.FloatField(default=0)
