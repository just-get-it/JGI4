from django.db import models
from nutrition.models import Nutrition_table
from django.urls import reverse

class NutritionModel(models.Model):
    Product = models.CharField(max_length=30, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True)
    Unit = models.CharField(max_length=30, null=True, blank=True)
    Kcal = models.IntegerField(null=True, blank=True)
    Protein = models.IntegerField(null=True, blank=True)
    Carbs = models.IntegerField(null=True, blank=True)
    Fat = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.Product

class diet(models.Model):
    diet_sr= models.IntegerField( null=True, blank=True)
    diet_day= models.IntegerField( null=True, blank=True)
    diet_time= models.IntegerField( null=True, blank=True)
    copy= models.FloatField(null=True, blank=True)
    Product= models.CharField(max_length=30, null=True, blank=True)
    type= models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.Product

    def get_absolute_url(self):
        return reverse('updt_diet1')

class diet_detail(models.Model):
    diet_sr= models.CharField(max_length=30, null=True, blank=True)
    type= models.CharField(max_length=30, null=True, blank=True,default='nonveg')
    regio= models.CharField(max_length=30, null=True, blank=True,default='north')
    seaso= models.CharField(max_length=30, null=True, blank=True,default='all')
    t_periods= models.CharField(max_length=30, null=True, blank=True,default=3)
    disease= models.CharField(max_length=30, null=True, blank=True,default='None')
    state= models.CharField(max_length=30, null=True, blank=True,default='Normal')
    Kcal = models.FloatField(null=True, blank=True,default=0)
    Protein = models.FloatField(null=True, blank=True,default=0)
    Fat = models.FloatField(null=True, blank=True,default=0)
    Carbs = models.FloatField(null=True, blank=True,default=0)
    Water = models.FloatField(null=True, blank=True,default=0)
    Vit_A_IU = models.FloatField(null=True, blank=True,default=0)
    Vit_C = models.FloatField(null=True, blank=True,default=0)
    Vit_D = models.FloatField(null=True, blank=True,default=0)
    sodium = models.FloatField(null=True, blank=True,default=0)
    Potassium = models.FloatField(null=True, blank=True,default=0)
    Calcium = models.FloatField(null=True, blank=True,default=0)
    Phosphorus = models.FloatField(null=True, blank=True,default=0)
    Magnesium = models.FloatField(null=True, blank=True,default=0)
    Iron = models.FloatField(null=True, blank=True,default=0)
    Zinc = models.FloatField(null=True, blank=True,default=0)



    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('updt_diet2')

class Nutrition_item(models.Model):
    Product = models.CharField(max_length=80, null=True, blank=True)
    region = models.CharField(max_length=100,default="north")
    type = models.CharField(max_length=100,default="nonveg")
    season = models.CharField(max_length=100,default="all")
    Kcal = models.FloatField(null=True, blank=True,default=0)
    Protein = models.FloatField(null=True, blank=True,default=0)
    Fat = models.FloatField(null=True, blank=True,default=0)
    Carbs = models.FloatField(null=True, blank=True,default=0)
    T_sat_fat = models.FloatField(null=True, blank=True,default=0)
    T_umo_fat = models.FloatField(null=True, blank=True,default=0)
    T_upo_fat = models.FloatField(null=True, blank=True,default=0)
    choles = models.FloatField(null=True, blank=True,default=0)
    sodium = models.FloatField(null=True, blank=True,default=0)
    T_fi = models.FloatField(null=True, blank=True,default=0)
    Vit_A_Re = models.FloatField(null=True, blank=True,default=0)
    Vit_A_IU = models.FloatField(null=True, blank=True,default=0)
    alpha_toco= models.FloatField(null=True, blank=True,default=0)
    ascor= models.FloatField(null=True, blank=True,default=0)
    thiami= models.FloatField(null=True, blank=True,default=0)
    iaci= models.FloatField(null=True, blank=True,default=0)
    Vit_B6 = models.FloatField(null=True, blank=True,default=0)
    folaci = models.FloatField(null=True, blank=True,default=0)
    #Vit_B9 = models.FloatField(null=True, blank=True,default=0)
    Vit_B12 = models.FloatField(null=True, blank=True,default=0)
    Potassium = models.FloatField(null=True, blank=True,default=0)
    Calcium = models.FloatField(null=True, blank=True,default=0)
    Phosphorus = models.FloatField(null=True, blank=True,default=0)
    Magnesium = models.FloatField(null=True, blank=True,default=0)
    Iron = models.FloatField(null=True, blank=True,default=0)
    Zinc = models.FloatField(null=True, blank=True,default=0)
    Pantothenic_acid = models.FloatField(null=True, blank=True,default=0)
    Copper = models.FloatField(null=True, blank=True,default=0)
    Manganese = models.FloatField(null=True, blank=True,default=0)
    Ash = models.FloatField(null=True, blank=True,default=0)
    Water = models.FloatField(null=True, blank=True,default=0)
    energy_kJ = models.FloatField(null=True, blank=True,default=0)
    #Selenium = models.FloatField(null=True, blank=True,default=0)
    #Sodium = models.FloatField(null=True, blank=True,default=0)
    Caprylic_Acid= models.FloatField(null=True, blank=True,default=0)
    Capric_Acid= models.FloatField(null=True, blank=True,default=0)
    Lauric_Acid= models.FloatField(null=True, blank=True,default=0)
    Myristic_Acid= models.FloatField(null=True, blank=True,default=0)
    Palmitic_Acid= models.FloatField(null=True, blank=True,default=0)
    Palmitoleic_Acid= models.FloatField(null=True, blank=True,default=0)
    Stearic_Acid= models.FloatField(null=True, blank=True,default=0)
    Oleic_Acid= models.FloatField(null=True, blank=True,default=0)
    Linoleic_acid= models.FloatField(null=True, blank=True,default=0)
    Linolenic_acid = models.FloatField(null=True, blank=True,default=0)
    Gadoleic_acid = models.FloatField(null=True, blank=True,default=0)
    Docosenoic_acid = models.FloatField(max_length=30, null=True, blank=True,default=0)
    Phytosterols=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Histidine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Isoleucine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Leucine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Lysine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Methionine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Cystine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Methionine_Cystine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Phenylalanine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Tyrosine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Phenylalanine_Tyrosine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Threonine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Tryptophan=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Valine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Arginine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Alanine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Aspartic_acid=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Glutamic_acid=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Glycine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Proline=models.FloatField(max_length=30, null=True, blank=True,default=0)
    Serine=models.FloatField(max_length=30, null=True, blank=True,default=0)
    # Vit_B1 = models.FloatField(null=True, blank=True,default=0)
    # Vit_B2 = models.FloatField(null=True, blank=True,default=0)
    # Vit_B3 = models.FloatField(null=True, blank=True,default=0)
    # Vit_B5 = models.FloatField(null=True, blank=True,default=0)
    Vit_C = models.FloatField(null=True, blank=True,default=0)
    Vit_D = models.FloatField(null=True, blank=True,default=0)
    # Vit_E = models.FloatField(null=True, blank=True,default=0)
    # Vit_K = models.FloatField(null=True, blank=True,default=0)
    #urls = models.FloatField(null=True, blank=True,default=0)
    
    def __str__(self):
        return self.Product

class ml(models.Model):
    wt = models.IntegerField(null=True, blank=True)
    mi = models.FloatField(null=True, blank=True)
    ac = models.IntegerField(null=True, blank=True)  #active
    pr = models.FloatField(null=True, blank=True) #protei required

class memo(models.Model):
    sr = models.IntegerField(null=True, blank=True)
    d = models.IntegerField(null=True, blank=True)
    mi = models.CharField(max_length=80, null=True, blank=True)
    ac = models.CharField(max_length=80, null=True, blank=True)  #active
    pr = models.CharField(max_length=80, null=True, blank=True) #protei required

#gen,age,height,weight,bodyfat,bodyphy,exercise,activity,blood_pressure,sugar,blood_group,food_habbit,food_preference,disability,
#medical_issues,diseases

class memo1(models.Model):
    d = models.IntegerField(null=True, blank=True)
    gen= models.CharField(max_length=80, null=True, blank=True)
    age= models.CharField(max_length=80, null=True, blank=True)
    height= models.CharField(max_length=80, null=True, blank=True)
    weight= models.FloatField(max_length=80, null=True, blank=True)
    bodyfat= models.CharField(max_length=80, null=True, blank=True)
    bodyphy= models.CharField(max_length=80, null=True, blank=True)
    exercise= models.CharField(max_length=80, null=True, blank=True)
    activity= models.CharField(max_length=80, null=True, blank=True)
    blood_pressure= models.CharField(max_length=80, null=True, blank=True)
    sugar= models.CharField(max_length=80, null=True, blank=True)
    blood_group= models.CharField(max_length=80, null=True, blank=True)
    food_habbit= models.CharField(max_length=80, null=True, blank=True)
    food_preference= models.CharField(max_length=80, null=True, blank=True)
    disability= models.CharField(max_length=80, null=True, blank=True)
    medical_issues= models.CharField(max_length=80, null=True, blank=True)
    diseases= models.CharField(max_length=80, null=True, blank=True)
    
class memo2(models.Model):
    d = models.IntegerField(null=True, blank=True)
    bmi=models.CharField(max_length=80, null=True, blank=True)
    lean_body_mass=models.CharField(max_length=80, null=True, blank=True)
    basal_metabolic_rate=models.CharField(max_length=80, null=True, blank=True)
    maintaince=models.CharField(max_length=80, null=True, blank=True)
    lean_bmi=models.CharField(max_length=80, null=True, blank=True)
    
class memo3(models.Model):
    d=models.IntegerField(null=True, blank=True)
    protein_in_gr=models.CharField(max_length=80, null=True, blank=True)
    carbs_in_gr=models.CharField(max_length=80, null=True, blank=True)
    fat_in_gr=models.CharField(max_length=80, null=True, blank=True)